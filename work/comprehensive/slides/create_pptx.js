const pptxgen = require('pptxgenjs');
const html2pptx = require('c:/_code/implementation_arch_tactics/.claude/skills/pptx/scripts/html2pptx');
const fs = require('fs');
const path = require('path');

const SLIDES_DIR = __dirname;
const OUT = path.join(SLIDES_DIR, '..', 'study_guide.pptx');

// Colors (no # for pptxgenjs)
const C = {
  navy: '1B2A4A', teal: '2E86AB', coral: 'E8573A',
  light: 'F4F6F9', white: 'FFFFFF', dark: '2C2C2C',
  gray: '8899AA', midgray: 'D0D8E0', green: '27AE60'
};

// Standard HTML slide wrapper
function slide(body, bg = '#F4F6F9') {
  return `<!DOCTYPE html><html><head><style>
html{background:${bg};}
body{width:720pt;height:405pt;margin:0;padding:0;background:${bg};font-family:Arial,sans-serif;display:flex;flex-direction:column;}
h1{font-size:28pt;color:#1B2A4A;margin:0 0 8pt 0;line-height:1.2;}
h2{font-size:20pt;color:#2E86AB;margin:0 0 6pt 0;line-height:1.2;}
h3{font-size:16pt;color:#1B2A4A;margin:0 0 4pt 0;}
p{font-size:12pt;color:#2C2C2C;margin:0 0 6pt 0;line-height:1.4;}
ul,ol{font-size:12pt;color:#2C2C2C;margin:0 0 6pt 0;padding-left:18pt;line-height:1.5;}
li{margin-bottom:3pt;}
.stat{font-size:32pt;color:#E8573A;font-weight:bold;margin:0;}
.stat-label{font-size:11pt;color:#8899AA;margin:0 0 4pt 0;}
.accent{color:#2E86AB;font-weight:bold;}
.highlight{color:#E8573A;font-weight:bold;}
.quote{font-size:11pt;color:#1B2A4A;font-style:italic;margin:0 0 6pt 0;line-height:1.4;}
</style></head><body>${body}</body></html>`;
}

// Section divider slide
function sectionSlide(chNum, title, subtitle) {
  return `<!DOCTYPE html><html><head><style>
html{background:#1B2A4A;}
body{width:720pt;height:405pt;margin:0;padding:0;background:#1B2A4A;font-family:Arial,sans-serif;display:flex;flex-direction:column;justify-content:center;}
</style></head><body>
<div style="margin-left:60pt;">
<p style="font-size:14pt;color:#2E86AB;margin:0 0 6pt 0;">CHAPTER ${chNum}</p>
<h1 style="font-size:36pt;color:#FFFFFF;margin:0 0 12pt 0;">${title}</h1>
<p style="font-size:14pt;color:#8899AA;margin:0;max-width:500pt;">${subtitle}</p>
</div>
</body></html>`;
}

const slides = [];

// ===== SLIDE 1: Title =====
slides.push(`<!DOCTYPE html><html><head><style>
html{background:#1B2A4A;}
body{width:720pt;height:405pt;margin:0;padding:0;background:#1B2A4A;font-family:Arial,sans-serif;display:flex;flex-direction:column;justify-content:center;}
</style></head><body>
<div style="margin-left:60pt;margin-right:60pt;">
<p style="font-size:11pt;color:#2E86AB;margin:0 0 12pt 0;">INNOPOLIS UNIVERSITY — MS STUDY GUIDE, 2026</p>
<h1 style="font-size:30pt;color:#FFFFFF;margin:0 0 16pt 0;line-height:1.3;">Automated Implementation of Architectural Tactics for Software Quality Improvement</h1>
<div style="width:60pt;height:3pt;background:#E8573A;margin-bottom:16pt;"></div>
<p style="font-size:13pt;color:#8899AA;margin:0 0 4pt 0;">A Comprehensive Study Guide</p>
<p style="font-size:11pt;color:#8899AA;margin:0;">February 2026</p>
</div>
</body></html>`);

// ===== SLIDE 2: Agenda =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>Study Guide Overview</h1>
<div style="display:flex;gap:20pt;margin-top:10pt;">
<div style="flex:1;">
<div style="border-left:3pt solid #2E86AB;padding-left:10pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;">Ch 1: Motivation &amp; Context</h3>
<p style="font-size:10pt;color:#8899AA;">Why maintenance costs dominate</p>
</div>
<div style="border-left:3pt solid #2E86AB;padding-left:10pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;">Ch 2: SA Foundations</h3>
<p style="font-size:10pt;color:#8899AA;">Components, connectors, styles</p>
</div>
<div style="border-left:3pt solid #2E86AB;padding-left:10pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;">Ch 3: Quality &amp; Maintainability</h3>
<p style="font-size:10pt;color:#8899AA;">ISO 25010, metrics, SIG model</p>
</div>
<div style="border-left:3pt solid #2E86AB;padding-left:10pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;">Ch 4: Architectural Tactics</h3>
<p style="font-size:10pt;color:#8899AA;">15 modifiability tactics catalog</p>
</div>
<div style="border-left:3pt solid #E8573A;padding-left:10pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;">Ch 5: Architecture Erosion</h3>
<p style="font-size:10pt;color:#8899AA;">Detection-remediation gap</p>
</div>
</div>
<div style="flex:1;">
<div style="border-left:3pt solid #2E86AB;padding-left:10pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;">Ch 6: Assessment Methods</h3>
<p style="font-size:10pt;color:#8899AA;">Metrics, tools, agreement crisis</p>
</div>
<div style="border-left:3pt solid #2E86AB;padding-left:10pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;">Ch 7: LLMs for Refactoring</h3>
<p style="font-size:10pt;color:#8899AA;">MANTRA, prompts, pipelines</p>
</div>
<div style="border-left:3pt solid #E8573A;padding-left:10pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;">Ch 8: Challenges</h3>
<p style="font-size:10pt;color:#8899AA;">Technical, measurement, practical</p>
</div>
<div style="border-left:3pt solid #E8573A;padding-left:10pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;">Ch 9: Research Gaps</h3>
<p style="font-size:10pt;color:#8899AA;">The transformation gap</p>
</div>
<div style="background:#1B2A4A;border-radius:6pt;padding:12pt;margin-top:14pt;">
<p style="font-size:11pt;color:#FFFFFF;margin:0;"><b>40+ papers</b> reviewed across architectural tactics, maintainability, and LLM-based code transformation</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 3: Section - Motivation =====
slides.push(sectionSlide('1', 'Motivation & Context', 'Why software maintenance dominates lifecycle costs and how architectural decisions determine maintainability'));

