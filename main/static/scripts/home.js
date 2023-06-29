import { sendFriendRequest, acceptFriendRequest } from "./utilities.js";
const friendsList = document.querySelector("#accepted-users");
const requestsList = document.querySelector("#pending-users");
const usersList = document.querySelector("#all-users");
async function loadFriends() {
    const res = await fetch("/users/friends");
    if (res.status === 200) {
        friendsList.innerHTML = "";
        requestsList.innerHTML = "";
    }
    const data = await res.json();
    data.forEach((user) => {
        const friend = document.createElement("div");
        friend.className = "users";
        const profImg = document.createElement("img");
        profImg.src = "/images/logos/justus-logo-bnb.png";
        const infoCon = document.createElement("div");
        const name = document.createElement("h4");
        const email = document.createElement("p");
        name.textContent = `${user.data.first_name} ${user.data.middle_name || ""} ${user.data.last_name}`;
        email.textContent = user.data.email;
        infoCon.append(name, email);
        friend.append(profImg, infoCon);
        if (user.status === "accepted") {
            friendsList.appendChild(friend);
            const chat = document.createElement("button");
            chat.addEventListener("click", () => {
                window.location.href = `/chats/${user.data.id}`;
            });
            chat.className = "chat";
            chat.innerHTML = "<i class='fa fa-comment'></i>";
            friend.appendChild(chat);
        }
        else if (user.status === "pending") {
            if (user.requester_id === user.data.id) {
                const accept = document.createElement("button");
                const reject = document.createElement("button");
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
            }
            else {
                const sent = document.createElement("p");
                sent.textContent = "Sent";
                sent.style.float = "right";
                friend.appendChild(sent);
            }
            requestsList.appendChild(friend);
        }
    });
}
async function loadAllUsers() {
    const res = await fetch("/users");
    if (res.status === 200)
        usersList.innerHTML = "";
    const data = await res.json();
    console.log(data);
    data.forEach((user) => {
        const friend = document.createElement("div");
        friend.className = "users";
        const profImg = document.createElement("img");
        profImg.src = "/images/logos/justus-logo-bnb.png";
        const infoCon = document.createElement("div");
        const name = document.createElement("h4");
        const email = document.createElement("p");
        name.textContent = `${user.first_name} ${user.middle_name || ""} ${user.last_name}`;
        email.textContent = user.email;
        infoCon.append(name, email);
        friend.append(profImg, infoCon);
        const addFriend = document.createElement("button");
        addFriend.addEventListener("click", () => {
            sendFriendRequest(user.id);
            loadAllUsers();
            loadFriends();
        });
        addFriend.className = "add-friend";
        addFriend.innerHTML = "<i class='fa fa-user-plus'></i>";
        friend.append(addFriend);
        usersList.appendChild(friend);
    });
}
loadAllUsers();
loadFriends();
