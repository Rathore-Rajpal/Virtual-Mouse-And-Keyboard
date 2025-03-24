
$(document).ready(function () {


    //Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {

        $(".siri-message li").text(message);
        $('.siri-message').textillate('start');

    }
    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#oval").attr("hidden", false);
        $("#siriwave").attr("hidden", true);
    }

    eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`;

            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    eel.expose(receiverText)
    function receiverText(message) {

        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`;

            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    }


    // Hide Loader and display Face Auth animation
    eel.expose(hideLoader)
    function hideLoader() {

        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", false);

    }
    // Hide Face auth and display Face Auth success animation
    eel.expose(hideFaceAuth)
    function hideFaceAuth() {

        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);

    }
    // Hide success and display 
    eel.expose(hideFaceAuthSuccess)
    function hideFaceAuthSuccess() {

        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);

    }


    // Hide Start Page and display blob
    eel.expose(hideStart)
    function hideStart() {

        $("#Start").attr("hidden", true);

        setTimeout(function () {
            $("#oval").addClass("animate__animated animate__zoomIn");

        }, 1000)
        setTimeout(function () {
            $("#oval").attr("hidden", false);
        }, 1000)
    }

    eel.expose(toggleEmailSection);

    function toggleEmailSection(show) {
        const emailSection = document.getElementById('emailSection');
        const bsOffcanvas = new bootstrap.Offcanvas(emailSection);

        if (show) {
            bsOffcanvas.show();
        } else {
            bsOffcanvas.hide();
        }
    }

    eel.expose(updateCodeContent);
    function updateCodeContent(code) {
        const codeSection = document.getElementById('codeSection');
        const codeElement = codeSection.querySelector('code');

        // Update code content
        codeElement.textContent = code;

        // Update line numbers
        const lineNumbers = code.split('\n')
            .map((_, i) => i + 1)
            .join('<br>');
        codeSection.querySelector('.line-numbers').innerHTML = lineNumbers;

        // Highlight syntax
        Prism.highlightAllUnder(codeSection);

        // Show section after content is updated
        setTimeout(() => {
            const bsOffcanvas = new bootstrap.Offcanvas(codeSection);
            bsOffcanvas.show();
        }, 100);
    }

    // Existing toggleCodeSection remains the same
    eel.expose(toggleCodeSection);
    function toggleCodeSection(show) {
        const codeSection = document.getElementById('codeSection');
        const bsOffcanvas = new bootstrap.Offcanvas(codeSection);
        show ? bsOffcanvas.show() : bsOffcanvas.hide();
    }

   // Add these functions to your existing JavaScript
eel.expose(showResponseSection);
function showResponseSection(initialContent) {
    const responseSection = document.getElementById('responseSection');
    const responseContent = document.querySelector('.response-content');
    
    // Show loading state
    responseContent.innerHTML = formatResponse(initialContent);
    responseContent.classList.add('loading');
    
    // Open the panel
    new bootstrap.Offcanvas(responseSection).show();
}

eel.expose(updateResponseContent);
function updateResponseContent(content) {
    const responseContent = document.querySelector('.response-content');
    responseContent.innerHTML = formatResponse(content);
    responseContent.classList.remove('loading');
    
    // Keep panel open
    const responseSection = document.getElementById('responseSection');
    if (!bootstrap.Offcanvas.getInstance(responseSection)) {
        new bootstrap.Offcanvas(responseSection).show();
    }
}



});
