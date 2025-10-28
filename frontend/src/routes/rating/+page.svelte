<svelte:head>
  <title>Рейтинг — Polyathlon</title>
</svelte:head>

<script>
  import { onMount } from 'svelte';
  
  const disciplines = [
    'Эстафета',
    'Троеборье',
    'Командные соревнования',
    'Двоеборье',
    'Четырехборье',
    'Пятиборье',
    'Гонки на лыжероллерах свободным стилем',
    'Лыжные гонки свободным стилем',
    'Сгибание и разгибание рук в упоре лежа',
    'Подтягивание на высокой перекладине',
    'Командные соревнования в стрельбе по закрывающимся мишеням',
    'Командные соревнования в стрельбе по стационарным мишеням',
    'Личные соревнования в стрельбе',
    'Плавание',
    'Метание спортивного снаряда',
    'Бег'
  ];
  
  let selectedDiscipline = disciplines[0];
  let ratings = [];
  
  // Функция для смены дисциплины
  function selectDiscipline(discipline) {
    selectedDiscipline = discipline;
    // Здесь будет загрузка рейтинга для выбранной дисциплины
    loadRatings(discipline);
  }
  
  // Функция для загрузки рейтинга (пока с тестовыми данными)
async function loadRatings(discipline) {
  try {
    const response = await fetch(`/api/rating/${encodeURIComponent(discipline)}`);
    if (response.ok) {
      ratings = await response.json();
    } else {
      console.error('Ошибка загрузки рейтинга');
      ratings = [];
    }
  } catch (error) {
    console.error('Ошибка сети:', error);
    ratings = [];
  }
}
  
  // Загрузка начальных данных
  onMount(() => {
    loadRatings(selectedDiscipline);
  });
</script>

<div class="rating-page">
  <div class="rating-container">
    <!-- Боковая панель с дисциплинами -->
    <aside class="disciplines-sidebar">
      <h2>Дисциплины</h2>
      <ul class="disciplines-list">
        {#each disciplines as discipline}
          <li 
            class="discipline-item {discipline === selectedDiscipline ? 'active' : ''}"
            on:click={() => selectDiscipline(discipline)}
          >
            {discipline}
          </li>
        {/each}
      </ul>
    </aside>
    
    <!-- Основная область с рейтингом -->
    <main class="rating-main">
      <div class="rating-header">
        <h1>{selectedDiscipline}</h1>
      </div>
      
      <div class="rating-table-container">
        <table class="rating-table">
          <thead>
            <tr>
              <th>Место</th>
              <th>ФИО</th>
              <th>Результат</th>
            </tr>
          </thead>
          <tbody>
            {#if ratings.length > 0}
              {#each ratings as rating}
                <tr>
                  <td>{rating.place}</td>
                  <td>{rating.name}</td>
                  <td>{rating.result}</td>
                </tr>
              {/each}
            {:else}
              <tr>
                <td colspan="3" class="no-data">Нет данных для отображения</td>
              </tr>
            {/if}
          </tbody>
        </table>
      </div>
    </main>
  </div>
</div>

<style>
  .rating-page {
    min-height: 100vh;
    padding: 2rem;
    background: #f8f9fa;
  }
  
  .rating-container {
    display: flex;
    max-width: 1400px;
    margin: 0 auto;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    min-height: 80vh;
  }
  
  /* Боковая панель с дисциплинами */
  .disciplines-sidebar {
    width: 300px;
    background: #f8f9fa;
    border-right: 1px solid #e9ecef;
    padding: 1.5rem;
  }
  
  .disciplines-sidebar h2 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    color: #333;
    font-size: 1.5rem;
  }
  
  .disciplines-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .discipline-item {
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.95rem;
    line-height: 1.4;
  }
  
  .discipline-item:hover {
    background: #e9ecef;
  }
  
  .discipline-item.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
  
  /* Основная область */
  .rating-main {
    flex: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
  }
  
  .rating-header h1 {
    margin-top: 0;
    margin-bottom: 1.5rem;
    color: #333;
    font-size: 1.8rem;
  }
  
  .rating-table-container {
    flex: 1;
    overflow: auto;
  }
  
  .rating-table {
    width: 100%;
    border-collapse: collapse;
    background: #fff;
  }
  
  .rating-table th,
  .rating-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
  }
  
  .rating-table th {
    background: #f8f9fa;
    font-weight: 600;
    color: #495057;
    position: sticky;
    top: 0;
  }
  
  .rating-table tbody tr:hover {
    background: #f8f9fa;
  }
  
  .rating-table td {
    color: #495057;
  }
  
  .no-data {
    text-align: center;
    color: #6c757d;
    font-style: italic;
    padding: 2rem;
  }
  
  @media (max-width: 992px) {
    .rating-container {
      flex-direction: column;
    }
    
    .disciplines-sidebar {
      width: 100%;
      border-right: none;
      border-bottom: 1px solid #e9ecef;
    }
    
    .rating-page {
      padding: 1rem;
    }
    
    .rating-main {
      padding: 1.5rem;
    }
  }
  
  @media (max-width: 576px) {
    .rating-page {
      padding: 0.5rem;
    }
    
    .rating-container {
      border-radius: 0;
    }
    
    .disciplines-sidebar,
    .rating-main {
      padding: 1rem;
    }
    
    .rating-table th,
    .rating-table td {
      padding: 0.75rem 0.5rem;
      font-size: 0.9rem;
    }
  }
</style>