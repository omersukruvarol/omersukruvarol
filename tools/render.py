"""Run python3 tools/render.py to rebuild the profile. No font, service or package required."""
from html import escape
from pathlib import Path
from pixels import length, lettering

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'terminal'
ASSETS.mkdir(parents=True, exist_ok=True)
INK, PANEL, LINE = '#171b35', '#202643', '#404867'
PAPER, LAV, LAV_SHADE = '#fff1d2', '#a9b6ff', '#8998e2'
MINT, BUTTER, ROSE = '#95f2cd', '#ffda82', '#ffaaa7'

COPY = {
    'tr': {
        'terminal':'KİŞİSEL TERMİNAL', 'city':'İSTANBUL', 'projects':'PROJELER',
        'bio':'Mekatronik kökenli bir Ar-Ge mühendisiyim. Endüstriyel görüntü işleme, yapay zekâ ajanları ve web/mobil uygulamalar geliştiriyorum.',
        'work':[
            ('Landed', 'TypeScript / Git', 'Ajanların yazdığı kod Git’e girdi mi? Landed, Claude Code ve Codex oturumlarını yerel commit’lerle eşleştiriyor.'),
            ('Linkletics', 'Go / TypeScript', 'Sporcular için bir sosyal ağ. Web ve mobilin ortak API’lerini yazıyor, PHP altyapısını Go servislerine taşıyorum.'),
            ('PID Tuning Visualizer', 'Python / Matplotlib', 'Üç katsayıyı değiştir, sistemin tepkisini grafikte izle. Kontrol ayarlarını denemek için yazdığım bir simülatör.'),
        ],
        'links': [('Portfolyo','https://omersukruvarol.com/'), ('LinkedIn','https://www.linkedin.com/in/omersukruvarol/'), ('English','./README.en.md')],
    },
    'en': {
        'terminal':'PERSONAL TERMINAL', 'city':'ISTANBUL', 'projects':'PROJECTS',
        'bio':'I’m an R&D engineer with a background in mechatronics. I build industrial vision systems, AI agents, and apps for web and mobile.',
        'work':[
            ('Landed', 'TypeScript / Git', 'What did Claude Code and Codex write, and what made it into a commit? Landed checks their edits against your local Git history.'),
            ('Linkletics', 'Go / TypeScript', 'A social network for athletes. I build the APIs its web and mobile apps share and move the PHP backend to Go services.'),
            ('PID Tuning Visualizer', 'Python / Matplotlib', 'Drag three sliders and watch the system respond. I built this simulator to experiment with controller gains.'),
        ],
        'links':[('Portfolio','https://omersukruvarol.com/'), ('LinkedIn','https://www.linkedin.com/in/omersukruvarol/'), ('Türkçe','./README.md')],
    },
}
PROJECT_URLS = [
    'https://github.com/omersukruvarol/landed-agents', 'https://omersukruvarol.com/#work',
    'https://github.com/omersukruvarol/PID-Tuning-Visualizer',
]
SLUGS = ['landed', 'linkletics', 'pid']
ACCENT = [MINT, BUTTER, ROSE]

class Screen:
    def __init__(self, width):
        self.width, self.parts = width, []

    def rect(self, x, y, w, h, color):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')

    def path(self, d, color, transform=''):
        self.parts.append(f'<path fill="{color}" transform="{transform}" d="{d}"/>')

    def label(self, text, x, y, unit, color, heavy=False):
        text = text.replace('’', "'")
        if x + length(text, unit) > self.width + 1:
            raise ValueError(f'Line overflows {self.width}: {text}')
        self.path(lettering(text, heavy=heavy), color, f'translate({x} {y}) scale({unit})')

    def paragraph(self, text, x, y, unit, max_width, line_height, color):
        line = ''
        for word in text.replace('’', "'").split():
            candidate = (line + ' ' + word).strip()
            if line and length(candidate, unit) > max_width:
                self.label(line, x, y, unit, color)
                y += line_height
                line = word
            else:
                line = candidate
        self.label(line, x, y, unit, color)
        return y + 9 * unit

    def save(self, name, height, title):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{height}" '
               f'viewBox="0 0 {self.width} {height}" role="img" aria-label="{escape(title, quote=True)}">'
               f'<title>{escape(title)}</title>' + ''.join(self.parts) + '</svg>\n')
        (ASSETS / (name + '.svg')).write_text(svg)

