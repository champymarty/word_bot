import traceback
import discord

from constant import TOKEN, WORD_FILE
from setup_logger import get_logger

from discord import ApplicationContext, option, Embed

from words import WordsRepo


LOGGER = get_logger()

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)
wordsRepo = WordsRepo()

@bot.event
async def on_ready():
    LOGGER.info(f"We have logged in as {bot.user}")

@bot.slash_command(
    description= "Show all your words"
)
@option(
    name="word",
    description="The word to add in the list",
    type=str,
    required=True
)
async def show(ctx: ApplicationContext):
    description = ""
    for word in wordsRepo.get_words():
        description += f"* {word}\n"
    embed = Embed(title="Here is all your words", description=description)
    await ctx.respond(embed=embed)

@bot.slash_command(
    description= "Get and consume daily words"
)
@option(
    name="word_count",
    description="The number of words for the day",
    type=int,
    required=True
)
async def get_daily(ctx: ApplicationContext, word_count: int):
    description = ""
    words = wordsRepo.consume_word(word_count)
    for word in words:
        description += f"* {word}\n"
    if len(words) == 0:
        description = "You have no more words :("
    embed = Embed(title="Here is all your words", description=description)
    await ctx.respond(embed=embed)

@bot.slash_command(
    description= "Command to add a word to the list"
)
@option(
    name="word",
    description="The word to add in the list",
    type=str,
    required=True
)
async def add(ctx: ApplicationContext, word: str):
    wordsRepo.add_word(word)
    embed = Embed(title="Word added success", description=f"The word `{word}` was added. You now have {wordsRepo.get_length()}")
    await ctx.respond(embed=embed)

@bot.slash_command(
    description= "Command to remove a word to the list"
)
@option(
    name="word",
    description="The word to remove in the list",
    type=str,
    required=True
)
async def remove(ctx: ApplicationContext, word: str):
    was_removed = wordsRepo.remove_word(word)

    embed = None
    if was_removed:
        embed = Embed(title="Word added success", description=f"The word `{word}` was removed. You now have {wordsRepo.get_length()}")
    else:
        embed = Embed(title="Word remove failure", description=f"The word `{word}` was not in the list.")

    await ctx.respond(embed=embed)

@bot.slash_command(
    description= "Download the list of words"
)
async def get_list(ctx: ApplicationContext):
    await ctx.respond("Here is the word list !",
                        file=discord.File(WORD_FILE))
    

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    description = f"""
    On guild `{ctx.guild}` by user {ctx.author.mention}
    On command `{ctx.command.name}` with values `{ctx.selected_options}`
    Error -> ```{error}```
    Original -> Error:`{error.original}` trace:```{"".join(traceback.format_tb(error.original.__traceback__))}```"""

    embed = Embed(title="Something went wrong", color=0xFF0000, description=description)
    LOGGER.exception(description)
    await ctx.respond(embed=embed)

bot.run(TOKEN)