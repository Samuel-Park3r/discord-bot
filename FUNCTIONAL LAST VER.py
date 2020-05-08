import discord, random, os, sqlite3, youtube_dl, string
from discord.ext import commands
from discord.utils import get

DB = sqlite3.connect('main_DB.db')
bwords = DB.cursor().execute('''SELECT words FROM bad_words''').fetchall()
bword_list = []
eng = string.ascii_lowercase
num = string.digits

deletion_checker = False
for a in bwords:
    for e in a:
        bword_list.append(e)

TOKEN = "NzAzNTM4MzQ1OTA4NjMzNjAw.XqQDkw.Rc6DlAEfOFMk_vy8BGxZueQaoU4"
emojis = ['<:harold:707287826085183588>', '<:kermit:707287825749377165> ', '<:who_r_u:707287825741250560> ',
          '<:classic:707287825674141746> ', '<:feelsbadman:707296702033559605> ', '<:pepega:707287825623547955> ',
          '<:itsfine:707295832499552368>', '<:think_about:707287825405575208> ', '<:yes:707287824436560012>',
          ':eggplant:', ':new_moon_with_face:']
bot = commands.Bot(command_prefix='./')


# events

@bot.event
async def on_message(message):
    global deletion_checker
    await bot.process_commands(message)

    xp = DB.cursor().execute(f'SELECT xp FROM users WHERE id = {str(message.author.id)}').fetchall()
    if len(xp) == 0:
        if message.author.id != 703538345908633600:
            DB.cursor().execute(f'INSERT INTO users VALUES ({str(message.author.id)}, {1}) ')
            DB.commit()
    else:
        DB.cursor().execute(f'UPDATE users SET xp = {str(xp[0][0] + 1)} WHERE id = {str(message.author.id)}')
        DB.commit()
    if message.channel.id == 693417279907561502:
        msg = message.content.lower()
        print(msg)
        msg1 = msg.replace(',', '').replace('.', '').replace('!', '').replace('/', '') \
            .replace('?', '').replace('|', '').replace('<', '').replace('>', '').replace('@', 'а').replace('0', 'о') \
            .replace('3', 'е').replace(':', '').replace(';', '').replace('`', '').replace('1', '').replace('2', '') \
            .replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '')
        eng_count = 0
        num_count = 0
        print(msg1)

        for i in range(len(msg1)):
            if msg1[i] in eng:
                eng_count += 1
            elif msg1[i] in num:
                num_count += 1
        if len(msg1) - eng_count - num_count < eng_count:
            if message.author.id != 703538345908633600:
                if msg[0:2] != './':
                    if msg[0] != ':' and msg[-1] != ':':
                        if msg[0:2] != '<:' and msg[-1] != '>':
                            deletion_checker = True
                            await message.delete()
                            await message.author.send('Вы не можете так много писать здесь на английском')

        msg1 = msg1.split(' ')
        if not deletion_checker:
            for i in msg1:
                if i in bword_list:
                    await message.delete()
                    await message.author.send('Прошу не употреблять плохие слова!')
                    break
        else:
            deletion_checker = False
    elif message.channel.id == 693417403689992242:
        msg1 = message.content.lower().replace(',', '').replace('.', '').replace('!', '').replace('/', '') \
            .replace('?', '').replace('|', '').replace('<', '').replace('>', '').replace('@', 'a').replace('0', 'o') \
            .replace('3', 'e').replace(':', '').replace(';', '').replace('`', '').replace('1', '').replace('2', '') \
            .replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '')
        eng_count = 0
        num_count = 0
        for i in range(len(msg1)):
            if msg1[i] in eng:
                eng_count += 1
            elif msg1[i] in num:
                num_count += 1
        if len(msg1) - eng_count - num_count > eng_count:
            if message.author.id != 703538345908633600:
                deletion_checker = True
                await message.delete()
                await message.author.send('Вы не можете так много писать здесь на русском')
        msg1 = msg1.split(' ')
        if not deletion_checker:
            for i in msg1:
                if i in bword_list:
                    await message.delete()
                    await message.author.send('Прошу не употреблять плохие слова!')
                    break
        else:
            deletion_checker = False

    if random.randint(1, 100) <= 10:
        if message.author.name != 'bad bot':
            await message.channel.send(random.choice(emojis))

    if message.content.lower() == 'no u' or message.content.lower() == 'no you':
        await message.channel.send(f'{message.author.name}, no u')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('really bad bot!'))


# commands

@bot.command(name='join', description=' — для того что бы бот вошел в голосовой чат')
async def join(ctx):
    if ctx.message.channel.id == 708299045180932147:
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send(f'Бот присоединился к каналу: {channel}')
    else:
        await ctx.send('Вы не можете сделать это в этом канале. Перейдите в канал специально сделаный для этого')


