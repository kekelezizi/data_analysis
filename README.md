# 第8天
## 1. 学习目标
今日学习目标为工程化
## 2. 实现方法

- 初始化运行参数
-- 1. 文件输入地址
-- 2. 文件输出地址
-- 3. 需要校验的状态
-- 4. 需要校验的类目
-- 5. 发件邮件地址
-- 6. 收件邮件地址
-- 7. 抄送邮件地址

- 加载数据
- 数据清洗
- 数据分表
- 数据导出
- 发送邮件

# 第 9 天
## 1. 学习目标
- 工程化对应的质量报表、错误报表输出
## 2. 实现方法
- cleaner.py
- 1. 先拷贝amount数据为一张表： original_amount = work_df['amount].copy()
- 2. 做数据转换：work_df['amount] = pd.to_numeric(work_df['amount'], errors='coerce')
- 3. 筛选出不为空但是转换失败的数据：amount_invalid_mask = original_amount.notna() & work_df['amount].isna()
- 4. 筛选为空的数据：empty_data = work_df['amount', ...].isna().any(axis=1)
## 3. 导出
## 4. 发送邮件

# 第 10 天
## 1. 学习目标
- 今日学习目标为 添加报表对应的图表例如 饼图、主状态

## 2. 使用技术：有以下两个常见技术
- 1. pandas + openpyxl 往Excel里面写图标
---- 优点：图表直接在Excel里面，适合业务交付。
---- 缺点：比pandas 还啰嗦
- 2. matplotlib生成图片之后再插入Excel
---- 优点：图表样式更灵活。
---- 缺点：中文字体，图片插入，路径管理更麻烦

## 3. 实现方法：今天使用openpyxl
新增chart_builder.py
- 1. 使用 wb = load_workbook('day11.xlsx')方法获取表格
- 2. 判断是否存在画图表 if CHART_SHEET in wb.sheet_name
- 3. 建表 ws_chart = wb.create(CHART_SHEET)
- 4. 做图
---- 1. 取数据 ws_data = wb['seller_summary']
---- 2. chart = PieChart()
---- 3. chart.title = '销售数据图'
---- 4. label = Reference(min_col = 1, min_row = 2, max_row = ws_data.max_row)
---- 5. data = Reference(min_col = 2, min_raw = 1, max_row = ws.data.max_row)
---- 6. chart.add_data(data, titles_from_data=True)
---- 7. chart.set_categories(label)
---- 8. ws_chart.add_chart(chatr, 'A1')
- 5. 保存 wb.save(output_path)

# 第 11 天
## 1. 学习目标
自动生成业务分析
输出结论类似于：
"""
本期销售总额为 28,500 元，其中张三销售额最高，占总销售额 42%。
硬件类目贡献最大，占比 55%。
本次数据共发现 6 条质量问题，主要集中在金额非法和订单状态异常。
建议重点关注低绩效销售员，并规范订单状态录入。
"""
## 2. 内容
1. 一般包含几类内容
- 销售总览
- 业务员表现
- 产品类目表现
- 数据质量风险
- 业务建议
| section | content |
| 销售总览 | 本期有效订单共计20单，总额为128000 |
| 销售员表现 | 张三销售额最高，为56000 |
| 产品类目表现 | 硬件类目贡献最大，销售额78000 |
| 数据质量风险 | 	本次发现 5 条异常数据，主要问题为 amount_invalid。 |
| 业务建议 | 建议复盘低销售额人员，并加强订单数据录入校验。 |
## 3. 实现
1. 新增ai_analyzer.py

# 第 12 天
## 1. 学习目标
升级为更像“业务交付物”的形式
（不是直接生成Excel，而是生成一份老板能直接看的文字报告）
- 优先做MarkDown导出
- 可选word导出
## 2. 内容（以MarkDown的形式）
- 输出形式
1. 销售总览
2. 销售员表现
3. 产品类目表现
4. 数据质量情况
5. AI分析结论
6. 附件说明
## 3. 实现
(需要安装to_markdown)
1. 对于需要将报表转换为md格式的表时，通过 seller_summary.to_markdown(index=False)
2. 然后按照md大纲格式进行拼接
3. 例如
"""
lines = []
lines.append("# 销售报表分析")
lines.append("")
lines.append(f"报表分析时间：{datetime.now().strftime("%Y-%d-%d %H:%M:%S ")}")
....
"""
4. 最后输出
md_path.write_text('\n'.join(lines), encoding='utf-8')

# 第13天学习
## 1. 学习目标
今日的学习目标为：给报表做一个streamlit页面：即升级为一个简单的页面
## 2. 内容
### 1. 页面上需要展示的内容
1. 上传csv/excel按钮
2. 点击按钮上传
3. 自动生成Excel报表
4. 自动生成Markdown报告
5. 页面展示分析摘要
6. 提供下载按钮
### 2. 浏览器中最终的效果
1. 销售报表自动化工具
2. 上传文件
3. 选择是否生成图表
4. 选择是否生成Markdown
5. 点击生成报表
6. 下载Excel
7. 下载Markdown
8. 预览AI分析结论
## 3. 实现
1. streamlit理解（参考前端页面对比理解）
| React页面 | app.py |
----------------------
| input上传组件 | st.file_uploader() |
-------------------------------------
| button | st.button() |
------------------------
| state | st.session_state() |
------------------------------
| table | st.datafream |
-------------------------
| dwonload | st.download_button() |
------------------------------------
| alert | st.success() / st.error() |
-------------------------------------
| markdown | st.markdown() |
----------------------------
2. 实现
一个模块两个入口（cli入口：mian.py，web入口：app.py）
- 新增app.py
- 引入streamlit
- 配置页面
- 写方法
-- st.subheader('销售分析总览')
-- st.datafream(seller_summary)  直接将表格展示出来

# 第 14 天学习
## 1. 学习目标
邮件整合 + AI 正文
## 2. 学习内容
邮件应该是正文 + 附件的形式，之前是只有附件没有正文的形式
## 3. 实现
新增 email_body_builder.py
1. 改造email_sender.py
2. 改造main.py

# 第 15 天学习
## 1. 学习目标
将之前完成的销售报表项目，封装成一个AI Agent，可以调用的 python 工具。作用：将之前的完整流程全部都封装起来
## 2. 学习内容
新增一个 agent_tool.py
实现一个核心函数
"""
python
def run_sales_report_tool(
  input_path,
  output_excel_path='....xlsx',
  output_markdown_path='....md',
  generate_chart=True,
  generate_markdown=True
) :
...
pass
"""
## 3. 实现

# 第 16 天学习
## 1. 学习目标
今天的学习内容是将这个项目整理成别人能看懂、能安装、能运行、能复用的正式项目
## 2. 内容
销售数据自动化分析工具
### 1. 项目简介
本项目是一个基于 Python 的销售数据自动化分析工具，支持从 CSV / Excel 文件读取销售订单数据，自动完成字段映射、数据清洗、数据质量检查、销售汇总分析、Excel 报表导出、图表生成、Markdown 报告生成和邮件发送。
项目同时提供命令行入口、Streamlit Web 页面入口，以及可被 AI Agent 调用的工具函数入口。
### 2. 核心功能
- 支持 CSV / Excel 销售数据读取
- 支持中文字段映射
- 支持销售金额、订单日期、状态、类目等字段清洗
- 生成数据质量问题明细和汇总
- 生成销售员维度汇总
- 生成商品类目维度汇总
- 生成透视分析表
- 导出多 Sheet Excel 报表
- 自动插入 Excel 图表
- 生成 Markdown 分析报告
- 生成 AI 规则分析结论
- 支持邮件正文和附件发送
- 封装为 AI Agent 可调用工具函数

## 3. 项目结构

```text
sales_report_tool/
├── main.py
├── app.py
├── agent_tool.py
├── data_loader.py
├── field_mapper.py
├── cleaner.py
├── report.py
├── chart_builder.py
├── ai_analyzer.py
├── report_writer.py
├── email_body_builder.py
├── send_email.py
├── input/
├── outputs/
├── uploads/
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```
### 4. 安装依赖
pip install -r requirements.txt
### 5. 配置环境变量
cp .env.example .env
### 6. 命令运行
python main.py
### 7. 启动web页面
streamlit run app.py
### 8. Agent tool 调用
from agent_tool import run_sales_report_tool

result = run_sales_report_tool(
    input_path="input/sales_sample.csv",
    output_excel_path="outputs/agent_report.xlsx",
    output_markdown_path="outputs/agent_report.md",
    generate_chart=True,
    generate_markdown=True,
    send_email_enabled=False,
)

print(result)
### 9. 输入文件数据字段说明

字段	说明
order_id	订单编号
order_date	订单日期
seller	销售员
category	商品类目
amount	销售金额
status	订单状态

