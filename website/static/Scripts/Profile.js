"use strict";

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const Select_language_field = document.getElementById("select-language-field");
const select_div = document.getElementById("select-div");


function AddSelect() {
  if (select_div.childElementCount > 30) return;
  const clone = Select_language_field.cloneNode(true);
  select_div.appendChild(clone);
}

function DeleteSelect(this_element) {
  this_element.parentElement.remove();
}

function DeletePost() {
  fetch("/deleteprofile");
  window.location.reload();
}

function SubmitPost() {
  const Sort_languages = document.querySelectorAll("#input-language");
  const Skill_langauages = document.querySelectorAll("#input-skill");
  let language_url = "";

  for (let i = 0; i < Sort_languages.length; i++) {
    language_url += Sort_languages[i].value + ":" + " " + Skill_langauages[i].value + ", ";
  }

  language_url = language_url.substring(0, language_url.length - 2);
  document.getElementById("language-form").value = language_url;

  document.getElementById("profile-form").submit();
}

function MakeEnglish() {
  document.querySelector("#school").placeholder = "university of Kharkiv, master in IT";
  document.querySelector("#comment").placeholder = "I have 20 years work experience in sales, I am good add comforting customers, I don't like to work late hours";
  document.querySelector("#outexperience").placeholder = "I worked 20 years in sales in Holland";
  document.querySelector("#inexperience").placeholder = "I worked 20 years in sales in Ukraine";
  document.querySelector("#contact").placeholder = "My email is Example@name.com and my phonenumber is 05-321867-68127";

  document.getElementById("time").options[0].innerHTML = "part-time";
  document.getElementById("time").options[1].innerHTML = "full-time";

  document.getElementById("gender").options[0].innerHTML = "men";
  document.getElementById("gender").options[1].innerHTML = "woman";

  document.getElementById("currently").options[0].innerHTML = "yes";
  document.getElementById("currently").options[1].innerHTML = "no";
}

function MakeUkrainian() {
  document.querySelector("#school").placeholder = "Харківський університет, диплом ІТ";
  document.querySelector("#comment").placeholder = "У мене 20 років досвіду у продажах і я добре спілкуюсь з клієнтами. У пізні години не працюю";
  document.querySelector("#contact").placeholder = "Мій e-mail: приклад@email.com, мій номер телефону: 05-321867-68127";
  document.querySelector("#outexperience").placeholder = "Я працював 20 років у відділі продаж у Голландії";
  document.querySelector("#inexperience").placeholder = "Я працював 20 років у відділі продаж в Україні";

  document.getElementById("time").options[0].innerHTML = "6-36 год в тиждень";
  document.getElementById("time").options[1].innerHTML = "36-40 год в тиждень";

  document.getElementById("gender").options[0].innerHTML = "чоловік";
  document.getElementById("gender").options[1].innerHTML = "жінка";

  document.getElementById("currently").options[0].innerHTML = "так";
  document.getElementById("currently").options[1].innerHTML = "ні";
}

if (getCookie("language") === "EN") MakeEnglish();
if (getCookie("language") === "UA") MakeUkrainian();

const language_value = document.getElementById("language-form").value.split(", ");
for (let i = 0; i < language_value.length - 1; i++) {
  AddSelect();
}

const all_language_inputs = document.querySelectorAll("#input-language");
const all_skills_inputs = document.querySelectorAll("#input-skill");
for (let i = 0; i < language_value.length; i++) {
  let temp_language = language_value[i].split(": ");
  all_language_inputs[i].value = temp_language[0];
  all_skills_inputs[i].value = temp_language[1];
}
