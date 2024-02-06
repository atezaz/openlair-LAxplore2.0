# For more information, please refer to https://aka.ms/vscode-docker-python
#FROM python:3.10-slim
FROM python:3.9
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
EXPOSE 8501
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
ENTRYPOINT [ "streamlit", "run", "main_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0" ]
#CMD ["python", "-m", "streamlit", "run", "main.py", "--server.port=8501"]