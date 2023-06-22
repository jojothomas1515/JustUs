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
newConvoBtn.addEventListener("click", async () => {
    const modal = document.createElement("div");
    // adding close button to the modal
    const closeBtn = document.createElement("button");
    closeBtn.className = "close-btn";
    closeBtn.innerHTML = "X";
    closeBtn.addEventListener("click", () => {
        modal.parentElement.removeChild(modal);
    });
    modal.appendChild(closeBtn);
    modal.className = "new-convo-modal";
    // getting all friends
    const data = await get_users();
    data.forEach(item => {
        const friends = document.createElement("div");
        friends.setAttribute("data-userId", item.data.id);
        friends.addEventListener('click', () => {
            friendProf.setAttribute("data-userId", item.data.id);
            friendProf.lastElementChild.textContent = item.data.first_name.concat(" ", item.data.last_name);
            closeBtn.click();
        });
        friends.className = 'friends';
        friends.innerHTML = `<h4>${item.data.first_name} ${item.data.last_name}</h4>`;
        modal.appendChild(friends);
    });
    document.querySelector(".chats-menu").appendChild(modal);
});
