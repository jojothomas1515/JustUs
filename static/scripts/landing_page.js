"use strict";
const navBtn = document.querySelector(".menu-btn");
const nav = document.querySelector(".links");
navBtn.addEventListener("click", () => {
    nav.classList.toggle("show-nav");
});
