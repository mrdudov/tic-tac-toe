const cells = document.querySelectorAll('.cell');

const winner = document.querySelector('#winner');
const description = document.querySelector('#description');

function getRandomInt(max) {
    return Math.floor(Math.random() * max) 
}

function remove_on_click_cell(cells) {
    cells.forEach(cell => {
        console.log(cell);
        cell.removeEventListener('click', on_cell_click );
    })
}

function on_cell_click (data) {
    if (data.target.innerHTML !== '') {
        alert("ЗАНЯТО БРАЗЕ")
        return
    }
    data.target.innerHTML = 'X'
    const is_winnerX = check_winner(cells);
     if (is_winnerX !== false) {
        winner.innerHTML = is_winnerX;
        description.innerHTML = 'WON THIS GAME';
        remove_on_click_cell(cells);
        after_win();
        return

    }

    let freecell = Array.from(cells).filter((c) => {
        return c.textContent == '';
    })

    const freecells_length = freecell.length;
    
    if (freecells_length === 0) {
        after_win();
        winner.innerHTML = 'GAME';
        description.innerHTML = 'OVER';
        return
    }

    const randNum = getRandomInt(freecells_length);
     freecell[randNum].textContent = 'O';
     const is_winnerO = check_winner(cells);
     if (is_winnerO !== false) {
        winner.innerHTML = is_winnerO;
        description.innerHTML = 'WON THIS GAME';
        remove_on_click_cell(cells);
        after_win();
        return
    }
}

cells.forEach((cell)=> {
    cell.addEventListener('click', on_cell_click)
})

function check_winner (cells) {
    const winningCombos = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
]

    let result = false;
    winningCombos.forEach((combo) => {
        if (cells[combo[0]].innerHTML == 'X' && cells[combo[1]].innerHTML == 'X' && cells[combo[2]].innerHTML == 'X') {
            cells[combo[0]].style.color = 'red';
            cells[combo[1]].style.color = 'red';
            cells[combo[2]].style.color = 'red';
            result = 'X'
        }
        if (cells[combo[0]].innerHTML == 'O' && cells[combo[1]].innerHTML == 'O' && cells[combo[2]].innerHTML == 'O') {
            cells[combo[0]].style.color = 'red';
            cells[combo[1]].style.color = 'red';
            cells[combo[2]].style.color = 'red';
            result =  'O'
        }
    })

    return result;
}

function after_win() {
    window_after_game_over.style.opacity = '1';
    window_after_game_over.style['z-index'] = '99';
}

function clear_game_board() {
    window_after_game_over.style.opacity = '0';
    window_after_game_over.style['z-index'] = '-1';
    cells.forEach(cell => {
        cell.innerHTML = '';
        cell.style.color = '';
        cell.classList.remove('disable_cell');
        cell.addEventListener('click', on_cell_click);
    })

}