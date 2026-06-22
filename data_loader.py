import pandas as pd
from pathlib import Path

def  load_data(data_path):
  if not Path(data_path).exists():
    raise FileNotFoundError(f'文件不存在: {data_path}')
  elif Path(data_path).suffix.lower() != '.csv':
    raise ValueError(f'文件格式错误: {data_path}')
  return pd.read_csv(data_path, encoding='utf-8-sig')
