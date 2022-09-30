console.log("Sanity check from order_pk")

let chatSocket = null;
const orderId = JSON.parse(document.getElementById('orderId').textContent);
console.log(orderId)
function connect() {
    console.log(orderId)
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + orderId + "/");


    chatSocket.onopen = function (e) {
        console.log("Successfully connected to the WebSocket.");
    };
    chatSocket.onclose = function (e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function () {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);
    };
}
connect();