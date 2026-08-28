# -*- coding: utf-8 -*-
"""24/7 Locksmith Miami — static site generator. Miami Art-Deco design.
Generates 250+ unique, locally-grounded pages. White-hat: no fake reviews,
no response-time guarantees, no license claims, approved lock brands only."""
import os, re, hashlib, html
from data import AREAS, SERVICES, COMBO_SERVICES, ZIP_NOTE, PHONE, PHONE_RAW, DOMAIN, BRAND, GSC_TOKEN

OUT = os.path.join(os.path.dirname(__file__), "..", "site")

def seed(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)

def pick(bank, key, n=1, offset=0):
    """Deterministically pick n distinct items from bank based on key."""
    s = seed(key) + offset
    out, used = [], set()
    for i in range(n):
        idx = (s // (7 ** (i + 1)) + i * 13) % len(bank)
        while idx in used:
            idx = (idx + 1) % len(bank)
        used.add(idx)
        out.append(bank[idx])
    return out if n > 1 else out[0]

AREA = {a[0]: a for a in AREAS}
SVC = {s[0]: s for s in SERVICES}

# ---------------- Design ----------------
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Limelight&family=Josefin+Sans:wght@400;600;700&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">'

CSS = """
:root{--navy:#0c1626;--navy2:#122036;--teal:#17bebb;--teal-d:#0e918f;--coral:#ff6f61;--cream:#f7f1e3;--sand:#efe6d0;--gold:#e8b04b;--ink:#1c2434;--line:rgba(23,190,187,.25)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Jost',system-ui,sans-serif;color:var(--ink);background:var(--cream);line-height:1.65;font-size:17px}
h1,h2,h3,h4{font-family:'Josefin Sans',sans-serif;line-height:1.2;color:var(--navy)}
a{color:var(--teal-d);text-decoration:none}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
/* deco top border */
.deco-band{height:8px;background:repeating-linear-gradient(90deg,var(--teal) 0 24px,var(--gold) 24px 32px,var(--coral) 32px 56px,var(--gold) 56px 64px)}
/* header */
header{background:var(--navy);position:sticky;top:0;z-index:50;box-shadow:0 2px 14px rgba(12,22,38,.35)}
.hd{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;max-width:1120px;margin:0 auto;gap:14px}
.logo{display:flex;align-items:center;gap:12px;color:var(--cream)}
.logo .mk{width:44px;height:44px;flex:none}
.logo b{font-family:'Limelight',cursive;font-size:1.25rem;font-weight:400;letter-spacing:.5px;color:var(--cream)}
.logo small{display:block;font-size:.68rem;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);font-family:'Josefin Sans',sans-serif}
nav{display:flex;gap:22px;align-items:center;flex-wrap:wrap}
nav a{color:#cfe8e7;font-family:'Josefin Sans',sans-serif;font-size:.95rem;letter-spacing:.04em}
nav a:hover{color:var(--gold)}
.call{background:var(--coral);color:#fff!important;padding:10px 20px;border-radius:999px;font-weight:700;box-shadow:0 4px 14px rgba(255,111,97,.4);white-space:nowrap}
.call:hover{background:#ff5a4a;color:#fff}
/* hero */
.hero{background:linear-gradient(160deg,var(--navy) 0%,var(--navy2) 55%,#16324f 100%);color:var(--cream);position:relative;overflow:hidden;padding:74px 0 66px}
.hero:before{content:"";position:absolute;inset:0;background:radial-gradient(1200px 400px at 85% -10%,rgba(23,190,187,.22),transparent 60%),radial-gradient(700px 300px at 5% 110%,rgba(255,111,97,.16),transparent 60%)}
.hero .wrap{position:relative}
.eyebrow{font-family:'Josefin Sans',sans-serif;letter-spacing:.32em;text-transform:uppercase;font-size:.74rem;color:var(--gold);margin-bottom:16px}
.hero h1{color:var(--cream);font-size:clamp(1.9rem,4.4vw,3.1rem);max-width:820px;text-wrap:balance}
.hero p.lead{max-width:640px;margin:18px 0 28px;color:#d9e6ea;font-size:1.08rem}
.cta-row{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.btn{display:inline-block;padding:14px 28px;border-radius:999px;font-family:'Josefin Sans',sans-serif;font-weight:700;font-size:1.02rem;letter-spacing:.03em}
.btn.primary{background:var(--coral);color:#fff;box-shadow:0 6px 20px rgba(255,111,97,.45)}
.btn.primary:hover{background:#ff5a4a}
.btn.ghost{border:2px solid var(--teal);color:var(--teal)}
.btn.ghost:hover{background:rgba(23,190,187,.12)}
.hero .sub{margin-top:20px;font-size:.9rem;color:#9fb8c4;letter-spacing:.05em}
/* deco divider */
.deco-div{display:flex;align-items:center;gap:10px;margin:0 0 26px}
.deco-div span{width:34px;height:3px;background:var(--gold)}
.deco-div i{width:10px;height:10px;border:2px solid var(--coral);transform:rotate(45deg)}
/* sections */
section{padding:58px 0}
section.alt{background:var(--sand)}
section.dark{background:var(--navy);color:var(--cream)}
section.dark h2,section.dark h3{color:var(--cream)}
h2{font-size:clamp(1.5rem,3vw,2.15rem);margin-bottom:14px;text-wrap:balance}
.sec-intro{max-width:720px;margin-bottom:32px;color:#3d4a5c}
section.dark .sec-intro{color:#c6d6dd}
/* cards */
.grid{display:grid;gap:20px}
.grid.c3{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.grid.c4{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.card{background:#fff;border-radius:14px;padding:26px 24px;border:1px solid var(--line);box-shadow:0 3px 14px rgba(12,22,38,.06);position:relative;overflow:hidden}
.card:before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:linear-gradient(90deg,var(--teal),var(--gold))}
.card h3{font-size:1.12rem;margin:0 0 8px}
.card p{font-size:.95rem;color:#435062}
.card a.more{font-weight:600;font-size:.9rem;display:inline-block;margin-top:10px}
/* area chips */
.chips{display:flex;flex-wrap:wrap;gap:10px}
.chips a{background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 16px;font-size:.9rem;color:var(--navy);font-family:'Josefin Sans',sans-serif}
.chips a:hover{border-color:var(--coral);color:var(--coral)}
/* steps */
.steps{counter-reset:st}
.step{display:flex;gap:18px;padding:18px 0;border-bottom:1px dashed var(--line);align-items:flex-start}
.step:last-child{border-bottom:0}
.step .n{counter-increment:st;flex:none;width:46px;height:46px;border-radius:50%;border:2px solid var(--gold);color:var(--navy);display:flex;align-items:center;justify-content:center;font-family:'Limelight',cursive;font-size:1.1rem}
.step .n:before{content:counter(st)}
section.dark .step .n{color:var(--gold)}
.step h3{font-size:1.05rem;margin-bottom:4px}
.step p{font-size:.95rem;color:#435062}
section.dark .step p{color:#c6d6dd}
/* faq */
details{background:#fff;border:1px solid var(--line);border-radius:12px;margin-bottom:12px;overflow:hidden}
summary{cursor:pointer;padding:16px 20px;font-family:'Josefin Sans',sans-serif;font-weight:600;color:var(--navy);list-style:none;position:relative;padding-right:44px}
summary:after{content:"+";position:absolute;right:18px;top:12px;font-size:1.4rem;color:var(--coral)}
details[open] summary:after{content:"–"}
details .a{padding:0 20px 18px;color:#435062;font-size:.96rem}
/* prose */
.prose{max-width:760px}
.prose p{margin-bottom:16px}
.prose h2{margin-top:34px}
.prose h3{margin-top:26px;margin-bottom:10px;font-size:1.15rem}
.prose ul{margin:0 0 16px 22px}
.prose li{margin-bottom:6px}
/* callout */
.callout{background:var(--navy);color:var(--cream);border-radius:16px;padding:34px 30px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px;position:relative;overflow:hidden}
.callout:before{content:"";position:absolute;inset:0;background:radial-gradient(500px 200px at 90% 0%,rgba(232,176,75,.18),transparent 60%)}
.callout h3{color:var(--cream);font-size:1.3rem;margin:0;position:relative}
.callout p{color:#c6d6dd;margin:6px 0 0;position:relative;font-size:.95rem}
/* footer */
footer{background:var(--navy);color:#9fb8c4;padding:54px 0 30px;font-size:.92rem}
footer h4{color:var(--cream);font-size:1rem;margin-bottom:14px;font-family:'Josefin Sans',sans-serif;letter-spacing:.06em}
footer a{color:#9fb8c4}
footer a:hover{color:var(--gold)}
.fgrid{display:grid;gap:34px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin-bottom:34px}
.fbot{border-top:1px solid rgba(255,255,255,.1);padding-top:22px;display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;font-size:.82rem}
footer ul{list-style:none}
footer li{margin-bottom:8px}
/* fx scroll */
.fxblk{opacity:0;transform:translateY(22px);transition:opacity .6s ease,transform .6s ease}
.fxlit{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.fxblk{opacity:1;transform:none;transition:none}}
/* breadcrumbs */
.crumbs{font-size:.84rem;padding:16px 0 0;color:#6b7887}
.crumbs a{color:var(--teal-d)}
/* mobile */
@media(max-width:760px){nav{display:none}.hd .call{padding:9px 16px;font-size:.9rem}section{padding:44px 0}}
.mnav{display:none}
@media(max-width:760px){.mnav{display:flex;gap:14px;flex-wrap:wrap;background:var(--navy2);padding:10px 22px}.mnav a{color:#cfe8e7;font-size:.85rem;font-family:'Josefin Sans',sans-serif}}
"""

FX = """<script>(function(){function lit(){var els=document.querySelectorAll('.fxblk');var vh=window.innerHeight;els.forEach(function(e){var r=e.getBoundingClientRect();if(r.top<vh*0.92&&r.bottom>0)e.classList.add('fxlit');});}
if(matchMedia('(prefers-reduced-motion: reduce)').matches){document.querySelectorAll('.fxblk').forEach(function(e){e.classList.add('fxlit')});return;}
window.addEventListener('scroll',lit,{passive:true});window.addEventListener('load',lit);document.addEventListener('DOMContentLoaded',lit);setTimeout(lit,60);})();</script>"""

LOGO_SVG = """<svg class="mk" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><rect width="44" height="44" rx="9" fill="#17bebb"/><path d="M22 6l12 7v18l-12 7-12-7V13z" fill="#0c1626"/><circle cx="22" cy="19" r="5.2" fill="none" stroke="#e8b04b" stroke-width="2.4"/><rect x="20.7" y="23" width="2.6" height="9" rx="1.3" fill="#e8b04b"/><rect x="23.3" y="27" width="3.6" height="2.3" rx="1" fill="#e8b04b"/><rect x="23.3" y="30.4" width="2.6" height="2.3" rx="1" fill="#ff6f61"/></svg>"""

FAVICON = '<link rel="icon" type="image/svg+xml" href="/favicon.svg">'

def nav_html():
    return f"""<div class="deco-band"></div><header><div class="hd">
<a class="logo" href="/">{LOGO_SVG}<span><b>24/7 Locksmith Miami</b><small>Miami-Dade · Around the Clock</small></span></a>
<nav><a href="/services/">Services</a><a href="/service-areas/">Service Areas</a><a href="/car-key-replacement/">Car Keys</a><a href="/about/">About</a><a href="/contact/">Contact</a><a class="call" href="tel:{PHONE_RAW}">☎ {PHONE}</a></nav>
</div><div class="mnav"><a href="/services/">Services</a><a href="/service-areas/">Areas</a><a href="/about/">About</a><a href="/contact/">Contact</a></div></header>"""

def footer_html():
    svc_links = "".join(f'<li><a href="/{s[0]}/">{s[1]}</a></li>' for s in SERVICES[:7])
    area_links = "".join(f'<li><a href="/locksmith-{a[0]}/">{a[1]}</a></li>' for a in AREAS[:7])
    return f"""<footer><div class="wrap"><div class="fgrid">
<div><h4>24/7 Locksmith Miami</h4><p>Mobile locksmith service across Miami-Dade County, Florida. Cars, homes and businesses — around the clock.</p><p style="margin-top:12px"><a class="call" style="display:inline-block" href="tel:{PHONE_RAW}">☎ {PHONE}</a></p></div>
<div><h4>Services</h4><ul>{svc_links}<li><a href="/services/">All services →</a></li></ul></div>
<div><h4>Service Areas</h4><ul>{area_links}<li><a href="/service-areas/">All areas →</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="/about/">About us</a></li><li><a href="/contact/">Contact</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
</div><div class="fbot"><span>© 24/7 Locksmith Miami. Mobile service — Miami-Dade County, FL.</span><span>Open 24 hours, 7 days a week.</span></div></div></footer>"""

def shell(title, desc, path, body, schema=""):
    canonical = DOMAIN + path
    og = f"""<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="{BRAND}">"""
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="google-site-verification" content="{GSC_TOKEN}">
{og}{FAVICON}{FONTS}<style>{CSS}</style>{schema}</head><body>
{nav_html()}
{body}
{footer_html()}{FX}</body></html>"""

def biz_schema(area_name=None):
    area = f", serving {area_name}" if area_name else ""
    return f"""<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Locksmith","name":"{BRAND}","telephone":"+1{PHONE_RAW}","url":"{DOMAIN}/","areaServed":{{"@type":"AdministrativeArea","name":"Miami-Dade County, FL"}},"description":"24/7 mobile locksmith service across Miami-Dade County{area}. Car lockouts, house lockouts, car key replacement, rekeying and commercial locksmith work.","openingHours":"Mo-Su 00:00-23:59","priceRange":"$$"}}</script>"""

def faq_schema(faqs):
    items = ",".join('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' % (q.replace('"','\\"'), a.replace('"','\\"')) for q, a in faqs)
    return f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{items}]}}</script>'

