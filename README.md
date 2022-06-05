<div align="center">

# Mute 10 Rolls

_🤐 禁言十连 🤐_

</div>

<p align="center">
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_mute10rolls/blob/beta/LICENSE">
    <img src="https://img.shields.io/github/license/MinatoAquaCrews/nonebot_plugin_mute10rolls?color=blue">
  </a>
  
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.2+-green">
  </a>
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_mute10rolls/releases/tag/v0.1.0">
    <img src="https://img.shields.io/github/v/release/MinatoAquaCrews/nonebot_plugin_mute10rolls?color=orange">
  </a>

  <a href="https://www.codefactor.io/repository/github/MinatoAquaCrews/nonebot_plugin_mute10rolls">
    <img src="https://img.shields.io/codefactor/grade/github/MinatoAquaCrews/nonebot_plugin_mute10rolls/beta?color=red">
  </a>
  
</p>

## 版本

v0.1.0a1

⚠ 适配nonebot2-2.0.0beta.2+

[更新日志](https://github.com/MinatoAquaCrews/nonebot_plugin_mute10rolls/releases/tag/v0.1.0)

## 安装

1. 通过`pip`或`nb`安装；

2. 数据会储存于同级目录下，设置`env`下`MUTE10ROLLS_PATH`更改数据路径，可更改默认的冷却时间及各禁言奖励的默认爆率：

    ```python
    MUTE10ROLLS_PATH="./data/m10r_data"
    MUTE_MISS_PROB=0.82
    MUTE_1MIN_PROB=0.10
    MUTE_2MIN_PROB=0.05
    MUTE_10MIN_PROB=0.016
    MUTE_30MIN_PROB=0.008
    MUTE_60MIN_PROB=0.004
    MUTE_120MIN_PROB=0.002
    DEFAULT_ROLL_CD=30      # 正式版/开启h时的冷却时间(秒)
    DEFAULT_TRIAL_CD=60     # 试用版/关闭时
    ```

## 功能

- [x] 十连抽取口球套餐，遵循**公开透明的概率分布**抽取禁言奖励；

- [x] [管理员权限] 管理功能、修改禁言冷却；

    ⚠ 注意：开启禁言十连功能使用正式版cd，BOT须有管理员权限才可禁言，否则仅抽奖。即使狗管理关闭禁言十连功能，依然能抽奖，此时使用体验版cd，且无论BOT有无管理员权限，均不可禁言

- [ ] TODO 禁言排行榜。

## 命令

1. 十连抽取口球套餐：[禁言十连]；

2. [管理员权限] 开启/关闭禁言十连：[开启|启用|关闭|禁用]禁言十连；

3. [管理员权限] 修改禁言冷却：[修改禁言cd/冷却][seconds]，例如：修改禁言cd 60。

    ⚠ 注意：冷却时间10~120，默认的体验版cd比正式版cd较长。建议管理员合理设置防止刷屏与抖M群友