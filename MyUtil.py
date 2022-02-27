import re

def com_replace(_s):
  '''
  dashではidに","（カンマ）は使えないため置換する。
  ※カンマをそのまま置換するとjson形式が崩れるため注意が必要
  ※(1, 1)->1
  
  '''
  pattern = r'(\d{1,4}?), (\d{1,4}?)'
  result = re.sub(pattern, r'\1_\2', str(_s))
  return result 