def crumbs(items):
    lis = "".join(f' › <a href="{u}">{t}</a>' if u else f' › {t}' for t, u in items)
    return f'<div class="wrap crumbs"><a href="/">Home</a>{lis}</div>'

def callout(title_txt, sub):
    return f"""<div class="callout fxblk"><div><h3>{title_txt}</h3><p>{sub}</p></div><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div>"""

# ---------------- Content banks ----------------
OPEN_COMBO = [
 "When you're standing outside {thing} in {area}, every minute feels long. {brand} runs mobile units across {roads}, so a technician heads your way the moment you call — day or night.",
 "A {svc_low} in {area} never happens at a convenient time. That's why {brand} keeps technicians on call around the clock, covering the blocks around {roads} and the rest of the neighborhood.",
 "{area} is {anchor} — and when {thing_need} here, you want someone who actually knows the area. {brand} dispatches mobile locksmiths across {roads} every day of the week.",
 "Locked out or locked up in {area}? {brand} covers this part of Miami-Dade around the clock, with mobile technicians who regularly work the streets off {roads}.",
 "From {roads} to the quieter streets beyond, {brand} handles {svc_low} calls across {area} at any hour — our dispatch line answers 24/7, every day of the year.",
 "{brand} treats {area} as home turf. Our mobile technicians handle {svc_low} calls throughout the neighborhood — including the busy stretch along {roads} — around the clock.",
]
LOCAL_COMBO = [
 "This part of Miami-Dade is known for {vibe}, which shapes how we work here. Our technicians arrive with the tools for exactly those doors, locks and parking situations — not a one-size-fits-all kit.",
 "Because {area} means {vibe}, our technicians come prepared for the hardware and access situations that are actually common here, from older cylinders to modern electronic locks.",
 "Anyone who works in {area} knows the housing here: {vibe}. We've equipped our mobile units accordingly, so the technician who arrives can finish the job in one visit in most cases.",
 "{area} — {anchor} — has its own mix of doors and locks: {vibe}. That local reality is exactly what our technicians deal with every week, so nothing about your call will be new to them.",
]
PROCESS_HEADERS = ["How it works when you call", "What happens after you call", "From your call to the fix", "Here's how we handle it"]
TRUST_COMBO = [
 "We quote before we work. You'll hear a clear price range on the phone based on what you describe, and the technician confirms the exact price on-site before touching the lock — no surprises when the job is done.",
 "Every job starts with a straight answer: our dispatcher gives you a realistic price range up front, and the technician confirms the final number in person before any work begins.",
 "You approve the price before the work starts. We give a range over the phone, the technician verifies the situation on arrival, and you get a firm number before we open a single tool bag.",
]
DAMAGE = [
 "Non-destructive entry always comes first. Drilling a lock is a last resort reserved for genuine high-security failures — in the great majority of lockouts we open the door and you keep your lock.",
 "Our first tools are picks, bypass tools and decoders — not drills. Most lockouts end with the door open and the original lock still working exactly as it did before.",
 "We open locks the patient way. Destructive entry is rare and only happens with your explicit go-ahead when there is no reasonable alternative.",
]
CTA_LINE = [
 "One call brings a mobile locksmith to you", "Talk to a live dispatcher now", "A technician can be on the way in minutes",
 "We answer around the clock", "Save the number — you'll be glad you did",
]

