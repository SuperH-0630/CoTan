import json
import os

from pyecharts import options as opts
from pyecharts.charts import Page, TreeMap


def treemap_base() -> TreeMap:
    data = [
        {"value": 40, "name": "我是A"},
        {
            "name": "我是B",
            "children": [
                {
                    "value": 76,
                    "name": "我是B.children",
                    "children": [
                        {"value": 12, "name": "我是B.children.a"},
                        {"value": 28, "name": "我是B.children.b"},
                        {"value": 20, "name": "我是B.children.c"},
                        {"value": 16, "name": "我是B.children.d"},
                    ],
                }
            ],
        },
    ]
    print(data)
    c = (
        TreeMap()
        .add("演示数据", data,label_opts=opts.LabelOpts(is_show=True,position='inside'))
        .set_global_opts(title_opts=opts.TitleOpts(title="TreeMap-基本示例"))
    )
    return c

treemap_base().render()