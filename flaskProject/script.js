function getResult() {

    var url = "http://localhost:8000";   // The URL and the port number must match server-side
    var endpoint = "/result";            // Endpoint must match server endpoint

    var http = new XMLHttpRequest();
    var textput = document.getElementById('yerr').value;
    document.getElementById("result").innerHTML = textput;
    // prepare GET request
    http.open("GET", url+endpoint, true);

    http.onreadystatechange = function() {
        var DONE = 4;       // 4 means the request is done.
        var OK = 200;       // 200 means a successful return.
        if (http.readyState == DONE && http.status == OK && http.responseText) {

            // JSON string
            var replyString = http.responseText;

            document.getElementById("result").innerHTML = "<h2>Here is the result</h2><br> JSON received: " + replyString;
            document.getElementById("result").innerHTML += "<br>";

            // convert JSON string into JavaScript object and get the scores

        }
    };

    // Send request
    http.send();
}