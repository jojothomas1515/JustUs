export async function sendFriendRequest(user_id: string) {
    const res = await fetch(`/users/friends/${user_id}`, {method: "POST"})
    if (res.status === 201) {
        alert("Friend request sent!");
        const data = await res.json();
        console.log(data);
    }const data = await res.json();
        console.log(data);

}
export async function acceptFriendRequest(user_id: string) {
    const res = await fetch(`/users/friends/${user_id}`, {method: "PUT"})
    if (res.status === 201) {
        alert("Friend request sent!");
        const data = await res.json();
        console.log(data);
    }const data = await res.json();
        console.log(data);

}