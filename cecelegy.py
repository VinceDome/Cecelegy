#region initialization
import os, discord, time, datetime, random, asyncio, math, sys, win32api, win32con, keyboard, pyautogui

from discord.ext import commands, tasks
from discord.ui import Button, View
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl

#importing the token
path_to_tokenL = os.getcwd().split("\\")
if len(path_to_tokenL) == 1:
    path_to_tokenL = os.getcwd().split("/")
del path_to_tokenL[len(path_to_tokenL)-1]

sys.path.append("/".join(path_to_tokenL))
from cece_token import *

testing_mode = False
client = commands.Bot(command_prefix="?", case_insensitive = True)
client.remove_command("help")

dev_id = 810910872792596550
guild_ids = [810938331520434227, 820606404506681345]

def tobool(boolean):
    if boolean == "True":
        return True
    elif boolean == "False":
        return False

_retek = "𝕽𝖊𝖙𝖊𝖐"

settings = open(os.getcwd()+"/cecelegy/settings.txt", "r", encoding="utf-8")
settingsR = settings.read().split("+++")
settings.close()
newday = datetime.datetime.strptime(settingsR[0], '%Y-%m-%d %H:%M:%S')




data = open(os.getcwd()+"/cecelegy/data.txt", "r", encoding="utf-8")
dataR = data.read().split("\n")
pfpcycle = tobool(dataR[0])
watch = tobool(dataR[1])
theme_color = int(dataR[2])
print(theme_color)
print(f"Pfpcycle = {pfpcycle}\nWatch = {watch}")
data.close()

#defbannedwordsL
banned_wordsF = open(os.getcwd()+"/cecelegy/banned_words.txt", "r", encoding="utf-8")
banned_wordsL = banned_wordsF.read().split("\n")
if banned_wordsL == [""]:
    banned_wordsL = []
banned_wordsF.close()


remindF = open(os.getcwd()+"/cecelegy/reminder.txt", "r", encoding="utf-8")
remindR = remindF.read().split("\n")
remindF.close()
remindR_dupe = remindR[:]


#endregion


@client.event
async def on_ready():
    print(f'{client.user} activated!')
    if not testing_mode:
        activity = discord.Game(name="Egy vérszívó légy aki néha válaszol", type=3)
        await client.change_presence(status=discord.Status.online, activity=activity)
    else:
        activity = discord.Game(name="Testing mode, use with caution!", type=3)
        await client.change_presence(status=discord.Status.dnd, activity=activity)
    
    general = client.get_channel(810938331520434230)
    remind_timer.start()
    #await general.send("Felkeltem! :)")




#region help

@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="Help", description = "Use ?help <command> to get more information on a command! ", color=theme_color)
    
    embed.add_field(name = "With prefix", value="hello, crash, napivers, random, coinflip, remind, gun")
    embed.add_field(name = "Autoreply", value="ping, pong, f, LOL, L, XD, gechi", inline=False)
    await ctx.send(embed = embed)

@help.command()
async def hello(ctx):
    embed = discord.Embed(title="Help", description = "The bot replies to you!", color=theme_color)
    
    embed.add_field(name = "**Syntax**", value="?hello")
    
    await ctx.send(embed = embed)

@help.command()
async def crash(ctx):
    embed = discord.Embed(title="Help", description = f"Crashes the bot, only usable by <@!{dev_id}>", color=theme_color)
    
    embed.add_field(name = "**Syntax**", value="?crash")
    
    await ctx.send(embed = embed)

@help.command()
async def napivers(ctx):
    embed = discord.Embed(title="Help", description = "Every day a new poem written by you is chosen, use this to see this poem!", color=theme_color)
    
    embed.add_field(name = "**Syntax**", value="?napvers")
    
    await ctx.send(embed = embed)

@help.command(aliases = ["random"])
async def _random(ctx):
    embed = discord.Embed(title="Help", description = "Sends a random number between (including) the two numbers you send!", color=theme_color)
    
    embed.add_field(name = "**Syntax**", value="?random <first_number> <second_number>")
    
    await ctx.send(embed = embed)

@help.command()
async def coinflip(ctx):
    embed = discord.Embed(title="Help", description = "Flip a coin!", color=theme_color)
    
    embed.add_field(name = "**Syntax**", value="?coinflip")
    
    await ctx.send(embed = embed)

@help.command()
async def remind(ctx):
    embed = discord.Embed(title="Help", description = "Set a reminder to yourself or someone else!", color=theme_color)
    
    embed.add_field(name = "**Syntax**", value="?remind <person> <?d-?h-?m-?s> <message>")

    embed.add_field(name = "**Note**", value="You don't need to type 0d-0h ect. everytime, for example if you want to set it for 1 hour 10 minutes, type: 1h-10m")
    
    await ctx.send(embed = embed)

@help.command()
async def gun(ctx):
    embed = discord.Embed(title="Help", description = "Assert dominance!", color=theme_color)
    
    embed.add_field(name = "**Syntax**", value="?gun <person>")
    
    await ctx.send(embed = embed)

#endregion


#region commands

@client.command()
async def hello(ctx):
    await ctx.send("SZIA TE GECHI")

@client.command(aliases=["szpík", "s"])
async def speak(ctx, *, args):
    if ctx.author.id == dev_id:
        await ctx.message.delete()
        await ctx.send(args)
    else:
        await ctx.send("Nem használhatod ikszDÉÉÉÉ")

@client.command()
async def crash(ctx):
    if ctx.author.id == dev_id:
        await ctx.send("Megyek aludni <:killme:822415900606332950>")
        exit()
    else:
        await ctx.send(f"<@{ctx.author.id}>, nem használhatod ezt lmao")

