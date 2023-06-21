"use strict";
const messagesBox = document.querySelector(".messages");
const messageInput = document.querySelector("#message-input");
const sendBtn = document.querySelector("#send");
// @ts-ignore
const sio = io();
sendBtn.addEventListener('click', () => {
    const message = document.createElement("div");
    message.className = "message";
    message.classList.add("me");
    const content = messageInput.value;
    message.textContent = content;
    messagesBox.appendChild(message);
    messagesBox.scrollTop = messagesBox.scrollHeight;
    messageInput.value = "";
    sio.emit("message", JSON.stringify({ message: content }));
});
messageInput.addEventListener("keydown", (evt) => {
    if (evt.key === "Enter")
        sendBtn.click();
});
// todo: delete this
async function get_users() {
    const res = await fetch("/users/friends", { method: "GET" });
    const data = await res.json();
    console.log(data);
}
setTimeout(get_users, 3000);
