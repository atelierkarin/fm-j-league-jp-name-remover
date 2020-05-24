import xml.etree.ElementTree as et
import unicodedata

def is_japanese(string):
  for ch in string:
    name = unicodedata.name(ch) 
    if "CJK UNIFIED" in name \
    or "HIRAGANA" in name \
    or "KATAKANA" in name:
      return True
  return False

def remove_japanese_name(source_file, output_file='result.xml', debug=False):
  tree = et.parse(source_file)
  l = tree.find("list[@id='db_changes']")
  remove_records = []

  for record in l.findall('record'):
    unsigned = record.find("unsigned[@id='property']")
    remove_records.append("Record = {}".format(unsigned.attrib['value']))
    # 日本語表記はCommon Name、IDは1348693601
    if unsigned.attrib['value'] == '1348693601':
      common_name = record.find("string[@id='new_value']")
      common_name_value = common_name.attrib['value']
      remove_records.append("Value = {}, Japanese? = {}".format(common_name_value, is_japanese(common_name_value)))
      if is_japanese(common_name_value):
        l.remove(record)
  tree.write(output_file, encoding='utf-8')

  # デバッグモードではファイルを出力
  if debug:
    with open("debug.txt", 'wt', encoding='utf-8') as f:
      for val in remove_records:
        f.writelines("{}\n".format(val))

remove_japanese_name('./data/j-league-player-1.xml', './formatted/j-league-player-1.xml')