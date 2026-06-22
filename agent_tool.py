import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

from data_loader import load_data
from field_mapper import map_fields
from cleaner import clean_df_data
from report import build_report, export_report
from ai_analyzer import generate_ai_analysis
from chart_builder import add_chart_to_workbook
from report_writer import export_markdown_report
from send_email import send_email
from email_body_builder import build_email_body

load_dotenv()

VALID_STATUSES = os.getenv('VALID_STATUSES')
VALID_CATEGORIES = os.getenv('VALID_CATEGORIES')
TO_EMAILS = os.getenv('TO_EMAILS')
CC_EMAILS = os.getenv('CC_EMAILS')

def build_summary(reports):
  """
  从报表结果中提取给 Agent 使用的摘要信息
  """
  # TODO 1. 从reports中 读取 clean_details
  clean_details = reports.get('clean_details', pd.DataFrame())
  # TODO 2. 计算total_amount
  total_amount = 0
  if not clean_details.empty and 'amount' in clean_details.columns:
    total_amount = clean_details['amount'].sum()  
  # TODO 3. 计算total_orders
  total_orders = len(clean_details)
  # TODO 4. 从quality_summary 中计算 quality_issue_count
  quality_summary = reports.get('quality_summary', pd.DataFrame())
  quality_total = 0
  if not quality_summary.empty and 'count' in quality_summary.columns:
    quality_total = quality_summary['count'].sum()
  # TODO 5. 返回dict
  return {
    "total_orders": total_orders,
    "total_amount": total_amount,
    "quality_total": quality_total,
  }

def run_sales_report_tool(
  input_path,
  output_excel_path='outputs/agent_report.xlsx',
  output_markdown_path='outputs/agent_report.md',
  generate_chart=True,
  generate_markdown=True,
  need_send_email=False,
  to_emails=TO_EMAILS
):
  try:
    input_path = Path(input_path)
    output_excel_path = Path(output_excel_path)
    output_excel_path.parent.mkdir(parents=True, exist_ok=True)

    df = load_data(input_path)

    mapped_df = map_fields(df)

    cleaned = clean_df_data(
      mapped_df,
      VALID_STATUSES,
      VALID_CATEGORIES
    )
    reports = build_report(
      cleaned['clean_df'],
      cleaned['quality_summary'],
    )
    reports["ai_analysis"] = generate_ai_analysis(reports)
    export_report(reports, output_excel_path)

    if generate_chart:
      add_chart_to_workbook(output_excel_path)
    # if generate_markdown & output_markdown_path:
    if generate_markdown and output_markdown_path:
      markdown_path = Path(output_markdown_path)
      markdown_path.parent.mkdir(parents=True, exist_ok=True)
      export_markdown_report(reports, output_markdown_path)
    if need_send_email:
      if len(to_emails) > 0:
        body = build_email_body(reports)
        send_email([str(output_excel_path), str(output_markdown_path)], to_emails, CC_EMAILS, '', body=body)

    return {
      "success": True,
      "message": "Sales report generated successfully",
      "excel_path": str(output_excel_path),
      "markdown_path": str(output_markdown_path),
      "summary": build_summary(reports),
    }
  except Exception as e:
    return {
      "success": False,
      "message": str(e),
      "excel_path": output_excel_path,
      "markdown_path": output_markdown_path,
    }

if __name__ == "__main__":
  run_sales_report_tool(
    "E:/浏览器文件/seller.csv",
    "output/agent_report.xlsx",
    "output/agent_report.md",
    True,
    True,
  )


