function Postform() {
  document.getElementById("language-input").value = getCookie("language");
  document.getElementById("forgot-form").submit();
}