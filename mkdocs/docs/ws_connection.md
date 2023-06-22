# WebSocket connection Example

## On prod

1. create ws connection

    ```js
    let ws = new WebSocket("ws://tic-tac-toe.mrdudov.ru/api/v1/ws")
    ```

2. set onmessage callback function

    ```js
    ws.onmessage = function(event) {
        console.log(event.data)
    }
    ```

3. send message

    ```js
    ws.send('get_online_users')
    ```

4. close ws connection

    ```js
    ws.close()
    ```

## On dev

1. create ws connection

    ```js
    let ws = new WebSocket("ws://localhost:8080/api/v1/ws")
    ```

2. set onmessage callback function

    ```js
    ws.onmessage = function(event) {
        console.log(event.data)
    }
    ```

3. send message

    ```js
    ws.send('get_online_users')
    ```

4. close ws connection

    ```js
    ws.close()
    ```
