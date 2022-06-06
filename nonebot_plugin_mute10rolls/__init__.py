from nonebot import on_command
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot import require
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.adapters.onebot.v11 import GROUP, GROUP_ADMIN, GROUP_OWNER, Message, GroupMessageEvent
from nonebot.params import Depends, CommandArg, State
from .data_source import *

__mute_rolls_vsrsion__ = "v0.1.0a2"
__mute_rolls_notes__ = f'''
禁言十连 {__mute_rolls_vsrsion__}
十连抽取口球套餐
开启/启用/禁用/关闭禁言十连
修改禁言冷却 [修改禁言cd/冷却][seconds]
'''.strip()

mute_rolls = on_command(cmd="禁言十连", permission=GROUP, priority=12)
rank = on_command(cmd="禁言统计", permission=GROUP, priority=12)
roll_on = on_command(cmd="启用禁言十连", aliases={"开启禁言十连"}, permission=GROUP_ADMIN | GROUP_OWNER, priority=12, block=True)
roll_off = on_command(cmd="禁用禁言十连", aliases={"关闭禁言十连"}, permission=GROUP_ADMIN | GROUP_OWNER, priority=12, block=True)
cd_change = on_command(cmd="修改禁言cd", aliases={"修改禁言冷却"}, permission=GROUP_ADMIN | GROUP_OWNER, priority=12, block=True)

scheduler = require("nonebot_plugin_apscheduler").scheduler

@roll_on.handle()
async def _(event: GroupMessageEvent):
    gid = str(event.group_id)
    m10r_manager.switch_enable(gid, True)
    await roll_on.finish("已启用禁言十连功能")

@roll_off.handle()
async def _(event: GroupMessageEvent):
    gid = str(event.group_id)
    m10r_manager.switch_enable(gid, False)
    await roll_off.finish("已禁用禁言十连功能")
    
async def get_new_cd(args: Message = CommandArg(), state: T_State = State()):
    args = args.extract_plain_text().strip().split()

    if not args:
        await cd_change.finish("缺少冷却时间参数")
    elif args and len(args) == 1:
        cd = int(args[0])
        if cd < 10:
            cd = 10
        if cd > 120:
            cd = 120
        return {**state, "cd": cd}
    else:
        await cd_change.finish("参数太多啦~")
        
@cd_change.handle()
async def _(event: GroupMessageEvent, state: T_State = Depends(get_new_cd)):
    gid = str(event.group_id)
    cd = state["cd"]
    m10r_manager.change_cd(gid, cd)
    
    if m10r_manager.check_enable(gid):
        await cd_change.finish(f"已修改冷却时间为 {cd}s")
    else:
        await cd_change.finish(f"已修改冷却时间为 {cd}s")

@mute_rolls.handle()
async def _(matcher: Matcher, event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip()
    if args == "帮助":
        await matcher.finish(__mute_rolls_notes__)
    
    gid = str(event.group_id)
    
    cd = m10r_manager.check_cd(gid)
    if not m10r_manager.check_enable(gid):
        # Trial version
        if cd > 0:
            await matcher.finish(f"技能冷却中，剩余 {cd}s\n需管理员启用该功能\n通过[修改禁言cd :seconds]可修改禁言冷却时间")
        else:
            mute_time, msg = await m10r_manager.one_go(event)
            await matcher.finish(msg)
    else:
        if cd > 0:
            await matcher.finish(f"技能冷却中，剩余 {cd}s\n需管理员通过[修改禁言cd :seconds]可修改禁言冷却时间")
        else:
            mute_time, msg = await m10r_manager.one_go(event)
            await matcher.send(msg)
            if mute_time > 0:
                is_botadmin = await is_BotAdmin(event.group_id)
                if not is_botadmin:
                    await matcher.finish("Bot没有群管权限呢，给个机会吧🤗")
                if is_SenderAdmin(event):
                    await matcher.finish("是管理员就嗯玩是吧？")
                else:
                    muting = muteSb(event.group_id, event.sender.user_id, mute_time)
                    async for muted in muting:
                        if muted:
                            try:
                                await muted
                            except ActionFailed:
                                await matcher.finish("出错啦，这次让你跑掉了~")
                            else:
                                logger.info(f"User {event.user_id} | Group {event.group_id} 禁言十连中奖 {mute_time} seconds")

@rank.handle()
async def _(event: GroupMessageEvent):
    gid = str(event.group_id)
    msg = await m10r_manager.day_rank(gid)
    await rank.finish(msg)

# 上周排行榜总结
@scheduler.scheduled_job("cron", day_of_week=0, hour=0, minute=0)
async def _():
    await m10r_manager.last_week_rank()

# 重置每日记录，且周一时重置每周记录
@scheduler.scheduled_job("cron", hour=0, minute=1)
async def _():
    m10r_manager.reset_record()
