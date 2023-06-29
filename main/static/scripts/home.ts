import {sendFriendRequest, acceptFriendRequest} from "./utilities.js";

const friendsList: HTMLDivElement = document.querySelector("#accepted-users") as HTMLDivElement;
const requestsList: HTMLDivElement = document.querySelector("#pending-users") as HTMLDivElement;
const usersList: HTMLDivElement = document.querySelector("#all-users") as HTMLDivElement;

interface User {

    id: string,
    first_name: string,
    last_name: string,
    middle_name: string,
    email: string,
    date_of_birth: string | null
}

interface Friend {
    status: string,
    requester_id: string,
    data: User,
}

async function loadFriends() {
    const res = await fetch("/users/friends");
    if (res.status === 200) {
        friendsList.innerHTML = ""
        requestsList.innerHTML = ""
    }
    const data = await res.json();
    data.forEach((user: Friend) => {
        const friend: HTMLDivElement = document.createElement("div");
        friend.className = "users";
        const profImg: HTMLImageElement = document.createElement("img");
        profImg.src = "/images/logos/justus-logo-bnb.png"
        const infoCon: HTMLDivElement = document.createElement("div");
        const name: HTMLHeadingElement = document.createElement("h4");
        const email: HTMLParagraphElement = document.createElement("p");
        name.textContent = `${user.data.first_name} ${user.data.middle_name || ""} ${user.data.last_name}`;

        email.textContent = user.data.email;
        infoCon.append(name, email);
        friend.append(profImg, infoCon)
        if (user.status === "accepted"){
            friendsList.appendChild(friend);
            const chat: HTMLButtonElement = document.createElement("button");
            chat.addEventListener("click", () => {
                window.location.href = `/chats/${user.data.id}`;
            });
            chat.className = "chat";
            chat.innerHTML = "<i class='fa fa-comment'></i>";
            friend.appendChild(chat);

        }  else if (user.status === "pending") {
            if (user.requester_id === user.data.id) {
                const accept: HTMLButtonElement = document.createElement("button");
                const reject: HTMLButtonElement = document.createElement("button");
                accept.addEventListener("click", () => {
                    acceptFriendRequest(user.data.id);
                    loadAllUsers();
                    loadFriends();
                });
                accept.className = "accept";
                reject.className = "reject";
                accept.innerHTML = "<i class='fa fa-check'></i>";
                reject.innerHTML = "<i class='fa fa-close'></i>";
                friend.append(accept, reject);
            } else {
                const sent: HTMLParagraphElement = document.createElement("p");
                sent.textContent = "Sent";
                sent.style.float = "right";
                friend.appendChild(sent);
            }
            requestsList.appendChild(friend);
        }
    })
}

async function loadAllUsers() {
    const res = await fetch("/users");
    if (res.status === 200) usersList.innerHTML = "";
    const data = await res.json();
    console.log(data);
    data.forEach((user: User) => {
        const friend: HTMLDivElement = document.createElement("div");
        friend.className = "users";
        const profImg: HTMLImageElement = document.createElement("img");
        profImg.src = "/images/logos/justus-logo-bnb.png"
        const infoCon: HTMLDivElement = document.createElement("div");
        const name: HTMLHeadingElement = document.createElement("h4");
        const email: HTMLParagraphElement = document.createElement("p");
        name.textContent = `${user.first_name} ${user.middle_name || ""} ${user.last_name}`;

        email.textContent = user.email;
        infoCon.append(name, email);
        friend.append(profImg, infoCon);
        const addFriend: HTMLButtonElement = document.createElement("button");
        addFriend.addEventListener("click", () => {
            sendFriendRequest(user.id);
            loadAllUsers();
            loadFriends();
        });
        addFriend.className = "add-friend";
        addFriend.innerHTML = "<i class='fa fa-user-plus'></i>";
        friend.append(addFriend);
        usersList.appendChild(friend);
    })
}

loadAllUsers();
loadFriends();