FROM python:3

WORKDIR /usr/src/app

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_DEVELOPMENT development
ENV FLASK_APP main.py

CMD ["flask", "run" , "-h" , "0.0.0.0" , "-p" , "8000"]
