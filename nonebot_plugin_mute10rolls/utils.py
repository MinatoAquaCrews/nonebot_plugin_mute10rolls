from .config import m10r_config, MUTE10ROLLS_PROB_LIST
from nonebot import get_bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from typing import AsyncGenerator, Coroutine, Any, Dict, Tuple, Union, Optional
from pathlib import Path
import random
import time
try:
    import ujson as json
except ModuleNotFoundError:
    import json
    
cd_data: Dict[str, int] = {}
data_path = m10r_config.mute10rolls_path / "m10r_data.json"
        
def init_data(gid: str) -> None:
    settings = load_json(data_path)
    if gid not in settings.keys():
        settings[gid] = {
            "enable": False,
            "roll_cd": m10r_config.default_roll_cd,
            "trial_cd": m10r_config.default_trial_cd
        }

        save_json(data_path, settings)
        
def check_enable(gid: str) -> bool:
    init_data(gid)
    
    settings = load_json(data_path)
    return settings[gid]["enable"]

def switch_enable(gid: str, new_state: bool) -> None:
    '''
        更改启用状态
    '''
    init_data(gid)
    
    settings = load_json(data_path)
    if settings[gid]["enable"] != new_state:
        clear_cd(gid)
    
    settings[gid]["enable"] = new_state
    
    save_json(data_path, settings)
    
def change_cd(gid: str, cd: int) -> None:
    '''
        修改当前模式下的cd
    '''
    init_data(gid)
    
    settings = load_json(data_path)
    if settings[gid]["enable"]:
        settings[gid]["roll_cd"] = cd
    else:
        settings[gid]["trial_cd"] = cd
    
    save_json(data_path, settings)

def add_cd(event: GroupMessageEvent, cooldown: int) -> None:
    cd_data[str(event.group_id)] = event.time + cooldown

def clear_cd(gid: str) -> None:
    cd_data.pop(gid)

def check_cd(gid: str) -> int:
    '''
        检查cd: 
        - OK则返回0
        - 冷却中，返回剩余时间(秒)
    '''
    try:
        rst_cd = int(cd_data[gid] - time.time())
    except KeyError:
        rst_cd = 0
    
    if rst_cd < 0:
        clear_cd(gid)
        
    return 0 if rst_cd <= 0 else rst_cd

async def one_go(event: GroupMessageEvent) -> Tuple[int, str]:
    '''
        一次禁言十连抽取
        :retval mute_total: 禁言总时长(秒)，大于0则中奖
        :retval msg: 抽取结果
    '''
    gid = str(event.group_id)
    settings = load_json(data_path)

    cooldown = settings[gid]["roll_cd"] if settings[gid]["enable"] else settings[gid]["trial_cd"]
    add_cd(event, cooldown)
    
    i = 1
    mute_total = 0
    msg = "禁言十连结果如下"
    result = random.choices([0, 1, 2, 10, 30, 60, 120], weights=MUTE10ROLLS_PROB_LIST, cum_weights=None, k=10)
    for roll in result:
        mute_total += roll
        cur_msg = "miss" if roll == 0 else f"{roll} min(s)"
        msg += f"\n{i} {cur_msg}"
        i = i + 1
        
    mute_total *= 60
    
    return mute_total, msg

async def muteSb(gid: int, mute_id: int, time: Optional[int]) -> AsyncGenerator[Coroutine, Any]:
    '''
        单人口球
        :param gid: 群号
        :param time: 时间 秒
        :param mute_id: qq
        :return:禁言操作
        未指定时间则随机
    '''
    if not time:
        time = random.randint(1, 3600)
        
    yield get_bot().set_group_ban(group_id=gid, user_id=mute_id, duration=time)      
       
async def is_BotAdmin(gid: int) -> bool:
    '''
        检查Bot是否有权限禁言
    '''
    info = await get_bot().get_group_member_info(group_id=gid, user_id=get_bot().self_id)
    return info["role"] != "member"

def is_SenderAdmin(event: GroupMessageEvent) -> bool:
    return event.sender.role != "member"

def save_json(file: Path, data: Dict[str, Union[bool, int]]) -> None:
    if file.exists():
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def load_json(file: Path) -> Dict[str, Union[bool, int]]:
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)