#!/usr/bin/env python3
"""Fix all templates: logo size, PDF button, color naming, consistency."""
import re, os

DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = [
    'audit-report-template.html',
    'stage1-audit-report-template.html',
    'stage2-audit-plan-template.html',
    'stage2-audit-findings-list-template.html',
]

PDF_BUTTON_HTML = '''
<!-- PDF Download Button -->
<button class="pdf-download-btn" onclick="downloadPDF()">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zM6 20V4h7v5h5v11H6zm5-6v-3h2v3h3l-4 4-4-4h3z"/></svg>
  PDF Download
</button>

<script>
function downloadPDF() {
  var btn = document.querySelector('.pdf-download-btn');
  btn.style.display = 'none';
  window.print();
  setTimeout(function() { btn.style.display = 'flex'; }, 500);
}
</script>
'''

for fname in TEMPLATES:
    path = os.path.join(DIR, fname)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix logo size in audit-report-template (missing height rule)
    if fname == 'audit-report-template.html':
        if '.page-header .logo-area img' not in html:
            html = html.replace(
                '.page-header .logo-area {',
                '.page-header .logo-area img { height: 40px; width: auto; }\n    .page-header .logo-area {'
            )

    # 2. Fix "Primary Blue" -> "Primary Dark Blue" in sidebar text
    html = html.replace(
        '– Primary Blue (Header',
        '– Primary Dark Blue (Header'
    )
    html = html.replace(
        'auf Primary Blue',
        'auf Primary Dark Blue'
    )
    html = html.replace(
        'Primary Blue, Unterstrich',
        'Primary Dark Blue, Unterstrich'
    )
    html = html.replace(
        'Primary Blue:    #0B253B',
        'Primary Dark Blue: #0B253B'
    )

    # 3. Add PDF button HTML + script if not present
    if '<button class="pdf-download-btn"' not in html:
        html = html.replace('</body>', PDF_BUTTON_HTML + '</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed {fname}")

print("All templates fixed!")