@bot.command(name='play', description=' — для проигрывания музыки')
async def play_music(ctx, url: str):
    if ctx.message.channel.id == 708299045180932147:
        song_there = os.path.isfile('song.mp3')

        try:
            if song_there:
                os.remove('song.mp3')
                print('[log] Старый файл удален')
        except PermissionError:
            print('[log] Не удалось удалить файл')

        await ctx.send('Пожалуйста ожидайте')

        voice = get(bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('[log] Загружаю музыку...')
            ydl.download([url])

        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                print(f'[log] Переименовываю файл: {file}')
                os.rename(file, 'song.mp3')

        voice.play(discord.FFmpegPCMAudio('song.mp3'),
                   after=lambda x: print(f'[log] {name}, музыка закончила своё проигрывание'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        song_name = name.rsplit('-', 2)
        await ctx.send(f'Сейчас играет: {song_name[0]}')
    else:
        await ctx.send('Вы не можете сделать это в этом канале. Перейдите в канал специально сделаный для этого')


@bot.command(name='leave', description=' — для того что бы бот вышел из голосового чата')
async def leave(ctx):
    if ctx.message.channel.id == 708299045180932147:
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'Бот отключился от канала: {channel}')
        else:
            voice = await channel.connect()
            await ctx.send(f'Бот отключился от канала: {channel}')
    else:
        await ctx.send('Вы не можете сделать это в этом канале. Перейдите в канал специально сделаный для этого')


@bot.command(name='report', description=' — репортит плохих чувачков')
async def report(ctx, member: discord.Member, reason='плохое поведение'):
    global deletion_checker
    if ctx.message.channel.id == 708299045180932147:
        ctx.message.delete()
        deletion_checker = True
        await ctx.send(f'Подана жалоба от участника {ctx.author.name} на учстника {member.name} по причине: {reason}.'
                       f' Жалоба будет рассмотрена в ближайшее время администратором.')
        await ctx.author.send(f'Вами была подана жалоба на учстника {member.name} по причине: {reason}.'
                              f' Жалоба будет рассмотрена в ближайшее время администратором.')
        await member.send(f'На вас была подана жалоба по причине: {reason}.'
                          f' Жалоба будет рассмотрена в ближайшее время администратором.')
    else:
        await ctx.send('Вы не можете сделать это в этом канале. Перейдите в канал специально сделаный для этого')


@bot.command(name='commands', description=' — для вывода, того, что бот умеет.')
async def help_com(ctx):
    if ctx.message.channel.id == 708299045180932147:
        comm_list = ['Используйте префикс `./` \n']
        for command in bot.commands:
            if not command.hidden:
                comm_list.append(f'`{command}` {command.description}\n')
        embed = discord.Embed(title=f'Список команд для {bot.user.name}:', description=''.join(comm_list),
                              color=ctx.author.colour)
        embed.set_footer(text=f'Вызвано пользователем {ctx.author}', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(
            url='''https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Goose_clipart_01.svg/740px-Goose_clipart_01.svg.png''')

        await ctx.send(embed=embed)
    else:
        await ctx.send('Вы не можете сделать это в этом канале. Перейдите в канал специально сделаный для этого')


# admin commands

@bot.command(name='about', description=' — показывает инфу')
async def me(ctx, member: discord.Member = 'exception'):
    if ctx.message.channel.id == 708299045180932147:
        info = []
        if member == 'exception':
            xp = DB.cursor().execute(f'SELECT xp FROM users WHERE id = {str(ctx.author.id)}').fetchall()[0][0]
            info.append(f'Уровень: {xp // 150} \n')
            info.append(f'Опыт: {xp % 150} (Всего: {xp}) \n')
            info_embed = discord.Embed(title=f'Инфа о {ctx.author.name}:', description=''.join(info),
                                       color=ctx.author.colour)
            info_embed.set_thumbnail(url='{}'.format(ctx.author.avatar_url))
        else:
            xp = DB.cursor().execute(f'SELECT xp FROM users WHERE id = {str(member.id)}').fetchall()[0][0]
            info.append(f'Уровень: {xp // 150} \n')
            info.append(f'Опыт: {xp % 150} (Всего: {xp}) \n')
            info_embed = discord.Embed(title=f'Инфа о {member.name}:', description=''.join(info),
                                       color=member.colour)
            info_embed.set_thumbnail(url='{}'.format(member.avatar_url))
        await ctx.send(embed=info_embed)
    else:
        await ctx.send('Вы не можете сделать это в этом канале. Перейдите в канал специально сделаный для этого')


@bot.command(name='clear', description=' — для чистки чата.')
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=10):
    global deletion_checker
    deletion_checker = True
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Очищенно {amount} сообщений!')


@bot.command(name='ban', description=' — для бана плохих ребят.')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason='что-то плохое!'):
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} забанен за {reason}')


@bot.command(name='kick', description=' — для кика участника.')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason='что-то плохое!'):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} кикнут за {reason}')


bot.run(TOKEN)
