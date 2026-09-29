"""One-time, source-preserving import of Anna's three selected COMP 536 decks.
Generated drafts are subsequently edited directly; do not rerun over reviewed edits.
"""
from pathlib import Path
import re,json,shutil,hashlib,html
ROOT=Path(__file__).resolve().parent
COURSE=Path('/Users/anna/Teaching/comp536-sp26')
DECKS={'software-engineering':'software-engineering/slides/software-engineering-for-scientists.qmd','ode-methods':'numerical-methods/slides/ode-methods.qmd','statistical-thinking':'statistical-thinking/slides/statistical-thinking-foundations.qmd'}
TITLES={'software-engineering':'Software Engineering for Scientists','ode-methods':'ODE Methods: The Beautiful Failure','statistical-thinking':'Statistical Thinking Foundations'}
records=[]
for name,rel in DECKS.items():
 source=COURSE/'lectures'/rel;original=source.read_text();body=original.split('---',2)[2].strip();assets=[];nbcells=[];mappings=[]
 (ROOT/'originals').mkdir(exist_ok=True);shutil.copyfile(source,ROOT/'originals'/f'{name}.qmd')
 def codeblock(m):
  lang,code=m.groups()
  if lang=='{mermaid}':
   (ROOT/'originals'/'professional-loop.mmd').write_text(code)
   return '\n**Spec → Contract → Validate (scientific evidence) → Test (behavioral evidence) → Plot (diagnostic evidence) → Iterate → Spec.**\n'
  if lang!='{python}':return m.group(0)
  opts=dict(re.findall(r'^#\| ([\w-]+):\s*(.*)$',code,re.M));code=re.sub(r'^#\|.*\n','',code,flags=re.M).strip()
  if opts.get('eval')=='false':return '```python\n'+code+'\n```'
  idx=len(nbcells)+1;label=f'{name}-cell-{idx}'
  nbcells.append({'cell_type':'code','id':label,'metadata':{'tags':[label]},'source':(f'#| label: {label}\n'+code+'\n').splitlines(True),'execution_count':None,'outputs':[]})
  if opts.get('include')=='false':return ''
  return f'<!-- executed:{label} echo:{opts.get("echo","true")} -->'
 body=re.sub(r'```([^\n]*)\n(.*?)\n```',codeblock,body,flags=re.S)
 # A Quarto horizontal rule separates source slides. Preserve their order and notes.
 sections=re.split(r'^---\s*$',body,flags=re.M)
 output=[]
 for n,section in enumerate(sections,1):
  if not section.strip():continue
  heading=re.search(r'^#{1,2}\s+(.*)$',section,re.M)
  if not heading:continue
  title=re.sub(r'\s*\{[^}]*\}\s*$','',heading.group(1)).strip()
  if not title:
   title=re.search(r'\{\.r-fit-text\}\s*\n([^\n]+)',section).group(1).strip('* ')
  mappings.append({'sourceSlide':n,'title':title,'sourceLine':original[:original.find(heading.group(0))].count('\n')+1})
  section=section[:heading.start()]+'## '+title+section[heading.end():]
  def image(m):
   alt,src=m.group(1),m.group(2);p=(source.parent/src).resolve();dest=ROOT/'assets'/p.name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(p,dest);assets.append({'source':str(p),'copy':'assets/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
   alt=alt or title+' — original COMP 536 teaching figure'
   return f'![{alt}](assets/{p.name})'
  section=re.sub(r'!\[([^\]]*)\]\(([^)]+)\)(?:\{[^\n]*\})?',image,section)
  section=re.sub(r'\{\{< video (\S+).*?>\}\}',r'[Watch the original lecture video](\1)\n\n*External video; internet connection required.*',section)
  def link(m):
   label,src=m.groups();p=(source.parent/src).resolve();return f'[{label}](https://astrobytes-edu.github.io/comp536-sp26/{p.relative_to(COURSE).with_suffix(".html")})'
  section=re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+\.qmd)\)',link,section)
  chunks=re.split(r'(```[^\n]*\n.*?\n```)',section,flags=re.S);result=[];stack=[]
  for chunk in chunks:
   if chunk.startswith('```'):result.append(chunk);continue
   lines=[]
   for line in chunk.splitlines():
    m=re.match(r'^:{3,}\s*(.*)$',line)
    if m:
     attrs=m.group(1)
     if not attrs:
      if stack:lines.append(stack.pop())
      continue
     fence=':'*(24-len(stack));stack.append(fence)
     if '.notes' in attrs:directive='speaker-note'
     elif re.search(r'\.columns\b',attrs):directive='slide-columns'
     elif re.search(r'\.column\b',attrs):directive='slide-column'
     elif '.incremental' in attrs:directive='slide-incremental'
     elif '.fragment' in attrs:directive='fragment'
     elif '.callout-' in attrs:directive='note'
     else:directive='div'
     line=fence+'{'+directive+'}'
     titlematch=re.search(r'title="([^"]+)"',attrs)
     if titlematch:line+='\n\n**'+titlematch.group(1)+'**\n'
    if line.strip()=='. . .':line='<!-- Source pause: retained as a teaching beat. -->'
    lines.append(line)
   result.append('\n'.join(lines))
  section='\n'.join(result)
  # Executable source is kept in the notebook; both source and results are visible.
  def embed(m):
   label,echo=m.groups();return f'\n```{{slide-code-example}} {name}-computations.ipynb#{label}\n:view: {"output" if echo=="false" else "both"}\n:alt: Executed output for {title.replace(chr(34),chr(39))}.\n```\n'
  section=re.sub(r'<!-- executed:(\S+) echo:(\S+) -->',embed,section)
  section=section.replace('\\underbrace','\\underbrace')
  output.append(section.strip())
 subtitle='COMP 521 adaptation · editorial draft' if name=='software-engineering' else 'Review copy · COMP 536 content · edits pending approval'
 (ROOT/f'{name}.md').write_text(f'---\ntitle: "{TITLES[name]}"\nsubtitle: "{subtitle}"\nauthor: Anna Rosen\n---\n\n'+'\n\n'.join(output)+'\n')
 if nbcells:
  for c in nbcells:c['metadata']['label']=c['id']
  nb={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'name':'python3','display_name':'Python 3','language':'python'}},'cells':[{'cell_type':'markdown','id':'intro','metadata':{},'source':[f'# {TITLES[name]}: original computations\n']},*nbcells]}
  (ROOT/f'{name}-computations.ipynb').write_text(json.dumps(nb,indent=1)+'\n')
 records.append({'deck':name,'source':str(source),'sha256':hashlib.sha256(original.encode()).hexdigest(),'slides':mappings,'codeCells':len(nbcells),'assets':assets})
(ROOT/'migration-record.json').write_text(json.dumps(records,indent=2)+'\n')
(ROOT/'myst.yml').write_text('version: 1\nproject:\n  title: COMP 536 lecture migration drafts\n  plugins:\n    - ../../plugin.mjs\n  toc:\n'+''.join('    - file: '+n+'.md\n'+('    - file: '+n+'-computations.ipynb\n' if n!='software-engineering' else '') for n in DECKS)+'  numbering:\n    heading_2: false\nsite:\n  template: book-theme\n')
(ROOT/'slides.json').write_text(json.dumps({'fit':'bounded','minFont':28,'css':['migration.css'],'decks':[{'name':n,'source':n+'.md','preset':'lecture','theme':'light'} for n in DECKS],'sources':[n+'-computations.ipynb' for n in DECKS if n!='software-engineering']},indent=2)+'\n')
(ROOT/'migration.css').write_text('.reveal .slides section { font-size:30px; }\n.reveal .slides h2 { font-size:1.35em; }\n.reveal .cell-outputs img { max-height:360px; }\n')
print([(r['deck'],len(r['slides']),r['codeCells']) for r in records])
