const cells =document.querySelectorAll('.cell');
console.log(cells)

cells.forEach((cell)=> {
    cell.addEventListener('click', (data) => {
        data.target.innerHTML = 'X'
        
        const randNum = getRandomInt(9);
        console.log(cells[randNum])
         cells[randNum].innerHTML = 'O';
    })
})

function getRandomInt(max) {
    return Math.floor(Math.random() * max) }