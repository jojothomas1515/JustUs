"use strict";
const messagesBox = document.querySelector(".messages");
const messageInput = document.querySelector("#message-input");
const sendBtn = document.querySelector("#send");
const newConvoBtn = document.querySelector("#new-convo");
const friendProf = document.querySelector(".profile-info");
// @ts-ignore
const sio = io();
sio.addEventListener("message", (data) => {
    const message = document.createElement("div");
    message.className = "message";
    message.classList.add("friend-message");
    console.log(JSON.parse(data));
    message.textContent = JSON.parse(data).message;
    messagesBox.appendChild(message);
    messagesBox.scrollTop = messagesBox.scrollHeight;
});
sendBtn.addEventListener('click', () => {
    const message = document.createElement("div");
    message.className = "message";
    message.classList.add("me");
    const content = messageInput.value;
    message.textContent = content;
    messagesBox.appendChild(message);
    messagesBox.scrollTop = messagesBox.scrollHeight;
    messageInput.value = "";
    sio.emit("message", JSON.stringify({ id: friendProf.getAttribute("data-userId"), message: content }));
});
messageInput.addEventListener("keydown", (evt) => {
    if (evt.key === "Enter")
        sendBtn.click();
});
// todo: delete this
async function get_users() {
    const res = await fetch("/users/friends", { method: "GET" });
    const data = await res.json();
    return data;
}
async function setMessages(user_id) {
    messagesBox.innerHTML = "";
    const friend_id = friendProf.getAttribute("data-userId");
    const response = await fetch(`/chats/messages/${user_id || friend_id}`);
    const messages = await response.json();
    messages.forEach((mesg) => {
        const message = document.createElement("div");
        message.className = "message";
        if (friend_id == mesg.sender_id)
            message.classList.add("friend-message");
        else
            message.classList.add("me");
        message.textContent = mesg.message;
        messagesBox.appendChild(message);
    });
    messagesBox.scrollTop = messagesBox.scrollHeight;
}
