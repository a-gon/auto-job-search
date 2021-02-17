FROM python:3.7
WORKDIR /app
# Install app dependencies
COPY src/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY src /app

CMD [ "python", "linkedinbot.py" ]