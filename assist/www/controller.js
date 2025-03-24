
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

    eel.expose(toggleContactsSection);

    eel.expose(js_alert);
    async function js_alert(message) {
        return confirm(message); // Return true if "OK" is clicked, false if "Cancel"
    }

    // Expose function to update response content
    eel.expose(updateResponseContent);
    function updateResponseContent(response) {
        const responseSection = document.getElementById('responseSection');
        const responseElement = responseSection.querySelector('.response-content');

        // Format response with markdown-like styling
        const formattedResponse = formatResponse(response);
        responseElement.innerHTML = formattedResponse;

        // Show section after content is updated
        setTimeout(() => {
            const bsOffcanvas = new bootstrap.Offcanvas(responseSection);
            bsOffcanvas.show();
        }, 100);
    }

    // Format response text (basic markdown support)
    function formatResponse(text) {
        // Convert **bold** to <strong>
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Convert *italic* to <em>
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        // Convert `code` to <code>
        text = text.replace(/`(.*?)`/g, '<code>$1</code>');
        // Convert links
        text = text.replace(/https?:\/\/[^\s]+/g, '<a href="$&" target="_blank">$&</a>');
        // Convert newlines to <br>
        text = text.replace(/\n/g, '<br>');
        return text;
    }

    // Copy response to clipboard
    function copyResponse() {
        const responseElement = document.querySelector('.response-content');
        const text = responseElement.innerText;

        navigator.clipboard.writeText(text).then(() => {
            // Show toast notification
            const toast = new bootstrap.Toast(document.getElementById('responseToast'));
            toast.show();
        });
    }



});
