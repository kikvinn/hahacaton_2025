<svelte:head>
  <title>Документация — Polyathlon</title>
</svelte:head>

<div class="docs-page">
  <div class="container">
    <h2>Документация</h2>
    <p>Здесь вы найдете всю необходимую информацию по работе с сервисом.</p>

    <ul class="docs-list">
      <li><a href="#">Как начать работу</a></li>
      <li><a href="#">API справочник</a></li>
      <li><a href="#">Часто задаваемые вопросы</a></li>
      <li><a href="#">Поддержка и обратная связь</a></li>
    </ul>
  </div>
</div>

<style>
  .docs-page {
    padding: 3rem 0;
    flex-grow: 1;
  }

  .docs-list {
    list-style-type: none;
    margin-top: 1.5rem;
  }

  .docs-list li {
    margin-bottom: 0.75rem;
  }

  .docs-list a {
    color: var(--primary);
    text-decoration: underline;
  }
</style>