let timer;

function logout() {
  let request = false;
  if (window.XMLHttpRequest) {
    request = new XMLHttpRequest();
  }

  if (request) {
    request.open("POST", "/logout");
    request.onreadystatechange = function handleRequestStateChange() {
      if (request.readyState === 4 && request.status === 200) {
        window.location.href = "/login?error=Signed out because of inactivity";
      }
    };
  }
  request.send();
}

function resetTimer() {
  clearTimeout(timer);
  timer = setTimeout(logout, 10000); // 10 sekunder
}

document.addEventListener("mousemove", resetTimer);
document.addEventListener("keydown", resetTimer);
document.addEventListener("click", resetTimer);

resetTimer();