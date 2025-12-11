# type_query_app.py
"""
宝可梦属性克制关系与属性查询主程序
- 支持属性和宝可梦名称的克制关系查询
- 支持命令行和函数调用两种方式
- 代码结构清晰，注释完善
"""
import os
import sys
import json
import argparse

class TypeQueryApp:
    """
    宝可梦属性克制关系查询主类
    负责加载数据、初始化、分发查询请求
    """
    def __init__(self, type_chart_path='pokemon_type_chart.json', name_type_map_path='pokemon_name_type_map.json'):
        self.type_chart = self._load_json(type_chart_path)
        self.name_type_map = self._load_json(name_type_map_path)
        # 预留：初始化标准化、别名映射等

    def _load_json(self, path):
        """加载JSON文件"""
        if not os.path.exists(path):
            print(f"[错误] 数据文件不存在: {path}", file=sys.stderr)
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def query_by_type(self, type_names):
        """
        按属性查询克制关系
        :param type_names: list[str]，属性名称列表
        :return: 查询结果（占位）
        """
        # TODO: 实现具体查询逻辑
        print(f"[占位] 按属性查询: {type_names}")
        return {}

    def query_by_name(self, pokemon_names):
        """
        按宝可梦名称查询属性及克制关系
        :param pokemon_names: list[str]，宝可梦名称列表
        :return: 查询结果（占位）
        """
        # TODO: 实现具体查询逻辑
        print(f"[占位] 按宝可梦名称查询: {pokemon_names}")
        return {}

    def query(self, types=None, names=None):
        """
        综合查询接口，支持属性和宝可梦名称
        :param types: list[str]，属性名称列表
        :param names: list[str]，宝可梦名称列表
        :return: 查询结果（占位）
        """
        if types:
            return self.query_by_type(types)
        elif names:
            return self.query_by_name(names)
        else:
            print("[错误] 未指定查询类型或宝可梦名称", file=sys.stderr)
            return None

def main():
    """
    命令行入口，支持属性和宝可梦名称查询
    """
    parser = argparse.ArgumentParser(description='宝可梦属性克制关系与属性查询工具')
    parser.add_argument('-t', '--type', nargs='+', help='属性名称（可多个）')
    parser.add_argument('-n', '--name', nargs='+', help='宝可梦名称（可多个）')
    parser.add_argument('--type_chart', default='pokemon_type_chart.json', help='属性克制关系数据文件路径')
    parser.add_argument('--name_type_map', default='pokemon_name_type_map.json', help='宝可梦名称与属性映射数据文件路径')
    args = parser.parse_args()

    app = TypeQueryApp(type_chart_path=args.type_chart, name_type_map_path=args.name_type_map)
    result = app.query(types=args.type, names=args.name)
    print("查询结果：", result)

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
type_query_app.py

宝可梦属性克制关系查询工具
支持属性查询（单属性、多属性组合），返回克制、被克制等分组结果。

数据文件依赖：pokemon_type_chart.json

主要功能：
- 属性名标准化处理
- 属性克制关系查询
- 多属性组合结果合并
- 结构清晰，注释完善