# Four-colour CRT character. Its display, controls, feet and antenna share one pixel grid.
BOT = [
    '           mm            ',
    '           mm            ',
    '           nn            ',
    '           nn            ',
    '     nnnnnnnnnnnnn       ',
    '   nnwwwwwwwwwwwwwnn     ',
    '   nwwwwwwwwwwwwwwwn     ',
    '   nwwnnnnnnnnnnnwwn     ',
    '   nwwndddddddddnwwn     ',
    '   nwwndmmdddmmdnwwn    ',
    '   nwwndmmdddmmdnwwn    ',
    '   nwwndddddddddnwwn     ',
    '   nwwndddmmmiddnwwn    ',
    '   nwwndddddddddnwwn     ',
    '   nwwnnnnnnnnnnnwwn     ',
    '   nwwwwwwwwwwwwwwwn     ',
    '   nwwnnnnwwwrwnnwwn     ',
    '   nwwwwwwwwwwwwwwwno    ',
    '    nooooooooooooonno    ',
    '     nnnnnnnnnnnnnno     ',
    '        ndn  ndn         ',
    '        nwn  nwn         ',
    '      nnwwn  nwwnn       ',
    '      nnnnn  nnnnn       ',
]
BOT_PALETTE = {'n':INK,'o':'#9c6c58','w':BUTTER,'d':'#304966','m':MINT,'r':ROSE,'i':'#74c8ae'}

def sprite(screen, rows, colors, x, y, zoom):
    screen.parts.append('<g shape-rendering="crispEdges">')
    for row_id, row in enumerate(rows):
        for col, pixel in enumerate(row):
            if pixel in colors:
                screen.rect(x+col*zoom, y+row_id*zoom, zoom, zoom, colors[pixel])
    screen.parts.append('</g>')

ICONS = [
    ['    xx       ', '   x  x      ', '    xx       ', '    xx    xx ', '    xx   x  x',
     '    xx    xx ', '    xx   xx  ', '    xx  xx   ', '    xxxxx    ', '    xx       ',
     '   x  x      ', '    xx       '],
    ['       xxxx  ', '      xx  xx ', '      x    x ', '     xx   xx ', '      x  xx  ',
     '   xxx xxx   ', '  xx  x      ', ' xx   xx     ', ' x    x      ', ' xx  xx      ', '  xxxx       '],
    [' x           ', ' x     xxx   ', ' x    xx xx  ', ' x    x   xxx', ' x   xx      ',
     ' x   x       ', ' x  xx       ', ' xxxx        ', ' x           ', ' xxxxxxxxxxxx'],
]

def arrow(screen, x, y, u, color):
    screen.path('M1 0h6v6H5V3H4v1H3v1H2v1H1v1H0V5h1V4h1V3h1V2h1V1H1z',color,
                f'translate({x} {y}) scale({u})')

def hero(lang, compact):
    c = COPY[lang]
    w = 304 if compact else 640
    s = Screen(w)
    # Insert the lavender base after measuring the paragraph.
    s.rect(0,0,w,26,INK)
    s.rect(11,9,7,7,MINT)
    s.label(c['terminal'],24,8,1.25,PAPER)
    city_width = length(c['city'],1.25)
    s.label(c['city'],w-city_width-12,8,1.25,LAV)
    x = 15 if compact else 26
    unit = 3.1 if compact else 6
    first, second = (48,81) if compact else (58,121)
    for line, y in [('ÖMER ŞÜKRÜ',first), ('VAROL',second)]:
        s.label(line,x+unit*.48,y+unit*.54,unit,LAV_SHADE,True)
        s.label(line,x,y,unit,INK,True)
    field_x, field_y, field_w, field_h = (196,37,97,72) if compact else (390,40,222,122)
    for gy in range(field_y+2,field_y+field_h,8):
        for gx in range(field_x,field_x+field_w,8):
            s.rect(gx,gy,1.25,1.25,'#7686ca')
    zoom = 2.65 if compact else 5.0
    bx = field_x+(field_w-24*zoom)/2
    by = field_y+(field_h-24*zoom)/2
    s.rect(bx+4*zoom,by+24*zoom,16*zoom,zoom,'#7e89c9')
    sprite(s,BOT,BOT_PALETTE,bx,by,zoom)
    by_text = 123 if compact else 185
    last = s.paragraph(c['bio'],x,by_text,1.62 if compact else 1.88,
                       w-2*x,19 if compact else 22,INK)
    divider = round(last + (15 if compact else 20))
    s.rect(0,divider,w,24,INK)
    s.label(c['projects'],x,divider+8,1.26,MINT)
    start = round(x+length(c['projects'],1.26)+9)
    s.rect(start,divider+12,w-start-x,1,LINE)
    s.parts.insert(0,f'<rect width="{w}" height="{divider}" fill="{LAV}"/>')
    return s, divider+24

