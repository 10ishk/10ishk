"""Build a flight animation from the real GitHub contribution calendar.

No third-party dependencies. Pass --calendar JSON for offline generation, or
GITHUB_TOKEN/GH_TOKEN to fetch the public calendar through GitHub GraphQL.
"""
import argparse
import datetime as dt
from html import escape
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

QUERY = '''query($login:String!){user(login:$login){contributionsCollection{
contributionCalendar{totalContributions weeks{contributionDays{
date contributionCount contributionLevel}}}}}}'''
LEVELS = {name: i for i, name in enumerate([
    'NONE', 'FIRST_QUARTILE', 'SECOND_QUARTILE', 'THIRD_QUARTILE', 'FOURTH_QUARTILE'])}
PLANE = 'M21 16V14L13 9V3.5A1.5 1.5 0 0 0 10 3.5V9L2 14V16L10 13.5V19L8 20.5V22L11.5 21L15 22V20.5L13 19V13.5Z'


def calendar_for(login):
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError('Set GH_TOKEN/GITHUB_TOKEN, or pass --calendar for offline generation')
    request = Request('https://api.github.com/graphql',
                      data=json.dumps({'query': QUERY, 'variables': {'login': login}}).encode(),
                      headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})
    with urlopen(request, timeout=45) as response:
        result = json.load(response)
    if result.get('errors'):
        raise ValueError('GitHub calendar query failed: ' + json.dumps(result['errors']))
    return result['data']['user']['contributionsCollection']['contributionCalendar']


