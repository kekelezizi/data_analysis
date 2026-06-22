
import streamlit as st
from pathlib import Path
from data_loader import load_data
from cleaner import clean_df_data
from field_mapper import map_fields
from report import build_report, export_report
from ai_analyzer import generate_ai_analysis
from chart_builder import add_chart_to_workbook
from report_writer import export_markdown_report

st.set_page_config(
  # 这个是浏览器标题
  page_title="销售报表自动化工具",
  # 
  layout="wide",
)
# 这个是页面标题
st.title("销售报表自动化工具")
st.write("上传销售数据文件，自动生成 Excel 和 Markdown 报告")

upload_file = st.file_uploader(
  "上传销售数据文件",
  type=["csv", "xlsx"],
  accept_multiple_files=False,
  help="请上传销售数据文件",
)

# 定义的两个常量：程序要在磁盘上使用两个目录（相对当前运行目录，一般在 dataAnalysis 下）。
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")

# 将网页里的文件存在磁盘
def save_uploaded_file(uploaded_file):
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True) # 创建目录
  input_path = OUTPUT_DIR / uploaded_file.name # 拼接路径
  input_path.write_bytes(uploaded_file.getbuffer()) # 写入文件
  return input_path

def run_report_pipeline(input_path, generate_chart=True, generate_markdown=True):
  # parents=True：父目录没有也会一起建
  # exist_ok=True：目录已存在不报错
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  output_excel_path = OUTPUT_DIR / "streamlit_report.xlsx"
  output_markdown_path = OUTPUT_DIR / "streamlit_report.md"

  df = load_data(input_path)
  map_field_df = map_fields(df)
  cleaned = clean_df_data(map_field_df, "已成交,成交,退款", "硬件,软件,服务")

  report = build_report(cleaned['clean_df'], cleaned['quality_summary'])
  report['ai_analysis'] = generate_ai_analysis(report)
  report['data_quality'] = cleaned['data_quality']

  export_report(report, output_excel_path)

  if generate_chart:
    add_chart_to_workbook(output_excel_path)

  if generate_markdown:
    export_markdown_report(report, output_markdown_path)

  return {
    "reports": report,
    "output_excel_path": output_excel_path,
    "output_markdown_path": output_markdown_path if generate_markdown else None,
  }

col1, col2 = st.columns(2)

with col1:
  generate_chart = st.checkbox("生成图表", value=True)

with col2:
  generate_markdown = st.checkbox("生成Markdown", value=True)

if upload_file is not None:
  st.success("文件上传成功")

  if st.button("生成报表"):
    try:
      input_path = save_uploaded_file(upload_file)
      with st.spinner("生成报表中..."):
        # result = run_report_pipeline(input_path, generate_chart, generate_markdown)
        result = run_report_pipeline(
          input_path, 
          generate_chart=generate_chart,
          generate_markdown=generate_markdown,
        )
      reports = result["reports"]
      excel_path = result["output_excel_path"]
      markdown_path = result["output_markdown_path"]
      st.success("报表生成成功")
      st.subheader("销售员汇总")
      st.dataframe(reports["seller_summary"])
      st.subheader("产品类目汇总")
      st.dataframe(reports["category_summary"])
      st.subheader("数据质量问题")
      st.dataframe(reports["quality_summary"])
      st.subheader("AI分析结论")
      if reports["ai_analysis"].empty:
        st.warning("AI分析结论为空，请检查数据质量")
      else:
        st.dataframe(reports["ai_analysis"])
      if markdown_path is not None and Path(markdown_path).exists():
        with open(markdown_path, "r", encoding="utf-8") as file:
          st.download_button(
            label="下载Markdown报表",
            data=file.read(),
            file_name=Path(markdown_path).name,
            mime="text/markdown",
          )
      if excel_path.exists():
        with open(excel_path, "rb") as file:
          st.download_button(
            label="下载Excel报表",
            data=file.read(),
            file_name=excel_path.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          )
    except Exception as e:
      st.error(f"生成报表失败: {e}")

"""
with open(excel_path, "rb") as file:
with open(excel_path, "r") as file:
  1. 第二个参数意义：打开模式，r是读取模式，rb是二进制读取模式
  2. 对比
  | 格式 | 含义 | 读取内容 | 典型用途 |
  | r | read text（读取文本） | 读出来的是字符串 | 典型用途 .md、.txt、.csv |
  | rb | read binary（读取二进制） | 读出来的是二进制数据 | 典型用途 .xlsx（本质是压缩包）、.png、.pdf、.zip |
  | w | write text（写入文本） | 写入的是字符串 | 典型用途 .md、.txt、.csv |
  | wb | write binary（写入二进制） | 写入的是二进制数据 | 典型用途 .png、.jpg、.pdf |
  | a | append text（追加文本） | 追加的是字符串 | 典型用途 .md、.txt、.csv |
  | ab | append binary（追加二进制） | 追加的是二进制数据 | 典型用途 .png、.jpg、.pdf |
  | x | exclusive write（独占写入） | 独占写入的是字符串 | 典型用途 .md、.txt、.csv |
  | xb | exclusive write binary（独占写入二进制） | 独占写入的是二进制数据 | 典型用途 .png、.jpg、.pdf |
  3. 记忆方式
  r  = read text   → 给人看的文字文件
  rb = read binary → 给程序用的二进制文件
"""