FAQ_BANK_COMBO = [
 ("How fast can a locksmith reach {area}?","Travel time depends on where our nearest mobile unit is and Miami traffic, so we don't promise a fixed number of minutes. What we can promise: dispatch answers immediately, tells you honestly where the closest technician is, and keeps you updated on the way."),
 ("How much does {svc_low} cost in {area}?","Pricing depends on the lock or vehicle involved and the time of day. You'll get a realistic range on the phone before anyone is dispatched, and the technician confirms the exact price on-site before starting work."),
 ("Will you damage my lock or car?","No — non-destructive methods come first, every time. For vehicles we use proper entry tools that protect paint, seals and electronics. Drilling a lock only happens as a genuine last resort, with your approval."),
 ("Do you really operate 24 hours in {area}?","Yes. Dispatch answers around the clock, every day of the year, and technicians rotate on call overnight. Late-night and holiday calls may carry an after-hours rate, which we state up front."),
 ("Do I need to show ID for a lockout?","Yes — for your protection we verify that you have a right to enter the home, business or vehicle before opening it. A driver's license, registration or lease normally settles it in seconds."),
 ("Can you make a car key if I lost all of mine?","In most cases, yes. We cut and program keys on-site for most makes and models, including transponder keys and proximity fobs — even when there's no key left to copy."),
 ("Should I rekey or replace my locks?","If the hardware is in good shape, rekeying is usually the smarter buy — the lock stays, old keys stop working. If the lock is worn, damaged or outdated, we'll recommend replacement and tell you why."),
 ("Do you serve gated communities and condo buildings?","Yes — a large share of our {area} calls are condos, gated communities and buildings with controlled access. Just let the gate or front desk know a locksmith is coming for you."),
]

