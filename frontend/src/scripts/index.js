const nickname = localStorage.getItem('myName');

        if (nickname) {
            window.location.href = 'gameboard.html';
        } else {
            window.location.href = 'registration.html';
        }