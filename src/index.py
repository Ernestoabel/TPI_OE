import discord
import csv
import os

# 📁 Ruta al CSV (fuera de src)
RUTA_CSV = "data/datos.csv"

# 🔐 TOKEN desde variable de entorno (NO hardcodear)
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

usuarios = {}

# -------------------------------
# 📌 CREAR CSV SI NO EXISTE
# -------------------------------
def inicializar_csv():
    if not os.path.isfile(RUTA_CSV):
        with open(RUTA_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Usuario", "Destino", "Dias", "Monto"])


# -------------------------------
# 💾 GUARDAR DATOS
# -------------------------------
def guardar_solicitud(usuario, destino, dias, monto):
    with open(RUTA_CSV, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([usuario, destino, dias, monto])


# -------------------------------
# 📜 LEER HISTORIAL
# -------------------------------
def leer_historial():
    if not os.path.isfile(RUTA_CSV):
        return "📂 No hay solicitudes registradas."

    with open(RUTA_CSV, mode="r", encoding="utf-8") as file:
        reader = list(csv.reader(file))

        if len(reader) <= 1:
            return "📂 No hay datos cargados."

        texto = "📜 Historial de solicitudes:\n"

        for fila in reader[1:][-5:]:
            usuario, destino, dias, monto = fila
            texto += f"👤 {usuario} | 📍 {destino} | 📅 {dias} días | 💰 ${monto}\n"

        return texto


# -------------------------------
# 🤖 EVENTOS
# -------------------------------
@client.event
async def on_ready():
    print(f"🤖 Bot conectado como {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id
    texto = message.content.lower()

    # -------------------------------
    # HISTORIAL
    # -------------------------------
    if texto == "!historial":
        await message.channel.send(leer_historial())
        return

    if user_id not in usuarios:
        usuarios[user_id] = {"estado": "inicio"}

    estado = usuarios[user_id]["estado"]

    # -------------------------------
    # INICIO
    # -------------------------------
    if texto == "!start":
        usuarios[user_id] = {"estado": "confirmacion"}
        await message.channel.send("👋 ¿Desea solicitar viáticos? (si/no)")
        return

    # -------------------------------
    # CONFIRMACION
    # -------------------------------
    if estado == "confirmacion":
        if texto == "si":
            usuarios[user_id]["estado"] = "destino"
            await message.channel.send("📍 Ingrese destino:")
        else:
            await message.channel.send("❌ Proceso cancelado")
            usuarios[user_id]["estado"] = "fin"

    # -------------------------------
    # DESTINO
    # -------------------------------
    elif estado == "destino":
        usuarios[user_id]["destino"] = texto
        usuarios[user_id]["estado"] = "dias"
        await message.channel.send("📅 Ingrese cantidad de días:")

    # -------------------------------
    # DIAS
    # -------------------------------
    elif estado == "dias":
        if not texto.isdigit() or int(texto) <= 0:
            await message.channel.send("⚠️ Ingrese un número válido de días")
            return

        usuarios[user_id]["dias"] = int(texto)
        usuarios[user_id]["estado"] = "monto"
        await message.channel.send("💰 Ingrese monto solicitado:")

    # -------------------------------
    # MONTO
    # -------------------------------
    elif estado == "monto":
        if not texto.isdigit():
            await message.channel.send("⚠️ Ingrese un monto válido")
            return

        monto = int(texto)
        usuarios[user_id]["monto"] = monto

        destino = usuarios[user_id]["destino"]
        dias = usuarios[user_id]["dias"]

        # 💾 Guardar en CSV
        guardar_solicitud(message.author.name, destino, dias, monto)

        await message.channel.send(
            f"📄 Solicitud registrada:\n"
            f"📍 Destino: {destino}\n"
            f"📅 Días: {dias}\n"
            f"💰 Monto: ${monto}"
        )

        # ✅ DECISIÓN 1
        if monto < 100000:
            await message.channel.send("✅ Solicitud aprobada")
        else:
            await message.channel.send("❌ Solicitud rechazada por monto elevado")
            usuarios[user_id]["estado"] = "fin"
            return

        # 💰 DECISIÓN 2
        fondos = 200000

        if fondos >= monto:
            await message.channel.send("💵 Viáticos entregados correctamente")
        else:
            await message.channel.send("❌ No hay fondos disponibles")

        usuarios[user_id]["estado"] = "fin"


# -------------------------------
# 🚀 EJECUCIÓN
# -------------------------------
if __name__ == "__main__":
    inicializar_csv()

    if not TOKEN:
        print("⚠️ ERROR: No definiste el DISCORD_TOKEN")
    else:
        client.run(TOKEN)