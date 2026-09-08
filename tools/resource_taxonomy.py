"""Canonical supported stages and topic-to-group mappings for YuBan resources."""

from __future__ import annotations


ALLOWED_AGE_STAGES = frozenset(
    {"備孕", "孕期", "0-1歲", "1-3歲", "3-6歲", "國小", "國中", "高中", "成人", "全齡"}
)

# A topic belongs to exactly one existing topic group. This preserves legacy
# topics while making the supported taxonomy explicit at the data boundary.
TOPIC_GROUPS = {
    "綜合育兒": "親職與家庭",
    "健康與安全": "健康與照護",
    "健康與發展": "健康與照護",
    "學習與教育": "發展與學習",
    "學習與閱讀": "發展與學習",
    "情緒與行為": "情緒與心理",
    "托育與幼兒園": "托育與服務",
    "托育 與幼兒園": "托育與服務",
    "發展與早療": "發展與學習",
    "睡眠": "健康與照護",
    "補助與權益": "親職與家庭",
    "親子互動與教養": "親職與家庭",
    "親子活動": "親職與家庭",
    "遊戲與學習": "發展與學習",
    "飲食與營養": "健康與照護",
    "孕產與嬰幼兒照護": "健康與照護",
    "健康與生活照護": "健康與照護",
    "預防接種": "健康與照護",
    "兒童預防保健": "健康與照護",
    "新生兒照護": "健康與照護",
    "兒童健康": "健康與照護",
    "母乳哺育": "健康與照護",
    "兒童就醫資源": "健康與照護",
    "生長發育": "健康與照護",
    "視力保健": "健康與照護",
    "兒童口腔保健": "健康與照護",
    "兒科疾病與照護": "健康與照護",
    "兒科疾病衛教": "健康與照護",
    "早產兒照護": "健康與照護",
    "兒童發展篩檢": "發展與學習",
    "早期療育": "發展與學習",
    "幼兒園與學前教保": "發展與學習",
    "課後照顧": "發展與學習",
    "兒童發展與早療": "發展與學習",
    "親子共讀": "發展與學習",
    "親職知能": "親職與家庭",
    "補助與家庭支持": "親職與家庭",
    "親職與家庭關係": "親職與家庭",
    "親職教養與家庭支持": "親職與家庭",
    "兒童事故傷害預防": "安全與保護",
    "兒少保護": "安全與保護",
    "兒童權利": "安全與保護",
    "兒少網路安全": "安全與保護",
    "托育媒合": "托育與服務",
    "兒童青少年心理健康": "情緒與心理",
    "注意力與過動（ADHD）": "發展與學習",
    "備孕與生殖": "健康與照護",
    "孕期健康": "健康與照護",
    "兒童健康與醫療": "健康與照護",
    "發展與早期支持": "發展與學習",
}

# Reviewed workbooks may use a narrow user need as their topic. Normalize those
# labels at the import boundary so the public index remains compact and uses
# its established topic vocabulary.
IMPORT_TOPIC_ALIASES = {
    "高齡妊娠": "孕產與嬰幼兒照護",
    "人工受孕": "備孕與生殖",
    "唇顎裂": "兒科疾病與照護",
    "早療": "發展與早療",
    "ADHD": "注意力與過動（ADHD）",
}
