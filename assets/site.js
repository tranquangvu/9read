/* AIFDE Mastery — shared runtime: module registry, sidebar, theme, mermaid, checklists, i18n */

const GROUPS = [
  { key: "FN", name: "AI & Data Foundations", nameVi: "Nền tảng AI & Dữ liệu", color: "#2563EB" },
  { key: "AI", name: "AI Application Engineering", nameVi: "Kỹ thuật Ứng dụng AI", color: "#7C3AED" },
  { key: "PR", name: "Production & Integration", nameVi: "Triển khai & Tích hợp", color: "#0D9488" },
  { key: "FD", name: "FDE Consulting & Delivery", nameVi: "Tư vấn & Triển khai FDE", color: "#DB2777" },
];

/* Order = recommended learning order (matrix column order). */
const MODULES = [
  { code: "FN1",  name: "Python for AI",                              nameVi: "Python cho AI",                                      critical: true  },
  { code: "FN2",  name: "LLM Fundamentals",                           nameVi: "Nền tảng LLM",                                      critical: true  },
  { code: "FN3",  name: "Embeddings & Vector Search",                 nameVi: "Embeddings & Tìm kiếm Vector",                      critical: true  },
  { code: "FN4",  name: "Classic ML Literacy",                        nameVi: "Kiến thức ML Cổ điển",                              critical: false },
  { code: "FN5",  name: "Data Engineering Basics",                    nameVi: "Cơ bản Kỹ thuật Dữ liệu",                           critical: false },
  { code: "FN6",  name: "SQL & Analytical Thinking",                  nameVi: "SQL & Tư duy Phân tích",                            critical: false },
  { code: "FN7",  name: "AI-assisted Development",                    nameVi: "Phát triển với AI Trợ lý",                          critical: true  },
  { code: "AI1",  name: "Prompt Engineering",                         nameVi: "Kỹ thuật Prompt",                                   critical: true  },
  { code: "AI2",  name: "LLM API Engineering",                        nameVi: "Kỹ thuật API LLM",                                  critical: true  },
  { code: "AI3",  name: "Context Engineering",                        nameVi: "Kỹ thuật Ngữ cảnh",                                 critical: true  },
  { code: "AI4",  name: "RAG & Enterprise Search",                    nameVi: "RAG & Tìm kiếm Doanh nghiệp",                       critical: true  },
  { code: "AI5",  name: "Vector Databases",                           nameVi: "Cơ sở dữ liệu Vector",                              critical: true  },
  { code: "AI6",  name: "Agentic Workflow Design",                    nameVi: "Thiết kế Luồng Tác tử",                             critical: true  },
  { code: "AI7",  name: "Agent Frameworks & SDKs",                    nameVi: "Framework & SDK Tác tử",                            critical: true  },
  { code: "AI8",  name: "Tool Calling & MCP",                         nameVi: "Gọi Công cụ & MCP",                                 critical: true  },
  { code: "AI9",  name: "AI Evaluation & Regression",                 nameVi: "Đánh giá & Hồi quy AI",                             critical: true  },
  { code: "AI10", name: "Fine-tuning & Model Adaptation",             nameVi: "Fine-tuning & Thích ứng Mô hình",                   critical: false },
  { code: "AI11", name: "Multimodal AI",                              nameVi: "AI Đa phương thức",                                 critical: false },
  { code: "AI12", name: "Open-source & Local Models",                 nameVi: "Mô hình Mã nguồn mở & Cục bộ",                     critical: false },
  { code: "AI13", name: "Reasoning Models & Extended Thinking",       nameVi: "Mô hình Lập luận & Suy nghĩ Mở rộng",              critical: true  },
  { code: "AI14", name: "Text-to-SQL & Structured Data",              nameVi: "Text-to-SQL & Dữ liệu Có cấu trúc",                critical: true  },
  { code: "AI15", name: "Multi-agent Systems",                        nameVi: "Hệ thống Đa tác tử",                                critical: false },
  { code: "AI16", name: "Red-teaming & Adversarial Evaluation",       nameVi: "Red-teaming & Đánh giá Đối kháng",                  critical: true  },
  { code: "PR1",  name: "AI Observability & Tracing",                 nameVi: "Giám sát & Truy vết AI",                            critical: true  },
  { code: "PR2",  name: "Model Routing, Latency & Cost",              nameVi: "Định tuyến Mô hình, Độ trễ & Chi phí",             critical: true  },
  { code: "PR3",  name: "Reliability & Background Processing",        nameVi: "Độ tin cậy & Xử lý Nền",                            critical: true  },
  { code: "PR4",  name: "AI Guardrails & Security",                   nameVi: "Hàng rào Bảo vệ & Bảo mật AI",                     critical: true  },
  { code: "PR5",  name: "Data Privacy & Compliance",                  nameVi: "Quyền riêng tư Dữ liệu & Tuân thủ",                critical: false },
  { code: "PR6",  name: "Cloud AI Platforms",                         nameVi: "Nền tảng AI Đám mây",                               critical: true  },
  { code: "PR7",  name: "Docker & CI/CD for AI Workloads",            nameVi: "Docker & CI/CD cho AI",                             critical: false },
  { code: "PR8",  name: "Enterprise Systems Integration",             nameVi: "Tích hợp Hệ thống Doanh nghiệp",                   critical: true  },
  { code: "PR9",  name: "Document Processing Pipelines",              nameVi: "Pipeline Xử lý Tài liệu",                           critical: false },
  { code: "PR10", name: "Testing AI Systems",                         nameVi: "Kiểm thử Hệ thống AI",                              critical: false },
  { code: "PR11", name: "Production Debugging & Incident Response",   nameVi: "Gỡ lỗi Production & Ứng phó Sự cố",               critical: true  },
  { code: "PR12", name: "Scalability & Multi-tenancy",                nameVi: "Khả năng Mở rộng & Đa khách thuê",                 critical: false },
  { code: "PR13", name: "Authentication, RBAC & Tenant Isolation",    nameVi: "Xác thực, RBAC & Cô lập Khách thuê",               critical: true  },
  { code: "FD1",  name: "Customer Discovery",                         nameVi: "Khám phá Khách hàng",                               critical: true  },
  { code: "FD2",  name: "Rapid Prototyping",                          nameVi: "Tạo mẫu Nhanh",                                     critical: true  },
  { code: "FD3",  name: "AI Solution Architecture",                   nameVi: "Kiến trúc Giải pháp AI",                            critical: true  },
  { code: "FD4",  name: "KPI, ROI & Value Measurement",               nameVi: "KPI, ROI & Đo lường Giá trị",                       critical: true  },
  { code: "FD5",  name: "Stakeholder Communication",                  nameVi: "Giao tiếp Bên liên quan",                           critical: true  },
  { code: "FD6",  name: "Expectation Management",                     nameVi: "Quản lý Kỳ vọng",                                   critical: true  },
  { code: "FD7",  name: "Embedded Working & Client Trust",            nameVi: "Làm việc Nhúng & Niềm tin Khách hàng",             critical: true  },
  { code: "FD8",  name: "Delivery Ownership",                         nameVi: "Làm chủ Bàn giao",                                  critical: false },
  { code: "FD9",  name: "Domain Ramp-up",                             nameVi: "Làm quen Lĩnh vực",                                 critical: true  },
  { code: "FD10", name: "Documentation, Handover & Adoption",         nameVi: "Tài liệu, Bàn giao & Áp dụng",                     critical: false },
  { code: "FD11", name: "Pre-sales Support",                          nameVi: "Hỗ trợ Tiền bán hàng",                              critical: false },
  { code: "FD12", name: "Business English & Cross-cultural Communication", nameVi: "Tiếng Anh Thương mại & Giao tiếp Đa văn hóa", critical: true  },
];

