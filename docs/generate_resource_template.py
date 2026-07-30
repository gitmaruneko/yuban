from openpyxl import Workbook
from openpyxl.styles import Font
import csv
from pathlib import Path

out_xlsx = Path('docs/resource-template.xlsx')
out_csv = Path('docs/resource-template.csv')

headers = [
    '資源名稱',
    '連結',
    '摘要',
    '內容類型',
    '提供方／來源類型',
    '原始來源',
    '是否為入口型資源',
    '年齡階段',
    '主題',
    '關鍵標籤',
    '審核狀態',
    '可信度備註',
    '注意事項'
]

rows = [
    [
        '政府育兒資源入口範例',
        'https://welfare.gov.taipei/Kids/Home/Index',
        '台北市政府提供的兒童與家庭資源入口頁',
        '連結入口',
        '政府',
        '台北市政府',
        '是',
        '全齡',
        '生活照護',
        '政府資源, 入口頁',
        '人工核實',
        '政府機構發布，內容可作為入口參考',
        '請以官方資訊為主，必要時再確認最新內容'
    ],
    [
        '新生兒睡眠基礎指南',
        'https://example.com/sleep',
        '介紹新生兒睡眠節律與安全睡眠做法',
        '文章',
        '個人創作者',
        'Parenting Blog',
        '否',
        '0–1歲',
        '睡眠',
        '新生兒, 安撫',
        'AI 整理・待人工核實',
        '內容需再確認來源可信度',
        '請以實際原始來源為準'
    ]
]

wb = Workbook()
ws = wb.active
ws.title = '資源清單'
ws.append(headers)
for row in rows:
    ws.append(row)

for cell in ws[1]:
    cell.font = Font(bold=True)

for col in ws.columns:
    max_len = 0
    for cell in col:
        if cell.value is not None:
            max_len = max(max_len, len(str(cell.value)))
    ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 50)

wb.save(out_xlsx)

with out_csv.open('w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f'Generated {out_xlsx}')
print(f'Generated {out_csv}')
