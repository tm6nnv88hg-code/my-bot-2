import discord
from discord.ext import commands
import random
import datetime
import os

# ڕێکخستنی دەسەڵاتەکانی بۆت (Intents)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# پێشگری بۆتەکە نیشانەی "!" دەبێت
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'=== بۆتەکە ئۆنلاین بوو و ئامادەیە! ===')
    print(f'ناوی بۆت: {bot.user.name}')
    print(f'ئایدی بۆت: {bot.user.id}')
    await bot.change_presence(activity=discord.Game(name="!help | ٢٤ کاتژمێر ئۆنلاین"))

# ==============================================================================
# بەشی یەکەم: فەرمانەکانی هاوکاری و زانیاری (Information & Help) - ١٠ کۆماند
# ==============================================================================

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 لیستی تەواوی فەرمانەکانی بۆت", color=discord.Color.blue())
    embed.add_field(name="🛡️ کارگێڕی (Admin)", value="`kick`, `ban`, `unban`, `mute`, `unmute`, `clear`, `lock`, `unlock`, `warn`, `warns`, `clearwarns`, `slowmode`, `addrole`, `removerole`, `nick`", inline=False)
    embed.add_field(name="📊 زانیاری (Utility)", value="`ping`, `userinfo`, `serverinfo`, `avatar`, `botinfo`, `membercount`, `roles`, `invite`, `uptime`, `id`", inline=False)
    embed.add_field(name="🎉 کات بەسەربردن (Fun)", value="`say`, `roll`, `coinflip`, `joke`, `meme`, `choose`, `love`, `8ball`, `predict`, `rps`", inline=False)
    embed.add_field(name="⚙️ ڕێکخستنی پێشکەوتوو", value="`embed`, `poll`, `memberinfo`, `channelinfo`, `servericon`, `channelcount`, `roleinfo`, `boosts`, `creationdate`, `pingstatus`", inline=False)
    embed.set_footer(text="بۆ بەکارهێنانی هەر فەرمانێک نیشانەی ! پێش ناوەکە دابنێ")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f'🏓 Pong! خێرایی بۆت: {round(bot.latency * 1000)}ms')

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"زانیاری بەکارهێنەر: {member.name}", color=member.color)
    embed.add_field(name="ناونیشان/ناو:", value=member.mention)
    embed.add_field(name="ئایدی (ID):", value=member.id)
    embed.add_field(name="بەرواری دروستکردنی ئەکاونت:", value=member.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="بەرواری هاتنە ناو سێرڤەر:", value=member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "نادیار")
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"زانیاری سێرڤەری: {guild.name}", color=discord.Color.green())
    embed.add_field(name="خاوەنی سێرڤەر:", value=guild.owner.mention if guild.owner else "نادیار")
    embed.add_field(name="ئایدی سێرڤەر:", value=guild.id)
    embed.add_field(name="ژمارەی ئەندامان:", value=guild.member_count)
    embed.add_field(name="ژمارەی چات و دەنگ:", value=len(guild.channels))
    embed.add_field(name="ژمارەی ڕانکەکان (Roles):", value=len(guild.roles))
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"وێنەی پرۆفایلی {member.name}", color=discord.Color.random())
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(title="🤖 زانیاری دەربارەی بۆتەکە", description="بۆتێکی پێشکەوتوو بە زمانی Python", color=discord.Color.purple())
    embed.add_field(name="کتێبخانە:", value="Discord.py")
    embed.add_field(name="سیستەمی هۆست:", value="Online 24/7")
    embed.add_field(name="پێشگر (Prefix):", value="`!`")
    await ctx.send(embed=embed)

@bot.command()
async def membercount(ctx):
    await ctx.send(f"📊 ژمارەی ئەندامانی سێرڤەر: **{ctx.guild.member_count}** ئەندام.")

@bot.command()
async def roles(ctx):
    role_list = [role.name for role in ctx.guild.roles if role.name != "@everyone"]
    await ctx.send(f"🎭 ڕانکەکانی سێرڤەر ({len(role_list)}): " + ", ".join(role_list[:30]) + ("..." if len(role_list) > 30 else ""))

@bot.command()
async def invite(ctx):
    await ctx.send("🔗 بۆ هێنانی بۆتەکە بۆ سێرڤەری خۆت ئەم لینکە بەکاربهێنە: \nhttps://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot")

@bot.command()
async def id(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"🆔 ئایدی {member.mention} بریتییە لە: `{member.id}`")

