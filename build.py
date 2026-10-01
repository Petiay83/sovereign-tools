#!/usr/bin/env python3
"""
Sovereign Tools Builder & Orchestrator
Builds the static Hub portal, injects navigation into micro-tools, generates sitemap & robots,
and provides seamless automated deployment to GitHub Pages.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Ensure utf-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = ROOT_DIR / "registry.json"
TOOLS_DIR = ROOT_DIR / "tools"

def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_hub_html(registry):
    site = registry["site"]
    clusters = registry["clusters"]
    tools = registry["tools"]

    clusters_json = json.dumps(clusters, ensure_ascii=False)
    tools_json = json.dumps(tools, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{site["title"]} — Sovereign & Rational Micro-Tools</title>
  <meta name="description" content="{site["description"]}">
  <meta property="og:title" content="{site["title"]}">
  <meta property="og:description" content="{site["description"]}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{site["baseUrl"]}">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#f0fdf4',
              500: '#10b981',
              600: '#059669',
              900: '#064e3b'
            }}
          }}
        }}
      }}
    }}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
  </style>
</head>
<body class="bg-[#090d16] text-zinc-100 min-h-screen flex flex-col selection:bg-emerald-500 selection:text-black">

  <!-- Subtle Top Gradient Banner -->
  <div class="h-1 bg-gradient-to-r from-emerald-500 via-cyan-500 to-indigo-500"></div>

  <!-- Header -->
  <header class="border-b border-zinc-800/80 bg-zinc-950/60 backdrop-blur-md sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm">
          ⚡
        </div>
        <div>
          <a href="{site["baseUrl"]}/" class="font-bold text-lg tracking-tight hover:text-emerald-400 transition-colors">
            SOVEREIGN<span class="text-emerald-400">.TOOLS</span>
          </a>
        </div>
      </div>

      <div class="flex items-center gap-4 text-xs sm:text-sm">
        <span class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-950/50 border border-emerald-800/50 text-emerald-400 font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          100% Client-Side · Radical Privacy
        </span>
        <a href="{site["github"]}" target="_blank" rel="noopener noreferrer" 
           class="p-2 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800/60 transition-colors flex items-center gap-2 border border-zinc-800">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
          <span class="hidden md:inline">GitHub</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <main class="flex-1 max-w-6xl mx-auto px-4 sm:px-6 py-12 w-full">
    <div class="text-center max-w-3xl mx-auto mb-12">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-800/80 border border-zinc-700/60 text-xs text-zinc-300 mb-6">
        <span class="text-emerald-400">●</span> Zero-Tracking Architecture
      </div>
      <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-white mb-4 leading-tight">
        High-Precision Tools for the <br class="hidden sm:inline"/><span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-cyan-400 to-indigo-400">Autonomous Individual</span>
      </h1>
      <p class="text-zinc-400 text-sm sm:text-base leading-relaxed">
        No accounts, no cookie banners, zero latency. All calculations, models, and transformations execute exclusively in your browser's local memory.
      </p>
    </div>

    <!-- Search & Filter Controls -->
    <div class="mb-10 space-y-4">
      <div class="relative max-w-2xl mx-auto">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-zinc-400">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
        <input type="text" id="searchInput" placeholder="Search by name, problem, or tag (e.g. 'caffeine', 'tax', 'sleep')..."
               class="w-full pl-11 pr-4 py-3 bg-zinc-900/90 border border-zinc-800 rounded-xl text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all text-sm shadow-xl">
      </div>

      <!-- Cluster Filter Tabs -->
      <div class="flex flex-wrap items-center justify-center gap-2 pt-2" id="clusterFilters">
        <button data-cluster="all" class="cluster-btn px-4 py-1.5 rounded-lg text-xs font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 transition-all">
          All Tools
        </button>
"""
    for c in clusters:
        html += f"""        <button data-cluster="{c['id']}" class="cluster-btn px-4 py-1.5 rounded-lg text-xs font-medium bg-zinc-900 text-zinc-400 border border-zinc-800 hover:text-zinc-200 hover:border-zinc-700 transition-all">
          {c['icon']} {c['name']}
        </button>\n"""

    html += f"""      </div>
    </div>

    <!-- Tools Grid -->
    <div id="toolsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      <!-- Tool cards will be rendered dynamically by JavaScript -->
    </div>

    <!-- Empty State -->
    <div id="emptyState" class="hidden text-center py-16">
      <p class="text-zinc-500 text-sm">No tools match your search criteria.</p>
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-zinc-800/80 bg-zinc-950/40 mt-16 py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-zinc-500">
      <div class="flex items-center gap-2">
        <span>© {datetime.now().year} Sovereign Tools</span>
        <span>·</span>
        <span class="text-emerald-500/80">Local Client-Side Runtime</span>
      </div>
      <div class="flex items-center gap-6">
        <a href="{site["github"]}" class="hover:text-zinc-300 transition-colors">Contribute on GitHub</a>
        <a href="https://github.com/Petiay83/sovereign-tools/issues" class="hover:text-zinc-300 transition-colors">Request a Tool</a>
      </div>
    </div>
  </footer>

  <!-- State & Dynamic Rendering Script -->
  <script>
    const TOOLS = {tools_json};
    const CLUSTERS = {clusters_json};
    const BASE_URL = "{site["baseUrl"]}";

    let activeCluster = 'all';
    let searchQuery = '';

    const grid = document.getElementById('toolsGrid');
    const emptyState = document.getElementById('emptyState');
    const searchInput = document.getElementById('searchInput');
    const filterButtons = document.querySelectorAll('.cluster-btn');

    function renderTools() {{
      const filtered = TOOLS.filter(t => {{
        const matchesCluster = activeCluster === 'all' || t.cluster === activeCluster;
        const query = searchQuery.toLowerCase();
        const matchesSearch = !query || 
          t.title.toLowerCase().includes(query) ||
          t.description.toLowerCase().includes(query) ||
          (t.tags && t.tags.some(tag => tag.toLowerCase().includes(query)));
        return matchesCluster && matchesSearch;
      }});

      if (filtered.length === 0) {{
        grid.innerHTML = '';
        emptyState.classList.remove('hidden');
        return;
      }}

      emptyState.classList.add('hidden');
      grid.innerHTML = filtered.map(t => {{
        const cluster = CLUSTERS.find(c => c.id === t.cluster) || {{ name: 'Tool', icon: '⚡' }};
        const isLive = t.status === 'live';
        const url = isLive ? `${{BASE_URL}}/tools/${{t.id}}/` : '#';
        const statusBadge = isLive 
          ? `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>Live</span>`
          : `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">Ready to build</span>`;

        return `
          <div class="group relative flex flex-col justify-between p-6 bg-zinc-900/60 hover:bg-zinc-900 border border-zinc-800/80 hover:border-zinc-700 rounded-2xl transition-all duration-200 hover:shadow-2xl hover:shadow-emerald-950/20">
            <div>
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-medium text-zinc-400 flex items-center gap-1.5">
                  <span>${{cluster.icon}}</span> ${{cluster.name}}
                </span>
                ${{statusBadge}}
              </div>
              <h3 class="text-base font-semibold text-zinc-100 group-hover:text-emerald-400 transition-colors mb-2 leading-snug">
                ${{t.title}}
              </h3>
              <p class="text-xs text-zinc-400 leading-relaxed mb-4">
                ${{t.description}}
              </p>
            </div>
            
            <div>
              <div class="flex flex-wrap gap-1.5 mb-4">
                ${{(t.tags || []).map(tag => `<span class="text-[10px] px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono">#${{tag}}</span>`).join('')}}
              </div>
              <a href="${{url}}" 
                 class="w-full inline-flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-xs font-medium transition-all ${{
                   isLive 
                     ? 'bg-emerald-500/10 hover:bg-emerald-500 text-emerald-300 hover:text-black border border-emerald-500/30' 
                     : 'bg-zinc-800/40 text-zinc-500 border border-zinc-800 cursor-not-allowed'
                 }}">
                <span>${{isLive ? 'Launch Micro-Tool' : 'Coming Up'}}</span>
                ${{isLive ? '<span>→</span>' : ''}}
              </a>
            </div>
          </div>
        `;
      }}).join('');
    }}

    searchInput.addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      renderTools();
    }});

    filterButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        filterButtons.forEach(b => {{
          b.className = 'cluster-btn px-4 py-1.5 rounded-lg text-xs font-medium bg-zinc-900 text-zinc-400 border border-zinc-800 hover:text-zinc-200 hover:border-zinc-700 transition-all';
        }});
        btn.className = 'cluster-btn px-4 py-1.5 rounded-lg text-xs font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 transition-all';
        activeCluster = btn.getAttribute('data-cluster');
        renderTools();
      }});
    }});

    renderTools();
  </script>
</body>
</html>
"""
    return html

