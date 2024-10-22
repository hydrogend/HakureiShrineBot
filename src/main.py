import discord
from discord.ext import tasks
from discord import app_commands
import time, os, random
from dotenv import load_dotenv

load_dotenv()

client = discord.Client(
  intents=discord.Intents.default(),
  activity=discord.Game("異変解決")
)
tree=app_commands.CommandTree(client)

TOKEN = os.getenv("TOKEN")

#omikuzi_list: list = ["大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶", "大福吉"]
omikuji_list: list = [
  {
    "name": "大吉",
    "description": [
      "やったわね！大吉よ！",
      "今日の異変解決はきっと大丈夫ね！",
    ],
    "color": 0x00ff00,
    "probability": 0.1
  },
  {
    "name": "中吉",
    "description": [
      "中吉ね！なんかいいことあるかもしれないわ！",
    ],
    "color": 0x00ff00,
    "probability": 0.15
  },
  {
    "name": "小吉",
    "description": [
      "小吉よ！まあまあいいことがあるかもね"
    ],
    "color": 0xffffff,
    "probability": 0.15
  },
  {
    "name": "吉",
    "description": [
      "吉ね！今日もいつも通りの一日になりそうね",
    ],
    "color": 0xffffff,
    "probability": 0.2
  },
  {
    "name": "末吉",
    "description": [
      "末吉よ。ちょっとだけいいことがあるかもね",
    ],
    "color": 0xffffff,
    "probability": 0.15
  },
  {
    "name": "凶",
    "description": [
      "凶ね...めげないでね...",
      "お祓いに行った方がいいかも..."
    ],
    "color": 0xff0000,
    "probability": 0.15
  },
  {
    "name": "大凶",
    "description": [
      "まずいわ...大凶よ...気をつけてね...",
      "今日は余計なことをしない方がいいかもしれない...",
      "もう残機ゼロよ..."
    ],
    "color": 0xff0000,
    "probability": 0.1
  },
  {
    "name": "大福吉",
    "description": [
      "「よくわかんないけどとりあえずよし！」",
      "「うーん、まあいいんじゃないかなぁ」"
    ],
    "color": 0xffd700,
    "probability": 0.01
  },
  {
    "name": "もちもち吉",
    "description": [
      "過労死には要注意",
      "タスクの掛け持ちはほどほどに",
    ],
    "color": 0xffd700,
    "probability": 0.01
  }
]

def get_omikuji() -> dict:
  omikuji: dict = {}
  time.sleep(0.001)
  random.seed(time.time() * 1000)
  total_probability = sum(item['probability'] for item in omikuji_list)
  pick = random.uniform(0, total_probability)
  current = 0
  for item in omikuji_list:
    current += item['probability']
    if current > pick:
      omikuji = item
      break
  return omikuji

@tree.command(name="omikuji", description="今日の運勢を占うわよ")
async def omikuji(interaction: discord.Interaction):
  omikuji: dict = {}
  omikuji = get_omikuji()

  omikuzi_embed = discord.Embed(
    title=omikuji['name'],
    description=random.choice(omikuji['description']),
    color=omikuji['color']
  )
  await interaction.response.send_message(embed=omikuzi_embed)

@tree.command(name="omikuji_x10", description="10回連続でおみくじを引くわよ")
async def omikuji_x10(interaction: discord.Interaction):
  omikuji_x10_results: list = []
  omikuji_x10_embed: list = []
  for i in range(10):
    omikuji: dict = get_omikuji()
    omikuji_x10_results.append(omikuji)
    omikuji_x10_embed.append(discord.Embed(
      title=omikuji['name'],
      description=random.choice(omikuji['description']),
      color=omikuji['color']
    ))
  
  await interaction.response.send_message(embeds=omikuji_x10_embed)

@client.event
async def on_ready():
  await tree.sync()
  print('Hakurei Shrine Bot is ready')

client.run(TOKEN)
