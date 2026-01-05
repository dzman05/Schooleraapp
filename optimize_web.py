import re
import os

file_path = r'd:\school-management\web_landing\index.html'
robots_path = r'd:\school-management\web_landing\robots.txt'

def minify_css(css_content):
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Remove whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    css_content = re.sub(r'\s*([{:;,}])\s*', r'\1', css_content)
    css_content = css_content.replace(';}', '}')
    return css_content.strip()

def optimize_html():
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Minify the large style block
    # Look for the block after "Styles (Inlined for 100/100 Performance)"
    # We use a pattern that captures the style tag content
    style_pattern = r'(<!-- Styles \(Inlined for 100/100 Performance\) -->\s*<style>)(.*?)(</style>)'
    
    match = re.search(style_pattern, content, re.DOTALL)
    if match:
        prefix, css, suffix = match.groups()
        minified_css = minify_css(css)
        print(f"Original CSS length: {len(css)}, Minified: {len(minified_css)}")
        content = content.replace(match.group(0), f'{prefix}{minified_css}{suffix}')
    else:
        print("Warning: CSS Block not found via regex.")

    # 2. Fix Footer Logo Dimensions
    # Original: <img src="assets/img/Logo.webp" alt="Logo" style="height: 45px; margin-bottom: 10px;">
    # Logic: Finding the tag by its src and style or context
    footer_logo_pattern = r'(<img src="assets/img/Logo\.webp" alt="Logo" style="height: 45px; margin-bottom: 10px;")'
    
    if re.search(footer_logo_pattern, content):
        content = re.sub(footer_logo_pattern, r'\1 width="45" height="45"', content)
        print("Fixed Footer Logo dimensions.")
    else:
        print("Warning: Footer logo not found directly.")

    # 3. Add Aria-Labels to Social Links
    # We look for the social-links div and then the anchors inside
    # Since regex for nested tags is hard, we'll target the specific hrefs known in the footer
    
    social_map = {
        'facebook.com': 'Facebook',
        'instagram.com': 'Instagram',
        'linkedin.com': 'LinkedIn',
        'wa.me': 'WhatsApp'
    }

    # Pattern: <a href="...facebook..." ... target="_blank" ... >
    # We want to insert aria-label before the closing >
    
    # We iterate over the file content lines or use precise replace
    
    for domain, label in social_map.items():
        # Find anchors containing this domain in href
        # This regex looks for <a ... href="...domain..." ... > where aria-label is NOT present
        pattern = f'(<a [^>]*href="[^"]*{domain}[^"]*"[^>]*)(?!aria-label)([^>]*>)'
        
        # We need to loop because there might be multiple (though unlikely for footer here)
        # But wait, there is a floating whatsapp button which HAS aria-label.
        # The footer one is: <a href="https://wa.me/213660639890" target="_blank" style="...">
        
        def replacement(m):
            # Check if aria-label already exists in the match (the negative lookahead in regex might miss if it's after the group 2)
            full_tag = m.group(0)
            if 'aria-label' in full_tag:
                return full_tag
            
            # Insert aria-label
            return f'{m.group(1)} aria-label="{label}" {m.group(2)}'

        content = re.sub(pattern, replacement, content)
    
    print("Added aria-labels to social links.")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_robots_txt():
    robots_content = """User-agent: *
Allow: /
Sitemap: https://schoolera.site/sitemap.xml
"""
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print("Created robots.txt")

if __name__ == '__main__':
    optimize_html()
    create_robots_txt()
