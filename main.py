import logginger  # 入口先加载日志配置，其它模块直接用 get_logger 即可
from data_analysis_argparse import arg_parse
from data_loader import load_data
from cleaner import clean_df_data
from report import build_report, export_report
from send_email import send_email
from logginger import get_logger
from field_mapper import map_fields
from chart_builder import add_chart_to_workbook
from ai_analyzer import generate_ai_analysis
from report_writer import export_markdown_report
from email_body_builder import build_email_body

logger = get_logger(__name__)

def main():
  args = arg_parse()
  logger.info('开始执行数据分析任务')
  df = load_data(args.data_path)
  map_field_df = map_fields(df)
  _clean_df_data = clean_df_data(map_field_df, args.valid_statue, args.valid_category)
  report = build_report(_clean_df_data['clean_df'], _clean_df_data['quality_summary'])
  ai_analysis_df = generate_ai_analysis(report)
  report['ai_analysis'] = ai_analysis_df
  export_report(report, args.output_path)
  md_path = export_markdown_report(report, args.markdown_path)
  add_chart_to_workbook(args.output_path)
  body = build_email_body(report)
  send_email([args.output_path, md_path], args.to_email, args.Cc_email, '', body=body)
  logger.info('数据分析任务执行完成')
  logger.info('图表已保存到: %s', args.output_path)


if __name__ == '__main__':
  main()