def combo_page(svc_slug, a):
    aslug, aname, kind, anchor, roads, vibe = a
    s = SVC[svc_slug]
    sname, sshort, sblurb = s[1], s[2], s[4]
    key = f"{svc_slug}|{aslug}"
    thing = {"car-lockout":"your locked car","house-lockout":"your own front door","car-key-replacement":"your car with no working key","lock-rekey":"a home that old keys can still open"}[svc_slug]
    thing_need = {"car-lockout":"you're locked out of your car","house-lockout":"you're locked out of your home","car-key-replacement":"you've lost your car keys","lock-rekey":"your locks need rekeying"}[svc_slug]
    svc_low = sname.lower().replace("service","").strip()
    fmt = dict(area=aname, brand=BRAND, roads=roads, anchor=anchor, vibe=vibe, thing=thing, thing_need=thing_need, svc_low=svc_low)
    if svc_slug == "lock-rekey":
        REKEY_OPEN = [
         "Moving into a new place in {area}? Until the locks are rekeyed, every previous keyholder can still walk in. {brand} sends mobile technicians across {roads} and the rest of the neighborhood to fix that in a single visit — any day, any hour.",
         "Old keys have a way of multiplying — contractors, cleaners, exes, former tenants. {brand} rekeys locks across {area} so your existing hardware answers to one new key, with mobile units working the blocks around {roads} daily.",
         "{area} is {anchor} — and homes here change hands, tenants and roommates like anywhere else. {brand} rekeys your existing locks on-site so old keys die instantly, without replacing hardware that still works.",
         "A rekey is the cheapest security upgrade there is: same locks, brand-new pins, old keys useless. {brand} covers all of {area} with mobile units, from {roads} out to the quiet residential streets.",
        ]
        p1 = pick(REKEY_OPEN, key).format(**fmt)
    else:
        p1 = pick(OPEN_COMBO, key).format(**fmt)
    p2 = pick(LOCAL_COMBO, key, offset=3).format(**fmt)
    trust = pick(TRUST_COMBO, key, offset=7)
    dmg = pick(DAMAGE, key, offset=11)
    zips = ZIP_NOTE.get(aslug)
    zipline = f" We cover all of {aname}, including the {zips} ZIP codes." if zips else f" We cover every corner of {aname} and the surrounding blocks."
    faqs_raw = pick(FAQ_BANK_COMBO, key, n=4, offset=17)
    faqs = [(q.format(**fmt), ans.format(**fmt)) for q, ans in faqs_raw]
    faq_html = "".join(f'<details class="fxblk"><summary>{q}</summary><div class="a">{ans}</div></details>' for q, ans in faqs)
    steps_h = pick(PROCESS_HEADERS, key, offset=23)
    other = [x for x in COMBO_SERVICES if x != svc_slug]
    rel = "".join(f'<a href="/{o}-{aslug}/">{SVC[o][1]} in {aname}</a>' for o in other)
    near = [x for x in AREAS if x[0] != aslug][seed(key) % (len(AREAS)-6):][:5]
    nearby = "".join(f'<a href="/{svc_slug}-{n[0]}/">{n[1]}</a>' for n in near)
    title = f"{sname} in {aname}, FL | {BRAND}"
    desc = f"{sname.rstrip('.')} in {aname} — 24/7 mobile locksmith serving all of Miami-Dade. Up-front pricing, damage-free methods. Call {PHONE}."
    body = f"""
<div class="hero"><div class="wrap"><div class="eyebrow">{aname} · Miami-Dade County</div>
<h1>{sname} in {aname}</h1>
<p class="lead">{sshort} Mobile service, 24 hours a day, anywhere in {aname}.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a><a class="btn ghost" href="/service-areas/">All service areas</a></div>
<div class="sub">Up-front pricing · Damage-free first · Open 24/7</div></div></div>
{crumbs([("Services","/services/"),(sname,f"/{svc_slug}/"),(aname,None)])}
<section><div class="wrap prose">
<div class="deco-div"><span></span><i></i><span></span></div>
<p class="fxblk">{p1}</p>
<p class="fxblk">{p2}</p>
<h2 class="fxblk">About our {svc_low} service</h2>
<p class="fxblk">{sblurb}{zipline}</p>
<p class="fxblk">{trust}</p>
<p class="fxblk">{dmg}</p>
</div></section>
<section class="alt"><div class="wrap"><h2 class="fxblk">{steps_h}</h2><div class="steps prose">
<div class="step fxblk"><span class="n"></span><div><h3>Call {PHONE}</h3><p>A live dispatcher takes your location in {aname}, what happened, and gives you an honest price range.</p></div></div>
<div class="step fxblk"><span class="n"></span><div><h3>A mobile unit heads your way</h3><p>The nearest available technician is dispatched to you with the tools for the job — we tell you who's coming and keep you posted.</p></div></div>
<div class="step fxblk"><span class="n"></span><div><h3>Price confirmed on-site</h3><p>Before any work begins, the technician confirms the exact price in person. You approve it first.</p></div></div>
<div class="step fxblk"><span class="n"></span><div><h3>Done — and tested</h3><p>The work is completed, tested in front of you, and you're back to your day. Payment by card or cash.</p></div></div>
</div></div></section>
<section><div class="wrap"><h2 class="fxblk">Questions we hear in {aname}</h2>{faq_html}</div></section>
<section class="alt"><div class="wrap">{callout(f"Need {svc_low} in {aname} right now?", pick(CTA_LINE, key, offset=29) + " — 24 hours a day, 7 days a week.")}
<div style="margin-top:34px"><h3 style="margin-bottom:12px">More locksmith help in {aname}</h3><div class="chips fxblk">{rel}</div>
<h3 style="margin:22px 0 12px">{sname} nearby</h3><div class="chips fxblk">{nearby}</div></div></div></section>"""
    schema = biz_schema(aname) + faq_schema(faqs)
    return title, desc, f"/{svc_slug}-{aslug}/", body, schema

