const cells = document.querySelectorAll('.cell');

const message = document.querySelector('#message');


function getRandomInt(max) {
    return Math.floor(Math.random() * max) 
}

function remove_on_click_cell(cells) {
    cells.forEach(cell => {
        console.log(cell)
        cell.removeEventListener('click', on_cell_click )
    })
}

function on_cell_click (data) {
    if (data.target.innerHTML !== '') {
        message.innerHTML = 'Занято'
        return
    }
    data.target.innerHTML = 'X'
    const is_winner1 = check_winner(cells)
     if (is_winner1 !== false) {
        message.innerHTML = '!!!We got a winner!!! ' + is_winner1
        remove_on_click_cell(cells);
        after_win();

    }

    let freecell = Array.from(cells).filter((c) => {
        return c.textContent == '';
    })

    const freecells_length = freecell.length;
    
    if (freecells_length === 0) {
        message.innerHTML = 'GAME OVER'
    }

    const randNum = getRandomInt(freecells_length);
     freecell[randNum].textContent = 'O';
     const is_winner = check_winner(cells)
     if (is_winner !== false) {
        message.innerHTML = '!!!We got a winner!!! ' + is_winner
        remove_on_click_cell(cells);
        after_win();
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
            result = 'X'
        }
        if (cells[combo[0]].innerHTML == 'O' && cells[combo[1]].innerHTML == 'O' && cells[combo[2]].innerHTML == 'O') {
            result =  'O'
        }
    })  
    return result;
}

function after_win () {
    cells.forEach(cell => {
        cell.classList.add('disable_cell')
    })
}
