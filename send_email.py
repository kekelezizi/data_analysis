
from email.message import EmailMessage
import smtplib
import os
from pathlib import Path
from logginger import get_logger

logger = get_logger(__name__)
# 1. 先获取本地的端口、host、用户名、密码
# 2. 添加附件
# 3. 设置抄送
# 4. 发送邮件
def send_email(attachment_paths, to_emails, cc_emails, subject="销售数据分析报告", body=None):
  smtp_host = os.getenv('SMTP_HOST')
  smtp_user = os.getenv('SMTP_USER')
  smtp_port = int(os.getenv('SMTP_PORT', '465'))
  smtp_password = os.getenv('SMTP_PASSWORD')
  if not smtp_host or not smtp_user or not smtp_port or not smtp_password:
    raise RuntimeError('SMTP_HOST, SMTP_USER, SMTP_PORT, SMTP_PASSWORD 不能为空')

  if len(attachment_paths) == 0:
    raise FileNotFoundError(f'附件文件不存在: {attachment_paths}')
  msg = EmailMessage()
  msg['From'] = smtp_user
  msg['To'] = normalize_email_list(to_emails)
  msg['Subject'] = '数据分析报告'
  msg['Cc'] = normalize_email_list(cc_emails)
  msg.set_content('请查看附件中的数据分析报告')
  for attachment_path in attachment_paths:
    path = Path(attachment_path)
    if not path.is_file():
      raise FileNotFoundError(f'附件文件不存在: {path}')
    maintype, subtype = guess_attachment_mime_type(path)
    msg.add_attachment(
      path.read_bytes(),
      maintype=maintype,
      subtype=subtype,
      filename=path.name
    )

  try:
    logger.info('开始发送邮件')
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
      smtp.login(smtp_user, smtp_password)
      all_emails = normalize_email_list(to_emails) + normalize_email_list(cc_emails)
      smtp.send_message(msg, to_addrs=all_emails)
      logger.info('邮件发送成功')
  except Exception as e:
    logger.error(f'邮件发送失败: {e}')
    raise RuntimeError(f'邮件发送失败: {e}')

def normalize_email_list(emails):
  if emails is None:
    return []
  if isinstance(emails, str):
    return [email.strip() for email in emails.split(',') if email.strip()]
  if isinstance(emails, list):
    return emails

  raise ValueError(f"不支持的邮箱列表类型: {type(emails)}")

def guess_attachment_mime_type(attachment_path):
  suffix = attachment_path.suffix.lower()
  if suffix == '.xlsx':
    return "application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  if suffix == '.csv':
    return "text","csv"
  if suffix == '.txt':
    return "text", "plain"
  if suffix == ".md":
    return "text", "markdown"
  if suffix == ".pdf":
    return "application", "pdf"
  if suffix == ".xls":
    return "application", "vnd.ms-excel"
  return "application", "octet-stream"

