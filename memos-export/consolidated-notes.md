# Memos Consolidated Notes

> Exported 2026-05-09 · 126 memos spanning Apr 2023 – Aug 2025

---

## EPICS & Control Systems

### Core EPICS & PV
- Learn SQL for EPICS integration — SQLite with EPICS
- IOC development for COSY simulation
- AsynPortDriver for data aggregation IOC
- Dynamically serving process variables: establish PVs via pcaspy, run as async tasks, manage pcaspy processes asynchronously
- Dynamic PV grouping at runtime (PVA)
- EPICS request through links (e.g. `asub`) vs SNL via subscription
- Idea: convert EPICS db to SQL db for visualization
- Add support of strftime to timestamp soft record

### EPICS GUI & Displays
- Connect Phoebus displays via Xpra, NX web client, and Guacamole
  - p4p gateway: https://mdavidsaver.github.io/p4p/gw.html
  - Nameserver env blocking Ctrl+C
- OPI time machine; opi-generator — XML introspection, analyzing element relationships
- Draw graphics in Inkscape and export as OPI?
- EPICS GUI concept: build UI blocks per record type; drag-and-drop designer for process workflow; run graph to fulfill functions. UI techniques: Qt Graphics View, WASM
- Build a new display manager with ImGui?
- Build a node-based app with ImGui for EPICS database relation visualization and development?
- Parse an OPI file, show stats data
- Idea: create interface to visualize EPICS data in a homepage info widget; make EPICS data as a new metric for Glances
- Control display manager: Python, Qt, Asynchronous

### Go-EPICS (go-epics)
- Develop libraries for building a portable PVXS server
- EPICS-TCA Node.js library
- Develop a control app with Golang for Archiver Appliance data retrieval
- Research MQTT: use Golang for server/client, CS-Studio integration, ImGui

### Cybersecurity for EPICS
- Introducing web development practice in terms of cyber security — gateway breach risk
- MITM attack awareness: https://www.keyfactor.com/blog/what-is-a-man-in-the-middle-attack/
- Git signed commit as PUT guard

---

## Golang

### Learning & References
- Go tutorial: https://go.nsddd.top/
- Effective Go: https://go.dev/doc/effective_go
- Code review comments: https://github.com/golang/go/wiki/CodeReviewComments
- Go proverbs: https://go-proverbs.github.io/
- Common Go mistakes: https://100go.co/
- Workaround for `http.DetectContentType` not returning `image/svg+xml`: https://github.com/golang/go/issues/15888#issuecomment-222457018

### Web Development
- Golang web app stack: HTMX + templates + gRPC
- WebSocket: https://github.com/nhooyr/websocket
- WebSocket in WASM: https://stackoverflow.com/a/55792270
- Object-oriented HTML: https://github.com/webqit/oohtml

### Configuration & Services
- Config: https://github.com/spf13/viper
- Run Go as a service: https://github.com/kardianos/service
- Signals/event system: https://www.reddit.com/r/golang/comments/19dje4s/
- Manylinux container for building Go programs for Linux distros

### Concurrency
- `conc` — better-structured concurrency: https://github.com/sourcegraph/conc
- `runtime.LockOSThread()`

### GUI / UI
- **ImGui for Go:**
  - cimgui-go (active): https://github.com/AllenDang/cimgui-go
  - imgui-go (archived): https://github.com/inkyblackness/imgui-go; fork: https://github.com/AllenDang/imgui-go
  - giu: https://github.com/AllenDang/giu
  - Power-saving mode: UI pauses refresh after 15 idle frames; force via `giu.Update()` (high overhead for real-time apps)
- **Nuklear** (ImGui in C, Go binding): https://github.com/golang-ui/nuklear (nk-example doesn't work on Linux Mint 21.3 + Go 1.21.3)
- **tview** (terminal UI): https://github.com/rivo/tview
- **egi** (Rust): https://docs.rs/egui/latest/egui/ — eframe_template is a good start; iced for more native feel with WASM

### cgo
- https://zhuanlan.zhihu.com/p/349197066
- Calling Go from C: https://medium.com/using-go-in-mobile-apps/using-go-in-mobile-apps-part-1-calling-go-functions-from-c-be1ecf7dfbc6
- CGO Go data types: https://gist.github.com/zchee/b9c99695463d8902cd33
- CCgo — translates C to Go: https://gitlab.com/cznic/ccgo

### Project Organization
- Reference: https://github.com/google/go-github
- gRPC UI: https://github.com/fullstorydev/grpcui
- Secure network / zero-trust: https://blog.openziti.io/go-is-amazing-for-zero-trust
- ServiceWeaver — modular binary → microservices: https://serviceweaver.dev/
- Write a BitTorrent client with Go: https://github.com/veggiedefender/torrent-client
- Project ideas: https://systems.codeyourfuture.io/projects/

### Other Go Topics
- SSH connections/tunnels management app
- Wazero — zero-dependency WASM runtime: https://wazero.io/, https://github.com/tetratelabs/wazero

---

## Python

### WebAssembly
- Pyodide: https://pyodide.org/en/stable/usage/quickstart.html
- Python + WASM for web apps: https://thenewstack.io/python-and-webassembly-elevating-performance-for-web-apps/

### Async & Concurrency
- BBC CloudFit (asyncio patterns): https://bbc.github.io/cloudfit-public-docs/
- Python asyncio article: https://mp.weixin.qq.com/s/9Z3xyyOC1Ls62KuVwJoArA
- Compose complex task execution workflow: https://www.biaodianfu.com/python-schedule.html