#region napivers
"""
@client.command()
async def napivers(ctx):
    global newday
    if datetime.datetime.now() > newday:
        versek = open(os.getcwd()+"/cecelegy/versek copy.txt", 'r', encoding='utf-8')
        verslista = versek.read().split("%%%")
        versek.close()

        
        random_number = random.randint(0, len(verslista)-1)
        chosen_poem = verslista[random_number]
        del verslista[random_number]
        
        date = datetime.datetime.strftime(datetime.datetime.now(), "%d %m %Y")

        day_of_week = datetime.datetime.strptime(date, "%d %m %Y").weekday()

        if day_of_week == 4:
            newday += datetime.timedelta(days=3)
        else:
            newday += datetime.timedelta(days=1)
        os.remove(os.getcwd()+"/cecelegy/settings.txt")
        

        settings = open(os.getcwd()+"/cecelegy/settings.txt", "a+", encoding="utf-8")
        settings.write(str(newday)+"+++"+chosen_poem)
        settings.close()

        os.remove(os.getcwd()+"/cecelegy/versek copy.txt")
        versek = open(os.getcwd()+"/cecelegy/versek copy.txt", "a+", encoding="utf-8")
        for i in verslista:
            versek.write(i)
            if i != verslista[len(verslista)-1]:
                versek.write("\n%%%")
        versek.close()
        try:
            embed=discord.Embed(title="Napivers", description="Minden hétköznap egy új vers", color=theme_color)
            embed.add_field(name="A mai vers:", value=chosen_poem, inline=False)
            await ctx.send(embed=embed)
        except discord.errors.HTTPException:
            await ctx.send("Nincs mit küldeni :(")

    else:
        settings = open(os.getcwd()+"/cecelegy/settings.txt", "r", encoding='utf-8')
        settingsR = settings.read().split("+++")
        settings.close()
        try:
            embed=discord.Embed(title="Napivers", description="Minden hétköznap egy új vers", color=theme_color)
            embed.add_field(name="A mai vers:", value=settingsR[1], inline=False)
            await ctx.send(embed=embed)
        except discord.errors.HTTPException:
            await ctx.send("Nincs mit küldeni :(")
"""
#endregion

@client.command(aliases=["rand", "random_number", "random"])
async def _random(ctx, *numbers):
    try:
        if len(numbers) == 0:
            await ctx.send("Írj be számokat lol")
            return None
        first = int(numbers[0])
        second = int(numbers[1])
        if first > second:
            switch = first
            first = second
            second = switch
        number = random.randint(first, second)
        await ctx.send(number)
    except ValueError:
        await ctx.send("Számokat írj be (:")

@client.command(aliases=["flip", "coin"])
async def coinflip(ctx):
    coin = random.choice(["heads", "tails"])
    await ctx.send(coin)

@client.command(aliases=["diceroll", "dice", "rolldice"])
async def roll(ctx):
    number = random.randint(1, 6)
    await ctx.send(number)

@client.command(aliases=["reminder"])
async def remind(ctx, *args):
    global remindR, remindR_dupe

    

    if len(args) < 3:
        await ctx.send("Minden paramétert írj be lmao")
        return None

    if args[0] == "me":
        person = ctx.author.mention
    else:
        person = args[0]
    wait_time = args[1]
    reminder_messageL = []

    for i in args:
        if i != args[0] and i != args[1]:
            reminder_messageL.append(i)

    reminder_message = " ".join(reminder_messageL)



    wait_timeLIST = wait_time.split("-")
    final_list = []
    final_seconds = 0
    for i in wait_timeLIST:
        time_added = ""
        for a in i:
            if a != i[len(i)-1]:
                time_added = str(time_added) + str(a)
        try:
            time_added = int(time_added)
        except ValueError:
            await ctx.send("Jól írd be azt, hogy mennyit várjak! (?help remind)")
        if i[len(i)-1] == "d":
            time_added *= 24 * 60 * 60
        elif i[len(i)-1] == "h":
            time_added *= 60 * 60
        elif i[len(i)-1] == "m":
            time_added *= 60


        final_list.append(time_added)


    for i in final_list:
        final_seconds += i


    second_counter = 0
    minute_counter = 0
    hour_counter = 0
    day_counter = 0
    final_time = ""


    second_counter = final_seconds%60
    minute_counter = math.floor(final_seconds/60)
    if minute_counter >= 60:
        minute_counter = minute_counter%60
        hour_counter = math.floor(final_seconds/60/60)
    if hour_counter >= 24:
        hour_counter = hour_counter%24
        day_counter = math.floor(final_seconds/60/60/24)

    if day_counter != 0:
        final_time += f" {day_counter} day(s)"
    if hour_counter != 0:
        final_time += f", {hour_counter} hour(s)"
    if minute_counter != 0:
        final_time += f", {minute_counter} minute(s)"
    if second_counter != 0:
        final_time += f", {second_counter} second(s)"


    if ctx.author.mention == person:
        await ctx.send(f"{ctx.author.mention}, I will remind you in{final_time}: {reminder_message}")
    else:
        await ctx.send(f"{ctx.author.mention}, I will remind {person} in{final_time}: {reminder_message}")

    




    if final_seconds <= 60:
        await asyncio.sleep(final_seconds)
    
        if ctx.author.mention == person:
            await ctx.send(f"""{person}, here's a reminder for you: "{reminder_message}" """)
        else:
            await ctx.send(f"""{person}, here's a reminder for you: "{reminder_message}" (set up by {ctx.author.mention})""")
    else:
        remindF = open(os.getcwd()+"/cecelegy/reminder.txt", "r", encoding="utf-8")
        remindFR = remindF.read()
        remindF.close()

        if remindFR != "" and remindFR != " ":
            remindF = open(os.getcwd()+"/cecelegy/reminder.txt", "a+", encoding="utf-8")
            remindF.write("\n")
            remindF.close()

        remindF = open(os.getcwd()+"/cecelegy/reminder.txt", "a+", encoding="utf-8")
        remind_date = datetime.datetime.now() + datetime.timedelta(seconds = final_seconds)
        remindF.write(f"{person}%%%{remind_date}%%%{ctx.author.id}%%%{ctx.channel.id}%%%{reminder_message}")
        remindF.close()

        remindF = open(os.getcwd()+"/cecelegy/reminder.txt", "r", encoding="utf-8")
        remindR = remindF.read().split("\n")
        remindF.close()
        remindR_dupe = remindR[:]      

