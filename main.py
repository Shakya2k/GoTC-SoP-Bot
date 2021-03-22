import os
import keep_alive
import discord
from dotenv import load_dotenv
from discord.ext import commands
import pandas as pd

keep_alive.keep_alive()

load_dotenv(' .env')
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix="$")

@bot.command()
@commands.is_owner()
async def broadcast(ctx, title, content):
  for guild in bot.guilds:
    for channel in guild.channels:
      if "sop" in channel.name:
        embed= discord.Embed(title=str(title), description=str(content), color=discord.Color.blue())
        await channel.send(embed=embed)
        break
@bot.command(help='Setup the bot')
async def setup(ctx):
  if ctx.guild is None:
    m= "sop.csv"
  else:
    m= "sop_"+str(ctx.guild.id)+".csv"
  if os.path.isfile(m)==True:
    await ctx.channel.send("Setup already done!")
  else:
    df = pd.read_csv("sop.csv")
    data=pd.DataFrame(df)
    data.to_csv(m)
    await ctx.channel.send("Setup Completed!")

@bot.command(help='Ping-Pong (type $ping)')
async def ping(ctx):
	await ctx.channel.send("Pong 🏓")

@bot.command(help='Displays information about an SoP (type $info <sop name>)')
async def info(ctx, name1, name2="", name3="", name4="", name5=""):
  if name2!="":
    if name3!="":
      if name4!="":
        if name5!="":
          n = name1 + " " + name2 + " " + name3 + " " +name4 + " " + name5
        else:
          n = name1 + " " + name2 + " " + name3 + " " + name4 
      else:
        n = name1 + " " + name2 + " " + name3
    else:
      n = name1 + " " + name2
  else:
    n = name1
  cols = ['Star', 'Seat Name', 'Region Overlap', 'Holder Buffs', 'Title name', 'Buff', 'Regional Bonuses', 'Owned', 'Owner', 'Rein', 'Slots', 'Wall', 'Tier']
  if ctx.guild is None:
    m= "sop.csv"
  else:
    m= "sop_"+str(ctx.guild.id)+".csv"
  if os.path.isfile(m)==False:
    await ctx.channel.send("Setup not done!(type $setup)")
  else:
    data = pd.read_csv(m, names=cols)
    l = data.values.tolist()
    sop = []
    p=""
    for i in range(1,len(l)):
      x = str(l[i][1])
      if x.upper() == n.upper():
        sop.append(l[i])

    if len(sop)==0:
      await ctx.channel.send("Enter Valid SoP name!!!")
      msg= ctx.message
      await msg.add_reaction('❌') 
    else: 
      p+= str(cols[2]) + ":     " + str(sop[1][2])+"\n"
      p+= str(cols[7]) + ":     " + str(sop[1][7])
      embed= discord.Embed(title=str(sop[1][0])+"⭐", description=p, color=discord.Color.red())
      p="" 
      embed.set_author(name=str(sop[1][1]), icon_url="https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffansided.com%2Ffiles%2F2019%2F02%2Firon-throne.jpg") 
      if ctx.guild is None:
        x=ctx.author.avatar_url 
      else:
        x=ctx.guild.icon_url
      embed.set_thumbnail(url=x) 
      for i in range (len(sop)):
        if str(sop[i][3]) != "0":
          p+= "\n" + str(sop[i][3])
      embed.add_field(name="Holder Buffs:", value=p, inline=False)
      i=0
      p=""
      while i<len(sop):
        p+= str(sop[i][4])+ ": " +"\n"+ str(sop[i][5])
        c=1
        for j in range(1, len(sop)):
          if i+j < len(sop):
            if str(sop[i+j][4]) == str(sop[i][4]):
              p+= "\n"+str(sop[i+j][5])
              c+=1
            else:
              break
        p+= "\n\n"
        i+=c
      embed.add_field(name="Titles:", value=p, inline=False)
      p= ""      
      for i in range (len(sop)):
        if sop[i][6] != "0":
          p+= str(sop[i][6]) + "\n"
      embed.add_field(name="Regional Bonuses", value=p, inline=False)
      msg= ctx.message
      await msg.add_reaction('✅')
      await ctx.author.send(embed=embed)
      #await ctx.channel.send(embed=embed)

