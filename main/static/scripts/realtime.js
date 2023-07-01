"use strict";
const constraint = {
    'video': true, 'audio': true,
};
// function setCall(stream: MediaStream) {
//     navigator.mediaDevices.getUserMedia(constraint)
//         .then((stream) => {
//             const vid_box = document.createElement("video");
//             vid_box.style.width = "500px";
//             vid_box.style.height = "600px";
//             vid_box.style.position = "fixed";
//             vid_box.style.zIndex = "100";
//             vid_box.setAttribute("controls", "true")
//             vid_box.style.top = "0";
//             document.querySelector(".all-users")!.appendChild(vid_box);
//             vid_box.srcObject = stream;
//             vid_box.play()
//
//         }).catch(err => console.log(err))
// }
// @ts-ignore
const sio = io();
sio.addEventListener("signal", (data) => {
    const res = JSON.parse(data);
});
sio.addEventListener("answer", async (data) => {
    console.log("answer gotten");
});
const configuration = { 'iceServers': [{ 'urls': 'stun:stun.l.google.com:19302' }] };
async function placeCall() {
    const peerConnection = new RTCPeerConnection(configuration);
    sio.addEventListener("answer", async (data) => {
        const message = JSON.parse(data);
        console.log("answer");
        if (message.answer) {
            console.log(message.answer);
            const remoteSessDecs = new RTCSessionDescription(message.answer);
            console.log("i have gotten an answer");
            await peerConnection.setRemoteDescription(remoteSessDecs);
            peerConnection.addEventListener("connectionstatechange", (evt) => {
                if (peerConnection.connectionState === "connected") {
                    peerConnection.addEventListener('track', async (event) => {
                        const vid_box = document.createElement("video");
                        vid_box.style.width = "500px";
                        vid_box.style.height = "600px";
                        vid_box.style.position = "fixed";
                        vid_box.style.zIndex = "100";
                        vid_box.setAttribute("controls", "true");
                        vid_box.style.top = "0";
                        document.querySelector(".all-users").appendChild(vid_box);
                        const [remoteStream] = event.streams;
                        vid_box.srcObject = remoteStream;
                    });
                }
            });
        }
    });
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    sio.emit("offer", JSON.stringify({ id: "45b0f1b4-e77f-476c-b26d-475a4233dfa8", offer: offer }));
}
sio.addEventListener("offer", async (data) => {
    const res = JSON.parse(data);
    console.log("recieved");
    console.log(res.offer);
    await answerCall(res);
});
async function answerCall(res) {
    const peerConnection = new RTCPeerConnection(configuration);
    const offer = new RTCSessionDescription(res.offer);
    await peerConnection.setRemoteDescription(offer);
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);
    sio.emit("answer", JSON.stringify({ id: "3afc9e6e-99ed-4a70-9c6f-b1a1a4e7b725", answer: answer }));
    peerConnection.addEventListener("connectionstatechange", async (evt) => {
        if (peerConnection.connectionState === "connected") {
            console.log("connected");
            const localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            localStream.getTracks().forEach(track => {
                peerConnection.addTrack(track, localStream);
            });
        }
    });
}
