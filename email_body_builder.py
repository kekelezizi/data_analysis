from logging import getLogger
import pandas as pd
from datetime import datetime

logger = getLogger(__name__)

# 根据报告的结果，书写正文
# 输入：报告的结果
# 输出：正文
def build_email_body(reports):
  """
  基于reports中的 ai_analysis 和 quality_summary 构建正文
  Args:
    reports: 报告的结果
  Returns:
    body: 正文
  """
  logger.info(f"开始构建正文，报告的结果：{reports}")
  # 使用函数的方式更稳定
  ai_analysis = reports.get("ai_analysis", pd.DataFrame())
  quality_summary = reports.get("quality_summary", pd.DataFrame())
  # quality_summary = reports.get("quality_summary") 与 quality_summary = reports.get("quality_summary", pd.DataFream)的区别
  lines = []
  lines.append("各位好：")
  lines.append("")
  lines.append("本期销售数据报表已分析完成，核心结论如下：")
  lines.append("")
  if ai_analysis.empty:
    lines.append("暂无AI分析结论，请查看附件")
    lines.append("")
  else:
    for index, row in ai_analysis.iterrows():
      section = row.get("section", "")
      content = row.get("content", "")
      lines.append(f"{index + 1}. 【{section}】{content}")
  lines.append("")

  if not quality_summary.empty and "count" in quality_summary.columns:
    total_issues = quality_summary["count"].sum()
    lines.append(f"本期销售数据共发现 {total_issues} 条数据质量问题，请查看附件")
    lines.append("")
  
  lines.append("完整数据报表请查看邮件中的附件")
  lines.append("")
  lines.append("感谢大家的支持与配合，祝大家工作顺利，生活愉快！")
  lines.append("")
  lines.append("此致")
  lines.append("")
  lines.append("销售分析团队")
  lines.append("")
  lines.append(f"日期：{datetime.now().strftime('%Y-%m-%d')}")
  body = "\n".join(lines)
  logger.info(f"构建的正文完成：{body}")
  return body

