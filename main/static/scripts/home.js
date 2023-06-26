"use strict";
const friendsList = document.querySelector("#accepted-users");
const requestsList = document.querySelector("#pending-users");
async function loadFriends() {
    const res = await fetch("/users/friends");
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
        if (user.status === "accepted")
            friendsList.appendChild(friend);
        else if (user.status === "pending") {
            const accept = document.createElement("button");
            const reject = document.createElement("button");
            accept.className = "accept";
            reject.className = "reject";
            accept.innerHTML = "<i class='fa fa-check'></i>";
            reject.innerHTML = "<i class='fa fa-close'></i>";
            friend.append(reject, accept);
            requestsList.appendChild(friend);
        }
    });
}
loadFriends();
