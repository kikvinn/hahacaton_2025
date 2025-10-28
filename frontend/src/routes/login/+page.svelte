<svelte:head>
  <title>Вход — MyService</title>
</svelte:head>

<script>
  let formData = {
    email: '',
    password: ''
  };

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData),
        credentials: 'include'
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Успешный вход:', result);
        // Здесь можно сохранить токен и перенаправить пользователя
        // localStorage.setItem('token', result.token);
        window.location.href = '/';
      } else {
        console.error('Ошибка входа:', response.statusText);
        // Здесь можно показать сообщение об ошибке пользователю
      }
    } catch (error) {
      console.error('Ошибка сети:', error);
      // Здесь можно показать сообщение об ошибке сети
    }
  }
</script>

<div class="auth-wrapper">
  <div class="auth-card">
    <h2>Вход в систему</h2>
    <form class="auth-form" on:submit={handleSubmit}>
      <div class="form-group">
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          bind:value={formData.email}
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Пароль</label>
        <input
          type="password"
          id="password"
          bind:value={formData.password}
          required
        />
      </div>
      <button type="submit" class="btn btn-primary full-width">Войти</button>
    </form>
    <p class="mt-1">Нет аккаунта? <a href="/register">Зарегистрироваться</a></p>
  </div>
</div>

<style>
  .auth-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 1rem;
  }

  .auth-card {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 2rem;
    width: 100%;
    max-width: 400px;
  }

  .auth-form {
    margin-top: 1.5rem;
  }

  .form-group {
    margin-bottom: 1.25rem;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
  }

  .form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border);
    border-radius: 4px;
  }

  .full-width {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    width: 100%;
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 4px;
    color: white;
    font-size: 1rem;
    cursor: pointer;
  }

  .mt-1 {
    margin-top: 1rem;
    text-align: center;
  }

  .mt-1 a {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-decoration: underline;
  }
</style>