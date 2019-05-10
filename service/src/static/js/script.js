function reply_click(clicked_id) {
    makeAjaxRequest();
}

function getAll(clicked_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("allPlanets").innerHTML = this.responseText;
            // alert(this.responseText)
        }
    };
    xhttp.open("GET", "../getAll", true)
    xhttp.send();
}

function addPlanet(clicked_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert(this.responseText)
        }
    };
    xhttp.open("GET", "../addPlanet" +
        "?name=" + document.getElementById("name").value +
        "&declination=" + document.getElementById("declination").value +
        "&rightAscension=" + document.getElementById("rightAscension").value +
        "&flag=none"
        , true)
    xhttp.send();
}

function getPlanet(clicked_id) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            alert(this.responseText)
        }
    };
    xhttp.open("GET", "../getPlanet?declination=" + document.getElementById("declination2").value
        + "&rightAscension=" + document.getElementById("rightAscension2").value
        + "&ticket=" + document.getElementById("ticket").value
        + "&id=" + document.getElementById("planetId").value
        , true)
    xhttp.send();
}

function makeAjaxRequest() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("result").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "../directTelscopeTo/" + document.getElementById("angleInput").value, true);
    xhttp.send();
}