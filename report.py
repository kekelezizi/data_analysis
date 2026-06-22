import pandas as pd
from pathlib import Path
from logginger import get_logger

logger = get_logger(__name__)

def build_report(df, quality_summary):
  export_df = df.copy()
  # seller 的统计
  # groupby：按照seller分组
  # agg：对分组后的数据进行聚合
  # total_amount: 生成新的一列，这一列展示amount的求和
  seller_summary = export_df.groupby('seller').agg(
    total_amount = ('amount', 'sum'),
    # total_amount = pd.NamedAgg(column='amount', aggfunc='sum'),  # 使用NamedAgg方式，更清晰，和上面的用法是一样的
    # order_count = 'count',
    order_count = ('order_date', 'count'),
    average_amount = ('amount', 'mean'),
  ).reset_index()

  category_summary = export_df.groupby('category').agg(
    total_amount = ('amount', 'sum'),
    order_count = ('order_date', 'count'),
    average_amount = ('amount', 'mean'),
  ).reset_index()

  pivot_table = export_df.pivot_table(
    index = 'seller',
    columns = 'category',
    values = 'amount',
    aggfunc = 'sum',
    fill_value = 0,
  ).reset_index()

  return {
    "clean_details": df,
    'seller_summary': seller_summary,
    'category_summary': category_summary,
    'pivot_table': pivot_table,
    'quality_summary': quality_summary,
  }

def export_report(report, output_path):
  output_path = Path(output_path)
  if output_path.suffix.lower() != '.xlsx':
    output_path = output_path.with_suffix('.xlsx')
  output_path.parent.mkdir(parents=True, exist_ok=True)
  logger.info('开始导出报告，报告路径为%s', output_path)
  with pd.ExcelWriter(output_path) as writer:
    for sheet_name, data in report.items():
      data.to_excel(writer, sheet_name=sheet_name, index=False)
  logger.info('报告导出完成，报告路径为%s', output_path)