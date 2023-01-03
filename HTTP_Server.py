import sys
import os
import socket
import re
from _thread import *
import module1

IP = '0.0.0.0'
PORT = 8080
SOCKET_TIMEOUT = 100
DEFAULT_DIR = 'WebRoot'  # Web root directory
REDIRECTION_DICTIONARY = {r'\index1.html':r'\movie1.html', r'\index2.html':r'\movie2.html', r'\index3.html':r'\movie3.html'}

def calculate_next_response(resource):
    """
    calculate the next successive number
    params: url
    extracts the number from url
    return: next successive number
    """
    # if there is no number parameter return 5 otherwise return the next succesive number

    num_index = resource.find('=')
    valid_parameters = num_index >= 0 and resource.find('?') >= 0
    sucessive_number = 5 if not valid_parameters else int(resource[num_index + 1:]) + 1
    successive_number_str = str(sucessive_number) + '\r\n'

    http_header = r'HTTP/1.1 200 OK' + '\r\n'
    http_header += 'Content-Length: ' + str(len(successive_number_str)) + '\r\n'
    http_header += r'Content-Type: text/plain' + '\r\n'
    http_header += '\r\n'
    calc_next_response = http_header + successive_number_str
    return calc_next_response

def read_file(file_path):
    """
    return file's content
    """
    file = open(file_path, 'rb')
    file_content = file.read()
    return file_content
    file.close()

def generate_http_packet_header(filetype, resource):
    file_size = os.path.getsize(DEFAULT_DIR + resource)
    http_header = r'HTTP/1.1 200 OK' + '\r\n'
    http_header += r'Content-Length: ' + str(file_size) + '\r\n'
    if filetype == 'html':
        http_header += r'Content-Type: ' + r'text/html' + '\r\n'
    elif filetype == 'jpg':
        http_header += r'Content-Type: ' + r'image/jpeg' + '\r\n'
    elif filetype == 'js':
        http_header += r'Content-Type: ' + r'text/javascript; charset=UTF-8' + '\r\n'
    elif filetype == 'css':
        http_header += r'Content-Type: ' + r'text/css' + '\r\n'
    else:
        print ("Illegal resource type")
    return http_header + '\r\n'


def handle_client_request(resource, client_socket):
    """Check the required resource, generate proper HTTP response and send to client"""
    http_response = ''
    print ("resource:  "  + resource)
    if (resource == '/' or resource == ''):
        required_resource = r'\index.html'
    else:
        required_resource = '\\'.join(resource.split('/'))
    print ("required_resource:  " + required_resource)
    # Checking if required_resource had been redirected, not available or other error codes.

    if required_resource in REDIRECTION_DICTIONARY:
        # Send 302 redirection response
        #http_header = r'HTTP/1.1 302 Moved Temporarily' + '\r\n'
        http_header = r'HTTP/1.1 302 Moved Temporarily' + '\r\n'
        http_header += 'Location: ' + REDIRECTION_DICTIONARY[required_resource] + '\r\n\r\n'
        print ('Sending 302 Moved Temporarily ...')
        client_socket.send(http_header.encode("utf-8"))
    elif required_resource == r'\forbidden_file.docx':
        # Send 403 response (Forbidden)
        http_header = r'HTTP/1.1 403 Forbidden' + '\r\n\r\n'
        print ('Sending 403 Forbidden ...')
        client_socket.send(http_header.encode("utf-8"))
    elif not(os.path.isfile(DEFAULT_DIR + required_resource)):
        # Send 404 response (File not found)
        http_header = r'HTTP/1.1 404 Not Found' + '\r\n\r\n'
        print ('Sending 404 Not Found ...')

        client_socket.send(http_header.encode("utf-8"))
    else:
        # Extract requested file type from URL (html, jpg etc)
        filetype = required_resource.split('.')[-1]
        http_header = generate_http_packet_header(filetype, required_resource)
        # Read the data from the file
        file_path = DEFAULT_DIR + required_resource
        body = read_file(file_path)

        http_response = http_header.encode("utf-8") + body

        print ("sending HTTP packet..." + str(os.path.getsize(file_path)))
        client_socket.send(http_response)

def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    #match = re.match('(GET)\s(.*)\s(HTTP/\d\.\d\r\n)',request)
    if re.match('(GET)\s(.*)\s(HTTP/\d\.\d\r\n)',request):
        match = re.match('(GET)\s(.*)\s(HTTP/\d\.\d\r\n)',request)
        type = re.match('(GET)\s(.*)\s(HTTP/\d\.\d\r\n)',request)
        type_cut = type.group(1).split("\s")
        return True,match.group(2),type_cut
    elif re.match('(POST)\s(.*)\s(HTTP/\d\.\d\r\n)',request):
        match = re.match('(POST)\s(.*)\s(HTTP/\d\.\d\r\n)', request)
        type = re.match('(POST)\s(.*)\s(HTTP/\d\.\d\r\n)',request)
        type_cut = type.group(1).split("\s")
        return True,match.group(2),type_cut
    else:
        return False,request, ""

def POST_client_request(client_request):
    x = client_request.split("\r\n")
    data = x[len(x) - 1]
    send = data.split("=")
    print(send[1])
    module1.DB(send[1])



def threaded_handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    while True:
        # Receiving client request
        try:
            print ('Wait for data recieve')
            client_request = client_socket.recv(1024).decode("utf-8")
            print(client_request)
        except:
            print ('Receive Time Out')
            break
        print (client_request.split())
        valid_http, resource, type = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            if str(type[0])== 'GET':
                handle_client_request(resource, client_socket)
            elif str(type[0])== 'POST':
                POST_client_request(client_request)
            else:
                continue
        else:
            print ('Error: Not a valid HTTP request')
            # Send 500 response (Internal Server Error)
            http_header = r'HTTP/1.1 500 Internal Server Error' + '\r\n\r\n'
            print ('Sending 500 Internal Server Error ...')
            client_socket.send(http_header.encode("utf-8"))
            break
    print ('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)

    while True:
        print ("Listening for connections on port %d" % PORT)
        client_socket, client_address = server_socket.accept()
        print ('New connection received:  ' + str(client_address))
        client_socket.settimeout(SOCKET_TIMEOUT)
        start_new_thread(threaded_handle_client, (client_socket,))


if __name__ == "__main__":
    # Call the main handler function
    main()
