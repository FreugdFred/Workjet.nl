const passwordBox = document.getElementById('password-placeholder');
const hiddenEye = document.getElementById('closed-eye');
const openEye = document.getElementById('open-eye');

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

const Email = urlParams.get("email");
const Hidden = urlParams.get("hidden");
const Already = urlParams.get("already");

if (Already === "True") {
  document.querySelector("#alreadyknown").classList.remove("hidden");
}

if (Email !== null) {
  document.querySelector("#login").value = Email;
}

if (Hidden === "False") {
  document.querySelector("#error").classList.remove("hidden");
}

function showpassword() {
  if (passwordBox.type === 'password') {
    passwordBox.type = 'text';
  } else {
    passwordBox.type = 'password';
  }

  hiddenEye.classList.toggle('hidden');
  openEye.classList.toggle('hidden');
}
