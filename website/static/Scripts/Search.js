"use-strict";

let counter = 1;
let StringQuery = "";
let ResultsCounter = 0;

let WORKNAMELIST = ["landbouw", "bouw", "handel", "gezondheidszorg", "communicatie", "onderwijs", "horeca", "transport", "productie", "engineering"];

const RESULTSELEMENT = document.getElementById("result-number");

const GENDERELEMENT = document.getElementById("gender");
const SEARCHINGELEMENT = document.getElementById("searching");
const WORKELEMENT = document.getElementById("work");
const REGIONELEMENT = document.getElementById("region");
const CHECKBOXELEMENT = document.getElementById("checkbox-div");
const SEARCHELEMENT = document.getElementById("input-search");

const TriggerDiv = document.querySelector("#trigger");
const TEMPLATE = document.querySelector("#profile");
const ProfileDiv = document.querySelector("#profile-div");
const WORKLIST = ["landbouw", "bouw", "handel", "gezondheidszorg", "communicatie", "onderwijs", "horeca", "transport", "productie", "engineering"];

const ProfileCookie = getCookie("saved_profiles");


const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const SEARCHVALUE = urlParams.get("searchvalue");
if (SEARCHVALUE) {
  REGIONELEMENT.value = SEARCHVALUE;
  history.pushState({}, "", "/search");
}

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      StringQuery = MakeUrl();
      FetchData(StringQuery);
      counter++;
    }
  });
});

observer.observe(TriggerDiv);

function MakeRequest() {
  observer.observe(TriggerDiv);
  ResultsCounter = 0;
  counter = 1;
  DeletePosts();
  StringQuery = MakeUrl();
  FetchData(StringQuery);
  counter++;
}

function MakeUrl() {
  StringQuery = "";

  const GENDER = GENDERELEMENT.value;
  const SEARCHING = SEARCHINGELEMENT.value;
  const WORK = WORKELEMENT.value;
  const REGION = REGIONELEMENT.value.replaceAll(" ", "%20");
  const SEARCH = SEARCHELEMENT.value.replaceAll(" ", "%20");

  if (GENDER !== "None") StringQuery += `gender=${GENDER}&`;
  if (SEARCHING !== "None") StringQuery += `working=${SEARCHING}&`;
  if (WORK !== "None") StringQuery += `worktime=${WORK}&`;
  if (REGION !== "None") StringQuery += `region=${REGION}&`;
  if (SEARCH) StringQuery += `search=${SEARCH}&`;

  const CHECKBOX = CHECKBOXELEMENT.querySelectorAll('input[type="checkbox"]:checked');
  CHECKBOX.forEach(checkbox => {
    StringQuery += checkbox.name + "=true&";
  });
  return StringQuery;
}

function ShowHide(THISELEMENT) {
  for (const child of THISELEMENT.children) child.classList.toggle("rotate-180");
  if (THISELEMENT.id === "filter-btn") document.getElementById("filter-div").classList.toggle("hidden");
  else document.getElementById("checkbox-div").classList.toggle("hidden");
}

function FetchData(StringQuery) {
  fetch(`/searchask?${StringQuery}&pagenumber=${counter}`)
    .then(response => response.json())
    .then(jsonresponse => {
      if (jsonresponse.length === 0) {
        observer.unobserve(TriggerDiv);
      }
      ResultsCounter += jsonresponse.length;
      RESULTSELEMENT.innerHTML = RESULTS + ResultsCounter;
      return jsonresponse;
    })
    .then(data => {
      data.forEach(profile => {
        if (profile.age) PostDataDom(profile);
      });
    });
}

function DeletePosts() {
  document.querySelectorAll("#profile-widget").forEach(post => post.remove());
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

function MakeAge(AgeNumb) {
  if (AgeNumb < 21) return "18 - 20";
  const JugdeNumb = AgeNumb - Math.floor(AgeNumb / 10) * 10;

  if (JugdeNumb > 5 || JugdeNumb === 5) {
    return `${Math.round(AgeNumb / 10) * 10 - 5} - ${Math.round(AgeNumb / 10) * 10}`;
  } else {
    return `${Math.round(AgeNumb / 10) * 10} - ${Math.round(AgeNumb / 10) * 10 + 5}`;
  }
}

function ButtonEvents(this_element) {
  this_element.classList.toggle("fill-blue-600");
  let savedProfilesCookie = getCookie("saved_profiles");

  if (this_element.classList.contains("fill-blue-600")) document.cookie = `saved_profiles=${savedProfilesCookie}-${this_element.name}`.replaceAll("undefined", "");
  else document.cookie = "saved_profiles=" + savedProfilesCookie.replaceAll(`-${this_element.name}`).replaceAll("undefined", "");
}

function GetContact(this_element) {
  const savedProfilesCookie = getCookie("saved_profiles");
  if (!savedProfilesCookie.includes(this_element.name)) document.cookie = `saved_profiles=${savedProfilesCookie}-${this_element.name}`;
  window.location.href = "/saved";
}
