import logging
import os
from dotenv import load_dotenv
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, JobQueue
from telegram.constants import ParseMode # No need for others like ForceReply in this example
# ... your handler functions will be here (e.g., async def start(update: Update, context: CallbackContext): ...)
from trainData import datos_entrenamiento
from DataProcess import procesar_texto_desde_cero
from LazyBayes import NaiveBayesNativo

modelo = NaiveBayesNativo()
load_dotenv()

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the command /start is issued."""
    # update.effective_chat is a safe way to get the chat object
    # await is required for all Telegram API calls (like reply_text)
    await update.message.reply_text('Hola, Bienvenid@, yo soy BayesBot! Dame tu consulta y te asignaré al personal adecuado para que te ayude.')

# 
# Note: Renamed from 'help' to 'help_command' to avoid conflicts with built-in 'help()'
async def help_command(update: Update, context: CallbackContext) -> None:
    """Sends a help message with usage instructions."""
    help_text = (
        "🤖 **BayesBot Commands**\n\n"
        "/start - Start the bot and get a welcome message.\n"
        "/help - Show this help message.\n\n"
        "Just type a sentence, and I'll use a **Bayesian Classifier** "
        "to determine its category or intent."
    )
    
    # Use context.bot.send_message if reply_text isn't suitable, 
    # but reply_text is usually better for direct replies.
    # ParseMode.MARKDOWN_V2 is often used for rich text formatting.
    await update.message.reply_markdown_v2(
        help_text.replace('.', r'\.').replace('-', r'\-')
    )

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Classifies the incoming text message using your Bayesian model."""
    user_text = update.message.text

    prediccion, scores = modelo.predict(user_text)

    
    # --- ⚠️ Your Classification Logic Goes Here ⚠️ ---
    
    # Placeholder for your actual Bayes classification logic:
    # Example: predicted_class = model.predict(user_text) 
    # For now, we'll just echo and say we're processing.
    
    # You would typically call a function like this:
    # predicted_class = classify_text_with_bayes(user_text) 
    
    # For this example:
    predicted_class = prediccion.upper()

    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    detalles = f"Detalle de Puntuaciones:\n\n"
    for clase, score in sorted_scores:
        # Un score más cercano a 0 (menos negativo) es mejor
        # Ejemplo: -5.2 es mejor que -12.8
          # barra = "█" * int((score + 50) / 2) if score > -50 else "" # Visualización simple
        detalles += f"   {clase:10}: {score:.4f}\n"
    detalles += "\n"
    
    response_text = f"Tu mensaje ha sido clasificado como: *{predicted_class}*\n\n{detalles}"

    # Use reply_text and ParseMode if you need basic formatting
    await update.message.reply_text(
        response_text,
        parse_mode=ParseMode.MARKDOWN # Using basic Markdown here
    )

# --- End Handler Functions ---

def main() -> None:
    # Use a timezone provided by pytz (e.g., 'America/New_York')
    # Change 'America/New_York' to your desired timezone if needed.
    
    # Instanciamos la clase
    # Separamos X e y

    datos_entrenamiento_procesados = []

    for dato in datos_entrenamiento:
        datos_entrenamiento_procesados.append((procesar_texto_desde_cero(dato[0]),dato[1]))

    mensajes_train = [d[0] for d in datos_entrenamiento_procesados]
    categorias_train = [d[1] for d in datos_entrenamiento_procesados]

    # Entrenamos
    modelo.fit(mensajes_train, categorias_train)
    
    
    
    timezone = pytz.timezone('America/La_Paz')


    # 1. Initialize the Application with an explicit timezone setting
    application = (
        Application.builder()
        .token(os.environ.get("TOKEN")) # <-- Pass the configured job_queue instance here
        .build()
    )

    # ... The rest of your main function (add_handler, run_polling) remains the same ...
    
    # 2. Add Handlers to the Application (as before)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 3. Start the Bot (Polling)
    print("Bot is starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()