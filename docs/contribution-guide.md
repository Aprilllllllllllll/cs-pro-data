# 数据贡献指南

欢迎贡献 CS 职业选手资料！本文档说明如何手动添加或修改数据。

## 快速开始

### 1. 复制模板

```bash
# 添加新选手
cp data/templates/player_template.json data/players/<team_id>/<player_id>.json

# 添加新战队
cp data/templates/team_template.json data/players/<team_id>/_team.json
```

### 2. 填写数据

按照模板中的字段填写，每个字段的详细说明见 [data-schema.md](data-schema.md)。

### 3. 校验

```bash
bash scripts/validate.sh
```

确保没有 ERROR 级别的报错。WARNING 可以接受（如尚未创建的历史战队引用）。

### 4. 重建索引

```bash
bash scripts/build_index.sh
```

## 数据来源

| 优先级 | 网站 | 内容 | 方式 |
|--------|------|------|------|
| 1 | [Liquipedia](https://liquipedia.net/counterstrike/) | 基础信息、战队历史、成就 | 手动查找 |
| 2 | [ProSettings.net](https://prosettings.net/) | 外设、灵敏度、分辨率 | 手动查找 |
| 3 | [HLTV](https://www.hltv.org/) | 统计数据（Rating、ADR 等） | 手动查找 |
| 4 | [Esports Earnings](https://www.esportsearnings.com/) | 奖金数据 | 手动查找 |

## HLTV 数据手动采集

HLTV 有严格的反爬机制，请手动浏览采集：

### 选手页面
1. 打开 `https://www.hltv.org/player/<id>/<name>`
2. 页面顶部卡片 → 获取：Rating 2.0、KPR、DPR、Impact、ADR、KAST
3. "Statistics" 标签 → 获取：总地图数、总击杀数、爆头率
4. "Achievements" 区域 → 获取：Major 参赛次数、MVP 奖章
5. "Team History" 区域 → 获取：战队历史时间线

### 战队页面
1. 打开 `https://www.hltv.org/team/<id>/<name>`
2. 页面顶部 → 获取：HLTV 最高排名
3. "Roster" 区域 → 获取：当前阵容

## 字段填写规范

### 选手 ID
- 游戏别名全小写，如 `s1mple`、`zywoo`、`donk`
- 保持原始拼写，包括数字和特殊字符
- 如遇重名，加后缀区分，如 `niko-faze` 和 `niko-og`

### 国家代码
使用 [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) 两位代码：
- 乌克兰 → `UA`
- 法国 → `FR`
- 俄罗斯 → `RU`
- 丹麦 → `DK`
- 国际战队 → `international`

### 日期格式
统一使用 `YYYY-MM-DD` 格式，如 `2021-11-07`。

### 赛事级别
- `S-Tier`: Major、IEM Katowice、IEM Cologne、BLAST World Final 等
- `A-Tier`: ESL Pro League、BLAST Premier、IEM 其他站等
- `B-Tier`: 次级联赛和区域赛事

## 目录规范

- 选手文件放在 `data/players/<current_team_id>/` 下
- 文件名必须与选手 `id` 一致，如 `s1mple.json`
- 退役选手放在 `data/players/_retired/` 下
- 无战队选手放在 `data/players/_free_agents/` 下
- 战队信息文件固定命名为 `_team.json` 放在对应战队文件夹内

## 示例

完整示例请参考 data/players/ 目录下的已有数据：

- [s1mple](../data/players/navi/s1mple.json) — 完整选手资料示例
- [NAVI _team.json](../data/players/navi/_team.json) — 战队资料示例
- [donk](../data/players/spirit/donk.json) — 新星选手示例