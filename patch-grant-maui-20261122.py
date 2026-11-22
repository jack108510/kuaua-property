"""Grant Maui update, 2026-11-22: new photos, Ohana/TV section order, AC + checkout.

The React source is not retained in this repository, so the live bundle is
patched with exact replacements, following patch-site-copy-20261025.py and
patch-booking-flow.py. A new bundle is created; the old bundle is untouched.

Photos (all in manus-storage/, copied before running this script):
  Direct replacements, same filename, so the Ra image map needs no change:
    photo_1.jpg            <- Open Lanai (FEF18A67)
    kitchen-2026.jpg       <- Kitchen (FE15C657)
    living-room-2026.jpg   <- Living Room (BEDC22D7)
    sitting-room-2026.jpg  <- TV Room (47C4690E)
    west-guest-room-2026.jpg <- West Guest Room (ED4344C3)
    photo_42.jpg           <- Ohana Living Room (0887E2CE)
  New files:
    guest-bedroom-2-2026.jpg <- Guest Room 2 (BEF2335D)
    murphy-bed-2026.jpg      <- Murphy Bed (FE8635D2)
    dining-sunset-2026.jpg   <- Dining Room Sunset (3D30313E)
    outdoor-kitchen-2026.jpg <- Outdoor Kitchen (36E05981)
    ohana-bedroom-2026.jpg   <- Ohana Bedroom (9FECFCE4)
    ohana-bedroom-2-2026.jpg <- Ohana 2nd Bedroom, cropped from iMessage
        screenshot B76F1E0A (twin beds, bounds x58-725 y1555-2045 in the
        1125x2436 screenshot); 667x490, the only source for that photo.
    pool-breakfast-2026.jpg  <- Breakfast by the Infinity Pool (5F4574E8:
        blueberries + coffee by the pool at dawn)

Bundle changes in assets/index-grant-20261122.js:
  1. Guest Rooms cards (Home.tsx:495): Guest Bedroom 2 and Murphy Bed had
     no image; both now get an image field, same format as West Guest Room.
     The card renders r.image && <img ...>, so the images now display.
     (The shared alt text "West guest room with ocean view" is pre-existing
     and still applies to all three cards.)
  2. Gallery v6: Blank Slots 8, 9, 11, 12 filled (Dining Room Sunset,
     Outdoor Kitchen, Ohana Bedroom, Ohana 2nd Bedroom), plus a 17th entry
     appended after Aerial View: Breakfast by the Infinity Pool. The gallery
     renders with CSS masonry columns (columns-2 md:columns-3) and skips
     null srcs, so a 17th entry flows in without breaking the layout.
  3. Section order: the whole Ohana section (Home.tsx:562, id "ohana") and
     the whole TV Room section (Home.tsx:599) are swapped with balanced-
     delimiter parsing, so TV Room now comes first, Ohana second.
  4. Air Conditioning (Home.tsx:661 accordion): added "Typical set point:
     77°F during the day, 74°F at night." The House Rules FAQ (HouseRules.tsx)
     previously said "A/C is set at 75°F ... 73°F works best for sleeping";
     that is reconciled to Grant's 77/74 as well.
  5. Checkout drawer: "Set all 3 thermostats to 78°F." becomes
     "Set all 3 thermostats in the house and 1 in Ohana to 80°F."
"""
from pathlib import Path

root = Path(__file__).parent
old_name = "index-private-retreat-20261025.js"
new_name = "index-grant-20261122.js"
source = root / "assets" / old_name
target = root / "assets" / new_name

bundle = source.read_text()


def replace_once(old: str, new: str) -> None:
    global bundle
    count = bundle.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match, found {count}: {old[:100]}")
    bundle = bundle.replace(old, new, 1)


# --- 1. Guest Rooms cards: add images to Guest Bedroom 2 and Murphy Bed ---
replace_once(
    '{title:"Guest Bedroom 2",desc:"Comfortable and private, with easy access to the pool-side guest shower."}',
    '{title:"Guest Bedroom 2",desc:"Comfortable and private, with easy access to the pool-side guest shower.",image:"/manus-storage/guest-bedroom-2-2026.jpg"}',
)
replace_once(
    '{title:"Murphy Bed",desc:"Queen-size Murphy bed for extra sleeping space. Flexible and comfortable."}',
    '{title:"Murphy Bed",desc:"Queen-size Murphy bed for extra sleeping space. Flexible and comfortable.",image:"/manus-storage/murphy-bed-2026.jpg"}',
)

# --- 2. Gallery v6: fill the four blank slots, append the breakfast photo ---
replace_once(
    '{src:null,label:"Blank Slot 8"}',
    '{src:"/manus-storage/dining-sunset-2026.jpg",label:"Dining Room Sunset"}',
)
replace_once(
    '{src:null,label:"Blank Slot 9"}',
    '{src:"/manus-storage/outdoor-kitchen-2026.jpg",label:"Outdoor Kitchen"}',
)
replace_once(
    '{src:null,label:"Blank Slot 11"}',
    '{src:"/manus-storage/ohana-bedroom-2026.jpg",label:"Ohana Bedroom"}',
)
replace_once(
    '{src:null,label:"Blank Slot 12"}',
    '{src:"/manus-storage/ohana-bedroom-2-2026.jpg",label:"Ohana 2nd Bedroom"}',
)
replace_once(
    '{src:"/manus-storage/photo_6.jpg",label:"Aerial View"}];',
    '{src:"/manus-storage/photo_6.jpg",label:"Aerial View"},{src:"/manus-storage/pool-breakfast-2026.jpg",label:"Breakfast by the Infinity Pool"}];',
)


