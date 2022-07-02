import csv
import random
import time
import discord
import requests as r
from discord.ext import commands
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

chromedriver_autoinstaller.install()
chromeOptions = Options()
chromeOptions.headless = True
chromeOptions.add_argument("window-size=1920,1080")

token = "Your Discord Bot Token"
apiTOKEN = "Idk what API this is"

intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command("help")


def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel


async def get_input_of_type(func, ctx):
    while True:
        try:
            msg = await client.wait_for('message', check=check(ctx))
            return func(msg.content)
        except ValueError:
            continue


@client.event
async def on_ready():
    # change_status.start()
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(name=".help", type=2))
    print(f'{client.user} has connected to Discord!')


@client.command()
async def help(ctx):
    await ctx.send("Hi, I am the Anki Bot. Created by Duck 🦆\nTo get started for:\nComputer Science: type .e\nMaths: type .mafs")


async def generateQuestion(option):
    if option == 1:  # Unit 1!!!
        file = open("Unit1.csv", encoding="utf-8")
        csvReader = csv.reader(file)
        number = random.randint(0, 110)
        i = 0
        for row in csvReader:
            row = str(row).replace("[", "")
            row = row.replace("]", "")
            row = str(row).split(",")
            i = i + 1
            if i == number:
                if row[0] == "''" or row[0] is None:
                    await generateQuestion(option=option)
                else:
                    return row[0]
    elif option == 2:
        file = open("Unit2.csv", encoding="utf-8")
        csvReader = csv.reader(file)
        number = random.randint(0, 202)
        i = 0
        for row in csvReader:
            row = str(row).replace("[", "")
            row = row.replace("]", "")
            row = str(row).split(",")
            i = i + 1
            if i == number:
                if row[0] == "''" or row[0] is None:
                    await generateQuestion(option=option)
                else:
                    return row[0]
    else:
        return ""


@client.command()
async def e(ctx, member: discord.Member = None):
    await ctx.send("Enter stop at anytime to end the questions")
    member = ctx.author if not member else member
    embed = discord.Embed(colour=member.colour)
    embed.set_author(name=f"Type a number")
    embed.add_field(name="1.", value="Unit 1 {programming}")
    embed.add_field(name="2.", value="Unit 2 {theory}")
    await ctx.send(embed=embed)
    option = await get_input_of_type(str, ctx)
    try:
        option = int(option)
    except ValueError:
        await ctx.send("Invalid option")
        return

    correct = 0
    total = 0

    while True:
        question = await generateQuestion(option)
        if question == "":
            await ctx.send("Coming soon!")
            break
        await ctx.send("What is " + str(question))
        answer = await get_input_of_type(str, ctx)
        if str(answer).lower() == "stop":
            await ctx.send(f"Ending endless mode, you got {correct}/{total} right :D")
            break
        total = total + 1
        if option == 1:
            file = open("Unit1.csv", encoding="utf-8")
            csvReader = csv.reader(file)
            for row in csvReader:
                row = str(row).replace("[", "")
                row = row.replace("]", "")
                row = str(row).split(",")
                if row[0] == question:
                    fileAnswer = row[1]
                    if row[1] is None:
                        fileAnswer = row[2]
                    embed = discord.Embed(colour=member.colour)
                    embed.set_author(name=f"Question: What is {question}")
                    embed.add_field(name="Answer", value=fileAnswer)
                    await ctx.send(embed=embed)
                    import urllib
                    userAnswer = urllib.parse.quote(answer)
                    actualAnswer = urllib.parse.quote(fileAnswer)
                    try:
                        url = f"https://api.dandelion.eu/datatxt/sim/v1/?text1={actualAnswer}&text2={userAnswer}&token={apiTOKEN}"
                        similarity = r.get(url).json()
                        ratio = similarity["similarity"] * 100
                        # ratio = actualAnswer.similarity(userAnswer) * 100
                        # ratio = fuzz.ratio(row[1].lower(), answer.lower())
                        if ratio <= 50:
                            await ctx.send(
                                f"{ctx.author.mention}, you need to revise this as you were only {int(ratio)}% correct!")
                        elif 51 <= ratio <= 70:
                            await ctx.send(
                                f"{ctx.author.mention}, pretty good answer. You only got {int(ratio)}% correct so you can work on it :)")
                            correct = correct + 1
                        else:
                            await ctx.send(f"{ctx.author.mention}, godly answer wow... {int(ratio)}% correct")
                            correct = correct + 1
                    except:
                        pass
        elif option == 2:
            file = open("Unit2.csv", encoding="utf-8")
            csvReader = csv.reader(file)
            for row in csvReader:
                row = str(row).replace("[", "")
                row = row.replace("]", "")
                row = str(row).split(",")
                if row[0] == question:
                    fileAnswer = row[1]
                    if fileAnswer == " ''":
                        fileAnswer = row[2]
                    embed = discord.Embed(colour=member.colour)
                    embed.set_author(name=f"Question: What is {question}")
                    embed.add_field(name="Answer", value=fileAnswer)
                    await ctx.send(embed=embed)
                    import urllib
                    userAnswer = urllib.parse.quote(answer)
                    actualAnswer = urllib.parse.quote(fileAnswer)
                    try:
                        url = f"https://api.dandelion.eu/datatxt/sim/v1/?text1={actualAnswer}&text2={userAnswer}&token={apiTOKEN}"
                        similarity = r.get(url).json()
                        ratio = similarity["similarity"] * 100
                        # ratio = actualAnswer.similarity(userAnswer) * 100
                        # ratio = fuzz.ratio(row[1].lower(), answer.lower())
                        if ratio <= 30:
                            await ctx.send(
                                f"{ctx.author.mention}, you need to revise this as you were only {int(ratio)}% correct!")
                        elif 31 <= ratio <= 70:
                            await ctx.send(
                                f"{ctx.author.mention}, pretty good answer. You got {int(ratio)}% correct so you can work on it :)")
                            correct = correct + 1
                        elif 71 <= ratio <= 80:
                            await ctx.send(f"{ctx.author.mention}, great answer! {int(ratio)}% correct")
                            correct += 1
                        else:
                            await ctx.send(f"{ctx.author.mention}, wow you smart... {int(ratio)}% correct!")
                            correct = correct + 1
                    except:
                        await ctx.send("Could not get percentage score for that :/")
                        pass


