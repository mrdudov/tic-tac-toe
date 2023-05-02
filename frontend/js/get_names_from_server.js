async function getPlayersNames() {
  const playersList = document.querySelector('.players__list');  
  let response = await fetch('http://tic-tac-toe.mrdudov.ru/api/v1/users');
  let result = await response.json();
  
  for (let key in result) {
    let playerName = result[key]['name'];
    
    playersList.innerHTML += `<a href="./gameboard.html" class="player">${playerName}</a>`;
    
  }

  const players = document.querySelectorAll('.player');
  players.forEach(player => {
    player.addEventListener('click', (event) => {
      localStorage.setItem('opponentsName', event.target.textContent.trim());
    });
  });
}
  
getPlayersNames();
