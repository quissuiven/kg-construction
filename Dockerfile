FROM python:3

WORKDIR /kg-construction

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en

COPY . .

CMD ["python3", "-m" , "flask", "--app", "app.py", "run", "--host=0.0.0.0"]