@client.command(aliases=["atacc"])
async def gun(ctx, *args):
    if len(args) == 0:
        await ctx.send(f"Bruh you need to tag someone {ctx.author.mention}!")
    elif ctx.author.mention == args[0]:
        await ctx.send(f"Bruh you can't gun yourself {ctx.author.mention}!")
    elif args[0] == "<@!820613259869814814>" or args[0] == "<@820613259869814814>":
        await ctx.send(f"Bruh you can't gun me {ctx.author.mention}, I'm too powerful!")
    elif not args[0].startswith("<@"):
        await ctx.send(f"Bruh you need to tag someone {ctx.author.mention}!")
    else:
        await ctx.message.delete()
        await ctx.send(f"<:gun:824614321141186580> HANDS UP {args[0]}, {ctx.author.mention} POINTED THEIR GUN AT YOU, OBEY THEM NOW!")

@client.command()
async def ping(ctx):
    await ctx.send(f"pong ({round(client.latency*1000)}ms)")
    print("-----------------------\nreplied to ?ping\n-----------------------")

@client.command(aliases=["defend", "def", "protecc"])
async def shield(ctx):
    await ctx.send(f"🖐🖐 {ctx.author.mention} has put up their hands, let's try to negotiate!")
    await ctx.message.delete()

@client.command()
async def cycle(ctx):
    global pfpcycle
    if ctx.author.id == dev_id:
        if pfpcycle:
            pfpcycle = False
        else:
            pfpcycle = True
        
        os.remove(os.getcwd()+"/cecelegy/data.txt")
        data = open(os.getcwd()+"/cecelegy/data.txt", "a+")
        data.write(f"{pfpcycle}\n{watch}\n{theme_color}")
        data.close()
        await ctx.send(f"Changed pfp cycle to {pfpcycle}.")
    
    else:
        await ctx.send(f"{ctx.author.mention}, nem használhatod ezt lmao")

@client.command(aliases=["theme"])
async def settheme(ctx, *args):
    global theme_color
    ids = [dev_id, 351427025078190101, 688681949887332437, 810959448935366706, 731865566230609943]
    if ctx.author.id in ids:
        karantenyek = client.get_guild(810938331520434227)
        cece_role = get(karantenyek.roles, id=836214251432837130)
        if len(args) > 1:
            avatar = False
        else:
            avatar = True

        colors = ["gold", "tür", "rw", "dc", "og"]
        if args[0] not in colors:
            if args[0] == "?":
                await ctx.send(f"Available themes: {colors}")
            else:
                await ctx.send(f"No such color as [{args[0]}]!")
            return None

        avatar_changed = False
        if args[0] == "og":
            if avatar:
                pfp = open(os.getcwd()+"/pfps/og_cecelegy.png", "rb")
                try:
                    await client.user.edit(avatar = pfp.read())
                    avatar_changed = True
                except:
                    pass
                pfp.close()

            theme_color = 16776958

        elif args[0] == "gold":
            if avatar:
                pfp = open(os.getcwd()+"/pfps/golden_cecelegy.png", "rb")
                try:
                    await client.user.edit(avatar = pfp.read())
                    avatar_changed = True
                except:
                    pass
                pfp.close()
            theme_color = 16765440
            
        elif args[0] == "tür":
            if avatar:
                pfp = open(os.getcwd()+"/pfps/türkiz_cecelegy.png", "rb")
                try:
                    await client.user.edit(avatar = pfp.read())
                    avatar_changed = True
                except:
                    pass
                pfp.close()

            theme_color = 2740128
            
        elif args[0] == "rw":
            if avatar:
                pfp = open(os.getcwd()+"/pfps/redwhite_cecelegy.png", "rb")
                try:
                    await client.user.edit(avatar = pfp.read())
                    avatar_changed = True
                except:
                    pass
                pfp.close()
            
            theme_color = 16711680
        
        elif args[0] == "dc":
            if avatar:
                pfp = open(os.getcwd()+"/pfps/blurple_cecelegy.png", "rb")
                try:
                    await client.user.edit(avatar = pfp.read())
                    avatar_changed = True
                except:
                    pass
                pfp.close()

            theme_color = 5793266
        
        await cece_role.edit(colour=theme_color)
        os.remove(os.getcwd()+"/cecelegy/data.txt")
        data = open(os.getcwd()+"/cecelegy/data.txt", "a+", encoding="utf-8")
        data.write(f"{pfpcycle}\n{watch}\n{theme_color}")
        data.close()
        if avatar_changed:
            await ctx.send(f"avatar and theme = [{args[0]}]")
        else:
            await ctx.send(f"theme = [{args[0]}]")
    else:
        await ctx.send(f"{ctx.author.mention}, nem használhatod ezt lmao")

@client.command()
async def suggest(ctx, *args):
    suggestions = open(os.getcwd()+"/cecelegy/suggestions.txt", "a+", encoding="utf-8")
    suggestions.write(f"""\n[{" ".join(args)}], suggested by: {ctx.author}""")
    suggestions.close()
    await ctx.send(f"""Suggested [{" ".join(args)}] to <@!{dev_id}>""")

@client.command()
async def timeleft(ctx):
    embed = discord.Embed(title="Reminders currently", description = "These are the reminders that are counting down currently:", color=theme_color)
    
  
    try:
        for i in remindR:
            individual_split = i.split("%%%")

            person = individual_split[0]
            remind_date = individual_split[1]
            setup_person_id = individual_split[2]
            reminderC = client.get_channel(int(individual_split[3]))
            reminder_message = individual_split[4]

            

            nowS = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            nowT = datetime.datetime.strptime(nowS, '%Y-%m-%d %H:%M:%S')

            remind_dateT = datetime.datetime.strptime(remind_date, '%Y-%m-%d %H:%M:%S.%f')
            remind_dateS = datetime.datetime.strftime(remind_dateT, '%Y-%m-%d %H:%M:%S')
            remind_date = datetime.datetime.strptime(remind_dateS, '%Y-%m-%d %H:%M:%S')
            

            
            embed.add_field(name = f"In #{reminderC}", value=f"""Reminding {person} in {remind_date-nowT} about: "{reminder_message}" (set up by <@!{setup_person_id}>)""", inline = False)
    except IndexError:
        embed.add_field(name = "None", value="There are no active reminders currently.")

            

    await ctx.send(embed = embed)

