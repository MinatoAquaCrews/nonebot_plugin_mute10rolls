<div align="center">

# Mute 10 Rolls

_ð¤ ç¦è¨åè¿ ð¤_

</div>

<p align="center">
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_mute10rolls/blob/beta/LICENSE">
    <img src="https://img.shields.io/github/license/MinatoAquaCrews/nonebot_plugin_mute10rolls?color=blue">
  </a>
  
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.2+-green">
  </a>
  
  <a href="https://github.com/MinatoAquaCrews/nonebot_plugin_mute10rolls/releases/tag/v0.1.0a2">
    <img src="https://img.shields.io/github/v/release/MinatoAquaCrews/nonebot_plugin_mute10rolls?color=orange">
  </a>

  <a href="https://www.codefactor.io/repository/github/MinatoAquaCrews/nonebot_plugin_mute10rolls">
    <img src="https://img.shields.io/codefactor/grade/github/MinatoAquaCrews/nonebot_plugin_mute10rolls/beta?color=red">
  </a>
  
</p>

## çæ¬

v0.1.0a2

â  éénonebot2-2.0.0beta.2+

[æ´æ°æ¥å¿](https://github.com/MinatoAquaCrews/nonebot_plugin_mute10rolls/releases/tag/v0.1.0a2)

## å®è£

1. éè¿`pip`æ`nb`å®è£ï¼

2. æ°æ®ä¼å¨å­äºåçº§ç®å½ä¸ï¼è®¾ç½®`env`ä¸`MUTE10ROLLS_PATH`æ´æ¹æ°æ®è·¯å¾ï¼å¯æ´æ¹é»è®¤çå·å´æ¶é´ååç¦è¨å¥å±çé»è®¤ççï¼

    ```python
    MUTE10ROLLS_PATH="./data/m10r_data"
    MUTE_MISS_PROB=0.82
    MUTE_1MIN_PROB=0.10
    MUTE_2MIN_PROB=0.05
    MUTE_10MIN_PROB=0.016
    MUTE_30MIN_PROB=0.008
    MUTE_60MIN_PROB=0.004
    MUTE_120MIN_PROB=0.002
    DEFAULT_ROLL_CD=30      # æ­£å¼ç/å¼å¯æ¶çå·å´æ¶é´(ç§)
    DEFAULT_TRIAL_CD=60     # è¯ç¨ç/å³é­æ¶
    ```

## åè½

- [x] åè¿æ½åå£çå¥é¤ï¼éµå¾ªå¬å¼éæçæ¦çåå¸æ½åç¦è¨å¥å±ï¼

- [x] [ç®¡çåæé] ç®¡çåè½ãä¿®æ¹ç¦è¨å·å´ï¼

    â  æ³¨æï¼å¼å¯ç¦è¨åè¿åè½ä½¿ç¨æ­£å¼çcdï¼BOTé¡»æç®¡çåæéæå¯ç¦è¨ï¼å¦åä»æ½å¥ãå³ä½¿çç®¡çå³é­ç¦è¨åè¿åè½ï¼ä¾ç¶è½æ½å¥ï¼æ­¤æ¶ä½¿ç¨ä½éªçcdï¼ä¸æ è®ºBOTææ ç®¡çåæéï¼åä¸å¯ç¦è¨

- [x] ç»è®¡æ¬æ¥ç¾¤ç¦è¨æ°æ®ï¼æ¯å¨èªå¨åå¸ä¸å¨ç¾¤ç¦è¨æ°æ®ã

## å½ä»¤

1. åè¿æ½åå£çå¥é¤ï¼[ç¦è¨åè¿]ï¼

2. æ¥çæ¬æ¥ç¾¤ç¦è¨æ°æ®ç»è®¡ï¼[ç¦è¨ç»è®¡]ï¼

3. [ç®¡çåæé] å¼å¯/å³é­ç¦è¨åè¿ï¼[å¼å¯|å¯ç¨|å³é­|ç¦ç¨]ç¦è¨åè¿ï¼

    â  æ³¨æï¼åå§ç¶æä¸ï¼ç¾¤ç¦è¨åè¿åè½é»è®¤å³é­ã

4. [ç®¡çåæé] ä¿®æ¹ç¦è¨å·å´ï¼[ä¿®æ¹ç¦è¨cd/å·å´][seconds]ï¼ä¾å¦ï¼ä¿®æ¹ç¦è¨cd 60ã

    â  æ³¨æï¼å·å´æ¶é´10~120ï¼é»è®¤ä½éªçcdæ¯æ­£å¼çcdè¾é¿ãå»ºè®®ç®¡çååçè®¾ç½®é²æ­¢å·å±ä¸æMç¾¤å