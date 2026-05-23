#!/usr/bin/env python3
"""
Convert MPM Deal Memo from Markdown to professional PDF.
"""
import markdown
from weasyprint import HTML
from pathlib import Path
import re

memo_path = Path("/home/ubuntu/.hermes/profiles/aurelius/home/mimo-build/gpt-researcher/deal_advisor_workspace/mpm_db/mandala_prima_makmur_deal_memo.md")
md_content = memo_path.read_text()

# Custom CSS for professional investment memo styling
css = """
@page {
  size: A4;
  margin: 2cm 2.2cm;
  @top-center {
    content: "DEAL ADVISOR INTELLIGENCE ENGINE — CONFIDENTIAL";
    font-family: 'Helvetica', 'Arial', sans-serif;
    font-size: 7pt;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  @bottom-center {
    content: "Page " counter(page) " of " counter(pages);
    font-family: 'Helvetica', 'Arial', sans-serif;
    font-size: 7pt;
    color: #888;
  }
  @bottom-left {
    content: "PT Mandala Prima Makmur — Deal Memo";
    font-family: 'Helvetica', 'Arial', sans-serif;
    font-size: 7pt;
    color: #888;
  }
}

@page :first {
  @top-center {
    content: none;
  }
}

body {
  font-family: 'Helvetica', 'Arial', sans-serif;
  font-size: 9.5pt;
  line-height: 1.55;
  color: #1a1a1a;
}

/* ── Cover-style header ── */
h1 {
  font-size: 22pt;
  font-weight: 800;
  color: #111;
  border-bottom: 3px solid #1a56db;
  padding-bottom: 14px;
  margin-bottom: 10px;
  line-height: 1.2;
}

h2 {
  font-size: 13pt;
  font-weight: 700;
  color: #1a56db;
  margin-top: 28px;
  margin-bottom: 10px;
  padding-bottom: 4px;
  border-bottom: 1px solid #e0e0e0;
  page-break-after: avoid;
}

h3 {
  font-size: 11pt;
  font-weight: 700;
  color: #2d3748;
  margin-top: 18px;
  margin-bottom: 6px;
  page-break-after: avoid;
}

p {
  margin: 6px 0;
  text-align: justify;
}

/* ── Meta line ── */
h1 + p, h1 + p + p, h1 + p + p + p {
  font-size: 8pt;
  color: #666;
  margin: 2px 0;
}

/* ── Scorecard table ── */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 14px 0;
  font-size: 8.5pt;
  page-break-inside: avoid;
}

th {
  background: #1a56db;
  color: white;
  font-weight: 700;
  padding: 7px 8px;
  text-align: left;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

td {
  padding: 6px 8px;
  border-bottom: 1px solid #e8e8e8;
  vertical-align: top;
}

tr:nth-child(even) td {
  background: #f8fafd;
}

/* ── Recommendation badge ── */
strong:has(+ :not(:empty)) {
  /* bold text already handled by strong tag */
}

/* ── Lists ── */
ul, ol {
  margin: 6px 0;
  padding-left: 22px;
}

li {
  margin: 3px 0;
}

/* ── Risk badges ── */
p:has(> strong:first-child) {
  /* Key statements */
}

/* ── Code / inline ── */
code {
  background: #f1f5f9;
  padding: 2px 5px;
  border-radius: 3px;
  font-size: 8.5pt;
  font-family: 'Menlo', 'Consolas', monospace;
}

pre {
  background: #f8fafd;
  padding: 10px;
  border-left: 3px solid #1a56db;
  font-size: 8pt;
  overflow-x: auto;
}

/* ── Horizontal rule ── */
hr {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 20px 0;
}

/* ── Blockquote for callouts ── */
blockquote {
  border-left: 3px solid #1a56db;
  margin: 12px 0;
  padding: 6px 14px;
  background: #f8fafd;
  font-style: italic;
  color: #555;
}

/* ── Footer / sources ── */
h2:last-of-type + ul, h2:nth-last-of-type(2) + ul {
  font-size: 8pt;
  color: #666;
}

/* ── Page breaks before major sections ── */
h2:nth-of-type(4), h2:nth-of-type(8), h2:nth-of-type(11) {
  page-break-before: always;
}

/* ── Keep headings with content ── */
h2, h3 {
  page-break-after: avoid;
}

/* ── Links ── */
a {
  color: #1a56db;
  text-decoration: none;
}

/* ── Watermark-style confidentiality ── */
body::after {
  content: "";
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-30deg);
  font-size: 72pt;
  color: rgba(26, 86, 219, 0.03);
  font-weight: 900;
  white-space: nowrap;
  pointer-events: none;
  z-index: -1;
}
"""

# Convert MD to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'nl2br', 'sane_lists']
html_body = markdown.markdown(md_content, extensions=md_extensions)

# Full HTML document
html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Deal Memo: PT Mandala Prima Makmur</title>
<style>{css}</style>
</head>
<body>
<div id="watermark">CONFIDENTIAL</div>
{html_body}
</body>
</html>"""

# Write HTML for reference
html_path = memo_path.with_suffix(".html")
html_path.write_text(html_doc)

# Generate PDF
pdf_path = memo_path.with_suffix(".pdf")
HTML(string=html_doc).write_pdf(str(pdf_path))

print(f"PDF generated: {pdf_path}")
print(f"Size: {pdf_path.stat().st_size / 1024:.1f} KB")
print(f"HTML preview: {html_path}")
