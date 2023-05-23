function ShowText(list_name, this_element) {
  this_element.children[0].classList.toggle("rotate-180");
  document.getElementById(list_name).classList.toggle("hidden");
}
