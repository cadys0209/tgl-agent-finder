TGL Agent Finder 找代理 — how to use, share, and update
========================================================

WHAT IT IS
  index.html IS the tool. It is one self-contained file (agent data is baked
  inside), works offline, and needs no server. Source: the "Summary" sheet of
  "0 Agent list TGL VBA 06.17 0303.xlsm".

  Search a destination (country / city / keyword) and toggle service-capability
  chips (Warehouse, Trucking, Customs, DG, OOG, Project, White Gloves, E-com)
  to shortlist the right overseas agent for an inquiry — e.g. type "Los Angeles"
  then click the 倉庫 Warehouse chip to get "LA agents that have a warehouse".

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

KEEP IN SYNC
  "TGL Agent Finder.html" (one folder up) is a COPY of index.html for
  double-click use. build.py updates both. If you hand-edit one, copy it over
  the other before sharing.

FILES
  index.html        the live tool (upload this)
  build.py          regenerates index.html from the .xlsm
  _template.html    the layout/logic without data (edited by build.py)
  README.txt        this file
