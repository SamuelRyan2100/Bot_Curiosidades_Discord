# Bot de curiosidades e utilidades para o discord
import json
import os
import random
from pathlib import Path

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents
intents = discord.Intents.default()
intents.message_content = True # ler o conteúdo da mensagem
intents.members = True         # detectar a entrada de membros

# Cria o Bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Executado quando o bot começa com sucesso
    print(f"Bot conectado como {bot.user}")


@bot.command(name="ola")
async def ola(ctx):
    # Cumprimenta o usuário pelo nome
    await ctx.send(f"Olá, {ctx.author.display_name}! 👋")


@bot.command(name="dado")
async def dado(ctx, lados: int = 6):
    # Rola um dado
    if lados < 2:
        await ctx.send("O dado precisa ter pelo menos 2 lados")
        return

    resultado = random.randint(1, lados)
    await ctx.send(f"🎲 Você rolou um d{lados} e tirou **{resultado}**!")


CURIOSIDADES = [
    "Polvos têm três corações e sangue azul.",
    "O mel nunca estraga: já acharam mel comestível em tumbas egípcias.",
    "Bananas são levemente radioativas por causa do potássio.",
    "O Python recebeu esse nome por causa do grupo de comédia Monty Python.",
    "Um dia em Vênus dura mais que um ano em Vênus.",
]

@bot.command(name="curiosidade")
async def curiosidade(ctx):
    # Envia uma curiosidade aleatória
    await ctx.send(f"💡 {random.choice(CURIOSIDADES)}")



# TRATAMENTO DE ERROS
@bot.event
async def on_command_error(ctx, error):
    """Trata erros de comandos de forma amigável."""
    if isinstance(error, commands.BadArgument):
        await ctx.send("❌ Argumento inválido. Confira como usar o comando.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Faltou informar algo no comando.")
    elif isinstance(error, commands.CommandNotFound):
        pass  # ignora comandos que não existem
    else:
        print(f"Erro inesperado: {error}")


# Comando usando APIs
@bot.command(name="clima")
async def clima(ctx, *, cidade: str):
    """Mostra o clima atual. Uso: !clima Fortaleza"""
    url = f"https://wttr.in/{cidade}"
    parametros = {"format": "j1", "lang": "pt"}

    try:
        resposta = requests.get(url, params=parametros, timeout=10)
        resposta.raise_for_status()  # gera erro se o status for ruim (404, 500...)
        dados = resposta.json()

        atual = dados["current_condition"][0]
        temperatura = atual["temp_C"]
        sensacao = atual["FeelsLikeC"]
        umidade = atual["humidity"]
        descricao = atual.get("lang_pt", atual["weatherDesc"])[0]["value"]
    except (requests.RequestException, KeyError, ValueError):
        await ctx.send("😕 Não consegui buscar o clima. Confira o nome da cidade.")
        return

    await ctx.send(
        f"🌤️ **Clima em {cidade.title()}**\n"
        f"Condição: {descricao}\n"
        f"Temperatura: {temperatura}°C (sensação de {sensacao}°C)\n"
        f"Umidade: {umidade}%"
    )


# Salvar notas em um arquivo
ARQUIVO_NOTAS = Path("notas.json")

def carregar_notas():
    # Lê as notas do arquivo
    if not ARQUIVO_NOTAS.exists():
        return {}
    
    with open(ARQUIVO_NOTAS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_notas(notas):
    # Grava o dicionário de notas no arquivo
    with open(ARQUIVO_NOTAS, "w", encoding="utf-8") as arquivo:
        json.dump(notas, arquivo, ensure_ascii=False, indent=2)

@bot.command(name="salvar")
async def salvar(ctx, *, texto: str):
    # Salva uma nota pessoal. Uso: !salvar comprar arroz
    notas = carregar_notas()
    usuario = str(ctx.author.id)
    notas.setdefault(usuario, []).append(texto)
    salvar_notas(notas)
    await ctx.send("📝 Nota salva!")

@bot.command(name="notas")
async def listar_notas(ctx):
    # Mostra as notas do usuário
    notas = carregar_notas()
    minhas = notas.get(str(ctx.author.id), [])

    if not minhas:
        await ctx.send("Você ainda não tem notas. Use `!salvar texto`")
        return

    lista = "\n".join(f"{i}. {nota}" for i, nota in enumerate(minhas, start=1))
    await ctx.send(f"📒 **Suas notas:**\n{lista}")

# Boas vindas automáticas
@bot.event
async def on_member_join(member):
    # Dá boas-vindas a quem entra no servidor
    canal = member.guild.system_channel
    if canal:
        await canal.send(f"Bem-vindo(a) ao servidor, {member.mention}! 🎉")



bot.run(TOKEN)