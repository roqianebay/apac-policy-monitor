#!/usr/bin/env python3
"""Build web/data/policy-zh.json from policies.json + bundled Chinese copy."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICIES = ROOT / "web" / "data" / "policies.json"
OUT = ROOT / "web" / "data" / "policy-zh.json"

# Curated seed entries (cn1–sea5) — full title + body
SEED_ZH = {
    "cn1": {
        "title": "劳动合同电子化备案系统上线",
        "body": "用人单位须通过全国电子平台备案劳动合同，2026年7月1日后签订的书面纸质备案不再受理。",
    },
    "cn2": {
        "title": "灵活就业职业伤害保障全国推行",
        "body": "平台灵活就业人员纳入职业伤害保障；使用平台用工的雇主须登记并缴费。",
    },
    "cn3": {
        "title": "招聘场景 AI 伦理指引（草案）",
        "body": "使用 AI 筛选的雇主须向候选人披露，并应其要求安排人工复核。",
    },
    "cn4": {
        "title": "2026 年度社保缴费基数调整",
        "body": "各省市公布 2026 年社保缴费基数上下限，雇主应按新基数核对缴费。",
    },
    "jp1": {
        "title": "最低工资：全国平均约 ¥1,055/小时",
        "body": "全国平均最低工资由 ¥1,004 上调至 ¥1,055/小时，进入执行周期，请核对时薪与兼职工资。",
    },
    "jp2": {
        "title": "中小企业育儿休业制度扩展",
        "body": "员工不足 300 人的中小企业须与大企业同等提供育儿休业安排。",
    },
    "jp3": {
        "title": "裁量劳动制改革",
        "body": "扩大适用职种并加强健康管理义务；采用该制度的雇主须更新协议。",
    },
    "jp4": {
        "title": "特定技能外国人分野扩大（征询中）",
        "body": "拟将电子制造、 hospitality 等纳入特定技能 2 号，目前公开征求意见。",
    },
    "kr1": {
        "title": "最低工资上调 2.9% → 韩元 10,320/小时",
        "body": "最低工资由 10,030 调至 10,320 韩元/小时，请更新合同与 payroll。",
    },
    "kr2": {
        "title": "每周 52 小时工时制 — 处罚加强",
        "body": "监察部门提高违规定额罚款，制造与 IT 行业为重点检查对象。",
    },
    "kr3": {
        "title": "非正式用工比例报告义务",
        "body": "300 人以上企业须向劳动部报告非正式用工比例，增强透明度。",
    },
    "kr4": {
        "title": "育儿津贴上限升至每月 250 万韩元",
        "body": "前 3 个月育儿津贴上限由 150 万提至 250 万韩元，鼓励男性休假。",
    },
    "kr5": {
        "title": "雇佣保险费率审查（征求意见）",
        "body": "劳动部拟调整雇佣保险费率以支撑延长育儿福利，预计 2026 Q3 定论。",
    },
    "sg1": {
        "title": "就业准证起薪：大企业 S$5,600 / 中小企业 S$5,000",
        "body": "2025 年 9 月起 EP 达标薪资调整；金融业门槛 S$6,200。续签与申请须满足新标准。",
    },
    "sg2": {
        "title": "大型雇主须做 AI 影响评估",
        "body": "25 人以上且用 AI 做 HR 决策的雇主须年度评估并向员工说明。",
    },
    "sg3": {
        "title": "渐进式加薪模式扩展至零售",
        "body": "零售业纳入 PWM，雇主须按技能与生产力阶梯调薪。",
    },
    "sg4": {
        "title": "55–60 岁员工公积金缴费率上调",
        "body": "该年龄段 CPF 总缴费率升至 37%，请更新 payroll。",
    },
    "sg5": {
        "title": "灵活工作安排 — 强制申请与回复流程",
        "body": "雇主须建立正式 FWA 申请-回复机制；拒绝须书面说明业务理由。",
    },
    "hk1": {
        "title": "法定最低工资 → 港币 40/小时",
        "body": "最低工资由 37.50 升至 40 港元/小时，请核对时薪岗位与外包合约。",
    },
    "hk2": {
        "title": "非本地毕业生 IANG 安排优化",
        "body": "雇主须为 IANG 持有人提供结构化导师与培训计划。",
    },
    "hk3": {
        "title": "侍产假由 5 日延长至 10 日（立法进程中）",
        "body": "相关法案完成首读，预计 2027 Q1 生效。",
    },
    "tw1": {
        "title": "基本工资 → 新台币 28,590/月（190/小时）",
        "body": "月薪由 27,470 调至 28,590 元，时薪 190 元，2025 年 1 月起适用。",
    },
    "tw2": {
        "title": "陪产假延长至 7 日",
        "body": "法定陪产假由 5 日增至 7 日，2026 年 1 月起登记出生适用。",
    },
    "tw3": {
        "title": "办公室人员人因风险评核（草案）",
        "body": "50 人以上办公室须做人因风险评估，目前征询意见。",
    },
    "au1": {
        "title": "全国最低工资上调 3.75% → 澳元 24.10/小时",
        "body": "F WC 将最低工资由 23.23 调至 24.10 澳元/小时，Modern Award 同步上调，2026 年 7 月 1 日生效。",
    },
    "au2": {
        "title": "「断开连接权」全面适用含小微企业",
        "body": "员工可拒绝不合理的非工作时间联系；雇主须书面政策，小企业亦适用。",
    },
    "au3": {
        "title": "养老金保证比例 11.5% → 12%",
        "body": "2026 年 7 月 1 日起 SG 升至 12%，请立即更新 payroll 系统。",
    },
    "au4": {
        "title": "临时雇员定义改革",
        "body": "以实际用工性质界定临时工；满 6 个月可申请转永久，不受合同文字限制。",
    },
    "au5": {
        "title": "薪酬透明 — 讨论工资权利",
        "body": "员工有权交流薪酬信息，雇主不得禁止，请检查合同条款。",
    },
    "au6": {
        "title": "零工平台最低标准（观望）",
        "body": "拟设最低收入底线及算法派工透明度等最低标准。",
    },
    "nz1": {
        "title": "最低工资 → 新西兰元 23.50/小时",
        "body": "最低工资由 22.70 调至 23.50 元/小时，入门级与培训工资同比例上调。",
    },
    "nz2": {
        "title": "90 天试用期再度扩大至全部雇主",
        "body": "试用期由仅小企业扩展至所有规模雇主（2023 年 12 月起）。",
    },
    "in1": {
        "title": "EPFO：Provident Fund 工资门槛拟由 1.5 万调至 2.1 万卢比",
        "body": "强制 PF 登记门槛若上调将显著扩大雇主义务，尚待正式通知。",
    },
    "in2": {
        "title": "四部劳动法典 — 各邦实施进度",
        "body": "各邦公布细则时间不一，跨邦雇主须分市场跟踪。",
    },
    "sea1": {
        "title": "越南：最低工资上调 6% — 一类区 VND 496 万/月",
        "body": "2025 年 7 月 1 日起四区统一上调 6%，河内/胡志明一类区 VND 496 万/月。",
    },
    "sea2": {
        "title": "泰国：工作许可数字化 — 7 个工作日",
        "body": "一站式数字平台上线，多数类别工作许可 7 个工作日内办结。",
    },
    "sea3": {
        "title": "印尼：综合法雇佣条款执行",
        "body": "定期合同最长合计 5 年；遣散费计算依宪法法院裁决厘清。",
    },
    "sea4": {
        "title": "菲律宾：远程办公法 — 须备正式政策",
        "body": "有远程员工的雇主须提供符合最低标准的远程办公政策（含加班与设备）。",
    },
    "sea5": {
        "title": "马来西亚：2026 最低工资年度审查",
        "body": "现行 MYR 1,500/月，预计 2026 Q3 公布新版本。",
    },
}

CRAWL_ZH = {
    "crawl-jp-80109e582d7e": {
        "title": "日法务省·厚劳省：技能实习就业合作备忘录",
        "body": "法务省与厚生劳动省就技能实习就业项目签署合作备忘录（厚劳省发布）。",
    },
    "crawl-sg-29dacbf20e26": {
        "title": "新加坡人力部：工资实务指引",
        "body": "人力部更新工资实务相关公开信息。",
    },
    "crawl-sg-2a9049e5b96a": {
        "title": "新加坡人力部：病假",
        "body": "医疗病假政策与雇主指引。",
    },
    "crawl-sg-26ead3ff49a5": {
        "title": "新加坡人力部：劳动力",
        "body": "劳动力市场与就业统计公开页。",
    },
    "crawl-sg-eb59bcbaccd9": {
        "title": "新加坡人力部：2026 年公积金补缴通知",
        "body": "CPF 相关补缴与 employer 通知（B2026）。",
    },
    "crawl-sg-e5fa39e6a02c": {
        "title": "新加坡人力部：CIVIC-AI 与未来劳动研讨会",
        "body": "协作智能与未来劳动（CIVIC-AI）研讨活动。",
    },
    "crawl-sg-5d0a8377e578": {
        "title": "新加坡人力部：年度工资变动",
        "body": "年度工资调整与劳动力调查信息。",
    },
    "crawl-sg-df185e28f8cb": {
        "title": "新加坡人力部：雇佣条件",
        "body": "雇佣条件合规与雇主须知。",
    },
    "crawl-sg-862ec1215a82": {
        "title": "新加坡 2025 劳动力报告：居民跳槽与转岗结果",
        "body": "《2025 劳动力》报告：居民就业流动性与转岗结果。",
    },
    "crawl-hk-7d43a2036c76": {
        "title": "2026 劳工咨询委员会雇主代表选举 — 获授权代表名单",
        "body": "劳工咨询委员会选举相关雇主代表任命名单。",
    },
    "crawl-hk-6f4408067477": {
        "title": "香港劳工处：加强补充劳工计划",
        "body": "补充劳工输入计划优化安排。",
    },
    "crawl-hk-d270c9f6ed18": {
        "title": "香港劳工处：指引说明（C 部分）",
        "body": "雇主合规指引文件 C 部分。",
    },
    "crawl-hk-27751c857910": {
        "title": "香港劳工处：要点摘要",
        "body": "劳工处近期政策与服务要点。",
    },
    "crawl-hk-2c1ef9477125": {
        "title": "香港劳工处：外籍家庭佣工雇主网上简介会",
        "body": "面向外籍家庭佣工雇主的在线简介会。",
    },
    "crawl-au-cdaed39a283d": {
        "title": "NAB 欠薪 1.27 亿澳元后签署可执行承诺",
        "body": "公平工作监察专员：NAB 签署 Enforceable Undertaking。",
    },
    "crawl-au-42a387b5baa6": {
        "title": "新州劳务中介因侵害移民采摘工被处罚",
        "body": "公平工作监察专员处罚劳务雇佣违规行为。",
    },
    "crawl-au-13d21073f10a": {
        "title": "家庭与家庭暴力假 — 概述",
        "body": "公平工作监察专员：FDV 假 entitlement 说明。",
    },
    "crawl-au-15e6042d69b2": {
        "title": "个人休假（personal leave）",
        "body": "个人/年假 sick leave 相关规定。",
    },
    "crawl-au-5b945f4c3503": {
        "title": "最低工资",
        "body": "澳大利亚全国最低工资与 Modern Award 指引。",
    },
    "crawl-au-38eb3c80d8e0": {
        "title": "各类休假",
        "body": "公平工作监察专员：休假类型总览。",
    },
    "crawl-au-cb2782d18db0": {
        "title": "如何请家庭与家庭暴力假",
        "body": "员工申请 FDV 假的程序说明。",
    },
    "crawl-au-1d07758fd14f": {
        "title": "FDV 假：通知与证据要求",
        "body": "雇主与员工在 FDV 假下的通知、举证要求。",
    },
    "crawl-nz-14884c57768d": {
        "title": "MBIE 吉斯本就业与移民风险专项执法",
        "body": "商业、创新与就业部在吉斯本地区执法行动。",
    },
    "crawl-nz-b5e33c539fc5": {
        "title": "就业争议早期调解",
        "body": "Employment New Zealand：早期解决机制。",
    },
    "crawl-nz-24d6717cc93c": {
        "title": "雇主签证停审报告（2026-11-19）",
        "body": "签证 stand-down 相关雇主合规报告。",
    },
    "crawl-in-90e435516504": {
        "title": "四部劳动法典与中央规则常见问题",
        "body": "印度劳动与就业部：新法典 FAQ 汇编。",
    },
    "crawl-in-a1319caed6ec": {
        "title": "工资委员会",
        "body": "工资委员会相关通知与机制。",
    },
    "crawl-in-6a8557046ba8": {
        "title": "印度劳动与就业部首页动态",
        "body": "劳动就业部官网最新公开信息。",
    },
    "crawl-in-3ffcf4b5a7da": {
        "title": "妇女儿童劳动",
        "body": "妇幼劳动保护与合规专题。",
    },
    "crawl-in-89698f50bdfc": {
        "title": "劳动就业部站内检索",
        "body": "政策与通告检索入口。",
    },
    "crawl-in-8fc3010db257": {
        "title": "法案与政策",
        "body": "劳动领域法案与政策汇编。",
    },
    "crawl-in-3200a982ec3b": {
        "title": "劳动法院案件公示（新德里）",
        "body": "劳动法院 II（新德里）案件编号 182/2018 等公示。",
    },
    "crawl-in-82091fba13ab": {
        "title": "劳动法院案件 L.C. No.3/24",
        "body": "劳动法院 2024 年第 3 号案件（2026-11-16）。",
    },
    "crawl-sea-3b3a87c8e0d1": {
        "title": "菲律宾劳动就业部（DOLE）",
        "body": "DOLE 官网政策与新闻入口。",
    },
    "crawl-sea-292ddde8e7d5": {
        "title": "DOLE 主持第 6 届 ALICOM 劳工监察会议",
        "body": "东盟劳工监察合作机制（ALICOM）会议成果。",
    },
    "crawl-sea-d0c02258e1e1": {
        "title": "DOLE 劳工研究所参与东盟劳动力市场数据论坛",
        "body": "ILS 参与改进劳动力市场数据使用方式的区域论坛。",
    },
    "crawl-sea-211aaa1e6876": {
        "title": "ILS 赴意参加全球就业影响评估论坛",
        "body": "国际劳工组织学院 EmpIA 体面劳动影响评估论坛。",
    },
    "crawl-sea-ffa779f6100e": {
        "title": "DOLE 北棉兰老：中小微企业劳工关系赋能",
        "body": "通过 WODP 与 LEES 加强劳资关系。",
    },
    "crawl-sea-876a174a2af0": {
        "title": "DOLE 与糖业三方委员会对话劳工挑战",
        "body": "糖业劳资议题三方磋商。",
    },
    "crawl-sea-17d0830241ae": {
        "title": "第 15 届 ALIC：劳工监察挑战与区域合作",
        "body": "东盟劳工监察合作（ALIC）会议议题。",
    },
    "crawl-sea-ccdb21776536": {
        "title": "DOLE 首都区 2025 PRAISE 表彰",
        "body": "首都区劳工部 PRAISE 员工与办公室表彰。",
    },
}


def main():
    data = json.loads(POLICIES.read_text(encoding="utf-8"))
    out = {}
    missing = []
    for p in data.get("policies", []):
        pid = p["id"]
        if pid in SEED_ZH:
            out[pid] = SEED_ZH[pid]
        elif pid in CRAWL_ZH:
            out[pid] = CRAWL_ZH[pid]
        else:
            missing.append(pid)
            out[pid] = {
                "title": f"【{p.get('country', '')}】{p['title'][:80]}",
                "body": p.get("body", p["title"])[:240],
            }
    if missing:
        print("Warning: fallback zh for ids:", missing)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(out)} entries -> {OUT}")


if __name__ == "__main__":
    main()