// Script for popup message displayed at top of the page

setTimeout(function () {
    let messages = document.getElementById('msg');
    let alert = new bootstrap.Alert(messages);
    alert.close();
}, 2500);
