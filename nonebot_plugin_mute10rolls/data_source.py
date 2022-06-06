from .config import m10r_config, MUTE10ROLLS_PROB_LIST
from nonebot import get_bot
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from typing import AsyncGenerator, Coroutine, Any, Dict, Tuple, Union, Optional
from pathlib import Path
import random
import datetime
import time
try:
    import ujson as json
except ModuleNotFoundError:
    import json

class M10R_Manager:
    
    def __init__(self):
        self.json_path: Path = m10r_config.mute10rolls_path / "m10r_data.json"
        self.cd_data: Dict[str, int] = {}
        
    def _init_data(self, gid: str) -> None:
        data = self._load_json()
        if gid not in data:
            data[gid] = dict()
            data[gid]["settings"] = {
                "enable": False,
                "roll_cd": m10r_config.default_roll_cd,
                "trial_cd": m10r_config.default_trial_cd
            }
            data[gid]["scores"] = {}

            self._save_json(data)
        
    def check_enable(self, gid: str) -> bool:
        self._init_data(gid)
        
        data = self._load_json()
        return data[gid]["settings"]["enable"]

    def switch_enable(self, gid: str, new_state: bool) -> None:
        '''
            更改启用状态
        '''
        self._init_data(gid)
        
        data = self._load_json()
        if data[gid]["settings"]["enable"] != new_state:
            self._clear_cd(gid)
        
        data[gid]["settings"]["enable"] = new_state
        
        self._save_json(data)
    
    def change_cd(self, gid: str, cd: int) -> None:
        '''
            修改当前模式下的cd
        '''
        self._init_data(gid)
        
        data = self._load_json()
        if data[gid]["settings"]["enable"]:
            data[gid]["settings"]["roll_cd"] = cd
        else:
            data[gid]["settings"]["trial_cd"] = cd
        
        self._save_json(data)

    def _add_cd(self, event: GroupMessageEvent, cooldown: int) -> None:
        self.cd_data[str(event.group_id)] = event.time + cooldown

    def _clear_cd(self, gid: str) -> None:
        self.cd_data.pop(gid)

    def check_cd(self, gid: str) -> int:
        '''
            检查cd: 
            - OK则返回0
            - 冷却中，返回剩余时间(秒)
        '''
        try:
            rst_cd = int(self.cd_data[gid] - time.time())
        except KeyError:
            rst_cd = 0
        
        if rst_cd < 0:
            self._clear_cd(gid)
            
        return 0 if rst_cd <= 0 else rst_cd

    def _mute_record(self, event: GroupMessageEvent, mute_time: int):
        gid = str(event.group_id)
        uid = str(event.user_id)
        
        data = self._load_json()
        if uid not in data[gid]["scores"].keys():
            data[gid]["scores"][uid] = {
                "day": {
                    "count": 1,
                    "max": mute_time,
                    "total": mute_time
                },
                "week": {
                    "count": 1,
                    "max": mute_time,
                    "total": mute_time
                }
            }
        else:
            data[gid]["scores"][uid]["day"]["count"] += 1
            data[gid]["scores"][uid]["day"]["total"] += mute_time
            data[gid]["scores"][uid]["week"]["count"] += 1
            data[gid]["scores"][uid]["week"]["total"] += mute_time
            if mute_time > data[gid]["scores"][uid]["day"]["max"]:
               data[gid]["scores"][uid]["day"]["max"] = mute_time
            
            if mute_time > data[gid]["scores"][uid]["week"]["max"]:
               data[gid]["scores"][uid]["week"]["max"] = mute_time 
        
        self._save_json(data)
    
    def _group_day_reset(self) -> None:
        data = self._load_json()
        for gid in data.keys():
            for uid in data[gid]["scores"].keys():
                data[gid]["scores"][uid]["day"]["count"] = 0
                data[gid]["scores"][uid]["day"]["max"] = 0
                data[gid]["scores"][uid]["day"]["total"] = 0
        
        self._save_json(data)
                
    def _group_week_reset(self) -> None:
        data = self._load_json()
        for gid in data.keys():
            for uid in data[gid]["scores"].keys():
                data[gid]["scores"][uid]["week"]["count"] = 0
                data[gid]["scores"][uid]["week"]["max"] = 0
                data[gid]["scores"][uid]["week"]["total"] = 0
                
        self._save_json(data)
    
    def reset_record(self) -> None:
        self._group_day_reset()
        if datetime.datetime.now().weekday() == 1:
            self._group_week_reset()
    
    async def day_rank(self, gid: str) -> MessageSegment:
        '''
            统计本日目前的数据
        '''
        data = self._load_json()
        msg: MessageSegment = ""
        
        if gid not in data or not bool(data[gid]["scores"]):
            # logger.warning()
            return MessageSegment.text("本日还没有统计数据呢~")
        
        for uid in data[gid]["scores"].keys():
            msg = MessageSegment.text("今日禁言统计数据\n")
            day_total: int = 0          # 今日总禁言
            day_count: int = 0          # 今日总次数    
            day_max_mute: int = 0       # 今日单次最长
            day_max_mute_uid: str = ""  # 今日单次最长uid

            day_count += data[gid]["scores"][uid]["day"]["count"]
            day_total += data[gid]["scores"][uid]["day"]["total"] 
            
            if day_max_mute < data[gid]["scores"][uid]["day"]["max"]:
                day_max_mute = data[gid]["scores"][uid]["day"]["max"]
                day_max_mute_uid = uid
        
        day_m, day_h = divmod(day_total, 60)
        max_m, max_h = divmod(day_max_mute, 60)
        
        bot = get_bot()
        dic = await bot.get_group_member_info(group_id=int(gid), user_id=int(day_max_mute_uid))
        mute_king = dic["nickname"] if not dic["card"] else dic["card"]
        
        msg += MessageSegment.text(f"今日禁言时长 {day_h}时{day_m}分，今日中奖次数 {day_count}\n")
        msg += MessageSegment.text(f"今日口球王为 {mute_king}，累计禁言时长 {max_h}时{max_m}分")
    
        return msg
        
    async def last_week_rank(self) -> None:
        '''
            统计本周数据及排行榜
            - 群禁言时间：各[uid]["week"]["total"]相加
            - 群禁言次数：各[uid]["week"]["count"]相加
            - 口球王：比较[uid]["week"]["total"]
            - 单次禁言时长最长：比较[uid]["week"]["max_mute"]
        '''
        data = self._load_json()
        msg: MessageSegment = ""
        
        if not bool(data):
            # logger.warning()
            return
        
        for gid in data.keys():
            if gid not in data or not bool(data[gid]["scores"]):
                # logger.warning()
                return

            msg = MessageSegment.text("周禁言统计数据\n")
            week_total: int = 0             # 上周群总禁言
            week_count: int = 0             # 周总禁言次数
            week_mute_king: int = 0         # 口球王禁言时长
            week_mute_king_uid: str = ""    # 口球王uid
            week_max_mute: int = 0          # 单次禁言最长
            
            for uid in data[gid]["scores"].keys():
                week_count += data[gid]["scores"][uid]["week"]["count"]
                week_total += data[gid]["scores"][uid]["week"]["total"]
                
                if week_mute_king < data[gid]["scores"][uid]["week"]["total"]:
                    week_mute_king = data[gid]["scores"][uid]["week"]["total"]
                    week_mute_king_uid = uid
                
                if week_max_mute < data[gid]["scores"][uid]["week"]["max"]:
                    week_max_mute = data[gid]["scores"][uid]["week"]["max"]
            
            week_m, week_h = divmod(week_total, 60)
            king_m, king_h = divmod(week_mute_king, 60)
            max_m, max_h = divmod(week_max_mute, 60)
            
            bot = get_bot()
            dic = await bot.get_group_member_info(group_id=int(gid), user_id=int(week_mute_king_uid))
            mute_king = dic["nickname"] if not dic["card"] else dic["card"]
            
            msg += MessageSegment.text(f"群累计禁言时长 {week_h}时{week_m}分，累计禁言中奖次数 {week_count}\n")
            msg += MessageSegment.text(f"群口球王为 {mute_king}，累计禁言时长 {king_h}时{king_m}分\n")
            msg += MessageSegment.text(f"单次禁言最长为 {max_h}时{max_m}分")
            
            # 群发
            await bot.send_group_msg(group_id=int(gid), message=msg)

    async def one_go(self, event: GroupMessageEvent) -> Tuple[int, str]:
        '''
            一次禁言十连抽取
            :retval mute_total: 禁言总时长(秒)，大于0则中奖
            :retval msg: 抽取结果
        '''
        gid = str(event.group_id)
        data = self._load_json()

        cooldown = data[gid]["settings"]["roll_cd"] if data[gid]["settings"]["enable"] else data[gid]["settings"]["trial_cd"]
        self._add_cd(event, cooldown)
        
        i = 1
        mute_total = 0
        msg = "禁言十连结果如下"
        result = random.choices([0, 1, 2, 10, 30, 60, 120], weights=MUTE10ROLLS_PROB_LIST, cum_weights=None, k=10)
        for roll in result:
            mute_total += roll
            if roll == 0:
                cur_msg = "miss"
            elif roll == 1:
                cur_msg = f"{roll} min"
            else:
                cur_msg = f"{roll} mins"
            msg += f"\n{i} {cur_msg}"
            i += 1
            
        mute_total *= 60
        
        # 开启功能才会记录
        if data[gid]["settings"]["enable"]:
            self._mute_record(event, mute_total)
        
        return mute_total, msg
    
    def _load_json(self) -> Dict[str, Dict[str, Union[Dict[str, Union[bool, int]], Dict[str, Dict[str, Dict[str, int]]]]]]:
        if self.json_path.exists():
            with open(self.json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        
    def _save_json(self, data: Dict[str, Dict[str, Union[Dict[str, Union[bool, int]], Dict[str, Dict[str, Dict[str, int]]]]]]) -> None:
        if self.json_path.exists():
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

m10r_manager = M10R_Manager()

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

