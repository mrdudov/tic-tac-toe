import '../styles/reset.css';
import '../styles/registration.css';

const submitBtn = document.querySelector('.registration__btn');
const emailInput = document.querySelector('.input-email');
const passwordInput = document.querySelector('.input-password');
const invalidNameMsg = document.querySelector('.registration__invalid-name');

function validateNickname(name) {
  if (name === '') {
    invalidNameMsg.textContent = 'Please enter your email';
    return false;
  }

  if (!/^[\w.-]+@[a-zA-Z_-]+?(?:\.[a-zA-Z]{2,})+$/.test(name)) {
    invalidNameMsg.textContent = 'Invalid email format';
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
    invalidNameMsg.textContent = 'Please enter your password';
    return false;
  }

  return true;
}

submitBtn.addEventListener('click', async (event) => {
  event.preventDefault();
  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  try {
    if (!validateNickname(email)) {
      console.log('email error')
      return;
    }

    if (!validatePassword(password)) {
      console.log('password error')
      return;
    }

    const response = await fetch('http://tic-tac-toe.mrdudov.ru/api/v1/auth/register', {
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

    if (response.ok) {
      const data = response.json();
      localStorage.setItem('accessToken', data.access_token);
      localStorage.setItem('refreshToken', data.access_token);
      localStorage.setItem('myEmail', email)
      window.location.href = './login.html';
    } else {
      invalidNameMsg.textContent = 'This user is already registered'
    }
  } catch (error) {
    invalidNameMsg.textContent = error;
  }
});
