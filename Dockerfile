
FROM python:3.12.9-slim 

#Prevent from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1   
#Makes print() logs show up right away in terminal/log files  (useful for debugging in Docker) 
ENV PYTHONUNBUFFERED=1

#Set working directory
WORKDIR /app

#Install system dependencies, for spaCy, numpy & Pandas, vadersentiment
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install spaCy English model
RUN pip install --upgrade pip && \
    pip install -r requirements.txt &&\
    python -m spacy download en_core_web_lg

# Copy project files
COPY . .

#Default command to run your main pipeline
CMD ["python", "main.py"]


