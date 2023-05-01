const nameInput = document.querySelector('.registration__input');
const nameBtn = document.querySelector('.registration__btn');
const form = document.querySelector('.registration__form');
const playersList = document.querySelector('.players__list');

const requestURL = 'http://tic-tac-toe.mrdudov.ru/api/v1/users';

async function getPlayersNames() {
  let response = await fetch('http://tic-tac-toe.mrdudov.ru/api/v1/users');
  let result = await response.json();

  for (let key in result) {
    let playerName = result[key]['name'];
    playersList.innerHTML += `<a href="./index.html" class="player">${playerName}</a>`;
  }

  const players = document.querySelectorAll('.player');
  players.forEach(player => {
    player.addEventListener('click', (event) => {
      localStorage.setItem('selectedPlayer', event.target.textContent.trim());
    });
  });
}

getPlayersNames();

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

function validateNickname(name) {
  const invalidNameMsg = document.querySelector('.registration__invalid-name');
  
  if (name.length < 3) {
    invalidNameMsg.textContent = 'At least 3 characters';
    return false;
  }

  if (name.length > 10) {
    invalidNameMsg.textContent = 'Maximum 10 characters';
    return false;
  }

  if (!/^[a-zA-Z0-9]+$/.test(name)) {
    invalidNameMsg.textContent = 'You can only use letters and numbers';
    return false;
  }

  invalidNameMsg.textContent = '';

  return true;
}

nameBtn.addEventListener('click', (event) => {
event.preventDefault();
const name = nameInput.value.trim();
if (validateNickname(name)) {
  window.location.href = './players_list.html'
    // return addPlayerNameToServer()
}
});

const selectedPlayer = localStorage.getItem('selectedPlayer');
const savedMyName = localStorage.getItem('savedMyName');
const opponentNickname = document.querySelector('.opponent-name');
const myNickname = document.querySelector('.my-name');

console.log(savedMyName)

opponentNickname.textContent = selectedPlayer;
myNickname.textContent = savedMyName;