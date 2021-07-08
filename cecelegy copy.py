import os, discord, time, datetime, random, asyncio, math

from discord.ext import commands, tasks
from cece_token import *
from discord.utils import get

testing_mode = False
client = commands.Bot(command_prefix="?", case_insensitive = True)
client.remove_command("help")

guild_ids = [810938331520434227, 820606404506681345]

def tobool(boolean):
    if boolean == "True":
        return True
    elif boolean == "False":
        return False

theme_color = 0xffd200

settings = open(os.getcwd()+"/cecelegy/settings.txt", "r", encoding="utf-8")
settingsR = settings.read().split("+++")
settings.close()
newday = datetime.datetime.strptime(settingsR[0], '%Y-%m-%d %H:%M:%S')




data = open(os.getcwd()+"/cecelegy/data.txt", "r", encoding="utf-8")
dataR = data.read().split("\n")
pfpcycle = tobool(dataR[0])
watch = tobool(dataR[1])
theme_color = int(dataR[2])
print(f"Pfpcycle = {pfpcycle}\nWatch = {watch}")
data.close()



remindF = open(os.getcwd()+"/cecelegy/reminder.txt", "r", encoding="utf-8")
remindR = remindF.read().split("\n")
remindF.close()
remindR_dupe = remindR[:]

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
    embed = discord.Embed(title="Help", description = "The bot replies to you!", color=ctx.author.color)
    
    embed.add_field(name = "**Syntax**", value="?hello")
    
    await ctx.send(embed = embed)

@help.command()
async def crash(ctx):
    embed = discord.Embed(title="Help", description = "Crashes the bot, only usable by <@!810910872792596550>", color=ctx.author.color)
    
    embed.add_field(name = "**Syntax**", value="?crash")
    
    await ctx.send(embed = embed)

@help.command()
async def napivers(ctx):
    embed = discord.Embed(title="Help", description = "Every day a new poem written by you is chosen, use this to see this poem!", color=ctx.author.color)
    
    embed.add_field(name = "**Syntax**", value="?napvers")
    
    await ctx.send(embed = embed)

@help.command(aliases = ["random"])
async def _random(ctx):
    embed = discord.Embed(title="Help", description = "Sends a random number between (including) the two numbers you send!", color=ctx.author.color)
    
    embed.add_field(name = "**Syntax**", value="?random <first_number> <second_number>")
    
    await ctx.send(embed = embed)

@help.command()
async def coinflip(ctx):
    embed = discord.Embed(title="Help", description = "Flip a coin!", color=ctx.author.color)
    
    embed.add_field(name = "**Syntax**", value="?coinflip")
    
    await ctx.send(embed = embed)

@help.command()
async def remind(ctx):
    embed = discord.Embed(title="Help", description = "Set a reminder to yourself or someone else!", color=ctx.author.color)
    
    embed.add_field(name = "**Syntax**", value="?remind <person> <?d-?h-?m-?s> <message>")

    embed.add_field(name = "**Note**", value="You don't need to type 0d-0h ect. everytime, for example if you want to set it for 1 hour 10 minutes, type: 1h-10m")
    
    await ctx.send(embed = embed)

@help.command()
async def gun(ctx):
    embed = discord.Embed(title="Help", description = "Assert dominance!", color=ctx.author.color)
    
    embed.add_field(name = "**Syntax**", value="?gun <person>")
    
    await ctx.send(embed = embed)

#endregion


#region commands

@client.command()
async def hello(ctx):
    await ctx.send("SZIA TE GECHI")

@client.command(aliases=["szpík"])
async def speak(ctx):
    await ctx.send("Menő a super dark profilképem, ty <@!810959448935366706>!")

@client.command()
async def crash(ctx):
    if ctx.author.id == 810910872792596550:
        await ctx.send("Megyek aludni <:killme:822415900606332950>")
        exit()
    else:
        await ctx.send(f"<@{ctx.author.id}>, nem használhatod ezt lmao")

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
        await ctx.send("Számokat írj be :)")