def generate_sitemap(registry):
    site = registry["site"]
    tools = registry["tools"]
    today = datetime.now().strftime("%Y-%m-%d")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{site["baseUrl"]}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
"""
    for t in tools:
        if t.get("status") == "live":
            xml += f"""  <url>
    <loc>{site["baseUrl"]}/tools/{t["id"]}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""
    xml += "</urlset>\n"
    return xml

def generate_robots(registry):
    site = registry["site"]
    return f"""User-agent: *
Allow: /

Sitemap: {site["baseUrl"]}/sitemap.xml
"""

def wrap_tool_content(tool_meta, content_html, registry):
    site = registry["site"]
    clusters = registry["clusters"]
    cluster = next((c for c in clusters if c["id"] == tool_meta["cluster"]), {"name": "Tool", "icon": "⚡"})

    full_html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{tool_meta["title"]} — Sovereign Tools</title>
  <meta name="description" content="{tool_meta["description"]}">
  <meta property="og:title" content="{tool_meta["title"]}">
  <meta property="og:description" content="{tool_meta["description"]}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{site["baseUrl"]}/tools/{tool_meta["id"]}/">
  
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#f0fdf4',
              500: '#10b981',
              600: '#059669',
              900: '#064e3b'
            }}
          }}
        }}
      }}
    }}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
  </style>
