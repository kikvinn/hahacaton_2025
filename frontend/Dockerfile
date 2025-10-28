# frontend/Dockerfile
FROM oven/bun:1 AS base
WORKDIR /app

# Копируем зависимости
COPY package.json bun.lockb* ./
RUN bun install --frozen-lockfile

# Копируем исходники
COPY . .

# Собираем приложение
RUN bun run build

# Финальный образ (легковесный)
FROM oven/bun:1 AS runner
WORKDIR /app

# Устанавливаем serve или используем адаптер node
RUN bun add -g serve

COPY --from=base /app/build ./build

EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]