@bot.command(help='Searches for SoPs offering the specific buff (type $search <"buff"> <star(if any)> quotes important in buff)')
async def search(ctx, buff1, star=""):
  n=buff1
  cols = ['Star', 'Seat Name', 'Region Overlap', 'Holder Buffs', 'Title name', 'Buff', 'Regional Bonuses', 'Owned', 'Owner', 'Rein', 'Slots', 'Wall', 'Tier']
  if ctx.guild is None:
    m= "sop.csv"
  else:
    m= "sop_"+str(ctx.guild.id)+".csv"
  if os.path.isfile(m)==False:
    await ctx.channel.send("Setup not done!(type $setup)")
  else:
    data = pd.read_csv(m, names=cols)
    l = data.values.tolist()
    sop = []
    p = ""
    for i in range(1,len(l)):
      for j in range (3, len(l[i])):
        x = str(l[i][j])
        y = str(l[i][0])
        if n.upper() in x.upper() and l[i] not in sop:
          if str(star)!="":
            if y==str(float(star)):
              sop.append(l[i])
          else:
            sop.append(l[i])
    if len(sop)==0:
      msg= ctx.message
      await msg.add_reaction('❌')
    else:
      count1 = []      
      for i in range (len(sop)):
        count2 = []
        if sop[i][1] not in count1:
          p+= "\n----------\n"+"***Name:*** " + str(sop[i][1]) + "\n" + "***Star:*** " + str(sop[i][0]) + "\n" + "***Region Overlap:*** " + str(sop[i][2]) + "\n" +  "***Owned:*** " + str(sop[i][7]) + "\n"
          if str(sop[i][7])=="YES":
            p+= "***Owner:*** <@" + str(int(sop[i][8])) + ">" + "\n\n"
          else:
            p+="\n"
          count1.append(str(sop[i][1]))
        for j in range (len(sop[i])):
          if n.upper() in str(sop[i][j]).upper():
            if str(cols[j]) != "Buff":
              if str(cols[j]) not in count2:
                p+= "***" + str(cols[j]) + ":*** " + str(sop[i][j]) + "\n"
                count2.append(cols[j])
            else:
              if sop[i][j-1] not in count2:
                p+= "***" + str(sop[i][j-1]) + " Title:*** " + str(sop[i][j]) + "\n"
                count2.append(str(sop[i][j-1]))
        p+= "\n"
      while True:
        if len(p)<=2000:
          msg= ctx.message
          await msg.add_reaction('✅')
          await ctx.author.send(p)
          #await ctx.channel.send(p)
          break
        else:
          a=p[:2000]
          for i in range (-1, -(len(a)), -1):
            if a[i]=="\n":
              x=len(a)+i
              a=a[:x]
              p=p[x:]
              await ctx.author.send(a)
              #await ctx.channel.send(a)
              break

@bot.command(help='Sets a locked list (type $set <"sop name"> <@owner> quotes in sop name mandatory)')
@commands.guild_only()
#@commands.has_role('Admin')
async def set(ctx, name, user : discord.Member):
  if ctx.guild is None:
    m= "sop.csv"
  else:
    m= "sop_"+str(ctx.guild.id)+".csv"
  if os.path.isfile(m)==False:
    await ctx.channel.send("Setup not done!(type $setup)")
  else:
    df =  pd.read_csv(m)
    data = pd.DataFrame(df)
    if 'Unnamed: 0' in data.columns:
      del data['Unnamed: 0']
    c=[]
    v=0
    for i in range (len(data["Seat Name"])):
      if name.lower()==data["Seat Name"][i].lower():
        v=1
        break
    if v==1:
      for i in range(len(data["Seat Name"])):
        x = data["Seat Name"]
        if x[i].lower()==name.lower():
          c.append(i)
      for i in range (len(c)):
        x = data["Owned"]
        y = data["Owner"]
        x[c[i]] = "YES"
        y[c[i]] = user.id
      data.to_csv(m)
      msg= ctx.message
      await msg.add_reaction('✅')
    else:
      msg= ctx.message
      await msg.add_reaction('❌')


