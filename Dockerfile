FROM python:3.11-slim
COPY requirements.txt /requirements.txt
COPY main.py /main.py
RUN pip install -r /requirements.txt
EXPOSE 5555
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5555"]