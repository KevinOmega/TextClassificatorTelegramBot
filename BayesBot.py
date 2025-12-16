import logging
import os
from dotenv import load_dotenv
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, JobQueue, CallbackQueryHandler
from telegram.constants import ParseMode 
from trainData import datos_entrenamiento
from DataProcess import procesar_texto_desde_cero
from LazyBayes import NaiveBayesNativo

modelo = NaiveBayesNativo()
load_dotenv()

async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    

    await query.answer()
    
    if query.data == 'pago_qr':

        await query.message.delete()


        qr_imagen = 'qr.png' 

        
        with open(qr_imagen, 'rb') as qr_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_file,
                caption="**Opción: Pago por QR**\n\n"
                        "*Importante:* Envía una captura del comprobante aquí cuando termines.",
                parse_mode=ParseMode.MARKDOWN
            )

        
    elif query.data == 'pago_banco':
        await query.edit_message_text(
            text="**Opción: Transferencia Bancaria**\n\n"
                 "🏦 **Banco:** Banco Nacional\n"
                 "👤 **Titular:** Simon.\n"
                 "🔢 **Cuenta:** 123412312\n"
                 "🆔 **NIT/CI:** 555666777\n\n"
                 "*Importante:* Envía una captura del comprobante aquí cuando termines.",
            parse_mode=ParseMode.MARKDOWN
        )
        
    elif query.data == 'cancelar':
        await query.edit_message_text(text="Entendido, hemos cancelado el proceso de compra. Avísanos si necesitas algo más.")



async def accion_saludo(update: Update, context: CallbackContext):
    mensaje = 'Hola, Bienvenid@, yo soy BayesBot! Dame tu consulta y te asignaré al personal adecuado para que te ayude.'
    await update.message.reply_text(mensaje)


# async def accion_compra(update: Update, context: CallbackContext):
#     keyboard = [
#         [
#             InlineKeyboardButton("📲 Pagar por QR", callback_data='pago_qr'),
#             InlineKeyboardButton("🏦 Transferencia", callback_data='pago_banco'),

