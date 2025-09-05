# 🚀 Quick Start Guide

## Запуск проекта за 5 минут

### Windows (PowerShell)
```powershell
# 1. Клонируйте репозиторий
git clone <your-repo-url>
cd Client_Churn_analyzer

# 2. Запустите автоматическую настройку
.\scripts\setup.bat

# 3. Откройте браузер
start http://localhost:8000
```

### Linux/macOS
```bash
# 1. Клонируйте репозиторий
git clone <your-repo-url>
cd Client_Churn_analyzer

# 2. Запустите автоматическую настройку
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Откройте браузер
open http://localhost:8000
```

## 🎯 Что вы увидите

### 1. **Dashboard** - Главная страница
- Статистика по клиентам
- Графики churn rate
- AI взаимодействия в реальном времени

### 2. **Customer Analysis** - Анализ клиентов
- Предсказание churn с объяснениями
- Сегментация клиентов
- Метрики удовлетворенности

### 3. **AI Chat** - ИИ помощник
- Интеллектуальный чат-бот
- LangGraph workflow
- Контекстные ответы

### 4. **Call Center** - Автоматизированный колл-центр
- Симуляция звонков
- AI обработка запросов
- Эскалация к людям

### 5. **Computer Vision** - Компьютерное зрение
- Анализ изображений
- Распознавание лиц и объектов
- OCR для текста

## 🔧 Управление

### Просмотр логов
```bash
docker-compose logs -f hotel-ai-app
```

### Остановка сервисов
```bash
docker-compose down
```

### Перезапуск
```bash
docker-compose restart
```

### Обновление
```bash
docker-compose pull
docker-compose up -d
```

## 📱 Доступные сервисы

- **Приложение**: http://localhost:8000
- **API документация**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Ollama**: http://localhost:11434

## 🎯 Демонстрация для интервью

### Сценарий 1: Churn Analysis
1. Откройте Customer Analysis
2. Покажите предсказания churn
3. Объясните feature importance
4. Продемонстрируйте бизнес-инсайты

### Сценарий 2: AI Chat
1. Откройте AI Chat
2. Спросите: "Show me customer churn analysis"
3. Покажите LangGraph workflow
4. Демонстрируйте контекстные ответы

### Сценарий 3: Call Center
1. Запустите симуляцию звонка
2. Покажите AI обработку
3. Демонстрируйте эскалацию
4. Покажите метрики производительности

### Сценарий 4: Computer Vision
1. Загрузите изображение отеля
2. Покажите детекцию лиц
3. Демонстрируйте распознавание объектов
4. Подчеркните применение в безопасности

## 🏗️ Архитектура проекта

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │   FastAPI Backend │    │   AI Services   │
│                 │    │                 │    │                 │
│ • Dashboard     │◄──►│ • REST API      │◄──►│ • LangGraph     │
│ • AI Chat       │    │ • Authentication│    │ • Computer Vision│
│ • Call Center   │    │ • Data Models   │    │ • ML Models     │
│ • Analytics     │    │ • Business Logic│    │ • Vector DB     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎯 Ключевые особенности

### ✅ Соответствие требованиям Архитех ИИ
- **Python & JavaScript/TypeScript** ✅
- **FastAPI** ✅
- **React** ✅
- **CI/CD** ✅
- **NLP (LangChain/LangGraph)** ✅
- **Computer Vision** ✅
- **Технический английский** ✅

### 🚀 Современные технологии
- Docker контейнеризация
- Микросервисная архитектура
- Redis кэширование
- PostgreSQL + ChromaDB
- GitHub Actions CI/CD

### 🎨 Пользовательский интерфейс
- Современный дизайн с Ant Design
- Интерактивные графики (Recharts)
- Адаптивная верстка
- Темная/светлая тема

## 📚 Дополнительная документация

- **README.md** - Полное описание проекта
- **docs/API.md** - Детальная документация API
- **docs/DEPLOYMENT.md** - Руководство по развертыванию
- **INTERVIEW_GUIDE.md** - Гид для интервью

## 🎉 Готово к демонстрации!

Проект полностью готов для демонстрации на интервью в **Архитех ИИ**. Все компоненты работают, документация написана, и архитектура соответствует современным стандартам разработки.

**Удачи на интервью! 🚀**
