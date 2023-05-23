"use strict";

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const Email = urlParams.get("email");
const Sendmail = urlParams.get("sendmail");

if (Email !== null) {
  document.querySelector("#email").value = Email;
  document.querySelector("#not-text").classList.remove("hidden");
}

if (Sendmail !== null) {
  document.querySelector("#sendemail").innerHTML += " " + Sendmail;
  document.querySelector("#sendemail").classList.remove("hidden");
}
