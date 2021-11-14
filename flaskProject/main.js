function getResult() {

    var url = "http://localhost:5000";   // The URL and the port number must match server-side
    var endpoint = "/inputMessage";            // Endpoint must match server endpoint

    var http = new XMLHttpRequest();

    var textput = document.getElementById( 'yerr' ).value;
    // document.getElementById("result").innerHTML = textput;
    var payloadObj = { "message" : textput };
    var obj = JSON.stringify( payloadObj );
    // prepare GET request
    http.open( "POST", url+endpoint, true );
    http.setRequestHeader( "Content-Type", "application/json" )

    http.onreadystatechange = function() {
        var DONE = 4;       // 4 means the request is done.
        var OK = 200;       // 200 means a successful return.
        if (http.readyState == DONE && http.status == OK && http.responseText) {

            // JSON string
            var replyString = http.responseText;
            var text = JSON.parse(replyString)

            document.getElementById("result").innerHTML = "<h2> Heres the Tweets Text:</h2><br> " + text['tweet'];
            document.getElementById("result").innerHTML += "<br>";
            document.getElementById("result").innerHTML += "<h2>The Text Sentiment is:</h2><br>" + text['sentiment'];
        }
    };

    // Send request
    http.send(obj);
}