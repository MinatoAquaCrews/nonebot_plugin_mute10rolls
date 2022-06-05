import nonebot
from pydantic import BaseModel, Extra
from typing import List
from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json
    
class Mute10RollsConfig(BaseModel, extra=Extra.ignore):

    mute10rolls_path: Path = Path(__file__).parent
    mute_miss_prob: float = 0.82
    mute_1min_prob: float = 0.10
    mute_2min_prob: float = 0.05
    mute_10min_prob: float = 0.016
    mute_30min_prob: float = 0.008
    mute_60min_prob: float = 0.004
    mute_120min_prob: float = 0.002
    
    default_roll_cd: int = 30   # 开启功能下的cd
    default_trial_cd: int = 60  # 关闭功能下的体验cd
    
driver = nonebot.get_driver()
global_config = driver.config
m10r_config: Mute10RollsConfig = Mute10RollsConfig.parse_obj(global_config.dict())
MUTE10ROLLS_PROB_LIST: List[float] = [
	m10r_config.mute_miss_prob,
	m10r_config.mute_1min_prob,
	m10r_config.mute_2min_prob,
	m10r_config.mute_10min_prob,
	m10r_config.mute_30min_prob,
	m10r_config.mute_60min_prob,
    m10r_config.mute_120min_prob
]

@driver.on_startup
async def config_check():    
    data_path: Path = m10r_config.mute10rolls_path / "m10r_data.json"
    if not data_path.exists():
        with open(data_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(dict()))
            f.close()