/* ---------- i18n ---------- */
const PATH = location.pathname.replace(/\\/g, "/");
const PATH_SEGMENTS = PATH.split("/").filter(Boolean);
const LANG = PATH_SEGMENTS.includes("vn") ? "vn" : "en";

const VI = {
  "All topics": "Tất cả chủ đề",
  "Overview & Curriculum": "Tổng quan & Chương trình",
  "Critical": "Trọng yếu",
  "Supporting": "Bổ trợ",
  "← Previous": "← Trước",
  "Next →": "Tiếp →",
  "Target 3 — independent production": "Mục tiêu 3 — làm việc độc lập",
  "Target 2 — works with support": "Mục tiêu 2 — làm việc với hỗ trợ",
  "modules": "mô-đun",
  "available": "có sẵn",
  "Coming soon": "Sắp ra mắt",
  "Critical skill": "Kỹ năng trọng yếu",
  "Supporting skill": "Kỹ năng bổ trợ",
  "Target score: 3 / 4": "Mục tiêu: 3 / 4",
  "Target score: 2 / 4": "Mục tiêu: 2 / 4",
};

function t(key, fallback) {
  if (LANG !== "vn") return fallback || key;
  return VI[key] || fallback || key;
}

function modName(m) { return LANG === "vn" ? m.nameVi : m.name; }
function grpName(g) { return LANG === "vn" ? g.nameVi : g.name; }