#         ],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')],
#         [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')]
#     ]
    
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     texto = (
#         "**¡Excelente decisión!**\n\n"
#         "Para finalizar tu pedido, por favor selecciona tu método de pago preferido:"
#     )
    
#     await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    # --- Lógica existente de Pagos ---
    if query.data == 'pago_qr':
        await query.message.delete()
        qr_imagen = 'qr.png' 
        try:
            with open(qr_imagen, 'rb') as qr_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=qr_file,
                    caption="**Opción: Pago por QR**\n\n*Importante:* Envía una captura del comprobante.",
                    parse_mode=ParseMode.MARKDOWN
                )
        except FileNotFoundError:
            await query.message.reply_text("Error: No se encontró la imagen QR.")

    elif query.data == 'pago_banco':
        await query.edit_message_text(
            text="**Opción: Transferencia Bancaria**\n\n🏦 **Banco:** Nacional\n🔢 **Cuenta:** 123456\n\nEnvía comprobante.",
            parse_mode=ParseMode.MARKDOWN
        )
        
    elif query.data == 'cancelar':
        await query.edit_message_text(text="Operación cancelada.")



    elif query.data.startswith('iphone_'):

        modelo_seleccionado = query.data
        

        keyboard = [
            [
                InlineKeyboardButton("⚫ Negro", callback_data=f'color_{modelo_seleccionado}_negro'),
                InlineKeyboardButton("⚪ Blanco", callback_data=f'color_{modelo_seleccionado}_blanco'),
            ],
            [
                InlineKeyboardButton("🔵 Azul", callback_data=f'color_{modelo_seleccionado}_azul'),
                InlineKeyboardButton("🟣 Morado", callback_data=f'color_{modelo_seleccionado}_morado'),
            ],
            [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        

        nombre_modelo = modelo_seleccionado.replace('_', ' ').title().replace('Iphone', 'iPhone')
        
        await query.edit_message_text(
            text=f"Has elegido: **{nombre_modelo}**\n\n🎨 Por favor, selecciona un color:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )


    elif query.data.startswith('color_'):

        partes = query.data.split('_') 

        
        modelo = f"{partes[1]} {partes[2]}".title().replace('Iphone', 'iPhone')
        color = partes[3].capitalize()
        
        keyboard = [
            [
                InlineKeyboardButton("📲 Pagar por QR", callback_data='pago_qr'),
                InlineKeyboardButton("🏦 Transferencia", callback_data='pago_banco'),
            ],
            [InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=f"✅ **Resumen del Pedido**\n\n"
                 f"📱 **Modelo:** {modelo}\n"
                 f"🎨 **Color:** {color}\n\n"
                 f"👇 **Selecciona tu método de pago:**",
                 reply_markup=reply_markup,
                 parse_mode=ParseMode.MARKDOWN
                 )
        





async def accion_catalogo(update: Update, context: CallbackContext):
    await update.message.reply_text("Claro, estoy subiendo el catálogo para ti. Un momento por favor...")
    
    nombre_archivo = 'herramientas_proyecto_IA2.pdf'

    try:
        with open(nombre_archivo, 'rb') as documento:
            
            await update.message.reply_document(
                document=documento,
                caption="Aquí tienes nuestra lista de precios y productos actualizada",
                filename="Catalogo.pdf" 
            )
            
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {nombre_archivo}")
        await update.message.reply_text("Lo siento, no encuentro el archivo del catálogo en el sistema. Contacta a un humano.")
    except Exception as e:
        print(f"ERROR AL ENVIAR: {e}")
        await update.message.reply_text("Ocurrió un error al intentar enviarte el archivo.")

async def accion_soporte(update: Update, context: CallbackContext):
    texto = (
        "**Soporte Técnico**\n"
        "Lamento que tengas problemas. Un técnico revisará tu caso.\n"
        "Por favor, envíame una foto del error si es posible."
    )
    await update.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN)


async def accion_ubicacion(update: Update, context: CallbackContext):
    await update.message.reply_text("Nos encontramos aquí:")
    await update.message.reply_location(latitude=-17.3933818, longitude=-66.1460324)


async def accion_macanas(update: Update, context: CallbackContext):
    await update.message.reply_text(f"No entiendo lo que tratas de decirme puedes ser mas espesifico :D")


async def accion_iphone(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("1 iPhone 12", callback_data='iphone_12'),
            InlineKeyboardButton("2 iPhone 13", callback_data='iphone_13'),
            InlineKeyboardButton("3 iPhone 14", callback_data='iphone_14'),
        ],
        [
            InlineKeyboardButton("4 iPhone 15", callback_data='iphone_15'),
            InlineKeyboardButton("5 iPhone 15 Pro", callback_data='iphone_15Pro'),
        ],
        [
            InlineKeyboardButton("6 iPhone 16", callback_data='iphone_16'),
        ],
        [
            InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "**Catálogo de Apple** 🍎\n\n"
        "Por favor, elige el modelo de celular que te interesa:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def accion_accesorios(update: Update, context: CallbackContext):
    await update.message.reply_text(f"accesorios")


ACCIONES = {
    "saludo": accion_saludo,
    # "compra": accion_compra,
    "catalogo": accion_catalogo,
    "soporte": accion_soporte,
    "ubicacion": accion_ubicacion,
    "macanas":accion_macanas,
    "iphone":accion_iphone,
    "accesorios":accion_accesorios
}

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hola, Bienvenid@, yo soy BayesBot! Dame tu consulta y te asignaré al personal adecuado para que te ayude.')


async def help_command(update: Update, context: CallbackContext) -> None:
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

    texto_procesado = procesar_texto_desde_cero(user_text)

    # 1. Predecir
    prediccion, scores = modelo.predict(texto_procesado)
    categoria_detectada = prediccion.lower() # Aseguramos minúsculas para buscar en el diccionario

    print(f"Mensaje: {user_text} | Clasificado como: {categoria_detectada}")

    # 2. Buscar la función correspondiente en el diccionario
    funcion_a_ejecutar = ACCIONES.get(categoria_detectada)

    # 3. Ejecutar la acción
    if funcion_a_ejecutar:
        # Si existe una función específica, la ejecutamos
        await funcion_a_ejecutar(update, context)
    else:
        # Si no hay función específica (ej. 'saludo' o 'queja'), usamos la genérica
        await accion_macanas(update, context, categoria_detectada)

    

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
    
# 2. Add Handlers to the Application (as before)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # AGREGAR ESTA LÍNEA: Manejador para los botones
    application.add_handler(CallbackQueryHandler(button_handler))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    


    # 3. Start the Bot (Polling)
    print("El bot esta listo....")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()