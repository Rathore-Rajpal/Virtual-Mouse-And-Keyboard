$(document).ready(function () {
    $('.text').textillate({
        loop: true,
        sync: requestAnimationFrame,
        in:{
            effect: "bounceIn",
        },
        out:{
            effect: "bounceOut",
        },
    })

    //siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 880,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autoStart: true
      });

      //siri message animation
      $('.siri-message').textillate({
        loop: true,
        sync: requestAnimationFrame,
        in:{
            effect: "fadeInUp",
            sync: true,
        },
        out:{
            effect: "fadeOutUp",
            sync: true,
        },
    })

    //mic button click event

    $("#MicBtn").click(function (e) { 
        eel.playMicSound()
        $("#oval").attr("hidden",true);
        $("#siriwave").attr("hidden",false);
        eel.allCommands()
    });

    function doc_keyUp(e) {
        if (e.key == 'j' && e.altKey) { // Alt + j
            eel.playMicSound();
            $("#oval").attr("hidden", true);
            $("#siriwave").attr("hidden", false);
            eel.allCommands();
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    function PlayAssistant(message) {

        if (message != "") {

            $("#oval").attr("hidden", true);
            $("#siriwave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });

     $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });

    $("#GoBackBtn").click(function () {
        eel.stopProcess();  // Replace with the actual function that stops the current assistant process

        // Switch sections
        $("#siriwave").attr("hidden", true);
        $("#oval").attr("hidden", false);
    });
    

});