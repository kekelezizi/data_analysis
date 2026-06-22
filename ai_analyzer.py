import pandas as pd
from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)

# 入参 reports为report.py中的表
"""
基于报表数据生成规则板业务分析
返回dataFream，方便导出到Excel 的 ai_analysis sheet
"""
def generate_ai_analysis(reports):
  seller_summary = reports['seller_summary']
  category_summary = reports['category_summary']
  quality_issues = reports['quality_summary']
  analysis_rows = []
  # 1. 销售总览
  # 2. 销售员表现
  # 3. 产品类目表现
  # 4. 数据质量风险
  # 5. 业务建议
  get_seller_summary(analysis_rows, seller_summary)
  get_category_summary(analysis_rows, category_summary)
  get_quality_issues(analysis_rows, quality_issues)

  analysis_df = pd.DataFrame(analysis_rows)
  logger.info(f"AI分析结果: {analysis_df}")
  return analysis_df

def get_seller_summary(analysis_rows, seller_summary):
  if seller_summary.empty:
    analysis_rows.append({
      'section': '销售员表现',
      'content': '本期没有销售员数据'
    })
    return
  top_seller = seller_summary.sort_values(by='total_amount', ascending=False).iloc[0]
  analysis_rows.append({
    'section': '销售员表现',
    'content': f'本期销售额最高的是{top_seller["seller"]}，销售额为{top_seller["total_amount"]}'
  })

def get_category_summary(analysis_rows, category_summary):
  if category_summary.empty:
    analysis_rows.append({
      'section': '产品类目表现',
      'content': '本期没有产品类目数据'
    })
    return
  top_category = category_summary.sort_values(by='total_amount', ascending=False).iloc[0]
  analysis_rows.append({
    'section': '产品类目表现',
    'content': f'本期销售额最高的是{top_category["category"]}，销售额为{top_category["total_amount"]}'
  })

def get_quality_issues(analysis_rows, quality_issues):
  if quality_issues.empty:
    analysis_rows.append({
      'section': '数据质量风险',
      'content': '本期没有数据质量风险数据'
    })
    return
  top_quality_issues = quality_issues.sort_values(by='count', ascending=False).iloc[0]
  analysis_rows.append({
    'section': '数据质量风险',
    'content': f'本期数据质量风险最高的是{top_quality_issues["reason"]}，数量为{top_quality_issues["count"]}'
  })
