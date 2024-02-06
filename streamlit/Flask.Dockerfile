# For more information, please refer to https://aka.ms/vscode-docker-python
#FROM python:3.10-slim
FROM python:3.11
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
EXPOSE 8502
# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN [ "python", "-c", "import nltk; nltk.download('stopwords', download_dir='usr/local/nltk_data')" ]
RUN [ "python", "-c", "import nltk; nltk.download('punkt', download_dir='usr/local/nltk_data')" ]


WORKDIR /app

#EXPOSE 8501
#HEALTHCHECK CMD curl --fail http://localhost:8051/_stcore_health

COPY . /app


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#ENTRYPOINT [ "streamlit", "run" ]
#CMD [ "main.py" ]
ENTRYPOINT [ "flask", "--app", "main_flask.py", "run", "-h", "0.0.0.0", "-p", "8502" ]
#CMD ["python", "-m", "streamlit", "run", "main.py", "--server.port=8501"]