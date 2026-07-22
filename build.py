# -*- coding: utf-8 -*-
"""
Rebuild TGL Agent Finder from the master agent-list workbook.
Reads the "Summary" sheet, groups by company-branch (company+country+city),
and bakes the data into index.html (and ../TGL Agent Finder.html).

Usage:  python build.py
If the .xlsm filename changes, update XLSM below (it auto-picks the newest
"*Agent list TGL VBA*.xlsm" in the parent folder if the default is missing).
"""
import openpyxl, json, re, os, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
XLSM = os.path.join(PARENT, "0 Agent list TGL VBA 06.17 0303.xlsm")
if not os.path.exists(XLSM):
    cands = [p for p in glob.glob(os.path.join(PARENT, "*Agent list TGL VBA*.xlsm"))
             if "~$" not in p and "backup" not in p.lower() and "BACKUP" not in p]
    if not cands:
        sys.exit("No agent-list .xlsm found in parent folder.")
    XLSM = max(cands, key=os.path.getmtime)
print("Reading:", os.path.basename(XLSM))

wb = openpyxl.load_workbook(XLSM, data_only=True, read_only=True)
ws = wb["Summary"]

NEG = {'', 'no', 'no.', 'n/a', 'na', 'x', 'none', '-', 'not specified', '/', '?'}
def clean(v):
    if v is None: return ''
    return str(v).replace('�', '').strip()
def has_cap(v):
    return clean(v).lower() not in NEG

# Column indexes (0-based) in the Summary data rows (header row 6, data from row 7)
# 0 Cat 1 Country 2 City 3 Code 4 Company 5 Network 6 Remark 7 Contact 8 Title
# 9 Email 10 TEL 11 Website 13 Address 14 Activities 15 Strength 16 Trucking
# 17 Warehouse 18 Customs 19 WhiteGloves 20 DG 21 OOG 22 Ecom 23 Project 24 Special 26 Note
CAPS = [("warehouse",17),("trucking",16),("customs",18),("whitegloves",19),
        ("dg",20),("oog",21),("ecom",22),("project",23)]
TEXTF = [("strength",15),("activities",14),("special",24),("note",26),("remark",6)]

groups, order = {}, []
for row in ws.iter_rows(min_row=7, max_col=27, values_only=True):
    if all(v is None for v in row): continue
    company, country = clean(row[4]), clean(row[1])
    if not company and not country: continue
    key = (company.lower(), country.lower(), clean(row[2]).lower())
    if key not in groups:
        groups[key] = {"cat":clean(row[0]),"country":country,"city":clean(row[2]),
            "code":clean(row[3]),"company":company,"networks":set(),"web":clean(row[11]),
            "addr":clean(row[13]),"contacts":[],"caps":{},"capraw":{},
            "strength":set(),"activities":set(),"special":set(),"note":set(),"remark":set()}
        order.append(key)
    g = groups[key]
    for nw in re.split(r'[\/,;]', clean(row[5])):
        if nw.strip(): g["networks"].add(nw.strip())
    if not g["web"] and clean(row[11]): g["web"] = clean(row[11])
    if not g["addr"] and clean(row[13]): g["addr"] = clean(row[13])
    name = clean(row[7])
    if name:
        c = {"name":name,"title":clean(row[8]),"email":clean(row[9]),"tel":clean(row[10])}
        if c not in g["contacts"]: g["contacts"].append(c)
    for label, idx in CAPS:
        raw = clean(row[idx])
        if has_cap(raw):
            g["caps"][label] = True
            if raw.lower() not in {'yes','v','y'}:
                g["capraw"].setdefault(label, set()).add(raw)
    for fld, idx in TEXTF:
        val = clean(row[idx])
        if val and val.lower() not in NEG: g[fld].add(val)

out = []
for key in order:
    g = groups[key]
    out.append({
        "cat":g["cat"],"country":g["country"],"city":g["city"],"code":g["code"],
        "company":g["company"],"networks":sorted(g["networks"]),"web":g["web"],"addr":g["addr"],
        "contacts":g["contacts"],"caps":{k:True for k in g["caps"]},
        "capraw":{k:" · ".join(sorted(v)) for k,v in g["capraw"].items()},
        "strength":" | ".join(sorted(g["strength"]))[:600],
        "activities":" | ".join(sorted(g["activities"]))[:400],
        "special":" | ".join(sorted(g["special"]))[:400],
        "note":" | ".join(sorted(g["note"]))[:400],
    })
print("Company-branches:", len(out))

data_json = json.dumps(out, ensure_ascii=False)
tpl = open(os.path.join(HERE, "_template.html"), encoding="utf-8").read()
if "/*__DATA__*/[]" not in tpl:
    sys.exit("Template placeholder /*__DATA__*/[] not found in _template.html")
html = tpl.replace("/*__DATA__*/[]", data_json)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
open(os.path.join(PARENT, "TGL Agent Finder.html"), "w", encoding="utf-8").write(html)
print("Wrote index.html (%d bytes) + ../TGL Agent Finder.html" % len(html.encode("utf-8")))
