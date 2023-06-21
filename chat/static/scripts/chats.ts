// @ts-ignore
const sio = io();

sio.addEventListener('connect', ()=> {
    console.log('connected')
})