import discord, random, os, sqlite3, youtube_dl
from discord.ext import commands
from discord.utils import get

# Токен бота нашего сервера
TOKEN = "NzAzNTM4MzQ1OTA4NjMzNjAw.XqQDkw.Rc6DlAEfOFMk_vy8BGxZueQaoU4"

# Весь мусор для работы: бд, роли, id и тд

# БД для фильтра чата
DB = sqlite3.connect('main_DB.db')
bwords = DB.cursor().execute('''SELECT words FROM bad_words''').fetchall()
bword_list = []

# Получения ролей
ROLES = {
    '🐍': 708353562643791964,  # Programmer
    '🧱': 708353724803973151,  # 3D'шник
    '🎮': 708353373425893456,  # Gamer
    '👶': 708354296739004487,  # Beginner
    '👌': 698449484434112543,  # PePeGa UsEr
}
# id поста для получения ролей
POST_ID_ROLES = 708360403880509572
POST_ID_INFO = 708381510784254012

# Распаковка фильтра плохих слов
for a in bwords:
    for e in a:
        bword_list.append(e)

# Дополнительный набор emoji
emojis = ['<:harold:707287826085183588>', '<:kermit:707287825749377165> ', '<:who_r_u:707287825741250560> ',
          '<:classic:707287825674141746> ', '<:feelsbadman:707296702033559605> ', '<:pepega:707287825623547955> ',
          '<:itsfine:707295832499552368>', '<:think_about:707287825405575208> ', '<:yes:707287824436560012>',
          ':eggplant:', ':new_moon_with_face:']

# Вызов команд бота
bot = commands.Bot(command_prefix='./')


# EVENTS


# Проверка на подключение бота к серверу
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('really bad bot!'))


# Обработка сообщений
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    xp = DB.cursor().execute(f'SELECT xp FROM users WHERE id = {str(message.author.id)}').fetchall()
    if len(xp) == 0:
        if message.author.id != 703538345908633600:
            DB.cursor().execute(f'INSERT INTO users VALUES ({str(message.author.id)}, {1}) ')
            DB.commit()
    else:
        DB.cursor().execute(f'UPDATE users SET xp = {str(xp[0][0] + 1)} WHERE id = {str(message.author.id)}')
        DB.commit()

    msg = message.content.lower().replace(',', '').replace('.', '').replace('!', '').replace('/', '').replace('?', '') \
        .replace('|', '').replace('<', '').replace('>', '').replace('@', 'а').replace('0', 'o').replace('3', 'е') \
        .replace(':', '').replace(';', '').replace('`', '').split(' ')
    for i in msg:
        if i in bword_list:
            await message.delete()
            await message.author.send('Прошу не употреблять плохие слова!')
            break

    if random.randint(1, 100) <= 10:
        if message.author.name != 'bad bot':
            await message.channel.send(random.choice(emojis))

    if message.content.lower() == 'no u' or message.content.lower() == 'no you':
        await message.channel.send(f'{message.author.name}, no u')


# Определение ролей, добавление роли
@bot.event
async def on_raw_reaction_add(payload):
    # Глобальные роли
    if payload.message_id == POST_ID_ROLES:  # ID Сообщения
        guild = bot.get_guild(payload.guild_id)
        role = None

        if str(payload.emoji) == '🐍':  # Emoji для реакций
            role = guild.get_role(708353562643791964)  # ID Ролей для выдачи
        elif str(payload.emoji) == '🧱':
            role = guild.get_role(708353724803973151)
        elif str(payload.emoji) == '🎮':
            role = guild.get_role(708353373425893456)
        elif str(payload.emoji) == '👶':
            role = guild.get_role(708354296739004487)

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.add_roles(role)

    # Основная роль прочитавшего правила
    elif payload.message_id == POST_ID_INFO:  # ID Сообщения
        guild = bot.get_guild(payload.guild_id)
        role = None

        if str(payload.emoji) == '👌':
            role = guild.get_role(698449484434112543)

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.add_roles(role)


