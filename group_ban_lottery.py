#!/usr/bin/python3

from nonebot import on_command, CommandSession, permission, on_startup, log, get_bot
from aiocqhttp.exceptions import Error as CQHTTPError
import random

"""
Group Ban Lottery Plugin
A Nonebot Plugin

Version:
0.2.1-Beta
"""

# Available Groups
ENABLE_GROUPS = [111111111, 22222222]


def get_length():
    level = random.randint(1, 100)
    if level < 50:
        length = random.randint(1, 1440)
    elif level < 80:
        length = random.randint(1401, 2880)
    elif level < 99:
        length = random.randint(2801, 4320)
    elif level < 100:
        length = random.randint(4320, 7200)
    else:
        length = 30*24*60
    return length


@on_command('lottery', aliases=('抽奖'), permission=permission.GROUP_MEMBER, only_to_me=False)
async def lottery(session: CommandSession):
    bot = get_bot()
    group = session.event.group_id
    if group is None or group not in ENABLE_GROUPS:
        return
    user = session.event['user_id']
    length = get_length()
    try:
        log.logger.info(f"[GB_Lottery]{group}, {user}, {length}")
        await bot.set_group_ban(group_id=group, user_id=user, duration=length * 60)
    except CQHTTPError:
        pass
    try:
        message = f"抽奖成功！！你抽中的是{length}分钟禁言套餐！"
        await session.send(message, at_sender=True)
    except CQHTTPError:
        pass


@lottery.args_parser
async def _(session: CommandSession):
    pass


@on_command('give_lottery', aliases=('帮你抽奖'), permission=permission.GROUP_ADMIN, only_to_me=False)
async def give_lottery(session: CommandSession):
    bot = get_bot()
    group = session.event.group_id
    if group is None or group not in ENABLE_GROUPS:
        return

    user = session.get('target')
    length = get_length()
    try:
        log.logger.info(f"[GB_Lottery]{group}, {user}, {length}")
        await bot.set_group_ban(group_id=group, user_id=user, duration=length * 60)
    except CQHTTPError:
        pass
    try:
        message = f"[CQ:at,qq={user}]抽奖成功！！你抽中的是{length}分钟禁言套餐！"
        await session.send(message)
    except CQHTTPError:
        pass


@give_lottery.args_parser
async def give_lottery_parser(session: CommandSession):
    stripped_arg = session.current_arg.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['target'] = int(stripped_arg.split('=')[1][:-1])

    return
