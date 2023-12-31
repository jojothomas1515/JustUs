const show_password: NodeListOf<HTMLElement> = document.querySelectorAll(".show-password");
const signup_form: HTMLFormElement = document.querySelector("#signup-form") as HTMLFormElement;


function hideOrShow(element: HTMLElement) {
    element.addEventListener('click', () => {
        const password = element.parentElement!.querySelector('input') as HTMLInputElement;
        if (password.type === 'password') {
            element.classList.add('fa-eye-slash');
            password.type = 'text';
        } else {
            element.classList.remove('fa-eye-slash');
            password.type = 'password';
        }
    })
}

show_password.forEach(hideOrShow)
