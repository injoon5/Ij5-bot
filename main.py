import discord
import random
import time
import requests
import json
import keep_alive
import asyncio
import os
import logging
import math
import xkcd
from neisparser import*
import datetime
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from replit import db
from tinydb import TinyDB, Query, where
from EZPaginator import Paginator
from meval import*
from dhooks import Webhook, Embed

from tinydb.operations import delete

ptsdb = TinyDB('usrpts.json')

badwordlist = ["씨발", "개새끼", "병신", "ㅂㅅ", "지랄", "ㅈㄹ", "ㅅㅂ", "시발", "ㅅ발", "좇까", "좇", "새끼"]


korea = "http://api.corona-19.kr/korea?serviceKey="
key = os.getenv("covidtoken") #API 키(https://api.corona-19.kr/ 에서 무료 발급 가능)
response = requests.get(korea + key)
text = response.text
data = json.loads(text)

config_dict = get_default_config()
config_dict['language'] = 'kr'  # your language here, eg. Portuguese
owm = OWM(os.getenv("weathertoken"), config_dict)
mgr = owm.weather_manager

# 로그 생성
msglog = logging.getLogger()

# 로그의 출력 기준 설정
msglog.setLevel(logging.CRITICAL)

# log 출력 형식
formatter = logging.Formatter('%(message)s')

# log 출력
#stream_handler = logging.StreamHandler()
#stream_handler.setFormatter(formatter)
#msglog.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('error.log')
file_handler.setFormatter(formatter)
msglog.addHandler(file_handler)

# 로그 생성
warnlog = logging.getLogger()

# 로그의 출력 기준 설정
warnlog.setLevel(logging.ERROR)

# log 출력 형식
formatter = logging.Formatter('%(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
msglog.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('messages.log')
file_handler.setFormatter(formatter)
warnlog.addHandler(file_handler)

config_dict = get_default_config()
config_dict['language'] = 'kr'  # your language here, eg. Portuguese

token = os.getenv("token")

mgr = owm.weather_manager()

def addpts(userid, pts):
  item = Query()
  if userid in ptsdb.all():
    dbsearch = int(ptsdb.search(item.name == userid)[0]["pts"]) + 1
    ptsdb.update({"name": userid, 'pts': dbsearch}, item.name == userid)

  elif not ptsdb.contains(item.name == userid):
    ptsdb.insert({"name": userid, "pts": 1})

hook = Webhook(os.getenv("webhookurl"))
embed = Embed(
    title="봇이 살아남",
    description='와! 봇이 잠에서 깼다!!',
    color=0x5CDBF0,
    timestamp='now'  # sets the timestamp to current time
    )


embed.add_field(name='와 내가 살아났어!', value='사랑해요 개발자님!')
embed.add_field(name='내 정보를 자랑하지', value=f"나는 2개의 샤드를 사용중이며 {len(ptsdb)}명의 유저(중복 X)가 사용중인 엄청난 봇이다!")


#The bot code from here
client = discord.AutoShardedClient(shard_count=2)

startTime = time.time()

@client.event
async def on_ready():
    print("""
  ___  _ ____        ____   ___ _____  __     __  _   _   ___  
 |_ _|(_) ___|      | __ ) / _ \_   _| \ \   / / / | / | / _ \ 
  | | | |___ \ _____|  _ \| | | || |    \ \ / /  | | | || | | |
  | | | |___) |_____| |_) | |_| || |     \ V /_  | |_| || |_| |
 |___|/ |____/      |____/ \___/ |_|      \_/(_) |_(_)_(_)___/ 
    |__/               
    """)
    print(f"{len(client.guilds)}개의 서버에서 활동중이고, 2개의 샤드를 사용중이며 {len(ptsdb)}명의 유저(중복 X)가 사용중...")
    hook.send(embed=embed)
    while True:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="i help 명령어를"))
      await asyncio.sleep(10)
      #Create a variable that contains all the servers
      activeServers = client.guilds
      #Create a variable to store amount of members per server
      sum = 0
      #Loop through the servers, get all members and add them up
      for s in activeServers:
        sum += len(s.members)
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{len(client.guilds)}개의 서버에서 일어나는 일을"))   
      await asyncio.sleep(10)
      await client.change_presence(activity=discord.Game(shard_id=0, name="이 서버는 샤드 0번에 속해 있음"))
      await client.change_presence(activity=discord.Game(shard_id=1, name="이 서버는 샤드 1번에 속해 있음"))
      await asyncio.sleep(10)

