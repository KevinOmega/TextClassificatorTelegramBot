# 🤖 BayesBot - Clasificador Bayesiano de Telegram

Este proyecto implementa un bot de Telegram utilizando la librería `python-telegram-bot` para clasificar mensajes de texto entrantes. Utiliza una arquitectura asíncrona y es ideal para integrar un modelo de **Clasificador Bayesiano** (o cualquier modelo de Machine Learning) para la toma de decisiones basada en el texto del usuario.

## 🚀 Puesta en Marcha

Sigue estos pasos para descargar, configurar y ejecutar el bot en tu máquina local.

### Requisitos

* **Python 3.10** o superior.
* Una cuenta de Telegram y un **Token de Bot** obtenido a través de [BotFather](https://t.me/BotFather).

### 1. Clonar el Repositorio

Abre tu terminal y clona el proyecto:

```bash
git clone https://github.com/KevinOmega/TextClassificatorTelegramBot.git

cd BayesBot
```

### Configurar el Entorno Virtual y Dependencias
Se recomienda usar un entorno virtual y luego instalar todas las dependencias listadas en requirements.txt.

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno (Linux/macOS)
source venv/bin/activate 

# Activar el entorno (Windows)
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```
### Configurar el Token de Telegram (Secreto)
Para que el bot se conecte, necesita tu token. El archivo .gitignore impide que el archivo .env se suba al repositorio.

Crea un archivo llamado .env en la raíz del proyecto.
```bash
#Arvhivo .env
TOKEN="<Remplaza el token aqui>"
```

### Ejecutar el Bot
Asegúrate de que tu entorno virtual esté activado y luego ejecuta:

```bash
python BayesBot.py
```
