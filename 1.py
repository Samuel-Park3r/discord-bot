import discord
from discord.ext import commands
import sqlite3
import random

DB = sqlite3.connect('main_DB.db')
EXP = DB.cursor().execute('''SELECT xp FROM users''').fetchall()
IDs = DB.cursor().execute('''SELECT id FROM users''').fetchall()
bwords = DB.cursor().execute('''SELECT words FROM bad_words''').fetchall()
bword_list = []
EXP_list = []
ID_list = []
print(IDs, EXP, bwords, sep='\n')


def unpacker(package, listt):
    for a in package:
        for e in a:
            listt.append(e)


unpacker(EXP, EXP_list)
unpacker(IDs, ID_list)
unpacker(bwords, bword_list)
print(bword_list)
TOKEN = "NzAzNTM4MzQ1OTA4NjMzNjAw.XqQDkw.Rc6DlAEfOFMk_vy8BGxZueQaoU4"
emojis = ['<:harold:707287826085183588>', '<:kermit:707287825749377165> ', '<:who_r_u:707287825741250560> ',
          '<:classic:707287825674141746> ', '<:feelsbadman:707296702033559605> ', '<:pepega:707287825623547955> ',
          '<:itsfine:707295832499552368>', '<:think_about:707287825405575208> ', '<:yes:707287824436560012>',
          ':eggplant:', ':new_moon_with_face:']
bot = commands.Bot(command_prefix='./')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    msg = message.content.lower().replace(',', '').replace('.', '').replace('!', '').replace('/', '').replace('?', '') \
        .replace('|', '').replace('<', '').replace('>', '').replace('@', 'а').replace('0', 'o').replace('3', 'е') \
        .split(' ')
    print(msg)
    for i in msg:
        if i in bword_list:
            await message.delete()
            await message.author.send('Прошу не употреблять плохие слова!')

    if random.randint(1, 20) <= 3:
        if message.author.name != 'bad bot':
            await message.channel.send(random.choice(emojis))

    if message.content.lower() == 'no u' or message.content.lower() == 'no you':
        await message.channel.send(f'{message.author.name}, no u')


@bot.command(name='clear', description=' — для чистки чата.')
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Очищенно {amount} сообщений!')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('really bad bot!'))


@bot.command(name='ban', description=' — для бана плохих ребят.')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason='что-то плохое!'):
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} забанен за {reason}')


@bot.command(name='commands', description=' — для вывода, того, что бот умеет.', hidden=True)
async def help_com(ctx):
    comm_list = ['Используйте префикс `./` \n']
    for command in bot.commands:
        if not command.hidden:
            comm_list.append(f'`{command}` {command.description}\n')
    embed = discord.Embed(
        title=f'Список команд для {bot.user.name}:',
        description=''.join(comm_list),
        color=ctx.author.colour)
    embed.set_footer(text=f'Вызвано пользователем {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(
        url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Goose_clipart_01.svg/740px-Goose_clipart_01.svg.png')

    await ctx.send(embed=embed)


@bot.command(name='kick', description=' — для кика участника.')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason='что-то плохое!'):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} кикнут за {reason}')


bot.run(TOKEN)