后续可扩展：宝可梦名称查询、命令行接口、函数接口等
"""

import json
import os
from typing import List, Dict, Any, Set

# 数据文件路径
TYPE_CHART_FILE = "pokemon_type_chart.json"

# 属性别名映射，可扩展
TYPE_ALIASES = {
    # 中文
    "一般": ["一般", "普通", "normal"],
    "格斗": ["格斗", "格鬥", "fight", "fighting"],
    "飞行": ["飞行", "飛行", "flying"],
    "毒": ["毒", "poison"],
    "地面": ["地面", "地", "ground"],
    "岩石": ["岩石", "岩", "rock"],
    "虫": ["虫", "蟲", "bug"],
    "幽灵": ["幽灵", "幽靈", "ghost"],
    "钢": ["钢", "鋼", "steel"],
    "火": ["火", "fire"],
    "水": ["水", "water"],
    "草": ["草", "grass"],
    "电": ["电", "電", "electric"],
    "超能力": ["超能力", "超能", "超", "psychic"],
    "冰": ["冰", "ice"],
    "龙": ["龙", "龍", "dragon"],
    "恶": ["恶", "惡", "dark"],
    "妖精": ["妖精", "fairy"],
}

# 反向映射：别名->标准属性
ALIAS_TO_TYPE = {}
for std_type, aliases in TYPE_ALIASES.items():
    for alias in aliases:
        ALIAS_TO_TYPE[alias.lower()] = std_type
        # 支持去除“系”后缀
        if alias.endswith("系"):
            ALIAS_TO_TYPE[alias[:-1].lower()] = std_type

# 属性标准化处理
def normalize_type(type_name: str) -> str:
    """
    标准化属性名，支持去除“系”、空格、大小写、别名等
    """
    t = type_name.strip().replace("系", "").replace(" ", "").lower()
    return ALIAS_TO_TYPE.get(t, None)

# 读取属性克制数据
def load_type_chart(file_path: str = TYPE_CHART_FILE) -> List[Dict[str, Any]]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到数据文件: {file_path}")
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    return data

# 构建属性到克制关系的映射
_TYPE_CHART = None
_TYPE_INDEX = None

def get_type_chart():
    global _TYPE_CHART, _TYPE_INDEX
    if _TYPE_CHART is None or _TYPE_INDEX is None:
        _TYPE_CHART = load_type_chart()
        _TYPE_INDEX = {item["属性"]: item for item in _TYPE_CHART}
    return _TYPE_INDEX

# 属性查询主函数

def query_type_relations(type_names: List[str]) -> Dict[str, Set[str]]:
    """
    输入属性名列表，返回克制、被克制等分组结果（去重合并）
    :param type_names: 属性名或别名列表
    :return: dict, 分组为：克制、被克制
    """
    type_index = get_type_chart()
    std_types = []
    for t in type_names:
        std = normalize_type(t)
        if std is None:
            raise ValueError(f"无效属性名: {t}")
        std_types.append(std)
    result = {"克制": set(), "被克制": set()}
    for std in std_types:
        info = type_index.get(std)
        if not info:
            continue
        result["克制"].update(info.get("克制", []))
        result["被克制"].update(info.get("被克制", []))
    # 去除自身
    for group in result:
        result[group] -= set(std_types)
    return result

# 示例用法
if __name__ == "__main__":
    print("宝可梦属性克制关系查询示例：")
    try:
        # 示例1：单属性
        res1 = query_type_relations(["火"])
        print("火属性：", {k: list(v) for k, v in res1.items()})
        # 示例2：多属性
        res2 = query_type_relations(["火", "飞行"])
        print("火+飞行属性：", {k: list(v) for k, v in res2.items()})
    except Exception as e:
        print("查询出错：", e)

"""
# 主要接口说明：
# query_type_relations(type_names: List[str]) -> Dict[str, Set[str]]
# 输入：属性名或别名列表
# 输出：dict，分组为“克制”、“被克制”，结果为去重后的属性集合
#
# 后续可扩展：
# - 支持抵抗、免疫等分组
# - 宝可梦名称查询
# - 命令行参数解析
# - 函数接口
# - 多语言和别名增强
"""

# 宝可梦属性克制关系与名称查询功能实现
import json
import os
import re
from typing import List, Dict, Any, Optional

# 数据文件路径（可根据实际情况调整）
TYPE_CHART_PATH = 'pokemon_type_chart.json'
NAME_TYPE_MAP_PATH = 'pokemon_name_type_map.json'

# 加载属性克制关系表
with open(TYPE_CHART_PATH, 'r', encoding='utf-8') as f:
    TYPE_CHART = json.load(f)

# 加载宝可梦名称到属性映射表
with open(NAME_TYPE_MAP_PATH, 'r', encoding='utf-8') as f:
    NAME_TYPE_MAP = json.load(f)

# 别名映射（可扩展，示例）
ALIAS_MAP = {
    '皮卡丘': ['Pikachu', 'ピカチュウ', '皮卡丘'],
    '妙蛙种子': ['Bulbasaur', 'フシギダネ', '妙蛙种子'],
    # 可继续补充
}

# 属性标准化映射（去除“系”、空格、大小写、别名等）
TYPE_ALIAS = {
    '火': ['火', '火系', 'Fire', 'ほのお'],
    '水': ['水', '水系', 'Water', 'みず'],
    '草': ['草', '草系', 'Grass', 'くさ'],
    # 可继续补充
}

def standardize_name(name: str) -> Optional[str]:
    """
    标准化宝可梦名称，支持多语言、别名、去除空格、大小写等。
    返回标准化后的名称（与NAME_TYPE_MAP主键一致），找不到则返回None。
    """
    name = name.strip().lower()
    # 直接查找
    for key in NAME_TYPE_MAP:
        if name == key.lower():
            return key
    # 别名查找
    for std_name, aliases in ALIAS_MAP.items():
        for alias in aliases:
            if name == alias.strip().lower():
                return std_name
    # 模糊匹配（如去除空格、特殊字符）
    name_clean = re.sub(r'\s+', '', name)
    for key in NAME_TYPE_MAP:
        if name_clean == re.sub(r'\s+', '', key.lower()):
            return key
    # 未找到
    return None

def get_types_by_name(name: str) -> Optional[List[str]]:
    """
    根据宝可梦名称查询属性，支持多语言和别名。
    返回属性列表，找不到则返回None。
    """
    std_name = standardize_name(name)
    if std_name and std_name in NAME_TYPE_MAP:
        types = NAME_TYPE_MAP[std_name]
        if isinstance(types, str):
            return [types]
        elif isinstance(types, list):
            return types
    return None

def standardize_type(type_name: str) -> Optional[str]:
    """
    标准化属性名称，支持多语言、别名、去除“系”、空格、大小写等。
    返回标准化后的属性主键，找不到则返回None。
    """
    type_name = type_name.strip().lower().replace('系', '')
    for std_type, aliases in TYPE_ALIAS.items():
        for alias in aliases:
            if type_name == alias.strip().lower().replace('系', ''):
                return std_type
    # 模糊匹配
    type_clean = re.sub(r'\s+', '', type_name)
    for std_type, aliases in TYPE_ALIAS.items():
        for alias in aliases:
            if type_clean == re.sub(r'\s+', '', alias.strip().lower().replace('系', '')):
                return std_type
    return None

def query_type_relations(types: List[str]) -> Dict[str, Any]:
    """
    查询属性的克制关系，支持多属性组合。
    返回分组结果：克制、被克制、抵抗、免疫。
    """
    result = {
        '克制': set(),
        '被克制': set(),
        '抵抗': set(),
        '免疫': set()
    }
    for t in types:
        std_type = standardize_type(t)
        if std_type and std_type in TYPE_CHART:
            chart = TYPE_CHART[std_type]
            for group in result:
                result[group].update(chart.get(group, []))
    # 转为列表并去重
    for group in result:
        result[group] = sorted(list(result[group]))
    return result

def query_pokemon_by_name(name: str) -> Dict[str, Any]:
    """
    宝可梦名称查询主函数。
    输入名称，返回属性及其克制分组结果。
    """
    types = get_types_by_name(name)
    if not types:
        return {
            '名称': name,
            '属性': [],
            '结果': None,
            '提示': '未找到该宝可梦名称或属性信息，请检查输入是否正确。'
        }
    relations = query_type_relations(types)
    return {
        '名称': name,
        '属性': types,
        '结果': relations,
        '提示': ''
    }

# 命令行接口示例
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='宝可梦属性克制关系与名称查询工具')
    parser.add_argument('--name', type=str, help='宝可梦名称（支持多语言、别名）')
    args = parser.parse_args()
    if args.name:
        res = query_pokemon_by_name(args.name)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print('请使用 --name 参数输入宝可梦名称进行查询。')

"""
使用说明：
1. 支持通过 query_pokemon_by_name(name) 函数调用，输入宝可梦名称，返回属性及克制分组结果。
2. 支持命令行方式：python type_query_app.py --name 皮卡丘
3. 输入支持多语言、别名、模糊匹配。
4. 输出分组包括：克制、被克制、抵抗、免疫。
5. 数据文件需与脚本同目录，或调整路径。
6. 代码结构清晰，便于扩展属性查询、批量查询等功能。
"""

# --- 输入标准化与容错处理模块 ---
"""
本模块用于对宝可梦属性和宝可梦名称的输入进行标准化处理，支持多语言、别名、去除“系”、空格、大小写等，保证所有查询逻辑的输入都能被统一识别。
"""

import re

# 属性别名和多语言映射表（可扩展）
POKEMON_TYPE_ALIASES = {
    '火': ['火', '火系', 'fire', '炎', '炎系', 'ほのお', 'ひのこ'],
    '水': ['水', '水系', 'water', 'みず'],
    '草': ['草', '草系', 'grass', 'くさ'],
    '电': ['电', '电系', '雷', '雷系', 'electric', 'でんき'],
    '冰': ['冰', '冰系', 'ice', 'こおり'],
    '格斗': ['格斗', '格斗系', 'fight', 'fighting', 'かくとう'],
    '毒': ['毒', '毒系', 'poison', 'どく'],
    '地面': ['地面', '地面系', 'ground', 'じめん'],
    '飞行': ['飞行', '飞行系', 'flying', 'ひこう'],
    '超能': ['超能', '超能力', '超能系', 'psychic', 'エスパー'],
    '虫': ['虫', '虫系', 'bug', 'むし'],
    '岩石': ['岩石', '岩石系', 'rock', 'いわ'],
    '幽灵': ['幽灵', '幽灵系', 'ghost', 'ゴースト'],
    '龙': ['龙', '龙系', 'dragon', 'ドラゴン'],
    '恶': ['恶', '恶系', 'dark', 'あく'],
    '钢': ['钢', '钢系', 'steel', 'はがね'],
    '妖精': ['妖精', '妖精系', 'fairy', 'フェアリー'],
    '一般': ['一般', '一般系', 'normal', 'ノーマル']
}

# 宝可梦名称别名和多语言映射表（示例，实际可从pokemon_name_type_map.json加载）
POKEMON_NAME_ALIASES = {
    '喷火龙': ['喷火龙', 'Charizard', 'リザードン', '火焰龙'],
    '皮卡丘': ['皮卡丘', 'Pikachu', 'ピカチュウ'],
    '妙蛙花': ['妙蛙花', 'Venusaur', 'フシギバナ'],
    '水箭龟': ['水箭龟', 'Blastoise', 'カメックス'],
    '火焰鸟': ['火焰鸟', 'Moltres', 'ファイヤー'],
    # ... 更多宝可梦
}

# 反向映射：别名 -> 标准属性
TYPE_ALIAS_TO_STANDARD = {}
for std_type, aliases in POKEMON_TYPE_ALIASES.items():
    for alias in aliases:
        TYPE_ALIAS_TO_STANDARD[alias.lower()] = std_type

# 反向映射：别名 -> 标准宝可梦名称
NAME_ALIAS_TO_STANDARD = {}
for std_name, aliases in POKEMON_NAME_ALIASES.items():
    for alias in aliases:
        NAME_ALIAS_TO_STANDARD[alias.lower()] = std_name


def standardize_type_input(type_input):
    """
    对属性输入进行标准化处理，支持多语言、别名、去除“系”、空格、大小写等。
    返回标准属性名（如“火”、“水”），无效输入返回None。
    """
    if not isinstance(type_input, str):
        return None
    # 去除空格、特殊字符、大小写
    clean = re.sub(r'[\s\-]', '', type_input).lower()
    # 去除“系”字
    clean = clean.replace('系', '')
    # 查找标准属性
    return TYPE_ALIAS_TO_STANDARD.get(clean, None)


def standardize_name_input(name_input):
    """
    对宝可梦名称输入进行标准化处理，支持多语言、别名、空格、大小写等。
    返回标准宝可梦名称（如“皮卡丘”、“喷火龙”），无效输入返回None。
    """
    if not isinstance(name_input, str):
        return None
    clean = re.sub(r'[\s\-]', '', name_input).lower()
    return NAME_ALIAS_TO_STANDARD.get(clean, None)


def standardize_multi_type_input(type_inputs):
    """
    支持多属性组合输入，返回标准属性列表。
    输入可以是字符串（逗号/空格分隔）或列表。
    """
    if isinstance(type_inputs, str):
        # 支持逗号、空格分隔
        items = re.split(r'[，,\s]+', type_inputs)
    elif isinstance(type_inputs, list):
        items = type_inputs
    else:
        return []
    result = []
    for item in items:
        std = standardize_type_input(item)
        if std and std not in result:
            result.append(std)
    return result


def standardize_multi_name_input(name_inputs):
    """
    支持多宝可梦名称组合输入，返回标准名称列表。
    输入可以是字符串（逗号/空格分隔）或列表。
    """
    if isinstance(name_inputs, str):
        items = re.split(r'[，,\s]+', name_inputs)
    elif isinstance(name_inputs, list):
        items = name_inputs
    else:
        return []
    result = []
    for item in items:
        std = standardize_name_input(item)
        if std and std not in result:
            result.append(std)
    return result

# --- 以上为输入标准化与容错处理模块，供后续查询逻辑调用 ---

"""
用法说明：
- standardize_type_input(type_input): 输入任意属性别名或多语言，返回标准属性名。
- standardize_name_input(name_input): 输入任意宝可梦名称别名或多语言，返回标准名称。
- standardize_multi_type_input(type_inputs): 输入多属性（字符串或列表），返回标准属性列表。
- standardize_multi_name_input(name_inputs): 输入多宝可梦名称（字符串或列表），返回标准名称列表。
"""

# type_query_app.py
"""
宝可梦属性克制关系与属性查询工具
支持命令行和函数调用两种方式，支持属性和宝可梦名称的克制关系查询，具备输入容错、多属性组合，分组清晰，代码结构规范，注释完善。
"""
import argparse
import json
import os
import sys
from typing import List, Dict, Any, Union

# 数据文件路径（假定与脚本同目录）
TYPE_CHART_FILE = os.path.join(os.path.dirname(__file__), 'pokemon_type_chart.json')
NAME_TYPE_MAP_FILE = os.path.join(os.path.dirname(__file__), 'pokemon_name_type_map.json')

# 加载数据文件
def load_json(file_path: str) -> Any:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

type_chart = load_json(TYPE_CHART_FILE)
name_type_map = load_json(NAME_TYPE_MAP_FILE)

# 属性标准化映射（可扩展，支持多语言、别名）
TYPE_ALIASES = {
    '火': ['火', '火系', 'fire'],
    '水': ['水', '水系', 'water'],
    '草': ['草', '草系', 'grass'],
    '电': ['电', '电系', 'electric'],
    '冰': ['冰', '冰系', 'ice'],
    '格斗': ['格斗', '格斗系', 'fighting'],
    '毒': ['毒', '毒系', 'poison'],
    '地面': ['地面', '地面系', 'ground'],
    '飞行': ['飞行', '飞行系', 'flying'],
    '超能': ['超能', '超能系', 'psychic'],
    '虫': ['虫', '虫系', 'bug'],
    '岩石': ['岩石', '岩石系', 'rock'],
    '幽灵': ['幽灵', '幽灵系', 'ghost'],
    '龙': ['龙', '龙系', 'dragon'],
    '恶': ['恶', '恶系', 'dark'],
    '钢': ['钢', '钢系', 'steel'],
    '妖精': ['妖精', '妖精系', 'fairy'],
    '一般': ['一般', '一般系', 'normal']
}

# 反向映射：别名->标准属性
def build_type_alias_map(type_aliases: Dict[str, List[str]]) -> Dict[str, str]:
    alias_map = {}
    for std_type, aliases in type_aliases.items():
        for alias in aliases:
            alias_map[alias.lower()] = std_type
    return alias_map

TYPE_ALIAS_MAP = build_type_alias_map(TYPE_ALIASES)

# 输入标准化处理
def normalize_type(type_name: str) -> Union[str, None]:
    """
    标准化属性输入，支持多语言、别名、去除“系”、空格、大小写
    """
    t = type_name.strip().replace('系', '').lower()
    return TYPE_ALIAS_MAP.get(t, None)

def normalize_types(type_names: List[str]) -> List[str]:
    result = []
    for t in type_names:
        std = normalize_type(t)
        if std:
            result.append(std)
    return result

# 宝可梦名称标准化（支持别名、大小写、空格）
def normalize_pokemon_name(name: str) -> str:
    return name.strip().lower()

# 查询属性克制关系
def query_type_relations(types: List[str]) -> Dict[str, List[str]]:
    """
    输入属性列表，输出分组结果：克制、被克制、抵抗、免疫
    多属性时合并结果（取并集/交集，具体见type_query_logic.md）
    """
    result = {
        '克制': set(),
        '被克制': set(),
        '抵抗': set(),
        '免疫': set()
    }
    for t in types:
        if t not in type_chart:
            continue
        chart = type_chart[t]
        for k in result.keys():
            result[k].update(chart.get(k, []))
    # 转为列表并去重
    for k in result:
        result[k] = sorted(list(result[k]))
    return result

# 查询宝可梦名称对应属性及其克制关系
def query_pokemon_relations(name: str) -> Dict[str, Any]:
    """
    输入宝可梦名称，输出其属性及分组结果
    """
    std_name = normalize_pokemon_name(name)
    types = name_type_map.get(std_name, None)
    if not types:
        return {'error': f'未找到宝可梦名称：{name}'}
    if isinstance(types, str):
        types = [types]
    norm_types = normalize_types(types)
    relations = query_type_relations(norm_types)
    return {
        '名称': name,
        '属性': norm_types,
        '克制关系': relations
    }

# 命令行参数解析
def main():
    parser = argparse.ArgumentParser(
        description='宝可梦属性克制关系与属性查询工具',
        epilog='示例：\n  python type_query_app.py --type 火 水\n  python type_query_app.py --name 皮卡丘\n  python type_query_app.py --type grass --type fire\n  python type_query_app.py --name Charizard'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--type', nargs='+', help='输入属性（可多选），如：火 水')
    group.add_argument('--name', help='输入宝可梦名称，如：皮卡丘')
    args = parser.parse_args()

    if args.type:
        types = normalize_types(args.type)
        if not types:
            print(f'无效属性输入：{args.type}')
            sys.exit(1)
        relations = query_type_relations(types)
        print(f'输入属性: {types}')
        print('克制关系分组:')
        for k, v in relations.items():
            print(f'  {k}: {", ".join(v) if v else "无"}')
    elif args.name:
        result = query_pokemon_relations(args.name)
        if 'error' in result:
            print(result['error'])
            sys.exit(1)
        print(f'宝可梦名称: {result["名称"]}')
        print(f'属性: {", ".join(result["属性"]) if result["属性"] else "无"}')
        print('克制关系分组:')
        for k, v in result['克制关系'].items():
            print(f'  {k}: {", ".join(v) if v else "无"}')

# 函数接口（可供其他脚本调用）
def type_query(types: List[str]) -> Dict[str, List[str]]:
    norm_types = normalize_types(types)
    return query_type_relations(norm_types)

def pokemon_query(name: str) -> Dict[str, Any]:
    return query_pokemon_relations(name)

if __name__ == '__main__':
    main()

"""
使用说明：
1. 命令行方式：
   - 查询属性克制关系：python type_query_app.py --type 火 水
   - 查询宝可梦名称属性及克制关系：python type_query_app.py --name 皮卡丘
