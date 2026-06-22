"""
本小节主要内容为将报告转换为MarkDown格式(需要安装tabulate)
"""

from datetime import datetime
from logginger import get_logger
import pandas as pd
from pathlib import Path

logger = get_logger(__name__)

"""
1. 先确定MarkDown包含哪些章节
2. 报告生成的时间 datetime.now().strftime("%Y-%m-%d %H:%M:%S")
3. 销售总览
  reports['clean_data']
4. 销售员表现seller_summary.to_markdown(index=False)
5. 产品类目输出
6. 数据质量情况
7. AI分析结论
8. 附件说明
"""

def export_markdown_report(reports, output_path):
  # 转为 Path；若传入的是 .xlsx 路径则自动改成 .md
  md_path = Path(output_path)
  if md_path.suffix.lower() != '.md':
    md_path = md_path.with_suffix('.md')

  seller_summary = reports.get('seller_summary', pd.DataFrame())
  category_summary = reports.get('category_summary', pd.DataFrame())
  quality_summary = reports.get('quality_summary', pd.DataFrame())
  analysis_df = reports.get('ai_analysis', pd.DataFrame())
  # 等同于 analysis_df = reports['analysis_df']

  lines = []

  # 1. 生成标题和时间
  lines.append("# 销售分析报告")
  lines.append("")
  lines.append(f"生成时间为：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
  # 这里是append，不要当成log的语法
  lines.append("")
  # 2. 销售总览
  lines.append("## 销售总览")
  lines.append("")
  lines.append('- 本期暂时没有销售总览数据')
  lines.append("")
  # 3. 销售员表现
  lines.append("## 销售员表现")
  lines.append("")
  if seller_summary.empty:
    lines.append('- 本期暂时没有销售员表现数据')
  else:
    lines.append(seller_summary.to_markdown(index=False))
  lines.append("")
  # 4. 产品类目表现
  lines.append("## 产品类目表现")
  lines.append("")
  if category_summary.empty:
    lines.append('- 本期暂时没有产品类目表现数据')
  else:
    lines.append(category_summary.to_markdown(index=False))
  lines.append("")  
  # 5. 数据质量情况
  lines.append("## 数据质量情况")
  lines.append("")
  if quality_summary.empty:
    lines.append('- 本期暂时没有数据质量情况数据')
  else:
    lines.append(quality_summary.to_markdown(index=False))
  lines.append("")
  # 6. AI分析结论
  lines.append("## AI分析结论")
  lines.append("")
  if analysis_df.empty:
    lines.append('- 本期暂时没有AI分析结论数据')
  else:
    lines.append(analysis_df.to_markdown(index=False))
  lines.append("")
  # 7. 附件说明
  lines.append("## 附件说明")
  lines.append("")
  lines.append('- 附件为原始数据文件，仅供参考')
  lines.append("")

  md_path.write_text("\n".join(lines), encoding='utf-8')
  logger.info('Markdown报告生成完成: %s', md_path)
  return md_path

