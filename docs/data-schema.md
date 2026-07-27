# CS 职业选手资料库 — 数据 Schema 说明

## 目录结构

```
data/
├── players/                    # 选手资料，按当前战队文件夹分类
│   ├── <team_id>/              # 战队文件夹名 = team_id
│   │   ├── _team.json          # 该战队自身信息
│   │   ├── <player_id>.json    # 选手资料文件
│   │   └── ...
│   ├── _retired/               # 退役选手
│   └── _free_agents/           # 无战队选手
├── index.json                  # 自动生成的全局索引（禁止手动编辑）
└── templates/                  # 人工填写模板
    ├── player_template.json
    └── team_template.json
```

## 选手 JSON Schema

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 选手唯一 ID，游戏别名全小写，如 `s1mple`、`zywoo` |
| `name` | string | ✅ | 真实姓名（英文），如 `Oleksandr Kostyliev` |
| `native_name` | string \| null | ❌ | 母语姓名 |
| `country` | string | ✅ | ISO 3166-1 alpha-2 两位国家代码，如 `UA`、`FR` |
| `country_name` | string | ✅ | 国家英文名，如 `Ukraine` |
| `birth_date` | string \| null | ❌ | 出生日期，格式 `YYYY-MM-DD` |
| `status` | enum | ✅ | `active` / `inactive` / `retired` / `banned` |
| `roles` | enum[] | ❌ | `AWPer` / `IGL` / `Entry` / `Support` / `Rifler` / `Lurker` / `Coach` |
| `years_active` | string \| null | ❌ | 活跃年份范围，如 `2013-present` |

### current_team

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `team_id` | string | ✅ | 当前战队 ID |
| `join_date` | string | ✅ | 入队日期，格式 `YYYY-MM-DD` |
| `contract_expiry` | string \| null | ❌ | 合同到期日 |

### team_history[] 

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `team_id` | string | ✅ | 历史战队 ID |
| `start_date` | string | ✅ | 入队日期 |
| `end_date` | string \| null | ❌ | 离队日期，仍在队填 `null` |
| `status` | enum | ❌ | `starter` / `substitute` / `stand-in` / `loan` |

### major_titles[]

| 字段 | 类型 | 说明 |
|------|------|------|
| `major_name` | string | Major 赛事全名 |
| `date` | string | 夺冠日期 |
| `team_id` | string | 夺冠时所属战队 |
| `placement` | string | 名次，冠军为 `1st` |

### statistics

| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `hltv_rating` | float \| null | HLTV Rating 2.0 | HLTV |
| `total_maps` | int \| null | 总地图数 | HLTV |
| `total_kills` | int \| null | 总击杀数 | HLTV |
| `headshot_percentage` | float \| null | 爆头率 % | HLTV |
| `kills_per_round` | float \| null | 每回合击杀 KPR | HLTV |
| `deaths_per_round` | float \| null | 每回合死亡 DPR | HLTV |
| `impact_rating` | float \| null | 影响力评分 | HLTV |
| `kast` | float \| null | KAST % | HLTV |
| `adr` | float \| null | 每回合伤害 ADR | HLTV |

### settings（游戏设置与外设）

| 字段 | 类型 | 说明 | 来源 |
|------|------|------|------|
| `sensitivity` | float \| null | 鼠标灵敏度 | ProSettings |
| `edpi` | float \| null | 有效 DPI | ProSettings |
| `resolution` | string \| null | 分辨率，如 `1280x960` | ProSettings |
| `aspect_ratio` | string \| null | 宽高比，如 `4:3` | ProSettings |
| `scaling_mode` | string \| null | `Stretched` / `Black Bars` / `Native` | ProSettings |
| `monitor` | string \| null | 显示器型号 | ProSettings |
| `mouse` | string \| null | 鼠标型号 | ProSettings |
| `keyboard` | string \| null | 键盘型号 | ProSettings |
| `headset` | string \| null | 耳机型号 | ProSettings |
| `mousepad` | string \| null | 鼠标垫型号 | ProSettings |

### 元数据

| 字段 | 类型 | 说明 |
|------|------|------|
| `last_updated` | string | ISO 8601 格式更新时间 |
| `sources` | string[] | 数据来源：`liquipedia` / `prosettings` / `hltv_manual` / `esl` / `blast` |
| `notes` | string \| null | 备注 |

---

## 战队 JSON Schema

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 战队唯一 ID，全小写 |
| `name` | string | ✅ | 战队全名 |
| `short_name` | string \| null | ❌ | 缩写 |
| `country` | string | ✅ | 国家代码或 `international` |
| `country_name` | string | ✅ | 国家英文名 |
| `region` | enum | ✅ | `EU` / `NA` / `SA` / `CIS` / `ASIA` / `OCE` / `MEA` |
| `founded` | string \| null | ❌ | 成立年份 |
| `status` | enum | ✅ | `active` / `inactive` / `disbanded` |
| `current_roster` | string[] | ❌ | 当前阵容选手 ID 列表 |
| `coach` | string \| null | ❌ | 教练 ID |
| `achievements.major_titles` | int | ❌ | Major 冠军数 |
| `achievements.major_appearances` | int | ❌ | Major 参赛次数 |
| `achievements.s_tier_titles` | int | ❌ | S 级赛事冠军数 |
| `achievements.hltv_ranking_best` | int \| null | ❌ | HLTV 最高排名 |

---

## 索引文件 `data/index.json`

由 `scripts/build_index.sh` 自动生成，提供：

- **正向索引**：`players.<id>` → 文件路径 + 摘要信息
- **反向索引**：
  - `by_country` — 按国家代码分组
  - `by_role` — 按角色分组
  - `by_status` — 按状态分组
- **统计**：`player_count`、`team_count`

## 校验流程

运行 `bash scripts/validate.sh` 执行四层校验：

1. **结构验证** — JSON 可解析 + Pydantic 模型校验
2. **语义验证** — 枚举值、日期、国家代码合法性
3. **交叉引用** — 选手与战队之间的 team_id / roster 引用完整性
4. **一致性验证** — 文件名与 id 匹配、文件夹与 current_team 匹配