/* ---------- topics (root hub) ---------- */
const TOPICS = [
  {
    slug: "aifde",
    name: "AIFDE Mastery",
    tagline: LANG === "vn" ? "Kỹ sư Triển khai AI" : "AI Forward Deployed Engineer",
    blurb: LANG === "vn"
      ? "Chương trình 48 mô-đun đưa kỹ sư từ nền tảng Python và LLM đến việc triển khai, " +
        "vận hành và bán các hệ thống AI trong môi trường của khách hàng — mỗi mô-đun đều có " +
        "bài tập thực hành và sản phẩm bằng chứng."
      : "A 48-module curriculum taking an engineer from Python and LLM fundamentals to shipping, " +
        "operating and selling AI systems inside a customer's stack — each module with hands-on labs " +
        "and an evidence artifact.",
    meta: LANG === "vn" ? `${MODULES.length} mô-đun` : `${MODULES.length} modules`,
    tags: GROUPS.map((g) => grpName(g)),
    accent: "#D97757",
    status: "live",
  },
];

const IN_MODULES_DIR = PATH.includes("/modules/");
/* Section root = the topic folder (aifde/); site root = the hub above it. */
const ROOT = IN_MODULES_DIR ? "../" : "./";
const IN_TOPIC = TOPICS.some((t) => PATH.includes(`/${t.slug}/`));
const SITE_ROOT = IN_MODULES_DIR ? "../../" : IN_TOPIC ? "../" : "./";
const CURRENT = (location.pathname.split("/").pop() || "index.html").replace(".html", "").toUpperCase();

function moduleHref(code) {
  return `${ROOT}modules/${code.toLowerCase()}.html`;
}

function langSwapHref() {
  /* Return the equivalent page in the other language.
     Works with any hosting setup: local file://, localhost, subdirectory, GitHub Pages. */
  const segs = location.pathname.replace(/\\/g, "/").split("/").filter(Boolean);
  if (LANG === "vn") {
    // Remove the 'vn' segment wherever it appears
    const idx = segs.indexOf("vn");
    if (idx >= 0) segs.splice(idx, 1);
  } else {
    // Insert 'vn' as the first path segment
    segs.unshift("vn");
  }
  return "/" + segs.join("/");
}

function groupOf(code) {
  return GROUPS.find((g) => code.startsWith(g.key));
}

/* ---------- theme ---------- */
const ICON_SUN = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>`;
const ICON_MOON = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>`;

function isDark() {
  return document.documentElement.classList.contains("dark");
}
function setThemeIcons() {
  const dark = isDark();
  document.querySelectorAll("[data-theme-icon]").forEach((el) => {
    el.innerHTML = dark ? ICON_SUN : ICON_MOON;
  });
}
function applyTheme(dark) {
  document.documentElement.classList.toggle("dark", dark);
  localStorage.setItem("fde-theme", dark ? "dark" : "light");
  setThemeIcons();
  renderMermaid();
}