# ---------------- Area pages ----------------
AREA_OPEN = [
 "{area} — {anchor} — deserves a locksmith that treats it like more than a pin on a map. {brand} runs mobile units through this part of Miami-Dade every day, covering everything from quick lockouts to full lock upgrades.",
 "Whether you live off {roads} or run a business nearby, {brand} keeps {area} covered 24 hours a day. One number reaches a live dispatcher and puts the nearest mobile locksmith on the road to you.",
 "{brand} covers all of {area}, around the clock. Our technicians know the neighborhood — {anchor} — and arrive equipped for the doors and locks that are actually common here.",
 "For drivers, homeowners and businesses across {area}, {brand} is one call away at any hour. We work this area daily, from {roads} to the residential streets beyond.",
]
AREA_MID = [
 "Housing here means {vibe} — and that changes what a locksmith needs on the truck. Our mobile units carry hardware and tools matched to the area, so most jobs finish in a single visit.",
 "The everyday reality of {area} is {vibe}. Our technicians work with that hardware constantly, which is why we can usually quote accurately over the phone and finish on the first trip.",
 "Expect {vibe} in this part of the county — our technicians handle exactly that mix every week, from vintage mortise locks to the newest smart deadbolts.",
]

def area_page(a):
    aslug, aname, kind, anchor, roads, vibe = a
    key = "area|" + aslug
    fmt = dict(area=aname, brand=BRAND, roads=roads, anchor=anchor, vibe=vibe)
    p1 = pick(AREA_OPEN, key).format(**fmt)
    p2 = pick(AREA_MID, key, offset=5).format(**fmt)
    zips = ZIP_NOTE.get(aslug)
    zipline = f"Coverage includes the {zips} ZIP codes and everything in between." if zips else f"Coverage includes every street and building in {aname}."
    cards = "".join(f'''<div class="card fxblk"><h3>{SVC[s][1]}</h3><p>{SVC[s][2]}</p><a class="more" href="/{s}-{aslug}/">{SVC[s][1]} in {aname} →</a></div>''' for s in COMBO_SERVICES)
    more = "".join(f'<a href="/{s[0]}/">{s[1]}</a>' for s in SERVICES if s[0] not in COMBO_SERVICES)
    near = [x for x in AREAS if x[0] != aslug][seed(key) % (len(AREAS)-8):][:7]
    nearby = "".join(f'<a href="/locksmith-{n[0]}/">{n[1]}</a>' for n in near)
    faqs = [(q.format(area=aname, svc_low="locksmith service"), ans.format(area=aname, svc_low="locksmith service")) for q, ans in pick(FAQ_BANK_COMBO, key, n=3, offset=13)]
    faq_html = "".join(f'<details class="fxblk"><summary>{q}</summary><div class="a">{ans}</div></details>' for q, ans in faqs)
    title = f"Locksmith in {aname}, FL — 24/7 Mobile Service | {BRAND}"
    desc = f"24/7 locksmith in {aname}: car lockouts, house lockouts, car keys made on-site, rekeying and more. Mobile service with up-front pricing. Call {PHONE}."
    body = f"""
<div class="hero"><div class="wrap"><div class="eyebrow">Serving {aname} · 24 hours</div>
<h1>Your 24/7 Locksmith in {aname}</h1>
<p class="lead">Cars, homes and businesses across {aname} — mobile locksmiths with up-front pricing, any hour of the day.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a><a class="btn ghost" href="/services/">See all services</a></div>
<div class="sub">Damage-free methods first · Live dispatch · Miami-Dade County</div></div></div>
{crumbs([("Service Areas","/service-areas/"),(aname,None)])}
<section><div class="wrap prose">
<div class="deco-div"><span></span><i></i><span></span></div>
<p class="fxblk">{p1}</p><p class="fxblk">{p2}</p><p class="fxblk">{zipline}</p>
</div></section>
<section class="alt"><div class="wrap"><h2 class="fxblk">Popular services in {aname}</h2><div class="grid c4">{cards}</div>
<div style="margin-top:26px"><h3 style="margin-bottom:12px">Also available here</h3><div class="chips fxblk">{more}</div></div></div></section>
<section><div class="wrap"><h2 class="fxblk">{aname} locksmith questions</h2>{faq_html}</div></section>
<section class="alt"><div class="wrap">{callout(f"Locked out in {aname}?","A live dispatcher answers 24/7 and sends the nearest mobile unit.")}
<div style="margin-top:34px"><h3 style="margin-bottom:12px">Nearby areas we serve</h3><div class="chips fxblk">{nearby}</div></div></div></section>"""
    return title, desc, f"/locksmith-{aslug}/", body, biz_schema(aname) + faq_schema(faqs)

