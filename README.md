Проект LearnCardBot

Цель проекта:

    Разработать Telegram-бот для изучения английского языка.
    Бот будет предлагать различные варианты слов и проверять их правильный перевод.

Основные функциональные требования:

    Необходимо разработать программу-бота, которая должна выполнять следующие действия:

    Оф.1. Заполнить базу данных общим набором слов для всех пользователей (цвета, местоимения и т.д.). Достаточно 10 слов.

    ОФ.2. Спрашивать перевод слова, предлагая 4 варианта ответа на английском языке в виде кнопок.

    Оф.3. При правильном ответе подтверждать ответ, при неправильном - предлагать попробовать снова.

    Оф.4. У каждого слова должен быть пример использования. Пример использования можно получать из сервиса dictionaryapi.

    Оф.5. Должна быть реализована функция добавления нового слова.

    Оф.6. После добавления нового слова выводить сколько слов изучает пользователь.

    Оф.7. Новые слова не должны появляться у других пользователей.

    Оф.8. Должна быть реализована функция удаления слова.

    Оф.9. Удаление должно быть реальзовано персонально для пользователя.

    Оф.10. Работа с ботом после запуска должна начинаться с приветственного сообщения.

Дополнительные функциональные требования:

    Дф.1. Реализовать категории слов (страны, средства передвижения и т.д.).

    Дф.2. Не повторять изученные слова.

    Дф.3. Реализовать «изученность» слова. Слово считается изученным, если его угадали 5 раз без ошибок.

    Дф.4. Реализовать напоминания раз в день изучение английского языка.


Технические требования:

    Т.1. Отсутствуют ошибки (traceback) во время выполнения программы.
    
    Т.2. Результат программы записывается в БД. Количество таблиц должно быть не меньше трёх. Приложена схема БД.
    
    Т.3. Программа добавляет новые слова в БД для каждого пользователя.
    
    Т.4. Программа декомпозирована на функции/классы/модули/пакеты.
    
    Т.5. Написана документация по использованию программы.
    
    Т.6. Код программы удовлетворяет PEP8.

Подробное описание цели:
    
    https://github.com/netology-code/fshpd-diplom/blob/main/README.md#цель-проекта

Пример возможной реализации:
    
    https://github.com/netology-code/fshpd-diplom/blob/main/README.md#инструкция-к-работе-над-проектом
    
Предлагаемые инструменты для реализации:
    
    https://github.com/netology-code/fshpd-diplom/blob/main/README.md#инструменты-дополнительные-материалы-которые-пригодятся-для-выполнения-задания

Пример чек листа готовности окружения для реализации:
    
    https://github.com/netology-code/fshpd-diplom/blob/main/README.md#чеклист-готовности-к-работе-над-проектом

Правила сдачи:

    https://github.com/netology-code/fshpd-diplom/blob/main/README.md#правила-сдачи-работы

    ОФ требования выполнены
    Т требования выполнены
-------------------------------------------------------------------------------------------
Интерпретация требований для упрощения разработки:

    A. Бот работает с каждым пользователем персонально, запоминая всё о нём - его карточках
        Oф.10 Работа с ботом после запуска должна начинаться с приветственного сообщения.
    B. Бот при запуске приветствует пользователя и объясняет как с ним работать
        Оф.1 Заполнить базу данных общим набором слов для всех пользователей (цвета, местоимения и т.д.). Достаточно 10 слов.
    C. Бот позволяет пользователю создать набор карточек
        английский-русский
        Оф.5 Должна быть реализована функция добавления нового слова.
        Оф.6 После добавления нового слова выводить сколько слов изучает пользователь.
    D. Бот позволяет пользователю увидеть набор карточек и их число
        Оф.7 Новые слова не должны появляться у других пользователей.
    E. Бот позволяет пользователю удалить карточки
        Оф.8 Должна быть реализована функция удаления слова.
        Оф.9 Удаление должно быть реальзовано персонально для пользователя.
    F. Бот позволяет пользователю потренироваться в запоминании карточек
        Оф.2 Спрашивать перевод слова, предлагая 4 варианта ответа на английском языке в виде кнопок.
        Оф.3 При правильном ответе подтверждать ответ, при неправильном - предлагать попробовать снова.
        Оф.4 У каждого слова должен быть пример использования. Пример использования можно получать из сервиса dictionaryapi.

    На самом деле требования чуть попроще, так как задание нужно выполнить не из netology-code/fshpd-diplom, а из netology-code/sqlpy-diplom:
        Интеграцию с dictionaryapi можно не делать

Ход работы:

    - Описать алгоритм работы боты
        - Начинают пользователи чат - бот предлагает ввести хелп и объясняет для чего он нужен
          - Бот запоминает человнека - нужно будет познакомиться или вычленить id
            - База пользователей - id и инфо какое-то
            - База карточек пользователей - id пользователя, id слова из глобальной базы
            - База слов и их значений - рус-инг - id слова, слово, перевод
          - Для чего бот и что напишем в хелпе
            - Для изучения английский слов
            - Как изучаем
              - Пользователю предлагается создавать карточки: русское слово - английский перевод
              - Пользователь может вывести свои карточки с номерами
              - Пользователь может добавить карточку
                - После добавления показать число изучаемых слов
              - Пользователь может удалить карточки
              - Ограничений на корточки пока не вводим - ни на число, ни на проверяемые слова при задании и значения при задании
              - Карточки запоминаются для каждого пользователя
              - При начале диалога пользователю создаётся, например, базовый набор карточек - местоимения, существительные, цвета - достаточно 10 слов
              - Пользователю доступен режим тренировки
                - Берётся случайно слово из русского языка и для него предлагается выбрать верный перевод из 4 вариантов
                  - Если выбрали удачно - бот говорит отлично и предлагает другое слово
                  - Если выбрали неудачно - бот предлагает данное слово ещё раз
                  - Изученность и встречаемость можно не учитывать
                  - Выбор кнопками под вводом ссобщения
                  - Есть возможность остановить тренировку
                  - Кнопок хелп, вывод слов, добавить и удалить нет
        - Продолжают пользователи вести чат - принятие ботом только команд глобальных и команд контекста
          - Как человек узнает о глобальных командах и какие команды доступны
            - Как узнает
              - Команды всегда доступны в виде кнопок под строкой ввода текста
            - Какие доступны
              - Посмотреть список карточек
              - Добавить карточку в набор
              - Удалить карточку из набора
              - Вывести описание бота
            - Действия бота при переходах
          - Как человек узнает о командах контекста и какие контексты доступны
            - Как узнает
              - Команды всегда доступны в виде кнопок под строкой ввода текста
            - Контексты и их команды
              - Главное меню - описание выше
              - Тренировка - 4 варианта перевода и выход в главмное меню
              - Добавление слова - значение, перевод
              - Удаление слова - айди
            - Действия бота при переходах
              - Смена статусов и действия для сменяемого статуса и нового

На будущее

    - Создание или использование имеющейся БД https://github.com/Spardoks/python_sqlalchemy_test/blob/main/main.py
    - Добавить requirements.txt
    - Более тщательное отслеживание и обработка исключений
    - Логирование
    - Обновить документацияю
    - Код по pep8
    - Русский язык
    - Добавить тесты

Как запускать

    - pip install psycopg2-binary
    - pip install sqlalchemy
    - pip install pyTelegramBotAPI
    - pip install python-dotenv
    - createdb -U postgres teledb
    - create .env with telegram token, postgres user and password
    - python3 main.py