# ws online users

## get online users example

```js
let access_token = "access token"

let data = {
    end_point: "online_users",
    query: "get_list",
    access_token: access_token
}

let json_data = JSON.stringify(data)

ws.send(json_data)
```
