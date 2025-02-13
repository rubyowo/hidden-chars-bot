from os import getenv
from typing import Optional
import traceback

import discord
from discord import app_commands
from dotenv import load_dotenv

import lib

load_dotenv()

global_sync = False
GUILD = discord.Object(id=getenv("DISCORD_GUILD_ID"))


class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)
        if global_sync:
            await self.tree.sync()


client = Bot(intents=discord.Intents.none())


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")

@client.tree.context_menu(name="Encode this message")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def encode(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(lib.encode(message.content))


@client.tree.context_menu(name="Decode this message")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def decode(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(lib.decode(message.content))


class EncodeHidden(discord.ui.Modal, title="Hide text in another string"):
    def __init__(self, *, messageContent: Optional[str] = None):
        super().__init__(title=self.title)
        self.messageContent = messageContent

        if messageContent:
            super().remove_item(self.hidden)
        
    hidden = discord.ui.TextInput(
        label="The text you want to hide",
        style=discord.TextStyle.long,
        placeholder="Type your text here...",
    )

    text = discord.ui.TextInput(
        label="The text you want to hide it in",
        style=discord.TextStyle.long,
        placeholder="Type your text here...",
    )

    async def on_submit(self, interaction: discord.Interaction):
        hidden = self.hidden.value if not self.messageContent else self.messageContent
        await interaction.response.send_message(lib.encode_hidden(hidden, self.text.value))

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

@client.tree.command()
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def hide_text(interaction: discord.Interaction):
    await interaction.response.send_modal(EncodeHidden())
    
@client.tree.context_menu(name="Hide this message")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def hide_text_context(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_modal(EncodeHidden(messageContent=message.content))

client.run(getenv("TOKEN"))
