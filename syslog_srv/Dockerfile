FROM python:3.11-slim
WORKDIR /app
COPY syslog.py .
RUN chmod 777 /app
EXPOSE 514
CMD ["python", "./syslog.py"]