<svelte:head>
  <title>Регистрация — Polyathlon</title>
</svelte:head>

<script>
let formData = {
    email: '',
    password: '',
    role: '',
    lastName: '',
    firstName: '',
    middleName: '',
    birthDate: '',
    height: '',
    weight: '',
    disciplines: [],
    roleOpen: false,
    disciplineOpen: false
  };

  const roles = [
    { value: 'participant', label: 'Участник' },
    { value: 'organizer', label: 'Организатор' },
    { value: 'judge', label: 'Судья' }
  ];

  const availableDisciplines = [
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

  function selectRole(r) {
    formData.role = r.label;
    formData.roleOpen = false;
  }

  function toggleRole() {
    formData.roleOpen = !formData.roleOpen;
    if (formData.roleOpen) formData.disciplineOpen = false;
  }

  function toggleDiscipline() {
    formData.disciplineOpen = !formData.disciplineOpen;
    if (formData.disciplineOpen) formData.roleOpen = false;
  }

  function selectDiscipline(discipline) {
    if (!formData.disciplines.includes(discipline)) {
      formData.disciplines = [...formData.disciplines, discipline];
    }
  }

  function removeDiscipline(discipline) {
    formData.disciplines = formData.disciplines.filter(d => d !== discipline);
  }

  function handleClickOutside(event) {
    if (formData.roleOpen && !event.target.closest('.custom-select.role')) {
      formData.roleOpen = false;
    }
    if (formData.disciplineOpen && !event.target.closest('.custom-select.discipline')) {
      formData.disciplineOpen = false;
    }
  }

  // Функция для автоматического форматирования даты
  function formatBirthDate(value) {
    // Убираем все нецифровые символы
    let cleanValue = value.replace(/\D/g, '');
    
    // Ограничиваем длину до 8 символов (ддммгггг)
    cleanValue = cleanValue.substring(0, 8);
    
    // Форматируем с точками
    let formattedValue = '';
    for (let i = 0; i < cleanValue.length; i++) {
      if (i === 2 || i === 4) {
        formattedValue += '.';
      }
      formattedValue += cleanValue[i];
    }
    
    return formattedValue;
  }

  // Обработчик ввода даты рождения
  function handleBirthDateInput(e) {
    const inputValue = e.target.value;
    const formattedValue = formatBirthDate(inputValue);
    formData.birthDate = formattedValue;
  }

  // Закрытие dropdown при клике вне его области
  typeof window !== 'undefined' && window.addEventListener('click', handleClickOutside);

  async function handleSubmit(e) {
    e.preventDefault();
    
    // Создаем копию formData без служебных полей
    const { roleOpen, disciplineOpen, ...submitData } = formData;
    
    console.log('Отправляемые данные:', submitData);
    
    try {
      const response = await fetch('http://localhost:8080/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(submitData)
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Успех:', result);
        // Здесь можно перенаправить пользователя или показать сообщение об успехе
      } else {
        console.error('Ошибка сервера:', response.statusText);
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
    <h2>Создать аккаунт</h2>
    <form class="auth-form" on:submit={handleSubmit}>
      <div class="form-group">
        <label>E-mail *</label>
        <input type="email" bind:value={formData.email} required />
      </div>

      <div class="form-group">
        <label>Пароль *</label>
        <input type="password" bind:value={formData.password} required />
      </div>

      <div class="form-group">
        <label>Роль *</label>
        <div class="custom-select role" on:click|stopPropagation={toggleRole}>
          <div class="select-trigger">
            {#if formData.role}
              {formData.role}
            {:else}
              Выберите роль
            {/if}
          </div>
          {#if formData.roleOpen}
            <div class="select-dropdown">
              {#each roles as r}
                <div class="select-option" on:click|stopPropagation={() => selectRole(r)}>
                  {r.label}
                </div>
              {/each}
            </div>
          {/if}
        </div>
      </div>

      <div class="form-group">
        <label>Фамилия *</label>
        <input type="text" bind:value={formData.lastName} required />
      </div>

      <div class="form-group">
        <label>Имя *</label>
        <input type="text" bind:value={formData.firstName} required />
      </div>

      <div class="form-group">
        <label>Отчество</label>
        <input type="text" bind:value={formData.middleName} />
      </div>

      <div class="form-group">
        <label>Дата рождения</label>
        <input 
          type="text" 
          bind:value={formData.birthDate} 
          on:input={handleBirthDateInput}
          placeholder="дд.мм.гггг" 
          maxlength="10"
        />
      </div>

      <div class="form-group">
        <label>Рост (см)</label>
        <input type="number" bind:value={formData.height} />
      </div>

      <div class="form-group">
        <label>Вес (кг)</label>
        <input type="number" bind:value={formData.weight} />
      </div>

      <div class="form-group">
        <label>Дисциплины</label>
        <div class="custom-select discipline" on:click|stopPropagation={toggleDiscipline}>
          <div class="select-trigger">
            Выберите дисциплины
          </div>
          {#if formData.disciplineOpen}
            <div class="select-dropdown">
              {#each availableDisciplines as discipline}
                <div class="select-option" on:click|stopPropagation={() => selectDiscipline(discipline)}>
                  {discipline}
                </div>
              {/each}
            </div>
          {/if}
        </div>
        
        <!-- Отображение выбранных дисциплин -->
        {#if formData.disciplines.length > 0}
          <div class="selected-disciplines">
            {#each formData.disciplines as discipline, i}
              <span class="discipline-tag">
                {discipline}
                <button type="button" class="remove-discipline" on:click|stopPropagation={() => removeDiscipline(discipline)}>×</button>
              </span>
            {/each}
          </div>
        {/if}
      </div>

      <button type="submit" class="btn btn-primary full-width">Зарегистрироваться</button>
    </form>
    <p class="mt-1">Уже есть аккаунт? <a href="/login">Войти</a></p>
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
    max-width: 500px;
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
    font-weight: 500;
  }

  .form-group input,
  .form-group textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
    box-sizing: border-box;
  }

  .full-width {
    width: 100%;
  }

  .mt-1 {
    text-align: center;
    margin-top: 1rem;
  }

  /* Custom Select */
  .custom-select {
    position: relative;
    width: 100%;
  }

  .select-trigger {
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    background: #fff;
    cursor: pointer;
    user-select: none;
    text-align: left;
  }

  .select-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #fff;
    border: 1px solid #ccc;
    border-top: none;
    border-radius: 0 0 4px 4px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    max-height: 200px;
    overflow-y: auto;
  }

  .select-option {
    padding: 0.75rem;
    cursor: pointer;
    text-align: left;
  }

  .select-option:hover {
    background-color: #f5f5f5;
  }

  .btn {
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
  }

  .btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  /* Selected Disciplines */
  .selected-disciplines {
    margin-top: 0.5rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .discipline-tag {
    background: #e9ecef;
    border-radius: 12px;
    padding: 0.25rem 0.75rem;
    font-size: 0.875rem;
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }

  .remove-discipline {
    background: none;
    border: none;
    color: #6c757d;
    cursor: pointer;
    font-size: 1rem;
    line-height: 1;
    padding: 0;
    width: auto;
  }

  .remove-discipline:hover {
    color: #dc3545;
  }
</style>