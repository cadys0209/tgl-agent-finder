TGL Agent Finder 找代理 — how to use, share, and update
========================================================

WHAT IT IS
  index.html IS the tool. It is one self-contained file (agent data is baked
  inside), works offline, and needs no server. Source: the "Summary" sheet of
  "0 Agent list TGL VBA 06.17 0303.xlsm".

  Search a destination (country / city / keyword) and toggle service-capability
  chips (Warehouse, Trucking, Customs, DG, OOG, Project, White Gloves, E-com)
  to shortlist the right overseas agent for an inquiry — e.g. type "Los Angeles"
  then click the Warehouse chip to get "LA agents that have a warehouse".
  The interface is English and opens behind a shared passcode (see below).
  Region / Country / City / IATA Code / Network are cascading dropdowns
  (each narrows to only the values still available under the others).

USE IT LOCALLY (no hosting)
  Double-click "TGL Agent Finder.html" (one folder up) — opens in any browser,
  fully offline. To share without hosting, email that single file; the
  colleague double-clicks it. Done.

SHARE A LINK (same as the Station Routing tool)
  OPTION A — GitHub Pages (permanent, free, what tgl-station-routing uses)
    1. Create a new public repo, e.g. "tgl-agent-finder".
    2. Upload index.html to the repo root.
    3. Settings > Pages > Source: Deploy from branch = main / root. Save.
    4. Link becomes  https://<your-github-user>.github.io/tgl-agent-finder/
  OPTION B — Netlify drop (fastest, ~30s)
    1. Open  https://app.netlify.com/drop
    2. Drag THIS WHOLE FOLDER (agent-finder-site) onto the page.
    3. Share the link it gives you.

WHEN THE AGENT LIST CHANGES (rebuild the data)
  The tool is a snapshot. After you update the Excel, regenerate index.html:
    1. Open a terminal in this folder.
    2. Run:  python build.py
       (it re-reads the .xlsm Summary sheet and rewrites index.html +
        "TGL Agent Finder.html").
    3. Re-upload index.html to GitHub / re-drag the folder to Netlify.

  DO THE CLEANUP RULES SURVIVE AN UPDATE?  Yes.
    All the tidy-up rules live in _template.html, NOT in the data, so build.py
    re-applies them to the fresh Excel every time. These work AUTOMATICALLY on
    new data, no matter what changes:
      - case merging (BLOC/Bloc, SEAJET/Seajet, JCtrans/Jctrans ...)
      - City cleanup: drop ", CA" / trailing US state, fix ALL-CAPS
      - Country ALL-CAPS -> Title Case
      - passcode, English UI, the 5 cascading dropdowns
    Nothing to do — just run build.py.

  ONE EXCEPTION — brand-new spelling variants of a Network.
    A few Network merges use a fixed list of the exact spellings seen today
    (e.g. COOP -> The Coop, Fryet -> Freyt World, OLO Family -> OLO). If a
    future update introduces a NEW spelling/typo not on that list, it will show
    up as its own separate item until the list is extended. (All the spellings
    already known will keep merging.)
    To add a new one yourself, open _template.html and edit these two lists:
      - NET_CANON  (~line 195): map an UPPERCASE variant to the name to show,
                    e.g.   'CO-OP':'The Coop',
      - NET_DROP   (~line 210): UPPERCASE junk values to hide from the filter,
                    e.g. add   'SOME-CERT',
    Then run  python build.py  and re-upload index.html.
    Easiest option: just send Fable the updated .xlsm and it will rebuild and
    top up these lists for you.

KEEP IN SYNC
  "TGL Agent Finder.html" (one folder up) is a COPY of index.html for
  double-click use. build.py updates both. If you hand-edit one, copy it over
  the other before sharing.

FILES
  index.html        the live tool (upload this)
  build.py          regenerates index.html from the .xlsm
  _template.html    the layout/logic without data (edited by build.py)
  README.txt        this file
