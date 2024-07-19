import discord
from discord.ext import commands
import google.generativeai as genai

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

genai.configure(api_key="GEMINI_API")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

message_history = {}#Da contexto para o bot através das mensagens antigas - Give context to the bot

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}!")

@bot.command(name = "moshi_moshi")
async def moshi_moshi(ctx: commands.Context, *, prompt: str):
    user_id = ctx.author.id

    if user_id not in message_history:
        message_history[user_id] = []

    message_history[user_id].append(prompt)#Adiciona o prompt para o contexto das mensagens

    context = "\n".join(message_history[user_id])#Faz o contexto em si, como se fosse uma grande mensagem

    #Fala para o Gemini não ultrapssar 2000 caracteres
    context += "\nPor favor, não passe de jeito nenhum de 2000 caracteres"

    response = model.generate_content(context)
    current_response = response.text
    # Ensure the response is within the character limit
    if len(current_response) > 2000:
        current_response = current_response[:2000]

    message_history[user_id].append(current_response)

    await ctx.reply(current_response)

    if len(message_history[user_id]) > 10:
        message_history[user_id] = message_history[user_id][-10:]

bot.run("DISCORD_API")