# ---------------- Service pages ----------------
def service_page(s):
    slug, name, short, cat, blurb = s
    key = "svc|" + slug
    in_combo = slug in COMBO_SERVICES
    if in_combo:
        area_links = "".join(f'<a href="/{slug}-{a[0]}/">{a[1]}</a>' for a in AREAS)
        area_sec = f'<section class="alt"><div class="wrap"><h2 class="fxblk">{name} across Miami-Dade</h2><p class="sec-intro">Choose your neighborhood for local details:</p><div class="chips fxblk">{area_links}</div></div></section>'
    else:
        area_sec = f'<section class="alt"><div class="wrap"><h2 class="fxblk">Available everywhere we serve</h2><p class="sec-intro">This service is available across all of Miami-Dade County — <a href="/service-areas/">see our full coverage map</a> or just call and tell dispatch where you are.</p>{callout("Ready when you are","One number, any hour: a live dispatcher and a mobile technician near you.")}</div></section>'
    others = [x for x in SERVICES if x[0] != slug][seed(key) % 9:][:4]
    rel = "".join(f'<div class="card fxblk"><h3>{o[1]}</h3><p>{o[2]}</p><a class="more" href="/{o[0]}/">Learn more →</a></div>' for o in others)
    faqs = [(q.format(area="Miami", svc_low=name.lower()), ans.format(area="Miami", svc_low=name.lower())) for q, ans in pick(FAQ_BANK_COMBO, key, n=4, offset=19)]
    faq_html = "".join(f'<details class="fxblk"><summary>{q}</summary><div class="a">{ans}</div></details>' for q, ans in faqs)
    extra = {
      "auto":"We service most makes and models on the road in Florida — domestic, Japanese, Korean and European — with key cutting and programming equipment on the truck. If your vehicle is unusual, tell dispatch the year, make and model and we'll confirm before rolling out.",
      "residential":"Houses, condos, townhomes and apartments all get the same treatment: honest advice about whether to repair, rekey or replace, quality hardware from names like Schlage, Kwikset and Yale, and installation that leaves doors closing the way they should.",
      "commercial":"Storefronts, offices, restaurants and warehouses across Miami-Dade rely on hardware that takes a beating. We install and service commercial-grade locks, exit devices and key control systems designed for daily abuse — and we document key assignments when you want them tracked.",
      "emergency":"Emergency work is the backbone of what we do. Dispatch answers around the clock, technicians rotate on call through the night, and after-hours rates are always stated before anyone is sent your way.",
    }[cat]
    title = f"{name} in Miami, FL | {BRAND}"
    desc = f"{short} 24/7 mobile service across Miami-Dade with up-front pricing. Call {PHONE}."
    body = f"""
<div class="hero"><div class="wrap"><div class="eyebrow">Miami-Dade County · 24/7</div>
<h1>{name} in Miami</h1><p class="lead">{short}</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a><a class="btn ghost" href="/service-areas/">Where we work</a></div>
<div class="sub">Up-front pricing · Damage-free first · Mobile units county-wide</div></div></div>
{crumbs([("Services","/services/"),(name,None)])}
<section><div class="wrap prose"><div class="deco-div"><span></span><i></i><span></span></div>
<p class="fxblk">{blurb}</p><p class="fxblk">{extra}</p>
<p class="fxblk">{pick(TRUST_COMBO,key)}</p><p class="fxblk">{pick(DAMAGE,key,offset=3)}</p></div></section>
{area_sec}
<section><div class="wrap"><h2 class="fxblk">Common questions</h2>{faq_html}</div></section>
<section class="alt"><div class="wrap"><h2 class="fxblk">Related services</h2><div class="grid c4">{rel}</div></div></section>"""
    return title, desc, f"/{slug}/", body, biz_schema() + faq_schema(faqs)