@client.command(aliases=["flip", "coin"])
async def coinflip(ctx):
    number = random.randint(1, 2)
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
    elif args[0] == "<@!820613259869814814>":
        await ctx.send(f"Bruh you can't gun me {ctx.author.mention}, I'm too powerful!")
    elif not args[0].startswith("<@"):
        await ctx.send(f"Bruh you need to tag someone {ctx.author.mention}!")
    else:
        await ctx.send(f"<:gun:824614321141186580> HANDS UP {args[0]}, A GUN HAS BEEN POINTED TOWARDS YOU BY {ctx.author.mention}, OBEY THEM NOW!")
        await ctx.message.delete()

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
    if ctx.author.id == 810910872792596550:
        if pfpcycle:
            pfpcycle = False
        else:
            pfpcycle = True
        
        os.remove(os.getcwd()+"/cecelegy/data.txt")
        data = open(os.getcwd()+"/cecelegy/data.txt", "a+")
        data.write(f"{pfpcycle}\n{watch}")
        data.close()
        await ctx.send(f"Changed pfp cycle to {pfpcycle}.")
    
    else:
        await ctx.send(f"{ctx.author.mention}, nem használhatod ezt lmao")

@client.command()
async def settheme(ctx, *args):
    global theme_color
    ids = [810910872792596550, 351427025078190101, 688681949887332437, 810959448935366706, 731865566230609943]
    if ctx.author.id in ids:
        karantenyek = client.get_guild(810938331520434227)
        cece_role = get(karantenyek.roles, id=836214251432837130)
        if len(args) > 1:
            avatar = False
        else:
            avatar = True

        colors = ["gold", "tür", "rw", "dc", "og"]
        if args[0] not in colors:
            await ctx.send(f"""No such color as "{args[0]}"!""")
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

            theme_color = 0xfffefe

        elif args[0] == "gold":
            if avatar:
                pfp = open(os.getcwd()+"/pfps/golden_cecelegy.png", "rb")
                try:
                    await client.user.edit(avatar = pfp.read())
                    avatar_changed = True
                except:
                    pass
                pfp.close()
            theme_color = 0xffd200
            
        elif args[0] == "tür":
            if avatar:
                pfp = open(os.getcwd()+"/pfps/türkiz_cecelegy.png", "rb")
                try:
                    await client.user.edit(avatar = pfp.read())
                    avatar_changed = True
                except:
                    pass
                pfp.close()

            theme_color = 0x29cfa0
            
        elif args[0] == "rw":
            if avatar:
                pfp = open(os.getcwd()+"/pfps/redwhite_cecelegy.png", "rb")
                try:
                    await client.user.edit(avatar = pfp.read())
                    avatar_changed = True
                except:
                    pass
                pfp.close()
            
            theme_color = 0xff0000
        
        elif args[0] == "dc":
            if avatar:
                pfp = open(os.getcwd()+"/pfps/discord_cecelegy.png", "rb")
                try:
                    await client.user.edit(avatar = pfp.read())
                    avatar_changed = True
                except:
                    pass
                pfp.close()

            theme_color = 0x769aff
        
        await cece_role.edit(colour=theme_color)
        os.remove(os.getcwd()+"/cecelegy/data.txt")
        data = open(os.getcwd()+"/cecelegy/data.txt", "a+", encoding="utf-8")
        data.write(f"{pfpcycle}\n{watch}\n{theme_color}")
        data.close()
        if avatar_changed:
            await ctx.send(f"Avatar and theme sucessfully changed to {args[0]}")
        else:
            await ctx.send(f"Only theme changed to {args[0]}")
    else:
        await ctx.send(f"{ctx.author.mention}, nem használhatod ezt lmao")

@client.command()
async def suggest(ctx, *args):
    suggestions = open(os.getcwd()+"/cecelegy/suggestions.txt", "a+", encoding="utf-8")
    suggestions.write(f"""\n[{" ".join(args)}], suggested by: {ctx.author}""")
    suggestions.close()
    await ctx.send(f"""Suggested [{" ".join(args)}] to <@!810910872792596550>""")

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
            

            print(remind_date, nowT)
            embed.add_field(name = f"In #{reminderC}", value=f"""Reminding {person} in {remind_date-nowT} about: "{reminder_message}" (set up by <@!{setup_person_id}>)""", inline = False)
    except IndexError:
        embed.add_field(name = "None", value="There are no active reminders currently.")

            

    await ctx.send(embed = embed)

@client.command()
async def refresh(ctx):
    if ctx.author.id == 810910872792596550:
        global remindR, remindR_dupe
        remindF = open(os.getcwd()+"/cecelegy/reminder.txt", "r", encoding="utf-8")
        remindR = remindF.read().split("\n")
        remindF.close()
        remindR_dupe = remindR[:]
        
        await ctx.send("Refresheltem a remindereket!")
    else:
        await ctx.send(f"{ctx.author.mention}, nem használhatod ezt lmao")

