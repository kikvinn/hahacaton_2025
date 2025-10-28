<svelte:head>
  <title>Главная — Polyathlon</title>
</svelte:head>

<script>
  import { goto } from '$app/navigation';
  
  function openDocumentation() {
    // Открывает PDF файл в новой вкладке
    window.open('/MPU_polyathlon_rules_new_edition-2016.pdf', '_blank');
    
    // Альтернативно, можно открыть в том же окне:
    // window.location.href = '/documentation.pdf';
  }
</script>

<div class="hero">
  <div class="hero-content">
    <h1 class="hero-title">Добро пожаловать в Polyathlon</h1>
    <p class="hero-subtitle">Платформа для управления спортивными мероприятиями</p>
  </div>
</div>

<div class="features">
  <div class="feature-card" on:click={() => goto('/team-registration')}>
    <h3>Регистрация команд</h3>
    <p>Быстрая и удобная регистрация ваших спортивных команд</p>
  </div>
  
  <div class="feature-card" on:click={() => goto('/rating')}>
    <h3>Рейтинг</h3>
    <p>Актуальные рейтинги участников и команд</p>
  </div>
  
  <div class="feature-card" on:click={() => goto('/stub')}>
    <h3>Мероприятия</h3>
    <p>Запланированные ивенты </p>
  </div>
</div>

<footer class="footer">
  <div class="footer-content">
    <div class="footer-left"></div>
    <div class="footer-center">
      <p class="footer-text">Polyathlon 2025 Все права защищены.</p>
    </div>
    <div class="footer-right">
      <a href="#" on:click|preventDefault={openDocumentation} class="footer-link">Документация</a>
    </div>
  </div>
</footer>

<style>
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

  .hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 2rem;
    text-align: center;
  }

  .hero-title {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
  }

  .hero-subtitle {
    font-size: 1.25rem;
    opacity: 0.9;
    max-width: 600px;
    margin: 0 auto;
  }

  .features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    padding: 4rem 2rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .feature-card {
    background: #fff;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
  }

  .feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }

  .feature-card h3 {
    color: #333;
    margin-bottom: 1rem;
    font-size: 1.5rem;
  }

  .feature-card p {
    color: #666;
    line-height: 1.6;
  }

  .footer {
    background: #f8f9fa;
    padding: 2rem;
    margin-top: 2rem;
  }

  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .footer-center p {
    color: #666;
    margin: 0;
    text-align: center;
  }

  .footer-link {
    color: #666;
    text-decoration: none;
    cursor: pointer;
  }

  .footer-link:hover {
    text-decoration: underline;
  }

  @media (max-width: 768px) {
    .header-content {
      flex-direction: column;
      gap: 1rem;
    }
    
    .hero {
      padding: 2rem 1rem;
    }
    
    .hero-title {
      font-size: 2rem;
    }
    
    .features {
      grid-template-columns: 1fr;
      padding: 2rem 1rem;
    }
    
    .footer-content {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }
    
    .footer-center p {
      text-align: center;
    }
  }
</style>