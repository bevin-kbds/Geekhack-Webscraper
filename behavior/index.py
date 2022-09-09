import discord
from discord.ext import tasks
from discord.ext import commands
import os
import geekhack
import googlesheets

ic_bot = geekhack.MessageScraper('https://geekhack.org/index.php?board=132.0', 'most_recent_IC_ID.txt')
post_bot = geekhack.MessageScraper('Insert post to watch', 'most_recent_post_ID.txt')
sheet_bot = googlesheets.Sheets('1dD4QSbrBYBxJfmBSrPmv0h0tP35393vytqnkWBa45fE')
bot = commands.Bot(command_prefix="+")
print(type(post_bot))
qa_channel = Insert QA channel
@tasks.loop(minutes = 60)
async def MainLoop():
    channel = bot.get_channel(Insert IC channel ID)
    ic_bot.update_ic()
    message_list = ic_bot.repost_message()
    if message_list is None:
        return
    for message in message_list:
        if message[2] is not None:
            embed_message = discord.Embed(title = message[0], url = message[1], description=f"**Author**: {message[3]}", color = discord.Color.dark_grey()).set_thumbnail(url = message[2])
        else:
            embed_message = discord.Embed(title = message[0], url = message[1], description=f"**Author**: {message[3]}", color = discord.Color.dark_grey())
        await channel.send(embed=embed_message)
        
       
    post_channel = bot.get_channel(Insert Post channel ID)
    post_bot.update_post()
    message_list = post_bot.repost_message()
    
    if message_list is None:
        return
    for message in message_list:
        if message[3][0] is not None:
            formatted_quote = '\n'.join(message[3][0])
            embed_message = discord.Embed(title = message[0], url = message[1], description=f"**{message[2]}**\n{formatted_quote}\n{message[3][1]}" , color = discord.Color.light_gray())
        else:
            embed_message = discord.Embed(title = message[0], url = message[1], description=f"**{message[2]}**\n{message[3][1]}" , color = discord.Color.light_gray())
        try:
            #await post_channel.send(embed=embed_message)
            pass
        except:
            pass
    print('done...')

        
@bot.event
async def on_ready():
    print('starting...')
    MainLoop.start()
    
@bot.command()
async def qa(ctx, arg):
    await ctx.message.delete()
    arg = int(arg)
    if not isinstance(arg, int):
        return
    message = sheet_bot.get_row(0, arg)
    embed_message = discord.Embed(title = message[1], description=f"{message[3]}", color = sheet_bot.get_color(message[2]))
    await ctx.send(embed=embed_message)

    
@bot.event
async def on_message(message):
    print('message received...')
    if message.author == bot.user or message.author.id != 376396366018117633:
        print('invalid UID')
        return
    await bot.process_commands(message)

    
bot.run('Insert Bot ID')