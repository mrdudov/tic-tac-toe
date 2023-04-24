const get_btn = document.querySelector('#get-data')
const name_btn = document.querySelector('#name-btn')
const name_input = document.querySelector('#name')

const REQUEST_URL = 'http://tic-tac-toe.mrdudov.ru/api/v1/users'


name_btn.onclick = () => {
    
    var payload = {
        "name": name_input.value  
    }

    fetch(REQUEST_URL,{
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then((res) => { 
        return res.json()
    })
    .then((data) => { 
        console.log( JSON.stringify( data ) ) 
    })
}

get_btn.onclick=() => {
    fetch(REQUEST_URL)
    .then(function(data) {
      return data.json()
    })
    .then((data) => {
      console.log(data)
    })
}
