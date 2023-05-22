import '../styles/reset.css'
import '../styles/registration.css'

function validateNickname(name) {
  const invalidNameMsg = document.querySelector('.registration__invalid-name');
  
  if (!/^[a-zA-Z0-9]+$/.test(name)) {
    invalidNameMsg.textContent = 'You can only use letters and numbers';
    return false;
  }

  if (name.length < 3) {
    invalidNameMsg.textContent = 'At least 3 characters';
    return false;
  }

  if (name.length > 10) {
    invalidNameMsg.textContent = 'Maximum 10 characters';
    return false;
  }

  invalidNameMsg.textContent = '';
  return true;
}

const submitBtn = document.querySelector('.registration__btn');
const nameInput = document.querySelector('.registration__input');

submitBtn.addEventListener('click', (event) => {
event.preventDefault();
const name = nameInput.value.trim();

if (validateNickname(name)) {
  localStorage.setItem('myName', name)
  window.location.href = './players_list.html'
  return addPlayerNameToServer()
}
});

// REQUSET URL ДЖОКЪДУ
function addPlayerNameToServer() {
  const requestBody = { 'name': nameInput.value }; 
  fetch(requestURL, { 
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
}