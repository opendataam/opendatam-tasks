import re
import os
import subprocess
import json
import tempfile

SOURCES_FILE = 'docs/armenian_data_sources.md'
TEMPLATE_FILE = 'docs/issue_template.md'

def get_existing_issues():
    """Fetches open issues as a dictionary {title: number} to support updates."""
    try:
        # Fetching number and title
        result = subprocess.run(['gh', 'issue', 'list', '--limit', '500', '--state', 'open', '--json', 'number,title'], capture_output=True, text=True, check=True)
        issues = json.loads(result.stdout)
        # return dict mapping title -> number
        return {issue['title']: issue['number'] for issue in issues}
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        print("Warning: Could not fetch existing issues. Duplicate checking disabled.")
        return {}

def parse_markdown_sources(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    sources = []
    current_source = {}
    collecting_text = False
    
    header_re = re.compile(r'^(#{2,3}) (\d+(\.\d+)?)\.?\s+(.+)$')
    meta_re = re.compile(r'^\*\*(Website|Type|Location):\*\* (.+)$')

    for line in lines:
        line = line.strip()
        header_match = header_re.match(line)
        
        if header_match:
            if current_source and current_source.get('title'):
                sources.append(current_source)
            
            level = len(header_match.group(1))
            number = header_match.group(2)
            title = header_match.group(4).strip()
            
            current_source = {
                'title': title,
                'number': number,
                'url': 'N/A',
                'type': 'Unknown',
                'description': [],
                'level': level
            }
            collecting_text = True
            continue

        if collecting_text and current_source:
            meta_match = meta_re.match(line)
            if meta_match:
                key = meta_match.group(1).lower()
                value = meta_match.group(2).strip()
                current_source[key] = value
                continue
            
            if line and not line.startswith('---') and not line.startswith('|'):
                current_source['description'].append(line)

    if current_source and current_source.get('title'):
        sources.append(current_source)

    return sources

def load_template(filename):
    with open(filename, 'r') as f:
        return f.read()

def generate_issue_body(source, template_content):
    match = re.search(r'```markdown\n(.*?)\n```', template_content, re.DOTALL)
    body_template = match.group(1) if match else template_content

    title = source['title']
    url = source.get('website', source.get('url', 'Search for URL'))
    source_type = source.get('type', 'Unknown')
    
    full_desc = "\n".join(source['description'])
    goal = f"Scrape metadata and data from {title} ({source_type})."
    
    context = full_desc[:2000]
    if len(full_desc) > 2000:
        context += "\n... (see data sources file for more)"

    body = body_template.replace('[One sentence summary of the objective, e.g., "Scrape metadata for all manuscripts from the Bodleian Library collection."]', goal)
    body = body.replace('[Source Name]', title)
    body = body.replace('[Source URL]', url)
    body = body.replace('[Source Type, e.g., Library, Archive]', source_type)
    body = body.replace('[target collection/website]', f"{title} website")
    body = body.replace('[Insert detailed description of the source, its collections, and its significance here. Extracted from the data sources file.]', context)
    body = body.replace('[Link to Source]', url)
    
    specific_fields = ""
    if "manuscript" in title.lower() or "library" in source_type.lower():
         specific_fields = "- Manuscript ID / Shelfmark\n    - Material (Parchment/Paper)\n    - Dimensions"
    elif "museum" in source_type.lower() or "gallery" in title.lower():
         specific_fields = "- Dimensions\n    - Medium/Technique\n    - Provenance"
    
    body = body.replace('[Add key specific fields based on source description]', specific_fields)
    body = body.replace('[Link to specific collection if applicable]', '')
    
    return body

def main():
    sources = parse_markdown_sources(SOURCES_FILE)
    existing_issues_map = get_existing_issues()
    template_content = load_template(TEMPLATE_FILE)
    
    valid_sources = []
    for s in sources:
        if s['url'] != 'N/A' or (s['type'] != 'Unknown' and len(s['description']) > 0):
             valid_sources.append(s)
    
    processed_count = 0
    MAX_ISSUES = 50

    for source in valid_sources:
        if processed_count >= MAX_ISSUES:
            break
            
        # Specific skip for "Subsections" that act as headers
        if "International Collections" in source['title'] or "Aggregators" in source['title']:
             continue

        title = f"[EN] Extract data from {source['title']}"
        body = generate_issue_body(source, template_content)
        
        # Check if exists
        # We need to find if the title matches any key in existing_issues_map
        # The titles constructed here are "[EN] Extract data from ..."
        # The headers in MD are just "Source Name".
        # So we construct the expected issue title `title` and check if it is in `existing_issues_map`.
        
        target_issue_number = None
        # Try exact match first
        if title in existing_issues_map:
            target_issue_number = existing_issues_map[title]
        else:
             # Fallback check? Maybe the user renamed it slightly?
             # For now, let's stick to strict title matching for safety, 
             # OR check if the source name is a substring of an existing title to be robust.
             for existing_title, num in existing_issues_map.items():
                 if source['title'] in existing_title:
                     target_issue_number = num
                     break
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            tmp.write(body)
            tmp_path = tmp.name
            
        try:
            if target_issue_number:
                print(f"Updating issue #{target_issue_number}: {title}")
                subprocess.run([
                    'gh', 'issue', 'edit', str(target_issue_number),
                    '--body-file', tmp_path
                    # We usually don't want to overwrite title or labels on edit unless asked, keeping it safe.
                ], check=True)
            else:
                print(f"Creating new issue: {title}")
                subprocess.run([
                    'gh', 'issue', 'create',
                    '--title', title,
                    '--body-file', tmp_path,
                    '--label', 'extraction,topic-culture'
                ], check=True)
            
            processed_count += 1
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to process issue {title}: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

if __name__ == '__main__':
    main()
