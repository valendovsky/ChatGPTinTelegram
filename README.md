# ChatGPTinTelegram

<p align="center">
   <img src="https://img.shields.io/badge/Python-3.9-blue" alt="Python Version">
   <img src="https://img.shields.io/badge/Aiogram-3.0.0b7-green" alt="Aiogram Version">
   <img src="https://img.shields.io/badge/OpenAI-0.27.6-ff69b4" alt="OpenAI Version">
   <img src="https://img.shields.io/badge/version-1.0-yellow" alt="Application Version">
   <img src="https://img.shields.io/badge/license-MIT-red" alt="License">
</p>

## Telegram bot with ChatGPT.

### About
This Telegram bot uses the Openal API to access ChatGPT.
Each user's chat has its own context.
The administrator can allow access to the bot only for subscribers.
The administrator has private commands to control the bot.

### Documentation
The project uses the following libraries:
 - aiogram-v3.0.0b7
 - openai-v0.27.6

The following variables must be set in the Environment variable:
 - TG_API_KEY - Telegram API token;
 - ADMIN_ID - admin ID;
 - OPENAI_API_KEY - OpenAI API key;
 - SUBSCRIBER_1 - by default, the ID of one subscriber is provided.

The Subscribers list from the configuration file must contain IDs of all subscribers of the bot.
They will be able to use the bot as usual.
If you get a list of subscribers from a separate source, then write a module yourself to access this source.

### Distribute
- [Docker Hub](https://hub.docker.com/r/valendovsky/chatgpt-in-telegram)

### Developers
- [Valendovsky](https://github.com/valendovsky)

### License
Project ChatGPTinTelegram is distributed under the MIT license.

---

## Телеграм бот с интегрированным ChatGPT.

### О проекте
Это Телеграм бот, в который интегрирован ChatGPT через OpenAI API.
Для каждого пользователя бота запоминается свой контекст.
Есть возможность предоставить доступ к боту только для указанных подписчиков.
Существуют приватные команды управления ботом для администратора.

### Документация
В проекте используются библиотеки:
 - aiogram-v3.0.0b7
 - openai-v0.27.6

Через переменные окружения необходимо предоставить следующие значения:
 - TG_API_KEY - API токен Вашего Телеграм бота;
 - ADMIN_ID - ID администратора бота;
 - OPENAI_API_KEY - код доступа к API OpenAI;
 - SUBSCRIBER_1 - по умолчанию предоставляется ID одного подписчика.

В конфигурационном файле приложения в списке SUBSCRIBERS можно перечислить всех подписчиков, которым будет предоставлен отдельный доступ к боту.
Или самостоятельно добавить модуль, который будет получать этот список из необходимого Вам источника.

### Загрузить
- [Docker Hub](https://hub.docker.com/r/valendovsky/chatgpt-in-telegram)

### Разработчики
- [Valendovsky](https://github.com/valendovsky)

### Лицензия
Проект ChatGPTinTelegram распространяется под лицензией MIT.
