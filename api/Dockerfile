# Usa una imagen base de Python 3.12.4
FROM python:3.12.4-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos
COPY requirements.txt .

# Actualiza setuptools e instala las dependencias
RUN pip install --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto 8080
EXPOSE 8080

# Define el punto de entrada para la aplicación Flask
ENTRYPOINT ["python", "wsgi.py"]

# Comando para ejecutar Gunicorn
CMD gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 wsgi:app