@client.command()
async def q(ctx):
    await ctx.send("Command moved to .e {stands for endless question}")
    await ctx.send("This will soon be a quiz command")


@client.command()
async def s(ctx):
    await ctx.send("Command moved to .e {stands for endless question}")
    await ctx.send("This will soon be a new command")


@client.command()
async def mafs(ctx):
    first = ["On the search for a question", "Ahh here we go again", "Oh boi another hunt for a question yay", "Booting up!", "Beep beep question hunt", "Gimme a second :D", "Why are we doing this again", "I hate my job"]
    second = ["Contacting NASA for assistance", "Looking through the entire Google database", "This looks interesting", "I'm getting somewhere", "Oooooo", "Phone a friend moment", "Wtf is this", "Why am I doing this"]
    third = ["I might have found something", "Hmmm this could be a question... or a virus", "Woaah I think I got something here", "UNLIMITED POWER MUAHAHAHA", "Oh sheeesh I actually found something no way", "Found some question from like 20 years ago :0"]
    fourth = ["Hacking through file", "Modifying the integrity of the data", "Manipulating the space time continuum", "I got itttttt!!!!!!!!!!!!!!!", "I love you.", "From Faheem", "From Duck", "Mwah", "HONEY VPN"]

    message = await ctx.send(random.choice(first))
    driver = webdriver.Chrome(options=chromeOptions)
    await message.edit(content=random.choice(second))
    driver.get("http://mathsbank.co.uk/home/random-question")
    await message.edit(content=random.choice(third))
    time.sleep(2)
    await message.edit(content=random.choice(fourth))
    question = driver.find_element_by_id("question")
    with open('mafsQuestion.png', 'wb') as f:
        f.write(question.screenshot_as_png)
    time.sleep(1)
    await message.edit(content="Sending over!")
    await ctx.send(file=discord.File("mafsQuestion.png"))
    driver.quit()

print("Connecting to discord...")
client.run(token, reconnect=True)