@client.command()
async def refresh(ctx):
    if ctx.author.id == dev_id:
        global remindR, remindR_dupe, banned_wordsL
        remindF = open(os.getcwd()+"/cecelegy/reminder.txt", "r", encoding="utf-8")
        remindR = remindF.read().split("\n")
        remindF.close()
        remindR_dupe = remindR[:]

        
        banned_wordsF = open(os.getcwd()+"/cecelegy/banned_words.txt", "r", encoding="utf-8")
        banned_wordsL = banned_wordsF.read().split("\n")
        if banned_wordsL == [""]:
            banned_wordsL = []
        banned_wordsF.close()
        print(banned_wordsL)


        await ctx.send("Refreshed stuff!")
    else:
        await ctx.send(f"{ctx.author.mention}, nem használhatod ezt lmao")

@client.command()
async def test(ctx):
    embed=discord.Embed(title="Help", description="Use the commands below with [?] prefix!", color=theme_color)
    embed.add_field(name="hello", value="""Cecelégy answers with "SZIA TE GECHI" """, inline=False)
    embed.add_field(name="crash", value=f"Only <@!{dev_id}> can use this, it crashes <@!820613259869814814>", inline=False)
    embed.add_field(name="random <num> <num2>", value="Generates a number between the two numbers", inline=False)
    embed.add_field(name="coinflip", value="Flips a freaking coin", inline=False)
    embed.add_field(name="gun <@somebody>", value="It SHOOTS the mentioned blithering idiot", inline=True)
    embed.add_field(name="shield", value="Oh god, I'm saved", inline=True)
    embed.add_field(name="napivers", value="Shows a new poem every day, made by us :)", inline=False)
    embed.add_field(name="remind <@somebody> <***X***d-***X***h-***X***m-***X***s> <message>", value="Reminds the mentioned blithering idiot", inline=True)
    embed.add_field(name="timeleft", value="Shows you the active reminders", inline=True)
    embed.add_field(name="suggest <something>", value=f"Suggest something for <@!{dev_id}> to implement into me :)", inline=False)


    embed.add_field(name="Autoreplies", value="ping, pong, f, L LOL, XD, gechi, ű, egyetértek", inline=False)

    await ctx.send(embed=embed)

@client.command(aliases=["watch"])
async def _watch(ctx):
    global watch
    if ctx.author.id == dev_id:
        if watch:
            watch = False
        else:
            watch = True
        
        os.remove(os.getcwd()+"/cecelegy/data.txt")
        data = open(os.getcwd()+"/cecelegy/data.txt", "a+")
        data.write(f"{pfpcycle}\n{watch}")
        data.close()
        print(f"--------------------\nChanged watch to {watch}\n--------------------")
        await ctx.send(f"watch = [{watch}]")

@client.command(aliases=["hájd"])
async def hide(ctx):  
    await ctx.send(" ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n ឵឵\n")

@client.command(aliases=["del"])
async def _del(ctx, *_id):
    if ctx.author.id == dev_id:
        try:
            if _id[0] == []:
                return
            op = await ctx.fetch_message(ctx.message.id)
            msg = await ctx.fetch_message(int(_id[0]))
            await msg.delete()
            await op.delete()
        except:
            await ctx.send("jól add meg az id-t <:bruh:836913355359780874>")

@client.command(aliases=["giverole"])
async def _giverole(ctx, _id):
    try:
        karantenyek = client.get_guild(810938331520434227)
        member = ctx.message.author
        role = get(karantenyek.roles, id=int(_id))
        await member.add_roles(role)
        await ctx.send(f"added [{role}] role to [{member}]")
    except:
        await ctx.send("nem így kell xddd L")

@client.command(aliases=["athome"])
async def _athome(ctx):
    karantenyek = client.get_guild(810938331520434227)
    member = ctx.author
    athomeR = get(karantenyek.roles, id=885412285525422090)
    if not athomeR in ctx.author.roles:
        await member.add_roles(athomeR)
        await ctx.send("kaptál rangot uram")
    else:
        await member.remove_roles(athomeR)
        await ctx.send("elvettem a rangot uram")

@client.command(aliases=["aludjá"])
async def chill(ctx, *args):
    if len(args) == 0:
        await ctx.send(f"Bruh you need to tag someone {ctx.author.mention}!")
    elif ctx.author.mention == args[0]:
        await ctx.send(f"Bruh you can't make yourself chill {ctx.author.mention}!")
    elif args[0] == "<@!820613259869814814>" or args[0] == "<@820613259869814814>":
        await ctx.send(f"Bruh you can't make me chill {ctx.author.mention}, I'm too powerful!")
    elif not args[0].startswith("<@") and args[0] != "@everyone":
        await ctx.send(f"Bruh you need to tag someone {ctx.author.mention}!")
    else:
        await ctx.message.delete()
        await ctx.send(f"🌿 {args[0]}, chill out, don't be so stressed! Here's some weed {ctx.author.mention} gave you to chill. 🌿")

@client.command()
async def bonk(ctx, *args):
    if len(args) == 0:
        await ctx.send(f"Bruh you need to tag someone {ctx.author.mention}!")
    elif ctx.author.mention == args[0]:
        await ctx.send(f"Bruh you can't bonk yourself {ctx.author.mention}!")
    elif args[0] == "<@!820613259869814814>" or args[0] == "<@820613259869814814>":
        await ctx.send(f"Bruh you can't bonk me {ctx.author.mention}, I'm too powerful!")
    elif not args[0].startswith("<@") and args[0] != "@everyone":
        await ctx.send(f"Bruh you need to tag someone {ctx.author.mention}!")
    else:
        await ctx.message.delete()
        await ctx.send(f"<:cheems:845344496979935312> {args[0]}, you got bonked by {ctx.author.mention}! <:cheems:845344496979935312>")

