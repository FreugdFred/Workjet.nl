"use strict";

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const LANGUAGECOOKIE = getCookie("language");

const TriggerDiv = document.querySelector("#trigger");
const TEMPLATE = document.querySelector("#profile");
const ProfileDiv = document.querySelector("#profile-div");
const WORKLIST = ["landbouw", "bouw", "handel", "gezondheidszorg", "communicatie", "onderwijs", "horeca", "transport", "productie", "engineering"];

const ProfileCookie = getCookie("saved_profiles");
const HastagEmails = ProfileCookie.replaceAll("-#", "\n#");
let emailTextareaInfo = `Goedendag,\n\nIk zou graag toegang willen vragen tot U volgende contacten:\n${HastagEmails}\n\nMet vriendelijke groeten,\n{U naam en het bedrijf waarvoor u werkt}`;

if (LANGUAGECOOKIE === "EN") {
  emailTextareaInfo = `Dear Robotta team,\n\nI would like to receive the contact information of the following profiles:\n${HastagEmails}\n\nWith kind regards,\n{The company you work for}`;
}
if (LANGUAGECOOKIE === "UA") {
  emailTextareaInfo = `Шановна команда Robotta,\n\n я хотів би отримати контакти цих робітників:\n${HastagEmails}\n\n З повагою,\n{Компанія, на яку ви працюєте}`;
}

document.querySelector("#copy-text-area").value = emailTextareaInfo;

const SavedList = ProfileCookie.split("-").filter(elm => elm);
let counter = 1;

document.querySelector("#contacts-btn").addEventListener("click", () => {
  document.querySelector("#contacts-svg").classList.toggle("rotate-180");
  document.querySelector("#clipboard-div").classList.toggle("hidden");
});

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      let MadeUrl = MakeURL(SavedList, counter);

      FetchData(MadeUrl);
      counter++;
    }
  });
});

observer.observe(TriggerDiv);

function MakeURL(InfoList, indexPage) {
  const LastPost = InfoList.length > indexPage * 10 ? indexPage * 10 : InfoList.length;
  const FirstPost = LastPost === InfoList.length ? (indexPage - 1) * 10 : LastPost - 10;
  let UrlString = "/savedask?profilesbycode=";

  if (LastPost === InfoList.length) observer.disconnect();
  for (let i = FirstPost; i < LastPost; i++) UrlString += InfoList[i].replace("#", "-");

  return UrlString;
}

function FetchData(StringQuery) {
  fetch(StringQuery)
    .then(response => response.json())
    .then(data => {
      data.forEach(profile => {
        if (profile.age) PostDataDom(profile);
      });
    });
}

function CopyClipBoard(this_element) {
  navigator.clipboard.writeText(emailTextareaInfo);

  this_element.classList.replace("bg-blue-600", "bg-green-600");
  this_element.classList.replace("hover:bg-blue-300", "hover:bg-green-300");

  document.querySelector("#no-copy-svg").classList.add("hidden");
  document.querySelector("#yes-copy-svg").classList.remove("hidden");

  document.querySelector("#button-text").innerText = "Copied!";
}

function PostDataDom(profile) {
  const TemplateClone = TEMPLATE.content.cloneNode(true);

  if (!profile.currentlylooking) TemplateClone.getElementById("search-profile").classList.replace("bg-green-600", "bg-red-600");
  if (ProfileCookie.includes(profile.code)) TemplateClone.getElementById("save-button").classList.add("fill-blue-600");

  TemplateClone.getElementById("save-button").name = profile.code;

  TemplateClone.getElementById("search-profile").textContent = profile.currentlylooking === true ? LOOKING : NOTLOOKING;
  TemplateClone.getElementById("name-profile").textContent = profile.name;
  TemplateClone.getElementById("age-profile").textContent = MakeAge(profile.age);
  TemplateClone.getElementById("gender-profile").textContent = profile.men === true ? MEN : WOMAN;
  TemplateClone.getElementById("worktime-profile").textContent = profile.fulltime === true ? FULLTIME : PARTTIME;
  TemplateClone.getElementById("study-profile").textContent = profile.schooling;
  TemplateClone.getElementById("language-profile").textContent = profile.language;
  TemplateClone.getElementById("region-profile").textContent = profile.region;
  TemplateClone.getElementById("code-profile").textContent = profile.code;

  TemplateClone.getElementById("inexperience-profile").textContent = profile.inexperience;
  TemplateClone.getElementById("experience-profile").textContent = profile.outexperience;
  TemplateClone.getElementById("comments-profile").textContent = profile.comment;

  for (let i = 0; i < WORKLIST.length; i++) {
    let Workname = WORKLIST[i]
    if (profile[Workname]) {
      TemplateClone.getElementById(`${Workname}-work`).classList.remove('hidden')
    }
  }
  ProfileDiv.appendChild(TemplateClone);
}

function ButtonEvents(this_element) {
  this_element.classList.toggle("fill-blue-600");
  let savedProfilesCookie = getCookie("saved_profiles");

  if (this_element.classList.contains("fill-blue-600")) document.cookie = `saved_profiles=${savedProfilesCookie}-${this_element.name}`;
  else document.cookie = "saved_profiles=" + savedProfilesCookie.replace(`-${this_element.name}`, "");
}

function MakeAge(AgeNumb) {
  if (AgeNumb < 21) return "18 - 20";

  const JugdeNumb = AgeNumb - Math.floor(AgeNumb / 10) * 10;

  if (JugdeNumb > 5 || JugdeNumb === 5) {
    return `${Math.round(AgeNumb / 10) * 10 - 5} - ${Math.round(AgeNumb / 10) * 10}`;
  } else {
    return `${Math.round(AgeNumb / 10) * 10} - ${Math.round(AgeNumb / 10) * 10 + 5}`;
  }
}