# ---------------- Index & misc pages ----------------
def home_page():
    svc_cards = "".join(f'<div class="card fxblk"><h3>{s[1]}</h3><p>{s[2]}</p><a class="more" href="/{s[0]}/">Details →</a></div>' for s in SERVICES[:8])
    area_chips = "".join(f'<a href="/locksmith-{a[0]}/">{a[1]}</a>' for a in AREAS)
    title = "24/7 Locksmith Miami — Car, Home & Business Locksmith | " + PHONE
    desc = f"24/7 mobile locksmith across Miami-Dade: car lockouts, house lockouts, car keys made on-site, rekeying, commercial locks. Up-front pricing. Call {PHONE}."
    body = f"""
<div class="hero"><div class="wrap"><div class="eyebrow">Miami-Dade County · Open 24 Hours</div>
<h1>Miami's locksmith that actually answers at 3&nbsp;AM.</h1>
<p class="lead">Car lockouts, house lockouts, lost car keys, rekeying, commercial locks — mobile technicians across Miami-Dade, around the clock, with the price agreed before the work starts.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a><a class="btn ghost" href="/services/">Explore services</a></div>
<div class="sub">Live dispatch 24/7 · Damage-free methods first · Cars · Homes · Businesses</div></div></div>
<section><div class="wrap"><div class="deco-div"><span></span><i></i><span></span></div>
<h2 class="fxblk">What we do</h2><p class="sec-intro fxblk">Every truck is a rolling locksmith shop — key machines, programmers, picks and hardware — so most jobs finish in one visit.</p>
<div class="grid c4">{svc_cards}</div>
<p style="margin-top:22px" class="fxblk"><a class="btn ghost" href="/services/">See all 14 services →</a></p></div></section>
<section class="dark"><div class="wrap"><h2 class="fxblk">How a call works</h2><div class="steps prose">
<div class="step fxblk"><span class="n"></span><div><h3>Tell us where you are</h3><p>A live dispatcher — not a machine — takes your location and situation, 24 hours a day.</p></div></div>
<div class="step fxblk"><span class="n"></span><div><h3>Get a real price range</h3><p>You hear an honest range before anyone is dispatched. After-hours rates are stated up front.</p></div></div>
<div class="step fxblk"><span class="n"></span><div><h3>The nearest unit rolls</h3><p>The closest available technician heads your way with the right tools for the job.</p></div></div>
<div class="step fxblk"><span class="n"></span><div><h3>Approve, then we work</h3><p>Exact price confirmed in person before work begins. Job done, tested, and you're on your way.</p></div></div>
</div></div></section>
<section><div class="wrap"><h2 class="fxblk">Serving all of Miami-Dade</h2>
<p class="sec-intro fxblk">From South Beach to Homestead, our mobile units cover the whole county. Find your neighborhood:</p>
<div class="chips fxblk">{area_chips}</div></div></section>
<section class="alt"><div class="wrap">{callout("Locked out right now?","Skip the searching — one call reaches live dispatch and puts a technician on the road.")}</div></section>"""
    return title, desc, "/", body, biz_schema()

def services_index():
    cats = [("auto","Automotive"),("residential","Residential"),("commercial","Commercial"),("emergency","Emergency")]
    secs = ""
    for c, label in cats:
        cards = "".join(f'<div class="card fxblk"><h3>{s[1]}</h3><p>{s[2]}</p><a class="more" href="/{s[0]}/">Details →</a></div>' for s in SERVICES if s[3] == c)
        secs += f'<h2 class="fxblk" style="margin-top:30px">{label}</h2><div class="grid c3">{cards}</div>'
    title = f"Locksmith Services in Miami | {BRAND}"
    desc = f"Every locksmith service we offer in Miami-Dade: automotive, residential, commercial and 24/7 emergency. Up-front pricing. Call {PHONE}."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">Full service menu</div><h1>Locksmith Services in Miami</h1>
<p class="lead">Fourteen services, one number, around the clock.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("Services",None)])}
<section><div class="wrap">{secs}</div></section>
<section class="alt"><div class="wrap">{callout("Not sure what you need?","Describe the problem to dispatch — they'll tell you exactly what it takes and what it costs.")}</div></section>"""
    return title, desc, "/services/", body, biz_schema()

def areas_index():
    hoods = "".join(f'<a href="/locksmith-{a[0]}/">{a[1]}</a>' for a in AREAS if a[2] == "neighborhood")
    cities = "".join(f'<a href="/locksmith-{a[0]}/">{a[1]}</a>' for a in AREAS if a[2] != "neighborhood")
    title = f"Service Areas — Miami-Dade County | {BRAND}"
    desc = f"All the Miami-Dade neighborhoods and cities served by our 24/7 mobile locksmiths — from Miami Beach to Homestead. Call {PHONE}."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">Coverage map</div><h1>Where We Work</h1>
<p class="lead">Mobile locksmiths across the whole of Miami-Dade County — find your area below.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("Service Areas",None)])}
<section><div class="wrap"><h2 class="fxblk">Miami neighborhoods</h2><div class="chips fxblk">{hoods}</div>
<h2 class="fxblk" style="margin-top:34px">Cities &amp; communities</h2><div class="chips fxblk">{cities}</div></div></section>
<section class="alt"><div class="wrap">{callout("Don't see your exact block?","If it's in Miami-Dade, we cover it. Call and tell dispatch where you are.")}</div></section>"""
    return title, desc, "/service-areas/", body, biz_schema()

def about_page():
    title = f"About {BRAND}"
    desc = f"Who we are: a mobile locksmith service covering Miami-Dade County 24/7 — honest pricing, damage-free methods, technicians who know the county. {PHONE}."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">Our story</div><h1>About 24/7 Locksmith Miami</h1>
