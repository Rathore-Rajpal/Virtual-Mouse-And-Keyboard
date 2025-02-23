
$(document).ready(function () {


    //Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {

        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');

    }
    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#oval").attr("hidden", false);
        $("#siriwave").attr("hidden", true);
        console.log("show hood called")
    }


});