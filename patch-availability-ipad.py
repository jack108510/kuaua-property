"""Apply the iPad calendar layout and touch fix to the retained build."""

from pathlib import Path

root = Path(__file__).parent
source = root / "assets/index-booking-sync-20261011.js"
target = root / "assets/index-availability-ipad-20261011.js"
bundle = source.read_text()


def replace_once(old: str, new: str) -> None:
    global bundle
    count = bundle.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match, found {count}: {old[:100]}")
    bundle = bundle.replace(old, new, 1)


replace_once(
    'onMouseEnter:()=>u(k),onMouseLeave:()=>u(null)',
    'onPointerEnter:re=>re.pointerType==="mouse"&&u(k),onPointerLeave:re=>re.pointerType==="mouse"&&u(null),onTouchStart:()=>u(null)',
)
replace_once(
    'className:"grid grid-cols-7",children:[Array.from({length:m})',
    'className:"grid grid-cols-7 wm-calendar-days",children:[Array.from({length:m})',
)
replace_once(
    'className:"grid md:grid-cols-2 gap-0"',
    'className:"grid wm-calendar-months"',
)
replace_once(
    'className:"p-6 md:border-r border-[oklch(0.92_0.02_80)]"',
    'className:"p-6 wm-calendar-first"',
)
target.write_text(bundle)

old_src = "/assets/index-booking-sync-20261011.js"
new_src = "/assets/index-availability-ipad-20261011.js"
stylesheet = '    <link rel="stylesheet" href="/assets/availability-ipad-20261011.css">\n'
for page_path in (root / "index.html", root / "404.html"):
    page = page_path.read_text()
    if page.count(old_src) != 1:
        raise RuntimeError(f"Expected one bundle reference in {page_path.name}")
    page = page.replace(old_src, new_src, 1)
    marker = '    <link rel="stylesheet" crossorigin href="/assets/index-sGUr-kiU.css">\n'
    if page.count(marker) != 1:
        raise RuntimeError(f"Expected one stylesheet reference in {page_path.name}")
    page_path.write_text(page.replace(marker, marker + stylesheet, 1))
