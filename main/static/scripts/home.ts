const friendsList: HTMLDivElement = document.querySelector("#accepted-users") as HTMLDivElement;
const requestsList: HTMLDivElement = document.querySelector("#pending-users") as HTMLDivElement;

interface Friend {
    status: string,
    data: {
        id: string,
        first_name: string,
        last_name: string,
        middle_name: string,
        email: string,
        date_of_birth: string | null,
    }
}

async function loadFriends() {
    const res = await fetch("/users/friends");
    const data = await res.json();
    data.forEach((user: Friend) => {
        const friend:HTMLDivElement = document.createElement("div");
        friend.className = "users";
        const profImg: HTMLImageElement = document.createElement("img");
        profImg.src = "/images/logos/justus-logo-bnb.png"
        const infoCon: HTMLDivElement = document.createElement("div");
        const name:HTMLHeadingElement = document.createElement("h4");
        const email: HTMLParagraphElement = document.createElement("p");
        name.textContent = `${user.data.first_name} ${user.data.middle_name || ""} ${user.data.last_name}`;

        email.textContent = user.data.email;
        infoCon.append(name, email);
        friend.append(profImg, infoCon)
        if (user.status === "accepted") friendsList.appendChild(friend);
        else if (user.status === "pending") {
            const accept: HTMLButtonElement = document.createElement("button");
            const reject: HTMLButtonElement = document.createElement("button");
            accept.className = "accept";
            reject.className= "reject";
            accept.innerHTML = "<i class='fa fa-check'></i>";
            reject.innerHTML = "<i class='fa fa-close'></i>";
            friend.append(reject, accept);
            requestsList.appendChild(friend);
        }
    })
}

loadFriends();