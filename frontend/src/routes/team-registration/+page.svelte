<svelte:head>
  <title>Регистрация команд — Polyathlon</title>
</svelte:head>

<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
    import { json } from '@sveltejs/kit';

  // Переменные состояния
  let teams = [];
  let isModalOpen = false;
  let isFormVisible = false;
  let currentTeam = null;
  let loading = false;
  let error = null;

  // Данные для формы
  let teamName = '';
  let teamDiscipline = '';
  let teamMembers = [''];

  // Список дисциплин (тот же, что и для мероприятий)
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

  // Загрузка команд при монтировании компонента
  onMount(() => {
    loadTeams();
  });

  // Загрузка команд с сервера
  async function loadTeams() {
    try {
      loading = true;
      error = null;

      const response = await fetch('/api/teams', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        teams = await response.json();
      } else if (response.status === 401) {
        // Пользователь не авторизован
        goto('/login');
      } else {
        throw new Error(`Ошибка загрузки: ${response.status}`);
      }
    } catch (err) {
      console.error('Ошибка загрузки команд:', err);
      error = 'Не удалось загрузить команды. Попробуйте обновить страницу.';
    } finally {
      loading = false;
    }
  }

  // Открытие модального окна для создания новой команды
  function openCreateModal() {
    isModalOpen = true;
    isFormVisible = true;
    currentTeam = null;

    // Сброс формы
    teamName = '';
    teamDiscipline = '';
    teamMembers = [''];
  }

  // Закрытие модального окна
  function closeModal() {
    isModalOpen = false;
    isFormVisible = false;
    currentTeam = null;
    error = null;
  }

  // Добавление поля для нового участника
  function addMemberField() {
    teamMembers = [...teamMembers, ''];
  }

  // Удаление поля участника
  function removeMemberField(index) {
    if (teamMembers.length > 1) {
      teamMembers = teamMembers.filter((_, i) => i !== index);
    }
  }

  // Обновление значения поля участника
  function updateMember(index, value) {
    teamMembers[index] = value;
  }

  // Сохранение команды
  async function saveTeam() {
    // Проверка валидности формы
    if (!teamName.trim()) {
      error = 'Пожалуйста, введите название команды';
      return;
    }

    if (!teamDiscipline) {
      error = 'Пожалуйста, выберите дисциплину';
      return;
    }

    const validMembers = teamMembers.filter(member => member.trim() !== '');
    if (validMembers.length === 0) {
      error = 'Пожалуйста, добавьте хотя бы одного участника';
      return;
    }

    try {
      loading = true;
      error = null;

      const teamData = {
        name: teamName.trim(),
        discipline: teamDiscipline,
        members: validMembers.map((member, index) => ({
          fullName: member.trim(),
          order: index + 1
        }))
      };
      console.log(JSON.stringify(teamData))
      const response = await fetch('/api/teams', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(teamData)
      });

      if (response.ok) {
        const newTeam = await response.json();
        teams = [...teams, newTeam];
        closeModal();
      } else if (response.status === 401) {
        // Пользователь не авторизован
        goto('/login');
      } else if (response.status === 403) {
        error = 'У вас нет прав для создания команд';
      } else if (response.status === 400) {
        const errorData = await response.json();
        error = errorData.message || 'Некорректные данные для создания команды';
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Ошибка при создании команды');
      }
    } catch (err) {
      console.error('Ошибка сохранения команды:', err);
      error = err.message || 'Не удалось создать команду. Попробуйте позже.';
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

  // Форматирование списка участников для отображения
  function formatMembersList(members) {
    if (!members || members.length === 0) return 'Нет участников';
    if (members.length === 1) return members[0].fullName || members[0];
    return `${members.length} участников`;
  }
</script>

<div class="teams-page">
  <div class="teams-header">
    <h1>Регистрация команд</h1>
    <button class="btn-new" on:click={openCreateModal} disabled={loading}>
      {loading ? '...' : 'NEW'}
    </button>
  </div>

  {#if loading && teams.length === 0}
    <div class="loading">
      <p>Загрузка команд...</p>
    </div>
  {:else if error && teams.length === 0}
    <div class="error-message">
      <p>{error}</p>
      <button class="btn-primary" on:click={loadTeams}>Повторить попытку</button>
    </div>
  {:else}
    <div class="teams-grid">
      {#if teams.length > 0}
        {#each teams as team}
          <div class="team-card">
            <div class="team-card-header">
              <h3 class="team-title">{team.name}</h3>
              <span class="team-discipline-badge">
                {team.discipline}
              </span>
            </div>
            <div class="team-details">
              <p class="team-members-count">
                <strong>Участники:</strong> {formatMembersList(team.members)}
              </p>
              <p class="team-created">
                <strong>Создана:</strong> {new Date(team.createdAt).toLocaleDateString('ru-RU')}
              </p>
            </div>
          </div>
        {/each}
      {:else}
        <div class="no-teams">
          <p>Пока нет зарегистрированных команд</p>
          <button class="btn-primary" on:click={openCreateModal} disabled={loading}>
            Создать первую команду
          </button>
        </div>
      {/if}
    </div>
  {/if}
</div>

<!-- Модальное окно для создания команды -->
{#if isModalOpen}
  <div class="modal-backdrop" on:click={handleBackdropClick}>
    <div class="modal-content">
      <div class="modal-header">
        <h2>{currentTeam ? 'Редактировать команду' : 'Создать новую команду'}</h2>
        <button class="modal-close" on:click={closeModal} disabled={loading}>×</button>
      </div>

      {#if isFormVisible}
        <div class="modal-body">
          {#if error}
            <div class="error-message-small">
              <p>{error}</p>
            </div>
          {/if}

          <form class="team-form" on:submit|preventDefault={saveTeam}>
            <div class="form-group">
              <label for="teamName">Название команды:</label>
              <input
                type="text"
                id="teamName"
                bind:value={teamName}
                placeholder="Введите название команды"
                required
                disabled={loading}
              />
            </div>

            <div class="form-group">
              <label for="teamDiscipline">Дисциплина:</label>
              <select
                id="teamDiscipline"
                bind:value={teamDiscipline}
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
              <label>Участники команды:</label>
              <div class="members-list">
                {#each teamMembers as member, i}
                  <div class="member-input-row">
                    <input
                      type="text"
                      placeholder={`ФИО участника ${i + 1}`}
                      bind:value={teamMembers[i]}
                      disabled={loading}
                    />
                    {#if teamMembers.length > 1}
                      <button
                        type="button"
                        class="btn-remove-member"
                        on:click={() => removeMemberField(i)}
                        disabled={loading}
                      >
                        ×
                      </button>
                    {/if}
                  </div>
                {/each}
                <button
                  type="button"
                  class="btn-add-member"
                  on:click={addMemberField}
                  disabled={loading}
                >
                  + Добавить участника
                </button>
              </div>
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
  .teams-page {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    min-height: calc(100vh - 120px);
  }

  .teams-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  .teams-header h1 {
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

  .teams-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
  }

  .team-card {
    background: #fff;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 1px solid #e9ecef;
  }

  .team-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }

  .team-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .team-title {
    margin: 0 0 0.5rem 0;
    color: #333;
    font-size: 1.25rem;
    line-height: 1.4;
    flex: 1;
    min-width: 0;
  }

  .team-discipline-badge {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    white-space: nowrap;
  }

  .team-details p {
    margin: 0.5rem 0;
    color: #666;
    font-size: 0.95rem;
  }

  .no-teams {
    grid-column: 1 / -1;
    text-align: center;
    padding: 3rem;
    background: #f8f9fa;
    border-radius: 8px;
  }

  .no-teams p {
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
    max-width: 600px;
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

  .team-form {
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

  .members-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .member-input-row {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .member-input-row input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }

  .member-input-row input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
  }

  .btn-remove-member {
    background: #ffebee;
    color: #c62828;
    border: 1px solid #ffcdd2;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
  }

  .btn-remove-member:hover:not(:disabled) {
    background: #ffcdd2;
  }

  .btn-add-member {
    background: transparent;
    color: #667eea;
    border: 1px dashed #667eea;
    border-radius: 4px;
    padding: 0.75rem;
    cursor: pointer;
    font-size: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }

  .btn-add-member:hover:not(:disabled) {
    background: #f0f4ff;
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
    .teams-page {
      padding: 1rem;
    }

    .teams-header {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }

    .teams-grid {
      grid-template-columns: 1fr;
    }

    .team-card-header {
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

    .member-input-row {
      flex-direction: column;
      align-items: stretch;
    }

    .btn-remove-member {
      align-self: flex-end;
    }
  }
</style>