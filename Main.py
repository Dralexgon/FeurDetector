#This is a discord bot made by Dralexgon. 
#It's a bot that counts the number of time each person said "feur" in the server.

import discord
from discord.ext import commands
from discord.ext.commands import Bot


from Log import Log

client = commands.Bot(command_prefix = "!", help_command=None, intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    Log.print("Bot is ready!")

@client.command(name="help", help="Shows this message.")
async def help(ctx):
    embed = discord.Embed(
        title = "Help",
        colour = discord.Colour.blue()
    )
    commandListinversed = []
    for command in client.commands:
        commandListinversed.append(command)
    for command in commandListinversed:
        embed.add_field(name=command.name, value=command.help, inline=False)
    await ctx.send(ctx.author.mention, embed=embed)

@client.command(pass_context = True, name="ping", help="Answers with pong, to check if the bot is online.")
async def ping(ctx: commands.Context):
    await ctx.send("Pong!")

@client.command(pass_context = True, name="test", help="To test stuff. (Only for Dralexgon)")
async def test(ctx: commands.Context):
    if ctx.author.id != 645005137714348041:
        await ctx.send("Only for dev ! Only for Dralexgon.")
        return
    await ctx.send("Test".__contains__("feur"))
    await ctx.send("Testfeurtruc".__contains__("feur"))

@client.command(pass_context = True, name="count_feur", aliases=["cf"], help="This command will count the number of time each person said 'feur' in the server.")
async def count_feur(ctx: commands.Context):
    result = {}
    for channel in ctx.guild.channels:
        if channel.type == discord.ChannelType.text:
            await ctx.send(f"Analyzing channel {channel.name}...")
            messages = await channel.history(limit=None).flatten()
            for message in messages:
                if message.content.lower().__contains__("feur"):
                    Log.print(f"Found feur in {channel.name} from {message.author.name}")
                    if message.author.name in result:
                        result[message.author.name] += 1
                    else:
                        result[message.author.name] = 1
            await ctx.send(f"Done analyzing channel {channel.name}")        
    embed = discord.Embed(
        title = "Number of feur",
        colour = discord.Colour.blue()
    )
    #sort the result
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    for user in result:
        embed.add_field(name=user, value=result[user], inline=False)
    await ctx.send(ctx.author.mention, embed=embed)
    

    
#note, if you want to run this code, you need to create a file called token.txt one directory above the code and put your token in it.
token = open('../token.txt', 'r').readlines()[0]
client.run(token)




#note for me,
#if I want to use slash commands,
#search on this link : https://discord-interactions.readthedocs.io/en/latest/quickstart.html