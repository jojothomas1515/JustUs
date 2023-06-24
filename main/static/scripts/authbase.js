"use strict";
const show_password = document.querySelectorAll(".show-password");
const signup_form = document.querySelector("#signup-form");
function hideOrShow(element) {
    element.addEventListener('click', () => {
        const password = element.parentElement.querySelector('input');
        if (password.type === 'password') {
            element.classList.add('fa-eye-slash');
            password.type = 'text';
        }
        else {
            element.classList.remove('fa-eye-slash');
            password.type = 'password';
        }
    });
}
show_password.forEach(hideOrShow);
