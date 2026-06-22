import pandas as pd
from logginger import get_logger
from collections import Counter

logger = get_logger(__name__)

def clean_data(df, vaild_statue, vaild_category):
  clean_df = df.copy()
  clean_df['amount'] = pd.to_numeric(clean_df['amount'], errors='coerce')
  clean_df['order_date'] = pd.to_datetime(clean_df['order_date'], errors='coerce')

  clean_df = clean_df[clean_df['amount'] > 0]
  clean_df = clean_df.dropna(subset=['amount', 'order_date', 'seller', 'category', 'status'])
  vaild_statue = handle_statue(vaild_statue)
  vaild_category = handle_statue(vaild_category)
  if len(vaild_statue) > 0:
    clean_df = clean_df[clean_df['status'].isin(vaild_statue)]
  if len(vaild_category) > 0:
    clean_df = clean_df[clean_df['category'].isin(vaild_category)]
  else:
    logger.error('valid_category 不能为空')
    raise ValueError('valid_category 不能为空')
  logger.info('数据已经清洗完成，清洗后的数据长度为%s, 原始数据长度为%s, 脏数据长度为%s', len(clean_df), len(df), len(df) - len(clean_df))
  return clean_df

def handle_statue(vaild_statue):
  if vaild_statue is None:
    return []
  if isinstance(vaild_statue, str):
    _vaild_statue = []
    for s in vaild_statue.split(','):
      if s.strip():
        _vaild_statue.append(s.strip())
    return _vaild_statue
  elif isinstance(vaild_statue, list):
    return vaild_statue
  else:
    logger.error('valid_statue must be a string or a list, but got %s', type(vaild_statue))
    return []




# day 9
# 目标
# 数据清洗
# 异常数据明细
# 异常原因统计

REQUIRED_COLUMNS = ["amount", "order_date", "seller", "category", "status"]

def clean_df_data(df, valid_statuses, valid_categories):
  work_df = df.copy();
  raw_count = len(work_df)

  missing_columns = [col for col in REQUIRED_COLUMNS if col not in work_df.columns]
  if missing_columns:
    logger.error('数据缺失列: %s', missing_columns)
    raise ValueError('数据缺失列: %s', missing_columns)
  
  origin_amount = work_df['amount'].copy()
  origin_date = work_df['order_date'].copy()
  # 转成数字；转不了变成 NaN（不报错）
  work_df['amount'] = pd.to_numeric(work_df['amount'], errors='coerce')
  work_df['order_date'] = pd.to_datetime(work_df['order_date'], errors='coerce')
  # not() 不是空， isna() 是空， & 与
  # 这个的意思是专门抓取有值但是转换失败了，说明是格式问题
  amount_invalid_mask = origin_amount.notna() & work_df['amount'].isna()
  order_date_invalid_mask = origin_date.notna() & work_df['order_date'].isna()

  # .any(axis=1)任何一列是空，就标记为 True
  required_missing_mask = work_df[REQUIRED_COLUMNS].isna().any(axis=1)

  amount_not_positive_mask = work_df['amount'].notna() & (work_df['amount'] <= 0)
  _valid_statuses = handle_statue(valid_statuses)
  _valid_categories = handle_statue(valid_categories)
  status_invalid_mask = (
    work_df["status"].notna()
    & ~work_df["status"].isin(_valid_statuses)
  )

  category_invalid_mask = (
    work_df["category"].notna()
    & ~work_df["category"].isin(_valid_categories)
  )

  quality_records = []

  def add_quality_records(mask, reason):
    for idx in work_df[mask].index:
      row = work_df.loc[idx].to_dict()
      row["row_index"] = idx
      row["reason"] = reason
      quality_records.append(row)

  add_quality_records(amount_invalid_mask, "amount_invalid")
  add_quality_records(order_date_invalid_mask, "order_date_invalid")
  add_quality_records(required_missing_mask, "required_missing")
  add_quality_records(amount_not_positive_mask, "amount_not_positive")
  add_quality_records(status_invalid_mask, "status_invalid")
  add_quality_records(category_invalid_mask, "category_invalid")

  invalid_mask = (
    amount_invalid_mask
    | order_date_invalid_mask
    | required_missing_mask
    | amount_not_positive_mask
    | status_invalid_mask
    | category_invalid_mask
  )

  clean_df = work_df[~invalid_mask].copy()
  data_quality = pd.DataFrame(quality_records)

  if data_quality.empty:
    quality_summary = pd.DataFrame(columns=["reason", "count"])
  else:
    quality_summary = (
      data_quality.groupby("reason")
      .size()
      .reset_index(name="count")
    )

  logger.info(
    "数据清洗完成，原始数据 %s 条，清洗后 %s 条，异常记录 %s 条",
    raw_count,
    len(clean_df),
    len(data_quality),
  )

  return {
    'clean_df': clean_df,
    'data_quality': data_quality,
    'quality_summary': quality_summary
  }




# def check_amount(df, index,issues_data):
#   if pd.isna(df['amount']):
#     issues_data.append(
#       {
#         'index': index,
#         'field': 'amount',
#         'value': df['amount'],
#         'issue': '金额不合法',
#       }
#     )
#   elif df['amount'] <= 0:
#     issues_data.append(
#       {
#         'index': index,
#         'field': 'amount',
#         'value': df['amount'],
#         'issue': '金额小于0',
#       }
#     )
#   return issues_data

# def check_date(df, index,issues_data):
#   if pd.isna(pd.to_datetime(df['order_date'], errors='coerce')):
#     issues_data.append({
#       "index": index,
#       "field": 'order_date',
#       "value": df['order_date'],
#       "issue": '日期不合法',
#     })
#   return issues_data

# def check_required_fields(df, index,issues_data):
#   for field in REQUIRED_COLUMNS:
#     if pd.isna(df[field]):
#       issues_data.append({
#         'index': index,
#         'field': field,
#         'value': df[field],
#         'issue': '必填字段为空',
#       })
#   return issues_data

# def check_status(df, index, issues_data, vaild_statue):
#   if pd.isna(df['status']) and df['status'] not in vaild_statue:
#     issues_data.append({
#       "index": index,
#       "field": 'status',
#       "value": df['status'],
#       "issue": '状态不合法',
#     })
#   return issues_data

# def check_category(df, index,issues_data, vaild_category):
#   if pd.isna(df['category']) and df['category'] not in vaild_category:
#     issues_data.append({
#       "index": index,
#       "field": 'category',
#       "value": df['category'],
#       "issue": '类目不合法',
#     })
#   return issues_data

# def check_duplicate(df, index,issues_data):
#   if df.duplicated():
#     issues_data.append({
#       "index": index,
#       "field": 'duplicate',
#       "value": df.duplicated(),
#       "issue": '重复数据',
#     })
#   return issues_data

# def reason(issues_data):
#   issue_stats = Counter(item['issue'] for item in issues_data)
#   quality_records = [
#     {'issue': reason, 'count': count}
#     for reason, count in issue_stats.items()
#   ]
#   return quality_records
