import '../styles/reset.css'
import '../styles/players_list.css'

const playersList = document.querySelector('.players__list');

async function getPlayersNames() {
  try {
    const response = await fetch('http://tic-tac-toe.mrdudov.ru/api/v1/users/users', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      throw new Error('Ошибка при выполнении запроса');
    }

    const result = await response.json();

    result.forEach(item => {
      playersList.innerHTML += `<a href="./gameboard.html" class="player">${item.email}</a>`;
    });

    const players = document.querySelectorAll('.player');
    players.forEach(player => {
      player.addEventListener('click', (event) => {
        localStorage.setItem('opponentsName', event.target.textContent.trim());
      });
    });

  } catch (error) {
    console.log('Произошла ошибка:', error);
  }
};



  getPlayersNames()