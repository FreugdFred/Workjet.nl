const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);


history.pushState({}, "", "/");

const Profile = urlParams.get("profile");
if (Profile === "updated") {
  document.querySelector("#update-flash").classList.remove("hidden");
}


function ParameterRedirect() {
  const ElementInput = document.querySelector("#input-bar");
  const RedirectValue = ElementInput.value;

  if (RedirectValue === "") {
    window.location.href = "/search";
  } else {
    window.location.href = `/search?searchvalue=${RedirectValue}`;
  }
}
