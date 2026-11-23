"""Official / public feeds used by the biweekly crawler.

Google News RSS is used as a public index of official-domain coverage
(not a login bypass). Direct RSS is used where the agency publishes one.
"""

TOPIC_QUERY = (
    "(employment OR labour OR labor OR wage OR payroll OR visa "
    "OR immigration OR CPF OR superannuation OR leave OR OSHA "
    "OR 最低工资 OR 劳动合同 OR 雇佣)"
)

SOURCES = [
    {"country": "CN", "flag": "🇨🇳", "name": "MOHRSS", "site": "mohrss.gov.cn",
     "home": "https://www.mohrss.gov.cn/"},
    {"country": "JP", "flag": "🇯🇵", "name": "MHLW", "site": "mhlw.go.jp",
     "home": "https://www.mhlw.go.jp/"},
    {"country": "KR", "flag": "🇰🇷", "name": "MOEL", "site": "moel.go.kr",
     "home": "https://www.moel.go.kr/"},
    {"country": "SG", "flag": "🇸🇬", "name": "MOM", "site": "mom.gov.sg",
     "home": "https://www.mom.gov.sg/"},
    {"country": "HK", "flag": "🇭🇰", "name": "Labour Dept", "site": "labour.gov.hk",
     "home": "https://www.labour.gov.hk/"},
    {"country": "TW", "flag": "🇹🇼", "name": "MOL", "site": "mol.gov.tw",
     "home": "https://www.mol.gov.tw/"},
    {"country": "AU", "flag": "🇦🇺", "name": "Fair Work", "site": "fairwork.gov.au",
     "home": "https://www.fairwork.gov.au/",
     "rss": ["https://www.fairwork.gov.au/about-us/newsroom/rss"]},
    {"country": "NZ", "flag": "🇳🇿", "name": "Employment NZ", "site": "employment.govt.nz",
     "home": "https://www.employment.govt.nz/"},
    {"country": "IN", "flag": "🇮🇳", "name": "Labour India", "site": "labour.gov.in",
     "home": "https://labour.gov.in/"},
    {"country": "SEA", "flag": "🌏", "name": "MOLISA Vietnam", "site": "molisa.gov.vn",
     "home": "https://www.molisa.gov.vn/"},
    {"country": "SEA", "flag": "🌏", "name": "DOL Thailand", "site": "dol.go.th",
     "home": "https://www.dol.go.th/"},
    {"country": "SEA", "flag": "🌏", "name": "Kemnaker", "site": "kemnaker.go.id",
     "home": "https://www.kemnaker.go.id/"},
    {"country": "SEA", "flag": "🌏", "name": "DOLE", "site": "dole.gov.ph",
     "home": "https://www.dole.gov.ph/"},
    {"country": "SEA", "flag": "🌏", "name": "MOHR Malaysia", "site": "mohr.gov.my",
     "home": "https://www.mohr.gov.my/"},
]

TYPE_RULES = [
    ("Wages", ("minimum wage", "最低工资", "basic wage", "hourly rate", "pwm", "pay rise", "pay increase")),
    ("Social Insurance", ("cpf", "epf", "superannuation", "社会保险", "pension", "insurance contribution", "工伤")),
    ("Foreign Workers", ("employment pass", "work permit", "visa", "foreign worker", "immigration", "ep ", "s pass")),
    ("AI & Tech", ("artificial intelligence", " ai ", "algorithm", "automation")),
    ("Workplace Safety", ("ohs", "osha", "workplace safety", "occupational safety", "ergonomic")),
    ("Leave", ("parental leave", "paternity", "maternity", "childcare leave", "annual leave", "disconnect")),
    ("Contracts", ("contract", "dismissal", "redundancy", "workweek", "hours of work", "casual", "gig")),
]

CRITICAL_WORDS = (
    "minimum wage", "mandatory", "penalty", "enforcement", "fine",
    "must", "effective immediately", "nationwide", "critical",
)
WATCH_WORDS = ("draft", "consult", "proposed", "pending", "review", "tbd")
UPCOMING_WORDS = ("will take effect", "from 2027", "from 2028", "upcoming", "to commence")