@client.command()
async def shit(ctx, *args):
    if len(args) == 0:
        await ctx.send(f"Bruh you need to tag someone {ctx.author.mention}!")
    elif ctx.author.mention == args[0]:
        await ctx.send(f"Bruh you can't shit on yourself {ctx.author.mention}!")
    elif args[0] == "<@!820613259869814814>" or args[0] == "<@820613259869814814>":
        await ctx.send(f"Bruh you can't shit on me {ctx.author.mention}, I'm too powerful!")
    elif not args[0].startswith("<@") and args[0] != "@everyone":
        await ctx.send(f"Bruh you need to tag someone {ctx.author.mention}!")
    else:
        await ctx.message.delete()
        await ctx.send(f"💩 {args[0]}, you just got shit on by {ctx.author.mention}! 💩")


@client.command(aliases=["banned"])
async def banned_words(ctx):
    global banned_wordsL
    embed=discord.Embed(title="Banned words", description="These are the words that are banned", color=theme_color)
    if len(banned_wordsL) == 0:
        embed.add_field(name=f"There are {len(banned_wordsL)} banned words", value=f"""The list is empty!""", inline=False)
    else:
        embed.add_field(name=f"There are {len(banned_wordsL)} banned words", value="\n".join(banned_wordsL), inline=False)
    
    await ctx.send(embed=embed)

@client.command(aliases=["calc", "math"])
async def calculate(ctx, *args):
    global operation, result, num1, num2, oper
    if len(args) < 3:
        if args[0].lower() == "sqrt" or args[0].lower() == "gyök" or args[0].lower() == "gyok":
            root = math.sqrt(float(args[1]))
            if root - int(root) == 0.0:
                root = int(root)

            await ctx.send(root)
            return None

        await ctx.send("Minden paramétert írj be lmao")
        return None

    try:
        num1 = float(args[0])
        num2 = float(args[2])
        oper = args[1]
    except ValueError:
        await ctx.send("Számokkal számolj!")
        return None

    if oper == "x" or oper == "X":
        oper = "*"
    result = 0
    operation = "result = num1 "+oper+" num2"
    exec(operation, globals())
    if result - int(result) == 0.0:
        result = int(result)
    await ctx.send(result)

@client.command(aliases=["masodfoku", "masod"])
async def _masodfoku_egyenlet(ctx, _a, _b, _c):
    try:
        _a, _b, _c = float(_a), float(_b), float(_c)
    except ValueError:
        await ctx.send("Számokat írj bruh")
        return None

    try:
        gyokos = math.sqrt((_b**2) - (4*_a*_c))
    except ValueError:
        await ctx.send("Nincs megoldás!")
    
    try:
        x1 = ((-1*_b)+gyokos)/(2*_a)
        x2 = ((-1*_b)-gyokos)/(2*_a)
    except ZeroDivisionError:
        await ctx.send("Öhm, biztos 0 az [a]? xd")


    if x1 - int(x1) == 0.0:
        x1 = int(x1)
    else:
        x1 = round(x1, 2)
    
    if x2 - int(x2) == 0.0:
        x2 = int(x2)
    else:
        x2 = round(x2, 2)
      
    
    if x1 == x2:
        await ctx.send(f"a két ág megegyezik: [{x1}]")
    else:
        await ctx.send(f"plusz ág: [{x1}], mínusz ág: [{x2}]")

@client.command(aliases=["pitagorasz", "pita", "haromszog", "háromszög"])
async def _pitagorasz_tetel(ctx, _a, _b, _c):
    if _a == "?":
        try:
            _b, _c = float(_b), float(_c)
        except ValueError:
            await ctx.send("Egyelőre csak egész számokat fogadok el!")
            return None

        try:
            _a = math.sqrt((_c ** 2) - (_b ** 2))
            if _a - int(_a) == 0.0:
                _a = int(_a)
            
            await ctx.send(f"a = [{_a}]")
        except ValueError:
            await ctx.send("Nincs megoldás!")
    elif _b == "?":
        try:
            _a, _c = float(_a), float(_c)
        except ValueError:
            await ctx.send("Egyelőre csak egész számokat fogadok el!")
            return None

        try:
            _b = math.sqrt((_c ** 2) - (_a ** 2))
            if _b - int(_b) == 0.0:
                _b = int(_b)
            await ctx.send(f"b = [{_b}]")
        except ValueError:
            await ctx.send("Nincs megoldás!")
    
    elif _c == "?":
        try:
            _a, _b = float(_a), float(_b)
        except ValueError:
            await ctx.send("Egyelőre csak egész számokat fogadok el!")
            return None

        try:
            _c = math.sqrt((_a ** 2) + (_b ** 2))
            if _c - int(_c) == 0.0:
                _c = int(_c)
            await ctx.send(f"c = [{_c}]")
        except ValueError:
            await ctx.send("Nincs megoldás!")

@client.command(aliases=["kör", "karika", "körszámolás"])
async def _kör_számolás(ctx, _given, _n):
    if _given == "r" or _given == "s":
        try:
            _r = float(_n)
        except ValueError:
            await ctx.send("számot írj bruh")
            return None

        _k = (_r * 2) * 3.14

        _t = (_r ** 2) * 3.14


        try:
            if _k - int(_k) == 0.0:
                _k = int(_k)

            if _t - int(_t) == 0.0:
                _t = int(_t)
            await ctx.send(f"kerület = [{_k}]\nterület = [{_t}]")
        except ValueError:
            await ctx.send("Nincs megoldás!")
    elif _given == "k":
        try:
            _k = float(_n)
        except ValueError:
            await ctx.send("számot írj bruh")
            return None

        _r = (_k/2)/3.14

        _t = (_r ** 2) * 3.14


        try:
            if _r - int(_r) == 0.0:
                _r = int(_r)

            if _t - int(_t) == 0.0:
                _t = int(_t)
            await ctx.send(f"sugár = [{_r}]\nterület = [{_t}]")
        except ValueError:
            await ctx.send("Nincs megoldás!")
    
    elif _given == "t":
        try:
            _t = float(_n)
        except ValueError:
            await ctx.send("számot írj bruh")
            return None

        _r = math.sqrt(_t / 3.14)

        _k = (_r * 2) * 3.14


        try:
            if _r - int(_r) == 0.0:
                _r = int(_r)

            if _k - int(_k) == 0.0:
                _k = int(_k)
            await ctx.send(f"sugár = [{_r}]\nterület = [{_k}]")
        except ValueError:
            await ctx.send("Nincs megoldás!")