@client.command()
async def test(ctx):
    embed=discord.Embed(title="Help", description="Use the commands below with [?] prefix!", color=theme_color)
    embed.add_field(name="hello", value="""Cecelégy answers with "SZIA TE GECHI" """, inline=False)
    embed.add_field(name="crash", value="Only <@!810910872792596550> can use this, it crashes <@!820613259869814814>", inline=False)
    embed.add_field(name="random <num> <num2>", value="Generates a number between the two numbers", inline=False)
    embed.add_field(name="coinflip", value="Flips a freaking coin", inline=False)
    embed.add_field(name="gun <@somebody>", value="It SHOOTS the mentioned blithering idiot", inline=True)
    embed.add_field(name="shield", value="Oh god, I'm saved", inline=True)
    embed.add_field(name="napivers", value="Shows a new poem every day, made by us :)", inline=False)
    embed.add_field(name="remind <@somebody> <***X***d-***X***h-***X***m-***X***s> <message>", value="Reminds the mentioned blithering idiot", inline=True)
    embed.add_field(name="timeleft", value="Shows you the active reminders", inline=True)
    embed.add_field(name="suggest <something>", value="Suggest something for <@!810910872792596550> to implement into me :)", inline=False)


    embed.add_field(name="Autoreplies", value="ping, pong, f, L LOL, XD, gechi, ű, egyetértek", inline=False)

    await ctx.send(embed=embed)

@client.command(aliases=["watch"])
async def _watch(ctx):
    global watch
    if ctx.author.id == 810910872792596550:
        if watch:
            watch = False
        else:
            watch = True
        
        os.remove(os.getcwd()+"/cecelegy/data.txt")
        data = open(os.getcwd()+"/cecelegy/data.txt", "a+")
        data.write(f"{pfpcycle}\n{watch}")
        data.close()
        print(f"Watch changed to {watch}")
        await ctx.send(f"Changed watch to {watch}.")
    



#endregion





#region game commands




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
    if message.author == client.user:
        return None

    if watch:
        print(f"""{message.author} in {message.guild} #{message.channel} sent "{message.content}" """)



    
    if message.content.startswith("ping"):
        await message.channel.send(f"pong ({round(client.latency*1000)}ms)")
        print("-----------------------\nreplied to ping\n-----------------------")

    if message.content.startswith("pong"):
        await message.channel.send(f"ping?? ({round(client.latency*1000)}ms)")
        print("-----------------------\nreplied to pong\n-----------------------")

    if message.content == "f" or message.content == "F":
        await message.channel.send(message.content)
        print("-----------------------\nreplied to f\n-----------------------")
    
    if message.content == "l" or message.content == "L":
        await message.channel.send(message.content)
        print("-----------------------\nreplied to L\n-----------------------")

    if message.content == "lol" or message.content == "LOL" or message.content == "lOl" or message.content == "LoL":
        await message.channel.send(message.content)
        print("-----------------------\nreplied to lol\n-----------------------")

    if message.content == "xd" or message.content == "XD" or message.content == "Xd" or message.content == "xD":
        await message.channel.send(message.content)
        print("-----------------------\nreplied to lol\n-----------------------")         

    if "<@!820613259869814814>" in message.content or "<@820613259869814814>" in message.content:
        if not message.content.startswith("?gun"):
            await message.channel.send(f"Szólítottál, <@!{message.author.id}>?")
            print("-----------------------\nreplied to mention\n-----------------------")

    if message.content == "ty" or " ty" in message.content or "ty " in message.content:
        await message.channel.send("<3")
        print("-----------------------\nreplied to ty\n-----------------------")
    if message.content == "Vince egy isten!":
        await message.channel.send("Szerintem is! Nagyon kedves <@!810910872792596550>, hogy leprogramozott engem :)")
    if message.content.startswith("?ki vagy") or message.content.startswith("?kivagy"):
        if message.author.id == 688681949887332437:
            await message.channel.send("Egy vérszívó gechi aki néha válaszol.")
        else:
            await message.channel.send("Egy vérszívó légy aki néha válaszol.")

    szavak = ["geci", "gechi", "fasz", "faszom"]
    if message.content in szavak:
        await message.reply("Egyetértek.")

    if message.content == "ű" or message.content == "Ű":
        await message.channel.send(message.content)

    szavak = ["egyetértek", "Egyetértek"]
    for i in szavak:
        if i in message.content:
            await message.reply("Én is.")
            break

    if message.content == "de":
        await message.reply("nem")
    elif message.content == "nem":
        await message.reply("de")

    await client.process_commands(message)
    



client.run(cecelegy)