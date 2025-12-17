from email.mime import application
import logging
import os
from dotenv import load_dotenv
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, JobQueue, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode 
from trainData import datos_entrenamiento
from DataProcess import procesar_texto_desde_cero
from LazyBayes import NaiveBayesNativo
import smtplib
from email.message import EmailMessage



mensaje_correo = ""



modelo = NaiveBayesNativo()
load_dotenv()


EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

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



    elif query.data.startswith('IPhone_'):

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


            modelo = f"{partes[1]} {partes[2]}"
            precio = f"{partes[3]}"
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
                    f"**Precio a pagar:** {precio}\n"
                    f"👇 **Selecciona tu método de pago:**",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                    )
            
    elif query.data.startswith('accesorios_'):

            partes = query.data.split('_') 


            modelo = f"{partes[1]} {partes[2]}"
            precio = f"{partes[3]}"

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
                    f"**Modelo:** {modelo}\n"
                    f"**Precio a pagar:** {precio}\n"
                    f"👇 **Selecciona tu método de pago:**",
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                    )
    
        





async def accion_saludo(update: Update, context: CallbackContext):
    mensaje = '🔰 iTech Store 🔰\n\n¡Hola!, Somos iTech Store, tu tienda de confianza para productos Apple.\n ¿Cómo podemos ayudarte?'
    await update.message.reply_text(mensaje)










