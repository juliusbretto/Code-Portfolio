function showInfo(param) {
  const params = new URLSearchParams(window.location.search);
  const div = document.querySelector(`#${param}`);
  if (params.has(param)) {
    div.classList.remove("d-none");
    div.innerText = params.get(param);
  }
}

showInfo("error");
showInfo("success");
