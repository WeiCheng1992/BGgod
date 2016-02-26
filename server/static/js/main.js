$(document).ready(function(){
    namespace = ""; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect("http://" + document.domain + ':' + location.port);
    socket.on("connect", function() {

        socket.emit("join_user");



    });

    socket.on("new_user", function(msg) {
        if (document.getElementById("username").innerHTML != msg["user"]) {
            $("#users").append("<span>"+msg["user"]+"</span>");
        }
    });

    socket.on("message", function(msg) {
        document.getElementById("dial").innerHTML += "\n" + msg;
    });


    $("form#input").submit(function(event) {
        var input = document.getElementById("input_content").value ;
        document.getElementById("input_content").value = "" ;

        document.getElementById("dial").innerHTML += "\n" + input;
        socket.send(input);
        return false;
    });
});