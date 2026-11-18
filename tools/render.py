"""Render the English GitHub profile using the checked-in public stats snapshot."""
from datetime import date
from html import escape
import json
from pathlib import Path

from pixels import length, lettering

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "terminal"
ASSETS.mkdir(parents=True, exist_ok=True)
INK, PANEL, LINE = '#171b35', '#202643', '#404867'
PAPER, LAV, LAV_SHADE = '#fff1d2', '#a9b6ff', '#8998e2'
MINT, BUTTER, ROSE = '#95f2cd', '#ffda82', '#ffaaa7'
BIO = ("My background is in mechatronics. I write software for factory cameras, "
       "build tools for AI coding agents, and develop web and mobile apps.")
ROLE = "AI systems & full-stack engineer"
PORTFOLIO = "https://omersukruvarol.com/"
EXPERIENCE = PORTFOLIO + "#experience-title"
WORK = [
    ("farmakod", "R&D engineer at FarmaKod", "Industrial computer vision and AI on embedded devices.", EXPERIENCE),
    ("linkletics", "Building Linkletics", "I develop the Go APIs behind its web and mobile apps for athletes.", "https://linkletics.com/"),
    ("landed", "Creator of Landed", "I trace edits from Claude Code and Codex sessions into Git commits.", "https://github.com/omersukruvarol/landed-agents"),
]
CONTACT = [
    ("contact", "Get in touch", "mailto:omersukruvarol@gmail.com"),
    ("linkedin", "LinkedIn", "https://www.linkedin.com/in/omersukruvarol/"),
    ("portfolio", "Portfolio", PORTFOLIO),
]

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

def arrow(screen, x, y, u, color):
    screen.path('M1 0h6v6H5V3H4v1H3v1H2v1H1v1H0V5h1V4h1V3h1V2h1V1H1z',color,
                f'translate({x} {y}) scale({u})')

def hero(compact):
    width = 304 if compact else 640
    screen = Screen(width)
    pad = 14 if compact else 24
    screen.rect(0, 0, width, 24, INK)
    screen.rect(pad, 9, 5, 5, MINT)
    screen.label("OMER SUKRU VAROL", pad + 11, 8, 1.23, PAPER)
    screen.label("ISTANBUL", width - pad - length("ISTANBUL", 1.23), 8, 1.23, LAV)

    headline = "Im Omer"
    unit = 2.95 if compact else 5.7
    y = 48 if compact else 62
    screen.label(headline, pad + unit * .45, y + unit * .5, unit, LAV_SHADE, True)
    screen.label(headline, pad, y, unit, INK, True)
    sub_y = 94 if compact else 124
    screen.label(ROLE, pad, sub_y, 1.52 if compact else 1.9, INK, True)

    field_x, field_y, field_w, field_h = (224, 33, 74, 54) if compact else (448, 35, 172, 107)
    for gy in range(field_y, field_y + field_h, 7):
        for gx in range(field_x, field_x + field_w, 7):
            screen.rect(gx, gy, 1, 1, '#7788cf')
    zoom = 2.1 if compact else 4.1
    bx = field_x + (field_w - 24 * zoom) / 2
    by = field_y + (field_h - 24 * zoom) / 2
    screen.rect(bx + 4 * zoom, by + 24 * zoom, 16 * zoom, zoom, '#7e89c9')
    sprite(screen, BOT, BOT_PALETTE, bx, by, zoom)
    bio_end = screen.paragraph(BIO, pad, sub_y + (23 if compact else 31),
                               1.56 if compact else 1.76, width - 2 * pad,
                               18 if compact else 20, INK)
    footer = round(bio_end + 16)
    screen.parts.insert(0, f'<rect width="{width}" height="{footer}" fill="{LAV}"/>')
    screen.rect(0, footer, width, 24, INK)
    screen.label("WORK & EXPERIENCE", pad, footer + 8, 1.2, MINT)
    start = pad + length("WORK & EXPERIENCE", 1.2) + 10
    screen.rect(start, footer + 12, width - start - pad, 1, LINE)
    return screen, footer + 24


def experience(compact, index):
    width = 304 if compact else 640
    pad = 13 if compact else 23
    screen = Screen(width)
    _, title, detail, _ = WORK[index]
    x = pad + (15 if compact else 20)
    accent = [MINT, BUTTER, ROSE][index]
    unit = 1.66 if compact else 2.05
    top = 11 if compact else 13
    # The entire bullet links to the work, including its caption.
    screen.rect(pad, top + 3, 5, 5, accent)
    end = screen.paragraph(title, x, top, unit, width - x - pad - 17,
                           18 if compact else 22, PAPER)
    arrow(screen, width - pad - 9, top + 2, 1.2, accent)
    end = screen.paragraph(detail, x, end + 4, 1.38 if compact else 1.55,
                           width - x - pad, 15 if compact else 18, '#d5dbef')
    height = round(end + 9)
    screen.parts.insert(0, f'<rect width="{width}" height="{height}" fill="{PANEL}"/>')
    screen.rect(pad, height - 1, width - 2 * pad, 1, LINE)
    return screen, height


