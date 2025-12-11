# type_query_app.py 使用说明

## 1. 功能简介

type_query_app.py 是一个支持宝可梦属性克制关系和宝可梦属性查询的命令行与函数调用工具。它具备如下功能：
- 查询任意属性（如“火”、“水”）的克制关系，包括克制、被克制、抵抗、免疫等分组。
- 查询任意宝可梦名称（如“妙蛙花”、“Charizard”）的属性及其克制关系。
- 支持多属性组合查询（如“火+飞行”），自动合并结果。
- 支持输入容错（如去除“系”、空格、大小写、别名、模糊匹配等）。
- 支持命令行和Python函数两种调用方式。
- 输出结构分组清晰，便于查阅和二次开发。

## 2. 输入类型说明

- **属性名称**：支持中文、英文、别名、带“系”后缀、大小写不敏感、空格自动忽略。例如：火、水、Fire、flying、草系。
- **宝可梦名称**：支持中文、英文、别名、部分模糊匹配。例如：妙蛙花、Charizard、喷火龙。
- **多属性组合**：用“+”或“/”或“,”分隔，顺序不限。例如：火+飞行、水/地面。
- **输入容错**：自动去除无关字符，支持常见别名和拼写错误的容错。

## 3. 命令行用法

```bash
python type_query_app.py <查询内容>
```

- 查询属性克制关系：
  ```bash
  python type_query_app.py 火
  python type_query_app.py "火+飞行"
  python type_query_app.py 水,地面
  ```
- 查询宝可梦属性及克制关系：
  ```bash
  python type_query_app.py 妙蛙花
  python type_query_app.py Charizard
  ```
- 支持多条批量查询（以空格分隔）：
  ```bash
  python type_query_app.py 火 水 妙蛙花
  ```
- 查看帮助：
  ```bash
  python type_query_app.py --help
  ```

## 4. Python 函数调用示例

```python
from type_query_app import query_type_relations, query_pokemon_relations

# 查询属性克制关系
result = query_type_relations(["火", "飞行"])
print(result)

# 查询宝可梦属性及克制关系
result = query_pokemon_relations("妙蛙花")
print(result)
```

- `query_type_relations(types: List[str]) -> dict`
- `query_pokemon_relations(name: str) -> dict`

## 5. 输入输出格式

### 5.1 输入参数
- 属性查询：属性列表（如["火", "飞行"]）或字符串（如"火+飞行"）。
- 宝可梦名称查询：宝可梦名称字符串。

### 5.2 输出结构
- 分组字段：
  - `克制`（super_effective）：本属性攻击哪些属性效果拔群
  - `被克制`（not_very_effective）：本属性攻击哪些属性效果减半
  - `无效`（no_effect）：本属性攻击哪些属性无效
  - `被克制于`（weak_to）：本属性被哪些属性攻击效果拔群
  - `抵抗`（resist）：本属性被哪些属性攻击效果减半
  - `免疫`（immune）：本属性被哪些属性攻击无效
- 宝可梦查询结果包含其属性及对应的克制关系。
- 多属性时，结果为所有属性的合并（如“火+飞行”）。

### 5.3 输出示例
```json
{
  "输入": "火+飞行",
  "属性": ["火", "飞行"],
  "克制": ["草", "虫", "冰", "格斗"],
  "被克制": ["岩石", "水", "电"],
  "抵抗": ["草", "虫", "钢", "火", "格斗"],
  "免疫": ["地面"]
}
```

## 6. 边界情况说明

- **无效输入**：返回错误提示及建议。例如输入“未知属性”或“xxx”。
- **未知宝可梦**：返回未找到提示。
- **组合属性无交集**：如“火+水”无共同克制，返回空列表。
- **输入为空**：返回帮助信息。
- **别名/模糊匹配失败**：返回最相近的匹配建议。

## 7. 数据文件依赖

- 依赖 `pokemon_type_chart.json` 和 `pokemon_name_type_map.json` 数据文件，需与脚本同目录。

## 8. 其他说明

- 支持扩展属性、别名、语言映射，便于后续维护。
- 代码结构清晰，注释完善，便于二次开发。
- 详细查询逻辑见 `type_query_logic.md`。

