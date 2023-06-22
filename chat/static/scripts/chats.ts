const messagesBox: HTMLDivElement = document.querySelector(".messages") as HTMLDivElement;
const messageInput: HTMLInputElement = document.querySelector("#message-input") as HTMLInputElement;
const sendBtn: HTMLButtonElement = document.querySelector("#send") as HTMLButtonElement;
const newConvoBtn: HTMLButtonElement = document.querySelector("#new-convo") as HTMLButtonElement;
const friendProf: HTMLDivElement = document.querySelector(".profile-info") as HTMLDivElement;

// @ts-ignore
const sio = io();

sio.addEventListener("message", (data: any) => {
    const message: HTMLDivElement = document.createElement("div");
    message.className = "message";
    message.classList.add("friend-message");
    message.textContent = JSON.parse(data).message;

    messagesBox.appendChild(message);
    messagesBox.scrollTop = messagesBox.scrollHeight;

});

sendBtn.addEventListener('click', () => {
    const message: HTMLDivElement = document.createElement("div");
    message.className = "message";
    message.classList.add("me");
    const content: string = messageInput.value;
    message.textContent = content;
    messagesBox.appendChild(message);
    messagesBox.scrollTop = messagesBox.scrollHeight;
    messageInput.value = "";
    sio.emit("message", JSON.stringify({id: friendProf.getAttribute("data-userId"), message: content}));
});

messageInput.addEventListener("keydown", (evt) => {
    if (evt.key === "Enter") sendBtn.click();
});

// todo: delete this
async function get_users() {
    const res: Response = await fetch("/users/friends", {method: "GET"});
    const data = await res.json();
    return data;
}


interface Users {
    data: {
        id: string,
        email: string,
        first_name: string,
        last_name: string,
        middle_name: string | null,
        date: Date | null,
        is_active: boolean,
    },
    status: string
}

newConvoBtn.addEventListener("click", async () => {
    const modal = document.createElement("div") as HTMLDivElement;

    // adding close button to the modal
    const closeBtn = document.createElement("button");
    closeBtn.className = "close-btn";
    closeBtn.innerHTML = "X";
    closeBtn.addEventListener("click", () => {
        modal.parentElement!.removeChild(modal);
    });
    modal.appendChild(closeBtn);
    modal.className = "new-convo-modal";

    // getting all friends
    const data: Array<Users> = await get_users();
    data.forEach(item => {

        const friends = document.createElement("div");
        friends.setAttribute("data-userId", item.data.id);
        friends.addEventListener('click', () => {
            friendProf.setAttribute("data-userId", item.data.id);
            friendProf.lastElementChild!.textContent = item.data.first_name.concat(" ", item.data.last_name);
            closeBtn.click();
        });
        friends.className = 'friends';
        friends.innerHTML = `<h4>${item.data.first_name} ${item.data.last_name}</h4>`;
        modal.appendChild(friends);
    })

    document.querySelector(".chats-menu")!.appendChild(modal);
})