</head>
<body class="bg-[#090d16] text-zinc-100 min-h-screen flex flex-col selection:bg-emerald-500 selection:text-black">

  <div class="h-1 bg-gradient-to-r from-emerald-500 via-cyan-500 to-indigo-500"></div>

  <!-- Universal Tool Navbar -->
  <header class="border-b border-zinc-800/80 bg-zinc-950/60 backdrop-blur-md sticky top-0 z-50">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <a href="{site["baseUrl"]}/" class="text-zinc-400 hover:text-white flex items-center gap-1.5 text-xs font-medium px-2.5 py-1.5 rounded-lg hover:bg-zinc-800/60 transition-colors border border-transparent hover:border-zinc-800">
          <span>←</span>
          <span>Hub</span>
        </a>
        <span class="text-zinc-700">/</span>
        <span class="text-xs text-zinc-400 font-medium flex items-center gap-1">
          <span>{cluster["icon"]}</span> {cluster["name"]}
        </span>
      </div>

      <div class="flex items-center gap-3">
        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-950/50 border border-emerald-800/50 text-emerald-400 text-xs font-medium">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          Radical Privacy
        </span>
      </div>
    </div>
  </header>

  <!-- Tool App Container -->
  <main class="flex-1 max-w-5xl mx-auto px-4 sm:px-6 py-8 w-full">
    {content_html}
  </main>

  <footer class="border-t border-zinc-800/80 bg-zinc-950/40 mt-16 py-6">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 flex items-center justify-between text-xs text-zinc-500">
      <a href="{site["baseUrl"]}/" class="hover:text-zinc-300">← Back to All Sovereign Tools</a>
      <span class="text-emerald-500/70">100% Client-Side Execution</span>
    </div>
  </footer>
</body>
</html>
"""
    return full_html

def build_all():
    print("🚀 Building Sovereign Tools...")
    registry = load_registry()

    # 1. Build Hub index.html
    hub_html = generate_hub_html(registry)
    with open(ROOT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(hub_html)
    print("✅ Created index.html (Hub)")

    # 2. Build Tools
    tools_built = 0
    for tool in registry["tools"]:
        tool_id = tool["id"]
        tool_folder = TOOLS_DIR / tool_id
        content_file = tool_folder / "content.html"
        standalone_file = tool_folder / "index.html"

        if content_file.exists():
            with open(content_file, "r", encoding="utf-8") as f:
                content = f.read()
            wrapped = wrap_tool_content(tool, content, registry)
            with open(tool_folder / "index.html", "w", encoding="utf-8") as f:
                f.write(wrapped)
            tool["status"] = "live"
            tools_built += 1
            print(f"✅ Built tool: {tool_id}")
        elif standalone_file.exists():
            tool["status"] = "live"
            tools_built += 1
            print(f"✅ Found standalone tool: {tool_id}")

    # Re-save updated registry if statuses changed
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    # 3. Generate Sitemap & Robots
    with open(ROOT_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write(generate_sitemap(registry))
    print("✅ Generated sitemap.xml")

    with open(ROOT_DIR / "robots.txt", "w", encoding="utf-8") as f:
        f.write(generate_robots(registry))
    print("✅ Generated robots.txt")

    print(f"🎉 Build completed successfully! Active tools: {tools_built}")

def deploy():
    build_all()
    print("📦 Committing and pushing to GitHub...")
    subprocess.run(["git", "add", "."], cwd=ROOT_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "Update site and micro-tools"], cwd=ROOT_DIR)
    subprocess.run(["git", "push", "origin", "main"], cwd=ROOT_DIR, check=True)
    print("🌐 Pushed to GitHub main branch! GitHub Pages will refresh automatically.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--deploy":
        deploy()
    else:
        build_all()
