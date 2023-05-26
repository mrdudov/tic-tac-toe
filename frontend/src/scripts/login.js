import '../styles/reset.css'
import '../styles/login.css'

localStorage.clear();
const submitBtn = document.querySelector('.login__btn');
const emailInput = document.querySelector('.input-email');
const passwordInput = document.querySelector('.input-password');
const invalidNameMsg = document.querySelector('.login__invalid-name');

function validateNickname(name) {

  if (name === '') {
    invalidNameMsg.textContent = 'Please enter your email';
    return false;
  }

  if (!/^[\w.-]+@[a-zA-Z_-]+?(?:\.[a-zA-Z]{2,})+$/.test(name)) {
    invalidNameMsg.textContent = 'Invalid email form';
    return false;
  }

  if (name.length > 30) {
    invalidNameMsg.textContent = 'Maximum 30 characters';
    return false;
  }

  invalidNameMsg.textContent = '';
  return true;
}

function validatePassword(password) {
  if (password === '') {
    invalidNameMsg.textContent = 'Please enter your password'
    return false
  }

  return true;
}

submitBtn.addEventListener('click', async(event) => {
  event.preventDefault();
  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  try {
    if (!validateNickname(email) || !validatePassword(password)) {
      return;
    }

    const loginResponse = await fetch('http://tic-tac-toe.mrdudov.ru/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });

    if (loginResponse.ok) {
      const loginData = await loginResponse.json();
      localStorage.setItem('accessToken', loginData.access_token);
      localStorage.setItem('myEmail', email);
      window.location.href = './players_list.html';
    }
  } catch (error) {
    console.error(error);
  }

  try {
    const usersResponse = await fetch('http://tic-tac-toe.mrdudov.ru/api/v1/users/users', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    });

    if (!usersResponse.ok) {
      invalidNameMsg.textContent = 'Wrong email or password'
    }
  } catch (error) {
    console.error(error);
  }
});
