"""Builds the profile README images (light + dark) into this folder.

Run:  python assets/build_assets.py
Edit the data blocks below, re-run, commit the SVGs.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
FONT = "Segoe UI, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace"

THEMES = {
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", title="#1f2328",
                  body="#59636e", chip="#f6f8fa", chip_border="#d0d7de", chip_text="#1f2328",
                  grid="#eaeef2"),
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", title="#e6edf3",
                 body="#9198a1", chip="#21262d", chip_border="#30363d", chip_text="#e6edf3",
                 grid="#161b22"),
}

C = dict(databricks="#FF3621", snowflake="#29B5E8", fabric="#0F8A7E", microsoft="#0078D4",
         sqlserver="#CC2927", oracle="#C74634", web3="#8B5CF6", dbt="#FF694B")


def w(text, size, bold=False):
    """Approximate rendered width of text in px."""
    return len(text) * size * (0.56 if bold else 0.5)


def wrap(text, size, width, bold=False):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if w(trial, size, bold) > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def t(x, y, s, size, fill, weight=400, family=FONT, anchor="start", spacing=0, opacity=1):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}" opacity="{opacity}">'
            f'{escape(s)}</text>')


def chip(x, y, label, th, size=13, dot=None):
    pad = 10
    width = w(label, size) + pad * 2 + (14 if dot else 0)
    h = size + 12
    out = [f'<rect x="{x}" y="{y}" width="{width:.0f}" height="{h}" rx="{h/2}" fill="{th["chip"]}" '
           f'stroke="{th["chip_border"]}"/>']
    tx = x + pad
    if dot:
        out.append(f'<circle cx="{x + pad + 4}" cy="{y + h/2}" r="4" fill="{dot}"/>')
        tx += 14
    out.append(t(tx, y + h / 2 + size * 0.36, label, size, th["chip_text"], 500))
    return "".join(out), width


def svg(width, height, body, th, rounded=True):
    frame = (f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="{12 if rounded else 0}" '
             f'fill="{th["bg"]}" stroke="{th["border"]}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">{frame}{body}</svg>\n')


def save(name, builder):
    for mode, th in THEMES.items():
        (OUT / f"{name}-{mode}.svg").write_text(builder(th), encoding="utf-8")


# ---------------------------------------------------------------- banner
def banner(th):
    W, H = 1000, 250
    b = [f'<defs><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
         f'<stop offset="0" stop-color="{C["databricks"]}"/><stop offset="0.5" stop-color="{C["snowflake"]}"/>'
         f'<stop offset="1" stop-color="{C["fabric"]}"/></linearGradient>'
         f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
         f'<circle cx="2" cy="2" r="1.4" fill="{th["grid"]}"/></pattern>'
         f'<clipPath id="clip"><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12"/></clipPath></defs>',
         f'<g clip-path="url(#clip)"><rect x="560" y="0" width="440" height="{H}" fill="url(#dots)"/>'
         f'<rect x="0" y="0" width="{W}" height="6" fill="url(#accent)"/></g>']
    b.append(t(48, 64, "DATA ENGINEER  ·  DATABASE ENGINEER", 13, th["body"], 600, spacing=2))
    b.append(t(46, 118, "Sadrul Alom", 52, th["title"], 700))
    b.append(t(48, 154, "Principal Database Engineer — 15+ years building data platforms", 19, th["body"], 400))
    x = 48
    for label, color in [("Snowflake", C["snowflake"]), ("Databricks", C["databricks"]),
                         ("Microsoft Fabric", C["fabric"]), ("SQL Server", C["sqlserver"])]:
        s, cw = chip(x, 184, label, th, 14, color)
        b.append(s)
        x += cw + 10
    # certification stack on the right
    certs = [("DATABRICKS", "Data Engineer Professional", C["databricks"]),
             ("SNOWFLAKE", "SnowPro Core", C["snowflake"]),
             ("MICROSOFT", "Fabric Data Engineer · DP-700", C["microsoft"])]
    y = 46
    for issuer, name, color in certs:
        b.append(f'<rect x="640" y="{y}" width="312" height="52" rx="10" fill="{th["panel"]}" stroke="{th["border"]}"/>')
        b.append(f'<rect x="640" y="{y}" width="5" height="52" rx="2" fill="{color}"/>')
        b.append(t(662, y + 21, issuer, 11, color, 700, spacing=1.5))
        b.append(t(662, y + 40, name, 15, th["title"], 600))
        b.append(t(934, y + 32, "✓", 16, color, 700, anchor="end"))
        y += 62
    return svg(W, H, "".join(b), th)


# ---------------------------------------------------------------- certifications
CERTS = [
    ("Databricks", "Certified Data Engineer Professional", "Nov 2026", C["databricks"], True),
    ("Snowflake", "SnowPro Core (COF-C02)", "Certified", C["snowflake"], False),
    ("Microsoft", "Fabric Data Engineer Associate (DP-700)", "Certified", C["microsoft"], False),
    ("Microsoft", "Azure Database Administrator Associate (DP-300)", "Certified", C["microsoft"], False),
    ("Microsoft", "MCSE", "Certified", C["microsoft"], False),
    ("Oracle", "MySQL 8.0 Database Administrator", "Certified", C["oracle"], False),
]


def certs(th):
    W, cols, tw, th_, gap = 1000, 3, 320, 104, 20
    rows = (len(CERTS) + cols - 1) // cols
    H = rows * th_ + (rows - 1) * gap
    b = []
    for i, (issuer, name, when, color, new) in enumerate(CERTS):
        x = (i % cols) * (tw + gap)
        y = (i // cols) * (th_ + gap)
        b.append(f'<clipPath id="t{i}"><rect x="{x+0.5}" y="{y+0.5}" width="{tw-1}" height="{th_-1}" rx="12"/></clipPath>')
        b.append(f'<rect x="{x+0.5}" y="{y+0.5}" width="{tw-1}" height="{th_-1}" rx="12" fill="{th["bg"]}" stroke="{th["border"]}"/>')
        b.append(f'<rect x="{x}" y="{y}" width="{tw}" height="5" fill="{color}" clip-path="url(#t{i})"/>')
        b.append(t(x + 20, y + 32, issuer.upper(), 12, color, 700, spacing=1.5))
        if new:
            b.append(f'<rect x="{x+tw-100}" y="{y+18}" width="82" height="20" rx="10" fill="{color}"/>')
            b.append(t(x + tw - 59, y + 32, f"NEW · {when[-4:]}", 11, "#ffffff", 700, anchor="middle", spacing=0.5))
        lines = wrap(name, 16, tw - 40, True)[:2]
        for j, line in enumerate(lines):
            b.append(t(x + 20, y + 60 + j * 22, line, 16, th["title"], 600))
    body = "".join(b)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{body}</svg>\n')


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("facility-master", "SNOWFLAKE · MASTER DATA", "Facility Master",
     "Healthcare facility master: hospitals, hospices, SNFs, dialysis centres and ASCs matched against CMS registries, "
     "with a data-steward review app.",
     ["Snowflake tasks", "Streamlit in Snowflake", "Azure DevOps"], C["snowflake"], True),
    ("commercial-master", "SNOWFLAKE · COMMERCIAL DATA", "Commercial Master",
     "Customer and GPO price-activation records mapped to the hospital master, with branch coverage maps, "
     "review queue and QA audit.",
     ["Snowflake", "Streamlit", "Azure Pipelines"], C["snowflake"], True),
    ("careflow", "DATABRICKS · LAKEHOUSE", "CareFlow Lakehouse",
     "Healthcare data platform: clinical, claims and device telemetry through a governed medallion lakehouse with CI/CD.",
     ["Delta Live Tables", "Unity Catalog", "MLflow"], C["databricks"]),
    ("d365-fabric", "MICROSOFT FABRIC · MIGRATION", "D365 F&O → Fabric Lakehouse",
     "Dataverse Link to Fabric, shortcuts and Materialized Lake Views across bronze, silver and gold.",
     ["Dataverse", "MLVs", "Semantic model"], C["fabric"]),
    ("takarail", "BLOCKCHAIN · PAYMENTS", "TakaRail",
     "Payments infrastructure for Bangladesh: tokenised taka, Bangla QR, remittance corridors and a double-entry ledger.",
     ["Solidity", "Fastify", "PostgreSQL", "React"], C["web3"]),
    ("rwa", "BLOCKCHAIN · TOKENISATION", "RWA Tokenization Platform",
     "Real estate, private credit and fund shares with ERC-3643-style compliance, KYC registry and income distribution.",
     ["Foundry", "NestJS", "Ponder", "Next.js"], C["web3"]),
    ("dataledger", "BLOCKCHAIN · DATA GOVERNANCE", "DataLedger",
     "Blockchain-anchored data management: Merkle-proof versioning, lineage, purpose-bound access and crypto-shredding.",
     ["Solidity", "Python", "FastAPI"], C["web3"]),
    ("sql-healthcheck", "SQL SERVER · DBA", "SQL Server Health Check",
     "Read-only T-SQL diagnostic covering configuration, backups, waits, indexes, statistics, blocking and security.",
     ["T-SQL", "Performance", "Security"], C["sqlserver"]),
]


def card(p):
    _, label, title, desc, tags, color, *rest = p
    private = bool(rest and rest[0])

    def build(th):
        W, H = 480, 196
        b = [f'<rect x="0.5" y="0.5" width="5" height="{H-1}" fill="{color}"/>',
             t(28, 38, label, 11, color, 700, spacing=1.5),
             t(28, 70, title, 21, th["title"], 700)]
        if private:
            b.append(f'<rect x="{W-104}" y="22" width="80" height="22" rx="11" fill="{th["chip"]}" stroke="{th["chip_border"]}"/>')
            b.append(t(W - 64, 37, "PRIVATE", 11, th["body"], 700, anchor="middle", spacing=1))
        else:
            b.append(t(W - 26, 40, "↗", 18, th["body"], 400, anchor="end"))
        for i, line in enumerate(wrap(desc, 14, W - 56)[:3]):
            b.append(t(28, 100 + i * 20, line, 14, th["body"]))
        x = 28
        for tag in tags:
            s, cw = chip(x, 154, tag, th, 12)
            b.append(s)
            x += cw + 8
        inner = "".join(b)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                f'<defs><clipPath id="c"><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12"/></clipPath></defs>'
                f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{th["bg"]}" stroke="{th["border"]}"/>'
                f'<g clip-path="url(#c)">{inner}</g></svg>\n')
    return build


# ---------------------------------------------------------------- stack
STACK = [
    ("Data platforms", [("Snowflake", C["snowflake"]), ("Databricks", C["databricks"]),
                        ("Microsoft Fabric", C["fabric"]), ("Delta Lake", "#00ADD4"),
                        ("Apache Spark", "#E25A1C"), ("Apache Iceberg", "#4E8EE9")]),
    ("Databases", [("SQL Server", C["sqlserver"]), ("PostgreSQL", "#4169E1"), ("MySQL", "#4479A1"),
                   ("MongoDB", "#47A248"), ("Oracle", C["oracle"])]),
    ("Engineering", [("Python", "#3776AB"), ("PySpark", "#E25A1C"), ("SQL / T-SQL", "#336791"),
                     ("dbt", C["dbt"]), ("Airflow", "#017CEE"), ("Airbyte", "#615EFF"),
                     ("Kafka", "#8B8B8B"), ("Streamlit", "#FF4B4B")]),
    ("Cloud & DevOps", [("Azure", C["microsoft"]), ("AWS", "#FF9900"), ("Azure DevOps", "#0078D7"),
                        ("GitHub Actions", "#2088FF"), ("Docker", "#2496ED"), ("Terraform", "#844FBA"),
                        ("Power BI", "#F2C811")]),
    ("Apps & Web3", [("C# / .NET", "#512BD4"), ("TypeScript", "#3178C6"), ("NestJS", "#E0234E"),
                     ("React", "#61DAFB"), ("Solidity", C["web3"]), ("Foundry", "#9C9C9C")]),
]


def stack(th):
    W, row_h, top = 1000, 50, 26
    H = top * 2 + row_h * len(STACK) - 14
    b = []
    for i, (label, items) in enumerate(STACK):
        y = top + i * row_h
        b.append(t(28, y + 21, label, 14, th["body"], 600))
        x = 190
        for name, color in items:
            s, cw = chip(x, y, name, th, 14, color)
            b.append(s)
            x += cw + 10
    return svg(W, H, "".join(b), th)


if __name__ == "__main__":
    save("banner", banner)
    save("certifications", certs)
    save("stack", stack)
    for p in PROJECTS:
        save(f"card-{p[0]}", card(p))
    print("written:", sorted(f.name for f in OUT.glob("*.svg")))
