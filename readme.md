### Пет-проект по созданию службы доставки готовой еды на базе телеграмм бота (Telegram API) и возможностей предоставляемых Telegram WebApp.

### Цель:
Создать/написать и оформить телеграм-бота предоставляющего возможность 
пользователю заказать готовую еду из меню реализованного на базе 
возможностей Telegram WebApp.
<br>
В качестве источника информации был использован: 
<a href="https://klient-vsegda-love.ru/">Клиент всегда Love</a>
<br>
<a href="https://fedorsannikov1988.github.io/index.html">Меню</a> 
использующее возможности Telegram WebApp реализовано в этом проекте: 
<a href="https://github.com/FedorSannikov1988/FedorSannikov1988.github.io.git">Telegram WebApp</a>.

### Технологии и инструменты:
- Язык программирования: Python версии 3.10; 
- СУБД: PostgreSQL версии 14 управляемая по средствам SQLAlchemy версии 2.0.22;
- Инструменты разработки: IDE PyCharm .
- Взаимодействие с Telegram API: aiogram 3.0.0
- Версионный контроль: Git.

<details><summary><strong>Структура базы данных (одна картинка):</strong></summary>

![database_structure](/pictures/database_structure_v1.jpg "database_structure") 

</details>

<br>

<details><summary><strong>Пример работы (картинки):</strong></summary>

#### Начало работы:

![start1](/pictures/bot_start_1.jpg "start1") 

#### Команда /start:

![start2](/pictures/bot_start_2.jpg "start2")

#### Команда /help:

![help](/pictures/bot_help.jpg "help") 

#### Выбор категории устройства (команда /catalog):

![catalog_categories](/pictures/bot_catalog_categories.jpg "catalog_categories")

#### Выбор производителя устройства:

![catalog_manufacturer](/pictures/bot_catalog_manufacturer.jpg "catalog_manufacturer")

#### Выбор по названию/модели устройства:

![catalog_name_devices](/pictures/bot_catalog_name_device.jpg "catalog_name_devices")

#### Вывод информации о выбранном устройстве вариант №1 (без прокрутки):

![catalog_name_device_and_picture](/pictures/bot_catalog_name_device_and_picture.jpg "catalog_name_device_and_picture")

#### Вывод информации о выбранном устройстве (нажата кнопка "Все устройства" в предыдущем меню) вариант №2 (с прокруткой):

![catalog_all_device](/pictures/bot_catalog_all_device.jpg "catalog_all_device")

</details>

### Запуск:

1. Скачать архив с файлом базы данных и медиа файлами можно по ссылке:
<a href="https://disk.yandex.ru/d/EAYgSwzjhibbJA">база данных и медиа файлы (картинки)</a>
и разместить: ***<u>"директорию размещения проекта/product_catalog/src/db_api/database
(папка из скаченного архива)"</u>***. Так же для создания или работы с базой данных можно использовать SQL-script расположенный:
***<u>"директория размещения проекта/product_catalog/src/db_api/database/for_create_shop_database.sql"</u>***.
Однако при создании базы данных таким образом необходимо учитывать отсутствие медиа файлов.
2. Создать файл .env (использутся для хранения переменных окружения 
в проекте) в дирректории telegram_bot: ***<u>"директория размещения 
проекта/telegram_bot/.env"</u>*** после чего указать в нем токен для телеграм-бота 
в переменной TOKEN_FOR_BOT (следующим образом TOKEN_FOR_BOT=).
3. Установить все зависимости/библиотеки указанные в requirements.txt
4. Запустить выполнение файла app.py.

