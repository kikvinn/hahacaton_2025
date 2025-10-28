<svelte:head>
  <title>Мероприятия — Polyathlon</title>
</svelte:head>

<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  
  // Переменные состояния
  let events = [];
  let isModalOpen = false;
  let isFormVisible = false;
  let currentEvent = null;
  let loading = false;
  let error = null;
  
  // Данные для формы
  let eventName = '';
  let eventDiscipline = '';
  let eventDate = '';
  
  // Список дисциплин
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
  
  // Загрузка мероприятий при монтировании компонента
  onMount(() => {
    loadEvents();
  });
  
  // Загрузка мероприятий с сервера
  async function loadEvents() {
    try {
      loading = true;
      error = null;
      
      const response = await fetch('/api/events', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (response.ok) {
        events = await response.json();
      } else if (response.status === 401) {
        // Пользователь не авторизован
        goto('/login');
      } else {
        throw new Error(`Ошибка загрузки: ${response.status}`);
      }
    } catch (err) {
      console.error('Ошибка загрузки мероприятий:', err);
      error = 'Не удалось загрузить мероприятия. Попробуйте обновить страницу.';
    } finally {
      loading = false;
    }
  }
  
  // Открытие модального окна для создания нового мероприятия
  function openCreateModal() {
    isModalOpen = true;
    isFormVisible = true;
    currentEvent = null;
    
    // Сброс формы
    eventName = '';
    eventDiscipline = '';
    eventDate = '';
  }
  
  // Закрытие модального окна
  function closeModal() {
    isModalOpen = false;
    isFormVisible = false;
    currentEvent = null;
    error = null;
  }
  
  // Сохранение мероприятия
  async function saveEvent() {
    // Проверка валидности формы
    if (!eventName.trim()) {
      error = 'Пожалуйста, введите название мероприятия';
      return;
    }
    
    if (!eventDiscipline) {
      error = 'Пожалуйста, выберите дисциплину';
      return;
    }
    
    if (!eventDate) {
      error = 'Пожалуйста, выберите дату проведения';
      return;
    }
    
    try {
      loading = true;
      error = null;
      
      const eventData = {
        name: eventName.trim(),
        discipline: eventDiscipline,
        date: eventDate
      };
      
      const response = await fetch('/api/events', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData)
      });
      
      if (response.ok) {
        const newEvent = await response.json();
        events = [...events, newEvent];
        closeModal();
      } else if (response.status === 401) {
        // Пользователь не авторизован
        goto('/login');
      } else if (response.status === 403) {
        error = 'У вас нет прав для создания мероприятий';
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Ошибка при создании мероприятия');
      }
    } catch (err) {
      console.error('Ошибка сохранения мероприятия:', err);
      error = err.message || 'Не удалось создать мероприятие. Попробуйте позже.';
    } finally {
      loading = false;
    }
  }
  
  // Обработка клика вне модального окна
  function handleBackdropClick(event) {
    if (event.target.classList.contains('modal-backdrop')) {
      closeModal();
    }
  }
</script>

