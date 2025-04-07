FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi[all] 

COPY . .

# Expose FastAPI and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# Run FastAPI + Streamlit
CMD ["bash", "-c", "fastapi dev app/main.py --host 0.0.0.0 --port 8000"]