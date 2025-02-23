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
});