def find_call_end(s: str, call_start: int) -> int:
    """Return the index just past the matching ')' of the y.jsx( call at call_start.

    String-aware scan: single/double-quoted strings (with backslash escapes)
    and regex literals are skipped so their brackets do not affect the depth
    count. The Ohana/TV region contains no template literals (verified).
    """
    i = s.index("(", call_start)
    depth = 0
    j = i
    n = len(s)
    while j < n:
        c = s[j]
        if c in "\"'":
            q = c
            j += 1
            while j < n:
                if s[j] == "\\":
                    j += 2
                    continue
                if s[j] == q:
                    j += 1
                    break
                j += 1
            continue
        if c == "`":
            raise RuntimeError("unexpected template literal in section region")
        if c == "/":
            k = j - 1
            while k >= 0 and s[k] in " \t\n":
                k -= 1
            prev = s[k] if k >= 0 else ""
            if prev in "=(:,[!&|?{};<>+-*%~^" or prev == "":
                j += 1
                in_class = False
                while j < n:
                    if s[j] == "\\":
                        j += 2
                        continue
                    if s[j] == "[":
                        in_class = True
                    elif s[j] == "]":
                        in_class = False
                    elif s[j] == "/" and not in_class:
                        j += 1
                        while j < n and s[j].isalpha():
                            j += 1
                        break
                    j += 1
                continue
        if c in "({[":
            depth += 1
        elif c in ")}]":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    raise RuntimeError("unbalanced delimiters in section call")


# --- 3. Swap the Ohana and TV Room sections ---
ohana_marker = 'y.jsx("section",{"data-loc":"client/src/pages/Home.tsx:562",id:"ohana"'
tv_marker = 'y.jsx("section",{"data-loc":"client/src/pages/Home.tsx:599"'
guide_marker = 'y.jsx("section",{"data-loc":"client/src/pages/Home.tsx:635"'
ohana_start = bundle.index(ohana_marker)
tv_start = bundle.index(tv_marker)
guide_start = bundle.index(guide_marker)
if not ohana_start < tv_start < guide_start:
    raise RuntimeError("section order is not Ohana, TV Room, House Guide as expected")
ohana_end = find_call_end(bundle, ohana_start)
tv_end = find_call_end(bundle, tv_start)
ohana_block = bundle[ohana_start:ohana_end]
tv_block = bundle[tv_start:tv_end]
if 'children:"Ohana"' not in ohana_block or 'id:"ohana"' not in ohana_block:
    raise RuntimeError("extracted Ohana block does not look like the Ohana section")
if 'children:"TV Room"' not in tv_block:
    raise RuntimeError("extracted TV Room block does not look like the TV Room section")
if bundle[ohana_end] != "," or bundle[tv_end] != ",":
    raise RuntimeError("expected a comma separator after each swapped section")
if tv_end != guide_start - 1:
    raise RuntimeError("TV Room block does not end immediately before the House Guide section")
bundle = (
    bundle[:ohana_start]
    + tv_block
    + bundle[ohana_end:tv_start]
    + ohana_block
    + bundle[tv_end:]
)

# --- 4. Air Conditioning: House Guide accordion + House Rules FAQ ---
replace_once(
    ']}),y.jsx("p",{"data-loc":"client/src/pages/Home.tsx:669"',
    ']}),y.jsx("p",{className:"mt-3",children:"Typical set point: 77°F during the day, 74°F at night."}),y.jsx("p",{"data-loc":"client/src/pages/Home.tsx:669"',
)
replace_once(
    'body:"A/C is set at 75°F. Controls are located near the wine cooler and in spare bedroom #1. We find 73°F works best for sleeping, but adjust to your comfort level."',
    'body:"Typical set point is 77°F during the day and 74°F at night. Controls are located near the wine cooler and in spare bedroom #1. Adjust to your comfort level."',
)

# --- 5. Checkout drawer thermostat line ---
replace_once(
    '"Set all 3 thermostats to 78°F."',
    '"Set all 3 thermostats in the house and 1 in Ohana to 80°F."',
)

target.write_text(bundle)

old_src = f"/assets/{old_name}"
new_src = f"/assets/{new_name}"
for page in (root / "index.html", root / "404.html", root / "admin/index.html"):
    html = page.read_text()
    if html.count(old_src) != 1:
        raise RuntimeError(f"Expected exactly one active bundle reference in {page}")
    page.write_text(html.replace(old_src, new_src, 1))

print(f"Wrote {target} and updated bundle references in index.html, 404.html, admin/index.html")
