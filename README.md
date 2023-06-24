# Weather_airflow
Решение несложной задачи по запросу данных с сайта, перегрузке их в БД, построением на основе данных БД витрины и графика, в планировщике AirFlow.

# Использованные технологии
* запросы к сайту по API
* парсинг ответа с помощью SQLAlchemy
* загрузка данных в стандартную PG БД Airflow (в ближайшее время постараюсь разобраться, как подключить свою БД, пока не очень понятно)
* запрос к БД для получения агрегирующих данных для построения витрины-датафрейма - делала через Pandas
* построение графика на основе датафрейма с помощью библиотеки MatplotLib с сохранением в файл (файл падает в папку logs докер-контейнера)
* постановка на выполнение по расписанию по принципу crontab

# Развертывание виртуальной машины с Linux
* установила под Windows OracleVM VirtualBox
* установила под Windows Vagrant
* скачала и развернула образ Linux Ubuntu Mantic под VM
* развернула docker с официального сайта
* поставила airflow по инструкции для установки в docker
* настроила через docker-compose.yaml порты для доступа к стандартной БД airflow и для выхода на веб-интерфейс airflow

# Описание проекта
* перенесла локальный проект в докер
* переделала файл main.py с учетом блока DAGs для Airflow
* поработала с распределением данных между выделенными тасками
* проследила через DBeaver за наполнением БД в контейнере PG Airflow
* протестировала с разными запросами
* проверила постановку на расписание и выполнение
* отчет в виде картинок помещаю сюда

# Иллюстрации по Airflow
![Календарь](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/calendar.png)
![Код](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/code.png)
![Даги](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/dags.png)
![Gant](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/gant.png)
![Граф](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/graph.png)
![Грид](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/grid.png)
![Логи](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/logs.png)
![БД_структура](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/db_weather_head_dbeaver.png)
![БД_содержание](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/db_weather_table_dbeaver.png)
![График](https://github.com/OlgaMurzina/Weather_airflow/blob/main/images/img_line.png)