def card(lang, index, compact):
    w = 304 if compact else 640
    s = Screen(w)
    title, tech, summary = COPY[lang]['work'][index]
    accent = ACCENT[index]
    p = 11 if compact else 14
    icon_size = 32 if compact else 56
    ix, iy = p, (13 if compact else 14)
    s.rect(ix,iy,icon_size,icon_size,accent)
    zoom = 2 if compact else 3
    sprite(s,ICONS[index],{'x':INK},ix+(icon_size-13*zoom)//2,iy+(icon_size-len(ICONS[index])*zoom)//2,zoom)
    x = ix+icon_size+(10 if compact else 18)
    s.label(tech,x,13 if compact else 17,1.13 if compact else 1.5,accent)
    title_y = 32 if compact else 39
    title_unit = 1.88 if compact and index==2 else (2.28 if compact else 3.25)
    s.label(title,x,title_y,title_unit,PAPER,True)
    ax = w-(27 if compact else 42)
    arrow(s,ax,14 if compact else 22,1.6 if compact else 2.4,accent)
    body_x = p if compact else x
    body_y = 58 if compact else 76
    last = s.paragraph(summary,body_x,body_y,1.52 if compact else 1.68,w-body_x-p-4,
                       17 if compact else 19,'#e1e4f6')
    height = round(last + (12 if compact else 16))
    # A cartridge lip and a corner notch make each independent link read as a control.
    shape = f'M0 0h{w-7}v3h4v4h3v{height-7}H0z'
    s.parts.insert(0,f'<path d="{shape}" fill="{PANEL}"/>')
    s.rect(0,height-2,w,2,LINE)
    return s, height

def button(label, kind, name):
    u = 1.52
    w = round(length(label,u)+32)
    s = Screen(w)
    s.rect(0,0,w,32,INK)
    s.rect(1,1,w-2,30,MINT if kind==2 else LAV)
    s.label(label,9,10,u,INK)
    if kind==2:
        s.path('M0 0h2v1h2v1h2v1H4v1H2v1H0z',INK,f'translate({w-17} 12) scale(1.5)')
    else:
        arrow(s,w-18,11,1.35,INK)
    s.save(name,32,label)
    return w

def responsive(slug, alt, url=None):
    base = './assets/terminal/' + slug
    label = escape(alt,quote=True)
    pic = (f'<picture><source media="(max-width: 767px)" srcset="{base}-mobile.svg">'
           f'<img src="{base}.svg" width="100%" alt="{label}"></picture>')
    return f'<a href="{url}">{pic}</a>' if url else pic

def render(lang):
    c = COPY[lang]
    alt = 'Ömer Şükrü Varol · '+c['city']+'. '+c['bio']
    sections = []
    for compact in (False,True):
        suffix = '-mobile' if compact else ''
        s,h = hero(lang,compact)
        s.save(f'{lang}-hero{suffix}',h,alt)
        for i, (name,tech,summary) in enumerate(c['work']):
            s,h=card(lang,i,compact)
            s.save(f'{lang}-{SLUGS[i]}{suffix}',h,name+'. '+summary)
    sections.append(responsive(lang+'-hero',alt+' '+c['projects']))
    for i,(title,tech,summary) in enumerate(c['work']):
        sections.append(responsive(lang+'-'+SLUGS[i],title+'. '+tech+'. '+summary,PROJECT_URLS[i]))
    buttons = []
    for i,(label,target) in enumerate(c['links']):
        slug = lang+'-link-'+str(i+1)
        w = button(label,i,slug)
        buttons.append(f'<a href="{target}"><img src="./assets/terminal/{slug}.svg" width="{w}" height="32" alt="{label}"></a>')
    sections.append(' '.join(buttons))
    readme = ROOT/('README.md' if lang=='tr' else 'README.en.md')
    readme.write_text('\n\n'.join(sections)+'\n')

if __name__ == '__main__':
    for language in COPY:
        render(language)