/* ---------- sidebar ---------- */
function buildSidebar() {
  const nav = document.getElementById("module-nav");
  if (!nav) return;
  let html = `
    <a href="${SITE_ROOT}index.html" class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs text-mute dark:text-mutedark hover:bg-sand dark:hover:bg-sanddark">
      <span>←</span> ${t("All topics", "All topics")}
    </a>
    <a href="${ROOT}index.html" class="mt-1 flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold hover:bg-sand dark:hover:bg-sanddark ${CURRENT === "INDEX" ? "current side-link" : ""}">
      <span class="text-coral">◆</span> ${t("Overview & Curriculum", "Overview & Curriculum")}
    </a>`;
  for (const g of GROUPS) {
    const mods = MODULES.filter((m) => groupOf(m.code) === g);
    html += `
      <div class="mt-5 mb-1 px-3 flex items-center gap-2">
        <span class="w-2 h-2 rounded-full gbg-${g.key}"></span>
        <span class="text-[11px] font-semibold uppercase tracking-wider text-mute dark:text-mutedark">${grpName(g)}</span>
      </div>`;
    for (const m of mods) {
      const cur = CURRENT === m.code ? "current" : "";
      html += `
        <a href="${moduleHref(m.code)}" class="side-link ${cur} flex items-baseline gap-2 px-3 py-1.5 rounded-lg text-[13px] hover:bg-sand dark:hover:bg-sanddark">
          <span class="font-mono text-[11px] w-9 shrink-0 gtx-${g.key}">${m.code}</span>
          <span class="leading-snug">${modName(m)}</span>
        </a>`;
    }
  }
  nav.innerHTML = html;
}

/* ---------- prev / next ---------- */
function buildPageNav() {
  const el = document.getElementById("page-nav");
  if (!el) return;
  const i = MODULES.findIndex((m) => m.code === CURRENT);
  if (i === -1) return;
  const prev = MODULES[i - 1];
  const next = MODULES[i + 1];
  const card = (m, label, align) =>
    m
      ? `<a href="${moduleHref(m.code)}" class="flex-1 rounded-xl border border-line dark:border-linedark bg-card dark:bg-carddark px-5 py-4 hover:border-coral transition-colors ${align}">
          <div class="text-[11px] uppercase tracking-wider text-mute dark:text-mutedark">${label}</div>
          <div class="mt-1 font-semibold text-sm"><span class="font-mono text-coral">${m.code}</span> ${modName(m)}</div>
        </a>`
      : `<div class="flex-1"></div>`;
  el.innerHTML = `${card(prev, t("← Previous", "← Previous"), "")}${card(next, t("Next →", "Next →"), "text-right")}`;
}

/* ---------- module hero meta (auto-fill from registry) ---------- */
function decorateHero() {
  const g = groupOf(CURRENT);
  if (!g) return;
  document.querySelectorAll("[data-group-chip]").forEach((el) => {
    el.classList.add(`gchip-${g.key}`);
    el.textContent = grpName(g);
  });
}

/* ---------- mermaid ---------- */
function renderMermaid() {
  if (!window.mermaid) return;
  const dark = isDark();
  const nodes = document.querySelectorAll(".mermaid");
  if (!nodes.length) return;
  nodes.forEach((el) => {
    if (!el.dataset.src) el.dataset.src = el.innerHTML;
    el.removeAttribute("data-processed");
    el.innerHTML = el.dataset.src;
  });
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif",
    theme: "base",
    flowchart: { htmlLabels: true, useMaxWidth: true },
    sequence: { useMaxWidth: true },
    themeVariables: dark
      ? {
          background: "#0A0A0A", primaryColor: "#222225", primaryTextColor: "#F0EEE9",
          primaryBorderColor: "#D97757", lineColor: "#A8A49B", secondaryColor: "#4A352C",
          tertiaryColor: "#161618", fontSize: "14px", clusterBkg: "#161618", clusterBorder: "#2A2A2E",
          edgeLabelBackground: "#161618", actorBkg: "#222225", actorTextColor: "#F0EEE9",
          actorBorder: "#D97757", signalColor: "#A8A49B", signalTextColor: "#F0EEE9",
          noteBkgColor: "#4A352C", noteTextColor: "#F0EEE9", noteBorderColor: "#D97757",
        }
      : {
          background: "#FAF9F5", primaryColor: "#F0EEE6", primaryTextColor: "#141413",
          primaryBorderColor: "#D97757", lineColor: "#6E6B64", secondaryColor: "#F7E9E2",
          tertiaryColor: "#FFFFFF", fontSize: "14px", clusterBkg: "#FFFFFF", clusterBorder: "#E6E3DA",
          edgeLabelBackground: "#FAF9F5", actorBkg: "#F0EEE6", actorTextColor: "#141413",
          actorBorder: "#D97757", signalColor: "#6E6B64", signalTextColor: "#141413",
          noteBkgColor: "#F7E9E2", noteTextColor: "#141413", noteBorderColor: "#D97757",
        },
  });
  mermaid.run({ querySelector: ".mermaid" });
}

