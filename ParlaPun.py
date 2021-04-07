import discord
import discord.permissions
from discord.ext import commands,tasks
import datetime
import asyncio
import sqlite3

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix='!',intents = intents)

client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.playing, name="ParlaPun version 1.10 (BETA)   !helpstaff"))
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS main(
    member_id TEXT,
    end_mute TEXT,
    end_ban TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
    member_id TEXT,
    from_id TEXT,
    datetime TEXT,
    howlong TEXT,
    reason TEXT,
    type TEXT    
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comment(
    member_id TEXT,
    url TEXT,
    reason TEXT
    )
    ''')
    timeban.start()
    timemute.start()
    print("bot is ready")

@tasks.loop(seconds=1)
async def timemute():
    guild = client.get_guild(782649390136688642)

    date = datetime.datetime.today()
    time = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
    fixdate = time.strftime('%d-%m-%Y-%H-%M-%S')

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT member_id FROM main WHERE end_mute = '{str(fixdate)}'")
    result = cursor.fetchone()

    if result is not None:
        for id_ in result:
            member2 = await client.fetch_user(id_)
            for role in guild.roles:
                if role.name == 'מורחק מכתיבה':
                    for member in guild.members:
                        if member2 == member:
                            await member.remove_roles(role)
                            for channel in guild.channels:
                                if channel.name == '⛔┃עונשים':
                                    embed = discord.Embed(title="ביטול השתקה (השתקה זמית)",description=f'בוטלה ההרחקה ל- {member.mention}',colour=discord.Colour.light_gray())
                                    embed.set_footer(text="Gamer Top/Appleツ🍏")
                                    await channel.send(embed=embed)
    db.commit()
    cursor.close()
    db.close()

@tasks.loop(seconds=1)
async def timeban():
    guild = client.get_guild(782649390136688642)

    date = datetime.datetime.today()
    time = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
    fixdate = time.strftime('%d-%m-%Y-%H-%M-%S')

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT member_id FROM main WHERE end_ban = '{str(fixdate)}'")
    result = cursor.fetchone()

    if result is not None:
        for id_ in result:
            member = await client.fetch_user(id_)
            await guild.unban(member)
            for channel in guild.channels:
                if channel.name == '⛔┃עונשים':
                    embed = discord.Embed(title="ביטול הרחקה (הרחקה זמית)",description=f' {member.mention} בוטלה ההרחקה ל- ',colour=discord.Colour.light_gray())
                    embed.set_footer(text="Gamer Top/Appleツ🍏")
                    await channel.send(embed=embed)

    db.commit()
    cursor.close()
    db.close()

@client.command()
@commands.has_any_role("עוזר", "מפקח דיסקורד", "אחראי דיסקורד")
async def helpstaff(ctx):
    embed = discord.Embed(title="פקודות צוות דיסקורד | Parlamentum 🪓",description=' פקודות לצוות הדיסקורד של הפרלמנטום.', colour=discord.Colour.light_gray())
    embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
    embed.set_footer(text="ParlaPun version 1.10 (BETA)")
    embed.add_field(name='!clear', value="!clear [messages]\n מנקה כמות הודעות עד שנבחרת 100")
    embed.add_field(name='!lockdown', value="!lockdown\n סוגר את האפשרות לרשום בצאט, לצוות גבוה בלבד")
    embed.add_field(name='!unlock', value="!unlock\n פותח את האפשרות לרשום בצאט, לצוות גבוה בלבד")
    embed.add_field(name='!tempmute',value="!tempmute [@member] [duration] [reason]\n  השתקה זמנית למשתמש")
    embed.add_field(name='!tempban',value="!tempban [@member] [duration] [reason]\n  הרחקה זמנית למשתמש")
    embed.add_field(name='!mute', value="!mute [@member] [reason]\n השתקה תמידית למשתמש")
    embed.add_field(name='!ban', value="!ban [@member] [reason]\n הרחקה תמידית למשתמש")
    embed.add_field(name='!unban', value="!unban [@member]\n הורדת הרחקה למשתמש")
    embed.add_field(name='!unmute', value="!unmute [@member]\n הורדת השתקה למשתמש")
    embed.add_field(name='!history',value="!history [@member]\n מציג את הסטורית העונשים של המשתמש")
    embed.add_field(name='!comment',value="!comment [@member] [url] [reason]\n רשימת הוחכה למשתמש מסויים")
    embed.add_field(name='!comments',value="!comments [@member]\n מציג את רשימת ההוחכות של המשתמש")
    await ctx.send(embed=embed)


@client.command()
@commands.has_any_role("מפקח דיסקורד", "אחראי דיסקורד")
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title="נוקה", description=f'  ➡  נמחקו  ️{amount} הודעות ',colour=discord.Colour.light_gray())
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.set_footer(text="ParlaPun version 1.10 (BETA)")
    await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=1)


@client.command()
@commands.has_any_role("מפקח דיסקורד", "אחראי דיסקורד")
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(title=f'🪓 | הרחקה', description=f'{member.mention} הורחק לצמיתות  ',colour=discord.Colour.light_gray())
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.set_footer(text="ParlaPun version 1.10 (BETA)")
    embed.add_field(name="סיבה - ", value=reason, inline=False)
    embed.add_field(name='הזמן הנשאר לעונש - ', value=f"הרחקה תמידית.")
    embed.add_field(name='העונש ניתן על ידי - ', value=f"{ctx.author}", inline=False)
    await ctx.send(embed=embed)

    fixdate = datetime.datetime.today().strftime('%d-%m-%Y-%H-%M-%S')

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    sql = ("INSERT INTO history(member_id, from_id, datetime, reason, type) VALUES(?,?,?,?,?)")
    val = (str(member.id), str(ctx.author.id), str(fixdate), reason, "הרחקה תמידת")

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


@client.command()
@commands.has_any_role("מפקח דיסקורד", "אחראי דיסקורד")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)

            embed = discord.Embed(title="🪓 | הסרת הרחקה", description=f" ההרחקה הוסרה ל - {member_name}#{member_discriminator}",colour=discord.Colour.light_gray())
            embed.set_author(name=ctx.author,
            icon_url=ctx.author.avatar_url)
            embed.set_footer(text="ParlaPun version 1.10 (BETA)")
            embed.add_field(name=' ניתן על ידי - ', value=f"{ctx.author}", inline=False)
            await ctx.send(embed=embed)

@client.command(description="Mutes the specified user.")
@commands.has_any_role("עוזר", "מפקח דיסקורד", "אחראי דיסקורד")
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="מורחק מכתיבה")

    if not mutedRole:
        mutedRole = await guild.create_role(name="מורחק מכתיבה")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True,read_messages=False)
    embed = discord.Embed(title=" 🪓 | השתקה תמידית", description=f"{member.mention} הושתק לצמיתות ",colour=discord.Colour.light_gray())
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.set_footer(text="ParlaPun version 1.10 (BETA)")
    embed.add_field(name="סיבה - ", value=reason, inline=False)
    embed.add_field(name='העונש ניתן על ידי - ', value=f"{ctx.author}", inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    fixdate = datetime.datetime.today().strftime('%d-%m-%Y-%H-%M-%S')

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    sql = ("INSERT INTO history(member_id, from_id, datetime, reason, type) VALUES(?,?,?,?,?)")
    val = (str(member.id), str(ctx.author.id), str(fixdate), reason, "השתקה תמידית")

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


@client.command()
@commands.has_any_role("עוזר", "מפקח דיסקורד", "אחראי דיסקורד")
async def tempmute(ctx, member: discord.Member, time, *, reason=None):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "מורחק מכתיבה":
            await member.add_roles(role)

            embed = discord.Embed(title="🪓 | השתקה זמנית", description=f" הושתק זמית {member.mention}", color=discord.Colour.light_gray())
            embed.set_author(name=ctx.author,icon_url=ctx.author.avatar_url)
            embed.add_field(name="סיבה - ", value=reason, inline=False)
            embed.add_field(name='העונש ניתן על ידי - ', value=f"{ctx.author}", inline=False)
            embed.add_field(name="הזמן הנשאר להשתקה - ", value=f"{time}",inline=False)

            d = time[-1]

            num = int(time[:-1])

            date = datetime.datetime.today()

            if d == "s":
                left = datetime.timedelta(seconds=num)
                date2 = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
                timeall = left + date2

            if d == "m":
                left = datetime.timedelta(minutes=num)
                date2 = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
                timeall = left + date2

            if d == "h":
                left = datetime.timedelta(hours=num)
                date2 = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
                timeall = left + date2

            if d == "d":
                left = datetime.timedelta(days=num)
                date2 = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
                timeall = left + date2

            embed.add_field(name=' סיום המיוט ב - ' , value=str((timeall)))
            embed.set_footer(text="ParlaPun version 1.10 (BETA)")
            await ctx.send(embed=embed)

            fixdate = timeall.strftime('%d-%m-%Y-%H-%M-%S')

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT end_mute FROM main WHERE member_id = {str(member.id)}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(member_id, end_mute) VALUES(?,?)")
                val = (str(member.id), str(fixdate))

            elif result is not None:
                sql = ("UPDATE main SET end_mute = ? WHERE member_id = ?")
                val = (str(fixdate), str(member.id))

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            sql = ("INSERT INTO history(member_id, from_id, datetime, howlong, reason, type) VALUES(?,?,?,?,?,?)")
            val = (str(member.id), str(ctx.author.id), str(fixdate), time, reason, "השתקה זמנית")

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            return

@client.command()
@commands.has_any_role("עוזר", "מפקח דיסקורד", "אחראי דיסקורד")
async def history(ctx, member: discord.Member):
    embed = discord.Embed(title=f"📜 | הסטוריה", description=f"הסטורית העונשים של {member.mention}", color=discord.Colour.light_gray())
    embed.set_footer(text="ParlaPun version 1.10 (BETA)")
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT datetime FROM history WHERE member_id = '{str(member.id)}'")
    result = cursor.fetchall()
    for date in result:
        for time in date:
            db2 = sqlite3.connect("main.sqlite")
            cursor2 = db2.cursor()
            cursor2.execute(f"SELECT reason FROM history WHERE datetime = '{str(time)}'")
            reason = cursor2.fetchone()

            db2.commit()
            cursor2.close()
            db2.close()

            db2 = sqlite3.connect("main.sqlite")
            cursor2 = db2.cursor()
            cursor2.execute(f"SELECT from_id FROM history WHERE datetime = '{str(time)}'")
            from_id = cursor2.fetchone()

            db2.commit()
            cursor2.close()
            db2.close()

            db2 = sqlite3.connect("main.sqlite")
            cursor2 = db2.cursor()
            cursor2.execute(f"SELECT type FROM history WHERE datetime = '{str(time)}'")
            type = cursor2.fetchone()

            db2.commit()
            cursor2.close()
            db2.close()

            db2 = sqlite3.connect("main.sqlite")
            cursor2 = db2.cursor()
            cursor2.execute(f"SELECT howlong FROM history WHERE datetime = '{str(time)}'")
            howlong = cursor2.fetchone()

            db2.commit()
            cursor2.close()
            db2.close()

            user = await client.fetch_user(from_id[0])

            if howlong[0] is None:
                embed.add_field(name=f"{reason[0]}", value=f"{type[0]} ב - {time}\n על ידי - {user}", inline=False)

            else:
                embed.add_field(name=f"{reason[0]}", value=f"{type[0]} ב - {time}\n על ידי - {user}\n לזמן - {howlong[0]}", inline=False)

    await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("מפקח דיסקורד", "אחראי דיסקורד")
async def tempban(ctx, member: discord.Member, time, *, reason=None):

    embed = discord.Embed(title="🪓 | הרחקה זמנית", description=f"{member.mention} הורחק זמנית מהשרת ", colour=discord.Colour.light_gray())
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.add_field(name="סיבה - ", value=reason, inline=False)
    embed.add_field(name="הזמן הנשאר להרחקה - ", value=f"{time}", inline=False)
    embed.add_field(name='העונש ניתן על ידי - ', value=f"{ctx.author}", inline=False)

    d = time[-1]

    num = int(time[:-1])

    date = datetime.datetime.today()

    if d == "s":
        left = datetime.timedelta(seconds=num)
        date2 = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
        timeall = left + date2

    if d == "m":
        left = datetime.timedelta(minutes=num)
        date2 = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
        timeall = left + date2

    if d == "h":
        left = datetime.timedelta(hours=num)
        date2 = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
        timeall = left + date2

    if d == "d":
        left = datetime.timedelta(days=num)
        date2 = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)
        timeall = left + date2

    embed.add_field(name="סיום ההרחקה ב-", value=str(timeall), inline=False)
    embed.set_footer(text="ParlaPun version 1.10 (BETA)")
    await ctx.send(embed=embed)

    fixdate = timeall.strftime('%d-%m-%Y-%H-%M-%S')

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT end_ban FROM main WHERE member_id = {str(member.id)}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO main(member_id, end_ban) VALUES(?,?)")
        val = (str(member.id), str(fixdate))

    elif result is not None:
        sql = ("UPDATE main SET end_ban = ? WHERE member_id = ?")
        val = (str(fixdate), str(member.id))

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    sql = ("INSERT INTO history(member_id, from_id, datetime, howlong, reason, type) VALUES(?,?,?,?,?,?)")
    val = (str(member.id), str(ctx.author.id), str(fixdate), time, reason, "הרחקה זמנית")

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

    await member.ban(reason=reason)

    return

@client.command()
@commands.has_any_role("עוזר", "מפקח דיסקורד", "אחראי דיסקורד")
async def unmute(ctx, member: discord.Member, *, reason=None):
    mutedRole = discord.utils.get(ctx.guild.roles, name="מורחק מכתיבה")

    await member.remove_roles(mutedRole)
    embed = discord.Embed(title="🪓 | ביטול השתקה", description=f" בוטלה ההשתקה ל-{member.mention}",colour=discord.Colour.light_gray())
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.set_footer(text="ParlaPun version 1.10 (BETA)")
    embed.add_field(name=' ניתן על ידי - ', value=f"{ctx.author}", inline=False)
    embed.add_field(name="סיבה - ", value=reason, inline=False)
    await ctx.send(embed=embed)

    fixdate = datetime.datetime.today().strftime('%d-%m-%Y-%H-%M-%S')

    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    sql = ("INSERT INTO history(member_id, from_id, datetime, reason, type) VALUES(?,?,?,?,?)")
    val = (str(member.id), str(ctx.author.id), str(fixdate), reason, "ביטול השתקה")

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()





@client.command()
@commands.has_role("אחראי דיסקורד")
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title="החדר נסגר! ", description=f" 🔒 {ctx.channel} סגור כעת ",color=discord.Colour.light_gray())
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.set_footer(text="ParlaPun version 1.10 (BETA)")
    await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=1)


@client.command()
@commands.has_role("אחראי דיסקורד")
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title="החדר נפתח! ", description=f" 🔓 {ctx.channel} פתוח כעת ",color=discord.Colour.light_gray())
    embed.set_author(name=ctx.author,
    icon_url=ctx.author.avatar_url)
    embed.set_footer(text="ParlaPun version 1.10 (BETA)")
    await ctx.send(embed=embed)
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=1)


@client.command()
@commands.has_any_role("עוזר", "מפקח דיסקורד", "אחראי דיסקורד")
async def comment(ctx, member: discord.Member, url, *, reason = None):
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    sql = ("INSERT INTO comment(member_id, url, reason) VALUES(?,?,?)")
    val = (str(member.id), str(url), reason)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

    embed = discord.Embed(title="📄 | הוכחה", description=f"ההוכחה נרשמה בהצלחה!",color=discord.Colour.light_gray())
    await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("עוזר", "מפקח דיסקורד", "אחראי דיסקורד")
async def comments(ctx, member: discord.Member):
    embed = discord.Embed(title="📄 | הוכחות", description=f" רשימת ההוכחות על - {member.mention}",color=discord.Colour.light_gray())
    db = sqlite3.connect("main.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT url FROM comment WHERE member_id = '{str(member.id)}'")
    url_list = cursor.fetchall()

    for urls in url_list:
        for url in urls:
            db2 = sqlite3.connect("main.sqlite")
            cursor2 = db2.cursor()
            cursor2.execute(f"SELECT reason FROM comment WHERE url = '{str(url)}'")
            reason = cursor2.fetchone()

            embed.add_field(name=f"{reason[0]}", value=f"{url}", inline=False)

            db2.commit()
            cursor2.close()
            db2.close()

    db.commit()
    cursor.close()
    db.close()

    await ctx.send(embed=embed)

client.run('Nzg2MTg1ODc5MjM2Mzc4NjM0.X9CuqA.xz7dz7BlQsQ_dMgTB5YdnHhYX8U')