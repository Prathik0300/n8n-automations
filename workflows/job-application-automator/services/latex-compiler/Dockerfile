FROM texlive/texlive:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-flask \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY app.py .

EXPOSE 5001
CMD ["python3", "app.py"]