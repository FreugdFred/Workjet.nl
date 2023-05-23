"use strict";

const NAVBAR = document.getElementById('nav-bar');
const EXTENDDIV = document.getElementById('extend-div');
const LANGUAGELIST = document.querySelector("#language-list");

const LANGUAGEPOPUP = document.querySelector("#language-popup");
const languageClose = document.querySelector("#close-language");

const dropdownList = document.querySelector("#dropdown-list");
const languageList = document.querySelector("#language-list");
const dropdownButton = document.querySelector("#dropdown-button");

let alert_del = document.querySelectorAll(".alert-del");

alert_del.forEach(x =>
  x.addEventListener("click", function () {
    x.parentElement.classList.add("hidden");
  })
);

dropdownButton.addEventListener("click", function () {
  languageList.classList.toggle("hidden");
  dropdownList.classList.toggle("hidden");
});

// ---------------------------------------------------- //


if (!document.cookie.match(/^(.*;)?\s*language\s*=\s*[^;]+(.*)?$/)) {
  togglepopup();
  SetProfileCookie();
}


function SelectedLanguage(language_name) {
  document.cookie = `language=${language_name}`;
  togglepopup();
  location.reload();
}


function togglepopup() {
  NAVBAR.classList.toggle('blur');
  EXTENDDIV.classList.toggle('blur');
  LANGUAGEPOPUP.classList.toggle('hidden');
}


function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function SetProfileCookie() {
  if (!document.cookie.match(/^(.*;)?\s*saved_profiles\s*=\s*[^;]+(.*)?$/)) document.cookie = "saved_profiles=";
}