document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('message-container');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
});