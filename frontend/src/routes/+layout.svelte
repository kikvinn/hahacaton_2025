<script>
  import '$lib/styles/global.css';
  import { goto } from '$app/navigation';
</script>

<div class="layout">
  <header class="header">
    <div class="header-content">
      <h1 class="logo" on:click={() => goto('/')}>Polyathlon</h1>
      <div class="auth-buttons">
        <button class="btn btn-outline" on:click={() => goto('/login')}>Вход</button>
        <button class="btn btn-primary" on:click={() => goto('/register')}>Регистрация</button>
      </div>
    </div>
  </header>
  
  <slot />
</div>

<style>
  .layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  .header {
    background: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 1rem 2rem;
  }

  .header-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo {
    font-size: 1.5rem;
    font-weight: 700;
    color: #333;
    margin: 0;
    cursor: pointer;
  }

  .logo:hover {
    color: #667eea;
  }

  .auth-buttons {
    display: flex;
    gap: 1rem;
  }

  .btn {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    border: none;
  }

  .btn-outline {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
  
  @media (max-width: 768px) {
    .header-content {
      flex-direction: column;
      gap: 1rem;
    }
  }
</style>