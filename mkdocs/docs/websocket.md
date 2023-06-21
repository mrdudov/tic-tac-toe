# WebSocket Example

    let ws = new WebSocket("ws://tic-tac-toe.mrdudov.ru/api/v1/ws")
    let ws = new WebSocket("ws://localhost:8080/ws")
    ws.onmessage = function(event) { console.log(event.data) }
    ws.send('get_online_users')
    ws.close()