### Data & EDA
- 10 Python auto-exploratory data analysis libraries: https://mp.weixin.qq.com/s/_mdHyy9MXF2rzttTtJ55Rw
- Pandas operations: https://mp.weixin.qq.com/s?__biz=MzA4MjEyNTA5Mw==&mid=2652600011 (WeChat)
- pygwalk: `pip install pygwalk`
- Navicat Premium Lite: https://navicat.com/en/products/navicat-premium-lite

### Performance
- Cython exploration
- High-performance Python built with LLVM: https://lpython.org/
- Mojo: https://www.modular.com/mojo
- Develop Python modules with Rust

### GUI
- Control display manager: Python, Qt, Asynchronous
- Custom Qt widgets: https://www.pythonguis.com/tutorials/creating-your-own-custom-widgets/
- Read: "Application Development with Qt Creator — Third Edition"
- Qt threading: https://www.xingyulei.com/post/qt-threading/
- Qt builds for different platforms: https://build-qt.fsu0413.me/index.html
- Skia for Python?
- NiceGUI: https://nicegui.io/
- Watchdog file monitoring: https://mp.weixin.qq.com/s/ckBfaBPfA6M3bCeJsVDmIg

---

## Rust

- Learning Rust: https://github.com/kyclark/command-line-rust
- egi / eframe_template: https://docs.rs/egui/latest/egui/
- iced — more native feel for WASM targets

---

## Web Development

### Frameworks
- React + TypeScript: https://handsonreact.com/docs/labs/react-tutorial-typescript
- Next.js + FastAPI: https://github.com/digitros/nextjs-fastapi
- Vue, Svelte, HTMX gaining popularity
- Fresh (frontend) + Deno (JS backend)
- React/Vue (Quasar) for work apps

### UI Libraries
- Semantic UI: https://semantic-ui.com/
- Materialize CSS: https://materializecss.com/getting-started.html
- WebSocket article: https://mp.weixin.qq.com/s/-dLKpim5q0NL1gkix8W5zQ

### Infrastructure
- Redis as data broker
- Web app for settings manager and other datasets
- Learn webpack

---

## Databases

- SQL: CS50 SQL course — https://cs50.harvard.edu/sql/2023/psets/0/
- Materialized views, views, indexes
- Database migrations: https://vadimkravcenko.com/shorts/database-migrations/
- Database with EPICS — SQLite integration

---

## LLM & AI

- txyz.ai — AI paper search: https://txyz.ai/
- Run Llama 2 uncensored locally: https://ollama.com/blog/run-llama2-uncensored-locally
- MinerU — PDF to Markdown: https://github.com/opendatalab/MinerU

---

## DevOps & Infrastructure

### Virtualization & Servers
- XCP-ng vs Proxmox home lab: https://www.virtualizationhowto.com/2023/04/xcp-ng-vs-proxmox-home-lab-comparison/
- Ansible AWX
- Synology IPFS with Portainer: https://mariushosting.com/synology-install-ipfs-with-portainer/

### Build Tools
- GNU Make tutorial: https://www.linode.com/docs/guides/gnu-make-tutorial-automate-tasks/
- Coroutines in C: https://www.chiark.greenend.org.uk/~sgtatham/coroutines.html

### Troubleshooting
- Citrix Workspace Linux SSL issue: https://askubuntu.com/a/1461132
- RAID to AHCI driver issue: https://superuser.com/a/1623018

### Tools
- Zealdocs — offline development docs: https://zealdocs.org/
- nexttrace: https://github.com/sjlleo/nexttrace
- OpenBB Terminal: https://github.com/OpenBB-finance/OpenBBTerminal

---

## Digital Twin & 3D

- three.js + Unity + Blender, 3D-Max
- GLB model format

---

## Photography

- https://www.zhihu.com/answer/3061346605

---

## Bookmarks & Resources

### Bookmarks & Reading
- Library Genesis: https://librarygenesis.net/, http://libgen.st/, http://libgen.is, http/libgen.rs
- Pinetree — bookmark organizer: https://github.com/Pintree-io/pintree
- Million lines of code visualization: https://www.informationisbeautiful.net/visualizations/million-lines-of-code/
- C++ cheat sheets: https://hackingcpp.com/cpp/cheat_sheets.html
- `volatile` for multithreaded C++: https://drdobbs.com/cpp/volatile-the-multithreaded-programmers-b/184403766
- Project-based learning: https://github.com/practical-tutorials/project-based-learning
- Awesome macOS: https://wangchujiang.com/awesome-mac/
- Excel tips: https://www.zhihu.com/answer/671701602
- Build OSRM server: https://rcarto.github.io/posts/build_osrm_server/

### Compression
- Brotli — lossless compression: https://github.com/google/brotli

---

## Ideas & To-Do

### Side Projects
- Home EPICS project: Dropbox notifier
- iOS for COSY simulation
- Go SSH tunnel/connection manager
- Android app: enable/disable screen tap, system control shortcuts integration
- Study Memos project itself (Golang + TypeScript): https://github.com/usememos/memos
- Try aardio on Windows

### Home Lab
- Homepage dashboard for all apps: https://github.com/gethomepage/homepage
- Glances monitoring: https://github.com/nicolargo/glances

---

## Personal

- 孩子不听劝，仍旧不停朝我射水，再三警告无效后，我把他的水枪砸坏了。(2023-04-22)
- BSAS, SLAC (2023-04-26)
- Configuration for take snapshot action (2023-04-26)
- Snapshot from retrieved data (2023-04-27)
- Human factors (2023-04-25)
- qsrv (2023-04-25)
