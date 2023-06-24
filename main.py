from airflow.models import Variable
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
import datetime as dt

args = {
    'owner': 'olga_murzina',
    'start_date': dt.datetime.now(),
    'provide_context': True
}

start_hour = 1
horizont_hours = 24


def extract_geo(**kwargs):
    import requests

    APPID = Variable.get("APPID")
    print(APPID)

    ti = kwargs['ti']
    # запрос локаций городов Московской области (города взяла просто из списка первых в МО)
    URL_GEO = "http://api.openweathermap.org/geo/1.0/direct?"
    CITYS = ['Москва', 'Абрамцево', 'Алабино', 'Апрелевка', 'Архангельское', 'Ашитково',
             'Бакшеево', 'Балашиха', 'Барыбино', 'Белозёрский', 'Белоомут', 'Белые Столбы',
             'Бородино', 'Бронницы']
    limit = 1
    # словарь город:локация
    geo = {}
    for q in CITYS:
        params = f'q={q}&limit={limit}&appid={APPID}'
        response = requests.get(f'{URL_GEO}{params}')
        if response.status_code == 200:
            response = response.json()
            lat = response[0]['lat']
            lon = response[0]['lon']
            geo[q] = (lat, lon)
    ti.xcom_push(key='geo', value=geo)


def extract_transform_weather(**kwargs):
    import datetime as dt
    from data.weather import Weather
    from data import db_session
    from sqlalchemy import create_engine
    import requests
    ti = kwargs['ti']
    geo = ti.xcom_pull(key='geo', task_ids=['extract_geo'])[0]
    # print(geo)
    # загрузка данных с сайта погоды
    APPID = Variable.get("APPID")
    print(APPID)
    URL_BASE = "https://api.openweathermap.org/data/2.5/forecast?"
    db_session.global_init("db/weather.db")
    # параметр - количество выгружаемых записей на один объект
    n = 24
    # формирование запроса по каждому объекту из модуля citys по геоданным
    for x in geo.keys():
        lat, lon = geo[x]
        params = f'lat={lat:.2f}&lon={lon:.2f}&cnt={n}&appid={APPID}&units=metric&lang=ru'
        # получение ответа и перевод его в .json
        response = requests.get(f'{URL_BASE}{params}')
        if response.status_code == 200:
            response = response.json()
            # print(response)
            # парсинг ответа с формированием записи для загрузки в БД
            for data in response['list']:
                report = Weather()
                report.date = dt.datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
                report.city = x
                report.humidity = int(data['main']['humidity'])
                report.pressure = int(data['main']['pressure'])
                report.temp_max = float(data['main']['temp_max'])
                report.temp_min = float(data['main']['temp_min'])
                report.clouds = int(data['clouds']['all'])
                report.wind_napr = int(data['wind']['deg'])
                report.wind_speed = float(data['wind']['speed'])
                report.description = data['weather'][0]['description']
                db_sess = db_session.create_session()
                # проверка дублей
                if db_sess.query(Weather).filter(
                        Weather.date == dt.datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S'),
                        Weather.city == x):
                    # существующую старую запись удаляем
                    db_sess.query(Weather).filter(
                        Weather.date == dt.datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S'),
                        Weather.city == x).delete()
                    db_sess.commit()
                # добавляем запись к БД
                db_sess.add(report)
                db_sess.commit()


def query(**kwargs):
    import datetime as dt
    from data.weather import Weather
    from data import db_session
    import matplotlib.pyplot as plt
    from sqlalchemy import create_engine
    import pandas as pd
    cols = f'city, avg(temp_min) as avg_temp_min, max(wind_speed) as max_wind_speed, min(wind_speed) as min_wind_speed'
    condition = "city like 'А%%' or city like '%%а'"
    group = 'city'
    type = 'line'
    # создание курсора
    engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres/airflow')
    # формирование витрины по запросам
    if cols and condition and group:
        qu = f'select {cols} from weather where {condition} group by {group}'
    elif cols and condition:
        qu = f'select {cols} from weather where {condition}'
    elif cols:
        qu = f'select {cols} from weather'
    print(qu)
    # получение датафрейма из ответа на запрос
    df = pd.read_sql_query(qu, engine)
    print(df)
    st = cols.split(', ')
    # функция построения графика для одной витрины под разные параметры
    plt.figure(figsize=(40, 24))
    x = st[0]
    y = ['avg_temp_min', 'max_wind_speed', 'min_wind_speed']
    if type == 'line':
        df.plot(title=f'{y}', x=x, y=y,
                grid=True, stacked=True)
    elif type == 'bar':
        df.plot(title=f'{y}', x=x, y=y,
                grid=True, kind='bar', stacked=True)
    elif type == 'hist':
        df.plot(title=f'{y}', x=x, y=y,
                grid=True, kind='hist', stacked=True)
    elif type == 'scatter':
        df.plot(title=f'{y}', x=x, y=y,
                grid=True, kind='scatter', stacked=True)
    elif type == 'pie':
        df.plot(title=f'{y}', y=x,
                grid=True, kind='pie')
    # cохраняем картинку
    plt.savefig(f'./logs/img_{type}.png', dpi=300)


with DAG('weather_base', description='weather_base', schedule_interval='5 * * * *', catchup=False,
         default_args=args) as dag:
    extract_geo = PythonOperator(task_id='extract_geo', python_callable=extract_geo)
    extract_transform_weather = PythonOperator(task_id='extract_transform_weather',
                                               python_callable=extract_transform_weather)
    query = PythonOperator(task_id='query', python_callable=query)

    extract_geo >> extract_transform_weather >> query
