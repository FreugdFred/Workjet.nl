const passwordBox = document.getElementById('password-1');
const hiddenEye = document.getElementById('closed-eye');
const openEye = document.getElementById('open-eye');


let EmployerSelect = document.getElementById("employer");
let PasswordLabel = document.getElementById('password-1-label')

if (EmployerSelect) {
  if (PasswordLabel.innerHTML === 'Password') {
    EmployerSelect.options[1].innerHTML = "employer";
    EmployerSelect.options[2].innerHTML = "employee";
  }

  if (PasswordLabel.innerHTML === 'Пароль') {
    EmployerSelect.options[1].innerHTML = "роботодавець";
    EmployerSelect.options[2].innerHTML = "робітник";
  }
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