@client.command(aliases=["c"])
async def clear(ctx, msgs):
    if ctx.author.id == dev_id:
        try:
            await ctx.channel.purge(limit=int(msgs)+1)
        except ValueError:
            await ctx.send("számot adj meg lol")
    else:
        await ctx.send("nem")

@client.command(aliases=["git"])
async def github(ctx):
    await ctx.send("https://github.com/VinceDome/Cecelegy")

@client.command()
async def retek(ctx):
    await ctx.send(_retek)

@client.command()
async def dm(ctx, _id, *, message):
    if ctx.author.id != dev_id:
        return None
    if "<@" in _id:
        _idL = list(_id)
        
        _idL.remove("@")
        _idL.remove("<")
        _idL.remove(">")
        try:
            _idL.remove("!")
        except ValueError:
            pass
        _id = int("".join(_idL))
    user = await client.fetch_user(int(_id))
    msg_dm = await user.create_dm()
    await msg_dm.send(message)
    await ctx.send(f""" "{message}" sent to [{user}]""")


#endregion

#region remote control

@client.command()
async def click(ctx):
    if ctx.author.id != dev_id:
        return None
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.01)
    await ctx.send("Clicked!")

@client.command()
async def left(ctx):
    if ctx.author.id != dev_id:
        return None
    keyboard.press_and_release("left_arrow")
    
    await ctx.send("Pressed left arrow!")

@client.command()
async def rewind(ctx):
    if ctx.author.id != dev_id:
        return None
    keyboard.press_and_release("j")
    await ctx.send("Pressed j, rewinded back 10 seconds!")

@client.command()
async def remote(ctx):
    if ctx.author.id != dev_id:
        return None

    pause_resume = Button(label="Pause/Resume", style = discord.ButtonStyle.green, emoji = "▶")
    rewind = Button(label="Rewind", style = discord.ButtonStyle.blurple, emoji = "⏪")
    forward = Button(label="Forward", style = discord.ButtonStyle.blurple, emoji = "⏩")
    fullscreen = Button(label="Fullscreen", style = discord.ButtonStyle.gray, emoji = "💻")

    async def pause_resume_callback(interaction):
        keyboard.press_and_release("space")
    async def rewind_callback(interaction):
        keyboard.press_and_release("j")
    async def forward_callback(interaction):
        keyboard.press_and_release("l")
    async def fullscreen_callback(interaction):
        keyboard.press_and_release("f")


    pause_resume.callback = pause_resume_callback
    rewind.callback = rewind_callback
    forward.callback = forward_callback
    fullscreen.callback = fullscreen_callback

    view = View()
    view.add_item(rewind)
    view.add_item(pause_resume)
    view.add_item(forward)
    view.add_item(fullscreen)

    msg = await ctx.send("TV remote", view=view)

@client.command(aliases=["p", "m"])
async def press(ctx, _button):
    if ctx.author.id != dev_id:
        return None


    try:
        
        if list(ctx.message.content)[1] == "m":
            if win32api.GetKeyState(win32con.VK_CAPITAL) == 0:
                keyboard.press_and_release("capslock")
                macro = True

        keyboard.press(_button)
        time.sleep(0.1)
        keyboard.release(_button)

        if _button == "capslock":
            if win32api.GetKeyState(win32con.VK_CAPITAL) == 1:
                await ctx.send(f"Pressed caps lock, it's now on!")
            else:
                await ctx.send(f"Pressed caps lock, it's now off!")
        else:
            if macro:
                await ctx.send(f"Macro {_button} activated!")
            else:
                await ctx.send(f"Pressed {_button}!")
        
    except:
        print("bruh")    

    
#endregion

#region voice commands
@client.command(pass_context=True)
async def join(ctx, _id=None):
    if _id == None:
        if not ctx.author.voice:
            await ctx.send("nem")
            return None

        vChannel = ctx.author.voice.channel
        
    else:
        try:
            _id = int(_id)
        except ValueError:
            await ctx.send("számot kérek bruh")
            return None
        vChannel = client.get_channel(int(_id))
    
    await vChannel.connect()
    await ctx.send(f"""Joined "{vChannel.name}" """)

@client.command(pass_context=True)
async def leave(ctx):
    if not ctx.voice_client:
        await ctx.send("honnan a fenéből lépjek ki")
        return None

    await ctx.voice_client.disconnect()
    await ctx.send("Left channel!")