/* ---------- evidence checklists (persisted) ---------- */
function bindChecklists() {
  const page = (location.pathname.split("/").pop() || "index").replace(".html", "");
  document.querySelectorAll("input.evidence-box").forEach((cb, i) => {
    const key = `fde-check-${page}-${cb.dataset.key || i}`;
    cb.checked = localStorage.getItem(key) === "1";
    cb.addEventListener("change", () => localStorage.setItem(key, cb.checked ? "1" : "0"));
  });
}

/* ---------- index dashboard cards ---------- */
function buildIndexCards() {
  for (const g of GROUPS) {
    const wrap = document.getElementById(`group-${g.key}`);
    if (!wrap) continue;
    const mods = MODULES.filter((m) => groupOf(m.code) === g);
    wrap.innerHTML = mods
      .map(
        (m) => `
      <a href="${moduleHref(m.code)}" class="group rounded-xl border border-line dark:border-linedark bg-card dark:bg-carddark p-4 hover:border-coral hover:shadow-sm transition-all">
        <div class="flex items-center justify-between">
          <span class="font-mono text-xs font-bold px-2 py-0.5 rounded-md text-white gbg-${g.key}">${m.code}</span>
          ${m.critical ? `<span class="text-[10px] font-semibold uppercase tracking-wide text-coral">${t("Critical", "Critical")}</span>` : `<span class="text-[10px] uppercase tracking-wide text-mute dark:text-mutedark">${t("Supporting", "Supporting")}</span>`}
        </div>
        <div class="mt-2.5 font-semibold text-[15px] leading-snug group-hover:text-coral transition-colors">${modName(m)}</div>
        <div class="mt-1.5 text-xs text-mute dark:text-mutedark">${m.critical ? t("Target 3 — independent production", "Target 3 — independent production") : t("Target 2 — works with support", "Target 2 — works with support")}</div>
      </a>`
      )
      .join("");
  }
}