def contact_button(slug, label):
    unit = 1.4
    width = round(length(label, unit) + 25)
    screen = Screen(width)
    screen.rect(0, 0, width, 32, INK)
    screen.rect(1, 1, width - 2, 30, MINT if slug == 'contact' else LAV)
    screen.label(label, 6, 10, unit, INK)
    arrow(screen, width - 14, 11, 1.2, INK)
    screen.save(slug, 32, label)
    return width


def language_shares(data):
    ordered = sorted(data.items(), key=lambda item: -item[1])
    shown = ordered[:4]
    if len(ordered) > 4:
        shown.append(('Other', sum(size for _, size in ordered[4:])))
    total = sum(data.values())
    return [(name, size / total) for name, size in shown] if total else []


def stats_panel(compact, stats, shares, stamp):
    width = 304 if compact else 640
    screen = Screen(width)
    pad = 13 if compact else 23
    screen.label("My GitHub Stats", pad, 14, 2.25 if compact else 3.0, PAPER, True)
    right = width - pad - length(stamp, 1.15)
    screen.label(stamp, right, 20, 1.15, LAV)
    columns = [
        (stats['public_repositories'], 'Public repos'),
        (stats['public_pull_requests_authored'], 'PRs opened'),
        (stats['public_issues_authored'], 'Issues opened'),
    ]
    col = (width - 2 * pad) / 3
    y = 50 if compact else 60
    for i, (value, label) in enumerate(columns):
        x = pad + i * col
        if i:
            screen.rect(x - 5, y, 1, 37, LINE)
        screen.label(str(value), x, y, 2.8 if compact else 3.5, MINT, True)
        screen.label(label, x, y + (27 if compact else 34),
                     1.12 if compact else 1.55, '#d5dbef')
    y += 56 if compact else 68
    screen.rect(pad, y, width - 2 * pad, 1, LINE)
    y += 16
    screen.label("Most used languages", pad, y, 1.8 if compact else 2.15, PAPER, True)
    y += 26 if compact else 30
    palette = [LAV, ROSE, MINT, BUTTER, '#91a3c0']
    bar = width - 2 * pad
    offset = 0
    for i, (_, share) in enumerate(shares):
        span = bar * share
        screen.rect(pad + offset, y, span, 8, palette[i])
        offset += span
    y += 20
    x = pad
    for i, (name, fraction) in enumerate(shares):
        label = f'{name} {fraction * 100:.1f}%'
        unit = 1.23 if compact else 1.42
        item_w = 10 + length(label, unit)
        if x + item_w > width - pad:
            x = pad
            y += 18 if compact else 22
        screen.rect(x, y + 2, 5, 5, palette[i])
        screen.label(label, x + 9, y, unit, '#e1e4f6')
        x += item_w + (10 if compact else 15)
    note = "By code size in my public repos, excluding forks and this profile."
    end = screen.paragraph(note, pad, y + 22, 1.25 if compact else 1.42,
                           width - 2 * pad, 15, '#b6c1dd')
    height = round(end + 13)
    screen.parts.insert(0, f'<rect width="{width}" height="{height}" fill="{INK}"/>')
    return screen, height


def picture(name, alt, target=None):
    base = './assets/terminal/' + name
    image = (f'<picture><source media="(max-width: 767px)" srcset="{base}-mobile.svg">'
             f'<img src="{base}.svg" width="100%" alt="{escape(alt, quote=True)}"></picture>')
    return f'<a href="{escape(target, quote=True)}">{image}</a>' if target else image


def render():
    stats = json.loads((ROOT / 'tools/stats.json').read_text())
    stamp = date.fromisoformat(stats['as_of']).strftime('%d %b %Y')
    shares = language_shares(stats['language_bytes'])
    intro = f"Im Omer. Omer Sukru Varol, {ROLE} in Istanbul. {BIO} Work and experience."
    stats_alt = (f"My GitHub Stats as of {stamp}. {stats['public_repositories']} public repos, "
                 f"{stats['public_pull_requests_authored']} public pull requests opened and "
                 f"{stats['public_issues_authored']} public issues opened. Most used languages by "
                 "code size in my public repos, excluding forks and this profile: " +
                 ', '.join(f'{name} {share:.1%}' for name, share in shares) + '.')
    for compact in (False, True):
        suffix = '-mobile' if compact else ''
        screen, height = hero(compact)
        screen.save('hello' + suffix, height, intro)
        for i, (slug, title, detail, _) in enumerate(WORK):
            screen, height = experience(compact, i)
            screen.save(slug + suffix, height, title + '. ' + detail)
        screen, height = stats_panel(compact, stats, shares, stamp)
        screen.save('stats' + suffix, height, stats_alt)
    roles = '<br>\n'.join(picture(slug, title + '. ' + detail, url)
                          for slug, title, detail, url in WORK)
    buttons = []
    for slug, label, url in CONTACT:
        width = contact_button(slug, label)
        buttons.append(f'<a href="{url}"><img src="./assets/terminal/{slug}.svg" '
                       f'width="{width}" height="32" alt="{label}"></a>')
    sections = [picture('hello', intro), roles, ' '.join(buttons), picture('stats', stats_alt)]
    (ROOT / 'README.md').write_text('\n\n'.join(sections) + '\n')


if __name__ == '__main__':
    render()
