const navBtn: HTMLButtonElement = document.querySelector(".menu-btn") as HTMLButtonElement;
const nav: HTMLDivElement = document.querySelector(".links") as HTMLDivElement;

navBtn.addEventListener("click", () => {
    nav.classList.toggle("show-nav");
})