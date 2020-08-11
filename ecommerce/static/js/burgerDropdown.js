//Burger dropdown toggle menu
let navBar = document.getElementsByTagName('nav')[0];
let burgerIcon = document.getElementsByClassName('burgerIcon')[0];
let crossIcon = document.getElementsByClassName('crossIcon')[0];
let mainLogo = document.getElementById('logo');
function showDropdown(){
    navBar.classList.toggle('burgerDropdown');
    burgerIcon.classList.toggle('displayNone');
    crossIcon.classList.toggle('display');
    mainLogo.classList.toggle('center');

}
