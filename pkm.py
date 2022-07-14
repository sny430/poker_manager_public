import discord
from discord.ext import commands
import utils

# Botのアクセストークン(非公開)
TOKEN = ''

# 接続に必要なオブジェクトを生成
bot = commands.Bot(command_prefix='./')


# オンラインか確認するコマンド
@bot.command()
async def active(ctx):
    await ctx.send('Poker Manager is active!')


# pt割り当て一覧を呼び出すコマンド
@bot.command()
async def rate(ctx, player, stack):
    rate = utils.pt_rate(int(player), int(stack))
    for i in range(len(rate)):
        await ctx.send('No.' + str(i+1) + ' +' + str(rate[i]) + 'pt')


# ptを確認するコマンド
@bot.command()
async def pt(ctx, name):
    data = utils.json_load()
    name = utils.key_to_value(data['name'], name)
    if not utils.value_check(data['name'], name):
        await ctx.send(utils.value_to_key(data['name'], name) + ' has ' + str(data['point'][name]) + ' point')
    else:
        await ctx.send(name + ' is not linked')


# ptのランキングを確認するコマンド
@bot.command()
async def ranking(ctx, num):
    data = utils.json_load()
    ranking = list(sorted(data['point'].items(), key=lambda x:x[1], reverse=True))
    for i in range(min(10, int(num))):
        await ctx.send(utils.value_to_key(data['name'], ranking[i][0]) + ' ' + str(ranking[i][1]) + 'pt')


# バックアップするコマンド
@bot.command()
@commands.has_role("Promoter")
async def backup(ctx):
    data = utils.json_load()
    utils.json_backup(data)
    await ctx.send('Successful!')


# Discordユーザーを紐付けるコマンド
@bot.command()
@commands.has_role("Promoter")
async def link(ctx, name, user):
    data = utils.json_load()
    if utils.key_check(data['name'], user):
        data['name'][user] = name
        await ctx.send(user + ' is linked to ' + name)
    else:
        await ctx.send(user + ' is linked yet')
    if utils.key_check(data['point'], name):
        data['point'][name] = 0
    utils.json_write(data)


# 固有名を定義するコマンド
@bot.command()
@commands.has_role("Promoter")
async def define(ctx, name):
    data = utils.json_load()
    if utils.key_check(data['point'], name):
        data['point'][name] = 0
        await ctx.send('Successful!')
    else: 
        await ctx.send(name + ' is defined yet')
    utils.json_write(data)


# ptを増減させるコマンド
@bot.command()
@commands.has_role("Promoter")
async def manage(ctx, name, value):
    data = utils.json_load()
    name = utils.key_to_value(data['name'], name)
    if not utils.key_check(data['point'], name):
        point = data['point'][name] + int(value)
        data['point'][name] = point
        await ctx.send('Successful!')
    else:
        await ctx.send(name + ' is not linked')
    utils.json_write(data)


# 結果を入力するとptを加算するコマンド
@bot.command()
@commands.has_role("Promoter")
async def result(ctx, player, stack, *names):
    rate = utils.pt_rate(int(player), int(stack))
    if (len(names) >= len(rate)):
        data = utils.json_load()
        for i in range(len(rate)):
            name = utils.key_to_value(data['name'], names[i])
            if not utils.key_check(data['point'], name):
                point = data['point'][name] + rate[i]
                data['point'][name] = point
                await ctx.send('Successful!')
            else:
                await ctx.send(name + ' is not linked')
        utils.json_write(data)
    else:
        await ctx.send('Result is not enough')


# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)
