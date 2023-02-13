const comments = fetch("results/movie1.json")
.then(response => response.json())
.then(data=> appendData(data));


function appendData(comments) {
    console.log(comments);
	let mainContainer = document.getElementById("tbl");
	console.log(comments.length);
	//document.write("<table>");
	for (let i = 0; i < comments.length; i++) {
    	console.log("aaa");
		let table = document.getElementById("tbl");
        /*document.write("<tr>");
	    document.write("<td>");
		document.write(comments[i].comments);
    	document.write("</td>");
    	document.write("</tr>");
		/*var row = document.createElement("tr");
		var cell = document.createElement("td");
		cell.innerHTML = comments[i].comments
		row.appendChild(cell);
		table.appendChild(row);*/
    	table.innerHTML += "<tr>" + "<td>" + comments[i].comments + "</td>" + "</tr>";
		//mainContainer.appendChild(table);
		}
    //document.write("</table>");

}
function appendData11(){
    alert("12345");
}