@bot.command(help= 'Deletes sop from locked list (type $del_sop <"sop name"> quotes in sop name mandatory)')
@commands.guild_only()
#@commands.has_role('Admin')
async def del_sop(ctx, name):
  if ctx.guild is None:
    m= "sop.csv"
  else:
    m= "sop_"+str(ctx.guild.id)+".csv"
  if os.path.isfile(m)==False:
    await ctx.channel.send("Setup not done!(type $setup)")
  else:
    df =  pd.read_csv(m)
    data = pd.DataFrame(df)
    if 'Unnamed: 0' in data.columns:
      del data['Unnamed: 0']
    c=[]
    v=0
    for i in range (len(data["Seat Name"])):
      if name.lower()==data["Seat Name"][i].lower():
        v=1
        break
    if v==1:
      for i in range (len(data["Seat Name"])):
        x = data["Seat Name"]
        if x[i].lower()==name.lower():
          c.append(i)
      for i in range (len(c)):
        x = data["Owned"]
        y = data["Owner"]
        x[c[i]] = "NO"
        y[c[i]] = 0
      data.to_csv(m)
      msg= ctx.message
      await msg.add_reaction('✅')
    else: 
      msg= ctx.message     
      await msg.add_reaction('❌')

@bot.command(help= 'Deletes entire locked list (type $del_list)')
@commands.guild_only()
#@commands.has_role('Admin')
async def del_list(ctx):
  if ctx.guild is None:
    m= "sop.csv"
  else:
    m= "sop_"+str(ctx.guild.id)+".csv"
  if os.path.isfile(m)==False:
    await ctx.channel.send("Setup not done!(type $setup)")
  else:
    df = pd.read_csv (m)
    data = pd.DataFrame(df)
    if 'Unnamed: 0' in data.columns:
      del data['Unnamed: 0']
    for i in range (len(data["Seat Name"])):
      x=data["Owned"]
      y=data["Owner"]
      if x[i]=="YES":
        x[i] = "NO"
        y[i] = "0"
    data.to_csv(m)
    msg=ctx.message
    await msg.add_reaction('✅')

@bot.command(help='Displays locked list (type $display)')
@commands.guild_only()
async def display(ctx):
  if ctx.guild is None:
    m= "sop.csv"
  else:
    m= "sop_"+str(ctx.guild.id)+".csv"
  if os.path.isfile(m)==False:
    await ctx.channel.send("Setup not done!(type $setup)")
  else:
    df = pd.read_csv(m)
    data = pd.DataFrame(df)
    if 'Unnamed: 0' in data.columns:
      del data['Unnamed: 0']
    n=[]
    s=[]
    o=[]
    t=[]
    b=[]
    r=[]
    for i in range (len(data["Owned"])-4):
      if str(data["Owned"][i]) == "YES":
        if str(data["Seat Name"][i]) not in n:
          n.append(str(data["Seat Name"][i]))
          s.append(str(data["Star"][i]))
          o.append(str(int(data["Owner"][i])))
          j=i
          c=[]
          q=[]
          d=[]
          count=[]

          for j in range (i,len(data["Owned"])-4):
            if str(data["Seat Name"][j])!=str(data["Seat Name"][i]):
              break
            if data["Regional Bonuses"][j]!="0" and data["Regional Bonuses"][j] not in q:
              q.append(str(data["Regional Bonuses"][j]))
            if data["Title Name"][j] not in count:
              count.append(data["Title Name"][j])
              c.append(data["Title Name"][j])
              k=j
              x=[]
              while data["Title Name"][k]==data["Title Name"][j]:
                x.append(data["Buff"][k])
                k+=1
              d.append(x)
          r.append(q)
          t.append(c)
          b.append(d)
    if len(n)==0:
      await ctx.channel.send("You don't have a locked SoP List!!!")
    else:
      for i in range(len(n)):
        p=""
        p+= "Owner:     <@" + str(o[i]) + ">"
        embed= discord.Embed(title=str(s[i])+"⭐", description=p, color=discord.Color.green())
        p="" 
        embed.set_author(name=str(n[i]), icon_url="https://images2.minutemediacdn.com/image/fetch/w_2000,h_2000,c_fit/https%3A%2F%2Ffansided.com%2Ffiles%2F2019%2F02%2Firon-throne.jpg") 
        if ctx.guild is None:
          x=ctx.author.avatar_url 
        else:
          x=ctx.guild.icon_url
        embed.set_thumbnail(url=x)
        p=""
        for j in range (len(t[i])):
          if "Attack x" not in str(t[i][j]):
            p+= "\n"+str(t[i][j])+":     \n"
            for k in range (len(b[i][j])):
              p+=b[i][j][k] + "\n"
        embed.add_field(name="Titles:", value=p, inline=False)
        p=""
        for j in range (len(r[i])):
          p+="\n"+str(str(r[i][j]))
        embed.add_field(name="Regional Bonuses:", value=p, inline=True)
        #await ctx.author.send(embed=embed)
        await ctx.channel.send(embed=embed)
