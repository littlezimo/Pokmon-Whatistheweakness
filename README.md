# 宝可梦ZA属性克制关系与属性查询应用交付说明

## 1. 文件清单与目录结构

- pokemon_type_chart.json  —— 属性克制关系表，标准化18种属性的克制、被克制、抵抗、免疫关系。
- pokemon_name_type_map.json  —— 宝可梦名称与属性对照表，含中英文名、别名、属性。
- type_query_logic.md  —— 查询逻辑说明，输入输出规范、边界处理、分组规则等。
- type_query_app.md  —— 应用实现说明/接口文档，含主要函数、命令行参数、扩展说明。
- type_query_app.py  —— 可直接调用的Python脚本，支持属性/宝可梦名称查询。
- type_query_test.md  —— 测试用例与优化报告，覆盖全部功能、边界、异常、国际化等场景。

## 2. 各文件用途说明

- **pokemon_type_chart.json**：结构化存储18种属性的克制关系，支持多语言别名，供查询逻辑调用。
- **pokemon_name_type_map.json**：存储宝可梦名称（中/英/别名）与属性对应关系，支持单/多属性宝可梦。
- **type_query_logic.md**：详细说明输入标准化、输出分组、组合属性处理、异常输入等逻辑。
- **type_query_app.md**：描述Python脚本的主要接口、命令行参数、返回结构、扩展点。
- **type_query_app.py**：主程序，支持命令行和函数调用，自动标准化输入，返回分组结果。
- **type_query_test.md**：测试用例设计、执行结果、问题与优化建议，便于查验和维护。

## 3. Python脚本使用方法

### 3.1 命令行调用
```bash
python type_query_app.py --type 草
python type_query_app.py --name 小火龙
python type_query_app.py --type "草/毒"
python type_query_app.py --name "Charizard"
```

### 3.2 作为模块导入
```python
from type_query_app import query_type_relations, query_pokemon_type_and_weakness

print(query_type_relations('草'))
print(query_pokemon_type_and_weakness('小火龙'))
```

## 4. 示例输入输出

- 输入：草
  输出：
  - 克制草系的属性：火、冰、飞行、虫
  - 草系克制的属性：水、地面、岩石
  - 草系抵抗的属性：水、电、草、地面
  - 草系免疫的属性：无

- 输入：小火龙
  输出：
  - 属性：火
  - 被克制属性：水、地面、岩石

- 输入：Charizard
  输出：
  - 属性：火、飞行
  - 被克制属性：水、电、岩石

## 5. 其他说明

- 所有输入均支持中英文、别名、去除“系”字、大小写不敏感。
- 多属性宝可梦自动合并属性克制关系，分组输出。
- 支持批量查询、异常输入提示、国际化扩展。
- 测试用例与优化建议详见type_query_test.md。

## 6. 维护与扩展建议

- 如需扩充新属性或宝可梦，请同步更新pokemon_type_chart.json和pokemon_name_type_map.json。
- 逻辑或功能扩展建议见type_query_logic.md和type_query_app.md。
- 测试与优化建议见type_query_test.md。

---

如有疑问或需定制扩展，请参考各说明文档或联系开发者。