# Определение ролей, забирание роли
@bot.event
async def on_raw_reaction_remove(payload):
    # Глобальные роли
    if payload.message_id == POST_ID_ROLES:  # ID Сообщения
        guild = bot.get_guild(payload.guild_id)
        role = None

        if str(payload.emoji) == '🐍':
            role = guild.get_role(708353562643791964)
        elif str(payload.emoji) == '🧱':
            role = guild.get_role(708353724803973151)
        elif str(payload.emoji) == '🎮':
            role = guild.get_role(708353373425893456)
        elif str(payload.emoji) == '👶':
            role = guild.get_role(708354296739004487)

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.remove_roles(role)

    # Основная роль прочитавшего правила
    elif payload.message_id == POST_ID_INFO:  # ID Сообщения
        guild = bot.get_guild(payload.guild_id)
        role = None

        if str(payload.emoji) == '👌':
            role = guild.get_role(698449484434112543)

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.remove_roles(role)


# COMMANDS

# Команды для бота
@bot.command(name='commands', description=' — для вывода, того, что бот умеет.')
async def help_com(ctx):
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


# Присоединение к чату
@bot.command(name='join', description=' — для того что бы бот вошел в голосовой чат')
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоединился к каналу: {channel}')


# Проигрывание музыки
@bot.command(name='play', description=' — для проигрывания музыки')
async def play_music(ctx, url: str):
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


# Отсоединение от чата
@bot.command(name='leave', description=' — для того что бы бот вышел из голосового чата')
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'Бот отключился от канала: {channel}')
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот отключился от канала: {channel}')


# Жалоба на участника
@bot.command(name='report', description=' — репортит плохих чувачков')
async def report(ctx, member: discord.Member, reason='плохое поведение'):
    await ctx.send(f'Подана жалоба от участника {ctx.author.name} на учстника {member.name} по причине {reason}.'
                   f' Жалоба будет рассмотрена в ближайшее время администратором.')
    await ctx.author.send(f'Вами была подана жалоба на учстника {member.name} по причине {reason}.'
                          f' Жалоба будет рассмотрена в ближайшее время администратором.')
    await member.send(f'На вас была подана жалоба от участника {ctx.author.name} по причине {reason}.'
                      f' Жалоба будет рассмотрена в ближайшее время администратором.')
    print(f'Подана жалоба от участника {ctx.author.name} на учстника {member.name} по причине {reason}.')


# Показывает информацию о участнике
@bot.command(name='about', description=' — показывает инфу')
async def me(ctx, member: discord.Member = 'exception'):
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


# Очищение чата
@bot.command(name='clear', description=' — для чистки чата.')
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Очищенно {amount} сообщений!')


# Бан участников
@bot.command(name='ban', description=' — для бана плохих ребят.')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason='что-то плохое!'):
    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} забанен за {reason}')


# Разбан участника
@bot.command(name='unban', description=' — для разбана участника.')
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)

    banned_users = await ctx.guild.bans()

    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)
        await ctx.send(f'Участник {user.mention} был разбанен')
        return


# Кик участника
@bot.command(name='kick', description=' — для кика участника.')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason='что-то плохое!'):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} кикнут за {reason}')


# Мут участника
@bot.command(name='user_mute', description=' — для мута участника.')
@commands.has_permissions(administrator=True)
async def user_mute(ctx, member: discord.Member):
    # Удаление самого сообщения
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name='MUTED')

    await member.add_roles(mute_role)
    await ctx.send(f'У {member.mention} ограничение чата за нарушение прав!')


# Канал для голосований
@bot.command(
    aliases=["Предложить", "предложить", "предложка", "Предложка", "Suggest"])  # Вариации разных написаний комманды
async def suggest(ctx, *, agr):
    suggest_chanell = bot.get_channel(708407159418912781)  # id канала предложки
    embed = discord.Embed(title=f"{ctx.author.name} предложил :", description=f" {agr} \n\n")

    embed.set_thumbnail(url=ctx.guild.icon_url)

    message = await suggest_chanell.send(embed=embed)
    await message.add_reaction('✅')
    await message.add_reaction('❎')


# Получение аватарки участника
@bot.command(name='get_avatar', description=' — для получения аватарки участника.')
async def avatar(ctx, member: discord.Member = None):
    user = ctx.message.author if (member == None) else member
    embed = discord.Embed(title=f'Аватар пользователя {user}', color=0x0c0c0c)
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)


bot.run(TOKEN)
