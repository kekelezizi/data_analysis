import argparse

def arg_parse():
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_path', type=str, default=r'E:\浏览器文件\seller.csv', help='data path')
  parser.add_argument('--output_path', type=str, default=r'E:\浏览器文件\day8.xlsx', help='output path')
  parser.add_argument('--markdown_path', '-mdp', type=str, default=r'E:\浏览器文件\day8.md', help='markdown path')
  parser.add_argument('--valid-statue', '-vs', help='请输入vaild statue')
  parser.add_argument('--valid-category', '-vc', help='请输入vaild category')
  parser.add_argument('--send-email', '-send', help='请输入输入邮件地址')
  parser.add_argument('--to-email', '-to', help='请输入输入邮件地址')
  parser.add_argument('--Cc-email', '-Cc', help='请输入输入邮件地址')
  args = parser.parse_args()
  return args