@client.command(pass_context=True, aliases = ["play"])
async def _play(ctx, _path=None, _channel=None):
    audio = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if audio:
        audio.stop()

    edit_msg = []
    msg = None
    just_joined = False

    #if bot is not connected
    if not ctx.voice_client:

       #and the person has given a channel 
        if _channel:
                try:
                    _channel = int(_channel)
                except ValueError:
                    await ctx.send("Enter a number!")
                vChannel = client.get_channel(int(_channel))

        #if the author is not connected
        elif ctx.author.voice:
            vChannel = ctx.author.voice.channel
        #if the author is connected
        else:
            await ctx.send("nem")
            return None
            


        msg = await ctx.send("Joining voice channel...")
        edit_msg.append("Joining voice channel...")        
        await vChannel.connect()

        edit_msg.append("DONE\n")
        await msg.edit(content="".join(edit_msg))

        just_joined = True

    voice = ctx.voice_client

    if "https:" in _path:
        edit_msg.append("Setting up player...")
        if not msg:
            msg = await ctx.send("".join(edit_msg))
        else:
            await msg.edit(content="".join(edit_msg))
        


        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}

        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        try:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(_path, download=False)
                I_URL = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
                voice.play(source)
        except:
            edit_msg.append("FAILED, check your link again!")
            await msg.edit(content="".join(edit_msg))
            return None

        edit_msg.append("PLAYING")
        await msg.edit(content="".join(edit_msg))
        tmp_channel = ctx.voice_client.channel
        
        #this patches audio stopping when moving bot to channels
        while True:
            await asyncio.sleep(0.5)
            if ctx.voice_client == None:
                break
            elif ctx.voice_client.channel != tmp_channel:
                if len(ctx.voice_client.channel.members) != 1:
                    tmp_channel = ctx.voice_client.channel
                    continue
                try:
                    voice.pause()
                except:
                    break
                await asyncio.sleep(0.5)
                voice.resume()
                tmp_channel = ctx.voice_client.channel
                





        """
        ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
            }],
        }

        edit_msg.append("Downloading video...")
        if not msg:
            msg = await ctx.send("".join(edit_msg))
        else:
            await msg.edit(content="".join(edit_msg))
        

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(_path, download=False)
            I_URL = info['formats'][0]['url']
            print(info)
            print("________________________________________________________________________________________________", I_URL)
            try:
                ydl.download([_path])
            except:
                edit_msg.append("FAILED, check your link again!")
                await msg.edit(content="".join(edit_msg))
                return None

        edit_msg.append("DONE\nRenaming file...")
        await msg.edit(content="".join(edit_msg))


        for file in os.listdir("./"):
            if file.endswith(".wav"):
                if os.path.exists(os.getcwd()+"/tmp/song.wav"):
                    os.remove(os.getcwd()+"/tmp/song.wav")

                os.rename(os.getcwd()+"/"+file, os.getcwd()+f"/tmp/song.wav")
                break
        else:
            edit_msg.append("FAILED, check your link again!")
            await msg.edit(content="".join(edit_msg))
            return None
        
        edit_msg.append("DONE\nStarting playback...")
        await msg.edit(content="".join(edit_msg))

        

        source = FFmpegPCMAudio(source=os.getcwd()+f"/tmp/song.wav")
        voice.play(source)

        edit_msg.append(f"PLAYING {_path}")
        await msg.edit(content="".join(edit_msg))
        """

      

    elif os.path.exists(os.getcwd()+f"/audio_files/{_path}.wav"):
        source = FFmpegPCMAudio(source=os.getcwd()+f"/audio_files/{_path}.wav")
        voice.play(source)
        await ctx.send(f"""Playing "{_path}.wav" """)


        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        tmp_channel = ctx.voice_client.channel
        #this patches audio stopping when moving bot to channels
        while True:
            await asyncio.sleep(0.5)
            if ctx.voice_client == None:
                break
            elif ctx.voice_client.channel != tmp_channel:
                if len(ctx.voice_client.channel.members) != 1:
                    tmp_channel = ctx.voice_client.channel
                    continue
                try:
                    voice.pause()
                except:
                    break
                await asyncio.sleep(0.5)
                voice.resume()
                tmp_channel = ctx.voice_client.channel

    else:   
        edit_msg.append("FAILED, I need a valid filename!")
        await msg.edit(content="".join(edit_msg))
        if just_joined:
            await ctx.voice_client.disconnect()
        return None

@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if not voice:
        await ctx.send("Nothing to resume <:bruh:836913355359780874>")
        return None

    if voice.is_playing():
        voice.pause()
        await ctx.send("Paused audio!")
    else:
        await ctx.send("Nothing to pause <:bruh:836913355359780874>")

@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if not voice:
        await ctx.send("Nothing to resume <:bruh:836913355359780874>")
        return None

    if voice.is_paused():
        voice.resume()
        await ctx.send("Resumed audio!")
    else:
        await ctx.send("Nothing to resume <:bruh:836913355359780874>")

@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if not voice:
        await ctx.send("Nothing to stpp <:bruh:836913355359780874>")
        return None

    voice.stop()
    await ctx.send("Stopped audio!")

@client.command(pass_context=True, aliases = ["download", "save"])
async def _download(ctx, _url=None, _name=None):
    if not _url or not "https://" in _url or not _name:
        await ctx.send("Please give the correct parameters!")
        return None
    edit_msg = []
    msg = None

    ydl_opts = {
        "format": "bestaudio/best",
        "max_filesize": 33350000,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
            }],
        }

    edit_msg.append("Downloading video...")
    msg = await ctx.send("".join(edit_msg))
    
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([_url])
        except:
            edit_msg.append("FAILED, check your link again!")
            await msg.edit(content="".join(edit_msg))
            return None

    for file in os.listdir("./"):
            if file.endswith(".part"):
                os.remove(file)
                edit_msg.append("FAILED\nNOTE: The max video length is around 30 minutes")
                await msg.edit(content="".join(edit_msg))
                return None
             

    edit_msg.append("DONE\nRenaming file...")
    await msg.edit(content="".join(edit_msg))


    for file in os.listdir("./"):
        if file.endswith(".wav"):
            try:
                os.rename(os.getcwd()+"/"+file, os.getcwd()+f"/audio_files/{_name}.wav")
            except:
                edit_msg.append("FAILED, file already exists!")
                await msg.edit(content="".join(edit_msg))
                return None

            break
    else:
        edit_msg.append("FAILED, check your link again!")
        await msg.edit(content="".join(edit_msg))
        return None
    
    edit_msg.append(f"""DONE, saved as "{_name}.wav" """)
    await msg.edit(content="".join(edit_msg))

@client.command(pass_context=True, aliases = ["audio_files", "list"])
async def _audio_files(ctx):
    edit_msg = []
    for i in os.listdir(os.getcwd()+"/audio_files/"):
        edit_msg.append(f""""{i}"\n""")

    await ctx.send("".join(edit_msg))   
 
#endregion