async def accion_catalogo(update: Update, context: CallbackContext):
    await update.message.reply_text("Claro, estoy subiendo el catálogo para ti. Un momento por favor...")
    
    nombre_archivo = 'Catalogo_Productos.pdf'

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
        "🛠️ *Soporte Técnico*\n\n"
        "Para ayudarte, necesitamos que nos brindes tu número de teléfono porfavor.\n"
        "Presiona el botón para compartirlo y un personal de soporte se pondrá en contacto contigo."
    )

    keyboard = [
        [KeyboardButton("📱 Compartir mi número", request_contact=True)]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


    await update.message.reply_text(
        texto,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


    
async def recibir_contacto_soporte(update: Update, context: ContextTypes.DEFAULT_TYPE):

    contact = update.message.contact
    user = update.effective_user
    username = update.effective_user.username

    phone_number = contact.phone_number
    user_id = user.id
    nombre_usuario = " ".join(
        filter(None, [user.first_name, user.last_name])
    )

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = "kevinomega01@gmail.com"
    msg["Subject"] = "[Soporte Técnico]"

    
    msg.set_content(
        f"Usuario: {nombre_usuario}\n"
        f"ID: {user_id}\n"
        f"Username: @{username}\n"
        f"Teléfono: {phone_number}\n"
        f"Mensaje: {mensaje_correo}"
    )




    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)

    await update.message.reply_text(
        "✅ Gracias, por favor espera mientras un agente de soporte se pone en contacto contigo.",
        reply_markup=ReplyKeyboardRemove()
    )
    

    print("Correo enviado correctamente ✅")

async def accion_ubicacion(update: Update, context: CallbackContext):
    await update.message.reply_text("Nos encontramos aquí:")
    await update.message.reply_location(latitude=-17.3933818, longitude=-66.1460324)


async def accion_macanas(update: Update, context: CallbackContext, categoria=None):
    texto_guia = (
        "Disculpa, no entendí muy bien tu mensaje soy un modelo bayeciano(un bot).\n\n"
        "Intenta escribiendo alguna de estas opciones para que pueda ayudarte:\n\n"
        "📱 *'Quiero comprar un celular'* -> Para ver celulares.\n"
        "🎧 *'Busco accesorios'* -> Para cargadores o audífonos.\n"
        "📍 *'Dónde están ubicados'* -> Para ver nuestra tienda.\n"
        "📄 *'Ver catálogo'* -> Para descargar la lista de precios.\n"
        "🆘 *'Necesito ayuda'* -> Para contactar soporte técnico.\n"
        "*'Reclamos/quejas'* -> Si tienes un reclamo queremos saberlo.\n\n"

    )
    await update.message.reply_text(texto_guia, parse_mode=ParseMode.MARKDOWN)


async def accion_iphone(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("1 iPhone 12", callback_data='IPhone_12_500$'),
            InlineKeyboardButton("2 iPhone 13", callback_data='IPhone_13_650$'),
            InlineKeyboardButton("3 iPhone 14", callback_data='IPhone_14_750$'),
        ],
        [
            InlineKeyboardButton("4 iPhone 15", callback_data='IPhone_15_900$'),
            InlineKeyboardButton("5 iPhone 15 Pro", callback_data='IPhone_15Pro_1100$'),
        ],
        [
            InlineKeyboardButton("6 iPhone 16", callback_data='IPhone_16_1300$'),
        ],
        [
            InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)#interfaz
    
    await update.message.reply_text(
        "**Catálogo de celulares**\n\n"
        "Por favor, elige el modelo de celular que te interesa:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def accion_accesorios(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("1 Audífonos EarPods con cable ", callback_data='accesorios_EarPods_Cable_30$'),
            InlineKeyboardButton("2 AirPods (3da generación)", callback_data='accesorios_AirPods_3gen_200$'),
            InlineKeyboardButton("3 AirPods (2da generación)", callback_data='accesorios_AirPods_2gen_250$'),
        ],
        [
            InlineKeyboardButton("4 Cargador USB-C 20W", callback_data='accesorios_Cargador_USBC20W_40$'),
            InlineKeyboardButton("5 Cargador MagSafe ", callback_data='accesorios_Cargador_MagSafe_50$'),
        ],
        [
            InlineKeyboardButton("❌ Cancelar", callback_data='cancelar')
        ]
    ]
        
    reply_markup = InlineKeyboardMarkup(keyboard)#interfaz
    
    await update.message.reply_text(
        "**Catálogo de accesorios**\n\n"
        "Por favor, elige lo que te interesa:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )
        

async def accion_queja(update: Update, context: CallbackContext):
    await update.message.reply_text(f"😞 Lamentamos que hayas tenido una mala experiencia. Por favor llena el siguiente formulario para que nuestro personal pueda atenderte de la mejor manera posible.\n\n https://docs.google.com/forms/d/e/1FAIpQLScvL5lTjEjDwgUw-apwwd0ojjx4b1XqhWKbmpSly-dIsOUrwQ/viewform?usp=sharing&ouid=108485986762957973838")



ACCIONES = {
    "saludo": accion_saludo,
    # "compra": accion_compra,
    "catalogo": accion_catalogo,
    "soporte": accion_soporte,
    "ubicacion": accion_ubicacion,
    "macanas":accion_macanas,
    "iphone":accion_iphone,
    "accesorios":accion_accesorios,
    "queja":accion_queja,
}

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('🔰 iTech Store 🔰\n\n¡Hola!, Somos iTech Store, tu tienda de confianza para productos Apple.\n ¿Cómo podemos ayudarte?')


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

    global mensaje_correo 
    mensaje_correo = user_text

    user_text_processed = procesar_texto_desde_cero(user_text)



    # 1. Predecir
    prediccion, scores = modelo.predict(user_text_processed)
    categoria_detectada = prediccion.lower() # Aseguramos minúsculas para buscar en el diccionario



    print(f"Mensaje: {user_text} | Clasificado como: {categoria_detectada}")

    
    funcion_a_ejecutar = ACCIONES.get(categoria_detectada)

   
    if funcion_a_ejecutar:
        
        await funcion_a_ejecutar(update, context)
    else:
        # Si no hay función específica, usamos macanas
        await accion_macanas(update, context, categoria_detectada)

    



def main() -> None:
    # Use a timezone provided by pytz (e.g., 'America/New_York')
    # Change 'America/New_York' to your desired timezone if needed.
    


    datos_entrenamiento_procesados = []

    for dato in datos_entrenamiento:
        datos_entrenamiento_procesados.append((procesar_texto_desde_cero(dato[0]),dato[1]))

    mensajes_train = [d[0] for d in datos_entrenamiento_procesados]
    categorias_train = [d[1] for d in datos_entrenamiento_procesados]

    # Entrenamos
    modelo.fit(mensajes_train, categorias_train)
    
    
    
    timezone = pytz.timezone('America/La_Paz')


    
    application = (
        Application.builder()
        .token(os.environ.get("TOKEN")) 
        .build()
    )

   
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    

    application.add_handler(CallbackQueryHandler(button_handler))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_handler(CommandHandler("soporte", accion_soporte))
    application.add_handler(MessageHandler(filters.CONTACT, recibir_contacto_soporte))
    


 
    print("El bot esta listo....")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()