// ===== SLIDE 4: The Maintenance Crisis =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>The Software Maintenance Crisis</h1>
<p>The root cause is rarely individual lines of code — it is <b>decisions at the architectural level</b> that determine how easily a system absorbs change.</p>
<div style="display:flex;gap:20pt;margin-top:14pt;">
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:16pt;text-align:center;">
<p class="stat">60–80%</p>
<p class="stat-label">Maintenance share of total lifecycle cost</p>
<p style="font-size:9pt;color:#8899AA;margin:0;">[Bass et al., 2021]</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:16pt;text-align:center;">
<p class="stat">75%</p>
<p class="stat-label">Development effort spent on refactoring</p>
<p style="font-size:9pt;color:#8899AA;margin:0;">[Fowler, 2018]</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:16pt;text-align:center;">
<p class="stat">83.8%</p>
<p class="stat-label">Practitioners reporting quality degradation from erosion</p>
<p style="font-size:9pt;color:#8899AA;margin:0;">[Li et al., 2021]</p>
</div>
</div>
<div style="background:#1B2A4A;border-radius:6pt;padding:12pt;margin-top:14pt;">
<p class="quote" style="color:#F4F6F9;font-style:italic;">"Software architecture can expose the dimensions along which a system is expected to evolve. By making explicit the <b style="color:#2E86AB;">load-bearing walls</b> of a system, maintainers can better understand the ramifications of changes."</p>
<p style="font-size:9pt;color:#8899AA;margin:0;">— Garlan &amp; Perry, 1995</p>
</div>
</div>`));

// ===== SLIDE 5: Knowledge Barrier =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>The Knowledge Barrier</h1>
<div style="display:flex;gap:20pt;">
<div style="flex:1;">
<h2 style="font-size:14pt;">Tactics Require Deep Knowledge</h2>
<ul>
<li>Architectural tactics are easy to state but hard to implement in real codebases</li>
<li>Require <b>inter-procedural changes</b> spanning multiple classes and packages</li>
<li>ChatGPT: 95% syntax-correct but only <span style="color:#E8573A;font-weight:bold;">5% semantically correct</span> on tactic synthesis [Shokri et al., 2024]</li>
</ul>
<h2 style="font-size:14pt;margin-top:10pt;">Detection ≠ Remediation</h2>
<ul>
<li>Rosik et al. (IBM): <span style="color:#E8573A;font-weight:bold;">0 of 9</span> detected violations were fixed by developers</li>
<li>Barriers: risk of ripple effects, time pressure, legacy entanglement</li>
<li>Developers <b>knew</b> about problems but chose not to fix them</li>
</ul>
</div>
<div style="flex:1;">
<div style="background:#FFFFFF;border-radius:6pt;padding:14pt;margin-bottom:10pt;">
<h3 style="font-size:12pt;color:#2E86AB;">The Vicious Cycle</h3>
<p style="font-size:11pt;">Technical debt causes erosion → erosion generates more debt → architecture degrades further</p>
<p style="font-size:9pt;color:#8899AA;margin:0;">[Li et al., 2021]</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:14pt;">
<h3 style="font-size:12pt;color:#27AE60;">The Promise</h3>
<p style="font-size:11pt;">LLMs can bridge the gap if placed in a <b>structured pipeline</b> with external verification</p>
<p style="font-size:11pt;">MANTRA: <span style="color:#27AE60;font-weight:bold;">82.8%</span> success rate with multi-agent pipeline vs 8.7% standalone</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 6: Section - SA Foundations =====
slides.push(sectionSlide('2', 'Software Architecture Foundations', 'Components, connectors, configurations, and the architectural styles that shape system quality'));

// ===== SLIDE 7: What Is Software Architecture? =====
slides.push(slide(`
<div style="margin:24pt 40pt;">
<h1 style="font-size:24pt;">What Is Software Architecture?</h1>
<div style="display:flex;gap:16pt;">
<div style="flex:1;">
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:6pt;">
<h3 style="font-size:12pt;color:#2E86AB;margin:0 0 2pt 0;">Perry &amp; Wolf (1992)</h3>
<p style="font-size:11pt;margin:0;"><b>Architecture = Elements + Form + Rationale</b></p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:6pt;">
<h3 style="font-size:12pt;color:#2E86AB;margin:0 0 2pt 0;">Garlan &amp; Shaw (1993)</h3>
<p style="font-size:11pt;margin:0;"><b>Components + Connectors + Configurations</b></p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:6pt;">
<h3 style="font-size:12pt;color:#2E86AB;margin:0 0 2pt 0;">Bass, Clements &amp; Kazman</h3>
<p style="font-size:11pt;margin:0;"><b>Structures needed to reason about the system</b></p>
</div>
<div style="background:#1B2A4A;border-radius:6pt;padding:10pt;">
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Architecture captures intent, not just structure — rationale is a first-class citizen</p>
</div>
</div>
<div style="flex:1;">
<h2 style="font-size:14pt;">Key Architectural Styles</h2>
<ul style="font-size:11pt;">
<li><b>Pipes-and-Filters:</b> Data flows through stages</li>
<li><b>Layered:</b> Hierarchical dependency rules</li>
<li><b>Event-Driven:</b> Components via events</li>
<li><b>Repository:</b> Shared data store</li>
<li><b>Client-Server:</b> Requestors and providers</li>
</ul>
<p style="font-size:10pt;color:#8899AA;margin-top:6pt;">KWIC case study: same problem in 4 styles yields different modifiability trade-offs</p>
</div>
</div>
</div>`));

// ===== SLIDE 8: Section - Quality =====
slides.push(sectionSlide('3', 'Quality & Maintainability', 'From McCall (1977) to ISO/IEC 25010 — how we define, decompose, and measure software quality'));

// ===== SLIDE 9: ISO 25010 =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>ISO/IEC 25010: Maintainability</h1>
<p>Maintainability is one of <b>8 quality characteristics</b>. It decomposes into 5 sub-characteristics:</p>
<div style="display:flex;gap:12pt;margin-top:12pt;">
<div style="flex:1;background:#2E86AB;border-radius:6pt;padding:12pt;">
<h3 style="font-size:13pt;color:#FFFFFF;">Modularity</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Changes to one component have minimal impact on others</p>
</div>
<div style="flex:1;background:#2E86AB;border-radius:6pt;padding:12pt;">
<h3 style="font-size:13pt;color:#FFFFFF;">Reusability</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Assets can be used in building other systems</p>
</div>
<div style="flex:1;background:#2E86AB;border-radius:6pt;padding:12pt;">
<h3 style="font-size:13pt;color:#FFFFFF;">Analysability</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Effectiveness of assessing change impact</p>
</div>
<div style="flex:1;background:#E8573A;border-radius:6pt;padding:12pt;">
<h3 style="font-size:13pt;color:#FFFFFF;">Modifiability</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Can be modified without degradation — <b>thesis focus</b></p>
</div>
<div style="flex:1;background:#2E86AB;border-radius:6pt;padding:12pt;">
<h3 style="font-size:13pt;color:#FFFFFF;">Testability</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Test criteria can be established and tests executed</p>
</div>
</div>
<div style="display:flex;gap:20pt;margin-top:14pt;">
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;">Key Finding: Hotspot Concentration</h3>
<p style="font-size:11pt;"><span style="color:#E8573A;font-weight:bold;">10% of packages</span> contain 80% of maintainability issues [Molnar &amp; Motogna, 2020]</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;">SIG Maintainability Model</h3>
<p style="font-size:11pt;">Visser's 10 guidelines with 1-5 star rating; issue resolution is <b>2x faster</b> in 4-star vs 2-star systems</p>
</div>
</div>
</div>`));

// ===== SLIDE 10: Section - Tactics =====
slides.push(sectionSlide('4', 'Architectural Tactics', 'Design decisions that influence the achievement of a quality attribute response'));

