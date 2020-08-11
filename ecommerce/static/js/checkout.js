
const name = document.getElementById("name");
const cardNumber = document.getElementById("cardNumber");
const securityCode = document.getElementById("securityCode");
const monthDropdown = document.getElementById("monthDropdown");
const yearDropdown = document.getElementById("yearDropdown");
const payForm = document.getElementById("payForm");

const invalidName = document.getElementById("invalidName");
const invalidCardnumber = document.getElementById("invalidCardnumber");
const invalidExpirationDate = document.getElementById("invalidExpirationDate");
const invalidSecurityCode = document.getElementById("invalidSecurityCode");

//Payment system still needs implementing
if(payForm){
    payForm.addEventListener('submit', handleForm);
    function handleForm(event) { 
        event.preventDefault(); 
    } 
}



// Automatically gives a space every 4 digits
//when the customer enters their card number
cardNumber.addEventListener('input', function(e){
    e.target.value = e.target.value.replace(/[^\d]/g, '').replace(/(.{4})/g, '$1 ').trim();
});

function validateName() {
    name.value = name.value.trim();


    if (name.value == ""){
        invalidName.innerHTML="You must insert a name"
        return false;
    }
    else {
        invalidName.innerHTML="";
        return true;
    }
}


function validateCardNumber() {
    cardNumber.value = cardNumber.value.trim();
    // It seems a card number can be between 12 and 19 digits in length
    validCardNumber = /^[0-9]{12,19}/

    if (cardNumber.value == ""){
        invalidCardnumber.innerHTML="You must insert your card number"
        return false;
    }
    else if (removeSpaces(cardNumber.value).match(validCardNumber)){
        invalidCardnumber.innerHTML="";
        return true;
    }
    else {
        invalidCardnumber.innerHTML="Card number must be between 12 and 19 digits long";
        return false;
    }
}


function validateExpiration(){
    if (monthDropdown.selectedOptions[0].label == "MM" || yearDropdown.selectedOptions[0].label == "YYYY"){
        invalidExpirationDate.innerHTML="You must insert both the month and year of the expiration date";
        return false;
    }
    else{
        invalidExpirationDate.innerHTML=""
        return true;
    }
}

function validateSecurityCode(){

    if (securityCode.value == ""){
        invalidSecurityCode.innerHTML = "Must insert a security code"
        return false;
    }
    else if (securityCode.value.length < 3){
        invalidSecurityCode.innerHTML = "Security code must be 3 digits long";
        return false;
    }
    else{
        invalidSecurityCode.innerHTML = "";
        return true;
    }
}

function removeSpaces(string){
    return string.split(" ").join("")
}

//Validates the entire payment form
function validatePayForm(form){
    if(
        validateName() &&
        validateCardNumber() &&
        validateExpiration() &&
        validateSecurityCode
    ){
        form.submit();
    }
    else{
        return;
    }
}
