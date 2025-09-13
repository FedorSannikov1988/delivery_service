### Учебный проект по созданию службы доставки готовой еды на базе телеграмм бота (Telegram API) и возможностей предоставляемых Telegram WebApp.

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
- Инструменты разработки: IDE PyCharm ;
- Взаимодействие с Telegram API: aiogram 3.0.0 ;
- Версионный контроль: Git ;

<details><summary><strong>Структура базы данных (одна картинка):</strong></summary>

![database_structure](/pictures/database_structure.jpg "database_structure") 

</details>

<br>


<details><summary><strong>Пример работы (картинки):</strong></summary>

#### Начало работы:

![start1](/pictures/bot_start_work.png "start work") 

#### Команда /start:

![start2](/pictures/bot_command_start.png "command start")

#### Команда /help или кнопка Помощь:

![help](/pictures/bot_command_help.png "command help") 

#### Команда /manual или кнопка Инструкция:

![catalog_categories](/pictures/bot_command_manual.png "command manual")

#### Команда /developer или кнопка Разработчик:

![catalog_manufacturer](/pictures/bot_command_developer.png "command developer")

#### Команда /hide_menu или кнопка Скрыть меню:

![catalog_name_devices](/pictures/bot_command_hide_menu.png "command hide_menu")

#### Команда /reviews или кнопка Книга отзывов:

![catalog_name_devices](/pictures/bot_command_reviews.png "command reviews")

#### Зарегестрироваться:

![catalog_name_devices](/pictures/register.png "register")

#### Меню готовых блюд:

![catalog_name_devices](/pictures/menu.png "menu")

#### Доставка:

![catalog_name_devices](/pictures/delivery.png "delivery")

#### Получение данных из WebApp в боте (первая часть):

![catalog_name_devices](/pictures/order_part_one.png "order_part_one")

#### Получение данных из WebApp в боте (вторая часть):

![catalog_name_devices](/pictures/order_part_two.png "order_part_two")

#### Команда /orders:

![catalog_name_devices](/pictures/bot_command_my_orders.png "orders")

</details>

### Запуск:

1. Скачать архив с медиа файлами формата jpg по ссылке:
<a href="https://disk.yandex.ru/d/PbETbXgVILuDxA">медиа файлы (картинки)</a> 
и разместить: ***<u>"директорию размещения проекта/src/db_api/media
(папка из скаченного архива)"</u>***.
2. Создать файл .env (используется для хранения переменных окружения 
в проекте): ***<u>"директория размещения проекта/.env"</u>***.
3. Формат файла .env:

TOKEN_FOR_BOT=токен телеграм-бота

HOST_SERVER=адрес сервера PostgreSQL к примеру localhost (если сервер размещен на вашем ПК)

PORT_SERVER=номер порта сервера PostgreSQL для подключения обычно это 5432

USER_LOG_IN_SERVER=логин для входа на сервер к примеру postgres

#### ! ВАЖНО: пользователь указанный в USER_LOG_IN_SERVER должен иметь права на создание базы данных (так как мы будем создавать свою базу данных)!

PASSWORD_LOG_IN_SERVER=пароль необходимый для входа на сервер пользователю указанному в USER_LOG_IN_SERVER

NAME_CREATED_DATABASE=имя для создаваемой базы данных к примеру food_delivery_service_in_telegram

NAME_MANAGER_CREATED_DATABASE=имя для создаваемого пользователя управляющего базой данных к примеру user_for_food_delivery_service_in_telegram

PASSWORD_MANAGER_CREATED_DATABASE=пароль для пользователя указанного в NAME_MANAGER_CREATED_DATABASE 

TOKEN_FOR_UPAY=токен полученный у системы оплаты Юкassa .

URL_FOR_WEB_APP=https://fedorsannikov1988.github.io/index.html

URL_FOR_WEB_APP не менять так как это ссылка на WebApp Telegram .

Обратите внимание модуль create_db.py отвечает за создание базы данных 
на сервере PostgreSQL и при повторном запуске будет выведено сообщение 
в консоль: 
***<u>2023-11-13 02:49:24.822 | ERROR    | loader:<module>:75 - ОШИБКА: база данных "food_delivery_service_in_telegram" уже существует</u>***.
Это означает, что база данных уже сущесвует. Сообщение будет автоматически сохранено в logs.

Даза данных (таблица food) заполняется на основе содержания файла food.json расположенного в папке: ***<u>"директорию размещения проекта/src/db_api/fixtures"</u>***.

4. Установить все зависимости/библиотеки указанные в requirements.txt
5. Запустить выполнение файла app.py.
