# 目标：
# 新增字段映射

import logging
from logginger import get_logger
import pandas as pd

logger = get_logger(__name__)

COLUNM_MAP = {
  "订单日期": "order_date",
  "订单编号": "order_id",
  "订单状态": "status",
  "类目": "category",
  "销售代表": "seller",
  "销售金额": "amount",
}

# 定义一个方法，这个方法的参数是原始的df，返回值是映射后的df
def map_fields(df):
  # 遍历COLUNM_MAP，如果原始的df中存在这个key，则将这个key的值映射到新的df中
  map_field_df = pd.DataFrame();
  for key, value in COLUNM_MAP.items():
    if key in df.columns:
      map_field_df[value] = df[key]
    else:
      # map_field_df[key] = df[key]
      logger.warning(f"列{key}不存在")
  if map_field_df.empty:
    logger.warning('没有找到任何映射的列, 返回原始列表')
    map_field_df = df.copy();
  logger.info('字段映射完成')
  return map_field_df

def normalize_columns(df):
  """
    将中文业务字段映射为程序标准字段
    未出现在映射字段中的字段也会被保存
  """
  map_columns = {
    col: COLUNM_MAP[col]
    for col in df.columns
    if col in COLUNM_MAP
  }

  if not map_columns:
    logging.error('没有找到任何映射的列, 返回原始列表')
    return df.copy()
  logger.info('字段映射完成')
  logger.info('映射后的列为%s', map_columns.values())
  return df.rename(columns=map_columns)
