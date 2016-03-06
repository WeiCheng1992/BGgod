$(document).ready(function(){
    namespace = ""; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect("http://" + document.domain + ':' + location.port);
    socket.emit("join_user");

    socket.on("connect", function() {

    });

    socket.on("greeting", function(msg) {
        document.getElementById("dial").innerHTML +=  "Welcome " + msg['username'] +
        "  id: " + msg['play_id'] +  "\n";
    });

    socket.on("message", function(msg) {
        document.getElementById("dial").innerHTML +=  msg + "\n";
    });


    socket.on("alert", function(msg) {
        alert(msg['msg']);
    });


    $("form#input").submit(function(event) {
        var input = document.getElementById("input_content").value ;
        document.getElementById("input_content").value = "" ;

        if(input != ""){
            document.getElementById("dial").innerHTML +=  input + "\n";
            socket.send(input);
        }
        return false;
    });


    $("form#begin").submit(function(event) {
        socket.emit("begin",room_id);
        return false;
    });
});


