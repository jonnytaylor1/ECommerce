const firstName = document.getElementById("firstName");
const surname = document.getElementById("surname");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const flashMessage = document.getElementById("flashMessage");

const signupForm = document.getElementById("signupForm");
const loginForm = document.getElementById("loginForm");

let invalidFirstName = document.getElementById("invalidFirstName");
let invalidSurname = document.getElementById("invalidSurname");
let invalidEmail = document.getElementById("invalidEmail");
let invalidPassword = document.getElementById("invalidPassword");
let requiredPassword = document.getElementById("requiredPassword");


let show = document.getElementById("show");


//Prevents default submit of signup form before handling
if(signupForm){
    signupForm.addEventListener('submit', handleForm);
    function handleForm(event) { 
        event.preventDefault(); 
    } 
}

//Prevents default submit of login form before handling
if(loginForm){
    loginForm.addEventListener('submit', handleForm);
    function handleForm(event) { 
        event.preventDefault(); 
    } 
}


function validateFirstName(){
    firstName.value = firstName.value.trim();
    let letters = /^[A-Za-z]+$/;
    if (firstName.value == ""){
        invalidFirstName.innerHTML = "First name required";
        return false;
    }
    else if(!firstName.value.match(letters) ){
        invalidFirstName.innerHTML = "Name must only contain letters";
        return false;
    }
    else{
        invalidFirstName.innerHTML = "";
        return true;
    }
}


function validateSurname(){
    surname.value = surname.value.trim();
    let letters = /^[A-Za-z]+$/;
    if (surname.value == ""){
        invalidSurname.innerHTML = "Last name required";
        return false;
    }
    else if(!surname.value.match(letters) ){
        invalidSurname.innerHTML = "Name must only contain letters";
        return false;
    }
    else{
        invalidSurname.innerHTML = "";
        return true;
    }
}



function validateEmail(){
    email.value = email.value.trim();
    let validEmail = /^[^\s@]+@[^\s@]+/;
    if (email.value == ""){
        invalidEmail.innerHTML = "Email required";
        return false;
    }
    else if(!email.value.match(validEmail)){
        invalidEmail.innerHTML = "Must enter a valid email address";
        return false;
    }
    else{
        invalidEmail.innerHTML = "";
        return true;
    }
}

function validatePassword(){
    let validPassword = /(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])/;
    validCounter = 0;
    if (password.value == ""){
        requiredPassword.innerHTML = "Password required";
        validCounter -= 1;
        return;
    }
    else{
        requiredPassword.innerHTML = "";
        validCounter += 1;
    }

    if(!password.value.match(validPassword)){
        invalidPassword.innerHTML = "Must include uppercase, lowercase and numerical characters";
        validCounter -= 1;
    }
    else{
        invalidPassword.innerHTML = "";
        validCounter += 1;
    }

    if(validCounter == 2){
        return true;
    }
    else{
        return false
    }
}


function signupFormValidate(form){
    if(
        validateFirstName() &&
        validateSurname() &&
        validateEmail() &&
        validatePassword()
    ){
        form.submit();
    }
    else{
        return;
    }
}

function loginFormValidate(form){
    if(
        validateEmail() &&
        validatePassword()
    ){
        form.submit();
    }
    else{
        return;
    }
}



function showPassword() {
    if (password.type === "password") {
      password.type = "text";
      show.innerHTML = "HIDE";
    } else {
      password.type = "password";
      show.innerHTML = "SHOW";
    }
  }
