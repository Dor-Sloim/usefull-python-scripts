"""
    Discord Bot for creating csgo teams from
    people inside voice channel.

    Setup:
    - pip install -U discord.py
    - pip install python-dotenv
"""

# bot.py
import os
import random
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandInvokeError
from dotenv import load_dotenv

load_dotenv()
"""
    'TOKEN' and 'SERVER_ID_KRU' are loaded
    from '.env' file in classpath.
    
"""
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID_KRU = os.getenv('SERVER_ID_KRU')

bot = commands.Bot(command_prefix='~')


def random_two_teams(members):
    print("members: ", len(members))
    copy_list = members
    random.shuffle(copy_list)

    mid_i = int(len(copy_list) / 2)
    print("mid_i: ", mid_i)

    if mid_i < 1:
        return None, None

    return copy_list[:mid_i], copy_list[mid_i:]


def grab_non_bots_members(members):
    members_without_bots = []
    for member in members:
        if not member.bot:
            members_without_bots.append(member)

    return members_without_bots


@bot.command(name='teams', help='Generates CT and T Side teams from the users in the Lmao voice channel')
async def generate_two_teams(ctx):
    output_ct = []
    output_t = []

    member_names = []
    for member in ctx.guild.voice_channels[0].members:
        member_names.append(member.name)

    ct_team, t_team = random_two_teams(grab_non_bots_members(ctx.guild.voice_channels[0].members))
    if ct_team is not None:

        for member in ct_team:
            output_ct.append('- ' + member.name)

        await send_colored(ctx, 'CT team:', '\n'.join(output_ct), discord.Color.dark_blue(),
                           'Players: {}'.format(str(len(ct_team))))

        for member in t_team:
            output_t.append('- ' + member.name)

        await send_colored(ctx, 'T team:', '\n'.join(output_t), discord.Color.dark_red(),
                           'Players: {}'.format(str(len(output_t))))

        await send_colored(ctx, 'Open a server here:', 'https://fshost.me/free/csgo', discord.Color.dark_magenta())

        def check_should_move_channels(mess):
            ans_lowered = mess.content.lower()

            return ans_lowered in ['yes', 'y', 'yeah'] and mess.channel == ctx.channel

        await ctx.send('Should i move you guys to the channels? (yes/no)')
        answer = await bot.wait_for('message', timeout=20)
        print(answer)
        if check_should_move_channels(answer):
            for member in ct_team:
                await member.move_to(ctx.guild.voice_channels[1])
            for member in t_team:
                await member.move_to(ctx.guild.voice_channels[2])

    else:
        await ctx.send('You need to have at least 2 players in a Voice Channel')


@bot.command(name='define_baiter', help='Explains what baiting is')
async def baiter_define(ctx):
    await ctx.send('Gone.')


@bot.command(name='assemble', help='Bros and Smiley, Assemble!')
async def assemble_members(ctx):
    for vc in ctx.guild.voice_channels:
        for member in vc.members:
            await member.move_to(ctx.guild.voice_channels[0])

    await ctx.send('Bros and Smiley, Assemble!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await send_colored(ctx, 'Stop trolling me', "Did you mean:\n~teams\n~assemble\n", discord.Color.dark_orange())
    elif isinstance(error, CommandInvokeError):
        await ctx.send('Too slow.. Punk')
    else:
        raise error


async def send_colored(ctx, title, description, color, footer=''):
    embed = discord.Embed(color=color,
                          description=description,
                          title=title)
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)


def main():
    bot.run(TOKEN)
    print('Running!')


if __name__ == '__main__':
    main()