<p class="lead">A mobile locksmith service built around one idea: answer every call, quote before working, and open things without breaking them.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("About",None)])}
<section><div class="wrap prose"><div class="deco-div"><span></span><i></i><span></span></div>
<p class="fxblk">24/7 Locksmith Miami is part of the 24/7 Locksmith family of services. We're a mobile operation — no storefront to drive to, because the shop comes to you. Every truck carries key-cutting machines, transponder programmers, entry tools and a stock of quality hardware, so the technician who arrives can almost always finish the job on the spot.</p>
<h2 class="fxblk">How we work</h2>
<p class="fxblk">Three rules govern every job. First, the price is agreed before the work starts — a realistic range on the phone, the exact figure confirmed in person. Second, non-destructive methods come first; drilling is a last resort, not a shortcut. Third, we verify authorization before opening anything, because that protects every honest customer we have.</p>
<h2 class="fxblk">Where we work</h2>
<p class="fxblk">All of Miami-Dade County: the beaches, the urban core, the Gables and the Grove, the western suburbs and all the way down to Homestead and Florida City. <a href="/service-areas/">Browse the full coverage list</a> or just call — if it's in the county, we cover it.</p>
<h2 class="fxblk">What we work on</h2>
<p class="fxblk">Cars (lockouts, lost keys, fobs, ignitions), homes (lockouts, rekeying, lock changes, smart locks) and businesses (commercial hardware, high-security cylinders, master key systems, safes). We install trusted brands including Schlage, Kwikset, Yale, Medeco and Mul-T-Lock.</p></div></section>
<section class="alt"><div class="wrap">{callout("Put us in your phone","The moment you need a locksmith is the worst moment to start searching for one.")}</div></section>"""
    return title, desc, "/about/", body, biz_schema()

def contact_page():
    title = f"Contact — {BRAND}"
    desc = f"Reach 24/7 Locksmith Miami any hour: {PHONE}. Live dispatch for all of Miami-Dade County."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">24 hours · 7 days</div><h1>Contact Us</h1>
<p class="lead">One number reaches a live dispatcher, day or night.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("Contact",None)])}
<section><div class="wrap prose"><div class="deco-div"><span></span><i></i><span></span></div>
<h2 class="fxblk">Call — it's the fastest way</h2>
<p class="fxblk">For lockouts and emergencies, calling beats any form: <a href="tel:{PHONE_RAW}"><b>{PHONE}</b></a>. Dispatch answers around the clock, every day of the year, and can usually give you a price range in under two minutes.</p>
<h2 class="fxblk">What to have ready</h2>
<ul class="fxblk"><li>Your location — address or nearest cross-streets</li><li>What happened (lockout, lost keys, broken lock…)</li><li>For vehicles: year, make and model</li><li>A callback number in case the line drops</li></ul>
<h2 class="fxblk">Service area</h2>
<p class="fxblk">All of Miami-Dade County — <a href="/service-areas/">see the full list of neighborhoods and cities</a>.</p></div></section>
<section class="alt"><div class="wrap">{callout("Locked out right now?","Skip the reading — call and a technician starts heading your way.")}</div></section>"""
    return title, desc, "/contact/", body, biz_schema()

def faq_page():
    faqs = [(q.format(area="Miami-Dade", svc_low="locksmith service"), a.format(area="Miami-Dade", svc_low="locksmith service")) for q, a in FAQ_BANK_COMBO]
    faq_html = "".join(f'<details class="fxblk"><summary>{q}</summary><div class="a">{a}</div></details>' for q, a in faqs)
    title = f"Locksmith FAQ | {BRAND}"
    desc = f"Straight answers about pricing, response, ID checks, car keys and rekeying from Miami's 24/7 mobile locksmith. Call {PHONE}."
    body = f"""<div class="hero"><div class="wrap"><div class="eyebrow">Straight answers</div><h1>Frequently Asked Questions</h1>
<p class="lead">Everything people ask before they call — answered honestly.</p>
<div class="cta-row"><a class="btn primary" href="tel:{PHONE_RAW}">Call {PHONE}</a></div></div></div>
{crumbs([("FAQ",None)])}
<section><div class="wrap">{faq_html}</div></section>
<section class="alt"><div class="wrap">{callout("Question not here?","Dispatch answers 24/7 — ask a human instead.")}</div></section>"""
    return title, desc, "/faq/", body, biz_schema() + faq_schema(faqs)

# ---------------- Writer ----------------
def write(path, content):
    fs = os.path.join(OUT, path.strip("/"))
    if path.endswith("/") or path == "/":
        fs = os.path.join(fs, "index.html")
    os.makedirs(os.path.dirname(fs), exist_ok=True)
    with open(fs, "w") as f:
        f.write(content)

def main():
    pages = []
    for gen in (home_page, services_index, areas_index, about_page, contact_page, faq_page):
        t, d, p, b, sc = gen()
        write(p, shell(t, d, p, b, sc)); pages.append(p)
    for s in SERVICES:
        t, d, p, b, sc = service_page(s)
        write(p, shell(t, d, p, b, sc)); pages.append(p)
    for a in AREAS:
        t, d, p, b, sc = area_page(a)
        write(p, shell(t, d, p, b, sc)); pages.append(p)
    for svc in COMBO_SERVICES:
        for a in AREAS:
            t, d, p, b, sc = combo_page(svc, a)
            write(p, shell(t, d, p, b, sc)); pages.append(p)
    # favicon
    fav = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 44"><rect width="44" height="44" rx="9" fill="#17bebb"/><path d="M22 6l12 7v18l-12 7-12-7V13z" fill="#0c1626"/><circle cx="22" cy="19" r="5.2" fill="none" stroke="#e8b04b" stroke-width="2.4"/><rect x="20.7" y="23" width="2.6" height="9" rx="1.3" fill="#e8b04b"/><rect x="23.3" y="27" width="3.6" height="2.3" rx="1" fill="#e8b04b"/><rect x="23.3" y="30.4" width="2.6" height="2.3" rx="1" fill="#ff6f61"/></svg>"""
    with open(os.path.join(OUT, "favicon.svg"), "w") as f: f.write(fav)
    # robots + sitemap
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{DOMAIN}{p}</loc></url>" for p in pages)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    print(f"Built {len(pages)} pages")

if __name__ == "__main__":
    main()
