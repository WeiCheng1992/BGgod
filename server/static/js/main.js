$(document).ready(function(){
    namespace = ""; // change to an empty string to use the global namespace

    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect("http://" + document.domain + ':' + location.port);
    socket.emit("join_user");

    socket.on("notice", function(msg) {
        document.getElementById("dial").innerHTML +=  msg['msg'] + "\n";
    });

    socket.on("deadnote", function(msg) {
        var dead = msg['id']
        if (dead == play_id){
            document.getElementById("dial").innerHTML +=  "You are killed!\n";
        }else{
            document.getElementById("dial").innerHTML +=  "No." + dead + "is killed!\n!";
        }
    });


    socket.on("alert", function(msg) {
        alert(msg['msg']);
    });



    socket.on("end",function(msg){
        socket.emit("leave_user",room_id, play_id);
        setTimeout(function(){
            window.location.assign("http://" + document.domain + ':' + location.port + "/index")
        },
        3000);
    });

    $("form#input").submit(function(event) {
        var input = document.getElementById("input_content").value ;
        document.getElementById("input_content").value = "" ;

        if(input != ""){
            document.getElementById("dial").innerHTML +=  input + "\n";
            socket.emit("msg",{'room_id': room_id , 'play_id': play_id,'msg' : input })
        }
        return false;
    });


    $("form#begin").submit(function(event) {
        socket.emit("begin",room_id);
        return false;
    });

    $("form#next").submit(function(event) {
        socket.emit("next",room_id);
        return false;
    });
});


