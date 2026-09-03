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
    '注意事項',
    '年齡群組',
    '地區',
    '資源類型',
    '使用對象',
    '來源地區',
    '語言'
]

rows = [
    [
        '孕產兒關懷網站',
        'https://mammy.hpa.gov.tw/',
        '整合孕前、孕期、產後與嬰幼兒照護資訊的官方資源入口',
        '連結入口',
        '政府',
        '衛生福利部國民健康署',
        '是',
        '孕前–2歲',
        '孕產與嬰幼兒照護',
        '孕產婦, 新生兒, 母乳, 諮詢',
        '人工核實',
        '中央主管機關官方網站',
        '供衛教與資源查找；急症或個別醫療問題應立即就醫。',
        '學齡前',
        '全國',
        '機構',
        '家長',
        '台灣',
        '繁體中文'
    ],
    [
        '兒童衛教手冊',
        'https://www.hpa.gov.tw/Pages/EBook.aspx?nodeid=1459',
        '提供嬰幼兒照護、營養與事故傷害預防等家長衛教內容',
        '文章',
        '政府',
        '衛生福利部國民健康署',
        '否',
        '0–6歲',
        '健康與生活照護',
        '新生兒, 安全睡眠, 營養',
        '人工核實',
        '政府機構正式出版的家長衛教手冊',
        '下載或引用前請確認頁面上的最新出版年月。',
        '學齡前',
        '全國',
        '學習教材',
        '家長',
        '台灣',
        '繁體中文'
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