# ==============================================================================
# بەشی دووەم: فەرمانەکانی کارگێڕی و ڕێکخستن (Moderation) - ١٥ کۆماند
# ==============================================================================

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'👤 {member.mention} دەرکرا لە سێرڤەر! هۆکار: {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'🚫 {member.mention} باندکرا لە سێرڤەر! هۆکار: {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_name):
    async for entry in ctx.guild.bans(limit=150):
        user = entry.user
        if (user.name == member_name) or (str(user) == member_name):
            await ctx.guild.unban(user)
            await ctx.send(f'✅ {user.mention} باندی لەسەر لادرا.')
            return
    await ctx.send("ئەم بەکارهێنەرە نەدۆزرایەوە لە لیستی باندکراوان.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'🧹 {amount} نامە پاککرایەوە.', delete_after=3)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 چاتی ئەم کەناڵە داخرا.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 چاتی ئەم کەناڵە کرایەوە.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"✅ ڕانکی {role.name} درا بە {member.mention}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"❌ ڕانکی {role.name} لادرا لەسەر {member.mention}")

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=nickname)
    await ctx.send(f"📝 ناوی {member.mention} گۆڕدرا بۆ {nickname}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)
    await member.add_roles(role)
    await ctx.send(f"🔇 {member.mention} میووت کرا.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"🔊 {member.mention} دەنگی بۆ گەڕایەوە.")
    else:
        await ctx.send("ئەم ئەندامە میووت نەکراوە.")

# سیستەمی هۆشداریدان (Warnings System)
bot.user_warns = {}

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason="بێ هۆکار"):
    if member.id not in bot.user_warns:
        bot.user_warns[member.id] = []
    bot.user_warns[member.id].append(reason)
    await ctx.send(f"⚠️ ئاگادارکردنەوە (Warn) درا بە {member.mention}. کۆی گشتی: {len(bot.user_warns[member.id])}")

@bot.command()
async def warns(ctx, member: discord.Member = None):
    member = member or ctx.author
    count = len(bot.user_warns.get(member.id, []))
    await ctx.send(f"👤 {member.mention} خاوەنی **{count}** ئاگادارکردنەوەیە.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def clearwarns(ctx, member: discord.Member):
    if member.id in bot.user_warns:
        bot.user_warns[member.id] = []
        await ctx.send(f"✅ هەموو ئاگادارکردنەوەکانی {member.mention} سڕانەوە.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"⏱️ لۆکاڵی چات (Slowmode) دانرا بۆ {seconds} چرکە.")

# ==============================================================================
# بەشی سێیەم: کات بەسەربردن و کایەکان (Fun & Games) - ١٥ کۆماند
# ==============================================================================

@bot.command()
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 ژمارەی بەختی تۆ لە دایسەکەدا: **{random.randint(1, 6)}**")

@bot.command()
async def coinflip(ctx):
    choices = ["شێر 🦁", "خەت 🪙"]
    await ctx.send(f"🪙 ئەنجامەکەت: **{random.choice(choices)}**")

@bot.command()
async def joke(ctx):
    jokes = [
        "کابرایەک تەلەفۆن بۆ پۆلیس دەکات دەڵێ: دز هاتووەتە ماڵمان! پۆلیس دەڵێ: خەم مەخۆ ئێستا دێین، کابرای دەڵێ: نا بۆ خۆم دەرگام لێ داخستوون بۆتان بگرن!",
        "غەواسێک لەژێر دەریا نامەیەکی بۆ دێت، دەڵێ ئەگەر تەنهای وەرە دەرەوە!",
        "کابرایەک دەچێتە بەردەم ئاوێنە دەڵێ: کێشە نییە گرنگ ئەوەیە ئەخلاقم جوان بێت."
    ]
    await ctx.send(random.choice(jokes))

@bot.command()
async def choose(ctx, *options):
    if len(options) < 2:
        await ctx.send("تکایە لانی کەم دوو هەڵبژاردن بنووسە. نموونە: `!choose یاری خوێندن`")
        return
    await ctx.send(f"🤔 من ئەمەیان هەڵدەبژێرم: **{random.choice(options)}**")

@bot.command()
async def love(ctx, member: discord.Member):
    percentage = random.randint(0, 100)
    await ctx.send(f"❤️ ڕێژەی خۆشەویستی نێوان تۆ و {member.mention} بریتییە لە: **{percentage}%**")

@bot.command()
async def rps(ctx, choice: str):
    options = ["بەرد", "کاغەز", "مەقەس"]
    bot_choice = random.choice(options)
    choice = choice.strip()
    if choice not in options:
        await ctx.send("تکایە بنووسە: `!rps بەرد` یان `کاغەز` یان `مەقەس`")
        return
    await ctx.send(f"🤖 من **{bot_choice}**م هەڵبژارد!")
    if choice == bot_choice: await ctx.send("🤝 یەکسان بووین!")
    elif (choice == "بەرد" and bot_choice == "مەقەس") or (choice == "کاغەز" and bot_choice == "بەرد") or (choice == "مەقەس" and bot_choice == "کاغەز"):
        await ctx.send("🎉 پیرۆزە تۆ بردیەوە!")
    else: await ctx.send("😢 من بردمەوە!")

@bot.command()
async def meme(ctx):
    meme_links = [
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z0M2o4bXNnbWJidWlyN2ZpaDFidm5wMzl6cm85cHZlbXo5eXpwNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/VbnUQpnihPSIgIXuZv/giphy.gif",
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXN6MzNydndvYW1reGszcnFqMmpyYWN2bWNuMG14ejhyeGZ4azE1OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cfuL5gqFDre7K/giphy.gif"
    ]
    await ctx.send(random.choice(meme_links))

@bot.command()
async def predict(ctx, *, question):
    answers = ["بێگومان ڕوودەدات", "مەحاڵە", "ڕەنگە لە داهاتوودا", "باشترە ئێستا نەزانیت"]
    await ctx.send(f"🔮 پرسیار: {question}\n✨ وەڵامی غەیب: **{random.choice(answers)}**")

@bot.command(name="8ball")
async def eightball(ctx, *, question):
    responses = ["بەڵێ", "نەخێر", "پێناچێت", "دڵنیام", "دووبارە بپرسەوە"]
    await ctx.send(f"🎱 {random.choice(responses)}")

# ==============================================================================
# بەشی چوارەم: فەرمانە پێشکەوتووەکان (Utility & Advanced) - ١٢ کۆماند
# ==============================================================================

@bot.command()
async def embed(ctx, title, *, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.gold())
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="📊 ڕاپرسی لۆکاڵی", description=question, color=discord.Color.blue())
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

@bot.command()
async def channelinfo(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    embed = discord.Embed(title=f"زانیاری کەناڵ: #{channel.name}", color=discord.Color.orange())
    embed.add_field(name="ئایدی کەناڵ:", value=channel.id)
    embed.add_field(name="جۆری کەناڵ:", value=str(channel.type))
    embed.add_field(name="بەرواری دروستکردن:", value=channel.created_at.strftime("%Y-%m-%d"))
    await ctx.send(embed=embed)

@bot.command()
async def servericon(ctx):
    if ctx.guild.icon: await ctx.send(ctx.guild.icon.url)
    else: await ctx.send("ئەم سێرڤەرە وێنەی نییە.")

@bot.command()
async def channelcount(ctx):
    await ctx.send(f"📁 کۆی گشتی کەناڵەکانی سێرڤەر: **{len(ctx.guild.channels)}** کەناڵ.")

@bot.command()
async def roleinfo(ctx, role: discord.Role):
    embed = discord.Embed(title=f"زانیاری ڕانک: {role.name}", color=role.color)
    embed.add_field(name="ئایدی ڕانک:", value=role.id)
    embed.add_field(name="رەنگی ڕانک (HEX):", value=str(role.color))
    embed.add_field(name="ژمارەی ئەندامانی خاوەن ڕانک:", value=len(role.members))
    await ctx.send(embed=embed)

@bot.command()
async def boosts(ctx):
    await ctx.send(f"💎 ژمارەی بوستەکانی سێرڤەر: **{ctx.guild.premium_subscription_count}** بوست.")

@bot.command()
async def creationdate(ctx):
    await ctx.send(f"📅 سێرڤەر دروستکراوە لە ڕێکەوتی: **{ctx.guild.created_at.strftime('%Y-%m-%d')}**")

# ڕێگریکردن لە ئێرۆری نەبوونی دەسەڵاتەکان
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ تۆ دەسەڵاتی پێویستت نییە بۆ بەکارهێنانی ئەم فەرمانە!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ کەمپوڕی هەیە لە نووسینی فەرمانەکەدا، تکایە دڵنیابەرەوە لە ڕاستی فەرمانەکە.")

# کارپێکردنی بۆتەکە بە شێوازی پارێزراو بۆ هۆست
# هۆستەکە خۆی تۆکنەکە لە DISCORD_TOKEN دەخوێنێتەوە
token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("⚠️ ئاگاداری: تۆکنی بۆتەکە لە ژینگەی هۆستەکە (Environment Variables) پێناسە نەکراوە!")