<div class="events-page">
  <div class="events-header">
    <h1>Мероприятия</h1>
    <button class="btn-new" on:click={openCreateModal} disabled={loading}>
      {loading ? '...' : 'NEW'}
    </button>
  </div>
  
  {#if loading && events.length === 0}
    <div class="loading">
      <p>Загрузка мероприятий...</p>
    </div>
  {:else if error && events.length === 0}
    <div class="error-message">
      <p>{error}</p>
      <button class="btn-primary" on:click={loadEvents}>Повторить попытку</button>
    </div>
  {:else}
    <div class="events-grid">
      {#if events.length > 0}
        {#each events as event}
          <div class="event-card">
            <div class="event-card-header">
              <h3 class="event-title">{event.name}</h3>
              <span class="event-status {event.status?.toLowerCase().replace(' ', '-') || 'запланировано'}">
                {event.status || 'Запланировано'}
              </span>
            </div>
            <div class="event-details">
              <p class="event-discipline"><strong>Дисциплина:</strong> {event.discipline}</p>
              <p class="event-date"><strong>Дата:</strong> {event.date}</p>
            </div>
          </div>
        {/each}
      {:else}
        <div class="no-events">
          <p>Пока нет запланированных мероприятий</p>
          <button class="btn-primary" on:click={openCreateModal} disabled={loading}>
            Создать первое мероприятие
          </button>
        </div>
      {/if}
    </div>
  {/if}
</div>

<!-- Модальное окно для создания мероприятия -->
{#if isModalOpen}
  <div class="modal-backdrop" on:click={handleBackdropClick}>
    <div class="modal-content">
      <div class="modal-header">
        <h2>{currentEvent ? 'Редактировать мероприятие' : 'Создать новое мероприятие'}</h2>
        <button class="modal-close" on:click={closeModal} disabled={loading}>×</button>
      </div>
      
      {#if isFormVisible}
        <div class="modal-body">
          {#if error}
            <div class="error-message-small">
              <p>{error}</p>
            </div>
          {/if}
          
          <form class="event-form" on:submit|preventDefault={saveEvent}>
            <div class="form-group">
              <label for="eventName">Название мероприятия:</label>
              <input 
                type="text" 
                id="eventName" 
                bind:value={eventName}
                placeholder="Введите название мероприятия"
                required
                disabled={loading}
              />
            </div>
            
            <div class="form-group">
              <label for="eventDiscipline">Дисциплина:</label>
              <select 
                id="eventDiscipline" 
                bind:value={eventDiscipline}
                required
                disabled={loading}
              >
                <option value="">Выберите дисциплину</option>
                {#each disciplines as discipline}
                  <option value={discipline}>{discipline}</option>
                {/each}
              </select>
            </div>
            
            <div class="form-group">
              <label for="eventDate">Дата проведения:</label>
              <input 
                type="date" 
                id="eventDate" 
                bind:value={eventDate}
                required
                disabled={loading}
              />
            </div>
            
            <div class="form-actions">
              <button 
                type="button" 
                class="btn-outline" 
                on:click={closeModal}
                disabled={loading}
              >
                Отмена
              </button>
              <button 
                type="submit" 
                class="btn-primary"
                disabled={loading}
              >
                {loading ? 'Сохранение...' : 'Сохранить'}
              </button>
            </div>
          </form>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .events-page {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    min-height: calc(100vh - 120px);
  }
  
  .events-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .events-header h1 {
    margin: 0;
    color: #333;
    font-size: 2rem;
  }
  
  .btn-new {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 1.5rem;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
  }
  
  .btn-new:hover:not(:disabled) {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  }
  
  .btn-new:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .events-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
  }
  
  .event-card {
    background: #fff;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 1px solid #e9ecef;
  }
  
  .event-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }
  
  .event-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
  }
  
  .event-title {
    margin: 0 0 0.5rem 0;
    color: #333;
    font-size: 1.25rem;
    line-height: 1.4;
  }
  
  .event-status {
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    white-space: nowrap;
  }
  
  .event-status.запланировано,
  .event-status.запланирован {
    background: #e3f2fd;
    color: #1976d2;
  }
  
  .event-status.регистрация-открыта {
    background: #e8f5e9;
    color: #388e3c;
  }
  
  .event-status.идет-регистрация,
  .event-status.идет {
    background: #fff3e0;
    color: #f57c00;
  }
  
  .event-status.завершено,
  .event-status.завершен {
    background: #f5f5f5;
    color: #666;
  }
  
  .event-details p {
    margin: 0.5rem 0;
    color: #666;
    font-size: 0.95rem;
  }
  
  .no-events {
    grid-column: 1 / -1;
    text-align: center;
    padding: 3rem;
    background: #f8f9fa;
    border-radius: 8px;
  }
  
  .no-events p {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 1.5rem;
  }
  
  .loading, .error-message {
    text-align: center;
    padding: 2rem;
  }
  
  .loading p, .error-message p {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 1rem;
  }
  
  .error-message-small {
    background: #ffebee;
    color: #c62828;
    padding: 0.75rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    font-size: 0.9rem;
  }
  
  /* Модальное окно */
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-content {
    background: #fff;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e9ecef;
  }
  
  .modal-header h2 {
    margin: 0;
    color: #333;
    font-size: 1.5rem;
  }
  
  .modal-close {
    background: none;
    border: none;
    font-size: 1.8rem;
    cursor: pointer;
    color: #999;
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal-close:hover:not(:disabled) {
    color: #333;
  }
  
  .modal-close:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .modal-body {
    padding: 1.5rem;
  }
  
  .event-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .form-group label {
    font-weight: 500;
    color: #333;
  }
  
  .form-group input,
  .form-group select {
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .form-group input:focus,
  .form-group select:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
  }
  
  .form-group input:disabled,
  .form-group select:disabled {
    background: #f5f5f5;
    cursor: not-allowed;
  }
  
  .form-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 1rem;
  }
  
  .btn {
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    border: none;
    font-weight: 500;
    transition: all 0.2s ease;
  }
  
  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .btn-outline {
    background: transparent;
    color: #667eea;
    border: 1px solid #667eea;
  }
  
  .btn-outline:hover:not(:disabled) {
    background: #667eea;
    color: white;
  }
  
  .btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
  
  .btn-primary:hover:not(:disabled) {
    opacity: 0.9;
  }
  
  @media (max-width: 768px) {
    .events-page {
      padding: 1rem;
    }
    
    .events-header {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }
    
    .events-grid {
      grid-template-columns: 1fr;
    }
    
    .event-card-header {
      flex-direction: column;
      gap: 0.5rem;
      align-items: flex-start;
    }
    
    .form-actions {
      flex-direction: column;
    }
    
    .modal-content {
      width: 95%;
      margin: 1rem;
    }
  }
</style>