#@client.event
#async def on_error(event, *args, **kwargs):
 #   message = args[0] #Gets the message object
  #  await message.channel.send(f"않이;;;; {message.author}!!! \n나 님때문에 에러났잖어!")
   # await client.change_presence(activity=discord.Game(name=f"방금 {message.author.name} 때문에 에러남..."))
    #print(event)
    #print(*args)

@client.event
async def on_message(message):
 
    if message.author.bot:
      return

    addpts(message.author.id, 1)
    #기본 포인트 추가 코드
    
    
    adding = str(math.trunc(int(ptsdb.search(Query().name == message.author.id)[0]["pts"])/100)+1)[0:1]
    if math.trunc(int(ptsdb.search(Query().name == message.author.id)[0]["pts"])/100)+1 < 9:
      adding = 1
    adding=int(adding)
    dbsearch = int(ptsdb.search(Query().name == message.author.id)[0]["pts"]) + adding
    ptsdb.update({"name": message.author.id, 'pts': dbsearch}, Query().name == message.author.id)

 
    
    if client.user.mention in message.content.split():
        await message.channel.send('누구인가?\n누가 나를 멘션했는가?')
    for i in badwordlist:
      if i in message.content:
        await message.channel.send("욕하지마셈. 포인트 1 감소함 ㅅㄱ")
        dbsearch = int(ptsdb.search(Query().name == message.author.id)[0]["pts"]) - 1
        await message.delete()
        ptsdb.update({"name": message.author.id, 'pts': dbsearch}, Query().name == message.author.id)
        warnlog.info(f"{message.guild.name}_{message.channel.name}  {message.author.name}-{message}")


    if message.content.startswith('i hello'):
      await message.channel.send('Hello!')

    if message.content.startswith('i bye'):
      await message.channel.send('Goodbye!')

    if message.content.startswith("i eval"):
      if message.author.id == 741109989309153290:
        a=message.content[7:]       
        try:
          output=await meval(a, globals())
          if not output:
            output="출력 결과가 없어요."
          await message.channel.send(output)
        except Exception as e:
          output=f"에러가 났다!\n{e}"
          await message.channel.send(output)
  
      else:
        await message.channel.send("권한없음")

    if message.content.startswith('i ping'):
      current_time = time.time()
      pingmsg = await message.channel.send("핑 측정중...")
      msgpingtime = time.time()
      pingtime = int((msgpingtime*1000) - (current_time*1000))
      await pingmsg.delete()
      updifference = int(round(current_time - startTime))
      uptext = f"{updifference}초"
      
      embed=discord.Embed(title="봇의 상태", description="@Ij5-BOT 에 대하여", color=0x864ffe)
      embed.add_field(name="이름", value=client.user.name, inline=True)
      embed.add_field(name="만들어진 날", value=client.user.created_at, inline=True)
      embed.add_field(name="활동중인 서버 개수", value=f"{len(client.guilds)}개", inline=True)
      #len(client.guilds)
      embed.set_thumbnail(url=client.user.avatar_url)
      embed.add_field(name="Ping", value=f"{pingtime}ms", inline=True)
      embed.add_field(name="업타임", value=uptext, inline=True)
      embed.add_field(name="자세한 상태", value="[여기](https://stats.injoon5.ga/786944157)", inline=True)
      await message.channel.send(embed=embed)
    
    if message.content.startswith("i addpts"):
      if message.author.id == 741109989309153290:
        apts = message.content.split()
        dbsearch = int(ptsdb.search(Query().name == message.mentions[0].id)[0]["pts"]) + int(apts[3])
        ptsdb.update({"name": message.mentions[0].id, 'pts': dbsearch}, Query().name == message.mentions[0].id)
        await message.channel.send("성공이다!")
      else:
        await message.channel.send("님아개발자 않이자나")
      
  
    if message.content.startswith("i minuspts"):
      apts = message.content.split()
      if message.author.id == 741109989309153290:
        dbsearch = int(ptsdb.search(Query().name == message.mentions[0].id)[0]["pts"]) - int(apts[3])
        ptsdb.update({"name": message.mentions[0].id, 'pts': dbsearch}, Query().name == message.mentions[0].id)
        await message.channel.send("성공이다!")
      else:
        await message.channel.send("님아개발자 않이자나")
        
    if message.content.startswith('i sel '):
      split = message.content.split()
      res = [
        "True",
        "True",
        "True",
        "Maybe",
        "Maybe",
        "Maybe not",
        "Maybe not",
        "False",
        "False",
        "False",
      ]
      await message.channel.send(f"Q: {message.content[6:]}\nA: {random.choice(res)}")

    if message.content.startswith("i refreshdata"):
      from requests import post
      BASEURL = "https://api.koreanbots.dev"
      token = os.getenv("kbotstoken")
      serverCount = len(client.guilds) # 서버 수
      response = post(f'{BASEURL}/bots/servers', headers={"token":token, "Content-Type": "application/json"}, json={"servers": serverCount})
      await message.channel.send("새로고침 완료!\n")
    if message.content.startswith("i pna"):
      msg = await message.channel.send("Test1")
      contents = ["Test1", "Test2", "Test3"]

      page = Paginator(bot=client, message=msg, contents=contents, use_extend=True)
      await page.start()
    
    if message.content.startswith("i pts"):
      item = Query()
      if not message.mentions:
        await message.channel.send(f'{message.author.name}님은 {ptsdb.search(item.name == message.author.id)[0]["pts"]} ipoints 있습니다!!\n{math.trunc(int(ptsdb.search(item.name == message.author.id)[0]["pts"])/100)+1}레벨입니다!')
      else:
        if message.mentions[0].bot:
          await message.channel.send("그는 봇이었다.")
        else:
          print(message.mentions[0].id)
          await message.channel.send(f'{message.mentions[0].name}님은 {ptsdb.search(item.name == message.mentions[0].id)[0]["pts"]} ipoints 있습니다!!\n{math.trunc(int(ptsdb.search(item.name == message.mentions[0].id)[0]["pts"])/100)+1}레벨입니다!')

    if message.content == "i delmyinfo":
      ptsdb.remove(where('name') == message.author.id)
      await message.channel.send("Goodbye...")

    if message.content.startswith('i say'):
      await message.channel.send(f"{message.content[6:]}") 
      
    if message.content.startswith('i calc '):
      split = message.content.split()
      
      if split[2] == "plus":
        a = int(split[3])
        b = int(split[4])
        result = int(a)+int(b)
      elif split[2] == "minus":
        a = int(split[3])
        b = int(split[4])
        result = int(a)-int(b)
      elif split[2] == "multiply":
        a = int(split[3])
        b = int(split[4])
        result = int(a)*int(b)
      elif split[2] == "divide":
        a = int(split[3])
        b = int(split[4])
        result = int(a)/int(b)
      else:
        result = "plus/minus/multiply/divide 이에는 지원이 안됩니다."
      await message.channel.send(result)

    if message.content.startswith('i userinfo'):
      author = message.author
      embed=discord.Embed(title="사용자 정보", description="사용자의 정보입니다.", color=discord.Color.blue())
      embed.add_field(name="이름", value=author.name, inline=False)
      embed.set_thumbnail(url=author.avatar_url)
      await message.channel.send(embed=embed)
      
    if message.content.startswith('i whereami'):
      channel = str(message.channel)
      guild = str(message.guild)
      embed=discord.Embed(title="서버 정보", description="서버의 정보입니다.", color=discord.Color.blue())
      embed.add_field(name="서버 이름", value=guild, inline=False)
      embed.add_field(name="채널 이름", value=channel, inline=False)
      embed.set_thumbnail(url=message.guild.icon_url)
      await message.channel.send(embed=embed)
    
    if message.content.startswith('i rsp '):
      res = [
        "✌️",
        "👊",
        "🖐",
      ]
      await message.channel.send(f"{random.choice(res)}!")

    if message.content.startswith('i cointhrow'):
      
      res = [
        "Front",
        "Back",
      ]
      await message.channel.send(f"{random.choice(res)}!")

    if message.content.startswith('i timer '):
      secs = message.content[8:]
      rsecs = int(secs)
      archivesecs = rsecs
      infomsg = await message.channel.send(f"{rsecs}초 타이머 시작!")
      while rsecs > 0:
        await asyncio.sleep(1)
        rsecs -= 1
        await infomsg.edit(content=f"{rsecs}초 남았습니다!")
      if rsecs == 0:
        await infomsg.delete()
        await message.channel.send(f"**삐리링 삐리링!!**\n{archivesecs}초 타이머가 끝났습니다! ")
    
    if message.content.startswith("i weather"):
      observation = mgr.weather_at_place('Seoul,South Korea')
      w = observation.weather
      await message.channel.send(f"현재 날씨 : {w.detailed_status}\n현재 기온 : {w.temperature('celsius')['temp']}\n최고 기온/최저 기온 : {w.temperature('celsius')['temp_max']}/{w.temperature('celsius')['temp_min']}\n습도 : {w.humidity}")
    
    if message.content.startswith('i draw'):
      gamblemsg = await message.channel.send("3분의 1 뽑기를 시작합니다.")
      await asyncio.sleep(1)
      await gamblemsg.edit(content="뽑기를 준비중입니다......\n1에서 4초정도 기다려 주세요......")      
      a = random.randrange(0,4)
      b = random.randrange(0,4)
      c = random.randrange(0,4)
      time.sleep(random.randrange(1,4))
      if a == b == c:
        await gamblemsg.edit(content = f"오 {a} {b} {c}로 뽑기를 우승했습니다!!\n포인트에 {a}+{b}+{c}*{10}의 값인 {(a+b+c)*10}가 추가됩니다!")
        dbsearch = int(ptsdb.search(Query().name == message.author.id)[0]["pts"]) + ((a+b+c)*10)
        ptsdb.update({"name": message.author.id, 'pts': dbsearch}, Query().name == message.author.id)
        
      else:
        await gamblemsg.edit(content=f"{a} {b} {c}로 뽑기를 졌습니다....\n포인트가 {a}-{b}-{c}*10인 {(a+b+c)*10}만큼 깎입니다...")
        dbsearch = int(ptsdb.search(Query().name == message.author.id)[0]["pts"]) - ((a-b-c)*10)
        ptsdb.update({"name": message.author.id, 'pts': dbsearch}, Query().name == message.author.id)        
       
    if message.content.startswith('populate'):
      emoji = '\N{THUMBS UP SIGN}'
      # or '\U0001f44d' or '👍' you payrolls had to go to
      await message.add_reaction(emoji)

    if message.content.startswith('pin'):
      if message.author.id == 741109989309153290 or message.author.guild_permissions.administrator == True:
        await message.pin()
        pin_id = message.id
        await message.channel.send(f"고정되었고, 아이디는 {message.id}")
      else:
        await message.channel.send("님 어드민 아니쥬?!")
        
    if message.content.startswith('unpin'):
      unpinsplit = message.content[5:]
      unpinmsg = await message.channel.fetch_message(unpinsplit)
      if unpinmsg.pinned:
        if message.author.id == 741109989309153290 or message.author.guild_permissions.administrator == True:
          await unpinmsg.unpin(reason="By ij5-BOT")
        else:
          await message.channel.send("님 어드민 아니쥬?!")
      else:
        await message.channel.send("그거 고정된 메시지 아닌디;;;")
        
    if message.content.startswith('delme'):
      infomsg = await message.channel.send("위 메시지는 10초 뒤에 삭제됩니다!")
      secs = 10
      while secs > 0:
        await asyncio.sleep(1)
        secs -= 1
        await infomsg.edit(content=f"위 메시지는 {secs}초 뒤에 삭제됩니다!")
      if secs == 0:
        await message.delete()
        await infomsg.edit(content="삭제되었습니다.")
        await asyncio.sleep(5)
        await infomsg.delete()
        
    if message.content.startswith("i randpic"):
      urllist=["https://source.unsplash.com/weekly?water", "https://source.unsplash.com/weekly", "https://source.unsplash.com/weekly?nature", "https://source.unsplash.com/random","https://source.unsplash.com/user/erondu", "https://source.unsplash.com/user/jackie/likes", "https://source.unsplash.com/user/erondu/daily", "https://source.unsplash.com/daily"]
      
      embed=discord.Embed(title="랜덤 사진", description="Source from unsplash.", color=discord.Color.blue())
      
      embed.set_image(url=random.choice(urllist))
      await message.channel.send(embed=embed)
      
    if message.content.startswith("i food "):
      foodsplit=message.content.split()
      today = datetime.date.today()
      d1 = today.strftime("%Y.%m.%d")
      d2 = (datetime.date.today() + datetime.timedelta(days=1)).weekday()
      meal = get_diet(2, d1, int(d2), foodsplit[2])

      await message.channel.send(f"내일의 급식 : \n{meal}")
    
    if message.content.startswith("i math"):
      await message.channel.send(f"파이값 : {math.pi}\n오일러 : {math.e}")
      
    if message.content.startswith("i xkcd"):
      xkcdtitle=xkcd.parse_newest("safe_title")
      xkcdnum = xkcd.get_newest_page_number()
      embed=discord.Embed(title="xkcd", description="A webcomic of romance, sarcasm, math, and language.", color=0x96a8c8)
      embed.add_field(name=f"{xkcdnum}_{xkcdtitle}", value=xkcd.parse_newest("alt"), inline=True)
      embed.set_image(url=xkcd.get_newest_image_url())
      embed.set_footer(text="This message is best viewed with Netscape Navigator 4.0 or below on a Pentium 3±1 emulated in Javascript on an Apple IIGS at a screen resolution of 1024x1. Please enable your ad blockers, disable high-heat drying, and remove your device from Airplane Mode and set it to Boat Mode. For security reasons, please leave caps lock on while browsing.") 
      
      embed.add_field(name="자세한 정보는 ", value="[여기서!](https://xkcd.com)", inline=True)
      await message.channel.send(embed=embed)
    
    if message.content.startswith("i db add"):
      dbsplit = message.content.split()
      db[dbsplit[3]] = dbsplit[4]
      await message.channel.send("저장 완료!!")
      
    if message.content.startswith("i db print"):
      dbsplita = message.content.split()
      await message.channel.send(db[dbsplita[3]])
    
    if message.content.startswith('i invite'):
      embed=discord.Embed(title="ij5-BOT invite", url="https://discord.com/api/oauth2/authorize?client_id=797712776012627988&permissions=268954704&scope=bot%20applications.commands", description="ij5-BOT을 자신의 서버에 초대하세요!", color=0x109319)
      await message.channel.send(embed=embed)

    if message.content.startswith("i covid"):
      response = requests.get(korea + key)
      text = response.text
      data = json.loads(text)
      await message.channel.send(
        "=== [ " + data["updateTime"] + "상황 ] ===\n\n" + 
        "국내 확진자: " + data["TotalCase"] + "\n" + 
        "국내 완치자: " + data["TotalRecovered"] + "\n" + 
        "국내 사망자: " + data["TotalDeath"] + "\n" + 
        "국내 치료중: " + data["NowCase"] + "\n\n" 
      )
      print("정보 요청: 국내 상황 정보")
    
    if message.content.startswith("i notice "):
      if message.author.id == 741109989309153290:
        noticesplit = message.content.split()
        channel = client.get_channel(int(noticesplit[2]))
        await channel.send(f'공지 : {noticesplit[3]}')
      else:
        await message.channel.send('권한이 업서여')
      
    if message.content.startswith('i help'):
      guild = str(message.guild)
      #### Create the initial embed object ####
      embed1=discord.Embed(title="ij5-BOT help", description="ij5-BOT의 도움말 입니다. 여기서 명령어에 대해 알아보세요!", color=discord.Color.blue())
      embed1.add_field(name="`i (hello/bye)`", value="인사하기", inline=True) 
      embed1.add_field(name="`i sel (질문)`", value="질문에 답하기", inline=True)
      embed1.add_field(name="`i say (아무 글자)`", value="입력한 글자 말하기", inline=True)
      embed1.set_footer(text=f"1/4\n{guild}에서 이 봇을 사용해 주셔서 감사합니다. \n이 봇을 자신의 서버에 초대하려면?\n i invite 로 자세한 정보를 알아보세요.\n{message.author.name}만 다음 페이지로 넘길 수 있습니다. {message.author.name}이 아니라면 `i help` 명령어를 사용하세요.\n Idea from codingPro01, Made with ❤️ by injoon5") 

      embed2=discord.Embed(title="ij5-BOT help", description="ij5-BOT의 도움말 입니다. 여기서 명령어에 대해 알아보세요!", color=discord.Color.blue())
      embed2.add_field(name="`i ping`", value="ping 확인", inline=True)
      embed2.add_field(name="`i userinfo`", value="User 정보 표시", inline=True)
      embed2.add_field(name="`i whereami`", value="서버, 채널 정보 표시", inline=True)
      embed2.add_field(name="`i covid`", value="코로나 19 국내 상황 확인", inline=True)
      embed2.add_field(name="`i randpic`", value="랜덤 사진 출력", inline=True)
      embed2.add_field(name="`i xkcd`", value="xkcd 만화 보기", inline=True)
      embed2.add_field(name="`i math`", value="파이값 등 출력", inline=True)
      embed2.add_field(name="`i food (학교고유코드)`", value="내일의 급식 보기(고유코드는 [여기!](https://schoolmenukr.ml/code/app))", inline=True)
      embed2.set_footer(text=f"2/4\n{guild}에서 이 봇을 사용해 주셔서 감사합니다. \n이 봇을 자신의 서버에 초대하려면?\n i invite 로 자세한 정보를 알아보세요.\n{message.author.name}만 다음 페이지로 넘길 수 있습니다. {message.author.name}이 아니라면 `i help` 명령어를 사용하세요.\n Idea from codingPro01, Made with ❤️ by injoon5") 
      
      embed3=discord.Embed(title="ij5-BOT help", description="ij5-BOT의 도움말 입니다. 여기서 명령어에 대해 알아보세요!", color=discord.Color.blue())
      embed3.add_field(name="`i rsp (가위, 바위, 보 중 하나)`", value="가위바위보", inline=True)
      embed3.add_field(name="`i cointhrow`", value="동전던지기", inline=True)   
      embed3.add_field(name="`i calc plus/minus/multiply/divide`", value="4칙연산", inline=True)
      embed3.add_field(name="`i timer (초)`", value="타이머", inline=True)
      embed3.add_field(name="`i draw`", value="뽑기", inline=True)
      embed3.add_field(name="`i pts (선택: 유저 멘션)`", value="유저의 포인트 확인", inline=True)
      embed3.add_field(name="`i delmyinfo`", value="캐시된 유저 정보 삭제", inline=True)
      embed3.add_field(name="`i db add (아이디) (내용)`", value="db에 아이디로 내용 저장", inline=True)  
      embed3.add_field(name="`i db print (아이디)`", value="아이디 내용 출력", inline=True)   
      embed3.add_field(name="`populate (메시지 내용)`", value="메시지에 좋아요 누르기", inline=True)
      embed3.add_field(name="`pin (메시지 내용)`", value="메시지 고정", inline=True)
      embed3.add_field(name="`unpin (메시지 id)`", value="입력한 id 메시지 고정해제", inline=True)
      embed3.add_field(name="`delme (메시지 내용)`", value="10초후 메시지 삭제", inline=True)
      embed3.set_footer(text=f"3/4\n{guild}에서 이 봇을 사용해 주셔서 감사합니다. \n이 봇을 자신의 서버에 초대하려면?\n i invite 로 자세한 정보를 알아보세요.\n{message.author.name}만 다음 페이지로 넘길 수 있습니다. {message.author.name}이 아니라면 `i help` 명령어를 사용하세요.\n Idea from codingPro01, Made with ❤️ by injoon5") 

      embed4=discord.Embed(title="ij5-BOT Credits", description="ij5-BOT의 Credit 입니다. 여기서 Credit에 대해 알아보세요!", color=discord.Color.blue()) 
      embed4.add_field(name="Idea", value="**codingPro01**\n[GitHub](https://github.com/codingpro01)", inline=True) 
      embed4.add_field(name="Coding", value="**injoon5**\n[GitHub](https://github.com/injoon5)", inline=True)  
      embed4.add_field(name="봇 개발자에게 하트는 큰 힘이 됩니다", value="[KOREANBOTS에서 하트 누르기](https://koreanbots.dev/bots/797712776012627988)", inline=False)  
      embed4.set_footer(text=f"4/4\n{guild}에서 이 봇을 사용해 주셔서 감사합니다. \n이 봇을 자신의 서버에 초대하려면?\n i invite 로 자세한 정보를 알아보세요.\n{message.author.name}만 다음 페이지로 넘길 수 있습니다. {message.author.name}이 아니라면 `i help` 명령어를 사용하세요.\n Idea from codingPro01, Made with ❤️ by injoon5")       

      embeds = [embed1, embed2, embed3, embed4]
      msg = await message.channel.send(embed=embed1)
      page = Paginator(bot=client, message=msg, embeds=embeds, use_extend=True,only=message.author)
      await page.start()
            
keep_alive.keep_alive()      


client.run(token) 