def render(calendar, dark, animated):
    weeks = calendar['weeks']
    days = [d for week in weeks for d in week['contributionDays']]
    if not days or not 1 <= len(weeks) <= 54:
        raise ValueError('Expected a nonempty annual contribution calendar')
    # Use the sum of the displayed days; GitHub's collection-wide total can differ.
    total = sum(d['contributionCount'] for d in days)
    if len({d['date'] for d in days}) != len(days) or any(d['contributionCount']<0 for d in days):
        raise ValueError('Calendar dates must be unique and daily counts nonnegative')
    bg, fg, muted, accent, border, colors = (
        ('#0f0e0d', '#f7f4ec', '#b6ad9e', '#f6d77a', '#726957',
         ['#302c26', '#5b513b', '#8d794b', '#bca061', '#e1c780']) if dark else
        ('#f7f4ec', '#171410', '#665d4e', '#e5372b', '#b4a990',
         ['#e8e2d6', '#d8c89f', '#b69c62', '#8a713b', '#5a4723']))
    step, tile = min(15, 790/max(1,len(weeks)-1)), 10
    x0 = (880 - ((len(weeks)-1)*step + tile))/2
    left, right = x0+tile/2, x0+(len(weeks)-1)*step+tile/2
    ys = [85+row*18 for row in range(7)]
    route = f'M{left:.2f} {ys[0]}'
    for row,y in enumerate(ys):
        end = right if row%2 == 0 else left
        route += f' H{end:.2f}'
        if row<6:
            control = end+(16 if row%2 == 0 else -16)
            route += f' C{control:.2f} {y} {control:.2f} {ys[row+1]} {end:.2f} {ys[row+1]}'
    css = f'''
.aircraft{{offset-path:path('{route}');offset-anchor:0px 0px;offset-rotate:auto;offset-distance:100%}}
.trail{{opacity:0;stroke-dasharray:32 968;stroke-dashoffset:-968}}
.activity{{opacity:0}}.inflight{{opacity:0}}.complete{{opacity:1}}
'''
    if animated:
        css += '''
.aircraft{animation:flight 32s linear infinite}
@keyframes flight{0%,3%{offset-distance:0%;opacity:1}83%,95%{offset-distance:100%;opacity:1}98%,100%{offset-distance:100%;opacity:0}}
.trail{animation:trail 32s linear infinite}
@keyframes trail{0%,3%{stroke-dashoffset:32;opacity:0}5%{opacity:.6}83%{stroke-dashoffset:-968;opacity:.6}95%,100%{stroke-dashoffset:-968;opacity:0}}
.activity{animation:activity 32s linear infinite}
@keyframes activity{0%{opacity:0}1%{opacity:.5}5%,100%{opacity:0}}
.inflight{animation:flying 32s linear infinite}
@keyframes flying{0%,81%{opacity:1}83%,100%{opacity:0}}
.complete{animation:complete 32s linear infinite}
@keyframes complete{0%,81%{opacity:0}84%,96%{opacity:1}99%,100%{opacity:0}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}.aircraft{offset-distance:100%;opacity:1}.trail,.activity,.inflight{opacity:0}.complete{opacity:1}}
'''
    body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="880" height="266" viewBox="0 0 880 266" role="img" aria-label="Flight log for 10ishk: {total} GitHub contributions. One plane follows the calendar; contribution tiles remain visible.">',
            f'<title>Flight log — {total:,} GitHub contributions</title>',
            f'<desc>Real contribution dates {days[0]["date"]} through {days[-1]["date"]}. The flight path is decorative; tile colours show activity levels.</desc>',
            f'<style>{css}</style><rect width="880" height="266" rx="10" fill="{bg}"/>']

    def text(x,y,value,size=11,color=fg,anchor='start'):
        return f'<text x="{x}" y="{y}" font-family="Consolas,monospace" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(value)}</text>'

    body += [text(28,30,'CONTRIBUTION AIRSPACE',12,accent),
             text(852,30,days[0]['date']+' / '+days[-1]['date'],11,muted,'end')]
    last_month = None
    for col,week in enumerate(weeks):
        date = dt.date.fromisoformat(week['contributionDays'][0]['date'])
        if date.month != last_month and col < len(weeks)-2:
            body.append(text(round(x0+col*step),59,date.strftime('%b'),10,muted))
            last_month = date.month
        for day in week['contributionDays']:
            date = dt.date.fromisoformat(day['date'])
            row = (date.weekday()+1)%7
            level = LEVELS[day['contributionLevel']]
            x,y = x0+col*step, ys[row]-tile/2
            tooltip = f'{day["date"]}: {day["contributionCount"]} contributions'
            body.append(f'<rect class="day" data-date="{day["date"]}" data-count="{day["contributionCount"]}" x="{x:.2f}" y="{y}" width="{tile}" height="{tile}" rx="2" fill="{colors[level]}" stroke="{border}" stroke-width=".45"><title>{tooltip}</title></rect>')
            if animated and level:
                progress = (row + (col/(len(weeks)-1) if row%2==0 else 1-col/(len(weeks)-1)))/7
                delay = 32*(.03+.8*progress)
                body.append(f'<rect class="activity" style="animation-delay:{delay:.3f}s" x="{x:.2f}" y="{y}" width="{tile}" height="{tile}" rx="2" fill="{accent}"/>')
    body += [f'<path class="trail" d="{route}" pathLength="1000" fill="none" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>']
    aircraft = f'<g transform="rotate(90)"><path transform="translate(-12 -12) scale(1.15)" d="{PLANE}" fill="{accent}" stroke="{bg}" stroke-width="1" stroke-linejoin="round"/></g>'
    if animated:
        body.append(f'<g class="aircraft">{aircraft}</g>')
    else:
        body.append(f'<g transform="translate({right:.2f} {ys[-1]})">{aircraft}</g>')
    body += [f'<path d="M28 218H852" stroke="{border}" stroke-dasharray="5 5"/>',
             text(28,244,f'DXB-010 / {total:,} CONTRIBUTIONS SHOWN',11,fg),
             '<g class="inflight">'+text(852,244,'IN FLIGHT →',11,accent,'end')+'</g>',
             '<g class="complete">'+text(852,244,'ROUTE COMPLETE ✓',11,accent,'end')+'</g>', '</svg>']
    return ''.join(body)+'\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user',default='10ishk')
    parser.add_argument('--calendar',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    calendar = json.loads(args.calendar.read_text(encoding='utf-8-sig')) if args.calendar else calendar_for(args.user)
    args.output.mkdir(parents=True,exist_ok=True)
    for dark in (False,True):
        for animated in (True,False):
            name='flight-log'+('-dark' if dark else '-light')+('' if animated else '-still')+'.svg'
            (args.output/name).write_text(render(calendar,dark,animated),encoding='utf-8')
    shown = sum(d['contributionCount'] for w in calendar['weeks'] for d in w['contributionDays'])
    print(f'Generated 4 flight-log SVGs from {len(calendar["weeks"])} weeks and {shown} displayed contributions.')
