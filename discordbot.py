import discord
import random
from youtube_dl import YoutubeDL
from discord.ext import commands
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from discord.utils import get
from discord import FFmpegPCMAudio

intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

user = []
musictitle = []
song_queue = []
musicnow = []


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("시험공부"))

# 주사위 게임
@bot.command()
async def 주사위(ctx):
    await ctx.send("주사위를 굴립니다.🎲")
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    if a > b:
        result = "패배😥"
    elif a == b:
        result = "무승부"
    elif a < b:
        result = "승리🎉"
    embed = discord.Embed(title="주사위 게임 결과🎲", description=None, color=0xFF0000)
    embed.add_field(name="봇의 숫자",
                    value="🎲 " + str(a), inline=True)
    embed.add_field(name=ctx.author.name+"님의 숫자",
                    value="🎲 " + str(b), inline=True)
    embed.set_footer(text="결과: " + result)
    await ctx.send(embed=embed)

# 사다리타기
@bot.command()
async def 사다리(ctx):
    insert_value = ctx.message.content[4:len(ctx.message.content)]
    key_, value_ = (insert_value.split('/'))[0], (insert_value.split('/'))[1]
    key = key_.split()
    value = value_.split()
    if len(key) != len(value):  # 짝이 맞지 않는 경우
        await ctx.send("짝이 맞지 않습니다!")
    else:
        random.shuffle(value)
        result = ''
        ladder_embed = discord.Embed(
            title="사다리타기의 결과는?", description="", color=0x7B68EE)
        for i in range(len(key)):
            result += str(key[i])+" ----> "+str(value[i])+"\n"
        ladder_embed.add_field(name="두구두구", value=result)
        await ctx.send(embed=ladder_embed)

# 이미 노래가 재생중일 때 저장해줄 함수
def title(msg):
    global music
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get("https://www.youtube.com/results?search_query="+msg+"lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']
    driver.quit()
    return music, URL

def play(ctx):
    global vc
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda e: next(ctx))

def next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                    after=lambda e: next(ctx))

# 음악재생
@bot.command()
async def play(ctx, *, msg):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel.connect())
        except:
            pass

    if not vc.is_playing():
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        driver.get("https://www.youtube.com/results?search_query="+msg+"lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl
        driver.quit()
        musicnow.insert(0, entireText)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        embed = discord.Embed(
            title="🎶 "+musicnow[0], url=url, color=0x00ff00)
        embed.set_footer(text="신청자: " + ctx.author.name)
        embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/2554/2554000.png")
        await ctx.send(embed=embed)
        vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),
                after=lambda x: next(ctx))
    elif vc.is_playing():
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send(embed=discord.Embed(title="🎶 재생목록 추가", description=result + "(을)를 재생목록에 추가했습니다!", color=0x00ff00))

# 현재 노래 정보
@bot.command()
async def now(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래를 재생하고 있지 않습니다!")
    else:
        await ctx.send(embed=discord.Embed(title="현재 재생 중인 노래", description=musicnow[0] + "을(를) 재생하고 있습니다!", color=0x330000))

# 봇 퇴장
@bot.command()
async def leave(ctx):
    await bot.voice_clients[0].disconnect()

# 일시정지
@bot.command()
async def pause(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed=discord.Embed(title="🛑일시정지", description=musicnow[0]+"(을)를 정지합니다!", color=0x330000))
    else:
        await ctx.send("지금은 노래를 재생하고 있지 않습니다!")

# 다시재생
@bot.command()
async def resume(ctx):
    try:
        vc.resume()
    except:
        await ctx.send("지금은 노래를 재생하고 있지 않습니다!")
    else:
        await ctx.send(embed=discord.Embed(title="🎶다시 재생", description=musicnow[0]+"(을)를 다시 재생합니다!", color=0x330000))

# 노래스킵
@bot.command()
async def skip(ctx):
    if len(musictitle) == 0:
        vc.stop()
        await ctx.send("남아있는 재생목록이 없어 노래를 종료했습니다!")
        await bot.voice_clients[0].disconnect()
    elif len(musictitle) > 0:
        vc.stop()
        await ctx.send(musicnow[0]+"(을)를 스킵했습니다!")

    else:
        await ctx.send("지금은 노래를 재생하고 있지 않습니다!")

# 재생목록
@ bot.command()
async def list(ctx):
    if len(musictitle) == 0:
        await ctx.send("재생목록이 비어있습니다!")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
        await ctx.send(embed=discord.Embed(title="재생목록", description=Text.strip(), color=0x330000))

# 노레 리스트 초기화
@ bot.command()
async def reset(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send("재생목록이 초기화되었습니다!")
    except:
        await ctx.send("재생목록이 이미 비어있습니다!")

# 명령어 목록
@bot.command()
async def 명령어(ctx):
    await ctx.send(embed=discord.Embed(title='명령어 목록!', description="""
    \n!명령어 - 봇의 모든 명령어를 볼 수 있습니다.
    
    \n<미니게임>
    !주사위 - 봇과 무작위로 주사위 게임을 진행합니다.🎲
    !사다리타기 [입력]/[출력] - 사다리타기 게임의 결과를 얻을 수 있습니다. 🪜
    
    \n<음악봇>
    !play [노래이름] - 음악봇이 노래를 검색해 틀어줍니다.
    !leave - 음악봇이 자신이 속한 채널에서 나갑니다.
    !skip - 현재 재생중인 노래를 넘어갑니다.
    !pause - 현재 재생중인 노래를 일시정지시킵니다.
    !resume - 일시정지시킨 노래를 다시 재생합니다.
    !now - 지금 재생되고 있는 노래의 제목을 알려줍니다.
    \n!list - 노래 재생목록을 보여줍니다.
    !reset - 재생목록에 추가된 모든 노래를 초기화합니다.""", color=0xCCFFFF))

# 정의되지 않은 명령어
@ bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 찾지 못했습니다")

# 봇을 실행시키기 위한 토큰을 작성해주는 곳
bot.run(token)
