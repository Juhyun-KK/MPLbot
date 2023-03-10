import discord #pycord
import os
from dotenv import load_dotenv

TOKEN = os.environ['TOKEN']
load_dotenv()
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

stack = dict()


@bot.event
async def on_ready():
	print(f"{bot.user} is ready and online!")


@bot.event
async def on_message(message):
	if not message.channel.id in stack:
		stack.setdefault(message.channel.id, message)
	else:
		stack.update({message.channel.id: message})


class Button(discord.ui.View):
	def __init__(self, thread):
		super().__init__()
		self.thread = thread

	@discord.ui.button(label="λ³΄κ΄", style=discord.ButtonStyle.success, emoji="π")
	async def archive(self, button, interaction):
		await interaction.response.send_message("μ΄ μ€λ λλ λ³΄κ΄λμμ΅λλ€. μλ¬΄λ λ©μμ§λ₯Ό λ³΄λ΄ λ³΄κ΄ν΄μ ν  μ μμ΅λλ€.")
		await self.thread.edit(archived=True)

	@discord.ui.button(label="μ κΈ", style=discord.ButtonStyle.danger, emoji="π")
	async def lock(self, button, interaction):
		await interaction.response.send_message("μ΄ μ€λ λλ μ κ²Όμ΅λλ€. μ€μ§ κ΄λ¦¬μλ§μ΄ μ κΈν΄μ ν  μ μμ΅λλ€.")
		await self.thread.edit(locked=True)


@bot.slash_command(name="thread", description="μ΄μ μ λ©μμ§μ μ€λ λλ₯Ό μμ±ν©λλ€.")
async def thread(ctx, auto_archive_duration=10080):
	message = stack[ctx.channel.id]
	thread = await message.create_thread(name=message.content[:50], auto_archive_duration=int(auto_archive_duration))
	await ctx.respond("μ±κ³΅!", ephemeral=True)
	await thread.send("<@&1077985851562278922>", view=Button(thread))


bot.run(TOKEN)
