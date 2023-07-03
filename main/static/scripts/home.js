import { acceptFriendRequest, sendFriendRequest } from "./utilities.js";
// @ts-ignore
const sio = io();
sio.addEventListener("message", (data) => {
    const res = JSON.parse(data);
    const notification = new Notification(`New message from ${res.sender.email}`, {
        body: res.message, requireInteraction: true, icon: "/static/logos/justus-logo-bowb.png",
    });
    notification.addEventListener("click", () => {
        location.href = `/chats/${res.sender.id}`;
    });
    notification.addEventListener("close", () => {
    });
});
const friendsList = document.querySelector("#accepted-users");
const requestsList = document.querySelector("#pending-users");
const usersList = document.querySelector("#all-users");
const updateProfile = document.querySelector("#update-profile-btn");
const closeUpdateProfile = document.querySelector("#close-update-profile-btn");
const updateProfileModal = document.querySelector(".update_profile");
updateProfile.addEventListener("click", () => {
    console.log("clicked");
    updateProfileModal.style.display = "block";
});
closeUpdateProfile.addEventListener("click", () => {
    console.log("clicked");
    updateProfileModal.style.display = "none";
});
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
        profImg.src = user.data.profile_img || "/images/logos/justus-logo-bnb.png";
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
    data.forEach((user) => {
        const friend = document.createElement("div");
        friend.className = "users";
        const profImg = document.createElement("img");
        profImg.src = user.profile_img || "/images/logos/justus-logo-bnb.png";
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
loadAllUsers().catch(err => console.log(err));
loadFriends().catch(err => console.log(err));
try {
    if (Notification.permission === "granted") {
        console.log("can show notification");
    }
    else if (Notification.permission !== "denied") {
        Notification.requestPermission();
    }
}
catch (e) {
    console.log(e);
}
