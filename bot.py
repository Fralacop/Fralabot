#Fralabot by Fralacop

#List of Commands (for Frankie's use only):

#Moderator commands:
#!ping - pong
#!clear (amount)
#!info - help (soon)
#!mute (user) - mutes a user
#!kick (user) - kicks a user
#!ban (user) - bans a user
#!userinfo (user) - reads information about a user e.g. when they joined
#!serverinfo - read information about the server you are in
#!unban - command not in use
#!unmute - command not in use


#Music commands
#!play (song) - command not in use
#!skip - command not in use

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from itertools import cycle
import youtube_dl

#IMPORTANT VARIABLES -------------------------------------------------------------
players = {}
#---------------------------------------------------------------------------------

bot = commands.Bot(command_prefix="!")
bot.remove_command("help")
status = ["!info", "!help"]

async def change_status():
    await bot.wait_until_ready()
    msgs = cycle(status)

    while not bot.is_closed:
        current_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(150)


@bot.event
async def on_ready():
    print ("Ready when you are...")
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)
    print (bot.user.name + " is Up and Running :)")

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say(":ping_pong: pong!")

@bot.command(pass_context=True)
async def info(ctx):
    await bot.say("To see a set of Rules visit the #rules channel. This command is in **BETA**. As of now it cannot do much (Frankie is open to suggestions).")

@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    await bot.kick(user)
    await bot.say("{} has been kicked!".format(user.name))


@bot.command(pass_context=True)
async def cmds(ctx):
    embed = discord.Embed(title="!user (user) - to see user info.", description="oof oof oof", color=0x339966)
    embed.set_footer(text="This is a footer (Frankie change later plz)")
    embed.set_author(name="Info:")
    embed.add_field(name="frankie change the field :p", value="value needs changing as well", inline=True)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def userinfo(ctx, user: discord.Member):
    embed = discord.Embed(title="**__{}'s Info__**".format(user.name), description="Here's what I Found:", color=0x66cc99)
    embed.add_field(name="Name: ", value=user.name, inline=True)
    embed.add_field(name="ID: ", value=user.id, inline=True)
    embed.add_field(name="Status: ", value=user.status, inline=True)
    embed.add_field(name="Top Role: ", value=user.top_role, inline=True)
    embed.add_field(name="Joined: ", value=user.joined_at, inline=True)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(title="**__{} Info__**".format(ctx.message.server.name), description="Here's what I Found:", color=0x339966)
    embed.add_field(name="Server Name: ", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID: ", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles: ", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members: ", value=len(ctx.message.server.members), inline=True)
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def ban(ctx, user: discord.Member):
    await bot.ban(user)
    await bot.say("{} has been banned!".format(user.name))

@bot.command(pass_context = True)
async def mute(ctx, member: discord.Member):
     if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '194151340090327041':
        role = discord.utils.get(member.server.roles, name='Muted')
        await bot.add_roles(member, role)
        embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await bot.say(embed=embed)
     else:
        embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
        await bot.say(embed=embed)

@bot.event
async def on_message(message):
    sender = message.author
    msg = message.content
    print("{}:{}".format(sender, msg))
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def clear(ctx, amount=5):
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount) + 1):
        messages.append(message)
    await bot.delete_messages(messages)
    msg = await bot.say("**{}** has deleted {} messages!".format(ctx.message.author.name, int(amount)))
    await asyncio.sleep(3)
    await bot.delete_message(msg)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="Member")
    await bot.add_roles(member, role)

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(title="**__{} Info__**".format(bot.user.name), description="Commands:", color=0x339966)
    embed.add_field(name="!help", value="Shows this List", inline=False)
    embed.add_field(name="!ping", value="Returns Pong", inline=False)
    embed.add_field(name="!userinfo (user)", value="Displays Information about a User", inline=False)
    embed.add_field(name="!serverinfo", value="Displays Information about the Server you are in", inline=False)
    embed.add_field(name="!add (number) (number)", value="For adding numbers.", inline=False)
    embed.add_field(name="!minus (number) (number)", value="For minusing numbers.", inline=False)
    embed.add_field(name="!multiply (number) (number)", value="For multiplying numbers.", inline=False)
    embed.add_field(name="!divide (number) (number)", value="For dividing numbers.", inline=False)
    await bot.send_message(author, embed=embed)

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)

@bot.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

@bot.command(pass_context=True)
async def tempban(ctx, user: discord.Member, amount=3600):
    await bot.ban(user)
    embed=discord.Embed(title="User Temp Banned!", description="User has been Temp Banned!", color=0xff00f6)
    await bot.say(embed=embed)
    await asyncio.sleep(int(amount))
    await bot.unban(user)

@bot.command(pass_context=True)
async def unban(ctx, userID = None):
    banned_users = await bot.get_bans(ctx.message.server)
    user = discord.utils.get(banned_users,id=userID)
    await bot.unban(ctx.message.server, user)

@bot.command(pass_context=True)
async def add(ctx, args1, args2):
    ans = (int(args1)+int(args2))
    await bot.say(f'{args1} + {args2} = {ans}')

@bot.command(pass_context=True)
async def minus(ctx, args1, args2):
    ans = (int(args1)-int(args2))
    await bot.say(f'{args1} - {args2} = {ans}')

@bot.command(pass_context=True)
async def divide(ctx, args1, args2):
    ans = (int(args1)/int(args2))
    await bot.say(f'{args1} ÷ {args2} = {ans}')

@bot.command(pass_context=True)
async def multiply(ctx, args1, args2):
    ans = (int(args1)*int(args2))
    await bot.say(f'{args1} x {args2} = {ans}')


bot.loop.create_task(change_status())
bot.run("BOT_TOKEN")
