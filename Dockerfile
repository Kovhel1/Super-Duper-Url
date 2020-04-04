#иногда пишут версию ubuntu
FROM python:3.6.9-alpine

#новый пользователь
RUN adduser -D main

#куда будет установлено изображение
WORKDIR /Домашняя папка/Рабочий стол/Super Duper Url

#передает файлы с компьютера в файловую систему контейнера
COPY requirements.txt requirements.txt

#RUN эквиволентна командной строке
RUN python3 -m venv venv
RUN pip install -r requirements.txt
#gunicorn будет испольоваться как веб-сервер
RUN venv/bin/pip install gunicorn pymysql

#устанавливают приложение в контейнер путем копирования пакета приложения
COPY migrations migrations
COPY static static
COPY templates templates
COPY db.sqlite3 db.sqlite3
#COPY config.py config.py
# boot.sh - обязательный файл для windows, не для ubuntu
#COPY main.py config.py boot.sh ./
COPY main.py config.py 
#RUN chmod +x - так не работает
#RUN chmod +x boot.sh

#переменная среды контейнера
ENV FLASK_APP main.py

RUN chown -R main:main ./
USER main

EXPOSE 500

#ENTRYPOINT ["./boot.sh"]