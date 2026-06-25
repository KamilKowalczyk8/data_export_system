#nasza lekka wersja pythona
FROM python:3.11-slim

# Ustawiamy katalog roboczy wewnątrz kontenera
WORKDIR /app

# Kopiujemy plik z wymaganiami, bibliotekami i instalujemy je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy całą resztę naszego kodu (folder app)
COPY . .

# Komenda startowa: uruchamiamy serwer Uvicorn, który będzie nasłuchiwał na porcie 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]