2. 函数调用方式：
   - type_query(['火', '水'])
   - pokemon_query('皮卡丘')
3. 支持多属性组合、输入容错（如“火系”、“Fire”、“fire”均可识别为“火”），分组输出克制、被克制、抵抗、免疫。
4. 数据文件需与脚本同目录：pokemon_type_chart.json、pokemon_name_type_map.json。
5. 详细逻辑和边界情况见type_query_logic.md。
"""

# type_query_app.py
"""
宝可梦属性克制关系与宝可梦名称查询接口模块。
本模块负责读取属性克制关系和名称-属性映射数据，提供公开查询函数接口，供其他Python程序调用。
支持输入属性名（单属性或多属性）或宝可梦名称，返回结构化克制信息结果。
详细输入输出约定请参考type_query_logic.md。
"""
import json
import os
from typing import List, Dict, Union, Any

# 数据文件路径（假设与py文件同目录）
TYPE_CHART_PATH = os.path.join(os.path.dirname(__file__), 'pokemon_type_chart.json')
NAME_TYPE_MAP_PATH = os.path.join(os.path.dirname(__file__), 'pokemon_name_type_map.json')

# 属性标准名称映射表，可根据type_query_logic.md扩充
# 示例: '草系' -> '草', 'grass' -> '草', 'fire' -> '火'
TYPE_ALIASES = {
    '草系': '草', 'grass': '草', 'グラス': '草',
    '火系': '火', 'fire': '火', 'ファイア': '火',
    '水系': '水', 'water': '水', 'ウォーター': '水',
    # 可补充完整属性列表
}

# 宝可梦名称别名映射表，可根据type_query_logic.md/数据补充
NAME_ALIASES = {
    # '妙蛙种子': 'Bulbasaur', 'bulbasaur': '妙蛙种子',
    # '小火龙': 'Charmander', 'charizard': '喷火龙', ...
}


def _load_json(file_path: str) -> Any:
    """
    加载JSON文件内容。
    """
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)

# 数据加载
_type_chart = _load_json(TYPE_CHART_PATH)  # 属性克制表
_name_type_map = _load_json(NAME_TYPE_MAP_PATH)  # 宝可梦名称到属性映射


def standardize_type_input(type_name: str) -> str:
    """
    标准化属性名输入，支持去除“系”、统一别名、大小写、空格。
    """
    t = type_name.replace('系', '').strip().lower()
    # 首先查找别名映射
    if t in TYPE_ALIASES:
        return TYPE_ALIASES[t]
    # 中文属性直接返回，英文标准化到中文（如Pokemon数据中）
    # 可扩展更多映射
    return t.capitalize()


def standardize_name_input(name: str) -> str:
    """
    标准化宝可梦名称输入，支持多语言、大小写、空格、别名。
    """
    n = name.strip().lower()
    if n in NAME_ALIASES:
        return NAME_ALIASES[n]
    # 优先中文名
    return n.capitalize()


def get_types_for_name(name: str) -> List[str]:
    """
    根据宝可梦名称查询其属性列表。
    支持名称标准化和别名映射。
    """
    std_name = standardize_name_input(name)
    return _name_type_map.get(std_name, [])


def query_type_relations(type_names: Union[str, List[str]]) -> Dict[str, List[str]]:
    """
    查询属性克制关系。
    输入可为单属性或多属性（支持逗号/空格分隔字符串或list）。
    返回结构化分组结果：
        {
            'super_effective': [list],    # 克制
            'not_effective': [list],      # 被克制
            'resistant': [list],          # 抵抗
            'immune': [list]              # 免疫
        }
    """
    # 支持输入如 "草,水" 等，或list
    if isinstance(type_names, str):
        types = [standardize_type_input(x) for x in type_names.replace(',', ' ').split() if x.strip()]
    else:
        types = [standardize_type_input(x) for x in type_names if x.strip()]
    # 结果集合
    super_eff = set()
    not_eff = set()
    resist = set()
    immune = set()
    # 合并多属性
    for t in types:
        info = _type_chart.get(t, {})
        super_eff.update(info.get('super_effective', []))
        not_eff.update(info.get('not_effective', []))
        resist.update(info.get('resistant', []))
        immune.update(info.get('immune', []))
    # 去重并返回
    return {
        'super_effective': sorted(super_eff),
        'not_effective': sorted(not_eff),
        'resistant': sorted(resist),
        'immune': sorted(immune)
    }


def query_pokemon_relations(name: str) -> Dict[str, List[str]]:
    """
    查询宝可梦名称的属性被/克制关系。
    输入为宝可梦名称（支持别名、多语言、大小写自动处理）
    返回结构化分组结果（参考query_type_relations说明）。
    """
    types = get_types_for_name(name)
    if not types:
        # 返回空结构
        return {
            'super_effective': [],
            'not_effective': [],
            'resistant': [],
            'immune': []
        }
    return query_type_relations(types)


def query(input_val: Union[str, List[str]]) -> Dict[str, Any]:
    """
    通用查询接口。
    输入可以为：属性名（单/多）、宝可梦名称。
    识别输入类型后，自动合并并查询。
    返回分组结果以及原始标准化信息。
    """
    # Heuristic: 先尝试当作宝可梦名称查询属性
    types = get_types_for_name(input_val)
    if types:
        relation = query_type_relations(types)
        return {
            'input_type': 'pokemon_name',
            'raw_input': input_val,
            'standardized_name': standardize_name_input(input_val),
            'types': types,
            'relations': relation
        }
    # 否则当作属性名（可能逗号/空格分隔）
    if isinstance(input_val, str):
        input_types = [standardize_type_input(x) for x in input_val.replace(',', ' ').split() if x.strip()]
    else:
        input_types = [standardize_type_input(x) for x in input_val if x.strip()]
    relation = query_type_relations(input_types)
    return {
        'input_type': 'type',
        'raw_input': input_val,
        'standardized_types': input_types,
        'relations': relation
    }

# 公共接口：
# 1. query(input_val)           # 自动识别输入类型（属性或名称），返回分组结果
# 2. query_type_relations(type_names)  # 属性名查询
# 3. query_pokemon_relations(name)     # 宝可梦名称查询
#
# 输入输出详见type_query_logic.md

"""
接口示例：
    result = query('草,火')
    result = query('妙蛙种子')
    result = query_type_relations(['草', '毒'])
    result = query_pokemon_relations('charizard')
返回示例：
    {
        'input_type': 'type',
        'raw_input': '草,火',
        'standardized_types': ['草','火'],
        'relations': {
            'super_effective': [...],
            ...
        }
    }
详细边界情况和说明请参考type_query_logic.md文件。
"""