@tasks.loop(minutes=1)
async def remind_timer():
    global remindR, remindR_dupe, theme_color
    
    #türkiz szín: #29cfa0           	0x29cfa0
    #arany szín: #ffd200                0xffd200
    try:
        #beolvasás

        for i in remindR:
            individual_split = i.split("%%%")

            person = individual_split[0]
            remind_date = individual_split[1]
            setup_person_id = individual_split[2]
            reminderC = client.get_channel(int(individual_split[3]))
            reminder_message = individual_split[4]

            if datetime.datetime.now() > datetime.datetime.strptime(remind_date, '%Y-%m-%d %H:%M:%S.%f'):
                if f"<@!{setup_person_id}>" == person:
                    await reminderC.send(f"""{person}, here's a reminder for you: "{reminder_message}" """)
                else:
                    await reminderC.send(f"""{person}, here's a reminder for you: "{reminder_message}" (set up by <@!{setup_person_id}>)""")
                remindR_dupe.remove(i)
        if remindR_dupe == remindR:
            return None
        else:
            os.remove(os.getcwd()+"/cecelegy/reminder.txt")
            remindW = open(os.getcwd()+"/cecelegy/reminder.txt", "a+", encoding="utf-8")
            for i in remindR_dupe:
                if i == remindR_dupe[0]:
                    remindW.write(i)
                else:
                    remindW.write(f"\n{i}")
            remindW.close()

            
            remindF = open(os.getcwd()+"/cecelegy/reminder.txt", "r", encoding="utf-8")
            remindR = remindF.read().split("\n")
            remindF.close()
            remindR_dupe = remindR[:]
    except IndexError:
        return None




@client.event
async def on_message(message):
    global operation, result, num1, num2, oper, banned_wordsL

    allowed_guilds = [826459488340672532, 810938331520434227]

    if message.guild == None:
        if message.author.id != dev_id:
            return None
    elif message.author == client.user or not message.guild.id in allowed_guilds:
        return None

    if watch:
        print(f"""{message.author} in {message.guild} #{message.channel} sent "{message.content}" """)

    for i in banned_wordsL:
        if i in message.content.lower() and message.channel.id != 810942077272588300:
            await message.delete()
            return
            

    #region autoreply
    if message.content.lower().startswith("ping"):
        szavak = ["pog", "pong", "bruh", "long", "kong", "loll", "chonk", "this cord"]
        await message.channel.send(f"{random.choice(szavak)} ({round(client.latency*1000)}ms)")
        print("-----------------------\nreplied to ping\n-----------------------")

    if message.content.lower().startswith("pong"):
        await message.channel.send(f"ping?? ({round(client.latency*1000)}ms)")
        print("-----------------------\nreplied to pong\n-----------------------")

    if message.content.lower() == "f":
        await message.channel.send(message.content)
        print("-----------------------\nreplied to f\n-----------------------")
    
    if message.content.lower() == "l":
        await message.channel.send(message.content)
        print("-----------------------\nreplied to L\n-----------------------")

    if message.content.lower() == "lol":
        await message.channel.send(message.content)
        print("-----------------------\nreplied to lol\n-----------------------")

    if message.content.lower() == "xd":
        await message.channel.send(message.content)
        print("-----------------------\nreplied to lol\n-----------------------")         

    if "<@!820613259869814814>" in message.content or "<@820613259869814814>" in message.content:
        if not message.content.startswith("?"):
            await message.channel.send(f"Szólítottál, <@!{message.author.id}>?")
            print("-----------------------\nreplied to mention\n-----------------------")

    if message.content == "ty" or " ty" in message.content or "ty " in message.content:
        await message.channel.send("<3")
        print("-----------------------\nreplied to ty\n-----------------------")
    if message.content == "Vince egy isten!":
        await message.channel.send(f"Szerintem is! Nagyon kedves <@!{dev_id}>, hogy leprogramozott engem :)")
    if message.content.startswith("?ki vagy") or message.content.startswith("?kivagy"):
        if message.author.id == 688681949887332437:
            await message.channel.send("Egy vérszívó gechi aki néha válaszol.")
        else:
            await message.channel.send("Egy vérszívó légy aki néha válaszol.")

    szavak = ["geci", "gechi", "fasz", "faszom"]
    if message.content.lower() in szavak:
        await message.reply("Egyetértek.")

    if message.content.lower() == "ű":
        await message.channel.send(message.content)

    szavak = ["egyetértek", "egyet értek", "én is"]
    for i in szavak:
        if i in message.content.lower():
            await message.reply("Én is.")
            break

    if message.content.lower() == "de" or message.content.lower() == "igen":
        await message.reply("nem")
    elif message.content.lower() == "nem":
        await message.reply("de")

    szavak = ["nempog", "Nempog"]    
    messageS = message.content.split(" ")
    for i in range(len(messageS)):
        if messageS[i] in szavak:
            await message.channel.send(messageS[i])
            return
        elif messageS[i].lower() == "pog" or messageS[i].lower() == "pogw":
            if not messageS[i-1] == messageS[i] and not messageS[i-1] == messageS[len(messageS)-1]:
                await message.channel.send(messageS[i-1] + " " + messageS[i])
            else:
                await message.channel.send(messageS[i])
            break

    
    if message.content.lower() == "bonk":
        await message.reply("GECHI")

    szavak = ["hatos", "6os", "6-os"]
    for i in szavak:
        if i in message.content.lower():
            await message.reply("Faszt, kilences!")
            break

    szavak = ["sus", "baka", "amogus", "among us", "amongus", "szász", "száász", "ඞ"]
    for i in szavak:
        if i in message.content.lower():
            await message.reply(random.choice(szavak)+"ඞ")
            break

    szavak = ["fekete", "buzi", "náci"]
    for i in szavak:
        if i in message.content.lower():
            await message.reply("ez nem pollkorrekt")
    #endregion
    
    

    
    

    if not message.content.lower().startswith("?"):
        args = message.content.split(" ")
        if len(args) < 3:
            if args[0].lower() == "sqrt" or args[0].lower() == "gyök" or args[0].lower() == "gyok":
                root = math.sqrt(float(args[1]))
                if root - int(root) == 0.0:
                    root = int(root)

                await message.channel.send(root)
                return None

            #await message.send("Minden paramétert írj be lmao")
            return None

        try:
            num1 = float(args[0])
            num2 = float(args[2])
            oper = args[1]
        except ValueError:
            #await message.send("Számokkal számolj!")
            return None

        if oper == "x" or oper == "X":
            oper = "*"
        result = 0
        operation = "result = num1 "+oper+" num2"
        exec(operation, globals())
        if result - int(result) == 0.0:
            result = int(result)
        await message.channel.send(result)    
    
    await client.process_commands(message)
    



client.run(cecelegy)