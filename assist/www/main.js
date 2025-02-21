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
});