/* ---------- root hub: topic rows ---------- */
const ICON_ARROW = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>`;

function buildTopicCards() {
  const wrap = document.getElementById("topic-list");
  if (!wrap) return;
  const count = document.getElementById("topic-count");
  if (count) count.textContent = `${TOPICS.length} ${t("available", "available")}`;
  wrap.innerHTML = TOPICS.map((t, i) => {
    const soon = t.status === "soon";
    const tags = (t.tags || [])
      .map((x) => `<span class="topic-tag">${x}</span>`)
      .join("");
    const inner = `
      <span class="topic-index" aria-hidden="true">${String(i + 1).padStart(2, "0")}</span>
      <div class="min-w-0">
        <div class="flex flex-wrap items-baseline gap-x-3 gap-y-1">
          <h3 class="font-display text-xl md:text-2xl font-bold tracking-[-0.015em]">${t.name}</h3>
          <span class="topic-tagline">${t.tagline}</span>
          ${soon ? `<span class="topic-tag topic-tag-soon">${t("Coming soon", "Coming soon")}</span>` : ""}
        </div>
        <p class="mt-3 text-sm md:text-[15px] text-mute dark:text-mutedark leading-relaxed max-w-[46rem]">${t.blurb}</p>
        <div class="mt-4 flex flex-wrap items-center gap-1.5">
          <span class="topic-tag topic-tag-meta">${t.meta}</span>${tags}
        </div>
      </div>
      <span class="topic-arrow">${soon ? "" : ICON_ARROW}</span>`;
    const cls = `topic-row${soon ? " is-soon" : ""}`;
    return soon
      ? `<div class="${cls}" style="--topic-color:${t.accent}">${inner}</div>`
      : `<a href="${SITE_ROOT}${t.slug}/index.html" class="${cls}" style="--topic-color:${t.accent}">${inner}</a>`;
  }).join("");
}

/* ---------- language switcher ---------- */
function buildLangSwitcher() {
  // Insert language toggle buttons next to theme toggles
  document.querySelectorAll("[data-theme-toggle]").forEach((themeBtn) => {
    // Avoid inserting twice
    if (themeBtn.parentNode.querySelector("[data-lang-switch]")) return;
    const btn = document.createElement("button");
    btn.setAttribute("data-lang-switch", "");
    btn.className = "w-9 h-9 rounded-full border border-line dark:border-linedark bg-card/60 dark:bg-carddark/50 backdrop-blur flex items-center justify-center text-sm hover:border-coral hover:text-coral transition-colors ml-2";
    btn.title = LANG === "vn" ? "Switch to English" : "Chuyển sang tiếng Việt";
    btn.setAttribute("aria-label", LANG === "vn" ? "Switch to English" : "Chuyển sang tiếng Việt");
    btn.textContent = LANG === "vn" ? "🇬🇧" : "🇻🇳";
    btn.addEventListener("click", () => {
      const target = langSwapHref();
      localStorage.setItem("fde-lang", LANG === "vn" ? "en" : "vn");
      location.href = target;
    });
    themeBtn.parentNode.insertBefore(btn, themeBtn.nextSibling);
  });

  // Also add to root hub header (no theme toggle in the fixed-top button row there)
  const hubHeader = document.querySelector("body > div.relative > header");
  if (hubHeader && !hubHeader.querySelector("[data-lang-switch]")) {
    const btn = document.createElement("button");
    btn.setAttribute("data-lang-switch", "");
    btn.className = "w-9 h-9 rounded-full border border-line dark:border-linedark bg-card/60 dark:bg-carddark/50 backdrop-blur flex items-center justify-center text-sm hover:border-coral hover:text-coral transition-colors ml-2";
    btn.title = LANG === "vn" ? "Switch to English" : "Chuyển sang tiếng Việt";
    btn.setAttribute("aria-label", LANG === "vn" ? "Switch to English" : "Chuyển sang tiếng Việt");
    btn.textContent = LANG === "vn" ? "🇬🇧" : "🇻🇳";
    btn.addEventListener("click", () => {
      const target = langSwapHref();
      localStorage.setItem("fde-lang", LANG === "vn" ? "en" : "vn");
      location.href = target;
    });
    hubHeader.appendChild(btn);
  }
}

/* ---------- sidebar toggle ---------- */
function bindMobileMenu() {
  const btn = document.getElementById("menu-btn");
  const aside = document.getElementById("sidebar");
  const overlay = document.getElementById("overlay");
  if (!btn || !aside) return;
  const isDesktop = () => matchMedia("(min-width: 1024px)").matches;
  const close = () => { aside.classList.add("-translate-x-full"); overlay?.classList.add("hidden"); };
  btn.addEventListener("click", () => {
    if (isDesktop()) {
      const collapsed = document.documentElement.classList.toggle("nav-collapsed");
      localStorage.setItem("fde-nav", collapsed ? "collapsed" : "open");
      return;
    }
    aside.classList.toggle("-translate-x-full");
    overlay?.classList.toggle("hidden");
  });
  overlay?.addEventListener("click", close);
  matchMedia("(min-width: 1024px)").addEventListener("change", (e) => {
    if (!e.matches) document.documentElement.classList.remove("nav-collapsed");
    else if (localStorage.getItem("fde-nav") === "collapsed") {
      document.documentElement.classList.add("nav-collapsed");
      close();
    }
  });
}

/* ---------- lab modals ---------- */
function bindModals() {
  document.querySelectorAll("[data-modal-open]").forEach((btn) =>
    btn.addEventListener("click", () => {
      const d = document.getElementById(btn.dataset.modalOpen);
      if (d && typeof d.showModal === "function") d.showModal();
    })
  );
  document.querySelectorAll("[data-modal-close]").forEach((btn) =>
    btn.addEventListener("click", () => btn.closest("dialog")?.close())
  );
}

document.addEventListener("DOMContentLoaded", () => {
  buildSidebar();
  bindModals();
  buildPageNav();
  decorateHero();
  buildIndexCards();
  buildTopicCards();
  buildLangSwitcher();
  bindChecklists();
  bindMobileMenu();
  document.querySelectorAll("[data-theme-toggle]").forEach((btn) =>
    btn.addEventListener("click", () => applyTheme(!isDark()))
  );
  setThemeIcons();
  renderMermaid();
});