// ===== SLIDE 11: What Are Tactics? =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>What Are Architectural Tactics?</h1>
<div style="display:flex;gap:20pt;">
<div style="flex:1;">
<div style="background:#1B2A4A;border-radius:6pt;padding:14pt;margin-bottom:12pt;">
<p style="font-size:13pt;color:#FFFFFF;margin:0;"><b>Definition:</b> A design decision that influences the achievement of a quality attribute response</p>
<p style="font-size:10pt;color:#8899AA;margin:4pt 0 0 0;">— Bass, Clements &amp; Kazman, 2021</p>
</div>
<h2 style="font-size:14pt;">Design Hierarchy</h2>
<ul>
<li><b>Style:</b> Overall system organization (e.g., Layered)</li>
<li><b>Pattern:</b> Recurring solution (e.g., MVC)</li>
<li><b>Tactic:</b> Targeted quality decision (e.g., Use Intermediary)</li>
<li><b>Technique:</b> Implementation detail (e.g., Adapter class)</li>
</ul>
<p style="font-size:11pt;margin-top:8pt;">Kassab et al.: <span style="color:#E8573A;font-weight:bold;">63%</span> of projects modify patterns with tactics</p>
</div>
<div style="flex:1;">
<h2 style="font-size:14pt;">Stimulus → Tactic → Response</h2>
<div style="background:#FFFFFF;border-radius:6pt;padding:12pt;margin-bottom:10pt;">
<p style="font-size:11pt;"><b>Stimulus:</b> A change request arrives</p>
<p style="font-size:11pt;"><b>Tactic:</b> Use an Intermediary to decouple</p>
<p style="font-size:11pt;margin:0;"><b>Response:</b> Change is confined to fewer modules</p>
</div>
<h2 style="font-size:14pt;">Tactic Research Landscape</h2>
<ul>
<li>Marquez (2022): 91 studies surveyed</li>
<li><span style="color:#E8573A;font-weight:bold;">71%</span> don't describe identification method</li>
<li>Detection: NLP/BERT, ML classifiers, Archie, ArchEngine</li>
<li>The rigor gap: most studies are qualitative</li>
</ul>
</div>
</div>
</div>`));

// ===== SLIDE 12: Modifiability Tactics Catalog =====
slides.push(slide(`
<div style="margin:26pt 40pt;">
<h1>Modifiability Tactics Catalog</h1>
<div style="display:flex;gap:16pt;margin-top:8pt;">
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:12pt;">
<div style="background:#2E86AB;border-radius:4pt;padding:6pt 10pt;margin-bottom:8pt;">
<h3 style="font-size:12pt;color:#FFFFFF;margin:0;">Increase Cohesion</h3>
</div>
<ul style="font-size:10pt;">
<li>Split Module</li>
<li>Increase Semantic Coherence</li>
<li>Abstract Common Services</li>
<li>Encapsulate</li>
<li>Restrict Dependencies</li>
</ul>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:12pt;">
<div style="background:#E8573A;border-radius:4pt;padding:6pt 10pt;margin-bottom:8pt;">
<h3 style="font-size:12pt;color:#FFFFFF;margin:0;">Reduce Coupling</h3>
</div>
<ul style="font-size:10pt;">
<li>Use an Intermediary</li>
<li>Use Encapsulation</li>
<li>Restrict Dependencies</li>
<li>Abstract Common Services</li>
</ul>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:12pt;">
<div style="background:#1B2A4A;border-radius:4pt;padding:6pt 10pt;margin-bottom:8pt;">
<h3 style="font-size:12pt;color:#FFFFFF;margin:0;">Defer Binding</h3>
</div>
<ul style="font-size:10pt;">
<li>Component Replacement</li>
<li>Publish-Subscribe</li>
<li>Configuration Files</li>
<li>Polymorphism</li>
<li>Protocol Binding</li>
<li>Runtime Registration</li>
</ul>
</div>
</div>
<div style="display:flex;gap:16pt;margin-top:10pt;">
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:10pt;">
<p style="font-size:11pt;margin:0;"><b>SOA:</b> Reduce Coupling dominates (49%) [Bogner, 2019]</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:10pt;">
<p style="font-size:11pt;margin:0;"><b>Microservices:</b> Defer Binding dominates (52%) [Bogner, 2019]</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:10pt;">
<p style="font-size:11pt;margin:0;"><b>Harrison (2010):</b> 7 interaction types between patterns &amp; tactics</p>
</div>
</div>
</div>`));

// ===== SLIDE 13: Section - Erosion =====
slides.push(sectionSlide('5', 'Architecture Erosion & Drift', 'Why detection alone does not solve architectural degradation'));

// ===== SLIDE 14: Erosion vs Drift =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>Erosion vs. Drift</h1>
<div style="display:flex;gap:20pt;">
<div style="flex:1;">
<div style="background:#E8573A;border-radius:6pt;padding:14pt;margin-bottom:10pt;">
<h3 style="font-size:14pt;color:#FFFFFF;">Erosion = Breaking the Rules</h3>
<p style="font-size:11pt;color:#FFFFFF;margin:0;">Explicit constraints violated — e.g., controller directly accessing the database layer</p>
</div>
<div style="background:#2E86AB;border-radius:6pt;padding:14pt;margin-bottom:10pt;">
<h3 style="font-size:14pt;color:#FFFFFF;">Drift = Losing the Map</h3>
<p style="font-size:11pt;color:#FFFFFF;margin:0;">Gradual divergence — no single rule broken, but the system drifts from intended design</p>
</div>
<h2 style="font-size:14pt;">Li et al. (2021) — Four Perspectives</h2>
<ul>
<li><b>Violation:</b> Implementation violates intended architecture</li>
<li><b>Structure:</b> Cyclic dependencies, god classes accumulate</li>
<li><b>Quality:</b> Maintainability, performance degrade</li>
<li><b>Evolution:</b> Architecture resists change</li>
</ul>
</div>
<div style="flex:1;">
<h2 style="font-size:14pt;">Causes of Erosion</h2>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:8pt;">
<p style="font-size:11pt;margin:0;"><b>Architecture violation</b> — 24.7%</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:8pt;">
<p style="font-size:11pt;margin:0;"><b>Evolution issues</b> — 23.3%</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:8pt;">
<p style="font-size:11pt;margin:0;"><b>Technical debt</b> — 17.8%</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:8pt;">
<p style="font-size:11pt;margin:0;"><b>Knowledge vaporization</b> — 15.1%</p>
</div>
<div style="background:#1B2A4A;border-radius:6pt;padding:12pt;margin-top:8pt;">
<p style="font-size:11pt;color:#F4F6F9;margin:0;"><b>35 tools</b> cataloged for erosion detection, but <span style="color:#E8573A;">82.2%</span> of studies are academic — developers don't use them in practice</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 15: IBM Case Study =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>IBM Dublin Case Study [Rosik et al., 2011]</h1>
<p>2-year longitudinal study of DAP 2.0 (28,500 LOC) using Reflexion Modelling</p>
<div style="display:flex;gap:20pt;margin-top:12pt;">
<div style="flex:1;">
<div style="display:flex;gap:12pt;margin-bottom:12pt;">
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:14pt;text-align:center;">
<p class="stat" style="font-size:36pt;">9</p>
<p class="stat-label">Divergent edges detected</p>
</div>
<div style="flex:1;background:#E8573A;border-radius:6pt;padding:14pt;text-align:center;">
<p class="stat" style="font-size:36pt;color:#FFFFFF;">0</p>
<p style="font-size:11pt;color:#FFFFFF;margin:0;">Violations fixed</p>
</div>
</div>
<h2 style="font-size:14pt;">Why Violations Persist</h2>
<ul>
<li><b>Risk aversion:</b> "Fixing minor issues might cause larger ones"</li>
<li><b>Cost-benefit:</b> Minor violations perceived as not worth the effort</li>
<li><b>Time pressure:</b> Architectural fixes never "in scope"</li>
</ul>
</div>
<div style="flex:1;">
<h2 style="font-size:14pt;">Hidden Violations</h2>
<p>5 of 8 convergent edges contained hidden divergent relationships</p>
<p>Worst case: 1 edge masked <span style="color:#E8573A;font-weight:bold;">41 of 44</span> inconsistent relationships</p>
<div style="background:#1B2A4A;border-radius:6pt;padding:12pt;margin-top:10pt;">
<p class="quote" style="color:#F4F6F9;">"If performance can be gained by breaking an architectural design, then this can sometimes be acceptable... time pressure is probably the main factor."</p>
<p style="font-size:9pt;color:#8899AA;margin:0;">— IBM developer</p>
</div>
<div style="background:#27AE60;border-radius:6pt;padding:10pt;margin-top:10pt;">
<p style="font-size:11pt;color:#FFFFFF;margin:0;"><b>Key insight:</b> Continuous monitoring needed, not batch detection</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 16: Detection-Remediation Gap =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>The Detection-Remediation Gap</h1>
<div style="display:flex;gap:20pt;">
<div style="flex:1;">
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:8pt;border-left:4pt solid #E8573A;">
<p style="font-size:11pt;margin:0;"><b>Detection exists but is underused</b> — 35 tools, but 82.2% academic-only</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:8pt;border-left:4pt solid #E8573A;">
<p style="font-size:11pt;margin:0;"><b>Detection does not lead to action</b> — 0/9 violations fixed at IBM</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:8pt;border-left:4pt solid #E8573A;">
<p style="font-size:11pt;margin:0;"><b>Knowledge exists but is fragmented</b> — 21% of QA-tactic relationships are undocumented</p>
</div>
<h2 style="font-size:14pt;margin-top:10pt;">Current Workflow (Manual)</h2>
<p style="font-size:11pt;">Detection → <span style="color:#E8573A;">Manual Analysis</span> → <span style="color:#E8573A;">Manual Design</span> → <span style="color:#E8573A;">Manual Implementation</span></p>
<p style="font-size:10pt;color:#8899AA;">Each step is a barrier; each barrier defers the fix</p>
</div>
<div style="flex:1;">
<h2 style="font-size:14pt;">Proposed Workflow (Automated)</h2>
<div style="background:#27AE60;border-radius:6pt;padding:12pt;margin-bottom:10pt;">
<p style="font-size:12pt;color:#FFFFFF;margin:0;"><b>Detection → LLM: Select Tactic → LLM: Implement → Static Analysis Validation</b></p>
</div>
<h2 style="font-size:14pt;">How LLMs Address Barriers</h2>
<ul>
<li><b>Risk reduced:</b> Changes validated by testing before deployment</li>
<li><b>Cost reduced:</b> No human architect needed for solution design</li>
<li><b>Time reduced:</b> Automated, runs in CI/CD on every commit</li>
</ul>
<div style="background:#1B2A4A;border-radius:6pt;padding:10pt;margin-top:8pt;">
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Stack Overflow mining (Bi et al., 2021): <b>4,195 posts</b> on tactics, but only 11% discuss applying tactics to existing systems</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 17: Section - Assessment =====
slides.push(sectionSlide('6', 'Maintainability Assessment', 'Metrics, tools, and the surprising disagreement between static analysis tools'));

// ===== SLIDE 18: Key Metrics =====
slides.push(slide(`
<div style="margin:26pt 40pt;">
<h1>Key Maintainability Metrics</h1>
<div style="display:flex;gap:16pt;margin-top:8pt;">
<div style="flex:1;">
<div style="background:#FFFFFF;border-radius:6pt;padding:12pt;margin-bottom:8pt;">
<h3 style="font-size:12pt;color:#2E86AB;">Maintainability Index (MI)</h3>
<p style="font-size:10pt;margin:0;">MI = 171 - 5.2·ln(V) - 0.23·G - 16.2·ln(LOC)</p>
<p style="font-size:9pt;color:#8899AA;margin:2pt 0 0 0;">&gt;85 = A (good), 65-85 = B, &lt;65 = C (bad)</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:12pt;margin-bottom:8pt;">
<h3 style="font-size:12pt;color:#2E86AB;">Cyclomatic Complexity (CC)</h3>
<p style="font-size:10pt;margin:0;">Decision points + 1; Visser recommends CC ≤ 5</p>
<p style="font-size:9pt;color:#8899AA;margin:2pt 0 0 0;">1-10 = Low, 11-20 = Moderate, 21-50 = High, &gt;50 = Very High</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;color:#2E86AB;">Halstead Volume</h3>
<p style="font-size:10pt;margin:0;">V = N · log2(n) — information content of the program</p>
<p style="font-size:9pt;color:#8899AA;margin:2pt 0 0 0;">Used in MI formula; higher = harder to maintain</p>
</div>
</div>
<div style="flex:1;">
<div style="background:#FFFFFF;border-radius:6pt;padding:12pt;margin-bottom:8pt;">
<h3 style="font-size:12pt;color:#E8573A;">CK Object-Oriented Suite</h3>
<p style="font-size:10pt;margin:0;"><b>CBO</b> — Coupling Between Objects (#1 cited metric, 18 studies)</p>
<p style="font-size:10pt;margin:0;"><b>RFC</b> — Response For a Class (#2 cited, 17 studies)</p>
<p style="font-size:10pt;margin:0;"><b>WMC</b> — Weighted Methods per Class</p>
<p style="font-size:10pt;margin:0;"><b>LCOM</b> — Lack of Cohesion in Methods</p>
<p style="font-size:10pt;margin:0;"><b>DIT/NOC</b> — Inheritance depth/breadth</p>
</div>
<div style="background:#1B2A4A;border-radius:6pt;padding:12pt;">
<p style="font-size:11pt;color:#F4F6F9;margin:0;">Ardito et al. (2020): <b>174 distinct metrics</b> cataloged, but 75% appear in only a single paper. Field has converged on ~15 core metrics.</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 19: Agreement Crisis =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>The Agreement Crisis</h1>
<p>[Lenarduzzi et al., 2023] — 6 tools × 47 Java projects</p>
<div style="display:flex;gap:20pt;margin-top:10pt;">
<div style="flex:1;">
<div style="background:#E8573A;border-radius:6pt;padding:18pt;text-align:center;margin-bottom:12pt;">
<p style="font-size:40pt;color:#FFFFFF;font-weight:bold;margin:0;">&lt; 0.4%</p>
<p style="font-size:13pt;color:#FFFFFF;margin:0;">Overall inter-tool detection agreement</p>
</div>
<h2 style="font-size:14pt;">Tool Precision</h2>
<ul>
<li>CheckStyle: <b>86%</b> (mostly formatting)</li>
<li>FindBugs: <b>57%</b></li>
<li>PMD: <b>52%</b></li>
<li>SonarQube: <b>18%</b> (broadest but least precise)</li>
</ul>
</div>
<div style="flex:1;">
<div style="background:#1B2A4A;border-radius:6pt;padding:14pt;margin-bottom:12pt;">
<p class="quote" style="color:#F4F6F9;">"There is no silver bullet that is able to guarantee source code quality assessment on its own."</p>
<p style="font-size:9pt;color:#8899AA;margin:0;">— Lenarduzzi et al., 2023</p>
</div>
<h2 style="font-size:14pt;">Implications</h2>
<ul>
<li>Any improvement measured by a <b>single tool</b> may not be confirmed by another</li>
<li>Cui et al. (2024): 35.7% of FN/FP from <b>missing cases</b></li>
<li>Issue count ≠ debt reduction (ratio as low as 0.71)</li>
</ul>
<div style="background:#27AE60;border-radius:6pt;padding:10pt;margin-top:8pt;">
<p style="font-size:11pt;color:#FFFFFF;margin:0;"><b>Solution: Multi-tool validation</b> — Radon + SonarQube + Pylint + custom architecture analysis</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 20: Section - LLMs =====
slides.push(sectionSlide('7', 'LLMs for Code Refactoring', 'From code completion to code transformation — capabilities, pipelines, and the architecture gap'));

// ===== SLIDE 21: LLM Revolution =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>The LLM Revolution in SE</h1>
<p>From syntax-level code completion (2021) to semantic-level code transformation (2023+)</p>
<div style="display:flex;gap:20pt;margin-top:10pt;">
<div style="flex:1;">
<h2 style="font-size:14pt;">What LLMs Handle Well</h2>
<div style="background:#27AE60;border-radius:6pt;padding:10pt;margin-bottom:8pt;">
<ul style="font-size:10pt;color:#FFFFFF;margin:0;">
<li>Rename Method/Variable</li>
<li>Extract Method</li>
<li>Simplify Conditionals</li>
<li>Remove Dead Code</li>
<li>Inline Variable</li>
</ul>
</div>
<p style="font-size:10pt;color:#8899AA;">Local, single-file, pattern-based</p>
</div>
<div style="flex:1;">
<h2 style="font-size:14pt;">What LLMs Struggle With</h2>
<div style="background:#E8573A;border-radius:6pt;padding:10pt;margin-bottom:8pt;">
<ul style="font-size:10pt;color:#FFFFFF;margin:0;">
<li>Extract Class (0% recall with generic prompts)</li>
<li>Move Method (cross-file)</li>
<li>Split Class</li>
<li>Extract Superclass</li>
</ul>
</div>
<p style="font-size:10pt;color:#8899AA;">Structural, cross-file, design-judgment</p>
</div>
<div style="flex:1;">
<h2 style="font-size:14pt;">Key Stats</h2>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:6pt;">
<p style="font-size:18pt;color:#E8573A;font-weight:bold;margin:0;">97.2%</p>
<p style="font-size:9pt;margin:0;">Behavior preservation [DePalma]</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:6pt;">
<p style="font-size:18pt;color:#E8573A;font-weight:bold;margin:0;">86.7%</p>
<p style="font-size:9pt;margin:0;">Recall with optimized prompts [Liu]</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;">
<p style="font-size:18pt;color:#2E86AB;font-weight:bold;margin:0;">3.7%</p>
<p style="font-size:9pt;margin:0;">Agentic refactorings >1 file</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 22: Prompt Engineering =====
slides.push(slide(`
<div style="margin:28pt 40pt;">
<h1>Prompt Engineering for Refactoring</h1>
<p>[Piao et al., 2025] — 5 strategies across all 61 Fowler refactoring types</p>
<div style="display:flex;gap:16pt;margin-top:10pt;">
<div style="flex:2;">
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;display:flex;margin-bottom:6pt;">
<div style="flex:2;"><p style="font-size:11pt;margin:0;"><b>Zero-Shot</b> — Just the refactoring name</p></div>
<div style="flex:1;text-align:right;"><p style="font-size:11pt;margin:0;color:#E8573A;">47.5% / 91.8%</p></div>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;display:flex;margin-bottom:6pt;">
<div style="flex:2;"><p style="font-size:11pt;margin:0;"><b>Two-Shot</b> — Two worked examples</p></div>
<div style="flex:1;text-align:right;"><p style="font-size:11pt;margin:0;color:#E8573A;">57.4% / 95.1%</p></div>
</div>
<div style="background:#27AE60;border-radius:6pt;padding:10pt;display:flex;margin-bottom:6pt;">
<div style="flex:2;"><p style="font-size:11pt;margin:0;color:#FFFFFF;"><b>Step-by-Step</b> — Procedural instructions</p></div>
<div style="flex:1;text-align:right;"><p style="font-size:11pt;margin:0;color:#FFFFFF;font-weight:bold;">83.6% / 100%</p></div>
</div>
<div style="background:#27AE60;border-radius:6pt;padding:10pt;display:flex;margin-bottom:6pt;">
<div style="flex:2;"><p style="font-size:11pt;margin:0;color:#FFFFFF;"><b>Rule-based</b> — Detection heuristics</p></div>
<div style="flex:1;text-align:right;"><p style="font-size:11pt;margin:0;color:#FFFFFF;font-weight:bold;">80.3% / 100%</p></div>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;display:flex;">
<div style="flex:2;"><p style="font-size:11pt;margin:0;"><b>Objective Learning</b> — High-level goal only</p></div>
<div style="flex:1;text-align:right;"><p style="font-size:11pt;margin:0;color:#8899AA;">29–36% / 31–38%</p></div>
</div>
<p style="font-size:9pt;color:#8899AA;margin-top:6pt;">Format: GPT-4o-mini / DeepSeek-V3 success rates</p>
</div>
<div style="flex:1;">
<div style="background:#1B2A4A;border-radius:6pt;padding:12pt;margin-bottom:10pt;">
<p style="font-size:12pt;color:#FFFFFF;margin:0;">Generic → Subcategory prompt boosts success from <span style="color:#E8573A;">15.6%</span> to <span style="color:#27AE60;">86.7%</span></p>
<p style="font-size:9pt;color:#8899AA;margin:4pt 0 0 0;">[Liu et al., 2025]</p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;color:#2E86AB;">Key Insight</h3>
<p style="font-size:10pt;margin:0;">Rule-based instructions (pre/post conditions) outperform descriptive ones — LLMs follow mechanical rules better than natural language</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 23: MANTRA =====
slides.push(slide(`
<div style="margin:28pt 40pt;">
<h1>MANTRA: Multi-Agent Refactoring</h1>
<p>[Xu et al., 2025] — The most significant advance in LLM-based refactoring to date</p>
<div style="display:flex;gap:20pt;margin-top:10pt;">
<div style="flex:1;">
<div style="display:flex;gap:8pt;margin-bottom:10pt;">
<div style="flex:1;background:#2E86AB;border-radius:6pt;padding:10pt;">
<h3 style="font-size:11pt;color:#FFFFFF;margin:0;">Developer Agent</h3>
<p style="font-size:9pt;color:#F4F6F9;margin:4pt 0 0 0;">Generates code via Context-Aware RAG</p>
</div>
<div style="flex:1;background:#E8573A;border-radius:6pt;padding:10pt;">
<h3 style="font-size:11pt;color:#FFFFFF;margin:0;">Reviewer Agent</h3>
<p style="font-size:9pt;color:#F4F6F9;margin:4pt 0 0 0;">Validates via SE tools (most critical)</p>
</div>
<div style="flex:1;background:#1B2A4A;border-radius:6pt;padding:10pt;">
<h3 style="font-size:11pt;color:#FFFFFF;margin:0;">Repair Agent</h3>
<p style="font-size:9pt;color:#F4F6F9;margin:4pt 0 0 0;">Iterative fixes via Reflexion</p>
</div>
</div>
<div style="display:flex;gap:10pt;">
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:12pt;text-align:center;">
<p style="font-size:28pt;color:#27AE60;font-weight:bold;margin:0;">82.8%</p>
<p style="font-size:10pt;margin:0;">MANTRA success</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:12pt;text-align:center;">
<p style="font-size:28pt;color:#E8573A;font-weight:bold;margin:0;">8.7%</p>
<p style="font-size:10pt;margin:0;">Raw GPT baseline</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:12pt;text-align:center;">
<p style="font-size:28pt;color:#2E86AB;font-weight:bold;margin:0;">9.5x</p>
<p style="font-size:10pt;margin:0;">Improvement</p>
</div>
</div>
</div>
<div style="flex:1;">
<h2 style="font-size:14pt;">Ablation: What Matters Most</h2>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:6pt;border-left:4pt solid #E8573A;">
<p style="font-size:11pt;margin:0;">Without Reviewer: <b>-61.9%</b></p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:6pt;border-left:4pt solid #E8573A;">
<p style="font-size:11pt;margin:0;">Without Repair: <b>-50.7%</b></p>
</div>
<div style="background:#FFFFFF;border-radius:6pt;padding:10pt;margin-bottom:10pt;border-left:4pt solid #2E86AB;">
<p style="font-size:11pt;margin:0;">Without RAG: <b>-40.7%</b></p>
</div>
<div style="background:#1B2A4A;border-radius:6pt;padding:12pt;">
<p style="font-size:11pt;color:#F4F6F9;margin:0;"><b>Key principle:</b> External verification via traditional tools is more valuable than additional LLM reasoning</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 24: Tool-Integrated Pipelines =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>Tool-Integrated Pipelines</h1>
<div style="display:flex;gap:20pt;">
<div style="flex:1;">
<h2 style="font-size:14pt;">SonarQube + LLM Loop [Goncalves, 2025]</h2>
<div style="background:#FFFFFF;border-radius:6pt;padding:12pt;margin-bottom:10pt;">
<p style="font-size:11pt;">Codebase → SonarQube Analysis → Issues List → LLM Prompt → Fix → Re-analyze → Repeat</p>
</div>
<ul>
<li>Best config: <span style="color:#27AE60;font-weight:bold;">81.3%</span> issue reduction</li>
<li>Average: &gt;58% across all configurations</li>
<li>5 iterations outperform 2 (diminishing returns after 3-4)</li>
<li>Low temp (0.1) + zero-shot = most consistent</li>
</ul>
<div style="background:#E8573A;border-radius:6pt;padding:10pt;margin-top:8pt;">
<p style="font-size:10pt;color:#FFFFFF;margin:0;"><b>Caveat:</b> 58.8% issue reduction = only 42.1% debt reduction (ratio 0.71). LLMs can create new issues while fixing others.</p>
</div>
</div>
<div style="flex:1;">
<h2 style="font-size:14pt;">Agentic Refactoring [Horikawa, 2025]</h2>
<p>15,451 instances from AIDev dataset — largest corpus</p>
<ul>
<li>26.1% of agentic commits target refactoring</li>
<li>Dominant: Rename (10.4%), Change Type (11.8%)</li>
<li>Only <span style="color:#E8573A;font-weight:bold;">3.7%</span> touch more than one file</li>
<li>Median design smell delta: <b>0.00</b></li>
<li>86.9% of PRs merged despite low impact</li>
</ul>
<div style="background:#1B2A4A;border-radius:6pt;padding:12pt;margin-top:8pt;">
<p class="quote" style="color:#F4F6F9;">"Agentic coding tools serve as <b style="color:#2E86AB;">incremental cleanup partners</b>, not software architects."</p>
<p style="font-size:9pt;color:#8899AA;margin:0;">— Horikawa et al., 2025</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 25: Code vs Architecture Gap =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>The Code-Level vs. Architecture-Level Gap</h1>
<p><b>No existing work uses LLMs to implement architectural tactics.</b></p>
<div style="display:flex;gap:16pt;margin-top:10pt;">
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;color:#2E86AB;">Code-Level (Current)</h3>
<ul style="font-size:10pt;">
<li><b>Scope:</b> Single method or class</li>
<li><b>Context:</b> Local (&lt;300 LOC)</li>
<li><b>Examples:</b> Extract Method, Rename</li>
<li><b>Files touched:</b> 1 (96.3%)</li>
<li><b>Design judgment:</b> Minimal</li>
<li><b>Best success:</b> 82.8% (MANTRA)</li>
</ul>
</div>
<div style="flex:1;background:#E8573A;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;color:#FFFFFF;">Architecture-Level (Thesis Gap)</h3>
<ul style="font-size:10pt;color:#FFFFFF;">
<li><b>Scope:</b> Multiple modules/packages</li>
<li><b>Context:</b> System-wide (project structure)</li>
<li><b>Examples:</b> Split Module, Use Intermediary</li>
<li><b>Files touched:</b> 5-15+</li>
<li><b>Design judgment:</b> Substantial</li>
<li><b>Best success:</b> Unknown — no data</li>
</ul>
</div>
</div>
<div style="display:flex;gap:16pt;margin-top:10pt;">
<div style="flex:1;background:#1B2A4A;border-radius:6pt;padding:10pt;">
<p style="font-size:10pt;color:#F4F6F9;margin:0;"><b>Why the gap:</b> Context window limits, no architecture-aware tools, training data bias (most commits are code-level)</p>
</div>
<div style="flex:1;background:#1B2A4A;border-radius:6pt;padding:10pt;">
<p style="font-size:10pt;color:#F4F6F9;margin:0;"><b>The opportunity:</b> Patterns from MANTRA + SonarQube pipeline can be extended from code-level to architecture-level</p>
</div>
</div>
</div>`));

// ===== SLIDE 26: Section - Challenges =====
slides.push(sectionSlide('8', 'Challenges & Limitations', 'Five core technical challenges and the measurement problems that complicate evaluation'));

// ===== SLIDE 27: Technical Challenges =====
slides.push(slide(`
<div style="margin:26pt 40pt;">
<h1>Five Core Technical Challenges</h1>
<div style="display:flex;gap:10pt;margin-top:8pt;">
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:10pt;">
<div style="background:#E8573A;border-radius:4pt;padding:4pt 8pt;margin-bottom:6pt;display:inline-block;">
<p style="font-size:9pt;color:#FFFFFF;margin:0;font-weight:bold;">HIGH</p>
</div>
<h3 style="font-size:12pt;">Context Blindness</h3>
<p style="font-size:9pt;margin:0;">LLMs see one file, tactics span many. RAG helps 40.7%.</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:10pt;">
<div style="background:#E8573A;border-radius:4pt;padding:4pt 8pt;margin-bottom:6pt;display:inline-block;">
<p style="font-size:9pt;color:#FFFFFF;margin:0;font-weight:bold;">CRITICAL</p>
</div>
<h3 style="font-size:12pt;">Hallucinations</h3>
<p style="font-size:9pt;margin:0;">95% syntax-correct but only 5% semantically correct on tactics.</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:10pt;">
<div style="background:#E8573A;border-radius:4pt;padding:4pt 8pt;margin-bottom:6pt;display:inline-block;">
<p style="font-size:9pt;color:#FFFFFF;margin:0;font-weight:bold;">HIGH</p>
</div>
<h3 style="font-size:12pt;">Token Limits</h3>
<p style="font-size:9pt;margin:0;">Performance degrades beyond ~300 LOC. Tactics need 10K+.</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:10pt;">
<div style="background:#E8573A;border-radius:4pt;padding:4pt 8pt;margin-bottom:6pt;display:inline-block;">
<p style="font-size:9pt;color:#FFFFFF;margin:0;font-weight:bold;">HIGH</p>
</div>
<h3 style="font-size:12pt;">Complexity Gap</h3>
<p style="font-size:9pt;margin:0;">0% Extract Class recall; agents are "cleanup partners."</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:10pt;">
<div style="background:#2E86AB;border-radius:4pt;padding:4pt 8pt;margin-bottom:6pt;display:inline-block;">
<p style="font-size:9pt;color:#FFFFFF;margin:0;font-weight:bold;">MEDIUM</p>
</div>
<h3 style="font-size:12pt;">Non-Determinism</h3>
<p style="font-size:9pt;margin:0;">Same prompt → different outputs. Temp=0 helps.</p>
</div>
</div>
<div style="display:flex;gap:16pt;margin-top:10pt;">
<div style="flex:1;background:#1B2A4A;border-radius:6pt;padding:10pt;">
<h3 style="font-size:11pt;color:#FFFFFF;">Measurement Challenges</h3>
<ul style="font-size:9pt;color:#F4F6F9;">
<li>Tool disagreement: &lt;0.4%</li>
<li>No tactic-specific metrics</li>
<li>Java-dominated datasets</li>
<li>Small benchmarks (IPSynth: 20 tasks)</li>
</ul>
</div>
<div style="flex:1;background:#1B2A4A;border-radius:6pt;padding:10pt;">
<h3 style="font-size:11pt;color:#FFFFFF;">Practical Challenges</h3>
<ul style="font-size:9pt;color:#F4F6F9;">
<li>Detection-remediation gap (0/9 fixed)</li>
<li>Developer resistance to automated changes</li>
<li>Behavior preservation vs. architecture improvement</li>
<li>Strict preservation may be inappropriate for tactic-level</li>
</ul>
</div>
</div>
</div>`));

// ===== SLIDE 28: Section - Research Gaps =====
slides.push(sectionSlide('9', 'Research Gaps & Future Directions', 'The transformation gap and the five-point research agenda'));

// ===== SLIDE 29: Transformation Gap =====
slides.push(slide(`
<div style="margin:28pt 40pt;">
<h1>The Transformation Gap</h1>
<p>Two mature research streams exist in <b>almost complete isolation</b></p>
<div style="display:flex;gap:12pt;margin-top:10pt;">
<div style="flex:1;background:#2E86AB;border-radius:6pt;padding:12pt;">
<h3 style="font-size:13pt;color:#FFFFFF;">Stream 1: Tactic Detection</h3>
<ul style="font-size:10pt;color:#FFFFFF;">
<li>Marquez: 91 studies surveyed</li>
<li>ArchTacRV: ML-based detection</li>
<li>IPSynth: 85% via program synthesis</li>
<li>Bi et al.: 4,195 SO posts mined</li>
</ul>
</div>
<div style="flex:0 0 60pt;display:flex;flex-direction:column;justify-content:center;align-items:center;">
<div style="background:#E8573A;border-radius:6pt;padding:8pt;text-align:center;">
<p style="font-size:10pt;color:#FFFFFF;font-weight:bold;margin:0;">GAP</p>
</div>
</div>
<div style="flex:1;background:#1B2A4A;border-radius:6pt;padding:12pt;">
<h3 style="font-size:13pt;color:#FFFFFF;">Stream 2: LLM Refactoring</h3>
<ul style="font-size:10pt;color:#F4F6F9;">
<li>MANTRA: 82.8% success</li>
<li>Liu et al.: 86.7% recall</li>
<li>Piao et al.: 61 types tested</li>
<li>Horikawa: 15,451 instances</li>
</ul>
</div>
</div>
<div style="background:#27AE60;border-radius:6pt;padding:12pt;margin-top:12pt;">
<p style="font-size:13pt;color:#FFFFFF;margin:0;text-align:center;"><b>Thesis Contribution:</b> Tactic Detection → <b>LLM Tactic Implementation</b> → Quality Measurement</p>
</div>
<div style="display:flex;gap:12pt;margin-top:8pt;">
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:8pt;">
<p style="font-size:9pt;margin:0;">IPSynth: 85% success but uses SMT solver, not LLMs. ChatGPT: only 5%</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:8pt;">
<p style="font-size:9pt;margin:0;">MANTRA: 82.8% but method-level only. No architecture-level data exists.</p>
</div>
<div style="flex:1;background:#FFFFFF;border-radius:6pt;padding:8pt;">
<p style="font-size:9pt;margin:0;">71% of tactic studies don't describe identification method [Marquez, 2022]</p>
</div>
</div>
</div>`));

// ===== SLIDE 30: Research Gaps Table =====
slides.push(slide(`
<div style="margin:28pt 40pt;">
<h1>Seven Specific Research Gaps</h1>
<div style="margin-top:8pt;">
<div style="display:flex;background:#1B2A4A;border-radius:4pt 4pt 0 0;padding:6pt 10pt;">
<div style="flex:0 0 24pt;"><p style="font-size:10pt;color:#FFFFFF;margin:0;font-weight:bold;">#</p></div>
<div style="flex:2;"><p style="font-size:10pt;color:#FFFFFF;margin:0;font-weight:bold;">Gap</p></div>
<div style="flex:3;"><p style="font-size:10pt;color:#FFFFFF;margin:0;font-weight:bold;">Evidence</p></div>
</div>
<div style="display:flex;background:#FFFFFF;padding:5pt 10pt;border-bottom:1pt solid #D0D8E0;">
<div style="flex:0 0 24pt;"><p style="font-size:9pt;color:#E8573A;margin:0;font-weight:bold;">1</p></div>
<div style="flex:2;"><p style="font-size:9pt;margin:0;">70% lack tactic identification methods</p></div>
<div style="flex:3;"><p style="font-size:9pt;color:#8899AA;margin:0;">65 of 91 studies [Marquez, 2022]</p></div>
</div>
<div style="display:flex;background:#F4F6F9;padding:5pt 10pt;border-bottom:1pt solid #D0D8E0;">
<div style="flex:0 0 24pt;"><p style="font-size:9pt;color:#E8573A;margin:0;font-weight:bold;">2</p></div>
<div style="flex:2;"><p style="font-size:9pt;margin:0;">Design rationale doesn't trace to code</p></div>
<div style="flex:3;"><p style="font-size:9pt;color:#8899AA;margin:0;">Detected violations not remediated [Rosik, 2011]</p></div>
</div>
<div style="display:flex;background:#FFFFFF;padding:5pt 10pt;border-bottom:1pt solid #D0D8E0;">
<div style="flex:0 0 24pt;"><p style="font-size:9pt;color:#E8573A;margin:0;font-weight:bold;">3</p></div>
<div style="flex:2;"><p style="font-size:9pt;margin:0;">No cost-benefit quantification for tactics</p></div>
<div style="flex:3;"><p style="font-size:9pt;color:#8899AA;margin:0;">Qualitative mappings only [Bogner, 2019]</p></div>
</div>
<div style="display:flex;background:#F4F6F9;padding:5pt 10pt;border-bottom:1pt solid #D0D8E0;">
<div style="flex:0 0 24pt;"><p style="font-size:9pt;color:#E8573A;margin:0;font-weight:bold;">4</p></div>
<div style="flex:2;"><p style="font-size:9pt;margin:0;">LLM + static analysis integration is ad hoc</p></div>
<div style="flex:3;"><p style="font-size:9pt;color:#8899AA;margin:0;">No standardized framework exists</p></div>
</div>
<div style="display:flex;background:#FFFFFF;padding:5pt 10pt;border-bottom:1pt solid #D0D8E0;">
<div style="flex:0 0 24pt;"><p style="font-size:9pt;color:#E8573A;margin:0;font-weight:bold;">5</p></div>
<div style="flex:2;"><p style="font-size:9pt;margin:0;">No Python architectural tactic benchmarks</p></div>
<div style="flex:3;"><p style="font-size:9pt;color:#8899AA;margin:0;">All datasets Java-only</p></div>
</div>
<div style="display:flex;background:#F4F6F9;padding:5pt 10pt;border-bottom:1pt solid #D0D8E0;">
<div style="flex:0 0 24pt;"><p style="font-size:9pt;color:#E8573A;margin:0;font-weight:bold;">6</p></div>
<div style="flex:2;"><p style="font-size:9pt;margin:0;">Agents don't plan architecturally</p></div>
<div style="flex:3;"><p style="font-size:9pt;color:#8899AA;margin:0;">"Cleanup partners" not "architects" [Horikawa, 2025]</p></div>
</div>
<div style="display:flex;background:#FFFFFF;padding:5pt 10pt;border-radius:0 0 4pt 4pt;">
<div style="flex:0 0 24pt;"><p style="font-size:9pt;color:#E8573A;margin:0;font-weight:bold;">7</p></div>
<div style="flex:2;"><p style="font-size:9pt;margin:0;">No formal verification of LLM refactorings</p></div>
<div style="flex:3;"><p style="font-size:9pt;color:#8899AA;margin:0;">7.4% unsafe rate [Liu, 2025]; IPSynth SMT only</p></div>
</div>
</div>
</div>`));

// ===== SLIDE 31: Future Research Agenda =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>Future Research Agenda</h1>
<div style="display:flex;gap:14pt;margin-top:10pt;">
<div style="flex:1;background:#2E86AB;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;color:#FFFFFF;">1. LLM-Driven Tactic Implementation</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Architecture context injection, multi-file transformation, tactic-specific prompting, 15 modifiability tactics as starting catalog</p>
</div>
<div style="flex:1;background:#2E86AB;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;color:#FFFFFF;">2. Multi-Tool Validation Frameworks</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Radon + SonarQube + Pylint + architecture analysis with Cliff's Delta + Wilcoxon + Benjamini-Hochberg</p>
</div>
</div>
<div style="display:flex;gap:14pt;margin-top:10pt;">
<div style="flex:1;background:#1B2A4A;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;color:#FFFFFF;">3. Architecture-Aware Agent Pipelines</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Architect + Developer + Reviewer + Repair agents; proactive tactic selection based on system health</p>
</div>
<div style="flex:1;background:#1B2A4A;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;color:#FFFFFF;">4. Tactic-Specific Benchmarks</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">Labeled before/after systems, multi-language (especially Python), verification criteria included</p>
</div>
<div style="flex:1;background:#1B2A4A;border-radius:6pt;padding:12pt;">
<h3 style="font-size:12pt;color:#FFFFFF;">5. Formal Verification Integration</h3>
<p style="font-size:10pt;color:#F4F6F9;margin:0;">AST-based structural verification, refinement calculus, hybrid LLM + SMT approach</p>
</div>
</div>
<div style="background:#27AE60;border-radius:6pt;padding:14pt;margin-top:12pt;">
<p style="font-size:13pt;color:#FFFFFF;margin:0;text-align:center;">The field is at an <b>inflection point</b>. All components exist individually — tactic catalogs, LLM code generation, multi-agent pipelines, static analysis verification. What doesn't exist is a system that <b>combines them all</b>.</p>
</div>
</div>`));

// ===== SLIDE 32: Key Takeaways =====
slides.push(slide(`
<div style="margin:30pt 40pt;">
<h1>Key Takeaways</h1>
<div style="display:flex;gap:16pt;margin-top:10pt;">
<div style="flex:1;">
<div style="border-left:4pt solid #2E86AB;padding-left:10pt;margin-bottom:12pt;">
<h3 style="font-size:12pt;">Architecture determines maintainability</h3>
<p style="font-size:10pt;color:#8899AA;margin:0;">60-80% of costs are maintenance; load-bearing walls metaphor</p>
</div>
<div style="border-left:4pt solid #2E86AB;padding-left:10pt;margin-bottom:12pt;">
<h3 style="font-size:12pt;">Tactics are the building blocks</h3>
<p style="font-size:10pt;color:#8899AA;margin:0;">15 modifiability tactics in 3 categories; 63% of projects modify patterns with tactics</p>
</div>
<div style="border-left:4pt solid #E8573A;padding-left:10pt;margin-bottom:12pt;">
<h3 style="font-size:12pt;">Detection ≠ Remediation</h3>
<p style="font-size:10pt;color:#8899AA;margin:0;">0/9 violations fixed at IBM; 82.2% academic-only tools</p>
</div>
<div style="border-left:4pt solid #E8573A;padding-left:10pt;margin-bottom:12pt;">
<h3 style="font-size:12pt;">Never trust a single tool</h3>
<p style="font-size:10pt;color:#8899AA;margin:0;">&lt;0.4% inter-tool agreement; multi-tool validation essential</p>
</div>
</div>
<div style="flex:1;">
<div style="border-left:4pt solid #27AE60;padding-left:10pt;margin-bottom:12pt;">
<h3 style="font-size:12pt;">LLMs work with pipelines</h3>
<p style="font-size:10pt;color:#8899AA;margin:0;">82.8% (MANTRA) vs 8.7% (standalone); verification is the critical component</p>
</div>
<div style="border-left:4pt solid #27AE60;padding-left:10pt;margin-bottom:12pt;">
<h3 style="font-size:12pt;">Prompt specificity matters enormously</h3>
<p style="font-size:10pt;color:#8899AA;margin:0;">15.6% → 86.7% with subcategory prompts; rule-based outperforms descriptive</p>
</div>
<div style="border-left:4pt solid #E8573A;padding-left:10pt;margin-bottom:12pt;">
<h3 style="font-size:12pt;">The gap is architecture-level</h3>
<p style="font-size:10pt;color:#8899AA;margin:0;">96.3% of agentic refactorings touch 1 file; no LLM implements tactics</p>
</div>
<div style="border-left:4pt solid #27AE60;padding-left:10pt;margin-bottom:12pt;">
<h3 style="font-size:12pt;">The transformation gap can be bridged</h3>
<p style="font-size:10pt;color:#8899AA;margin:0;">All components exist individually — combining them is the research frontier</p>
</div>
</div>
</div>
</div>`));

// ===== SLIDE 33: Thank You =====
slides.push(`<!DOCTYPE html><html><head><style>
html{background:#1B2A4A;}
body{width:720pt;height:405pt;margin:0;padding:0;background:#1B2A4A;font-family:Arial,sans-serif;display:flex;flex-direction:column;justify-content:center;}
</style></head><body>
<div style="margin-left:60pt;margin-right:60pt;">
<h1 style="font-size:36pt;color:#FFFFFF;margin:0 0 16pt 0;">Thank You</h1>
<div style="width:60pt;height:3pt;background:#E8573A;margin-bottom:16pt;"></div>
<p style="font-size:14pt;color:#8899AA;margin:0 0 6pt 0;">Automated Implementation of Architectural Tactics</p>
<p style="font-size:14pt;color:#8899AA;margin:0 0 20pt 0;">for Software Quality Improvement</p>
<p style="font-size:12pt;color:#2E86AB;margin:0 0 4pt 0;">Innopolis University — MS Study Notes, 2026</p>
<p style="font-size:11pt;color:#8899AA;margin:0;">Based on 40+ papers across SA, maintainability, and LLM research</p>
</div>
</body></html>`);

// ===== WRITE HTML FILES AND CONVERT =====
async function main() {
  // Write all HTML files
  for (let i = 0; i < slides.length; i++) {
    const num = String(i + 1).padStart(3, '0');
    fs.writeFileSync(path.join(SLIDES_DIR, `slide-${num}.html`), slides[i]);
  }
  console.log(`Wrote ${slides.length} HTML slide files`);

  // Create PPTX
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Innopolis University';
  pptx.title = 'Automated Implementation of Architectural Tactics for Software Quality Improvement';
  pptx.subject = 'Comprehensive Study Guide';

  for (let i = 0; i < slides.length; i++) {
    const num = String(i + 1).padStart(3, '0');
    const htmlFile = path.join(SLIDES_DIR, `slide-${num}.html`);
    console.log(`Processing slide ${i + 1}/${slides.length}...`);
    await html2pptx(htmlFile, pptx);
  }

  await pptx.writeFile({ fileName: OUT });
  console.log(`Presentation saved to ${OUT}`);
}

main().catch(err => { console.error(err); process.exit(1); });
