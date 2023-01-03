function buildTable() {

    var attributes = JSON.parse(responseText);

    var table = document.getElementById("tbl");
    var titles = document.createElement("tr");
    table.appendChild(titles);
    var t1 = document.createElement("th");
    titles.appendChild(t1);
    t1.innerHTML = "comments";
    titles.style.fontSize = "30px";
    titles.style.fontFamily = "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif";
    titles.style.textAlign = "center";
    for (var i = 0; i < attributes.length; i++) {
        var tr1 = document.createElement("tr");
        var td1 = document.createElement("td");
        table.appendChild(tr1);
        tr1.appendChild(td1);

        tr1.style.fontSize = "30px";
        tr1.style.textAlign = "center";

        //tr1.style.fontFamily = "'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif";
        tr1.style.fontFamily = "'Segoe UI'";
        var link = document.createElement("a");
        td1.appendChild(link);

    }
}