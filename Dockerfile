FROM python:3

COPY src/mim /mim

COPY requirements.txt .

RUN pip install -r requirements.txt

#CMD [ "python", "/mim/main.py" ]