@bot.command(help='Displays SoP list (type $seat <star level(only 5,4.5,4,3.5,3,2.5 now)>)')
async def seat(ctx, star):
  s=['5','4.5','4','3.5','3','2.5']
  if star not in s:
    msg= ctx.message
    await msg.add_reaction('❌')
    await ctx.channel.send('Star Level does not exist!!')
  else:
    if ctx.guild is None:
      m= "sop.csv"
    else:
      m= "sop_"+str(ctx.guild.id)+".csv"
    if os.path.isfile(m)==False:
      await ctx.channel.send("Setup not done!(type $setup)")
    else:
      df = pd.read_csv(m)
      data = pd.DataFrame(df)
      if 'Unnamed: 0' in data.columns:
        del data['Unnamed: 0']
      sop=[]
      for i in range (len(data["Seat Name"])):
        if float(data["Star"][i])==float(star):
          if str(data["Seat Name"][i]) not in sop:
            sop.append(str(data["Seat Name"][i]))      
      p="All "+ str(star) + "⭐  Sop are:"
      q=""
      for i in range (len(sop)):
        q+= str(sop[i]) + "\n"
      embed = discord.Embed(title=p, description=q, color=discord.Color.blue())
      msg= ctx.message
      await msg.add_reaction('✅')
      await ctx.author.send(embed=embed)
      #await ctx.channel.send(embed=embed)
      
@bot.command(help='Displays Star Info (type $star_info <star level(only 5,4.5,4,3.5,3,2.5 now)>)')
async def star_info(ctx, star):
  s=['5','4.5','4','3.5','3','2.5']
  if star not in s:
    await ctx.channel.send('Star Level does not exist!!')
  else:
    if ctx.guild is None:
      m= "sop.csv"
    else:
      m= "sop_"+str(ctx.guild.id)+".csv"
    if os.path.isfile(m)==False:
      await ctx.channel.send("Setup not done!(type $setup)")
    else:
      df = pd.read_csv(m)
      data = pd.DataFrame(df)
      if 'Unnamed: 0' in data.columns:
        del data['Unnamed: 0']
      rein=[]
      slots=[]
      wall=[]
      tier=[]
      for i in range (len(data["Star"])):
        if float(data["Star"][i])==float(star):
            rein.append(str(data["Rein"][i]))
            slots.append(str(data["Slots"][i]))
            wall.append(str(data["Wall"][i]))
            tier.append(str(data["Tier"][i]))
            break      
      p="Info for "+str(star)+"⭐  SoP:"
      q= "\n\nReinforcement Capacity:   " + str(rein[0]) + "\nReinforcement Slots:   " + str(slots[0])[0:2] + "\nWall Health:   " + str(wall[0]) + "\nTier Level:   " + str(tier[0])
      embed = discord.Embed(title=p, description=q, color=discord.Color.blue())
      #await ctx.author.send(embed=embed)
      await ctx.channel.send(embed=embed)
  
bot.run(TOKEN)
