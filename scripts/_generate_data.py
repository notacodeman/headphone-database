#!/usr/bin/env python3
"""One-off generator: builds the expanded CSVs from researched headphone data."""
import csv
from pathlib import Path

OUT = Path("database")

# ---------------------------------------------------------------------------
# Manufacturers
# ---------------------------------------------------------------------------
manufacturers = [
    # id, name, country, website, status
    (1,  "Sony",             "Japan",       "https://www.sony.com",            "Active"),
    (2,  "Sennheiser",       "Germany",     "https://www.sennheiser.com",      "Active"),
    (3,  "Philips",          "Netherlands", "https://www.philips.com",         "Active"),
    (4,  "Audio-Technica",   "Japan",       "https://www.audio-technica.com",  "Active"),
    (5,  "AKG",              "Austria",     "https://www.akg.com",             "Active"),
    (6,  "Beyerdynamic",     "Germany",     "https://www.beyerdynamic.com",    "Active"),
    (7,  "Bose",             "USA",         "https://www.bose.com",            "Active"),
    (8,  "Audeze",           "USA",         "https://www.audeze.com",          "Active"),
    (9,  "HiFiMan",          "China",       "https://www.hifiman.com",         "Active"),
    (10, "Focal",            "France",      "https://www.focal.com",           "Active"),
    (11, "Bowers & Wilkins", "UK",          "https://www.bowerswilkins.com",   "Active"),
    (12, "Grado",            "USA",         "https://gradolabs.com",           "Active"),
    (13, "Meze Audio",       "Romania",     "https://mezeaudio.com",           "Active"),
    (14, "Dan Clark Audio",  "USA",         "https://danclarkaudio.com",       "Active"),
    (15, "Apple",            "USA",         "https://www.apple.com",           "Active"),
    (16, "Beats",            "USA",         "https://www.beatsbydre.com",      "Active"),
    (17, "Shure",            "USA",         "https://www.shure.com",           "Active"),
    # Gaming
    (18, "SteelSeries",      "Denmark",     "https://steelseries.com",         "Active"),
    (19, "HyperX",           "USA",         "https://www.hyperx.com",          "Active"),
    (20, "Razer",            "USA",         "https://www.razer.com",           "Active"),
    (21, "Logitech G",       "Switzerland", "https://www.logitechg.com",       "Active"),
    (22, "Astro Gaming",     "USA",         "https://www.astro.com",           "Active"),
    (23, "Turtle Beach",     "USA",         "https://www.turtlebeach.com",     "Active"),
    (24, "Corsair",          "USA",         "https://www.corsair.com",         "Active"),
    (25, "ASUS ROG",         "Taiwan",      "https://rog.asus.com",            "Active"),
    # High-end / niche audiophile
    (26, "Abyss",            "USA",         "https://abyss-headphones.com",    "Active"),
    (27, "ZMF Headphones",   "USA",         "https://www.zmfheadphones.com",   "Active"),
    (28, "Stax",             "Japan",       "https://stax.co.jp",              "Active"),
    (29, "Final Audio",      "Japan",       "https://final-inc.com",           "Active"),
    (30, "Fostex",           "Japan",       "https://www.fostex.jp",           "Active"),
    (31, "Denon",            "Japan",       "https://www.denon.com",           "Active"),
    (32, "Rosson Audio",     "USA",         "https://rossonaudiodesign.com",   "Active"),
    (33, "Kennerton",        "Russia",      "https://kennerton.com",           "Active"),
    (34, "Ultrasone",        "Germany",     "https://www.ultrasone.com",       "Active"),
    # Consumer / mainstream
    (35, "Bang & Olufsen",   "Denmark",     "https://www.bang-olufsen.com",    "Active"),
    (36, "Sonos",            "USA",         "https://www.sonos.com",           "Active"),
    (37, "Marshall",         "UK",          "https://www.marshallheadphones.com","Active"),
    (38, "JBL",              "USA",         "https://www.jbl.com",             "Active"),
    (39, "Skullcandy",       "USA",         "https://www.skullcandy.com",      "Active"),
    (40, "Anker Soundcore",  "China",       "https://www.soundcore.com",       "Active"),
    (41, "Technics",         "Japan",       "https://www.technics.com",        "Active"),
    (42, "Nothing",          "UK",          "https://nothing.tech",            "Active"),
    # New brands — mainstream / popular
    (43, "Koss",             "USA",         "https://www.koss.com",            "Active"),
    (44, "V-Moda",           "USA",         "https://www.v-moda.com",          "Active"),
    (45, "Yamaha",           "Japan",       "https://www.yamaha.com",          "Active"),
    (46, "Pioneer",          "Japan",       "https://www.pioneer-audiovisual.com","Active"),
    (47, "AIAIAI",           "Denmark",     "https://www.aiaiai.audio",        "Active"),
    (48, "1More",            "China",       "https://www.1more.com",           "Active"),
    (49, "Edifier",          "China",       "https://www.edifier.com",         "Active"),
    (50, "Cleer",            "USA",         "https://www.cleeraudio.com",      "Active"),
    # New brands — audiophile / boutique
    (51, "Austrian Audio",   "Austria",     "https://austrian.audio",          "Active"),
    (52, "Neumann",          "Germany",     "https://www.neumann.com",         "Active"),
    (53, "Moondrop",         "China",       "https://moondroplab.com",         "Active"),
    (54, "Sivga",            "China",       "https://www.sivgaaudio.com",      "Active"),
    (55, "Sendy Audio",      "China",       "https://www.sendyaudio.com",      "Active"),
    (56, "FiiO",             "China",       "https://www.fiio.com",            "Active"),
    (57, "Spirit Torino",    "Italy",       "https://www.spirittorino.com",    "Active"),
    (58, "Warwick Acoustics","UK",          "https://warwickacoustics.com",    "Active"),
    (59, "Mark Levinson",    "USA",         "https://www.marklevinson.com",    "Active"),
    (60, "T+A",              "Germany",     "https://www.ta-hifi.com",         "Active"),
    (61, "HEDD Audio",       "Germany",     "https://hedd.audio",              "Active"),
    (62, "Grell Audio",      "Germany",     "https://grell-audio.com",         "Active"),
    (63, "Ollo Audio",       "Slovenia",    "https://www.olloaudio.com",       "Active"),
    # New brands — value / budget
    (64, "Monoprice",       "USA",         "https://www.monoprice.com",       "Active"),
    (65, "Superlux",        "Taiwan",      "https://www.superlux.com",        "Active"),
    (66, "Samson",          "USA",         "https://samsontech.com",          "Active"),
    (67, "Status Audio",    "USA",         "https://status.co",               "Active"),
    # Office / professional
    (68, "Jabra",           "Denmark",     "https://www.jabra.com",           "Active"),
    # Consumer premium
    (69, "Harman Kardon",  "USA",         "https://www.harmankardon.com",    "Active"),
    # New brands from OPRA cross-reference
    (70, "Oppo",           "USA",         "https://www.oppodigital.com",     "Discontinued"),
    (71, "Creative",       "Singapore",   "https://us.creative.com",         "Active"),
    (72, "Rode",           "Australia",   "https://rode.com",                "Active"),
    (73, "Klipsch",        "USA",         "https://www.klipsch.com",         "Active"),
    (74, "RAAL",           "USA",         "https://raalrequisite.com",       "Active"),
    # More from OPRA gap-fill
    (75, "HarmonicDyne",   "China",       "https://harmonicdyne.com",        "Active"),
    (76, "PSB",            "Canada",      "https://www.psbspeakers.com",     "Active"),
    (77, "E-Mu",           "USA",         "https://us.creative.com",         "Discontinued"),
    # From spreadsheet verified additions
    (78, "Audioquest",     "USA",         "https://www.audioquest.com",      "Active"),
    (79, "NAD",            "Canada",      "https://nadelectronics.com",      "Active"),
    (80, "Brainwavz",      "China",       "https://www.brainwavzaudio.com",  "Active"),
    # From OPRA gap-fill round 3
    (81, "Modhouse Audio", "USA",         "https://modhouse.io",             "Active"),
    (82, "Kiwi Ears",      "China",       "https://www.kiwiears.com",        "Active"),
    (83, "Plantronics",    "USA",         "https://www.poly.com",            "Active"),
    (84, "Phiaton",        "South Korea", "https://www.phiaton.com",         "Active"),
    (85, "Teufel",         "Germany",     "https://www.teufel.de",           "Active"),
    (86, "House of Marley","USA",         "https://www.thehouseofmarley.com","Active"),
    (87, "Cooler Master",  "Taiwan",      "https://www.coolermaster.com",    "Active"),
    # Fresh additions — notable brands not in OPRA
    (88, "JVC",            "Japan",       "https://www.jvc.com",             "Active"),
    (89, "Tago Studio",    "Japan",       "https://tagostudio.com",          "Active"),
    (90, "Takstar",        "China",       "https://www.takstar.com",         "Active"),
    (91, "Goldplanar",     "China",       "https://goldplanar.com",          "Active"),
    (92, "MySphere",       "Austria",     "https://mysphere.at",             "Active"),
    (93, "Panasonic",      "Japan",       "https://www.panasonic.com",       "Active"),
    (94, "Crosszone",      "Japan",       "https://crosszone.jp",            "Active"),
]
mfr_id = {name: i for i, name, *_ in manufacturers}

# ---------------------------------------------------------------------------
# Families  (family_id, manufacturer, family_name, family_type)
# ---------------------------------------------------------------------------
families_raw = [
    ("Sony", "WH", "Headphone"),
    ("Sony", "MDR", "Headphone"),
    ("Sony", "ULT", "Headphone"),
    ("Sennheiser", "HD", "Headphone"),
    ("Sennheiser", "Momentum", "Headphone"),
    ("Sennheiser", "HDB", "Headphone"),
    ("Sennheiser", "Accentum", "Headphone"),
    ("Philips", "Fidelio", "Headphone"),
    ("Philips", "SHP", "Headphone"),
    ("Audio-Technica", "M-Series", "Studio"),
    ("Audio-Technica", "R-Series", "Studio"),
    ("Audio-Technica", "A-Series", "Headphone"),
    ("Audio-Technica", "W-Series", "Headphone"),
    ("Audio-Technica", "MSR", "Headphone"),
    ("AKG", "K-Series", "Headphone"),
    ("AKG", "N-Series", "Headphone"),
    ("Beyerdynamic", "DT", "Studio"),
    ("Beyerdynamic", "T-Series", "Headphone"),
    ("Beyerdynamic", "Amiron", "Headphone"),
    ("Beyerdynamic", "MMX", "Gaming"),
    ("Bose", "QuietComfort", "Headphone"),
    ("Bose", "700", "Headphone"),
    ("Audeze", "LCD", "Headphone"),
    ("Audeze", "MM", "Studio"),
    ("Audeze", "Maxwell", "Gaming"),
    ("Audeze", "CRBN", "Headphone"),
    ("HiFiMan", "HE", "Headphone"),
    ("HiFiMan", "Edition", "Headphone"),
    ("HiFiMan", "Ananda", "Headphone"),
    ("HiFiMan", "Arya", "Headphone"),
    ("HiFiMan", "Susvara", "Headphone"),
    ("HiFiMan", "Sundara", "Headphone"),
    ("HiFiMan", "Deva", "Headphone"),
    ("Focal", "Utopia", "Headphone"),
    ("Focal", "Clear", "Headphone"),
    ("Focal", "Elegia", "Headphone"),
    ("Focal", "Bathys", "Headphone"),
    ("Focal", "Listen", "Headphone"),
    ("Bowers & Wilkins", "P-Series", "Headphone"),
    ("Bowers & Wilkins", "PX", "Headphone"),
    ("Grado", "Prestige", "Headphone"),
    ("Grado", "Reference", "Headphone"),
    ("Grado", "Statement", "Headphone"),
    ("Grado", "GW", "Headphone"),
    ("Meze Audio", "Classics", "Headphone"),
    ("Meze Audio", "Flagship", "Headphone"),
    ("Dan Clark Audio", "Aeon", "Headphone"),
    ("Dan Clark Audio", "Ether", "Headphone"),
    ("Dan Clark Audio", "Flagship", "Headphone"),
    ("Apple", "AirPods Max", "Headphone"),
    ("Beats", "Studio", "Headphone"),
    ("Beats", "Solo", "Headphone"),
    ("Shure", "SRH", "Studio"),
    ("Shure", "AONIC", "Headphone"),
    # Gaming
    ("SteelSeries", "Arctis Nova", "Gaming"),
    ("SteelSeries", "Arctis", "Gaming"),
    ("HyperX", "Cloud", "Gaming"),
    ("Razer", "BlackShark", "Gaming"),
    ("Razer", "Kraken", "Gaming"),
    ("Logitech G", "G Pro", "Gaming"),
    ("Logitech G", "G", "Gaming"),
    ("Astro Gaming", "A-Series", "Gaming"),
    ("Turtle Beach", "Stealth", "Gaming"),
    ("Corsair", "Virtuoso", "Gaming"),
    ("Corsair", "HS", "Gaming"),
    ("ASUS ROG", "Delta", "Gaming"),
    # High-end / niche
    ("Abyss", "AB-1266", "Headphone"),
    ("Abyss", "Diana", "Headphone"),
    ("ZMF Headphones", "Verite", "Headphone"),
    ("ZMF Headphones", "Auteur", "Headphone"),
    ("ZMF Headphones", "Atrium", "Headphone"),
    ("ZMF Headphones", "Caldera", "Headphone"),
    ("Stax", "SR", "Headphone"),
    ("Final Audio", "D-Series", "Headphone"),
    ("Fostex", "TH", "Headphone"),
    ("Denon", "AH-D", "Headphone"),
    ("Rosson Audio", "RAD", "Headphone"),
    ("Kennerton", "Flagship", "Headphone"),
    ("Ultrasone", "Edition", "Headphone"),
    # Consumer
    ("Bang & Olufsen", "Beoplay", "Headphone"),
    ("Sonos", "Ace", "Headphone"),
    ("Marshall", "Monitor", "Headphone"),
    ("JBL", "Tour", "Headphone"),
    ("JBL", "Live", "Headphone"),
    ("Skullcandy", "Crusher", "Headphone"),
    ("Anker Soundcore", "Space", "Headphone"),
    ("Technics", "EAH", "Headphone"),
    ("Nothing", "Headphone", "Headphone"),
    # Deep-dive additions
    ("Sennheiser", "HD 500-series", "Headphone"),
    ("Sennheiser", "PXC", "Headphone"),
    ("Sony", "MDR Studio", "Studio"),
    ("Sony", "ZX", "Headphone"),
    ("Sony", "XB", "Headphone"),
    ("Sony", "CH", "Headphone"),
    ("Audio-Technica", "ART Monitor", "Headphone"),
    ("Audio-Technica", "SR/BT", "Headphone"),
    ("AKG", "K-Studio", "Studio"),
    ("Beyerdynamic", "Custom", "Headphone"),
    ("Bose", "AE/SoundLink", "Headphone"),
    ("Bose", "QuietComfort On-Ear", "Headphone"),
    # Deepening batch 2
    ("Focal", "Spirit", "Studio"),
    ("Grado", "Statement-PS", "Headphone"),
    ("Razer", "Barracuda", "Gaming"),
    ("Logitech G", "Astro", "Gaming"),
    ("Bang & Olufsen", "Beoplay Portal", "Gaming"),
    ("JBL", "Quantum", "Gaming"),
    # Deepening batch 3
    ("Beats", "Pro", "Headphone"),
    ("Beats", "Executive", "Headphone"),
    ("JBL", "Everest", "Headphone"),
    ("JBL", "Tune", "Headphone"),
    ("Skullcandy", "Hesh", "Headphone"),
    ("Sony", "h.ear", "Headphone"),
    ("Marshall", "Major", "Headphone"),
    # Pre-2010 legacy families
    ("Sennheiser", "HD Classic", "Headphone"),
    ("Sennheiser", "HD 200-series", "Studio"),
    ("Sony", "Qualia/SA", "Headphone"),
    ("AKG", "K-Reference", "Headphone"),
    ("Audio-Technica", "ESW/ES", "Headphone"),
    ("Grado", "Vintage", "Headphone"),
    ("Bose", "TriPort/QC Legacy", "Headphone"),
    ("Beyerdynamic", "DT Classic", "Headphone"),
    # Complete-the-brands batch
    ("Shure", "SRH-DJ", "Studio"),
    ("ZMF Headphones", "Eikon", "Headphone"),
    ("ZMF Headphones", "Atticus", "Headphone"),
    ("ZMF Headphones", "Bokeh", "Headphone"),
    ("Stax", "Lambda", "Headphone"),
    ("Final Audio", "Sonorous", "Headphone"),
    ("Sony", "MA", "Headphone"),
    ("Abyss", "Diana TC", "Headphone"),
    # New brand families
    ("Koss", "Porta Pro", "Headphone"),
    ("Koss", "KSC", "Headphone"),
    ("Koss", "Pro", "Studio"),
    ("V-Moda", "Crossfade", "Headphone"),
    ("V-Moda", "M-200", "Studio"),
    ("Yamaha", "HPH", "Headphone"),
    ("Yamaha", "YH", "Headphone"),
    ("Pioneer", "SE-Monitor", "Headphone"),
    ("Pioneer", "HDJ", "Studio"),
    ("AIAIAI", "TMA", "Studio"),
    ("1More", "SonoFlow", "Headphone"),
    ("Edifier", "STAX Spirit", "Headphone"),
    ("Edifier", "WH", "Headphone"),
    ("Cleer", "Flow/Enduro", "Headphone"),
    ("Austrian Audio", "Hi-X", "Studio"),
    ("Neumann", "NDH", "Studio"),
    ("Moondrop", "Planar", "Headphone"),
    ("Sivga", "Open", "Headphone"),
    ("Sendy Audio", "Flagship", "Headphone"),
    ("FiiO", "FT", "Headphone"),
    ("Spirit Torino", "Flagship", "Headphone"),
    ("Warwick Acoustics", "Sonoma", "Headphone"),
    ("Mark Levinson", "No. 5909", "Headphone"),
    ("T+A", "Solitaire", "Headphone"),
    # Newest makers + 2025-2026 model lines
    ("HEDD Audio", "HEDDphone", "Studio"),
    ("Grell Audio", "OAE", "Headphone"),
    ("Ollo Audio", "S-Series", "Studio"),
    ("Ollo Audio", "X-Series", "Studio"),
    ("Moondrop", "Wireless", "Headphone"),
    ("Moondrop", "On-Ear", "Headphone"),
    # New brands
    ("Monoprice", "Monolith", "Headphone"),
    ("Superlux", "HD", "Studio"),
    ("Samson", "SR", "Studio"),
    ("Status Audio", "CB", "Studio"),
    ("Status Audio", "BT", "Headphone"),
    ("Jabra", "Evolve2", "Headphone"),
    ("Harman Kardon", "FLY", "Headphone"),
    ("Harman Kardon", "SOHO", "Headphone"),
    ("Oppo", "PM", "Headphone"),
    ("Creative", "Aurvana", "Headphone"),
    ("Rode", "NTH", "Studio"),
    ("Klipsch", "Heritage", "Headphone"),
    ("Klipsch", "Reference", "Headphone"),
    ("RAAL", "Ribbon", "Headphone"),
    ("HarmonicDyne", "Dynamic", "Headphone"),
    ("HarmonicDyne", "Planar", "Headphone"),
    ("PSB", "M4U", "Headphone"),
    ("E-Mu", "Wood", "Headphone"),
    ("Audioquest", "NightHawk", "Headphone"),
    ("Audioquest", "NightOwl", "Headphone"),
    ("NAD", "VISO", "Headphone"),
    ("Brainwavz", "HM", "Studio"),
    ("Modhouse Audio", "Argon", "Headphone"),
    ("Modhouse Audio", "Tungsten", "Headphone"),
    ("Kiwi Ears", "Planar", "Headphone"),
    ("Plantronics", "BackBeat", "Headphone"),
    ("Phiaton", "Chord", "Headphone"),
    ("Phiaton", "Bridge", "Headphone"),
    ("Teufel", "Real", "Headphone"),
    ("House of Marley", "Positive", "Headphone"),
    ("Cooler Master", "MH", "Headphone"),
    ("JVC", "HA", "Headphone"),
    ("Tago Studio", "T3", "Studio"),
    ("Takstar", "Pro", "Studio"),
    ("Takstar", "HF", "Headphone"),
    ("Goldplanar", "GL", "Headphone"),
    ("MySphere", "MySphere", "Headphone"),
    ("Panasonic", "RP", "Headphone"),
    ("Crosszone", "CZ", "Headphone"),
]
families = []
fam_id = {}
for i, (mfr, fname, ftype) in enumerate(families_raw, start=1):
    families.append((i, mfr_id[mfr], fname, ftype))
    fam_id[(mfr, fname)] = i

# ---------------------------------------------------------------------------
# Products
# fields: product_id, mfr, family, model_name, full_name, year, disc_year,
#         status, category, design, driver, wireless, anc, pred, succ, notes
# ---------------------------------------------------------------------------
P = []
# ---------------------------------------------------------------------------
# Valid values for categorical fields — enforced at generation time.
# Any add() call with an invalid value will raise immediately.
# ---------------------------------------------------------------------------
VALID_DESIGN   = {"Open Back", "Closed Back", "Semi-Open"}
VALID_DRIVER   = {"Dynamic", "Planar Magnetic", "Electrostatic", "Ribbon", "AMT", "Hybrid"}
VALID_STATUS   = {"Active", "Discontinued", "Legacy Active"}
VALID_WIRELESS = {"Yes", "No"}
VALID_CATEGORY = {"Headphone", "Studio", "Gaming"}
VALID_FIT      = {"Over-Ear", "On-Ear"}

def add(pid, mfr, fam, model, full, year, status, design, driver, wireless, anc,
        pred="", succ="", notes="", disc="", category="Headphone",
        driver_size="", impedance="", sensitivity="", date_added="", fit="Over-Ear"):
    # Validate categorical fields — fail loudly, never silently
    assert design   in VALID_DESIGN,   f"{pid}: invalid design={design!r}"
    assert driver   in VALID_DRIVER,   f"{pid}: invalid driver={driver!r}"
    assert status   in VALID_STATUS,   f"{pid}: invalid status={status!r}"
    assert wireless in VALID_WIRELESS, f"{pid}: invalid wireless={wireless!r}"
    assert anc      in VALID_WIRELESS, f"{pid}: invalid anc={anc!r}"
    assert category in VALID_CATEGORY, f"{pid}: invalid category={category!r}"
    assert fit      in VALID_FIT,      f"{pid}: invalid fit={fit!r}"
    P.append([pid, mfr, fam, model, full, year, disc, status, category,
              design, driver, driver_size, impedance, sensitivity,
              wireless, anc, pred, succ, notes, date_added, fit])

# ---- Sony ----
add("SONY_MDR1R","Sony","MDR","MDR-1R","Sony MDR-1R",2012,"Discontinued","Closed Back","Dynamic","No","No",succ="SONY_MDR1A",notes="Premium closed-back")
add("SONY_MDR1A","Sony","MDR","MDR-1A","Sony MDR-1A",2014,"Discontinued","Closed Back","Dynamic","No","No",pred="SONY_MDR1R")
add("SONY_MDRZ7","Sony","MDR","MDR-Z7","Sony MDR-Z7",2014,"Discontinued","Closed Back","Dynamic","No","No",succ="SONY_MDRZ7M2",notes="70mm driver")
add("SONY_MDRZ7M2","Sony","MDR","MDR-Z7M2","Sony MDR-Z7M2",2018,"Active","Closed Back","Dynamic","No","No",pred="SONY_MDRZ7")
add("SONY_MDRZ1R","Sony","MDR","MDR-Z1R","Sony MDR-Z1R",2016,"Active","Closed Back","Dynamic","No","No",notes="Signature Series flagship")
add("SONY_MDR1000X","Sony","WH","MDR-1000X","Sony MDR-1000X",2016,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="SONY_WH1000XM2",notes="First in the 1000X line")
add("SONY_WH1000XM2","Sony","WH","WH-1000XM2","Sony WH-1000XM2",2017,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="SONY_MDR1000X",succ="SONY_WH1000XM3")
add("SONY_WH1000XM3","Sony","WH","WH-1000XM3","Sony WH-1000XM3",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="SONY_WH1000XM2",succ="SONY_WH1000XM4")
add("SONY_WH1000XM4","Sony","WH","WH-1000XM4","Sony WH-1000XM4",2020,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="SONY_WH1000XM3",succ="SONY_WH1000XM5")
add("SONY_WH1000XM5","Sony","WH","WH-1000XM5","Sony WH-1000XM5",2022,"Active","Closed Back","Dynamic","Yes","Yes",pred="SONY_WH1000XM4",succ="SONY_WH1000XM6",notes="Flagship ANC")
add("SONY_WH1000XM6","Sony","WH","WH-1000XM6","Sony WH-1000XM6",2025,"Active","Closed Back","Dynamic","Yes","Yes",pred="SONY_WH1000XM5",notes="Foldable redesign, QN3 processor")
add("SONY_WHH900N","Sony","WH","WH-H900N","Sony WH-H900N (h.ear on 2)",2017,"Discontinued","Closed Back","Dynamic","Yes","Yes",fit="On-Ear")
add("SONY_ULTWEAR","Sony","ULT","ULT WEAR","Sony ULT WEAR",2024,"Active","Closed Back","Dynamic","Yes","Yes",notes="Bass-focused ANC")

# ---- Sennheiser ----
add("SENN_HD600","Sennheiser","HD","HD 600","Sennheiser HD 600",1997,"Legacy Active","Open Back","Dynamic","No","No",succ="SENN_HD650",notes="Reference open-back, still in production")
add("SENN_HD650","Sennheiser","HD","HD 650","Sennheiser HD 650",2003,"Legacy Active","Open Back","Dynamic","No","No",pred="SENN_HD600",succ="SENN_HD660S")
add("SENN_HD700","Sennheiser","HD","HD 700","Sennheiser HD 700",2012,"Discontinued","Open Back","Dynamic","No","No")
add("SENN_HD800","Sennheiser","HD","HD 800","Sennheiser HD 800",2009,"Legacy Active","Open Back","Dynamic","No","No",succ="SENN_HD800S",notes="56mm ring radiator")
add("SENN_HD800S","Sennheiser","HD","HD 800 S","Sennheiser HD 800 S",2015,"Active","Open Back","Dynamic","No","No",pred="SENN_HD800")
add("SENN_HD820","Sennheiser","HD","HD 820","Sennheiser HD 820",2018,"Active","Closed Back","Dynamic","No","No",notes="Closed-back flagship, glass earcups")
add("SENN_HD660S","Sennheiser","HD","HD 660S","Sennheiser HD 660S",2017,"Discontinued","Open Back","Dynamic","No","No",pred="SENN_HD650",succ="SENN_HD660S2")
add("SENN_HD660S2","Sennheiser","HD","HD 660S2","Sennheiser HD 660S2",2023,"Active","Open Back","Dynamic","No","No",pred="SENN_HD660S")
add("SENN_HD560S","Sennheiser","HD","HD 560S","Sennheiser HD 560S",2020,"Active","Open Back","Dynamic","No","No",notes="Reference value pick")
add("SENN_HD400PRO","Sennheiser","HD","HD 400 Pro","Sennheiser HD 400 Pro",2021,"Active","Open Back","Dynamic","No","No",notes="Budget open-back reference; replaceable earpads")
add("SENN_HD620S","Sennheiser","HD","HD 620S","Sennheiser HD 620S",2024,"Active","Closed Back","Dynamic","No","No",notes="Closed-back addition to 600 line")
add("SENN_HD550","Sennheiser","HD","HD 550","Sennheiser HD 550",2025,"Active","Open Back","Dynamic","No","No")
add("SENN_MOMENTUM","Sennheiser","Momentum","Momentum","Sennheiser Momentum",2013,"Discontinued","Closed Back","Dynamic","No","No",succ="SENN_MOMENTUM2",notes="Original Momentum over-ear",fit="On-Ear")
add("SENN_MOMENTUM2","Sennheiser","Momentum","Momentum 2.0","Sennheiser Momentum 2.0",2015,"Discontinued","Closed Back","Dynamic","No","No",pred="SENN_MOMENTUM",succ="SENN_MOMENTUM3")
add("SENN_MOMENTUM3","Sennheiser","Momentum","Momentum 3 Wireless","Sennheiser Momentum 3 Wireless",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="SENN_MOMENTUM2",succ="SENN_MOMENTUM4")
add("SENN_MOMENTUM4","Sennheiser","Momentum","Momentum 4 Wireless","Sennheiser Momentum 4 Wireless",2022,"Active","Closed Back","Dynamic","Yes","Yes",pred="SENN_MOMENTUM3",succ="SENN_MOMENTUM5")
add("SENN_MOMENTUM5","Sennheiser","Momentum","Momentum 5 Wireless","Sennheiser Momentum 5 Wireless",2024,"Active","Closed Back","Dynamic","Yes","Yes",pred="SENN_MOMENTUM4")
add("SENN_HDB630","Sennheiser","HDB","HDB 630","Sennheiser HDB 630",2025,"Active","Closed Back","Dynamic","Yes","Yes",notes="First wireless model in the audiophile 600 line")
add("SENN_ACCENTUM","Sennheiser","Accentum","Accentum Wireless","Sennheiser Accentum Wireless",2023,"Active","Closed Back","Dynamic","Yes","Yes",succ="SENN_ACCENTUMPLUS")
add("SENN_ACCENTUMPLUS","Sennheiser","Accentum","Accentum Plus","Sennheiser Accentum Plus Wireless",2024,"Active","Closed Back","Dynamic","Yes","Yes",pred="SENN_ACCENTUM")

# ---- Philips ----
add("PHIL_X1","Philips","Fidelio","X1","Philips Fidelio X1",2012,"Discontinued","Open Back","Dynamic","No","No",succ="PHIL_X2")
add("PHIL_X2","Philips","Fidelio","X2","Philips Fidelio X2",2014,"Discontinued","Open Back","Dynamic","No","No",pred="PHIL_X1",succ="PHIL_X2HR")
add("PHIL_X2HR","Philips","Fidelio","X2HR","Philips Fidelio X2HR",2017,"Active","Open Back","Dynamic","No","No",pred="PHIL_X2",succ="PHIL_X3",notes="Popular open-back value pick")
add("PHIL_X3","Philips","Fidelio","X3","Philips Fidelio X3",2020,"Active","Open Back","Dynamic","No","No",pred="PHIL_X2HR")
add("PHIL_L2","Philips","Fidelio","L2","Philips Fidelio L2",2013,"Discontinued","Open Back","Dynamic","No","No",succ="PHIL_L3")
add("PHIL_L3","Philips","Fidelio","L3","Philips Fidelio L3",2021,"Active","Closed Back","Dynamic","Yes","Yes",pred="PHIL_L2")
add("PHIL_SHP9500","Philips","SHP","SHP9500","Philips SHP9500",2014,"Active","Open Back","Dynamic","No","No",notes="Budget open-back favorite")

# ---- Audio-Technica ----
add("ATECH_M40X","Audio-Technica","M-Series","ATH-M40x","Audio-Technica ATH-M40x",2014,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("ATECH_M50X","Audio-Technica","M-Series","ATH-M50x","Audio-Technica ATH-M50x",2014,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Best-selling studio monitor")
add("ATECH_M60X","Audio-Technica","M-Series","ATH-M60x","Audio-Technica ATH-M60x",2019,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("ATECH_M70X","Audio-Technica","M-Series","ATH-M70x","Audio-Technica ATH-M70x",2015,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("ATECH_M50XBT","Audio-Technica","M-Series","ATH-M50xBT","Audio-Technica ATH-M50xBT",2018,"Discontinued","Closed Back","Dynamic","Yes","No",succ="ATECH_M50XBT2")
add("ATECH_M50XBT2","Audio-Technica","M-Series","ATH-M50xBT2","Audio-Technica ATH-M50xBT2",2021,"Active","Closed Back","Dynamic","Yes","No",pred="ATECH_M50XBT")
add("ATECH_MSR7","Audio-Technica","MSR","ATH-MSR7","Audio-Technica ATH-MSR7",2014,"Discontinued","Closed Back","Dynamic","No","No")
add("ATECH_R70X","Audio-Technica","R-Series","ATH-R70x","Audio-Technica ATH-R70x",2015,"Active","Open Back","Dynamic","No","No",category="Studio",succ="ATECH_R70XA",notes="First A-T open-back reference")
add("ATECH_R70XA","Audio-Technica","R-Series","ATH-R70xa","Audio-Technica ATH-R70xa",2025,"Active","Open Back","Dynamic","No","No",category="Studio",pred="ATECH_R70X")
add("ATECH_R50X","Audio-Technica","R-Series","ATH-R50x","Audio-Technica ATH-R50x",2025,"Active","Open Back","Dynamic","No","No",category="Studio")
add("ATECH_R30X","Audio-Technica","R-Series","ATH-R30x","Audio-Technica ATH-R30x",2025,"Active","Open Back","Dynamic","No","No",category="Studio")
add("ATECH_ADX5000","Audio-Technica","A-Series","ATH-ADX5000","Audio-Technica ATH-ADX5000",2017,"Active","Open Back","Dynamic","No","No",notes="Flagship open-back")
add("ATECH_ADX3000","Audio-Technica","A-Series","ATH-ADX3000","Audio-Technica ATH-ADX3000",2025,"Active","Open Back","Dynamic","No","No")
add("ATECH_AD700X","Audio-Technica","A-Series","ATH-AD700X","Audio-Technica ATH-AD700X",2012,"Active","Open Back","Dynamic","No","No")
add("ATECH_AD900X","Audio-Technica","A-Series","ATH-AD900X","Audio-Technica ATH-AD900X",2012,"Active","Open Back","Dynamic","No","No")
add("ATECH_WP900","Audio-Technica","W-Series","ATH-WP900","Audio-Technica ATH-WP900",2019,"Active","Closed Back","Dynamic","No","No",notes="Flame maple wood earcups")
add("ATECH_AWKT","Audio-Technica","W-Series","ATH-AWKT","Audio-Technica ATH-AWKT",2019,"Active","Closed Back","Dynamic","No","No",notes="Ebony wood")

# ---- AKG ----
add("AKG_K702","AKG","K-Series","K702","AKG K702",2009,"Legacy Active","Open Back","Dynamic","No","No",notes="Reference open-back")
add("AKG_K612","AKG","K-Series","K612 Pro","AKG K612 Pro",2011,"Active","Open Back","Dynamic","No","No")
add("AKG_K812","AKG","K-Series","K812","AKG K812",2013,"Active","Open Back","Dynamic","No","No",notes="Reference flagship")
add("AKG_K712","AKG","K-Series","K712 Pro","AKG K712 Pro",2014,"Active","Open Back","Dynamic","No","No")
add("AKG_K371","AKG","K-Series","K371","AKG K371",2019,"Active","Closed Back","Dynamic","No","No",notes="Harman-tuned closed-back")
add("AKG_K361","AKG","K-Series","K361","AKG K361",2019,"Active","Closed Back","Dynamic","No","No")
add("AKG_N700NC","AKG","N-Series","N700NC","AKG N700NC",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="AKG_N700NCM2")
add("AKG_N700NCM2","AKG","N-Series","N700NC M2","AKG N700NC M2",2019,"Active","Closed Back","Dynamic","Yes","Yes",pred="AKG_N700NC")
add("AKG_N90Q","AKG","N-Series","N90Q","AKG N90Q",2016,"Discontinued","Closed Back","Dynamic","No","Yes",notes="Tuned by Quincy Jones")

# ---- Beyerdynamic ----
add("BEYER_DT770PRO","Beyerdynamic","DT","DT 770 Pro","Beyerdynamic DT 770 Pro",1985,"Legacy Active","Closed Back","Dynamic","No","No",category="Studio",notes="Studio classic, still produced")
add("BEYER_DT880","Beyerdynamic","DT","DT 880","Beyerdynamic DT 880",1980,"Legacy Active","Semi-Open","Dynamic","No","No",succ="BEYER_DT880_2005",notes="Original semi-open classic")
add("BEYER_DT990PRO","Beyerdynamic","DT","DT 990 Pro","Beyerdynamic DT 990 Pro",1985,"Legacy Active","Open Back","Dynamic","No","No",category="Studio")
add("BEYER_DT1770","Beyerdynamic","DT","DT 1770 Pro","Beyerdynamic DT 1770 Pro",2016,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Tesla driver")
add("BEYER_DT1990","Beyerdynamic","DT","DT 1990 Pro","Beyerdynamic DT 1990 Pro",2016,"Active","Open Back","Dynamic","No","No",category="Studio",succ="BEYER_DT1990MK2")
add("BEYER_DT1990MK2","Beyerdynamic","DT","DT 1990 Pro MkII","Beyerdynamic DT 1990 Pro MkII",2024,"Active","Open Back","Dynamic","No","No",category="Studio",pred="BEYER_DT1990")
add("BEYER_DT700PROX","Beyerdynamic","DT","DT 700 Pro X","Beyerdynamic DT 700 Pro X",2022,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Stellar.45 driver")
add("BEYER_DT900PROX","Beyerdynamic","DT","DT 900 Pro X","Beyerdynamic DT 900 Pro X",2022,"Active","Open Back","Dynamic","No","No",category="Studio")
add("BEYER_T1","Beyerdynamic","T-Series","T1","Beyerdynamic T1 (1st Gen)",2009,"Discontinued","Open Back","Dynamic","No","No",succ="BEYER_T1_2",notes="Tesla flagship")
add("BEYER_T1_2","Beyerdynamic","T-Series","T1 2nd Gen","Beyerdynamic T1 2nd Generation",2014,"Discontinued","Open Back","Dynamic","No","No",pred="BEYER_T1",succ="BEYER_T1_3")
add("BEYER_T1_3","Beyerdynamic","T-Series","T1 3rd Gen","Beyerdynamic T1 3rd Generation",2020,"Active","Open Back","Dynamic","No","No",pred="BEYER_T1_2")
add("BEYER_T5_3","Beyerdynamic","T-Series","T5 3rd Gen","Beyerdynamic T5 3rd Generation",2020,"Active","Closed Back","Dynamic","No","No",notes="Closed sibling of T1")
add("BEYER_AMIRON","Beyerdynamic","Amiron","Amiron Home","Beyerdynamic Amiron Home",2017,"Active","Open Back","Dynamic","No","No")
add("BEYER_AMIRONW","Beyerdynamic","Amiron","Amiron Wireless","Beyerdynamic Amiron Wireless",2018,"Active","Closed Back","Dynamic","Yes","No")
add("BEYER_AVENTHOW","Beyerdynamic","T-Series","Aventho Wireless","Beyerdynamic Aventho Wireless",2017,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone",fit="On-Ear")
add("BEYER_MMX300","Beyerdynamic","MMX","MMX 300","Beyerdynamic MMX 300",2014,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Gaming headset")
add("BEYER_CUSTOM1","Beyerdynamic","DT","Custom One Pro","Beyerdynamic Custom One Pro",2012,"Active","Closed Back","Dynamic","No","No",notes="Adjustable bass sliders")

# ---- Bose ----
add("BOSE_QC25","Bose","QuietComfort","QuietComfort 25","Bose QuietComfort 25",2014,"Discontinued","Closed Back","Dynamic","No","Yes",succ="BOSE_QC35")
add("BOSE_QC35","Bose","QuietComfort","QuietComfort 35","Bose QuietComfort 35",2016,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="BOSE_QC25",succ="BOSE_QC35II")
add("BOSE_QC35II","Bose","QuietComfort","QuietComfort 35 II","Bose QuietComfort 35 II",2017,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="BOSE_QC35",succ="BOSE_QC45")
add("BOSE_QC45","Bose","QuietComfort","QuietComfort 45","Bose QuietComfort 45",2021,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="BOSE_QC35II",succ="BOSE_QCHP")
add("BOSE_NC700","Bose","700","Noise Cancelling 700","Bose Noise Cancelling Headphones 700",2019,"Active","Closed Back","Dynamic","Yes","Yes",notes="Premium business/travel line")
add("BOSE_QCULTRA","Bose","QuietComfort","QuietComfort Ultra","Bose QuietComfort Ultra Headphones",2023,"Active","Closed Back","Dynamic","Yes","Yes",succ="BOSE_QCULTRA2",notes="Immersive spatial audio")
add("BOSE_QCULTRA2","Bose","QuietComfort","QuietComfort Ultra (2nd Gen)","Bose QuietComfort Ultra Headphones (2nd Gen)",2025,"Active","Closed Back","Dynamic","Yes","Yes",pred="BOSE_QCULTRA")
add("BOSE_QCHP","Bose","QuietComfort","QuietComfort Headphones","Bose QuietComfort Headphones",2024,"Active","Closed Back","Dynamic","Yes","Yes",pred="BOSE_QC45")

# ---- Audeze ----
add("AUDEZE_LCD2","Audeze","LCD","LCD-2","Audeze LCD-2",2009,"Legacy Active","Open Back","Planar Magnetic","No","No",notes="The headphone that launched Audeze")
add("AUDEZE_LCD3","Audeze","LCD","LCD-3","Audeze LCD-3",2011,"Active","Open Back","Planar Magnetic","No","No")
add("AUDEZE_LCDX","Audeze","LCD","LCD-X","Audeze LCD-X",2013,"Active","Open Back","Planar Magnetic","No","No",notes="Studio reference")
add("AUDEZE_LCDXC","Audeze","LCD","LCD-XC","Audeze LCD-XC",2013,"Active","Closed Back","Planar Magnetic","No","No")
add("AUDEZE_LCD4","Audeze","LCD","LCD-4","Audeze LCD-4",2015,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Former flagship")
add("AUDEZE_LCD1","Audeze","LCD","LCD-1","Audeze LCD-1",2020,"Active","Open Back","Planar Magnetic","No","No",notes="Lightweight portable planar")
add("AUDEZE_LCD5","Audeze","LCD","LCD-5","Audeze LCD-5",2021,"Discontinued","Open Back","Planar Magnetic","No","No",succ="AUDEZE_LCD5S",disc="2026",notes="Flagship planar; replaced by LCD-5s")
add("AUDEZE_LCD5S","Audeze","LCD","LCD-5s","Audeze LCD-5s",2026,"Active","Open Back","Planar Magnetic","No","No",pred="AUDEZE_LCD5",notes="SLAM acoustic tech")
add("AUDEZE_MM500","Audeze","MM","MM-500","Audeze MM-500",2022,"Active","Open Back","Planar Magnetic","No","No",category="Studio",notes="Co-developed with Manny Marroquin")
add("AUDEZE_MM100","Audeze","MM","MM-100","Audeze MM-100",2023,"Active","Open Back","Planar Magnetic","No","No",category="Studio")
add("AUDEZE_CRBN","Audeze","CRBN","CRBN","Audeze CRBN",2022,"Active","Open Back","Electrostatic","No","No",notes="Carbon-nanotube electrostatic")
add("AUDEZE_MAXWELL","Audeze","Maxwell","Maxwell","Audeze Maxwell",2023,"Active","Closed Back","Planar Magnetic","Yes","No",category="Gaming",succ="AUDEZE_MAXWELL2",notes="Wireless gaming planar")
add("AUDEZE_MAXWELL2","Audeze","Maxwell","Maxwell 2","Audeze Maxwell 2",2025,"Active","Closed Back","Planar Magnetic","Yes","No",category="Gaming",pred="AUDEZE_MAXWELL")

# ---- HiFiMan ----
add("HIFIMAN_HE400","HiFiMan","HE","HE-400","HiFiMan HE-400",2011,"Discontinued","Open Back","Planar Magnetic","No","No",succ="HIFIMAN_HE400I")
add("HIFIMAN_HE400I","HiFiMan","HE","HE-400i","HiFiMan HE-400i",2014,"Discontinued","Open Back","Planar Magnetic","No","No",pred="HIFIMAN_HE400")
add("HIFIMAN_HE400SE","HiFiMan","HE","HE400SE","HiFiMan HE400SE",2021,"Active","Open Back","Planar Magnetic","No","No",notes="Budget Stealth Magnet planar")
add("HIFIMAN_HE560","HiFiMan","HE","HE-560","HiFiMan HE-560",2014,"Active","Open Back","Planar Magnetic","No","No")
add("HIFIMAN_HE6SE","HiFiMan","HE","HE6se","HiFiMan HE6se",2018,"Active","Open Back","Planar Magnetic","No","No",notes="Hard-to-drive planar")
add("HIFIMAN_SUNDARA","HiFiMan","Sundara","Sundara","HiFiMan Sundara",2018,"Active","Open Back","Planar Magnetic","No","No",notes="Popular mid-tier planar")
add("HIFIMAN_ANANDA","HiFiMan","Ananda","Ananda","HiFiMan Ananda",2018,"Active","Open Back","Planar Magnetic","No","No",succ="HIFIMAN_ANANDANANO")
add("HIFIMAN_ANANDANANO","HiFiMan","Ananda","Ananda Nano","HiFiMan Ananda Nano",2023,"Active","Open Back","Planar Magnetic","No","No",pred="HIFIMAN_ANANDA")
add("HIFIMAN_ARYA","HiFiMan","Arya","Arya","HiFiMan Arya",2018,"Active","Open Back","Planar Magnetic","No","No",succ="HIFIMAN_ARYAORGANIC")
add("HIFIMAN_ARYAORGANIC","HiFiMan","Arya","Arya Organic","HiFiMan Arya Organic",2023,"Active","Open Back","Planar Magnetic","No","No",pred="HIFIMAN_ARYA")
add("HIFIMAN_HE1000","HiFiMan","HE","HE1000","HiFiMan HE1000",2015,"Discontinued","Open Back","Planar Magnetic","No","No",succ="HIFIMAN_HE1000V2",notes="Nanometer diaphragm")
add("HIFIMAN_HE1000SE","HiFiMan","HE","HE1000se","HiFiMan HE1000se",2020,"Active","Open Back","Planar Magnetic","No","No",pred="HIFIMAN_HE1000V2")
add("HIFIMAN_SUSVARA","HiFiMan","Susvara","Susvara","HiFiMan Susvara",2017,"Active","Open Back","Planar Magnetic","No","No",notes="Reference flagship planar")
add("HIFIMAN_EDITIONXS","HiFiMan","Edition","Edition XS","HiFiMan Edition XS",2021,"Active","Open Back","Planar Magnetic","No","No",notes="Value Stealth Magnet planar")
add("HIFIMAN_DEVA","HiFiMan","Deva","Deva","HiFiMan Deva",2019,"Discontinued","Open Back","Planar Magnetic","Yes","No",succ="HIFIMAN_DEVAPRO",notes="Optional Bluemini wireless module")
add("HIFIMAN_DEVAPRO","HiFiMan","Deva","Deva Pro","HiFiMan Deva Pro",2021,"Active","Open Back","Planar Magnetic","Yes","No",pred="HIFIMAN_DEVA")

# ---- Focal ----
add("FOCAL_ELEAR","Focal","Clear","Elear","Focal Elear",2016,"Discontinued","Open Back","Dynamic","No","No",notes="Aluminum-magnesium dome")
add("FOCAL_CLEAR","Focal","Clear","Clear","Focal Clear",2017,"Discontinued","Open Back","Dynamic","No","No",succ="FOCAL_CLEARMG")
add("FOCAL_CLEARMG","Focal","Clear","Clear MG","Focal Clear MG",2021,"Active","Open Back","Dynamic","No","No",pred="FOCAL_CLEAR",notes="Magnesium dome")
add("FOCAL_UTOPIA","Focal","Utopia","Utopia","Focal Utopia",2016,"Discontinued","Open Back","Dynamic","No","No",succ="FOCAL_UTOPIA2022",notes="Beryllium dome flagship")
add("FOCAL_UTOPIA2022","Focal","Utopia","Utopia 2022","Focal Utopia 2022",2022,"Active","Open Back","Dynamic","No","No",pred="FOCAL_UTOPIA")
add("FOCAL_ELEGIA","Focal","Elegia","Elegia","Focal Elegia",2018,"Discontinued","Closed Back","Dynamic","No","No")
add("FOCAL_STELLIA","Focal","Elegia","Stellia","Focal Stellia",2019,"Active","Closed Back","Dynamic","No","No",notes="Closed beryllium flagship")
add("FOCAL_CELESTEE","Focal","Elegia","Celestee","Focal Celestee",2021,"Active","Closed Back","Dynamic","No","No")
add("FOCAL_BATHYS","Focal","Bathys","Bathys","Focal Bathys",2022,"Active","Closed Back","Dynamic","Yes","Yes",succ="FOCAL_BATHYSMG",notes="First Focal wireless ANC")
add("FOCAL_BATHYSMG","Focal","Bathys","Bathys MG","Focal Bathys MG",2025,"Active","Closed Back","Dynamic","Yes","Yes",pred="FOCAL_BATHYS",notes="Magnesium driver edition")
add("FOCAL_AZURYS","Focal","Listen","Azurys","Focal Azurys",2025,"Active","Closed Back","Dynamic","No","No",notes="Affordable closed-back")
add("FOCAL_HADENYS","Focal","Listen","Hadenys","Focal Hadenys",2025,"Active","Open Back","Dynamic","No","No",notes="Affordable open-back")

# ---- Bowers & Wilkins ----
add("BW_P5","Bowers & Wilkins","P-Series","P5","Bowers & Wilkins P5",2010,"Discontinued","Closed Back","Dynamic","No","No",notes="First B&W headphone",fit="On-Ear")
add("BW_P7","Bowers & Wilkins","P-Series","P7","Bowers & Wilkins P7",2013,"Discontinued","Closed Back","Dynamic","No","No")
add("BW_P9","Bowers & Wilkins","P-Series","P9 Signature","Bowers & Wilkins P9 Signature",2016,"Discontinued","Closed Back","Dynamic","No","No")
add("BW_PX","Bowers & Wilkins","PX","PX","Bowers & Wilkins PX",2017,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="BW_PX7")
add("BW_PX7","Bowers & Wilkins","PX","PX7","Bowers & Wilkins PX7",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="BW_PX",succ="BW_PX7S2")
add("BW_PX7S2","Bowers & Wilkins","PX","Px7 S2","Bowers & Wilkins Px7 S2",2022,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="BW_PX7",succ="BW_PX7S2E")
add("BW_PX7S2E","Bowers & Wilkins","PX","Px7 S2e","Bowers & Wilkins Px7 S2e",2023,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="BW_PX7S2",succ="BW_PX7S3")
add("BW_PX7S3","Bowers & Wilkins","PX","Px7 S3","Bowers & Wilkins Px7 S3",2025,"Active","Closed Back","Dynamic","Yes","Yes",pred="BW_PX7S2E")
add("BW_PX8","Bowers & Wilkins","PX","Px8","Bowers & Wilkins Px8",2022,"Active","Closed Back","Dynamic","Yes","Yes",succ="BW_PX8S2",notes="Carbon cone drivers")
add("BW_PX8S2","Bowers & Wilkins","PX","Px8 S2","Bowers & Wilkins Px8 S2",2025,"Active","Closed Back","Dynamic","Yes","Yes",pred="BW_PX8")

# ---- Grado ----
add("GRADO_SR60X","Grado","Prestige","SR60x","Grado SR60x",2021,"Active","Open Back","Dynamic","No","No",category="Headphone",fit="On-Ear")
add("GRADO_SR80X","Grado","Prestige","SR80x","Grado SR80x",2021,"Active","Open Back","Dynamic","No","No",notes="Longest-running Grado model",fit="On-Ear")
add("GRADO_SR325X","Grado","Prestige","SR325x","Grado SR325x",2021,"Active","Open Back","Dynamic","No","No",notes="Metal housing",fit="On-Ear")
add("GRADO_RS1X","Grado","Reference","RS1x","Grado RS1x",2021,"Active","Open Back","Dynamic","No","No",notes="Tri-wood housing",fit="On-Ear")
add("GRADO_RS2X","Grado","Reference","RS2x","Grado RS2x",2021,"Active","Open Back","Dynamic","No","No",fit="On-Ear")
add("GRADO_GS3000X","Grado","Statement","GS3000x","Grado GS3000x",2021,"Active","Open Back","Dynamic","No","No",notes="Cocobolo flagship",fit="On-Ear")
add("GRADO_HEMP","Grado","Prestige","Hemp","Grado Hemp Headphone",2020,"Discontinued","Open Back","Dynamic","No","No",notes="Limited hemp-housing model",fit="On-Ear")
add("GRADO_GW100X","Grado","GW","GW100x","Grado GW100x",2021,"Active","Open Back","Dynamic","Yes","No",notes="Wireless open-back",fit="On-Ear")
# ---- Meze Audio ----
add("MEZE_99CLASSICS","Meze Audio","Classics","99 Classics","Meze 99 Classics",2015,"Active","Closed Back","Dynamic","No","No",notes="Walnut wood earcups")
add("MEZE_99NEO","Meze Audio","Classics","99 Neo","Meze 99 Neo",2017,"Active","Closed Back","Dynamic","No","No")
add("MEZE_109PRO","Meze Audio","Classics","109 Pro","Meze 109 Pro",2022,"Active","Open Back","Dynamic","No","No",notes="Open-back dynamic")
add("MEZE_105AER","Meze Audio","Classics","105 AER","Meze 105 AER",2024,"Active","Open Back","Dynamic","No","No")
add("MEZE_EMPYREAN","Meze Audio","Flagship","Empyrean","Meze Empyrean",2018,"Active","Open Back","Planar Magnetic","No","No",notes="Isodynamic hybrid array")
add("MEZE_ELITE","Meze Audio","Flagship","Elite","Meze Elite",2021,"Active","Open Back","Planar Magnetic","No","No",notes="Flagship planar")
add("MEZE_LIRIC","Meze Audio","Flagship","Liric","Meze Liric",2022,"Active","Closed Back","Planar Magnetic","No","No",succ="MEZE_LIRIC2",notes="Closed planar")
add("MEZE_LIRIC2","Meze Audio","Flagship","Liric 2nd Gen","Meze Liric 2nd Generation",2024,"Active","Closed Back","Planar Magnetic","No","No",pred="MEZE_LIRIC")
add("MEZE_POET","Meze Audio","Flagship","Poet","Meze Poet",2024,"Active","Open Back","Planar Magnetic","No","No")

# ---- Dan Clark Audio ----
add("DCA_AEONFLOW","Dan Clark Audio","Aeon","Aeon Flow","Dan Clark Audio Aeon Flow",2017,"Discontinued","Closed Back","Planar Magnetic","No","No",notes="Originally MrSpeakers")
add("DCA_AEON2","Dan Clark Audio","Aeon","Aeon 2","Dan Clark Audio Aeon 2",2019,"Active","Closed Back","Planar Magnetic","No","No")
add("DCA_AEON2NOIRE","Dan Clark Audio","Aeon","Aeon 2 Noire","Dan Clark Audio Aeon 2 Noire",2020,"Active","Closed Back","Planar Magnetic","No","No")
add("DCA_ETHER2","Dan Clark Audio","Ether","Ether 2","Dan Clark Audio Ether 2",2018,"Active","Open Back","Planar Magnetic","No","No")
add("DCA_STEALTH","Dan Clark Audio","Flagship","Stealth","Dan Clark Audio Stealth",2021,"Active","Closed Back","Planar Magnetic","No","No",notes="AMTS tuning, closed flagship")
add("DCA_EXPANSE","Dan Clark Audio","Flagship","Expanse","Dan Clark Audio Expanse",2022,"Active","Open Back","Planar Magnetic","No","No",notes="Open-back sibling of Stealth")
add("DCA_E3","Dan Clark Audio","Flagship","E3","Dan Clark Audio E3",2024,"Active","Closed Back","Planar Magnetic","No","No",notes="Brings AMTS to lower price")
add("DCA_CORINA","Dan Clark Audio","Flagship","Corina","Dan Clark Audio Corina",2023,"Active","Open Back","Electrostatic","No","No",notes="Electrostatic flagship")

# ---- Apple ----
add("APPLE_AIRPODSMAX","Apple","AirPods Max","AirPods Max","Apple AirPods Max",2020,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="APPLE_AIRPODSMAXUSBC",notes="Lightning port")
add("APPLE_AIRPODSMAXUSBC","Apple","AirPods Max","AirPods Max (USB-C)","Apple AirPods Max (USB-C)",2024,"Active","Closed Back","Dynamic","Yes","Yes",pred="APPLE_AIRPODSMAX",notes="USB-C, lossless audio support")

# ---- Beats ----
add("BEATS_STUDIO2","Beats","Studio","Studio 2","Beats Studio 2 Wireless",2014,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="BEATS_STUDIO3")
add("BEATS_STUDIO3","Beats","Studio","Studio 3","Beats Studio 3 Wireless",2017,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="BEATS_STUDIO2",succ="BEATS_STUDIOPRO")
add("BEATS_STUDIOPRO","Beats","Studio","Studio Pro","Beats Studio Pro",2023,"Active","Closed Back","Dynamic","Yes","Yes",pred="BEATS_STUDIO3")
add("BEATS_SOLO3","Beats","Solo","Solo 3","Beats Solo 3 Wireless",2016,"Discontinued","Closed Back","Dynamic","Yes","No",succ="BEATS_SOLO4",category="Headphone",fit="On-Ear")
add("BEATS_SOLO4","Beats","Solo","Solo 4","Beats Solo 4",2024,"Active","Closed Back","Dynamic","Yes","No",pred="BEATS_SOLO3",category="Headphone",fit="On-Ear")
# ---- Shure ----
add("SHURE_SRH1540","Shure","SRH","SRH1540","Shure SRH1540",2014,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("SHURE_SRH1840","Shure","SRH","SRH1840","Shure SRH1840",2011,"Active","Open Back","Dynamic","No","No",category="Studio")
add("SHURE_AONIC50","Shure","AONIC","AONIC 50","Shure AONIC 50",2020,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="SHURE_AONIC50G2")
add("SHURE_AONIC50G2","Shure","AONIC","AONIC 50 Gen 2","Shure AONIC 50 Gen 2",2023,"Active","Closed Back","Dynamic","Yes","Yes",pred="SHURE_AONIC50")

# =========================== GAMING HEADSETS ===========================
G = "Gaming"
# ---- SteelSeries ----
add("STEEL_ARCTIS7","SteelSeries","Arctis","Arctis 7","SteelSeries Arctis 7",2017,"Discontinued","Closed Back","Dynamic","Yes","No",category=G)
add("STEEL_ARCTISPRO","SteelSeries","Arctis","Arctis Pro Wireless","SteelSeries Arctis Pro Wireless",2018,"Discontinued","Closed Back","Dynamic","Yes","No",category=G)
add("STEEL_NOVAPRO","SteelSeries","Arctis Nova","Arctis Nova Pro Wireless","SteelSeries Arctis Nova Pro Wireless",2022,"Active","Closed Back","Dynamic","Yes","Yes",category=G,notes="Dual hot-swap batteries, ANC")
add("STEEL_NOVA7","SteelSeries","Arctis Nova","Arctis Nova 7","SteelSeries Arctis Nova 7",2022,"Active","Closed Back","Dynamic","Yes","No",category=G)
add("STEEL_NOVA3","SteelSeries","Arctis Nova","Arctis Nova 3","SteelSeries Arctis Nova 3",2022,"Active","Closed Back","Dynamic","No","No",category=G)
add("STEEL_NOVA5","SteelSeries","Arctis Nova","Arctis Nova 5","SteelSeries Arctis Nova 5",2024,"Active","Closed Back","Dynamic","Yes","No",category=G)
add("STEEL_NOVAELITE","SteelSeries","Arctis Nova","Arctis Nova Elite","SteelSeries Arctis Nova Elite",2025,"Active","Closed Back","Dynamic","Yes","Yes",category=G,notes="Simultaneous BT + 2.4GHz")
# ---- HyperX ----
add("HYPERX_CLOUD2","HyperX","Cloud","Cloud II","HyperX Cloud II",2015,"Active","Closed Back","Dynamic","No","No",category=G,notes="Long-running wired classic")
add("HYPERX_CLOUDALPHA","HyperX","Cloud","Cloud Alpha","HyperX Cloud Alpha",2017,"Active","Closed Back","Dynamic","No","No",category=G,notes="Dual-chamber drivers")
add("HYPERX_CLOUDALPHAW","HyperX","Cloud","Cloud Alpha Wireless","HyperX Cloud Alpha Wireless",2022,"Active","Closed Back","Dynamic","Yes","No",category=G,notes="~300hr battery life")
add("HYPERX_CLOUD3","HyperX","Cloud","Cloud III","HyperX Cloud III",2023,"Active","Closed Back","Dynamic","No","No",category=G,pred="HYPERX_CLOUD2")
add("HYPERX_CLOUD3W","HyperX","Cloud","Cloud III Wireless","HyperX Cloud III Wireless",2023,"Active","Closed Back","Dynamic","Yes","No",category=G)
# ---- Razer ----
add("RAZER_BSV2","Razer","BlackShark","BlackShark V2","Razer BlackShark V2",2020,"Active","Closed Back","Dynamic","No","No",category=G,notes="TriForce Titanium drivers")
add("RAZER_BSV2PRO","Razer","BlackShark","BlackShark V2 Pro","Razer BlackShark V2 Pro",2020,"Active","Closed Back","Dynamic","Yes","No",category=G,succ="RAZER_BSV2PRO23")
add("RAZER_BSV2PRO23","Razer","BlackShark","BlackShark V2 Pro (2023)","Razer BlackShark V2 Pro (2023)",2023,"Active","Closed Back","Dynamic","Yes","No",category=G,pred="RAZER_BSV2PRO")
add("RAZER_BSV3PRO","Razer","BlackShark","BlackShark V3 Pro","Razer BlackShark V3 Pro",2025,"Active","Closed Back","Dynamic","Yes","No",category=G,notes="HyperClear mic")
add("RAZER_KRAKENV3","Razer","Kraken","Kraken V3","Razer Kraken V3",2021,"Active","Closed Back","Dynamic","No","No",category=G)
add("RAZER_KRAKENV4PRO","Razer","Kraken","Kraken V4 Pro","Razer Kraken V4 Pro",2025,"Active","Closed Back","Dynamic","Yes","No",category=G)
# ---- Logitech G ----
add("LOGI_GPROX","Logitech G","G Pro","G Pro X","Logitech G Pro X",2019,"Discontinued","Closed Back","Dynamic","No","No",category=G,notes="Blue VO!CE mic",succ="LOGI_GPROX2")
add("LOGI_GPROX2","Logitech G","G Pro","G Pro X 2 Lightspeed","Logitech G Pro X 2 Lightspeed",2023,"Active","Closed Back","Dynamic","Yes","No",category=G,pred="LOGI_GPROX",notes="50mm Pro-G Graphene drivers")
add("LOGI_G535","Logitech G","G","G535 Lightspeed","Logitech G535 Lightspeed",2021,"Active","Closed Back","Dynamic","Yes","No",category=G)
add("LOGI_G733","Logitech G","G","G733 Lightspeed","Logitech G733 Lightspeed",2020,"Active","Closed Back","Dynamic","Yes","No",category=G)
# ---- Astro Gaming ----
add("ASTRO_A50G4","Astro Gaming","A-Series","A50 Wireless Gen 4","Astro A50 Wireless (Gen 4)",2019,"Discontinued","Closed Back","Dynamic","Yes","No",category=G,succ="ASTRO_A50X")
add("ASTRO_A50X","Astro Gaming","A-Series","A50 X Lightspeed","Astro A50 X Lightspeed",2024,"Active","Closed Back","Dynamic","Yes","No",category=G,pred="ASTRO_A50G4",notes="HDMI base station, multi-console switching")
add("ASTRO_A40TR","Astro Gaming","A-Series","A40 TR","Astro A40 TR",2017,"Active","Open Back","Dynamic","No","No",category=G)
# ---- Turtle Beach ----
add("TB_STEALTH700G2","Turtle Beach","Stealth","Stealth 700 Gen 2","Turtle Beach Stealth 700 Gen 2",2020,"Active","Closed Back","Dynamic","Yes","No",category=G)
add("TB_STEALTHPRO","Turtle Beach","Stealth","Stealth Pro","Turtle Beach Stealth Pro",2023,"Active","Closed Back","Dynamic","Yes","Yes",category=G,notes="Swappable batteries, ANC")
add("TB_ATLASAIR","Turtle Beach","Stealth","Atlas Air","Turtle Beach Atlas Air",2024,"Active","Open Back","Dynamic","Yes","No",category=G,notes="Open-back wireless")
# ---- Corsair ----
add("CORSAIR_VIRTUOSO","Corsair","Virtuoso","Virtuoso RGB Wireless","Corsair Virtuoso RGB Wireless",2019,"Active","Closed Back","Dynamic","Yes","No",category=G)
add("CORSAIR_VIRTUOSOXT","Corsair","Virtuoso","Virtuoso RGB Wireless XT","Corsair Virtuoso RGB Wireless XT",2021,"Active","Closed Back","Dynamic","Yes","No",category=G)
add("CORSAIR_VIRTUOSOPRO","Corsair","Virtuoso","Virtuoso Pro","Corsair Virtuoso Pro",2023,"Active","Open Back","Dynamic","No","No",category=G,notes="Open-back, graphene drivers")
add("CORSAIR_HS80","Corsair","HS","HS80 RGB Wireless","Corsair HS80 RGB Wireless",2021,"Active","Closed Back","Dynamic","Yes","No",category=G)
# ---- ASUS ROG ----
add("ASUS_DELTAS","ASUS ROG","Delta","ROG Delta S","ASUS ROG Delta S",2021,"Active","Closed Back","Dynamic","No","No",category=G,notes="USB-C, quad-DAC")
add("ASUS_DELTA2","ASUS ROG","Delta","ROG Delta II","ASUS ROG Delta II",2025,"Active","Closed Back","Dynamic","Yes","No",category=G)

# =========================== HIGH-END / NICHE ===========================
# ---- Abyss ----
add("ABYSS_AB1266","Abyss","AB-1266","AB-1266","Abyss AB-1266",2013,"Active","Open Back","Planar Magnetic","No","No",notes="Reference flagship planar; later revised as Phi and Phi TC")
add("ABYSS_DIANA","Abyss","Diana","Diana","Abyss Diana",2017,"Active","Open Back","Planar Magnetic","No","No",succ="ABYSS_DIANAV2")
add("ABYSS_DIANAV2","Abyss","Diana","Diana V2","Abyss Diana V2",2020,"Active","Open Back","Planar Magnetic","No","No",pred="ABYSS_DIANA")
# ---- ZMF Headphones ----
add("ZMF_AUTEUR","ZMF Headphones","Auteur","Auteur","ZMF Auteur",2017,"Active","Open Back","Dynamic","No","No",notes="Hand-built wood")
add("ZMF_VERITEOPEN","ZMF Headphones","Verite","Verite Open","ZMF Verite Open",2019,"Active","Open Back","Dynamic","No","No",notes="Beryllium-coated driver")
add("ZMF_VERITECLOSED","ZMF Headphones","Verite","Verite Closed","ZMF Verite Closed",2019,"Active","Closed Back","Dynamic","No","No")
add("ZMF_ATRIUM","ZMF Headphones","Atrium","Atrium","ZMF Atrium",2022,"Active","Open Back","Dynamic","No","No")
add("ZMF_CALDERA","ZMF Headphones","Caldera","Caldera","ZMF Caldera",2023,"Active","Open Back","Planar Magnetic","No","No",notes="First ZMF planar")
# ---- Stax ----
add("STAX_SR009","Stax","SR","SR-009","Stax SR-009",2011,"Active","Open Back","Electrostatic","No","No",notes="Electrostatic earspeaker, needs energizer")
add("STAX_SR009S","Stax","SR","SR-009S","Stax SR-009S",2018,"Active","Open Back","Electrostatic","No","No")
add("STAX_SRL700","Stax","SR","SR-L700","Stax SR-L700",2015,"Active","Open Back","Electrostatic","No","No")
add("STAX_X9000","Stax","SR","SR-X9000","Stax SR-X9000",2021,"Active","Open Back","Electrostatic","No","No",notes="Flagship electrostatic")
# ---- Final Audio ----
add("FINAL_D8000","Final Audio","D-Series","D8000","Final Audio D8000",2017,"Active","Open Back","Planar Magnetic","No","No",notes="AFDS planar tech")
add("FINAL_D8000PRO","Final Audio","D-Series","D8000 Pro","Final Audio D8000 Pro",2019,"Active","Open Back","Planar Magnetic","No","No")
# ---- Fostex ----
add("FOSTEX_TH900MK2","Fostex","TH","TH900 mk2","Fostex TH900 mk2",2015,"Active","Closed Back","Dynamic","No","No",notes="Biodynamic driver, urushi finish")
add("FOSTEX_TH610","Fostex","TH","TH610","Fostex TH610",2016,"Discontinued","Closed Back","Dynamic","No","No")
add("FOSTEX_TH909","Fostex","TH","TH909","Fostex TH909",2018,"Active","Open Back","Dynamic","No","No")
# ---- Denon ----
add("DENON_D5200","Denon","AH-D","AH-D5200","Denon AH-D5200",2017,"Active","Closed Back","Dynamic","No","No",notes="Zebrawood, FreeEdge driver")
add("DENON_D7200","Denon","AH-D","AH-D7200","Denon AH-D7200",2016,"Active","Closed Back","Dynamic","No","No")
add("DENON_D9200","Denon","AH-D","AH-D9200","Denon AH-D9200",2018,"Active","Closed Back","Dynamic","No","No",notes="Bamboo flagship")
# ---- Rosson Audio ----
add("ROSSON_RAD0","Rosson Audio","RAD","RAD-0","Rosson Audio RAD-0",2020,"Active","Open Back","Planar Magnetic","No","No",notes="Hand-finished resin")
# ---- Kennerton ----
add("KENNERTON_ODIN","Kennerton","Flagship","Odin","Kennerton Odin",2014,"Active","Open Back","Planar Magnetic","No","No")
add("KENNERTON_THROR","Kennerton","Flagship","Thror","Kennerton Thror",2018,"Active","Open Back","Planar Magnetic","No","No")
# ---- Ultrasone ----
add("ULTRA_ED5","Ultrasone","Edition","Edition 5","Ultrasone Edition 5",2014,"Active","Closed Back","Dynamic","No","No",notes="S-Logic Plus")
add("ULTRA_PERF880","Ultrasone","Edition","Performance 880","Ultrasone Performance 880",2014,"Active","Closed Back","Dynamic","No","No")

# =========================== CONSUMER / MAINSTREAM ===========================
# ---- Bang & Olufsen ----
add("BO_H95","Bang & Olufsen","Beoplay","Beoplay H95","Bang & Olufsen Beoplay H95",2020,"Active","Closed Back","Dynamic","Yes","Yes",notes="Anniversary flagship")
add("BO_HX","Bang & Olufsen","Beoplay","Beoplay HX","Bang & Olufsen Beoplay HX",2021,"Active","Closed Back","Dynamic","Yes","Yes")
add("BO_H100","Bang & Olufsen","Beoplay","Beoplay H100","Bang & Olufsen Beoplay H100",2024,"Active","Closed Back","Dynamic","Yes","Yes",notes="Luxury flagship")
add("BO_H6","Bang & Olufsen","Beoplay","Beoplay H6","Bang & Olufsen Beoplay H6",2013,"Discontinued","Closed Back","Dynamic","No","No",fit="On-Ear")
# ---- Sonos ----
add("SONOS_ACE","Sonos","Ace","Ace","Sonos Ace",2024,"Active","Closed Back","Dynamic","Yes","Yes",notes="First Sonos headphone")
# ---- Marshall ----
add("MARSHALL_MONITOR2","Marshall","Monitor","Monitor II ANC","Marshall Monitor II ANC",2020,"Active","Closed Back","Dynamic","Yes","Yes")
add("MARSHALL_MAJOR4","Marshall","Monitor","Major IV","Marshall Major IV",2021,"Active","Closed Back","Dynamic","Yes","No",category="Headphone",fit="On-Ear")
add("MARSHALL_MAJOR5","Marshall","Monitor","Major V","Marshall Major V",2024,"Active","Closed Back","Dynamic","Yes","No",category="Headphone",fit="On-Ear")
# ---- JBL ----
add("JBL_TOUR1","JBL","Tour","Tour One","JBL Tour One",2020,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="JBL_TOUR1M2")
add("JBL_TOUR1M2","JBL","Tour","Tour One M2","JBL Tour One M2",2023,"Active","Closed Back","Dynamic","Yes","Yes",pred="JBL_TOUR1")
add("JBL_LIVE660","JBL","Live","Live 660NC","JBL Live 660NC",2021,"Active","Closed Back","Dynamic","Yes","Yes")
# ---- Skullcandy ----
add("SKULL_CRUSHERANC2","Skullcandy","Crusher","Crusher ANC 2","Skullcandy Crusher ANC 2",2023,"Active","Closed Back","Dynamic","Yes","Yes",notes="Sensory bass")
add("SKULL_CRUSHEREVO","Skullcandy","Crusher","Crusher Evo","Skullcandy Crusher Evo",2021,"Active","Closed Back","Dynamic","Yes","No")
# ---- Anker Soundcore ----
add("ANKER_SPACEQ45","Anker Soundcore","Space","Space Q45","Anker Soundcore Space Q45",2022,"Active","Closed Back","Dynamic","Yes","Yes")
add("ANKER_SPACEONE","Anker Soundcore","Space","Space One","Anker Soundcore Space One",2023,"Active","Closed Back","Dynamic","Yes","Yes")
add("ANKER_SPACEONEPRO","Anker Soundcore","Space","Space One Pro","Anker Soundcore Space One Pro",2024,"Active","Closed Back","Dynamic","Yes","Yes")
# ---- Technics ----
add("TECH_EAHA800","Technics","EAH","EAH-A800","Technics EAH-A800",2022,"Active","Closed Back","Dynamic","Yes","Yes")
# ---- Nothing ----
add("NOTHING_HEADPHONE1","Nothing","Headphone","Headphone (1)","Nothing Headphone (1)",2025,"Active","Closed Back","Dynamic","Yes","Yes",notes="First Nothing over-ear, KEF-tuned")

# ============================================================================
# DEEP-DIVE BATCH — filling out full catalogs of brands already in the DB
# ============================================================================

# ---- Sennheiser: HD 500-series + studio + wireless travel ----
add("SENN_HD518","Sennheiser","HD 500-series","HD 518","Sennheiser HD 518",2010,"Discontinued","Open Back","Dynamic","No","No")
add("SENN_HD558","Sennheiser","HD 500-series","HD 558","Sennheiser HD 558",2010,"Discontinued","Open Back","Dynamic","No","No",succ="SENN_HD559")
add("SENN_HD598","Sennheiser","HD 500-series","HD 598","Sennheiser HD 598",2010,"Discontinued","Open Back","Dynamic","No","No",succ="SENN_HD599",notes="Popular mid-tier open-back")
add("SENN_HD598CS","Sennheiser","HD 500-series","HD 598 CS","Sennheiser HD 598 CS",2016,"Discontinued","Closed Back","Dynamic","No","No",notes="Closed-back 598; Amazon exclusive; 23Ω; uses 569 driver")
add("SENN_HD559","Sennheiser","HD 500-series","HD 559","Sennheiser HD 559",2016,"Active","Open Back","Dynamic","No","No",pred="SENN_HD558")
add("SENN_HD569","Sennheiser","HD 500-series","HD 569","Sennheiser HD 569",2016,"Active","Closed Back","Dynamic","No","No")
add("SENN_HD579","Sennheiser","HD 500-series","HD 579","Sennheiser HD 579",2016,"Active","Open Back","Dynamic","No","No")
add("SENN_HD599","Sennheiser","HD 500-series","HD 599","Sennheiser HD 599",2016,"Active","Open Back","Dynamic","No","No",pred="SENN_HD598")
add("SENN_HD505","Sennheiser","HD 500-series","HD 505","Sennheiser HD 505",2025,"Active","Open Back","Dynamic","No","No")
add("SENN_HD25","Sennheiser","HD","HD 25","Sennheiser HD 25",2010,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="On-ear DJ/monitoring standard",fit="On-Ear")
add("SENN_HD250BT","Sennheiser","HD","HD 250BT","Sennheiser HD 250BT",2020,"Active","Closed Back","Dynamic","Yes","No",category="Headphone",fit="On-Ear")
add("SENN_HD350BT","Sennheiser","HD","HD 350BT","Sennheiser HD 350BT",2019,"Active","Closed Back","Dynamic","Yes","No")
add("SENN_HD450BT","Sennheiser","HD","HD 450BT","Sennheiser HD 450BT",2019,"Active","Closed Back","Dynamic","Yes","Yes")
add("SENN_HD4_40BT","Sennheiser","HD","HD 4.40 BT","Sennheiser HD 4.40 BT",2016,"Discontinued","Closed Back","Dynamic","Yes","No",fit="On-Ear")
add("SENN_HD4_50BTNC","Sennheiser","HD","HD 4.50 BTNC","Sennheiser HD 4.50 BTNC",2016,"Discontinued","Closed Back","Dynamic","Yes","Yes")
add("SENN_PXC550","Sennheiser","PXC","PXC 550 Wireless","Sennheiser PXC 550 Wireless",2016,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="SENN_PXC550II")
add("SENN_PXC550II","Sennheiser","PXC","PXC 550-II Wireless","Sennheiser PXC 550-II Wireless",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="SENN_PXC550")
add("SENN_HD58X","Sennheiser","HD","HD 58X Jubilee","Drop x Sennheiser HD 58X Jubilee",2018,"Active","Open Back","Dynamic","No","No",notes="Drop collaboration")
add("SENN_HD6XX","Sennheiser","HD","HD 6XX","Drop x Sennheiser HD 6XX",2016,"Active","Open Back","Dynamic","No","No",notes="Drop-exclusive HD 650 variant")
add("SENN_HD8XX","Sennheiser","HD","HD 8XX","Drop x Sennheiser HD 8XX",2020,"Active","Open Back","Dynamic","No","No",notes="Drop-exclusive HD 800 variant")

# ---- Sony: studio classics, ZX, XB, CH lines ----
add("SONY_MDR7506","Sony","MDR Studio","MDR-7506","Sony MDR-7506",1991,"Legacy Active","Closed Back","Dynamic","No","No",category="Studio",notes="Studio monitoring standard, still produced")
add("SONY_MDRV6","Sony","MDR Studio","MDR-V6","Sony MDR-V6",1985,"Discontinued","Closed Back","Dynamic","No","No",category="Studio",succ="SONY_MDR7506")
add("SONY_MDR7510","Sony","MDR Studio","MDR-7510","Sony MDR-7510",2010,"Discontinued","Closed Back","Dynamic","No","No",category="Studio")
add("SONY_CD900ST","Sony","MDR Studio","MDR-CD900ST","Sony MDR-CD900ST",1989,"Legacy Active","Closed Back","Dynamic","No","No",category="Studio",notes="Japanese studio standard")
add("SONY_ZX110","Sony","ZX","MDR-ZX110","Sony MDR-ZX110",2014,"Active","Closed Back","Dynamic","No","No",notes="Budget on-ear",fit="On-Ear")
add("SONY_ZX310","Sony","ZX","MDR-ZX310","Sony MDR-ZX310",2014,"Active","Closed Back","Dynamic","No","No",fit="On-Ear")
add("SONY_ZX750BN","Sony","ZX","MDR-ZX750BN","Sony MDR-ZX750BN",2014,"Discontinued","Closed Back","Dynamic","Yes","Yes")
add("SONY_XB650","Sony","XB","MDR-XB650BT","Sony MDR-XB650BT",2016,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Extra Bass",fit="On-Ear")
add("SONY_XB950B1","Sony","XB","MDR-XB950B1","Sony MDR-XB950B1",2016,"Discontinued","Closed Back","Dynamic","Yes","No")
add("SONY_XB900N","Sony","XB","WH-XB900N","Sony WH-XB900N",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="SONY_XB910N",notes="Extra Bass ANC")
add("SONY_XB910N","Sony","XB","WH-XB910N","Sony WH-XB910N",2021,"Active","Closed Back","Dynamic","Yes","Yes",pred="SONY_XB900N")
add("SONY_CH500","Sony","CH","WH-CH500","Sony WH-CH500",2018,"Discontinued","Closed Back","Dynamic","Yes","No",fit="On-Ear")
add("SONY_CH510","Sony","CH","WH-CH510","Sony WH-CH510",2019,"Active","Closed Back","Dynamic","Yes","No",fit="On-Ear")
add("SONY_CH520","Sony","CH","WH-CH520","Sony WH-CH520",2023,"Active","Closed Back","Dynamic","Yes","No",fit="On-Ear")
add("SONY_CH700N","Sony","CH","WH-CH700N","Sony WH-CH700N",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="SONY_CH710N")
add("SONY_CH710N","Sony","CH","WH-CH710N","Sony WH-CH710N",2020,"Discontinued","Closed Back","Dynamic","Yes","Yes",pred="SONY_CH700N",succ="SONY_CH720N")
add("SONY_CH720N","Sony","CH","WH-CH720N","Sony WH-CH720N",2023,"Active","Closed Back","Dynamic","Yes","Yes",pred="SONY_CH710N")

# ---- Audio-Technica: ART Monitor (A), AD open, W wood, SR/BT wireless ----
add("ATECH_A550Z","Audio-Technica","ART Monitor","ATH-A550Z","Audio-Technica ATH-A550Z",2014,"Active","Closed Back","Dynamic","No","No")
add("ATECH_A990Z","Audio-Technica","ART Monitor","ATH-A990Z","Audio-Technica ATH-A990Z",2014,"Active","Closed Back","Dynamic","No","No",notes="Art Monitor, D.A.D.S.")
add("ATECH_A1000Z","Audio-Technica","ART Monitor","ATH-A1000Z","Audio-Technica ATH-A1000Z",2014,"Active","Closed Back","Dynamic","No","No")
add("ATECH_A2000Z","Audio-Technica","ART Monitor","ATH-A2000Z","Audio-Technica ATH-A2000Z",2014,"Active","Closed Back","Dynamic","No","No")
add("ATECH_AD500X","Audio-Technica","A-Series","ATH-AD500X","Audio-Technica ATH-AD500X",2013,"Active","Open Back","Dynamic","No","No")
add("ATECH_AD1000X","Audio-Technica","A-Series","ATH-AD1000X","Audio-Technica ATH-AD1000X",2013,"Active","Open Back","Dynamic","No","No")
add("ATECH_AD2000X","Audio-Technica","A-Series","ATH-AD2000X","Audio-Technica ATH-AD2000X",2013,"Active","Open Back","Dynamic","No","No",notes="Flagship Air series")
add("ATECH_W1000Z","Audio-Technica","W-Series","ATH-W1000Z","Audio-Technica ATH-W1000Z",2014,"Active","Closed Back","Dynamic","No","No",notes="Teak wood")
add("ATECH_W5000","Audio-Technica","W-Series","ATH-W5000","Audio-Technica ATH-W5000",2007,"Discontinued","Closed Back","Dynamic","No","No")
add("ATECH_MSR7B","Audio-Technica","MSR","ATH-MSR7b","Audio-Technica ATH-MSR7b",2018,"Active","Closed Back","Dynamic","No","No",pred="ATECH_MSR7")
add("ATECH_M20X","Audio-Technica","M-Series","ATH-M20x","Audio-Technica ATH-M20x",2014,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("ATECH_M30X","Audio-Technica","M-Series","ATH-M30x","Audio-Technica ATH-M30x",2014,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("ATECH_SR50BT","Audio-Technica","SR/BT","ATH-SR50BT","Audio-Technica ATH-SR50BT",2018,"Active","Closed Back","Dynamic","Yes","Yes")
add("ATECH_SR30BT","Audio-Technica","SR/BT","ATH-SR30BT","Audio-Technica ATH-SR30BT",2019,"Active","Closed Back","Dynamic","Yes","No",notes="70hr battery")
add("ATECH_ANC900BT","Audio-Technica","SR/BT","ATH-ANC900BT","Audio-Technica ATH-ANC900BT QuietPoint",2019,"Active","Closed Back","Dynamic","Yes","Yes")

# ---- AKG: studio K-line and consumer ----
add("AKG_K240STUDIO","AKG","K-Studio","K240 Studio","AKG K240 Studio",1991,"Legacy Active","Semi-Open","Dynamic","No","No",category="Studio",notes="Studio classic, still produced")
add("AKG_K271MK2","AKG","K-Studio","K271 MkII","AKG K271 MkII",2008,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("AKG_K72","AKG","K-Studio","K72","AKG K72",2015,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("AKG_K92","AKG","K-Studio","K92","AKG K92",2015,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("AKG_K245","AKG","K-Studio","K245","AKG K245",2018,"Active","Open Back","Dynamic","No","No",category="Studio")
add("AKG_K550","AKG","K-Series","K550","AKG K550",2012,"Discontinued","Closed Back","Dynamic","No","No",succ="AKG_K553")
add("AKG_K553","AKG","K-Series","K553 Pro","AKG K553 Pro",2015,"Active","Closed Back","Dynamic","No","No",pred="AKG_K550",category="Studio")
add("AKG_K701","AKG","K-Series","K701","AKG K701",2005,"Legacy Active","Open Back","Dynamic","No","No",notes="Reference open-back classic")
add("AKG_Y50BT","AKG","K-Series","Y50BT","AKG Y50BT",2015,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone",fit="On-Ear")
# ---- Beyerdynamic: impedance variants (real spec differences) + more ----
add("BEYER_DT770_32","Beyerdynamic","DT","DT 770 Pro 32 Ohm","Beyerdynamic DT 770 Pro (32 Ohm)",2014,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Low-impedance mobile variant")
add("BEYER_DT770_80","Beyerdynamic","DT","DT 770 Pro 80 Ohm","Beyerdynamic DT 770 Pro (80 Ohm)",1985,"Legacy Active","Closed Back","Dynamic","No","No",category="Studio",notes="Most popular impedance")
add("BEYER_DT770_250","Beyerdynamic","DT","DT 770 Pro 250 Ohm","Beyerdynamic DT 770 Pro (250 Ohm)",1985,"Legacy Active","Closed Back","Dynamic","No","No",category="Studio",notes="High-impedance studio variant")
add("BEYER_DT880_250","Beyerdynamic","DT","DT 880 Pro 250 Ohm","Beyerdynamic DT 880 Pro (250 Ohm)",2005,"Legacy Active","Semi-Open","Dynamic","No","No",category="Studio")
add("BEYER_DT990_250","Beyerdynamic","DT","DT 990 Pro 250 Ohm","Beyerdynamic DT 990 Pro (250 Ohm)",1985,"Legacy Active","Open Back","Dynamic","No","No",category="Studio")
add("BEYER_DT240PRO","Beyerdynamic","DT","DT 240 Pro","Beyerdynamic DT 240 Pro",2016,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("BEYER_DT700PROX2","Beyerdynamic","DT","DT 700 Pro X mkII","Beyerdynamic DT 700 Pro X mkII",2025,"Active","Closed Back","Dynamic","No","No",category="Studio",pred="BEYER_DT700PROX")
add("BEYER_CUSTOMSTUDIO","Beyerdynamic","Custom","Custom Studio","Beyerdynamic Custom Studio",2015,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("BEYER_LAGOONANC","Beyerdynamic","Custom","Lagoon ANC","Beyerdynamic Lagoon ANC",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes")
add("BEYER_MMX150","Beyerdynamic","MMX","MMX 150","Beyerdynamic MMX 150",2022,"Active","Closed Back","Dynamic","No","No",category="Gaming")
add("BEYER_MMX300_2","Beyerdynamic","MMX","MMX 300 2nd Gen","Beyerdynamic MMX 300 (2nd Gen)",2019,"Active","Closed Back","Dynamic","No","No",category="Gaming",pred="BEYER_MMX300")
add("BEYER_TYGR300R","Beyerdynamic","DT","TYGR 300 R","Beyerdynamic TYGR 300 R",2020,"Active","Open Back","Dynamic","No","No",notes="Gaming-focused open-back; popular with audiophiles")

# ---- Bose: on-ear and earlier travel models ----
add("BOSE_QC3","Bose","QuietComfort On-Ear","QuietComfort 3","Bose QuietComfort 3",2006,"Discontinued","Closed Back","Dynamic","No","Yes",notes="On-ear ANC",fit="On-Ear")
add("BOSE_OE2","Bose","AE/SoundLink","OE2","Bose OE2",2011,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",fit="On-Ear")
add("BOSE_AE2","Bose","AE/SoundLink","AE2","Bose AE2",2010,"Discontinued","Closed Back","Dynamic","No","No")
add("BOSE_SOUNDLINKAE","Bose","AE/SoundLink","SoundLink Around-Ear II","Bose SoundLink Around-Ear II",2015,"Discontinued","Closed Back","Dynamic","Yes","No")
add("BOSE_SOUNDLINKOE","Bose","AE/SoundLink","SoundLink On-Ear","Bose SoundLink On-Ear",2016,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone",fit="On-Ear")
# ============================================================================
# DEEPENING BATCH 2 — more models for HiFiMan, Focal, Grado, Meze, B&W, gaming
# ============================================================================

# ---- HiFiMan: fuller planar catalog ----
add("HIFIMAN_HE500","HiFiMan","HE","HE-500","HiFiMan HE-500",2011,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Beloved early planar")
add("HIFIMAN_HE6","HiFiMan","HE","HE-6","HiFiMan HE-6",2011,"Discontinued","Open Back","Planar Magnetic","No","No",succ="HIFIMAN_HE6SE",notes="Famously power-hungry")
add("HIFIMAN_EDITIONX","HiFiMan","Edition","Edition X","HiFiMan Edition X",2015,"Discontinued","Open Back","Planar Magnetic","No","No",succ="HIFIMAN_EDITIONXV2")
add("HIFIMAN_EDITIONXV2","HiFiMan","Edition","Edition X V2","HiFiMan Edition X V2",2016,"Discontinued","Open Back","Planar Magnetic","No","No",pred="HIFIMAN_EDITIONX")
add("HIFIMAN_EDITIONS","HiFiMan","Edition","Edition S","HiFiMan Edition S",2016,"Discontinued","Open Back","Dynamic","No","No",notes="On-ear, switchable open/closed")
add("HIFIMAN_HE400S","HiFiMan","HE","HE400S","HiFiMan HE400S",2015,"Discontinued","Open Back","Planar Magnetic","No","No")
add("HIFIMAN_HE1000V2","HiFiMan","HE","HE1000 V2","HiFiMan HE1000 V2",2016,"Discontinued","Open Back","Planar Magnetic","No","No",pred="HIFIMAN_HE1000",succ="HIFIMAN_HE1000SE")
add("HIFIMAN_HE1000UNV","HiFiMan","HE","HE1000 Unveiled","HiFiMan HE1000 Unveiled",2024,"Active","Open Back","Planar Magnetic","No","No",pred="HIFIMAN_HE1000SE",notes="Stator-less open design")
add("HIFIMAN_ARYASTEALTH","HiFiMan","Arya","Arya Stealth","HiFiMan Arya Stealth Magnet",2021,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Stealth Magnet revision")
add("HIFIMAN_ARYAUNV","HiFiMan","Arya","Arya Unveiled","HiFiMan Arya Unveiled",2024,"Active","Open Back","Planar Magnetic","No","No")
add("HIFIMAN_ANANDANANOUNV","HiFiMan","Ananda","Ananda Unveiled","HiFiMan Ananda Unveiled",2024,"Active","Open Back","Planar Magnetic","No","No")
add("HIFIMAN_SUNDARAC","HiFiMan","Sundara","Sundara Closed-Back","HiFiMan Sundara Closed-Back",2022,"Active","Closed Back","Planar Magnetic","No","No")
add("HIFIMAN_HER9","HiFiMan","HE","HE-R9","HiFiMan HE-R9",2021,"Active","Closed Back","Dynamic","Yes","No",notes="Dynamic, optional Bluemini")
add("HIFIMAN_HER10P","HiFiMan","HE","HE-R10P","HiFiMan HE-R10P",2021,"Discontinued","Closed Back","Planar Magnetic","No","No",notes="Homage to R10")
add("HIFIMAN_HE4XX","HiFiMan","HE","HE4XX","Drop x HiFiMan HE4XX",2017,"Active","Open Back","Planar Magnetic","No","No",notes="Drop collaboration")
add("HIFIMAN_HE5XX","HiFiMan","HE","HE5XX","Drop x HiFiMan HE5XX",2021,"Active","Open Back","Planar Magnetic","No","No",notes="Drop collaboration")
add("HIFIMAN_JADE2","HiFiMan","HE","Jade II","HiFiMan Jade II",2019,"Active","Open Back","Electrostatic","No","No",notes="Electrostatic, needs energizer")
add("HIFIMAN_SHANGRILA","HiFiMan","HE","Shangri-La Jr","HiFiMan Shangri-La Jr",2017,"Active","Open Back","Electrostatic","No","No")
add("HIFIMAN_AUDIVINA","HiFiMan","HE","Audivina","HiFiMan Audivina",2023,"Active","Closed Back","Planar Magnetic","No","No",notes="Closed-back home listening")

# ---- Focal: studio Spirit line + Listen + Clear Pro ----
add("FOCAL_SPIRITONE","Focal","Spirit","Spirit One","Focal Spirit One",2012,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone")
add("FOCAL_SPIRITPRO","Focal","Spirit","Spirit Professional","Focal Spirit Professional",2013,"Discontinued","Closed Back","Dynamic","No","No",category="Studio")
add("FOCAL_LISTEN","Focal","Listen","Listen","Focal Listen",2016,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",fit="On-Ear")
add("FOCAL_LISTENPRO","Focal","Spirit","Listen Professional","Focal Listen Professional",2017,"Active","Closed Back","Dynamic","No","No",category="Studio",fit="On-Ear")
add("FOCAL_LISTENWL","Focal","Listen","Listen Wireless","Focal Listen Wireless",2017,"Discontinued","Closed Back","Dynamic","Yes","No",fit="On-Ear")
add("FOCAL_ELEX","Focal","Clear","Elex","Drop x Focal Elex",2017,"Active","Open Back","Dynamic","No","No",notes="Drop collaboration")
add("FOCAL_CLEARPRO","Focal","Clear","Clear Professional","Focal Clear Professional",2018,"Active","Open Back","Dynamic","No","No",category="Studio")
add("FOCAL_RADIANCE","Focal","Elegia","Radiance","Focal Radiance",2019,"Discontinued","Closed Back","Dynamic","No","No",notes="Bentley edition")
add("FOCAL_CLEARMGPRO","Focal","Clear","Clear MG Professional","Focal Clear MG Professional",2021,"Active","Open Back","Dynamic","No","No",category="Studio")

# ---- Grado: full Prestige/Reference/Statement, i and e generations ----
add("GRADO_SR125X","Grado","Prestige","SR125x","Grado SR125x",2021,"Active","Open Back","Dynamic","No","No",fit="On-Ear")
add("GRADO_SR225X","Grado","Prestige","SR225x","Grado SR225x",2021,"Active","Open Back","Dynamic","No","No",fit="On-Ear")
add("GRADO_SR80E","Grado","Prestige","SR80e","Grado SR80e",2014,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR80X",fit="On-Ear")
add("GRADO_SR325E","Grado","Prestige","SR325e","Grado SR325e",2014,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR325X",fit="On-Ear")
add("GRADO_RS2E","Grado","Reference","RS2e","Grado RS2e",2014,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_RS2X",fit="On-Ear")
add("GRADO_GS1000X","Grado","Statement","GS1000x","Grado GS1000x",2022,"Active","Open Back","Dynamic","No","No",fit="On-Ear")
add("GRADO_PS500E","Grado","Statement-PS","PS500e","Grado PS500e",2014,"Discontinued","Open Back","Dynamic","No","No",fit="On-Ear")
add("GRADO_PS1000E","Grado","Statement-PS","PS1000e","Grado PS1000e",2014,"Active","Open Back","Dynamic","No","No",notes="Pro statement flagship",fit="On-Ear")
add("GRADO_PS2000E","Grado","Statement-PS","PS2000e","Grado PS2000e",2017,"Active","Open Back","Dynamic","No","No",notes="Statement flagship",fit="On-Ear")
# ---- Meze: lower lines + variants ----
add("MEZE_99NOIR","Meze Audio","Classics","99 Classics Noir","Meze 99 Classics Noir",2017,"Active","Closed Back","Dynamic","No","No",notes="All-black variant w/ tuning tweak")
add("MEZE_109PRODESC","Meze Audio","Classics","109 Pro Descenso","Meze 109 Pro Descenso",2024,"Active","Open Back","Dynamic","No","No")
add("MEZE_EMPYREAN2","Meze Audio","Flagship","Empyrean II","Meze Empyrean II",2024,"Active","Open Back","Planar Magnetic","No","No",pred="MEZE_EMPYREAN")
add("MEZE_LIRICII","Meze Audio","Flagship","Liric II","Meze Liric II",2024,"Active","Closed Back","Planar Magnetic","No","No")

# ---- Bowers & Wilkins: earlier on-ear P-series + PX5 ----
add("BW_P3","Bowers & Wilkins","P-Series","P3","Bowers & Wilkins P3",2011,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",fit="On-Ear")
add("BW_P5S2","Bowers & Wilkins","P-Series","P5 Series 2","Bowers & Wilkins P5 Series 2",2014,"Discontinued","Closed Back","Dynamic","No","No",pred="BW_P5",category="Headphone",fit="On-Ear")
add("BW_P7WIRELESS","Bowers & Wilkins","P-Series","P7 Wireless","Bowers & Wilkins P7 Wireless",2015,"Discontinued","Closed Back","Dynamic","Yes","No")
add("BW_PX5","Bowers & Wilkins","PX","PX5","Bowers & Wilkins PX5",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",category="Headphone",notes="On-ear ANC",fit="On-Ear")
# ---- Audeze: more LCD + gaming/closed ----
add("AUDEZE_LCD2C","Audeze","LCD","LCD-2 Classic","Audeze LCD-2 Classic",2018,"Active","Open Back","Planar Magnetic","No","No")
add("AUDEZE_LCDGX","Audeze","LCD","LCD-GX","Audeze LCD-GX",2019,"Active","Open Back","Planar Magnetic","No","No",category="Gaming",notes="Open-back gaming")
add("AUDEZE_LCD4Z","Audeze","LCD","LCD-4z","Audeze LCD-4z",2017,"Active","Open Back","Planar Magnetic","No","No",notes="Low-impedance LCD-4")
add("AUDEZE_LCDXC2021","Audeze","LCD","LCD-XC (2021)","Audeze LCD-XC (2021)",2021,"Active","Closed Back","Planar Magnetic","No","No",pred="AUDEZE_LCDXC")
add("AUDEZE_CRBN2","Audeze","CRBN","CRBN2","Audeze CRBN2",2024,"Active","Open Back","Electrostatic","No","No",pred="AUDEZE_CRBN")

# ---- Gaming: more from existing brands ----
add("STEEL_ARCTIS5","SteelSeries","Arctis","Arctis 5","SteelSeries Arctis 5",2017,"Discontinued","Closed Back","Dynamic","No","No",category="Gaming")
add("STEEL_NOVA1","SteelSeries","Arctis Nova","Arctis Nova 1","SteelSeries Arctis Nova 1",2022,"Active","Closed Back","Dynamic","No","No",category="Gaming")
add("STEEL_NOVA7X","SteelSeries","Arctis Nova","Arctis Nova 7X","SteelSeries Arctis Nova 7X",2022,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")
add("STEEL_NOVAPROOMNI","SteelSeries","Arctis Nova","Arctis Nova Pro Omni","SteelSeries Arctis Nova Pro Omni",2025,"Active","Closed Back","Dynamic","Yes","Yes",category="Gaming",pred="STEEL_NOVAPRO")
add("HYPERX_CLOUD","HyperX","Cloud","Cloud","HyperX Cloud",2014,"Discontinued","Closed Back","Dynamic","No","No",category="Gaming",succ="HYPERX_CLOUD2")
add("HYPERX_CLOUD2W","HyperX","Cloud","Cloud II Wireless","HyperX Cloud II Wireless",2020,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")
add("HYPERX_CLOUDFLIGHT","HyperX","Cloud","Cloud Flight","HyperX Cloud Flight",2018,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")
add("RAZER_KRAKENKITTYV2","Razer","Kraken","Kraken Kitty V2","Razer Kraken Kitty V2",2022,"Active","Closed Back","Dynamic","No","No",category="Gaming")
add("RAZER_BARRACUDAPRO","Razer","Barracuda","Barracuda Pro","Razer Barracuda Pro",2022,"Active","Closed Back","Dynamic","Yes","Yes",category="Gaming",notes="ANC, hybrid gaming/lifestyle")
add("RAZER_BLACKSHARKV2X","Razer","BlackShark","BlackShark V2 X","Razer BlackShark V2 X",2020,"Active","Closed Back","Dynamic","No","No",category="Gaming")
add("LOGI_G933","Logitech G","G","G933 Artemis Spectrum","Logitech G933 Artemis Spectrum",2015,"Discontinued","Closed Back","Dynamic","Yes","No",category="Gaming")
add("LOGI_GPROXWL","Logitech G","G Pro","G Pro X Wireless","Logitech G Pro X Wireless",2020,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")
add("CORSAIR_VOID","Corsair","HS","Void RGB Elite Wireless","Corsair Void RGB Elite Wireless",2019,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")
add("TB_STEALTH600G2","Turtle Beach","Stealth","Stealth 600 Gen 2","Turtle Beach Stealth 600 Gen 2",2020,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")
add("TB_STEALTHPRO2","Turtle Beach","Stealth","Stealth Pro II","Turtle Beach Stealth Pro II",2025,"Active","Closed Back","Dynamic","Yes","Yes",category="Gaming",pred="TB_STEALTHPRO")

# ---- Consumer: deepen B&O, JBL, Marshall, Skullcandy, Bose gaming-adjacent ----
add("BO_H4","Bang & Olufsen","Beoplay","Beoplay H4","Bang & Olufsen Beoplay H4",2017,"Discontinued","Closed Back","Dynamic","Yes","No",fit="On-Ear")
add("BO_H9","Bang & Olufsen","Beoplay","Beoplay H9","Bang & Olufsen Beoplay H9",2017,"Discontinued","Closed Back","Dynamic","Yes","Yes",fit="On-Ear")
add("BO_PORTAL","Bang & Olufsen","Beoplay Portal","Beoplay Portal","Bang & Olufsen Beoplay Portal",2021,"Active","Closed Back","Dynamic","Yes","Yes",category="Gaming",notes="Gaming/lifestyle hybrid")
add("JBL_LIVE770NC","JBL","Live","Live 770NC","JBL Live 770NC",2023,"Active","Closed Back","Dynamic","Yes","Yes")
add("JBL_QUANTUM910","JBL","Quantum","Quantum 910 Wireless","JBL Quantum 910 Wireless",2022,"Active","Closed Back","Dynamic","Yes","Yes",category="Gaming")
add("MARSHALL_MIDANC","Marshall","Monitor","Mid ANC","Marshall Mid ANC",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",category="Headphone",fit="On-Ear")
add("SKULL_HESH3","Skullcandy","Crusher","Hesh 3","Skullcandy Hesh 3",2018,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone")
add("SKULL_CRUSHERANC","Skullcandy","Crusher","Crusher ANC","Skullcandy Crusher ANC",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="SKULL_CRUSHERANC2")

# ============================================================================
# DEEPENING BATCH 3 — Beats history, consumer catalogs, more gaming
# ============================================================================

# ---- Beats: full over-ear/on-ear history ----
add("BEATS_STUDIO2013","Beats","Studio","Studio (2013)","Beats Studio (2013)",2013,"Discontinued","Closed Back","Dynamic","No","Yes",succ="BEATS_STUDIO2",notes="Redesigned wired Studio")
add("BEATS_MIXR","Beats","Pro","Mixr","Beats Mixr",2011,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",notes="DJ on-ear, David Guetta",fit="On-Ear")
add("BEATS_PRO","Beats","Pro","Pro","Beats Pro",2011,"Discontinued","Closed Back","Dynamic","No","No",notes="All-metal over-ear")
add("BEATS_EXECUTIVE","Beats","Executive","Executive","Beats Executive",2012,"Discontinued","Closed Back","Dynamic","No","Yes",notes="Aluminum ANC over-ear")
add("BEATS_SOLO2","Beats","Solo","Solo 2","Beats Solo 2",2014,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",succ="BEATS_SOLO3",fit="On-Ear")
add("BEATS_SOLOPRO","Beats","Solo","Solo Pro","Beats Solo Pro",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",category="Headphone",notes="On-ear ANC",fit="On-Ear")
add("BEATS_EP","Beats","Solo","EP","Beats EP",2016,"Active","Closed Back","Dynamic","No","No",category="Headphone",notes="Budget wired on-ear",fit="On-Ear")
# ---- Sony: h.ear and earlier NC line ----
add("SONY_MDR100ABN","Sony","h.ear","MDR-100ABN","Sony MDR-100ABN (h.ear on)",2015,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="SONY_WHH900N",notes="h.ear series ANC")
add("SONY_MDR100AAP","Sony","h.ear","MDR-100AAP","Sony MDR-100AAP (h.ear on)",2015,"Discontinued","Closed Back","Dynamic","No","No")
add("SONY_MDR10R","Sony","MDR","MDR-10R","Sony MDR-10R",2013,"Discontinued","Closed Back","Dynamic","No","No")
add("SONY_MDR10RBT","Sony","MDR","MDR-10RBT","Sony MDR-10RBT",2013,"Discontinued","Closed Back","Dynamic","Yes","No")

# ---- JBL: Everest + Tune over-ear lines ----
add("JBL_EVEREST700","JBL","Everest","Everest 700","JBL Everest 700",2015,"Discontinued","Closed Back","Dynamic","Yes","No")
add("JBL_EVEREST710","JBL","Everest","Everest 710","JBL Everest 710",2016,"Discontinued","Closed Back","Dynamic","Yes","No")
add("JBL_EVERESTELITE750","JBL","Everest","Everest Elite 750NC","JBL Everest Elite 750NC",2016,"Discontinued","Closed Back","Dynamic","Yes","Yes")
add("JBL_TUNE750","JBL","Tune","Tune 750BTNC","JBL Tune 750BTNC",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes")
add("JBL_TUNE760","JBL","Tune","Tune 760NC","JBL Tune 760NC",2021,"Active","Closed Back","Dynamic","Yes","Yes")
add("JBL_TUNE770","JBL","Tune","Tune 770NC","JBL Tune 770NC",2023,"Active","Closed Back","Dynamic","Yes","Yes")

# ---- Skullcandy: Hesh + Crusher line ----
add("SKULL_HESH2","Skullcandy","Hesh","Hesh 2 Wireless","Skullcandy Hesh 2 Wireless",2015,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone")
add("SKULL_HESHANC","Skullcandy","Hesh","Hesh ANC","Skullcandy Hesh ANC",2020,"Active","Closed Back","Dynamic","Yes","Yes",category="Headphone")
add("SKULL_HESHEVO","Skullcandy","Hesh","Hesh Evo","Skullcandy Hesh Evo",2020,"Active","Closed Back","Dynamic","Yes","No",category="Headphone")
add("SKULL_CRUSHER540","Skullcandy","Crusher","Crusher 540 Active","Skullcandy Crusher 540 Active",2025,"Active","Closed Back","Dynamic","Yes","No",category="Headphone",notes="Sensory bass, fitness-focused")

# ---- Marshall: full Major + Monitor line ----
add("MARSHALL_MAJOR2","Marshall","Major","Major II","Marshall Major II",2014,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",succ="MARSHALL_MAJOR3",fit="On-Ear")
add("MARSHALL_MAJOR3","Marshall","Major","Major III","Marshall Major III",2018,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone",pred="MARSHALL_MAJOR2",succ="MARSHALL_MAJOR4",fit="On-Ear")
add("MARSHALL_MONITOR","Marshall","Monitor","Monitor","Marshall Monitor",2013,"Discontinued","Closed Back","Dynamic","No","No",succ="MARSHALL_MONITOR2")
add("MARSHALL_MONITOR3","Marshall","Monitor","Monitor III ANC","Marshall Monitor III ANC",2024,"Active","Closed Back","Dynamic","Yes","Yes",pred="MARSHALL_MONITOR2",notes="100hr battery")

# ---- Anker Soundcore + Technics deepen ----
add("ANKER_LIFEQ30","Anker Soundcore","Space","Life Q30","Anker Soundcore Life Q30",2020,"Active","Closed Back","Dynamic","Yes","Yes")
add("ANKER_LIFEQ20","Anker Soundcore","Space","Life Q20","Anker Soundcore Life Q20",2019,"Active","Closed Back","Dynamic","Yes","Yes")
add("TECH_EAHA800M2","Technics","EAH","EAH-A800M2","Technics EAH-A800M2",2025,"Active","Closed Back","Dynamic","Yes","Yes",pred="TECH_EAHA800")

# ---- More gaming from existing brands ----
add("RAZER_KRAKENV4","Razer","Kraken","Kraken V4","Razer Kraken V4",2025,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")
add("RAZER_BLACKSHARKV3","Razer","BlackShark","BlackShark V3","Razer BlackShark V3",2025,"Active","Closed Back","Dynamic","No","No",category="Gaming")
add("STEEL_NOVA5X","SteelSeries","Arctis Nova","Arctis Nova 5X","SteelSeries Arctis Nova 5X",2024,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")
add("LOGI_G935","Logitech G","G","G935","Logitech G935",2019,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")
add("ASTRO_A40","Astro Gaming","A-Series","A40 TR Gen 2","Astro A40 TR (Gen 2)",2019,"Active","Open Back","Dynamic","No","No",category="Gaming")
add("CORSAIR_HS80MAX","Corsair","HS","HS80 Max Wireless","Corsair HS80 Max Wireless",2023,"Active","Closed Back","Dynamic","Yes","No",category="Gaming")

# ============================================================================
# PRE-2010 LEGACY CLASSICS — older models from brands already in the DB
# ============================================================================

# ---- Sennheiser ----
add("SENN_HD414","Sennheiser","HD Classic","HD 414","Sennheiser HD 414",1968,"Discontinued","Open Back","Dynamic","No","No",notes="World's first open-back hi-fi headphone")
add("SENN_HD580","Sennheiser","HD","HD 580 Precision","Sennheiser HD 580 Precision",1991,"Discontinued","Open Back","Dynamic","No","No",succ="SENN_HD600",notes="Direct ancestor of the HD 600")
add("SENN_HD540","Sennheiser","HD Classic","HD 540 Reference","Sennheiser HD 540 Reference",1985,"Discontinued","Open Back","Dynamic","No","No")
add("SENN_HD25_1","Sennheiser","HD","HD 25-1","Sennheiser HD 25-1",1988,"Legacy Active","Closed Back","Dynamic","No","No",category="Studio",notes="On-ear monitoring/DJ standard",fit="On-Ear")
add("SENN_HD555","Sennheiser","HD 500-series","HD 555","Sennheiser HD 555",2005,"Discontinued","Open Back","Dynamic","No","No",succ="SENN_HD558")
add("SENN_HD595","Sennheiser","HD 500-series","HD 595","Sennheiser HD 595",2005,"Discontinued","Open Back","Dynamic","No","No",succ="SENN_HD598")
add("SENN_HD280PRO","Sennheiser","HD 200-series","HD 280 Pro","Sennheiser HD 280 Pro",2003,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Studio monitoring staple")
add("SENN_HD202","Sennheiser","HD 200-series","HD 202","Sennheiser HD 202",2003,"Discontinued","Closed Back","Dynamic","No","No",fit="On-Ear")
add("SENN_PX100","Sennheiser","HD Classic","PX 100","Sennheiser PX 100",2003,"Discontinued","Open Back","Dynamic","No","No",category="Headphone",notes="Portable on-ear",fit="On-Ear")
add("SENN_PX200","Sennheiser","HD Classic","PX 200","Sennheiser PX 200",2004,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",fit="On-Ear")
add("SENN_HE60","Sennheiser","HD Classic","HE 60 (Orpheus)","Sennheiser HE 60 / HEV 70",1991,"Discontinued","Open Back","Electrostatic","No","No",notes="Baby Orpheus electrostatic")

# ---- Sony ----
add("SONY_MDRSA5000","Sony","Qualia/SA","MDR-SA5000","Sony MDR-SA5000",2004,"Discontinued","Open Back","Dynamic","No","No",notes="Lightweight magnesium open-back")
add("SONY_MDRR10","Sony","Qualia/SA","MDR-R10","Sony MDR-R10",1989,"Discontinued","Closed Back","Dynamic","No","No",notes="Legendary wood-cup flagship")
add("SONY_MDRCD3000","Sony","Qualia/SA","MDR-CD3000","Sony MDR-CD3000",1991,"Discontinued","Closed Back","Dynamic","No","No")
add("SONY_QUALIA010","Sony","Qualia/SA","Qualia 010 (MDR-Q010)","Sony Qualia 010",2004,"Discontinued","Open Back","Dynamic","No","No",notes="Qualia-series flagship")
add("SONY_MDRV600","Sony","MDR Studio","MDR-V600","Sony MDR-V600",1992,"Discontinued","Closed Back","Dynamic","No","No",category="Studio")
add("SONY_MDR7509HD","Sony","MDR Studio","MDR-7509HD","Sony MDR-7509HD",2003,"Discontinued","Closed Back","Dynamic","No","No",category="Studio",notes="Larger-driver pro model")
add("SONY_MDRXB700","Sony","XB","MDR-XB700","Sony MDR-XB700",2009,"Discontinued","Closed Back","Dynamic","No","No",notes="Original Extra Bass over-ear")

# ---- AKG ----
add("AKG_K1000","AKG","K-Reference","K1000","AKG K1000",1989,"Discontinued","Open Back","Dynamic","No","No",notes="Ear-speaker, hinged off-ear design")
add("AKG_K240SEXTETT","AKG","K-Reference","K240 Sextett","AKG K240 Sextett",1979,"Discontinued","Semi-Open","Dynamic","No","No",notes="Passive-radiator classic")
add("AKG_K340","AKG","K-Reference","K340","AKG K340",1978,"Discontinued","Closed Back","Hybrid","No","No",notes="Dynamic + electrostatic hybrid")
add("AKG_K501","AKG","K-Reference","K501","AKG K501",1995,"Discontinued","Open Back","Dynamic","No","No",succ="AKG_K601")
add("AKG_K601","AKG","K-Reference","K601","AKG K601",2005,"Discontinued","Open Back","Dynamic","No","No",pred="AKG_K501")
add("AKG_K271","AKG","K-Studio","K271 Studio","AKG K271 Studio",2003,"Discontinued","Closed Back","Dynamic","No","No",category="Studio",succ="AKG_K271MK2")
add("AKG_K141","AKG","K-Studio","K141 Studio","AKG K141 Studio",2003,"Active","Semi-Open","Dynamic","No","No",category="Studio")

# ---- Beyerdynamic ----
add("BEYER_DT48","Beyerdynamic","DT Classic","DT 48","Beyerdynamic DT 48",1937,"Discontinued","Closed Back","Dynamic","No","No",notes="Among the oldest headphones in continuous production")
add("BEYER_DT831","Beyerdynamic","DT Classic","DT 831","Beyerdynamic DT 831",1994,"Discontinued","Closed Back","Dynamic","No","No")
add("BEYER_DT880_2005","Beyerdynamic","DT","DT 880 Edition (2005)","Beyerdynamic DT 880 Edition (2005)",2005,"Active","Semi-Open","Dynamic","No","No",pred="BEYER_DT880",notes="Consumer Edition revision")
add("BEYER_DT150","Beyerdynamic","DT Classic","DT 150","Beyerdynamic DT 150",1980,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Broadcast monitoring classic")
add("BEYER_DT100","Beyerdynamic","DT Classic","DT 100","Beyerdynamic DT 100",1965,"Legacy Active","Closed Back","Dynamic","No","No",category="Studio",notes="Broadcast/studio staple")

# ---- Audio-Technica ----
add("ATECH_M50","Audio-Technica","M-Series","ATH-M50","Audio-Technica ATH-M50",2007,"Discontinued","Closed Back","Dynamic","No","No",category="Studio",succ="ATECH_M50X",notes="The original M50, fixed cable")
add("ATECH_ESW9","Audio-Technica","ESW/ES","ATH-ESW9","Audio-Technica ATH-ESW9",2006,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",notes="Portable wood on-ear")
add("ATECH_ES7","Audio-Technica","ESW/ES","ATH-ES7","Audio-Technica ATH-ES7",2005,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone")
add("ATECH_AD2000","Audio-Technica","A-Series","ATH-AD2000","Audio-Technica ATH-AD2000",2005,"Discontinued","Open Back","Dynamic","No","No",succ="ATECH_AD2000X")
add("ATECH_L3000","Audio-Technica","W-Series","ATH-L3000","Audio-Technica ATH-L3000",2002,"Discontinued","Closed Back","Dynamic","No","No",notes="Leather-wrapped wood flagship")
add("ATECH_W1000","Audio-Technica","W-Series","ATH-W1000","Audio-Technica ATH-W1000",2002,"Discontinued","Closed Back","Dynamic","No","No",succ="ATECH_W1000Z")

# ---- Grado ----
add("GRADO_SR60","Grado","Vintage","SR60","Grado SR60",1991,"Discontinued","Open Back","Dynamic","No","No",notes="The headphone that launched the Prestige line",fit="On-Ear")
add("GRADO_RS1","Grado","Reference","RS1","Grado RS1",1994,"Discontinued","Open Back","Dynamic","No","No",notes="Original mahogany Reference",fit="On-Ear")
add("GRADO_SR325I","Grado","Prestige","SR325i","Grado SR325i",2008,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR325E",fit="On-Ear")
add("GRADO_GS1000","Grado","Statement","GS1000","Grado GS1000",2006,"Discontinued","Open Back","Dynamic","No","No",notes="First Statement-series, large bowl pads",fit="On-Ear")
add("GRADO_PS1000","Grado","Statement-PS","PS1000","Grado PS1000",2009,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_PS1000E",fit="On-Ear")
# ---- Bose ----
add("BOSE_TRIPORT","Bose","TriPort/QC Legacy","TriPort","Bose TriPort",2003,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",succ="BOSE_AE2")
add("BOSE_QC2","Bose","TriPort/QC Legacy","QuietComfort 2","Bose QuietComfort 2",2003,"Discontinued","Closed Back","Dynamic","No","Yes",notes="Defined consumer ANC")
add("BOSE_QC15","Bose","QuietComfort","QuietComfort 15","Bose QuietComfort 15",2009,"Discontinued","Closed Back","Dynamic","No","Yes",succ="BOSE_QC25",notes="Hugely popular wired ANC")

# ---- Philips ----
add("PHIL_SHP2000","Philips","SHP","SHP2000","Philips SHP2000",2008,"Discontinued","Open Back","Dynamic","No","No")

# ---- Ultrasone / Denon / Fostex legacy ----
add("ULTRA_HFI580","Ultrasone","Edition","HFI-580","Ultrasone HFI-580",2008,"Discontinued","Closed Back","Dynamic","No","No",notes="S-Logic surround positioning")
add("DENON_D2000","Denon","AH-D","AH-D2000","Denon AH-D2000",2007,"Discontinued","Closed Back","Dynamic","No","No",notes="Beloved bio-cellulose closed-back")
add("DENON_D5000","Denon","AH-D","AH-D5000","Denon AH-D5000",2007,"Discontinued","Closed Back","Dynamic","No","No",notes="Mahogany-cup classic")
add("FOSTEX_TH900","Fostex","TH","TH900","Fostex TH900",2011,"Discontinued","Closed Back","Dynamic","No","No",succ="FOSTEX_TH900MK2",notes="Original urushi-lacquer flagship")

# ============================================================================
# COMPLETE-THE-BRANDS BATCH — remaining gaps in the current 42
# ============================================================================

# ---- Philips: Fidelio L line + budget over-ear ----
add("PHIL_L1","Philips","Fidelio","L1","Philips Fidelio L1",2012,"Discontinued","Open Back","Dynamic","No","No",notes="First Fidelio over-ear flagship")
add("PHIL_L4","Philips","Fidelio","L4","Philips Fidelio L4",2024,"Active","Closed Back","Dynamic","Yes","Yes",pred="PHIL_L3",notes="Wireless ANC flagship")
add("PHIL_SHP9600","Philips","SHP","SHP9600","Philips SHP9600",2020,"Active","Open Back","Dynamic","No","No",pred="PHIL_SHP9500")
add("PHIL_H8505","Philips","Fidelio","Fidelio H1","Philips Fidelio H1",2014,"Discontinued","Open Back","Dynamic","No","No",category="Headphone")

# ---- Shure: full SRH studio/DJ line ----
add("SHURE_SRH240A","Shure","SRH","SRH240A","Shure SRH240A",2011,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("SHURE_SRH440","Shure","SRH","SRH440","Shure SRH440",2009,"Active","Closed Back","Dynamic","No","No",category="Studio",succ="SHURE_SRH440A")
add("SHURE_SRH440A","Shure","SRH","SRH440A","Shure SRH440A",2023,"Active","Closed Back","Dynamic","No","No",category="Studio",pred="SHURE_SRH440")
add("SHURE_SRH840","Shure","SRH","SRH840","Shure SRH840",2009,"Active","Closed Back","Dynamic","No","No",category="Studio",succ="SHURE_SRH840A")
add("SHURE_SRH840A","Shure","SRH","SRH840A","Shure SRH840A",2023,"Active","Closed Back","Dynamic","No","No",category="Studio",pred="SHURE_SRH840")
add("SHURE_SRH750DJ","Shure","SRH-DJ","SRH750DJ","Shure SRH750DJ",2010,"Discontinued","Closed Back","Dynamic","No","No",category="Studio")
add("SHURE_SRH940","Shure","SRH","SRH940","Shure SRH940",2011,"Discontinued","Closed Back","Dynamic","No","No",category="Studio")
add("SHURE_SRH1440","Shure","SRH","SRH1440","Shure SRH1440",2012,"Active","Open Back","Dynamic","No","No",category="Studio")
add("SHURE_AONIC40","Shure","AONIC","AONIC 40","Shure AONIC 40",2022,"Active","Closed Back","Dynamic","Yes","Yes")

# ---- ZMF: complete dynamic + closed range ----
add("ZMF_EIKON","ZMF Headphones","Eikon","Eikon","ZMF Eikon",2016,"Active","Closed Back","Dynamic","No","No",notes="Bio-cellulose closed-back")
add("ZMF_ATTICUS","ZMF Headphones","Atticus","Atticus","ZMF Atticus",2016,"Active","Closed Back","Dynamic","No","No",notes="Warm 'ZMF house sound'")
add("ZMF_AEOLUS","ZMF Headphones","Atticus","Aeolus","ZMF Aeolus",2018,"Active","Open Back","Dynamic","No","No",notes="Open-back Atticus sibling")
add("ZMF_ATRIUMCLOSED","ZMF Headphones","Atrium","Atrium Closed","ZMF Atrium Closed",2023,"Active","Closed Back","Dynamic","No","No")
add("ZMF_BOKEHOPEN","ZMF Headphones","Bokeh","Bokeh Open","ZMF Bokeh Open",2024,"Active","Open Back","Dynamic","No","No")
add("ZMF_BOKEHCLOSED","ZMF Headphones","Bokeh","Bokeh Closed","ZMF Bokeh Closed",2024,"Active","Closed Back","Dynamic","No","No")
add("ZMF_CALDERACLOSED","ZMF Headphones","Caldera","Caldera Closed","ZMF Caldera Closed",2024,"Active","Closed Back","Planar Magnetic","No","No",pred="ZMF_CALDERA")

# ---- Stax: fuller electrostatic Lambda + Omega lines ----
add("STAX_SR007","Stax","SR","SR-007 (Omega II)","Stax SR-007 mk2",2003,"Active","Open Back","Electrostatic","No","No",notes="Omega II reference")
add("STAX_SRL300","Stax","Lambda","SR-L300","Stax SR-L300",2015,"Active","Open Back","Electrostatic","No","No")
add("STAX_SRL500","Stax","Lambda","SR-L500","Stax SR-L500",2015,"Active","Open Back","Electrostatic","No","No")
add("STAX_SRL700MK2","Stax","Lambda","SR-L700 MK2","Stax SR-L700 MK2",2020,"Active","Open Back","Electrostatic","No","No",pred="STAX_SRL700")
add("STAX_SR404","Stax","Lambda","SR-404 Signature","Stax SR-404 Signature",2002,"Discontinued","Open Back","Electrostatic","No","No")

# ---- Final Audio: Sonorous closed line ----
add("FINAL_SONOROUS3","Final Audio","Sonorous","Sonorous III","Final Audio Sonorous III",2014,"Discontinued","Closed Back","Dynamic","No","No")
add("FINAL_SONOROUS6","Final Audio","Sonorous","Sonorous VI","Final Audio Sonorous VI",2014,"Discontinued","Closed Back","Dynamic","No","No")
add("FINAL_SONOROUSX","Final Audio","Sonorous","Sonorous X","Final Audio Sonorous X",2015,"Discontinued","Closed Back","Dynamic","No","No",notes="Flagship closed dynamic")

# ---- Abyss: Diana TC + 1266 variants ----
add("ABYSS_DIANATC","Abyss","Diana TC","Diana TC","Abyss Diana TC",2021,"Active","Open Back","Planar Magnetic","No","No",notes="Diana with TC driver tech")
add("ABYSS_DIANAMR","Abyss","Diana","Diana MR","Abyss Diana MR",2023,"Active","Open Back","Planar Magnetic","No","No")

# ---- Sony: MA open-back + recent studio reference ----
add("SONY_MDRMA900","Sony","MA","MDR-MA900","Sony MDR-MA900",2012,"Discontinued","Open Back","Dynamic","No","No",notes="Lightweight 70mm open-back")
add("SONY_MDRMV1","Sony","MA","MDR-MV1","Sony MDR-MV1",2023,"Active","Open Back","Dynamic","No","No",category="Studio",notes="Open-back studio reference")
add("SONY_MDRM1","Sony","MA","MDR-M1","Sony MDR-M1",2024,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Modern studio monitor")

# ---- Audeze: remaining LCD + headset ----
add("AUDEZE_LCD24","Audeze","LCD","LCD-24","Audeze LCD-24 (Anniversary)",2023,"Active","Open Back","Planar Magnetic","No","No",notes="Limited anniversary LCD")
add("AUDEZE_PENROSE","Audeze","Maxwell","Penrose","Audeze Penrose",2020,"Discontinued","Closed Back","Planar Magnetic","Yes","No",category="Gaming",notes="Wireless gaming predecessor to Maxwell")

# ---- Meze: 99 line + IEM-adjacent over-ear ----
add("MEZE_99CLASSICSWALNUT","Meze Audio","Classics","99 Classics Walnut Gold","Meze 99 Classics Walnut Gold",2015,"Active","Closed Back","Dynamic","No","No",notes="Standard walnut/gold finish")

# ============================================================================
# NEW BRANDS
# ============================================================================

# ---- Koss ----
add("KOSS_PORTAPRO","Koss","Porta Pro","Porta Pro","Koss Porta Pro",1984,"Legacy Active","Open Back","Dynamic","No","No",category="Headphone",notes="Iconic on-ear, in production since 1984",fit="On-Ear")
add("KOSS_PORTAPROWL","Koss","Porta Pro","Porta Pro Wireless","Koss Porta Pro Wireless",2020,"Active","Open Back","Dynamic","Yes","No",category="Headphone",fit="On-Ear")
add("KOSS_KSC75","Koss","KSC","KSC75","Koss KSC75",1998,"Active","Open Back","Dynamic","No","No",category="Headphone",notes="Cult-favorite clip-on",fit="On-Ear")
add("KOSS_KPH30I","Koss","KPH","KPH30i","Koss KPH30i",2018,"Active","Open Back","Dynamic","No","No",category="Headphone",notes="Budget audiophile on-ear; wide soundstage",fit="On-Ear")
add("KOSS_PRO4AA","Koss","Pro","Pro4AA","Koss Pro4AA",1970,"Discontinued","Closed Back","Dynamic","No","No",category="Studio",notes="Vintage studio classic")
add("KOSS_ESP95X","Koss","Pro","ESP/95X","Koss ESP/95X",2015,"Active","Open Back","Electrostatic","No","No",notes="Electrostatic system w/ energizer")

# ---- V-Moda ----
add("VMODA_LP","V-Moda","Crossfade","Crossfade LP","V-Moda Crossfade LP",2010,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone")
add("VMODA_LP2","V-Moda","Crossfade","Crossfade LP2","V-Moda Crossfade LP2",2012,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",pred="VMODA_LP")
add("VMODA_M100","V-Moda","Crossfade","Crossfade M-100","V-Moda Crossfade M-100",2012,"Discontinued","Closed Back","Dynamic","No","No",succ="VMODA_M100MASTER",notes="DJ/production favorite")
add("VMODA_M100MASTER","V-Moda","Crossfade","Crossfade M-100 Master","V-Moda Crossfade M-100 Master",2019,"Active","Closed Back","Dynamic","No","No",pred="VMODA_M100")
add("VMODA_CROSSFADE2WL","V-Moda","Crossfade","Crossfade 2 Wireless","V-Moda Crossfade 2 Wireless",2016,"Active","Closed Back","Dynamic","Yes","No")
add("VMODA_M200","V-Moda","M-200","M-200","V-Moda M-200",2019,"Active","Closed Back","Dynamic","No","No",category="Studio")

# ---- Yamaha ----
add("YAMAHA_HPH200","Yamaha","HPH","HPH-200","Yamaha HPH-200",2013,"Discontinued","Open Back","Dynamic","No","No")
add("YAMAHA_HPHMT8","Yamaha","HPH","HPH-MT8","Yamaha HPH-MT8",2016,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("YAMAHA_YHL700A","Yamaha","YH","YH-L700A","Yamaha YH-L700A",2021,"Active","Closed Back","Dynamic","Yes","Yes",notes="3D field ANC")
add("YAMAHA_YHE700A","Yamaha","YH","YH-E700A","Yamaha YH-E700A",2021,"Active","Closed Back","Dynamic","Yes","Yes")
add("YAMAHA_HP1","Yamaha","HPH","HP-1","Yamaha HP-1",1976,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Orthodynamic classic by Mark Levinson")

# ---- Pioneer ----
add("PIONEER_SEMONITOR5","Pioneer","SE-Monitor","SE-Monitor 5","Pioneer SE-Monitor 5",2017,"Active","Closed Back","Dynamic","No","No",notes="Flagship hi-res closed-back")
add("PIONEER_SEMASTER1","Pioneer","SE-Monitor","SE-Master 1","Pioneer SE-Master 1",2015,"Discontinued","Open Back","Dynamic","No","No",notes="Hand-built flagship")
add("PIONEER_HDJX10","Pioneer","HDJ","HDJ-X10","Pioneer HDJ-X10",2017,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Pro DJ headphone")
add("PIONEER_HDJ2000","Pioneer","HDJ","HDJ-2000","Pioneer HDJ-2000",2010,"Discontinued","Closed Back","Dynamic","No","No",category="Studio")

# ---- AIAIAI ----
add("AIAIAI_TMA1","AIAIAI","TMA","TMA-1","AIAIAI TMA-1",2010,"Discontinued","Closed Back","Dynamic","No","No",category="Studio",succ="AIAIAI_TMA2")
add("AIAIAI_TMA2","AIAIAI","TMA","TMA-2 (Modular)","AIAIAI TMA-2 Modular",2015,"Active","Closed Back","Dynamic","No","No",category="Studio",pred="AIAIAI_TMA1",notes="Fully modular system")
add("AIAIAI_TMA2STUDIO","AIAIAI","TMA","TMA-2 Studio","AIAIAI TMA-2 Studio",2018,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("AIAIAI_TMA2WL","AIAIAI","TMA","TMA-2 Studio Wireless+","AIAIAI TMA-2 Studio Wireless+",2021,"Active","Closed Back","Dynamic","Yes","No",category="Studio")

# ---- 1More ----
add("1MORE_SONOFLOW","1More","SonoFlow","SonoFlow","1More SonoFlow",2022,"Active","Closed Back","Dynamic","Yes","Yes",notes="Budget ANC value pick")
add("1MORE_SONOFLOWSE","1More","SonoFlow","SonoFlow SE","1More SonoFlow SE",2023,"Active","Closed Back","Dynamic","Yes","Yes")
add("1MORE_MK802","1More","SonoFlow","MK802 Bluetooth","1More MK802 Bluetooth",2017,"Discontinued","Closed Back","Dynamic","Yes","No")

# ---- Edifier ----
add("EDIFIER_STAXGT1","Edifier","STAX Spirit","STAX Spirit S3","Edifier STAX Spirit S3",2022,"Active","Closed Back","Planar Magnetic","Yes","No",notes="Planar under licensed STAX Spirit brand")
add("EDIFIER_STAXGT5","Edifier","STAX Spirit","STAX Spirit S5","Edifier STAX Spirit S5",2024,"Active","Closed Back","Planar Magnetic","Yes","No")
add("EDIFIER_W820NB","Edifier","WH","W820NB","Edifier W820NB",2021,"Active","Closed Back","Dynamic","Yes","Yes")
add("EDIFIER_WH950NB","Edifier","WH","WH950NB","Edifier WH950NB",2023,"Active","Closed Back","Dynamic","Yes","Yes")

# ---- Cleer ----
add("CLEER_FLOW2","Cleer","Flow/Enduro","Flow II","Cleer Flow II",2019,"Active","Closed Back","Dynamic","Yes","Yes")
add("CLEER_ENDURO100","Cleer","Flow/Enduro","Enduro 100","Cleer Enduro 100",2020,"Active","Closed Back","Dynamic","Yes","No",notes="100hr battery")
add("CLEER_ALPHA","Cleer","Flow/Enduro","Alpha","Cleer Alpha",2022,"Active","Closed Back","Dynamic","Yes","Yes")

# ---- Austrian Audio ----
add("AUSTRIAN_HIX55","Austrian Audio","Hi-X","Hi-X55","Austrian Audio Hi-X55",2019,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("AUSTRIAN_HIX65","Austrian Audio","Hi-X","Hi-X65","Austrian Audio Hi-X65",2020,"Active","Open Back","Dynamic","No","No",category="Studio")
add("AUSTRIAN_HIX60","Austrian Audio","Hi-X","Hi-X60","Austrian Audio Hi-X60",2022,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("AUSTRIAN_THECOMPOSER","Austrian Audio","Hi-X","The Composer","Austrian Audio The Composer",2022,"Active","Open Back","Dynamic","No","No",notes="Flagship open-back")

# ---- Neumann ----
add("NEUMANN_NDH20","Neumann","NDH","NDH 20","Neumann NDH 20",2019,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Studio reference closed-back")
add("NEUMANN_NDH30","Neumann","NDH","NDH 30","Neumann NDH 30",2021,"Active","Open Back","Dynamic","No","No",category="Studio",notes="Open-back studio reference")

# ---- Moondrop ----
add("MOONDROP_VENUS","Moondrop","Planar","Venus","Moondrop Venus",2022,"Active","Open Back","Planar Magnetic","No","No",notes="First Moondrop over-ear planar")
add("MOONDROP_PARA","Moondrop","Planar","Para","Moondrop Para",2023,"Active","Open Back","Planar Magnetic","No","No",notes="Value planar")
add("MOONDROP_COSMO","Moondrop","Planar","Cosmo","Moondrop Cosmo",2023,"Active","Open Back","Planar Magnetic","No","No",notes="Flagship planar")

# ---- Sivga ----
add("SIVGA_PHOENIX","Sivga","Open","Phoenix","Sivga Phoenix",2021,"Active","Open Back","Dynamic","No","No")
add("SIVGA_PII","Sivga","Open","P-II","Sivga P-II",2021,"Active","Open Back","Planar Magnetic","No","No",notes="Also sold as Sendy Aiva")
add("SIVGA_SV021","Sivga","Open","SV021 Robin","Sivga SV021 Robin",2022,"Active","Open Back","Dynamic","No","No")
add("SIVGA_ORIOLE","Sivga","Open","Oriole","Sivga Oriole",2023,"Active","Open Back","Dynamic","No","No")

# ---- Sendy Audio ----
add("SENDY_AIVA","Sendy Audio","Flagship","Aiva","Sendy Audio Aiva",2019,"Active","Open Back","Planar Magnetic","No","No",notes="Zebrawood planar")
add("SENDY_PEACOCK","Sendy Audio","Flagship","Peacock","Sendy Audio Peacock",2021,"Active","Open Back","Planar Magnetic","No","No",notes="Four-coil 88mm planar flagship")
add("SENDY_APOLLO","Sendy Audio","Flagship","Apollo","Sendy Audio Apollo",2023,"Active","Open Back","Planar Magnetic","No","No")

# ---- FiiO ----
add("FIIO_FT3","FiiO","FT","FT3","FiiO FT3",2023,"Active","Open Back","Dynamic","No","No",notes="60mm dynamic open-back")
add("FIIO_FT5","FiiO","FT","FT5","FiiO FT5",2024,"Active","Open Back","Planar Magnetic","No","No",notes="Value planar flagship")
add("FIIO_FT1","FiiO","FT","FT1","FiiO FT1",2024,"Active","Closed Back","Dynamic","No","No")
add("FIIO_FT1PRO","FiiO","FT","FT1 Pro","FiiO FT1 Pro",2025,"Active","Open Back","Planar Magnetic","No","No")

# ---- Spirit Torino ----
add("SPIRITTORINO_SUPER","Spirit Torino","Flagship","Super Leggera","Spirit Torino Super Leggera",2019,"Active","Open Back","Dynamic","No","No",notes="Hand-built Italian flagship")
add("SPIRITTORINO_RADIANTE","Spirit Torino","Flagship","Radiante","Spirit Torino Radiante",2021,"Active","Closed Back","Dynamic","No","No")

# ---- Warwick Acoustics ----
add("WARWICK_SONOMA","Warwick Acoustics","Sonoma","Sonoma Model One","Warwick Acoustics Sonoma Model One",2017,"Active","Open Back","Electrostatic","No","No",notes="Electrostatic system w/ amp/DAC")
add("WARWICK_APERIO","Warwick Acoustics","Sonoma","Aperio","Warwick Acoustics Aperio",2019,"Active","Open Back","Electrostatic","No","No",notes="Reference electrostatic system")

# ---- Mark Levinson ----
add("MARKLEV_5909","Mark Levinson","No. 5909","No. 5909","Mark Levinson No. 5909",2022,"Active","Closed Back","Dynamic","Yes","Yes",notes="High-end wireless ANC")

# ---- T+A ----
add("TA_SOLITAIRE_P","T+A","Solitaire","Solitaire P","T+A Solitaire P",2020,"Active","Open Back","Planar Magnetic","No","No",notes="Flagship planar")
add("TA_SOLITAIRE_PSE","T+A","Solitaire","Solitaire P-SE","T+A Solitaire P-SE",2021,"Active","Open Back","Planar Magnetic","No","No")
add("TA_SOLITAIRE_T","T+A","Solitaire","Solitaire T","T+A Solitaire T",2023,"Active","Closed Back","Dynamic","Yes","Yes",notes="Wireless ANC")

# ============================================================================
# NEWEST MAKERS + 2025-2026 MODELS
# ============================================================================

# ---- HEDD Audio (Germany, AMT/dynamic studio) ----
add("HEDD_HEDDPHONE","HEDD Audio","HEDDphone","HEDDphone","HEDD Audio HEDDphone",2020,"Discontinued","Open Back","AMT","No","No",category="Studio",succ="HEDD_HEDDPHONE2",notes="World's first full-range AMT (Air Motion Transformer) headphone")
add("HEDD_HEDDPHONE2","HEDD Audio","HEDDphone","HEDDphone TWO","HEDD Audio HEDDphone TWO",2023,"Active","Open Back","AMT","No","No",category="Studio",pred="HEDD_HEDDPHONE",notes="AMT driver, improved comfort")
add("HEDD_HEDDPHONED1","HEDD Audio","HEDDphone","HEDDphone D1","HEDD Audio HEDDphone D1",2025,"Active","Open Back","Dynamic","No","No",category="Studio",notes="50mm TPCD dynamic driver, $799")

# ---- Grell Audio (Germany, by ex-Sennheiser Axel Grell) ----
add("GRELL_OAE2","Grell Audio","OAE","OAE2","Grell Audio OAE2",2026,"Active","Open Back","Dynamic","No","No",notes="40mm bio-cellulose, angled OAE drivers, $599")

# ---- Ollo Audio (Slovenia, modular studio) ----
add("OLLO_S4X","Ollo Audio","S-Series","S4X","Ollo Audio S4X",2021,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("OLLO_S5X","Ollo Audio","S-Series","S5X","Ollo Audio S5X",2022,"Active","Open Back","Dynamic","No","No",category="Studio")
add("OLLO_X1","Ollo Audio","X-Series","X1","Ollo Audio X1",2023,"Active","Open Back","Dynamic","No","No",category="Studio",notes="Reference open-back")

# ---- HiFiMan: 2025 launches ----
add("HIFIMAN_HE600","HiFiMan","HE","HE600","HiFiMan HE600",2025,"Active","Open Back","Planar Magnetic","No","No",notes="Ultra-thin diaphragm, $799")
add("HIFIMAN_EDITIONXV","HiFiMan","Edition","Edition XV","HiFiMan Edition XV",2025,"Active","Open Back","Planar Magnetic","No","No")

# ---- Moondrop: wireless + on-ear additions ----
add("MOONDROP_HORIZON","Moondrop","Planar","Horizon","Moondrop Horizon",2025,"Active","Open Back","Dynamic","No","No",notes="Dynamic driver, low-distortion")
add("MOONDROP_EDGE","Moondrop","Wireless","Edge","Moondrop Edge",2024,"Active","Closed Back","Dynamic","Yes","Yes",notes="First Moondrop over-ear wireless ANC")
add("MOONDROP_OLDFASHIONED","Moondrop","On-Ear","Old Fashioned","Moondrop Old Fashioned",2025,"Active","Open Back","Dynamic","No","No",category="Headphone",notes="$25 retro on-ear, 40mm driver")

# ---- FiiO: FT1 Pro already added? add if missing ----
# (FIIO_FT1PRO added in new-brands batch)

# ---- Audeze: 2026 LCD-S20 ----
add("AUDEZE_LCDS20","Audeze","LCD","LCD-S20","Audeze LCD-S20",2025,"Active","Open Back","Planar Magnetic","No","No",notes="Accessible LCD line w/ SLAM, $499")

# ---- Sennheiser: 2026 HD 480 Pro studio ----
add("SENN_HD480PRO","Sennheiser","HD 200-series","HD 480 Pro","Sennheiser HD 480 Pro",2026,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Closed studio, flexible cable")

# ---- Grado: 2026 Signature ----
add("GRADO_S550","Grado","Statement","Signature S550","Grado Signature S550",2026,"Active","Open Back","Dynamic","No","No",notes="Debuted CanJam NYC 2026",fit="On-Ear")
# ---- Sennheiser: HD 490 Pro ----
add("SENN_HD490PRO","Sennheiser","HD","HD 490 PRO","Sennheiser HD 490 PRO",2024,"Active","Open Back","Dynamic","No","No",category="Studio",notes="Open-frame architecture; two swappable pad sets for mixing vs producing")

# ---- AKG: K872, K175, K275 ----
add("AKG_K872","AKG","K","K872","AKG K872",2016,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Flagship closed-back; 53mm 1.5 Tesla drivers")
add("AKG_K175","AKG","K","K175","AKG K175",2018,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="On-ear foldable; road-tough design",fit="On-Ear")
add("AKG_K275","AKG","K","K275","AKG K275",2018,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Over-ear foldable version of K175")

# ---- Monoprice Monolith ----
add("MONO_M1060","Monoprice","Monolith","M1060","Monoprice Monolith M1060",2017,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Budget planar flagship; 106mm driver")
add("MONO_M1060C","Monoprice","Monolith","M1060C","Monoprice Monolith M1060C",2018,"Discontinued","Closed Back","Planar Magnetic","No","No",notes="Closed-back variant of M1060")
add("MONO_M1070","Monoprice","Monolith","M1070","Monoprice Monolith M1070",2019,"Active","Open Back","Planar Magnetic","No","No",succ="",notes="Updated M1060; 106mm driver, removable cable")
add("MONO_M570","Monoprice","Monolith","M570","Monoprice Monolith M570",2019,"Active","Open Back","Planar Magnetic","No","No",notes="Mid-range planar; zebra wood cups")
add("MONO_M650","Monoprice","Monolith","M650","Monoprice Monolith M650",2018,"Active","Open Back","Dynamic","No","No",notes="Budget open-back dynamic")
add("MONO_M1570","Monoprice","Monolith","M1570","Monoprice Monolith M1570",2020,"Active","Open Back","Planar Magnetic","No","No",notes="Flagship planar; angled drivers")

# ---- Superlux ----
add("SUPERLUX_HD668B","Superlux","HD","HD668B","Superlux HD668B",2010,"Active","Semi-Open","Dynamic","No","No",category="Studio",notes="Budget studio icon; semi-open semi-AKG design")
add("SUPERLUX_HD681","Superlux","HD","HD681","Superlux HD681",2008,"Active","Semi-Open","Dynamic","No","No",category="Studio",notes="Entry-level semi-open; popular for gaming and monitoring")
add("SUPERLUX_HD681EVO","Superlux","HD","HD681 EVO","Superlux HD681 EVO",2014,"Active","Semi-Open","Dynamic","No","No",category="Studio",notes="Revised HD681 with velour pads")
add("SUPERLUX_HD669","Superlux","HD","HD669","Superlux HD669",2010,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Closed-back counterpart to HD668B")
add("SUPERLUX_HD662EVO","Superlux","HD","HD662 EVO","Superlux HD662 EVO",2014,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Improved HD662 with better pad comfort")
add("SUPERLUX_HD330","Superlux","HD","HD330","Superlux HD330",2013,"Active","Open Back","Dynamic","No","No",notes="Music-tuned open-back; more relaxed than studio line")

# ---- Samson ----
add("SAMSON_SR850","Samson","SR","SR850","Samson SR850",2006,"Active","Semi-Open","Dynamic","No","No",category="Studio",notes="Budget semi-open classic; self-adjusting headband")
add("SAMSON_SR950","Samson","SR","SR950","Samson SR950",2008,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Closed-back companion to SR850")

# ---- Status Audio ----
add("STATUS_CB1","Status Audio","CB","CB-1","Status Audio CB-1",2016,"Active","Closed Back","Dynamic","No","No",notes="Unbranded studio monitor; popular value pick")
add("STATUS_BTONE","Status Audio","BT","BT One","Status Audio BT One",2019,"Active","Closed Back","Dynamic","Yes","No",notes="Wireless on-ear; no branding; portable focus")

# ---- Jabra Evolve2 (professional UC headsets) ----
add("JABRA_E230","Jabra","Evolve2","Evolve2 30","Jabra Evolve2 30",2021,"Active","Closed Back","Dynamic","No","No",category="Headphone",notes="Wired UC stereo headset; Teams/UC certified")
add("JABRA_E240","Jabra","Evolve2","Evolve2 40","Jabra Evolve2 40",2021,"Active","Closed Back","Dynamic","No","No",category="Headphone",notes="Wired stereo headset with USB; pro-grade mic")
add("JABRA_E255","Jabra","Evolve2","Evolve2 55","Jabra Evolve2 55",2022,"Active","Closed Back","Dynamic","Yes","Yes",category="Headphone",notes="Wireless UC headset; ANC; Teams certified")
add("JABRA_E265","Jabra","Evolve2","Evolve2 65","Jabra Evolve2 65",2021,"Active","Closed Back","Dynamic","Yes","No",category="Headphone",notes="Wireless UC stereo headset; no ANC")
add("JABRA_E275","Jabra","Evolve2","Evolve2 75","Jabra Evolve2 75",2021,"Active","Closed Back","Dynamic","Yes","Yes",category="Headphone",notes="8-mic ANC wireless; leading UC headset")
add("JABRA_E285","Jabra","Evolve2","Evolve2 85","Jabra Evolve2 85",2021,"Active","Closed Back","Dynamic","Yes","Yes",category="Headphone",notes="Flagship wireless ANC; hidden boom arm")

# ---- Harman Kardon ----
add("HK_SOHO","Harman Kardon","SOHO","SOHO","Harman Kardon SOHO",2013,"Discontinued","Closed Back","Dynamic","No","No",notes="Stylish on-ear; premium build",fit="On-Ear")
add("HK_SOHOWL","Harman Kardon","SOHO","SOHO Wireless","Harman Kardon SOHO Wireless",2014,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Wireless on-ear companion to SOHO",fit="On-Ear")
add("HK_SOHOWNC","Harman Kardon","SOHO","SOHO Wireless NC","Harman Kardon SOHO Wireless NC",2017,"Discontinued","Closed Back","Dynamic","Yes","Yes",notes="SOHO with active noise cancellation",fit="On-Ear")
add("HK_FLY","Harman Kardon","FLY","FLY","Harman Kardon FLY",2019,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Lightweight travel wireless")
add("HK_FLYANC","Harman Kardon","FLY","FLY ANC","Harman Kardon FLY ANC",2020,"Active","Closed Back","Dynamic","Yes","Yes",notes="Travel wireless with ANC; 40mm drivers")

# ---- Oppo PM series (discontinued 2018; respected audiophile planars) ----
add("OPPO_PM1","Oppo","PM","PM-1","Oppo PM-1",2014,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Flagship planar; 85x69mm driver; genuine leather")
add("OPPO_PM2","Oppo","PM","PM-2","Oppo PM-2",2014,"Discontinued","Open Back","Planar Magnetic","No","No",pred="OPPO_PM1",notes="PM-1 with OFC cable, slightly lighter")
add("OPPO_PM3","Oppo","PM","PM-3","Oppo PM-3",2014,"Discontinued","Closed Back","Planar Magnetic","No","No",notes="World's first portable closed-back planar; 55mm driver")

# ---- Creative (Aurvana Live! is a budget beloved classic) ----
add("CREATIVE_AVLIVE","Creative","Aurvana","Aurvana Live!","Creative Aurvana Live!",2010,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget cult classic; biodynamic driver from Denon AH-D1001",fit="On-Ear")
add("CREATIVE_AVLIVE2","Creative","Aurvana","Aurvana Live! 2","Creative Aurvana Live! 2",2012,"Discontinued","Closed Back","Dynamic","No","No",succ="CREATIVE_SXFLAIR",pred="CREATIVE_AVLIVE",fit="On-Ear")
add("CREATIVE_SXFLAIR","Creative","Aurvana","SXFI Air","Creative SXFI Air",2019,"Active","Closed Back","Dynamic","Yes","No",notes="Super X-Fi holographic audio; built-in DAC")

# ---- Rode NTH-100 (popular studio headphone) ----
add("RODE_NTH100","Rode","NTH","NTH-100","Rode NTH-100",2022,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="40mm reference closed-back; rotating earcups; detachable cable")

# ---- Klipsch ----
add("KLIPSCH_HP3","Klipsch","Heritage","Heritage HP-3","Klipsch Heritage HP-3",2017,"Active","Open Back","Dynamic","No","No",notes="Walnut or cherry wood; 52mm driver; heritage aesthetic")
add("KLIPSCH_REFONE","Klipsch","Reference","Reference ONE","Klipsch Reference ONE",2017,"Active","Closed Back","Dynamic","No","No",notes="Oval ear design; oval-shaped 40mm driver",fit="On-Ear")
# ---- RAAL (ribbon driver headphones) ----
add("RAAL_SR1A","RAAL","Ribbon","SR1a","RAAL SR1a",2019,"Active","Open Back","Ribbon","No","No",notes="True ribbon driver headphone; requires interface box; speaker-like sound")
add("RAAL_CA1A","RAAL","Ribbon","CA1a","RAAL CA1a",2022,"Active","Open Back","Ribbon","No","No",notes="CA version of SR1a; closed-able with included attachment")

# ---- Fostex RP and TH additions ----
add("FOSTEX_T20RPMK3","Fostex","RP","T20RP Mk3","Fostex T20RP MK3",2015,"Active","Open Back","Planar Magnetic","No","No",category="Studio",notes="Open-back RP studio; modding platform")
add("FOSTEX_T40RPMK3","Fostex","RP","T40RP Mk3","Fostex T40RP MK3",2015,"Active","Closed Back","Planar Magnetic","No","No",category="Studio",notes="Closed-back RP studio; modding platform")
add("FOSTEX_T50RPMK3","Fostex","RP","T50RP Mk3","Fostex T50RP MK3",2015,"Active","Semi-Open","Planar Magnetic","No","No",category="Studio",notes="The original headphone modding platform; RP driver")
add("FOSTEX_T50RPMK4","Fostex","RP","T50RP Mk4","Fostex T50RP MK4",2022,"Active","Semi-Open","Planar Magnetic","No","No",category="Studio",pred="FOSTEX_T50RPMK3",notes="Updated RP driver; detachable cable added")
add("FOSTEX_T60RP","Fostex","RP","T60RP","Fostex T60RP",2018,"Active","Semi-Open","Planar Magnetic","No","No",category="Studio",notes="Top of the RP studio line")
add("FOSTEX_THXOO","Fostex","TH","TH-X00","Fostex TH-X00",2015,"Discontinued","Closed Back","Dynamic","No","No",notes="Massdrop collab; biodynamic 50mm; mahogany/purpleheart/ebony variants")
add("FOSTEX_TH600","Fostex","TH","TH600","Fostex TH600",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="Mid-tier lacquer closed-back; predecessor to TH900")
add("FOSTEX_TH500RP","Fostex","TH","TH500RP","Fostex TH500RP",2014,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Open planar from Fostex; RP driver in TH chassis")

# ---- Yamaha additions ----
add("YAMAHA_YH5000SE","Yamaha","YH","YH-5000SE","Yamaha YH-5000SE",2022,"Active","Open Back","Planar Magnetic","No","No",notes="Flagship orthodynamic; made in Japan; 5Hz-70kHz")
add("YAMAHA_YH4000","Yamaha","YH","YH-4000","Yamaha YH-4000",2024,"Active","Open Back","Planar Magnetic","No","No",notes="Open orthodynamic; step below YH-5000SE")
add("YAMAHA_HPHMT220","Yamaha","HPH","HPH-MT220","Yamaha HPH-MT220",2016,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Studio closed-back; flat reference tuning")

# ---- Sony additions ----
add("SONY_INZONEH3","Sony","INZONE","INZONE H3","Sony INZONE H3",2022,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Wired gaming headset; 40mm drivers")
add("SONY_INZONEH7","Sony","INZONE","INZONE H7","Sony INZONE H7",2022,"Active","Closed Back","Dynamic","Yes","No",category="Gaming",notes="Wireless gaming; no ANC")
add("SONY_INZONEH9","Sony","INZONE","INZONE H9","Sony INZONE H9",2022,"Active","Closed Back","Dynamic","Yes","Yes",category="Gaming",notes="Wireless gaming with ANC; flagship INZONE")
add("SONY_MDR7520","Sony","MDR","MDR-7520","Sony MDR-7520",2011,"Discontinued","Closed Back","Dynamic","No","No",category="Studio",notes="Pro studio closed-back; 50mm driver")

# ---- Audeze additions ----
add("AUDEZE_EL8O","Audeze","EL-8","EL-8 Open","Audeze EL-8 Open",2015,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Entry-level Audeze planar; thin-film driver")
add("AUDEZE_EL8C","Audeze","EL-8","EL-8 Closed","Audeze EL-8 Closed",2015,"Discontinued","Closed Back","Planar Magnetic","No","No",notes="Closed-back entry Audeze")
add("AUDEZE_LCDMX4","Audeze","LCD","LCD-MX4","Audeze LCD-MX4",2017,"Active","Open Back","Planar Magnetic","No","No",notes="High efficiency 106mm planar; 1.5 Tesla Fluxor magnets")
add("AUDEZE_MOBIUS","Audeze","Gaming","Mobius","Audeze Mobius",2018,"Active","Closed Back","Planar Magnetic","Yes","Yes",category="Gaming",notes="3D planar gaming headset; head tracking; Waves Nx audio")

# ---- Beyerdynamic additions ----
add("BEYER_DT1350","Beyerdynamic","DT","DT 1350","Beyerdynamic DT 1350",2011,"Active","Closed Back","Dynamic","No","No",notes="Premium on-ear; Tesla driver; high isolation",fit="On-Ear")
add("BEYER_DT177XGO","Beyerdynamic","DT","DT 177X Go","Beyerdynamic DT 177X Go",2020,"Active","Closed Back","Dynamic","No","No",notes="Drop + Beyerdynamic collab; DT 1770 driver; 250Ω")
add("BEYER_DT250","Beyerdynamic","DT","DT 250","Beyerdynamic DT 250",1998,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Broadcast/monitoring classic; still in production")

# ---- AKG additions ----
add("AKG_Q701","AKG","K","Q701","AKG Q701",2010,"Active","Open Back","Dynamic","No","No",notes="Quincy Jones signature; K701 with bass boost port")
add("AKG_K7XX","AKG","K","K7XX","AKG K7XX",2014,"Discontinued","Open Back","Dynamic","No","No",notes="Massdrop collab K702 with K712 bass port; beloved value pick")
add("AKG_N60NC","AKG","N","N60 NC","AKG N60 NC",2016,"Discontinued","Closed Back","Dynamic","No","Yes",notes="Compact on-ear with ANC; folding",fit="On-Ear")
add("AKG_K267","AKG","K","K267 Tiesto","AKG K267 Tiesto",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="DJ collaboration; three-position bass adjustment")

# ---- Sennheiser gap fills ----
add("SENN_AMPERIOR","Sennheiser","HD","Amperior","Sennheiser Amperior",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="Aluminum-cup HD 25 variant; iPhone-compatible",fit="On-Ear")
add("SENN_HD201","Sennheiser","HD","HD 201","Sennheiser HD 201",2004,"Discontinued","Closed Back","Dynamic","No","No",notes="Entry-level budget closed-back",fit="On-Ear")
add("SENN_HD203","Sennheiser","HD","HD 203","Sennheiser HD 203",2006,"Discontinued","Closed Back","Dynamic","No","No",notes="DJ-oriented entry-level",fit="On-Ear")
add("SENN_HD219","Sennheiser","HD","HD 219","Sennheiser HD 219",2010,"Discontinued","Closed Back","Dynamic","No","No",fit="On-Ear")
add("SENN_HD229","Sennheiser","HD","HD 229","Sennheiser HD 229",2010,"Discontinued","Closed Back","Dynamic","No","No",fit="On-Ear")
add("SENN_HD238","Sennheiser","HD","HD 238","Sennheiser HD 238",2008,"Discontinued","Open Back","Dynamic","No","No",notes="Portable open-back; popular value pick in its era",fit="On-Ear")
add("SENN_GAMEONE","Sennheiser","HD","GAME ONE","Sennheiser GAME ONE",2014,"Active","Open Back","Dynamic","No","No",category="Gaming",notes="Open-back gaming headset; HD 558 driver")
add("SENN_GSP600","Sennheiser","HD","GSP 600","Sennheiser GSP 600",2018,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Pro closed-back gaming; broadcast-quality boom mic")
add("SENN_GSP300","Sennheiser","HD","GSP 300","Sennheiser GSP 300",2017,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Entry gaming closed-back")

# ---- Koss additions ----
add("KOSS_KPH40","Koss","KPH","KPH40 Utility","Koss KPH40 Utility",2022,"Active","Open Back","Dynamic","No","No",category="Headphone",notes="KPH30i successor; on-ear; wide soundstage for price",fit="On-Ear")
add("KOSS_KPH7","Koss","KPH","KPH7","Koss KPH7",1985,"Legacy Active","Open Back","Dynamic","No","No",category="Headphone",notes="Classic folding on-ear; budget favorite",fit="On-Ear")
# ---- Dan Clark Audio historical ----
add("DCA_ETHERFLOW","Dan Clark Audio","Ether","Ether Flow","Dan Clark Audio Ether Flow",2016,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Tuning filter system; MrSpeakers era")
add("DCA_ETHERCFLOW","Dan Clark Audio","Ether","Ether C Flow","Dan Clark Audio Ether C Flow",2016,"Discontinued","Closed Back","Planar Magnetic","No","No",notes="Closed-back Ether Flow; MrSpeakers era")
add("DCA_AEONOPEN","Dan Clark Audio","Aeon","Aeon Open","Dan Clark Audio Aeon Open",2018,"Discontinued","Open Back","Planar Magnetic","No","No",notes="Open-back Aeon; foldable planar")

# ---- JBL gaming/consumer gap fill ----
add("JBL_QUANTUM100","JBL","Quantum","Quantum 100","JBL Quantum 100",2020,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Entry gaming wired headset")
add("JBL_QUANTUM400","JBL","Quantum","Quantum 400","JBL Quantum 400",2020,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Gaming headset with USB and RGB")
add("JBL_QUANTUM800","JBL","Quantum","Quantum 800","JBL Quantum 800",2020,"Active","Closed Back","Dynamic","Yes","Yes",category="Gaming",notes="Wireless ANC gaming flagship")
add("JBL_QUANTUMONE","JBL","Quantum","Quantum ONE","JBL Quantum ONE",2020,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Top-tier JBL gaming; head-tracking surround")

# ---- Denon historical ----
add("DENON_D7000","Denon","AH-D","AH-D7000","Denon AH-D7000",2007,"Discontinued","Closed Back","Dynamic","No","No",notes="Mahogany flagship; biodynamic 50mm driver")
add("DENON_D7100","Denon","AH-D","AH-D7100","Denon AH-D7100",2012,"Discontinued","Closed Back","Dynamic","No","No",succ="DENON_D7200",pred="DENON_D7000",notes="Successor to D7000; updated driver")
add("DENON_D600","Denon","AH-D","AH-D600","Denon AH-D600",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="Mid-tier closed; walnut wood")

# ---- Yamaha YH-C3000 (new 2024 closed-back) ----
add("YAMAHA_YHC3000","Yamaha","YH","YH-C3000","Yamaha YH-C3000",2024,"Active","Closed Back","Dynamic","No","No",notes="Beech wood closed-back; Armodynamic driver")

# ---- Modhouse Audio ----
add("MODHOUSE_ARGONMK3","Modhouse Audio","Argon","Argon Mk3","Modhouse Audio Argon Mk3",2020,"Active","Semi-Open","Planar Magnetic","No","No",notes="T50RP Mk2 base with custom Argon planar driver; wildly popular mod")
add("MODHOUSE_TUNGSTEN","Modhouse Audio","Tungsten","Tungsten","Modhouse Audio Tungsten",2022,"Active","Open Back","Planar Magnetic","No","No",notes="Original planar design; not T50RP-based; open-back flagship")

# ---- Kiwi Ears ----
add("KIWIEARS_ARDOR","Kiwi Ears","Planar","Ardor","Kiwi Ears Ardor",2023,"Active","Open Back","Planar Magnetic","No","No",notes="90mm planar; acclaimed value flagship")
add("KIWIEARS_ELLIPSE","Kiwi Ears","Planar","Ellipse","Kiwi Ears Ellipse",2023,"Active","Closed Back","Planar Magnetic","No","No",notes="Closed-back 90mm planar companion to Ardor")
add("KIWIEARS_ATHEIA","Kiwi Ears","Planar","Atheia","Kiwi Ears Atheia",2024,"Active","Open Back","Planar Magnetic","No","No",notes="Successor to Ardor; improved tuning")
add("KIWIEARS_AVENTUS","Kiwi Ears","Planar","Aventus","Kiwi Ears Aventus",2024,"Active","Open Back","Planar Magnetic","No","No",notes="Mid-fi open planar")
add("KIWIEARS_DIVISION","Kiwi Ears","Planar","Division","Kiwi Ears Division",2024,"Active","Open Back","Dynamic","No","No",notes="Dynamic flagship from Kiwi Ears")

# ---- Plantronics / Poly (BackBeat consumer wireless) ----
add("PLANT_BB500","Plantronics","BackBeat","BackBeat 500","Plantronics BackBeat 500",2016,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Wireless on-ear; foldable; entry BackBeat",fit="On-Ear")
add("PLANT_BB600","Plantronics","BackBeat","BackBeat Go 600","Plantronics BackBeat Go 600",2018,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Wireless on-ear with optional ANC",fit="On-Ear")
add("PLANT_BB810","Plantronics","BackBeat","BackBeat Go 810","Plantronics BackBeat Go 810",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",notes="ANC wireless over-ear; successor to 600")

# ---- Phiaton (premium wireless, Korean design) ----
add("PHIATON_MS530","Phiaton","Chord","MS 530","Phiaton Chord MS 530",2013,"Discontinued","Closed Back","Dynamic","Yes","Yes",notes="Bluetooth + ANC; premium wireless early adopter")
add("PHIATON_MS500","Phiaton","Chord","MS 500","Phiaton Chord MS 500",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="Wired premium closed-back; wood + metal design")
add("PHIATON_PS500","Phiaton","Bridge","PS 500","Phiaton Bridge PS 500",2011,"Discontinued","Closed Back","Dynamic","No","No",notes="Over-ear flaghship; semi-open cups")
add("PHIATON_PS320","Phiaton","Bridge","PS 320","Phiaton Bridge PS 320",2011,"Discontinued","Closed Back","Dynamic","No","No",notes="Compact over-ear; wood accents",fit="On-Ear")
add("PHIATON_BT460","Phiaton","Bridge","BT 460","Phiaton Bridge BT 460",2016,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Wireless foldable; aptX; popular value wireless",fit="On-Ear")
# ---- Teufel (German consumer electronics) ----
add("TEUFEL_ZOLA","Teufel","Real","Zola","Teufel Zola",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",notes="German ANC wireless; clean tuning",fit="On-Ear")
add("TEUFEL_CAGE","Teufel","Real","CAGE","Teufel CAGE",2017,"Discontinued","Closed Back","Dynamic","No","No",notes="Wired studio-style closed-back",fit="On-Ear")
add("TEUFEL_REALBLUENC","Teufel","Real","Real Blue NC","Teufel Real Blue NC",2019,"Active","Closed Back","Dynamic","Yes","Yes",notes="ANC wireless; strong value in Europe")
add("TEUFEL_REALZ","Teufel","Real","Real Z","Teufel Real Z",2021,"Active","Open Back","Dynamic","No","No",notes="Open-back audiophile design")

# ---- House of Marley ----
add("MARLEY_PV2","House of Marley","Positive","Positive Vibration 2","House of Marley Positive Vibration 2",2017,"Active","Closed Back","Dynamic","No","No",notes="Sustainable materials; bamboo and fabric; casual on-ear",fit="On-Ear")
add("MARLEY_PV2BT","House of Marley","Positive","Positive Vibration 2 Wireless","House of Marley Positive Vibration 2 Wireless",2018,"Active","Closed Back","Dynamic","Yes","No",notes="Wireless version of PV2; 10hr battery",fit="On-Ear")
add("MARLEY_STIRIUP","House of Marley","Positive","Stir It Up Wireless","House of Marley Stir It Up Wireless",2019,"Active","Closed Back","Dynamic","Yes","No",notes="Over-ear wireless; sustainable build")
add("MARLEY_EXODUS","House of Marley","Positive","Exodus","House of Marley Exodus",2014,"Discontinued","Closed Back","Dynamic","No","No",notes="Premium over-ear; red cherry wood")

# ---- Cooler Master gaming headsets ----
add("CM_MH630","Cooler Master","MH","MH630","Cooler Master MH630",2018,"Discontinued","Closed Back","Dynamic","No","No",category="Gaming",notes="Wired gaming headset; 40mm driver")
add("CM_MH751","Cooler Master","MH","MH751","Cooler Master MH751",2019,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="40mm driver; popular gaming headset value pick")
add("CM_MH752","Cooler Master","MH","MH752","Cooler Master MH752",2019,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="MH751 with USB soundcard; surround 7.1")

# ---- Ultrasone additional (S-Logic lineup) ----
add("ULTRA_ED8","Ultrasone","Edition","Edition 8","Ultrasone Edition 8",2010,"Active","Closed Back","Dynamic","No","No",notes="S-Logic II; 40mm; Ethiopian sheepskin; flagship portable")
add("ULTRA_ED10","Ultrasone","Edition","Edition 10","Ultrasone Edition 10",2011,"Active","Open Back","Dynamic","No","No",notes="S-Logic Plus; open-back flagship; Ruthenium-plated")
add("ULTRA_ED15","Ultrasone","Edition","Edition 15","Ultrasone Edition 15",2015,"Active","Open Back","Dynamic","No","No",notes="S-Logic Plus; anniversary flagship")
add("ULTRA_HFI780","Ultrasone","HFI","HFI-780","Ultrasone HFI-780",2008,"Discontinued","Semi-Open","Dynamic","No","No",notes="S-Logic; popular semi-open; discontinued")
add("ULTRA_HFI450","Ultrasone","HFI","HFI-450","Ultrasone HFI-450",2007,"Discontinued","Closed Back","Dynamic","No","No",notes="Entry S-Logic closed-back")
add("ULTRA_HFI2400","Ultrasone","HFI","HFI-2400","Ultrasone HFI-2400",2009,"Discontinued","Semi-Open","Dynamic","No","No",notes="S-Logic Plus; higher-tier HFI")
add("ULTRA_SIGPURE","Ultrasone","Signature","Signature Pure","Ultrasone Signature Pure",2020,"Active","Closed Back","Dynamic","No","No",notes="Refined S-Logic; clean reference tuning")
add("ULTRA_TRIB7","Ultrasone","Edition","Tribute 7","Ultrasone Tribute 7",2014,"Discontinued","Closed Back","Dynamic","No","No",notes="Limited 25th anniversary; gold-plated; 700 units only")

# ---- Dan Clark Audio MrSpeakers era remaining ----
add("DCA_MADDOG","Dan Clark Audio","Ether","Mad Dog","Dan Clark Audio Mad Dog",2012,"Discontinued","Closed Back","Planar Magnetic","No","No",notes="MrSpeakers era; T50RP-based closed planar; the one that started it all")
add("DCA_VOCE","Dan Clark Audio","Ether","Voce","Dan Clark Audio Voce",2017,"Active","Open Back","Electrostatic","No","No",notes="DCA electrostatic; requires compatible energizer")
add("DCA_NOIRECLOSED","Dan Clark Audio","Ether","Noire","Dan Clark Audio Noire",2021,"Active","Closed Back","Planar Magnetic","No","No",notes="Closed-back planar; tuned for music production")

# ---- Fostex additions ----
add("FOSTEX_T50RPMK2","Fostex","RP","T50RP Mk2","Fostex T50RP MK2",2011,"Discontinued","Semi-Open","Planar Magnetic","No","No",category="Studio",pred="",succ="FOSTEX_T50RPMK3",notes="Pre-Mk3; detachable cable not yet available; still the modding base")
add("FOSTEX_TXO","Fostex","TH","T-X0","Fostex T-X0",2016,"Discontinued","Closed Back","Dynamic","No","No",notes="Biodynamic 50mm driver; base for Massdrop TH-X00; premium Fostex tech")
add("FOSTEX_TXOII","Fostex","TH","T-X0 II","Fostex T-X0 II",2019,"Active","Closed Back","Dynamic","No","No",notes="Updated T-X0 driver; improved housing")
add("FOSTEX_TR80","Fostex","RP","TR-80","Fostex TR-80",2012,"Active","Open Back","Dynamic","No","No",category="Studio",notes="Open reference monitor; large 50mm driver")
add("FOSTEX_TH616","Fostex","TH","TH616","Fostex TH616",2020,"Active","Closed Back","Dynamic","No","No",notes="Mid-tier TH closed-back; 50mm driver")

# ---- JBL CLUB series and remaining ----
add("JBL_CLUBONE","JBL","Club","CLUB ONE","JBL CLUB ONE",2020,"Active","Closed Back","Dynamic","Yes","Yes",notes="Premium ANC flagship; adaptive noise cancelling; True Adaptive Sound")
add("JBL_CLUB700","JBL","Club","CLUB 700BT","JBL CLUB 700BT",2020,"Active","Closed Back","Dynamic","Yes","No",notes="Wireless on-ear; Club series entry",fit="On-Ear")
add("JBL_CLUB950","JBL","Club","CLUB 950NC","JBL CLUB 950NC",2020,"Active","Closed Back","Dynamic","Yes","Yes",notes="ANC wireless over-ear; Club series")
add("JBL_LIVE670","JBL","Live","Live 670NC","JBL Live 670NC",2022,"Active","Closed Back","Dynamic","Yes","Yes",notes="ANC wireless on-ear; successor to Live 460NC")
add("JBL_DUETNC","JBL","Tune","Duet NC","JBL Duet NC",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",notes="ANC wireless on-ear; foldable; mid-tier",fit="On-Ear")
# ---- More Logitech G gaming headsets ----
add("LOGI_G430","Logitech G","G-Series","G430","Logitech G430",2013,"Discontinued","Closed Back","Dynamic","No","No",category="Gaming",notes="Wired surround-sound gaming; 40mm driver")
add("LOGI_G433","Logitech G","G-Series","G433","Logitech G433",2017,"Discontinued","Closed Back","Dynamic","No","No",category="Gaming",notes="Wired DTS Headphone:X 7.1 surround")
add("LOGI_G435","Logitech G","G-Series","G435 Lightspeed","Logitech G435 Lightspeed",2021,"Active","Closed Back","Dynamic","Yes","No",category="Gaming",notes="Ultra-lightweight Lightspeed wireless; 165g")
add("LOGI_G533","Logitech G","G-Series","G533","Logitech G533",2017,"Discontinued","Closed Back","Dynamic","Yes","No",category="Gaming",notes="Wireless Dolby 7.1 gaming; 40mm Pro-G driver")
add("LOGI_G635","Logitech G","G-Series","G635","Logitech G635",2018,"Discontinued","Closed Back","Dynamic","No","No",category="Gaming",notes="Wired DTS Headphone:X 2.0; 50mm")
add("LOGI_G735","Logitech G","G-Series","G735","Logitech G735",2022,"Active","Closed Back","Dynamic","Yes","No",category="Gaming",notes="Wireless; colourful customizable; target female gamers market")
add("LOGI_G930","Logitech G","G-Series","G930","Logitech G930",2011,"Discontinued","Closed Back","Dynamic","Yes","No",category="Gaming",notes="Early Logitech wireless gaming; 40mm driver")

# ---- More Razer gaming headsets ----
add("RAZER_KRAKENX","Razer","Kraken","Kraken X","Razer Kraken X",2019,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Lightweight wired Kraken; 40mm driver; 250g")
add("RAZER_KRAKENULTI","Razer","Kraken","Kraken Ultimate","Razer Kraken Ultimate",2020,"Discontinued","Closed Back","Dynamic","No","No",category="Gaming",notes="USB THX Spatial; 50mm driver; ANC mic")
add("RAZER_NARIU","Razer","Kraken","Nari Ultimate","Razer Nari Ultimate",2018,"Discontinued","Closed Back","Dynamic","Yes","No",category="Gaming",notes="Wireless with HyperSense haptic feedback")
add("RAZER_OPUS2020","Razer","Opus","Opus","Razer Opus",2020,"Discontinued","Closed Back","Dynamic","Yes","Yes",notes="Lifestyle ANC headphone; not gaming-focused")
add("RAZER_BARRACUDAX","Razer","Barracuda","Barracuda X","Razer Barracuda X",2021,"Active","Closed Back","Dynamic","Yes","No",category="Gaming",notes="Wireless multi-platform; USB-C and 2.4GHz")

# ---- More Audio-Technica ----
add("ATECH_EW9","Audio-Technica","W-Series","ATH-EW9","Audio-Technica ATH-EW9",2004,"Discontinued","Open Back","Dynamic","No","No",notes="Clip-on premium; cherrywood housing; 13.4mm driver")
add("ATECH_ES55","Audio-Technica","ESW","ATH-ES55","Audio-Technica ATH-ES55",2006,"Discontinued","Closed Back","Dynamic","No","No",notes="Portable on-ear; rosewood; gold accents")
add("ATECH_ANC70","Audio-Technica","ANC","ATH-ANC70","Audio-Technica ATH-ANC70",2013,"Discontinued","Closed Back","Dynamic","No","Yes",notes="Active noise cancelling; foldable; 40mm driver")
add("ATECH_ANC50","Audio-Technica","ANC","ATH-ANC50iS","Audio-Technica ATH-ANC50iS",2014,"Discontinued","Closed Back","Dynamic","No","Yes",notes="ANC on-ear with iOS inline remote")

# ---- AKG missing notable models ----
add("AKG_K272HD","AKG","K","K272HD","AKG K272HD",2007,"Discontinued","Semi-Open","Dynamic","No","No",category="Studio",notes="High-definition 55Ω studio semi-open; gold-plated connector")
add("AKG_K67","AKG","K","K67 Tiesto","AKG K67 Tiesto",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="On-ear DJ; companion to K267; bass-reinforced",fit="On-Ear")
add("AKG_K44","AKG","K","K44","AKG K44",2010,"Discontinued","Closed Back","Dynamic","No","No",notes="Entry budget closed-back; 32Ω")

# ---- More Sennheiser consumer budget ----
add("SENN_HD429","Sennheiser","HD","HD 429","Sennheiser HD 429",2011,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget closed; asymmetric cable; E.A.R. technology",fit="On-Ear")
add("SENN_HD439","Sennheiser","HD","HD 439","Sennheiser HD 439",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget closed; improved comfort over HD 419",fit="On-Ear")
add("SENN_HD449","Sennheiser","HD","HD 449","Sennheiser HD 449",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget closed; extra bass tuning",fit="On-Ear")
add("SENN_HD471","Sennheiser","HD","HD 471i","Sennheiser HD 471i",2016,"Discontinued","Closed Back","Dynamic","No","No",notes="Closed-back; iOS inline remote",fit="On-Ear")
add("SENN_HD515","Sennheiser","HD","HD 515","Sennheiser HD 515",2004,"Discontinued","Open Back","Dynamic","No","No",pred="",succ="SENN_HD518",notes="Mid-tier open-back; precursor to HD 518 line")

# ---- More HiFiMan (original planar era) ----
add("HIFIMAN_HE5LE","HiFiMan","HE","HE-5LE","HiFiMan HE-5LE",2011,"Discontinued","Open Back","Planar Magnetic","No","No",pred="HIFIMAN_HE500",notes="HE-5 revised for easier driving; 50Ω; precursor to HE-500")
add("HIFIMAN_HEX4","HiFiMan","HE","HE-X4","HiFiMan HE-X4",2023,"Active","Open Back","Planar Magnetic","No","No",notes="Entry planar; stealth magnet array; accessible price point")
add("HIFIMAN_HE300","HiFiMan","HE","HE-300","HiFiMan HE-300",2011,"Discontinued","Open Back","Dynamic","No","No",notes="Dynamic open-back from HiFiMan; unusual for the brand; 32Ω")

# ---- Beyerdynamic budget consumer additions ----
add("BEYER_DT231","Beyerdynamic","DT","DT 231","Beyerdynamic DT 231",2008,"Discontinued","Open Back","Dynamic","No","No",notes="Budget open-back consumer; 32Ω; entry Beyerdynamic")
add("BEYER_DT235","Beyerdynamic","DT","DT 235","Beyerdynamic DT 235",2008,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget closed consumer; 32Ω; entry Beyerdynamic")

# ---- Fostex T50RP Mk2 (new entry) ----
# Already added above

# ---- More JBL legacy (completing history) ----
add("JBL_J55","JBL","J-Series","J55i","JBL J55i",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="iOS-compatible over-ear; bass-forward consumer")
add("JBL_E65BTNC","JBL","E-Series","E65BTNC","JBL E65BTNC",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",notes="ANC wireless; 40mm driver; popular mid-tier ANC")

# ---- JVC (Victor) — Japanese wood-driver series ----
# These are iconic in Japan; rarely covered in western catalogs
add("JVC_HADX1000","JVC","HA","HA-DX1000","JVC HA-DX1000",2006,"Discontinued","Closed Back","Dynamic","No","No",notes="Mahogany closed flagship; first Victor wood-driver headphone")
add("JVC_HADX2000","JVC","HA","HA-DX2000","JVC HA-DX2000",2009,"Discontinued","Closed Back","Dynamic","No","No",notes="Refined mahogany closed flagship; Biomass Carbon Diaphragm")
add("JVC_HASW01","JVC","HA","HA-SW01","JVC HA-SW01",2013,"Discontinued","Open Back","Planar Magnetic","No","No",notes="First Victor Micro HD planar with wood; innovative isodynamic design")
add("JVC_HASW02","JVC","HA","HA-SW02","JVC HA-SW02",2016,"Discontinued","Open Back","Planar Magnetic","No","No",succ="",pred="JVC_HASW01",notes="Refined HA-SW01; improved isodynamic planar; cherrywood")
add("JVC_HAMX100Z","JVC","HA","HA-MX100-Z","JVC HA-MX100-Z",2015,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Professional studio monitor; DJ and studio use")
add("JVC_HASR75S","JVC","HA","HA-SR75S","JVC HA-SR75S",2019,"Active","Closed Back","Dynamic","No","No",notes="Solid treble on-ear; popular export model",fit="On-Ear")
# ---- Tago Studio ----
add("TAGO_T301","Tago Studio","T3","T3-01","Tago Studio T3-01",2019,"Active","Semi-Open","Dynamic","No","No",category="Studio",notes="Semi-open reference; Pentaconn 4.4mm; 1.5T driver; made in Japan")
add("TAGO_T302","Tago Studio","T3","T3-02","Tago Studio T3-02",2020,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Closed reference companion to T3-01; same 1.5T driver; made in Japan")

# ---- Takstar ----
add("TAKSTAR_PRO80","Takstar","Pro","Pro 80","Takstar Pro 80",2012,"Active","Semi-Open","Dynamic","No","No",category="Studio",notes="OEM base for Gemini, OneOdio, others; excellent budget studio value; widely rebranded")
add("TAKSTAR_PRO82","Takstar","Pro","Pro 82","Takstar Pro 82",2018,"Active","Semi-Open","Dynamic","No","No",category="Studio",notes="Updated Pro 80; replaceable earpads; improved tuning",pred="TAKSTAR_PRO80")
add("TAKSTAR_HF580","Takstar","HF","HF580","Takstar HF580",2019,"Active","Open Back","Planar Magnetic","No","No",notes="Budget open planar; large 77mm driver; punches above price")
add("TAKSTAR_HF660S","Takstar","HF","HF660S","Takstar HF660S",2022,"Active","Open Back","Planar Magnetic","No","No",notes="Updated HF580; improved 77mm planar driver",pred="TAKSTAR_HF580")
add("TAKSTAR_SR5H","Takstar","Pro","SR 5H","Takstar SR 5H",2016,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Professional DJ/studio closed-back; double-sided cable")

# ---- Goldplanar ----
add("GOLD_GL2000DS","Goldplanar","GL","GL2000 Dual-Sided","Goldplanar GL2000 Dual-Sided",2021,"Active","Open Back","Planar Magnetic","No","No",notes="Dual-sided magnet 68mm planar; strong competition at the price")
add("GOLD_GL2000SS","Goldplanar","GL","GL2000 Single-Sided","Goldplanar GL2000 Single-Sided",2021,"Active","Open Back","Planar Magnetic","No","No",notes="Single-sided version; lighter; softer sound")
add("GOLD_GL850","Goldplanar","GL","GL850","Goldplanar GL850",2022,"Active","Open Back","Planar Magnetic","No","No",notes="Mid-range open planar; 68mm driver; wood cup option")

# ---- MySphere (Austrian, successor to AKG K1000 concept) ----
add("MYSPHERE_3","MySphere","MySphere","MySphere 3","MySphere 3",2018,"Active","Open Back","Dynamic","No","No",notes="Open-air earspeaker; no earcups; 3D sound reproduction; spiritual successor to AKG K1000")
add("MYSPHERE_3X","MySphere","MySphere","MySphere 3.X","MySphere 3.X",2022,"Active","Open Back","Dynamic","No","No",notes="Updated MySphere 3; improved driver; designed by original AKG engineers")

# ---- Panasonic ----
add("PANA_RPHC800","Panasonic","RP","RP-HC800","Panasonic RP-HC800",2009,"Discontinued","Closed Back","Dynamic","No","Yes",notes="Noise-cancelling closed-back; foldable")
add("PANA_RPHT600","Panasonic","RP","RP-HT600","Panasonic RP-HT600",2003,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget closed consumer; popular in its era")
add("PANA_RPHD10","Panasonic","RP","RP-HD10","Panasonic RP-HD10",2017,"Active","Closed Back","Dynamic","No","No",notes="High-res certified; 40mm DIATONE-inspired driver")

# ---- Crosszone (Japanese crossfeed headphones) ----
add("CZ_CZ1","Crosszone","CZ","CZ-1","Crosszone CZ-1",2017,"Active","Closed Back","Dynamic","No","No",notes="Unique acoustic crossfeed via in-ear secondary drivers; eliminates headphone imaging artifacts")
add("CZ_CZ10","Crosszone","CZ","CZ-10","Crosszone CZ-10",2020,"Active","Open Back","Dynamic","No","No",notes="Open-back CZ with same acoustic crossfeed technology as CZ-1")

# ---- 2024-2025 new releases for existing brands ----
# Beyerdynamic
add("BEYER_DT770PRO_LTD","Beyerdynamic","DT","DT 770 Pro X Limited Edition","Beyerdynamic DT 770 Pro X Limited Edition",2024,"Active","Closed Back","Dynamic","No","No",notes="STELLAR.45 driver in DT 770 shell; limited colourway run",pred="BEYER_DT770PRO")
add("BEYER_DT1990MK2","Beyerdynamic","DT","DT 1990 Pro MkII","Beyerdynamic DT 1990 Pro MkII",2024,"Active","Open Back","Dynamic","No","No",pred="BEYER_DT1990",notes="New TESLA.45 driver; 30Ω; updated ear pad design")
add("BEYER_MMX300PRO","Beyerdynamic","MMX","MMX 300 Pro","Beyerdynamic MMX 300 Pro",2024,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Pro gaming closed-back; STELLAR.45 driver")
# HiFiMan
add("HIFIMAN_SUSVARAUNV","HiFiMan","HE","Susvara Unveiled","HiFiMan Susvara Unveiled",2023,"Active","Open Back","Planar Magnetic","No","No",notes="Susvara with exposed driver; limited production; premium over standard Susvara",pred="HIFIMAN_SUSVARA")
# Audeze
add("AUDEZE_LCD5S","Audeze","LCD","LCD-5S","Audeze LCD-5S",2024,"Active","Open Back","Planar Magnetic","No","No",notes="Studio-tuned LCD-5; different pad set and EQ voicing")
# Meze
add("MEZE_EMPYREAN3","Meze Audio","Flagship","Empyrean 3","Meze Audio Empyrean 3",2025,"Active","Open Back","Planar Magnetic","No","No",notes="Third-gen isodynamic planar; new Rinaro PCOCC driver")
# Sennheiser
add("SENN_HD620S","Sennheiser","HD","HD 620S","Sennheiser HD 620S",2024,"Active","Closed Back","Dynamic","No","No",notes="Closed-back addition to 600 line; shares 42mm driver with HD 660S2")
# Focal
add("FOCAL_DIABLO","Focal","Flagship","Celestee Diablo","Focal Celestee Diablo",2024,"Active","Closed Back","Dynamic","No","No",notes="Celestee variant with unique Diablo orange finish; same driver",pred="FOCAL_CELESTEE")
# Sony  
add("SONY_WH1000XM6","Sony","WH","WH-1000XM6","Sony WH-1000XM6",2025,"Active","Closed Back","Dynamic","Yes","Yes",notes="6th-gen XM flagship; 30mm driver; improved ANC",pred="SONY_WH1000XM5")

# ---- HarmonicDyne ----
add("HD_HELIOS","HarmonicDyne","Dynamic","Helios","HarmonicDyne Helios",2019,"Active","Open Back","Dynamic","No","No",notes="Debut model; 50mm bio-film driver; wood cups")
add("HD_ZEUS","HarmonicDyne","Dynamic","Zeus","HarmonicDyne Zeus",2020,"Active","Open Back","Dynamic","No","No",notes="Nickel-plated 50mm driver; walnut cups")
add("HD_POSEIDON","HarmonicDyne","Dynamic","Poseidon","HarmonicDyne Poseidon",2021,"Active","Open Back","Dynamic","No","No",notes="Upgraded bio-film driver; flagship dynamic before G200")
add("HD_BLACKHOLE","HarmonicDyne","Dynamic","Black Hole","HarmonicDyne Black Hole",2023,"Active","Semi-Open","Dynamic","No","No",notes="Carbon fiber bio-film diaphragm; accessible price")
add("HD_G200","HarmonicDyne","Planar","G200","HarmonicDyne G200",2022,"Active","Open Back","Planar Magnetic","No","No",notes="First HarmonicDyne planar; 102mm driver; flagship")

# ---- PSB (Canadian; RoomFeel psychoacoustic tuning) ----
add("PSB_M4U1","PSB","M4U","M4U 1","PSB M4U 1",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="Passive flagship; RoomFeel tuning; Harman-adjacent target",fit="On-Ear")
add("PSB_M4U2","PSB","M4U","M4U 2","PSB M4U 2",2012,"Discontinued","Closed Back","Dynamic","No","Yes",notes="ANC version of M4U 1; excellent measured performance",fit="On-Ear")
add("PSB_M4U8","PSB","M4U","M4U 8","PSB M4U 8",2017,"Active","Closed Back","Dynamic","Yes","Yes",notes="Wireless ANC; RoomFeel; Harman-inspired tuning")

# ---- E-Mu (Creative sub-brand; Fostex T-X0 base with wood cups) ----
add("EMU_TEAK","E-Mu","Wood","Teak","E-Mu Teak",2016,"Discontinued","Closed Back","Dynamic","No","No",notes="Fostex T-X0 driver; teak wood cups; biodynamic")
add("EMU_PURPLEHEART","E-Mu","Wood","Purpleheart","E-Mu Purpleheart",2016,"Discontinued","Closed Back","Dynamic","No","No",notes="Fostex T-X0 driver; purpleheart wood cups; sister to Teak")

# ---- Stax historical completeness ----
add("STAX_SR1","Stax","Lambda","SR-1","Stax SR-1",1960,"Discontinued","Open Back","Electrostatic","No","No",notes="The first Stax headphone; launched electrostatic headphones")
add("STAX_SR3","Stax","Lambda","SR-3","Stax SR-3",1966,"Discontinued","Open Back","Electrostatic","No","No",notes="Classic vintage electrostatic")
add("STAX_SR5","Stax","Lambda","SR-5","Stax SR-5",1970,"Discontinued","Open Back","Electrostatic","No","No",notes="Normal-bias classic")
add("STAX_SR84","Stax","Lambda","SR-84","Stax SR-84",1993,"Discontinued","Open Back","Electrostatic","No","No",notes="Budget Lambda Normal Bias")
add("STAX_SR207","Stax","Lambda","SR-207","Stax SR-207",2007,"Discontinued","Open Back","Electrostatic","No","No",succ="STAX_SRL300",notes="Lambda Normal Bias entry; entry into the Stax world")
add("STAX_SR507","Stax","Lambda","SR-507","Stax SR-507",2010,"Discontinued","Open Back","Electrostatic","No","No",succ="STAX_SRL500",notes="Lambda Pro Bias; mid-tier")
add("STAX_SR4070","Stax","Lambda","SR-4070","Stax SR-4070",2009,"Discontinued","Closed Back","Electrostatic","No","No",notes="Rare closed-back Stax")
add("STAX_LAMBDANOVA","Stax","Lambda","Lambda Nova Signature","Stax Lambda Nova Signature",1999,"Discontinued","Open Back","Electrostatic","No","No",notes="Pro-bias Lambda; precursor to SR-404")

# ---- Grado older / missing models ----
add("GRADO_SR125E","Grado","Prestige","SR125e","Grado SR125e",2014,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR125X",fit="On-Ear")
add("GRADO_SR125I","Grado","Prestige","SR125i","Grado SR125i",2008,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR125E",fit="On-Ear")
add("GRADO_SR225E","Grado","Prestige","SR225e","Grado SR225e",2014,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR225X",fit="On-Ear")
add("GRADO_SR225I","Grado","Prestige","SR225i","Grado SR225i",2008,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR225E",fit="On-Ear")
add("GRADO_GS3000E","Grado","Statement","GS3000e","Grado GS3000e",2015,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_GS3000X",notes="Cocobolo Statement flagship",fit="On-Ear")
add("GRADO_HF1","Grado","Heritage","HF1","Grado HF1",2005,"Discontinued","Open Back","Dynamic","No","No",notes="First Head-Fi collaboration; aluminum cups",fit="On-Ear")
add("GRADO_HF2","Grado","Heritage","HF2","Grado HF2",2009,"Discontinued","Open Back","Dynamic","No","No",notes="Second Head-Fi collaboration; mahogany cups",fit="On-Ear")
# ---- Beyerdynamic additions ----
add("BEYER_DT770M","Beyerdynamic","DT","DT 770 M","Beyerdynamic DT 770 M",2020,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Monitor variant; limited bass response; 80Ω")
add("BEYER_T50P","Beyerdynamic","T","T 50p","Beyerdynamic T 50p",2013,"Discontinued","Closed Back","Dynamic","No","No",notes="Portable Tesla; high-end on-ear for mobile use",fit="On-Ear")
add("BEYER_DT880_600","Beyerdynamic","DT","DT 880 Edition 600 Ohm","Beyerdynamic DT 880 Edition 600 Ohm",2005,"Active","Semi-Open","Dynamic","No","No",notes="High-impedance variant; intended for high-end sources/amps",pred="BEYER_DT880_2005")
add("BEYER_DT860","Beyerdynamic","DT","DT 860","Beyerdynamic DT 860",2003,"Discontinued","Closed Back","Dynamic","No","No",notes="Reference closed-back monitoring; semi-open character")

# ---- Audio-Technica A-series and other gaps ----
add("ATECH_A700","Audio-Technica","A-Series","ATH-A700","Audio-Technica ATH-A700",2003,"Discontinued","Closed Back","Dynamic","No","No",notes="Air-dynamic wing support; 53mm driver; precursor to A700X")
add("ATECH_A900X","Audio-Technica","A-Series","ATH-A900X","Audio-Technica ATH-A900X",2011,"Active","Closed Back","Dynamic","No","No",notes="53mm air dynamic; flagship A-series")
add("ATECH_AWAS","Audio-Technica","W-Series","ATH-AWAS","Audio-Technica ATH-AWAS",2019,"Active","Closed Back","Dynamic","No","No",notes="Wenge/sakura wood; 58mm driver; flagship W-series")
add("ATECH_L5000","Audio-Technica","W-Series","ATH-L5000","Audio-Technica ATH-L5000",2017,"Active","Closed Back","Dynamic","No","No",notes="Lambskin leather; 58mm driver; ultra-premium closed-back")
add("ATECH_DSR9BT","Audio-Technica","W-Series","ATH-DSR9BT","Audio-Technica ATH-DSR9BT",2016,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Full digital wireless; first to send digital signal to driver")
add("ATECH_G1","Audio-Technica","M-Series","ATH-G1","Audio-Technica ATH-G1",2019,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Wired gaming headset; lightweight; boom mic")

# ---- Sony vintage and gap fills ----
add("SONY_MDRV500","Sony","MDR","MDR-V500","Sony MDR-V500",2001,"Discontinued","Closed Back","Dynamic","No","No",notes="DJ classic; 50mm driver")
add("SONY_MDRV700","Sony","MDR","MDR-V700","Sony MDR-V700",1999,"Discontinued","Closed Back","Dynamic","No","No",notes="Iconic DJ headphone; large 50mm driver")
add("SONY_MDRSA3000","Sony","MDR","MDR-SA3000","Sony MDR-SA3000",2004,"Discontinued","Open Back","Dynamic","No","No",notes="Open-air premium; 50mm driver")
add("SONY_MDRF1","Sony","MDR","MDR-F1","Sony MDR-F1",1998,"Discontinued","Open Back","Dynamic","No","No",notes="Radical open-air baffle design; 50mm driver; no earcup")
add("SONY_MDRCD2000","Sony","MDR","MDR-CD2000","Sony MDR-CD2000",1995,"Discontinued","Open Back","Dynamic","No","No",notes="Reference flagship of its era")
add("SONY_MDRXB1000","Sony","MDR","MDR-XB1000","Sony MDR-XB1000",2010,"Discontinued","Closed Back","Dynamic","No","No",notes="Extreme bass XB flagship; 70mm driver; sub-bass focused")

# ---- Sennheiser consumer gap fills ----
add("SENN_HD205","Sennheiser","HD","HD 205","Sennheiser HD 205",2003,"Discontinued","Closed Back","Dynamic","No","No",notes="DJ-style entry closed-back; rotatable cup",fit="On-Ear")
add("SENN_HD218","Sennheiser","HD","HD 218","Sennheiser HD 218",2010,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget consumer closed",fit="On-Ear")
add("SENN_HD228","Sennheiser","HD","HD 228","Sennheiser HD 228",2010,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget bass-heavy consumer",fit="On-Ear")
add("SENN_HD239","Sennheiser","HD","HD 239","Sennheiser HD 239",2013,"Discontinued","Open Back","Dynamic","No","No",notes="Semi-open budget; warm sound",fit="On-Ear")
add("SENN_HD419","Sennheiser","HD","HD 419","Sennheiser HD 419",2012,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget closed; replaceable cable",fit="On-Ear")
add("SENN_HD424","Sennheiser","HD","HD 424","Sennheiser HD 424",1973,"Discontinued","Open Back","Dynamic","No","No",notes="Iconic vintage; one of Sennheiser's best-selling ever")
add("SENN_HD428","Sennheiser","HD","HD 428","Sennheiser HD 428",2011,"Discontinued","Closed Back","Dynamic","No","No",notes="Budget closed consumer",fit="On-Ear")
add("SENN_HD438","Sennheiser","HD","HD 438","Sennheiser HD 438",2011,"Discontinued","Closed Back","Dynamic","No","No",notes="Folding closed consumer; tangle-free cable",fit="On-Ear")
# ---- JBL consumer gap fills ----
add("JBL_E45BT","JBL","E-Series","E45BT","JBL E45BT",2016,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Wireless on-ear; 40mm driver",fit="On-Ear")
add("JBL_E55BT","JBL","E-Series","E55BT","JBL E55BT",2016,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Wireless over-ear; popular for value")
add("JBL_LIVE650","JBL","Live","Live 650BTNC","JBL Live 650BTNC",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",notes="ANC wireless; precursor to Live 660NC",succ="JBL_LIVE660")
add("JBL_LIVE400","JBL","Live","Live 400BT","JBL Live 400BT",2019,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Budget wireless on-ear",fit="On-Ear")
add("JBL_LIVE460","JBL","Live","Live 460NC","JBL Live 460NC",2021,"Active","Closed Back","Dynamic","Yes","Yes",notes="ANC on-ear; successor to E45BT line",fit="On-Ear")
add("JBL_LIVE500","JBL","Live","Live 500BT","JBL Live 500BT",2019,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Over-ear wireless; precursor to Live 660NC line")

# ---- Denon historical ----
add("DENON_D1001","Denon","AH-D","AH-D1001","Denon AH-D1001",2007,"Discontinued","Closed Back","Dynamic","No","No",notes="Biodynamic entry-level; cult favorite for the price")
add("DENON_D1100","Denon","AH-D","AH-D1100","Denon AH-D1100",2010,"Discontinued","Closed Back","Dynamic","No","No",succ="DENON_D1001",notes="Successor to D1001; improved bio-cellulose driver")
add("DENON_D400","Denon","AH-D","AH-D400","Denon AH-D400",2011,"Discontinued","Closed Back","Dynamic","No","No",notes="Entry audiophile closed-back")

# ---- Dan Clark Audio (MrSpeakers era remaining) ----
add("DCA_AEONCLOSED","Dan Clark Audio","Aeon","Aeon Closed","Dan Clark Audio Aeon Closed",2017,"Discontinued","Closed Back","Planar Magnetic","No","No",notes="Original Aeon; first compact folding DCA planar; MrSpeakers era")
add("DCA_ETHERCX","Dan Clark Audio","Ether","Ether CX","Dan Clark Audio Ether CX",2017,"Discontinued","Closed Back","Planar Magnetic","No","No",notes="Closed version of Ether C with tuning filter system")

# ---- Pioneer DJ and audiophile ----
add("PIONEER_HDJ500","Pioneer","HDJ","HDJ-500","Pioneer DJ HDJ-500",2011,"Discontinued","Closed Back","Dynamic","No","No",category="Studio",notes="DJ entry; 40mm driver")
add("PIONEER_HDJ1000","Pioneer","HDJ","HDJ-1000","Pioneer DJ HDJ-1000",2002,"Discontinued","Closed Back","Dynamic","No","No",category="Studio",notes="The DJ reference standard; 50mm driver")
add("PIONEER_SEA1000","Pioneer","SE","SE-A1000","Pioneer SE-A1000",2001,"Discontinued","Open Back","Dynamic","No","No",notes="Open-back audiophile; 50mm driver; wide soundstage")
add("PIONEER_HDJCUE1","Pioneer","HDJ","DJ HDJ-CUE1BT","Pioneer DJ HDJ-CUE1BT",2019,"Active","Closed Back","Dynamic","Yes","No",category="Studio",notes="Wireless DJ monitoring")

# ---- Audioquest (NightHawk/NightOwl family; discontinued 2019) ----
# All four share: 25Ω, 99 dB/mW, 50mm biocellulose pistonic driver
add("AQ_NIGHTHAWK","Audioquest","NightHawk","NightHawk","Audioquest NightHawk",2015,"Discontinued","Semi-Open","Dynamic","No","No",succ="AQ_NIGHTHAWKCARBON",notes="Liquid Wood cups; 50mm biocellulose; semi-open")
add("AQ_NIGHTHAWKCARBON","Audioquest","NightHawk","NightHawk Carbon","Audioquest NightHawk Carbon",2016,"Discontinued","Semi-Open","Dynamic","No","No",pred="AQ_NIGHTHAWK",notes="Updated NightHawk; carbon finish; carbon-fabric earpads")
add("AQ_NIGHTOWL","Audioquest","NightOwl","NightOwl","Audioquest NightOwl",2015,"Discontinued","Closed Back","Dynamic","No","No",succ="AQ_NIGHTOWLCARBON",notes="Closed-back companion to NightHawk; aperiodic damping")
add("AQ_NIGHTOWLCARBON","Audioquest","NightOwl","NightOwl Carbon","Audioquest NightOwl Carbon",2016,"Discontinued","Closed Back","Dynamic","No","No",pred="AQ_NIGHTOWL",notes="Updated NightOwl; carbon finish; tighter tolerances")

# ---- NAD ----
# Designed by PSB's Paul Barton (same Lenbrook group); RoomFeel tuning
add("NAD_HP50","NAD","VISO","VISO HP50","NAD VISO HP50",2014,"Discontinued","Closed Back","Dynamic","No","No",notes="Designed by PSB's Paul Barton; RoomFeel psychoacoustic tuning; Sound and Vision Top Pick 2014")

# ---- Brainwavz ----
add("BWAVZ_HM5","Brainwavz","HM","HM5","Brainwavz HM5",2012,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Budget studio reference; Sennheiser-inspired neutral tuning; popular pad-swapping base")

# ---- Beyerdynamic T-series portable additions ----
add("BEYER_T51P","Beyerdynamic","T","T 51p","Beyerdynamic T 51p",2013,"Discontinued","Closed Back","Dynamic","No","No",notes="Portable Tesla on-ear; 60Ω; premium portable",fit="On-Ear")
add("BEYER_T51I","Beyerdynamic","T","T 51i","Beyerdynamic T 51i",2013,"Discontinued","Closed Back","Dynamic","No","No",notes="T51p with 3-button iOS remote; 32Ω",fit="On-Ear")
add("BEYER_T90","Beyerdynamic","T","T 90","Beyerdynamic T 90",2012,"Discontinued","Open Back","Dynamic","No","No",notes="Open Tesla flagship; 250Ω; 102 dB sensitivity; 45mm Tesla driver")

# ---- Sennheiser Orpheus HE-1 ----
add("SENN_HE1","Sennheiser","Orpheus","Orpheus HE-1","Sennheiser Orpheus HE-1",2016,"Active","Open Back","Electrostatic","No","No",notes="~€55,000 flagship electrostatic system; built-in amp/DAC; marble and glass construction")

# ---- ZMF Ori (original; T50RP-based wood-cup closed planar) ----
add("ZMF_ORI","ZMF Headphones","Flagship","Ori","ZMF Ori",2015,"Discontinued","Closed Back","Planar Magnetic","No","No",succ="ZMF_ORI3",notes="ZMF's first headphone; T50RP Mk2 driver in handcrafted wood cups")
add("ZMF_ORI3","ZMF Headphones","Flagship","Ori 3.0","ZMF Ori 3.0",2025,"Active","Closed Back","Planar Magnetic","No","No",pred="ZMF_ORI",notes="Complete redesign; 80mm CAMS planar; torrefied Black Limba cups")

# ---- AKG vintage 600Ω models ----
add("AKG_K240DF","AKG","K","K240 DF","AKG K240 DF",1975,"Discontinued","Semi-Open","Dynamic","No","No",category="Studio",notes="Vienna-made 600Ω; diffuse-field compensation; audiophile vintage classic")
add("AKG_K240M","AKG","K","K240M","AKG K240M",1975,"Discontinued","Semi-Open","Dynamic","No","No",category="Studio",notes="Vienna-made 600Ω monitor; sibling to K240 DF; highly regarded vintage")

# ---- Monoprice M560 (distinct from M570 we have) ----
add("MONO_M560","Monoprice","Monolith","M560","Monoprice Monolith M560",2018,"Active","Semi-Open","Planar Magnetic","No","No",notes="Semi-open planar; 42Ω; wood trim; different driver from M570")

# ---- Status Audio additional models ----
add("STATUS_HDONE","Status Audio","CB","HD One","Status Audio HD One",2020,"Active","Closed Back","Dynamic","No","No",notes="Wired closed-back; unbranded; flat reference tuning")
add("STATUS_HDTWO","Status Audio","CB","HD Two","Status Audio HD Two",2021,"Active","Closed Back","Dynamic","No","No",notes="Updated HD One; detachable cable; 17Ω")
add("STATUS_OB1","Status Audio","CB","OB-1","Status Audio OB-1",2019,"Active","Open Back","Dynamic","No","No",notes="Open-back from Status; 54Ω; flat reference tuning")

# ---- AKG remaining notable models ----
add("AKG_K240MKII","AKG","K","K240 MkII","AKG K240 MkII",2006,"Active","Semi-Open","Dynamic","No","No",notes="Updated K240 with improved driver and self-adjusting headband")
add("AKG_K52","AKG","K","K52","AKG K52",2017,"Active","Closed Back","Dynamic","No","No",notes="Budget closed-back; 40mm driver; entry studio")
add("AKG_K450","AKG","K","K450","AKG K450",2010,"Discontinued","Closed Back","Dynamic","No","No",notes="Portable on-ear; foldable; 30mm driver",fit="On-Ear")
# ---- Grado Heritage Series ----
add("GRADO_GH1","Grado","Heritage","GH1","Grado GH1",2015,"Discontinued","Open Back","Dynamic","No","No",notes="Heritage Series 1; Brooklyn maple cups; limited edition",fit="On-Ear")
add("GRADO_GH2","Grado","Heritage","GH2","Grado GH2",2016,"Discontinued","Open Back","Dynamic","No","No",notes="Heritage Series 2; cocobolo wood cups; limited edition",fit="On-Ear")
add("GRADO_GH3","Grado","Heritage","GH3","Grado GH3",2018,"Discontinued","Open Back","Dynamic","No","No",notes="Heritage Series 3; Norwegian pine; on-ear S-cushions",fit="On-Ear")
add("GRADO_GH4","Grado","Heritage","GH4","Grado GH4",2018,"Discontinued","Open Back","Dynamic","No","No",pred="GRADO_GH2",notes="Heritage Series 4; Norwegian pine full-size; successor to GH2 line",fit="On-Ear")
# ---- ZMF Tessidera (2025 planar) ----
add("ZMF_TESSIDERA","ZMF Headphones","Flagship","Tessidera","ZMF Tessidera",2025,"Active","Open Back","Planar Magnetic","No","No",notes="First ZMF planar with 1-micron diaphragm; CAMS magnet system")

# ---------------------------------------------------------------------------
# Resolve family ids and build lineage from predecessor/successor links
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# SPECS backfill table — driver size (mm), impedance (ohms), sensitivity (dB)
# Keyed by product_id. Sourced from manufacturer pages / reputable spec sheets.
# Grown brand-by-brand over time; leave a field "" when not reliably published.
# ---------------------------------------------------------------------------
SPECS = {
    # ---- Sennheiser (driver size rarely published officially; impedance & sensitivity well documented) ----
    "SENN_HD600":    {"impedance": "300", "sensitivity": "97"},
    "SENN_HD650":    {"impedance": "300", "sensitivity": "103"},
    "SENN_HD660S":   {"impedance": "150", "sensitivity": "104"},
    "SENN_HD660S2":  {"impedance": "300", "sensitivity": "104", "driver_size": "38"},
    "SENN_HD700":    {"impedance": "150", "sensitivity": "103"},
    "SENN_HD800":    {"impedance": "300", "sensitivity": "102", "driver_size": "56"},
    "SENN_HD800S":   {"impedance": "300", "sensitivity": "102", "driver_size": "56"},
    "SENN_HD820":    {"impedance": "300", "sensitivity": "103", "driver_size": "56"},
    "SENN_HD560S":   {"impedance": "120", "sensitivity": "110"},
    "SENN_HD580":    {"impedance": "300", "sensitivity": "97"},
    "SENN_HD540":    {"impedance": "300", "sensitivity": "94"},
    "SENN_HD518":    {"impedance": "50",  "sensitivity": "108"},
    "SENN_HD555":    {"impedance": "50",  "sensitivity": "112"},
    "SENN_HD558":    {"impedance": "50",  "sensitivity": "112"},
    "SENN_HD598":    {"impedance": "50",  "sensitivity": "112"},
    "SENN_HD599":    {"impedance": "50",  "sensitivity": "106"},
    "SENN_HD569":    {"impedance": "23",  "sensitivity": "115"},
    "SENN_HD579":    {"impedance": "50",  "sensitivity": "106"},
    "SENN_HD595":    {"impedance": "50",  "sensitivity": "112"},
    "SENN_HD280PRO": {"impedance": "64",  "sensitivity": "113", "driver_size": "40"},
    "SENN_HD25":     {"impedance": "70",  "sensitivity": "120", "driver_size": "25"},
    "SENN_HD25_1":   {"impedance": "70",  "sensitivity": "120", "driver_size": "25"},
    "SENN_HD58X":    {"impedance": "150", "sensitivity": "104"},
    "SENN_HD6XX":    {"impedance": "300", "sensitivity": "103"},
    "SENN_HD8XX":    {"impedance": "300", "sensitivity": "102", "driver_size": "56"},
    "SENN_HD620S":   {"impedance": "150", "sensitivity": "107"},
    "SENN_MOMENTUM4":{"impedance": "18",  "sensitivity": "107", "driver_size": "42"},
    "SENN_MOMENTUM3":{"impedance": "18",  "sensitivity": "106", "driver_size": "42"},
    "SENN_MOMENTUM2":{"impedance": "18",  "sensitivity": "113", "driver_size": "42"},
    "SENN_MOMENTUM": {"impedance": "18",  "sensitivity": "110", "driver_size": "42"},
    "SENN_HD4_40BT": {"impedance": "18",  "sensitivity": "100", "driver_size": "40"},
    "SENN_HD350BT":  {"impedance": "18",  "sensitivity": "108", "driver_size": "40"},
    "SENN_HD450BT":  {"impedance": "18",  "sensitivity": "108", "driver_size": "38"},
    "SENN_PXC550":   {"impedance": "150", "sensitivity": "105", "driver_size": "40"},
    "SENN_PXC550II": {"impedance": "150", "sensitivity": "105", "driver_size": "40"},
    "SENN_HD480PRO": {"impedance": "120", "sensitivity": "108"},
    "SENN_HD400PRO": {"impedance": "120", "sensitivity": "110"},
    # ---- Beyerdynamic (DT series all use 45mm drivers; Tesla driver prefix indicates premium line) ----
    "BEYER_DT770_32":    {"impedance": "32",  "sensitivity": "102", "driver_size": "45"},
    "BEYER_DT770_80":    {"impedance": "80",  "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT770_250":   {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT770PRO":    {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT880":       {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT880_250":   {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT880_2005":  {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT990PRO":    {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT990_250":   {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT1770":      {"impedance": "250", "sensitivity": "102", "driver_size": "45"},
    "BEYER_DT1990":      {"impedance": "250", "sensitivity": "102", "driver_size": "45"},
    "BEYER_DT1990MK2":   {"impedance": "30",  "sensitivity": "94",  "driver_size": "45"},
    "BEYER_DT700PROX":   {"impedance": "48",  "sensitivity": "100", "driver_size": "45"},
    "BEYER_DT700PROX2":  {"impedance": "48",  "sensitivity": "100", "driver_size": "45"},
    "BEYER_DT900PROX":   {"impedance": "48",  "sensitivity": "100", "driver_size": "45"},
    "BEYER_T1":          {"impedance": "600", "sensitivity": "102", "driver_size": "45"},
    "BEYER_T1_2":        {"impedance": "600", "sensitivity": "102", "driver_size": "45"},
    "BEYER_T1_3":        {"impedance": "32",  "sensitivity": "100", "driver_size": "45"},
    "BEYER_T5_3":        {"impedance": "32",  "sensitivity": "100", "driver_size": "45"},
    "BEYER_AMIRON":      {"impedance": "250", "sensitivity": "102", "driver_size": "45"},
    "BEYER_DT150":       {"impedance": "250", "sensitivity": "102", "driver_size": "45"},
    "BEYER_DT100":       {"impedance": "400", "sensitivity": "115", "driver_size": "45"},
    "BEYER_DT240PRO":    {"impedance": "16",  "sensitivity": "101", "driver_size": "45"},
    "BEYER_TYGR300R":    {"impedance": "32",  "sensitivity": "102", "driver_size": "45"},
    # ---- Audio-Technica ----
    "ATECH_M20X":    {"impedance": "47", "sensitivity": "96",  "driver_size": "40"},
    "ATECH_M30X":    {"impedance": "47", "sensitivity": "98",  "driver_size": "40"},
    "ATECH_M40X":    {"impedance": "35", "sensitivity": "98",  "driver_size": "40"},
    "ATECH_M50X":    {"impedance": "38", "sensitivity": "99",  "driver_size": "45"},
    "ATECH_M50XBT":  {"impedance": "32", "sensitivity": "99",  "driver_size": "45"},
    "ATECH_M50XBT2": {"impedance": "32", "sensitivity": "99",  "driver_size": "45"},
    "ATECH_M60X":    {"impedance": "28", "sensitivity": "106", "driver_size": "45"},
    "ATECH_M70X":    {"impedance": "35", "sensitivity": "97",  "driver_size": "45"},
    "ATECH_R70X":    {"impedance": "470","sensitivity": "99"},
    "ATECH_R70XA":   {"impedance": "470","sensitivity": "99"},
    "ATECH_R50X":    {"impedance": "39", "sensitivity": "98"},
    "ATECH_R30X":    {"impedance": "44", "sensitivity": "98"},
    "ATECH_ADX5000": {"impedance": "420","sensitivity": "100", "driver_size": "58"},
    "ATECH_AD700X":  {"impedance": "38", "sensitivity": "100", "driver_size": "53"},
    "ATECH_AD900X":  {"impedance": "38", "sensitivity": "100", "driver_size": "53"},
    "ATECH_AD1000X": {"impedance": "42", "sensitivity": "100", "driver_size": "53"},
    "ATECH_MSR7":    {"impedance": "36", "sensitivity": "102", "driver_size": "45"},
    "ATECH_MSR7B":   {"impedance": "36", "sensitivity": "102", "driver_size": "45"},
    # ---- HiFiMan (planar magnetic; driver size not typically published) ----
    "HIFIMAN_HE400":     {"impedance": "50",  "sensitivity": "92"},
    "HIFIMAN_HE400I":    {"impedance": "35",  "sensitivity": "93"},
    "HIFIMAN_HE400SE":   {"impedance": "32",  "sensitivity": "91"},
    "HIFIMAN_HE400S":    {"impedance": "22",  "sensitivity": "98"},
    "HIFIMAN_HE500":     {"impedance": "38",  "sensitivity": "89"},
    "HIFIMAN_HE560":     {"impedance": "50",  "sensitivity": "90"},
    "HIFIMAN_HE6":       {"impedance": "50",  "sensitivity": "83"},
    "HIFIMAN_HE6SE":     {"impedance": "50",  "sensitivity": "86"},
    "HIFIMAN_SUNDARA":   {"impedance": "37",  "sensitivity": "94"},
    "HIFIMAN_SUNDARAC":  {"impedance": "20",  "sensitivity": "96"},
    "HIFIMAN_ANANDA":    {"impedance": "25",  "sensitivity": "103"},
    "HIFIMAN_ANANDANANO":{"impedance": "16",  "sensitivity": "103"},
    "HIFIMAN_ARYA":      {"impedance": "35",  "sensitivity": "91"},
    "HIFIMAN_ARYASTEALTH":{"impedance": "32", "sensitivity": "94"},
    "HIFIMAN_HE1000":    {"impedance": "35",  "sensitivity": "90"},
    "HIFIMAN_HE1000V2":  {"impedance": "35",  "sensitivity": "90"},
    "HIFIMAN_HE1000SE":  {"impedance": "35",  "sensitivity": "96"},
    "HIFIMAN_SUSVARA":   {"impedance": "60",  "sensitivity": "83"},
    "HIFIMAN_EDITIONXS": {"impedance": "18",  "sensitivity": "92"},
    "HIFIMAN_EDITIONX":  {"impedance": "25",  "sensitivity": "103"},
    "HIFIMAN_EDITIONXV2":{"impedance": "25",  "sensitivity": "103"},
    "HIFIMAN_HE4XX":     {"impedance": "35",  "sensitivity": "93"},
    "HIFIMAN_HE5XX":     {"impedance": "18",  "sensitivity": "91"},
    "HIFIMAN_DEVA":      {"impedance": "18",  "sensitivity": "93"},
    "HIFIMAN_DEVAPRO":   {"impedance": "18",  "sensitivity": "94"},
    # ---- AKG ----
    "AKG_K240STUDIO": {"impedance": "55",  "sensitivity": "91",  "driver_size": "30"},
    "AKG_K271MK2":    {"impedance": "55",  "sensitivity": "91",  "driver_size": "30"},
    "AKG_K271":       {"impedance": "55",  "sensitivity": "91",  "driver_size": "30"},
    "AKG_K361":       {"impedance": "32",  "sensitivity": "110", "driver_size": "50"},
    "AKG_K371":       {"impedance": "32",  "sensitivity": "114", "driver_size": "50"},
    "AKG_K550":       {"impedance": "32",  "sensitivity": "111", "driver_size": "50"},
    "AKG_K553":       {"impedance": "32",  "sensitivity": "114", "driver_size": "50"},
    "AKG_K612":       {"impedance": "120", "sensitivity": "101", "driver_size": "50"},
    "AKG_K701":       {"impedance": "62",  "sensitivity": "105", "driver_size": "50"},
    "AKG_K702":       {"impedance": "62",  "sensitivity": "105", "driver_size": "45"},
    "AKG_K712":       {"impedance": "62",  "sensitivity": "105", "driver_size": "50"},
    "AKG_K72":        {"impedance": "32",  "sensitivity": "112", "driver_size": "40"},
    "AKG_K92":        {"impedance": "32",  "sensitivity": "110", "driver_size": "40"},
    "AKG_K245":       {"impedance": "32",  "sensitivity": "109", "driver_size": "50"},
    "AKG_K812":       {"impedance": "36",  "sensitivity": "110", "driver_size": "53"},
    # ---- Focal (all flagship use 40mm drivers) ----
    "FOCAL_UTOPIA":     {"impedance": "80", "sensitivity": "104", "driver_size": "40"},
    "FOCAL_UTOPIA2022": {"impedance": "80", "sensitivity": "104", "driver_size": "40"},
    "FOCAL_ELEAR":      {"impedance": "80", "sensitivity": "104", "driver_size": "40"},
    "FOCAL_ELEX":       {"impedance": "80", "sensitivity": "104", "driver_size": "40"},
    "FOCAL_CLEAR":      {"impedance": "55", "sensitivity": "104", "driver_size": "40"},
    "FOCAL_CLEARMG":    {"impedance": "55", "sensitivity": "104", "driver_size": "40"},
    "FOCAL_CLEARPRO":   {"impedance": "55", "sensitivity": "104", "driver_size": "40"},
    "FOCAL_CLEARMGPRO": {"impedance": "55", "sensitivity": "104", "driver_size": "40"},
    "FOCAL_ELEGIA":     {"impedance": "35", "sensitivity": "105", "driver_size": "40"},
    "FOCAL_CELESTEE":   {"impedance": "35", "sensitivity": "105", "driver_size": "40"},
    "FOCAL_STELLIA":    {"impedance": "35", "sensitivity": "106", "driver_size": "40"},
    "FOCAL_RADIANCE":   {"impedance": "35", "sensitivity": "105", "driver_size": "40"},
    "FOCAL_BATHYS":     {"impedance": "35", "sensitivity": "106", "driver_size": "40"},
    "FOCAL_BATHYSMG":   {"impedance": "35", "sensitivity": "106", "driver_size": "40"},
    "FOCAL_HADENYS":    {"impedance": "55", "sensitivity": "100", "driver_size": "40"},
    "FOCAL_AZURYS":     {"impedance": "35", "sensitivity": "106", "driver_size": "40"},
    "FOCAL_LISTEN":     {"impedance": "32", "sensitivity": "116", "driver_size": "40"},
    # ---- Audeze (planar; most classic LCDs use 106mm drivers) ----
    "AUDEZE_LCD1":    {"impedance": "16",  "sensitivity": "99",  "driver_size": "90"},
    "AUDEZE_LCD2":    {"impedance": "70",  "sensitivity": "101", "driver_size": "106"},
    "AUDEZE_LCD2C":   {"impedance": "70",  "sensitivity": "101", "driver_size": "106"},
    "AUDEZE_LCD24":   {"impedance": "70",  "sensitivity": "101", "driver_size": "106"},
    "AUDEZE_LCD3":    {"impedance": "110", "sensitivity": "102", "driver_size": "106"},
    "AUDEZE_LCD4":    {"impedance": "200", "sensitivity": "97",  "driver_size": "106"},
    "AUDEZE_LCD4Z":   {"impedance": "15",  "sensitivity": "98",  "driver_size": "106"},
    "AUDEZE_LCD5":    {"impedance": "14",  "sensitivity": "90",  "driver_size": "90"},
    "AUDEZE_LCD5S":   {"impedance": "14",  "sensitivity": "92",  "driver_size": "90"},
    "AUDEZE_LCDX":    {"impedance": "20",  "sensitivity": "103", "driver_size": "106"},
    "AUDEZE_LCDXC":   {"impedance": "20",  "sensitivity": "103", "driver_size": "106"},
    "AUDEZE_LCDXC2021":{"impedance": "20", "sensitivity": "103", "driver_size": "106"},
    "AUDEZE_MM100":   {"impedance": "16",  "sensitivity": "103"},
    "AUDEZE_MM500":   {"impedance": "16",  "sensitivity": "100"},
    # ---- Meze Audio ----
    "MEZE_99CLASSICS":   {"impedance": "32",   "sensitivity": "103", "driver_size": "40"},
    "MEZE_99NEO":        {"impedance": "26",   "sensitivity": "103", "driver_size": "40"},
    "MEZE_109PRO":       {"impedance": "40",   "sensitivity": "112", "driver_size": "50"},
    "MEZE_105AER":       {"impedance": "40",   "sensitivity": "112", "driver_size": "50"},
    "MEZE_EMPYREAN":     {"impedance": "31.6", "sensitivity": "100"},
    "MEZE_EMPYREAN2":    {"impedance": "31.6", "sensitivity": "101"},
    "MEZE_ELITE":        {"impedance": "31.6", "sensitivity": "101"},
    "MEZE_LIRIC":        {"impedance": "31.6", "sensitivity": "101"},
    "MEZE_LIRIC2":       {"impedance": "31.6", "sensitivity": "102"},
    # ---- Shure ----
    "SHURE_SRH240A":  {"impedance": "44",  "sensitivity": "105", "driver_size": "40"},
    "SHURE_SRH440":   {"impedance": "44",  "sensitivity": "105", "driver_size": "40"},
    "SHURE_SRH440A":  {"impedance": "44",  "sensitivity": "105", "driver_size": "40"},
    "SHURE_SRH840":   {"impedance": "44",  "sensitivity": "99",  "driver_size": "40"},
    "SHURE_SRH840A":  {"impedance": "44",  "sensitivity": "99",  "driver_size": "40"},
    "SHURE_SRH940":   {"impedance": "42",  "sensitivity": "100", "driver_size": "40"},
    "SHURE_SRH1440":  {"impedance": "44",  "sensitivity": "100", "driver_size": "40"},
    "SHURE_SRH1540":  {"impedance": "46",  "sensitivity": "99",  "driver_size": "46"},
    "SHURE_SRH1840":  {"impedance": "65",  "sensitivity": "99",  "driver_size": "40"},
    "SHURE_AONIC50":  {"impedance": "24",  "sensitivity": "96",  "driver_size": "40"},
    "SHURE_AONIC50G2":{"impedance": "24",  "sensitivity": "96",  "driver_size": "40"},
    "SHURE_AONIC40":  {"impedance": "18",  "sensitivity": "111", "driver_size": "40"},
    # ---- Philips ----
    "PHIL_X2HR":    {"impedance": "30", "sensitivity": "100", "driver_size": "50"},
    "PHIL_SHP9500": {"impedance": "32", "sensitivity": "101", "driver_size": "50"},
    "PHIL_X3":      {"impedance": "30", "sensitivity": "100", "driver_size": "50"},
    "PHIL_X1":      {"impedance": "30", "sensitivity": "100", "driver_size": "50"},
    "PHIL_X2":      {"impedance": "30", "sensitivity": "100", "driver_size": "50"},
    # ---- Koss ----
    "KOSS_PORTAPRO":  {"impedance": "60",  "sensitivity": "101", "driver_size": "25"},
    "KOSS_KSC75":     {"impedance": "60",  "sensitivity": "101", "driver_size": "25"},
    "KOSS_KPH30I":    {"impedance": "35",  "sensitivity": "101", "driver_size": "30"},
    "KOSS_ESP95X":    {"impedance": "100", "sensitivity": "104"},
    # ---- Sony ----
    "SONY_MDR7506":    {"impedance": "63", "sensitivity": "106", "driver_size": "40"},
    "SONY_MDRV6":      {"impedance": "63", "sensitivity": "106", "driver_size": "40"},
    "SONY_MDRZ1R":     {"impedance": "64", "sensitivity": "100", "driver_size": "70"},
    "SONY_MDRMV1":     {"impedance": "24", "sensitivity": "100", "driver_size": "40"},
    "SONY_WH1000XM5":  {"impedance": "48", "sensitivity": "101", "driver_size": "30"},
    "SONY_WH1000XM4":  {"impedance": "48", "sensitivity": "101", "driver_size": "40"},
    "SONY_WH1000XM3":  {"impedance": "47", "sensitivity": "104", "driver_size": "40"},
    "SONY_MDRZ7":      {"impedance": "70", "sensitivity": "102", "driver_size": "70"},
    "SONY_MDRZ7M2":    {"impedance": "70", "sensitivity": "102", "driver_size": "70"},
    "SONY_MDR1A":      {"impedance": "24", "sensitivity": "105", "driver_size": "40"},
    "SONY_CD900ST":    {"impedance": "63", "sensitivity": "106", "driver_size": "40"},
    "SONY_MDR7510":    {"impedance": "24", "sensitivity": "106", "driver_size": "40"},
    # ---- Sony backfill (verified; wireless ANC models listed with their wired/passive figures) ----
    "SONY_MDRCD3000":  {"impedance": "32",  "sensitivity": "104", "driver_size": "50"},
    "SONY_MDRR10":     {"impedance": "40",  "sensitivity": "100", "driver_size": "50"},
    "SONY_MDRSA5000":  {"impedance": "70",  "sensitivity": "102", "driver_size": "50"},
    "SONY_MDRSA3000":  {"impedance": "70",  "sensitivity": "102", "driver_size": "50"},
    "SONY_MDRMA900":   {"impedance": "12",  "sensitivity": "103", "driver_size": "70"},
    "SONY_MDRM1":      {"impedance": "50",  "sensitivity": "102", "driver_size": "40"},
    "SONY_MDRV600":    {"impedance": "45",  "sensitivity": "106", "driver_size": "40"},
    "SONY_MDR7509HD":  {"impedance": "24",  "sensitivity": "107", "driver_size": "50"},
    "SONY_MDRXB700":   {"impedance": "24",  "sensitivity": "106", "driver_size": "50"},
    "SONY_MDR1R":      {"impedance": "24",  "sensitivity": "105", "driver_size": "40"},
    "SONY_MDR10R":     {"impedance": "24",  "sensitivity": "105", "driver_size": "40"},
    "SONY_MDR1000X":   {"impedance": "46",  "sensitivity": "103", "driver_size": "40"},
    "SONY_WH1000XM2":  {"impedance": "46",  "sensitivity": "103", "driver_size": "40"},
    "SONY_WH1000XM6":  {"impedance": "16",  "sensitivity": "100", "driver_size": "30"},
    "SONY_INZONEH7":   {"impedance": "32",  "sensitivity": "100", "driver_size": "40"},
    "SONY_ZX110":      {"impedance": "24",  "sensitivity": "98",  "driver_size": "30"},
    "SONY_ZX310":      {"impedance": "24",  "sensitivity": "98",  "driver_size": "30"},
    "SONY_ULTWEAR":    {"impedance": "16",  "sensitivity": "100", "driver_size": "40"},
    # ---- Sony consumer/vintage remaining ----
    "SONY_WHH900N":    {"impedance": "48",  "sensitivity": "101", "driver_size": "40"},
    "SONY_XB650":      {"impedance": "24",  "sensitivity": "103", "driver_size": "40"},
    "SONY_XB950B1":    {"impedance": "24",  "sensitivity": "103", "driver_size": "40"},
    "SONY_XB900N":     {"impedance": "48",  "sensitivity": "100", "driver_size": "40"},
    "SONY_XB910N":     {"impedance": "48",  "sensitivity": "103", "driver_size": "30"},
    "SONY_CH500":      {"impedance": "32",  "sensitivity": "100", "driver_size": "30"},
    "SONY_CH510":      {"impedance": "32",  "sensitivity": "98",  "driver_size": "30"},
    "SONY_CH520":      {"impedance": "32",  "sensitivity": "100", "driver_size": "30"},
    "SONY_CH700N":     {"impedance": "48",  "sensitivity": "100", "driver_size": "40"},
    "SONY_CH710N":     {"impedance": "48",  "sensitivity": "100", "driver_size": "30"},
    "SONY_CH720N":     {"impedance": "48",  "sensitivity": "100", "driver_size": "30"},
    "SONY_MDR100ABN":  {"impedance": "46",  "sensitivity": "103", "driver_size": "40"},
    "SONY_MDR100AAP":  {"impedance": "24",  "sensitivity": "105", "driver_size": "40"},
    "SONY_MDR10RBT":   {"impedance": "32",  "sensitivity": "102", "driver_size": "40"},
    "SONY_MDRCD2000":  {"impedance": "32",  "sensitivity": "106", "driver_size": "50"},
    "SONY_MDRXB700":   {"impedance": "24",  "sensitivity": "106", "driver_size": "50"},
    "SONY_ZX750BN":    {"impedance": "40",  "sensitivity": "103", "driver_size": "40"},
    # ---- Sennheiser backfill ----
    "SENN_HD550":    {"impedance": "50",  "sensitivity": "112"},
    "SENN_HD505":    {"impedance": "50",  "sensitivity": "112"},
    "SENN_HD559":    {"impedance": "50",  "sensitivity": "108"},
    "SENN_HD202":    {"impedance": "32",  "sensitivity": "111", "driver_size": "40"},
    "SENN_HD205":    {"impedance": "32",  "sensitivity": "110", "driver_size": "40"},
    "SENN_HD218":    {"impedance": "32",  "sensitivity": "115", "driver_size": "40"},
    "SENN_HD228":    {"impedance": "32",  "sensitivity": "115", "driver_size": "40"},
    "SENN_HD238":    {"impedance": "32",  "sensitivity": "112", "driver_size": "40"},
    "SENN_HD239":    {"impedance": "32",  "sensitivity": "108", "driver_size": "40"},
    "SENN_HD419":    {"impedance": "32",  "sensitivity": "110", "driver_size": "40"},
    "SENN_HD428":    {"impedance": "32",  "sensitivity": "110", "driver_size": "40"},
    "SENN_HD438":    {"impedance": "32",  "sensitivity": "110", "driver_size": "40"},
    "SENN_HD424":    {"impedance": "400", "sensitivity": "91"},
    "SENN_PX100":    {"impedance": "32",  "sensitivity": "108", "driver_size": "25"},
    "SENN_PX200":    {"impedance": "32",  "sensitivity": "108", "driver_size": "25"},
    "SENN_HD4_50BTNC":{"impedance": "18", "sensitivity": "113", "driver_size": "38"},
    "SENN_HD250BT":  {"impedance": "18",  "sensitivity": "115", "driver_size": "40"},
    "SENN_MOMENTUM5":{"impedance": "18",  "sensitivity": "107", "driver_size": "42"},
    "SENN_ACCENTUM": {"impedance": "18",  "sensitivity": "107", "driver_size": "36"},
    "SENN_ACCENTUMPLUS":{"impedance":"18","sensitivity": "107", "driver_size": "36"},
    # ---- Bose (mostly ANC wireless; impedance not officially published for most) ----
    "BOSE_QC2":      {"impedance": "30",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_QC15":     {"impedance": "30",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_QC25":     {"impedance": "30",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_QC35":     {"impedance": "32",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_QC35II":   {"impedance": "32",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_QC45":     {"impedance": "32",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_NC700":    {"impedance": "32",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_QCULTRA":  {"impedance": "32",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_QCULTRA2": {"impedance": "32",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_QCHP":     {"impedance": "32",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_QC3":      {"impedance": "30",  "sensitivity": "107", "driver_size": "40"},
    "BOSE_OE2":      {"impedance": "32",  "sensitivity": "109", "driver_size": "40"},
    "BOSE_AE2":      {"impedance": "32",  "sensitivity": "109", "driver_size": "40"},
    "BOSE_TRIPORT":  {"impedance": "32",  "sensitivity": "104", "driver_size": "40"},
    "BOSE_SOUNDLINKAE":{"impedance":"32", "sensitivity": "105", "driver_size": "40"},
    "BOSE_SOUNDLINKOE":{"impedance":"32", "sensitivity": "105", "driver_size": "40"},
    # ---- Bowers & Wilkins (22Ω is characteristic of their newer Px line) ----
    "BW_P3":         {"impedance": "32",  "sensitivity": "106"},
    "BW_P5":         {"impedance": "32",  "sensitivity": "105"},
    "BW_P5S2":       {"impedance": "32",  "sensitivity": "105"},
    "BW_P7":         {"impedance": "22",  "sensitivity": "102"},
    "BW_P7WIRELESS": {"impedance": "22",  "sensitivity": "102"},
    "BW_P9":         {"impedance": "30",  "sensitivity": "104"},
    "BW_PX":         {"impedance": "32",  "sensitivity": "100"},
    "BW_PX5":        {"impedance": "32",  "sensitivity": "100"},
    "BW_PX7":        {"impedance": "22",  "sensitivity": "100"},
    "BW_PX7S2":      {"impedance": "22",  "sensitivity": "100"},
    "BW_PX7S2E":     {"impedance": "22",  "sensitivity": "100"},
    "BW_PX7S3":      {"impedance": "22",  "sensitivity": "100"},
    "BW_PX8":        {"impedance": "22",  "sensitivity": "100"},
    "BW_PX8S2":      {"impedance": "22",  "sensitivity": "100"},
    # ---- HiFiMan remaining ----
    "HIFIMAN_ARYAORGANIC":  {"impedance": "32",  "sensitivity": "94"},
    "HIFIMAN_HE1000UNV":    {"impedance": "35",  "sensitivity": "90"},
    "HIFIMAN_ARYAUNV":      {"impedance": "35",  "sensitivity": "91"},
    "HIFIMAN_ANANDANANOUNV":{"impedance": "16",  "sensitivity": "103"},
    "HIFIMAN_HER9":         {"impedance": "18",  "sensitivity": "91"},
    "HIFIMAN_HER10P":       {"impedance": "18",  "sensitivity": "91"},
    "HIFIMAN_HE600":        {"impedance": "50",  "sensitivity": "92"},
    "HIFIMAN_AUDIVINA":     {"impedance": "14",  "sensitivity": "91"},
    "HIFIMAN_EDITIONS":     {"impedance": "35",  "sensitivity": "96"},
    "HIFIMAN_EDITIONXV":    {"impedance": "35",  "sensitivity": "103"},
    # ---- Beats (all 40mm; impedance varies 32-64Ω) ----
    "BEATS_STUDIO2":   {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "BEATS_STUDIO3":   {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "BEATS_STUDIOPRO": {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "BEATS_STUDIO2013":{"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "BEATS_SOLO2":     {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "BEATS_SOLO3":     {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "BEATS_SOLO4":     {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "BEATS_SOLOPRO":   {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "BEATS_MIXR":      {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "BEATS_PRO":       {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "BEATS_EXECUTIVE": {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "BEATS_EP":        {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    # ---- Marshall ----
    "MARSHALL_MAJOR2":   {"impedance": "64", "sensitivity": "103", "driver_size": "40"},
    "MARSHALL_MAJOR3":   {"impedance": "64", "sensitivity": "103", "driver_size": "40"},
    "MARSHALL_MAJOR4":   {"impedance": "64", "sensitivity": "103", "driver_size": "40"},
    "MARSHALL_MAJOR5":   {"impedance": "64", "sensitivity": "103", "driver_size": "40"},
    "MARSHALL_MONITOR":  {"impedance": "64", "sensitivity": "99",  "driver_size": "40"},
    "MARSHALL_MONITOR2": {"impedance": "32", "sensitivity": "96",  "driver_size": "40"},
    "MARSHALL_MONITOR3": {"impedance": "32", "sensitivity": "96",  "driver_size": "40"},
    "MARSHALL_MIDANC":   {"impedance": "32", "sensitivity": "95",  "driver_size": "40"},
    # ---- SteelSeries gaming headsets (all ~40mm; 32-65Ω) ----
    "STEEL_ARCTIS5":    {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "STEEL_ARCTIS7":    {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "STEEL_ARCTISPRO":  {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "STEEL_NOVA1":      {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "STEEL_NOVA3":      {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "STEEL_NOVA5":      {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "STEEL_NOVA5X":     {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "STEEL_NOVA7":      {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "STEEL_NOVA7X":     {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "STEEL_NOVAPRO":    {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "STEEL_NOVAELITE":  {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "STEEL_NOVAPROOMNI":{"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- Razer gaming headsets ----
    "RAZER_KRAKENV3":     {"impedance": "32", "sensitivity": "109", "driver_size": "50"},
    "RAZER_KRAKENV4":     {"impedance": "32", "sensitivity": "109", "driver_size": "50"},
    "RAZER_KRAKENV4PRO":  {"impedance": "32", "sensitivity": "109", "driver_size": "50"},
    "RAZER_KRAKENKITTYV2":{"impedance": "32", "sensitivity": "109", "driver_size": "50"},
    "RAZER_BSV2":         {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "RAZER_BSV2PRO":      {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "RAZER_BSV2PRO23":    {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "RAZER_BSV3PRO":      {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "RAZER_BARRACUDAPRO": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "RAZER_BLACKSHARKV2X":{"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "RAZER_BLACKSHARKV3": {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    # ---- HyperX (Cloud series all use 53mm except Flight 40mm) ----
    "HYPERX_CLOUD":       {"impedance": "60", "sensitivity": "98", "driver_size": "53"},
    "HYPERX_CLOUD2":      {"impedance": "60", "sensitivity": "98", "driver_size": "53"},
    "HYPERX_CLOUD2W":     {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "HYPERX_CLOUDALPHA":  {"impedance": "65", "sensitivity": "98", "driver_size": "50"},
    "HYPERX_CLOUDALPHAW": {"impedance": "62", "sensitivity": "98", "driver_size": "50"},
    "HYPERX_CLOUD3":      {"impedance": "60", "sensitivity": "98", "driver_size": "53"},
    "HYPERX_CLOUD3W":     {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "HYPERX_CLOUDFLIGHT": {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    # ---- AKG remaining ----
    "AKG_N700NC":    {"impedance": "32",  "sensitivity": "114"},
    "AKG_N700NCM2":  {"impedance": "32",  "sensitivity": "114"},
    "AKG_N90Q":      {"impedance": "40",  "sensitivity": "110", "driver_size": "50"},
    "AKG_K1000":     {"impedance": "120", "sensitivity": "74"},
    "AKG_K501":      {"impedance": "120", "sensitivity": "97",  "driver_size": "50"},
    "AKG_K601":      {"impedance": "120", "sensitivity": "97",  "driver_size": "50"},
    "AKG_K141":      {"impedance": "55",  "sensitivity": "101", "driver_size": "30"},
    "AKG_K240SEXTETT":{"impedance": "600","sensitivity": "92",  "driver_size": "30"},
    "AKG_K340":      {"impedance": "400", "sensitivity": "93"},
    "AKG_Y50BT":     {"impedance": "32",  "sensitivity": "115", "driver_size": "40"},
    # ---- Beyerdynamic remaining ----
    "BEYER_AMIRONW":     {"impedance": "32",  "sensitivity": "108"},
    "BEYER_AVENTHOW":    {"impedance": "32",  "sensitivity": "108"},
    "BEYER_MMX300":      {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_MMX300_2":    {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_CUSTOM1":     {"impedance": "16",  "sensitivity": "96",  "driver_size": "45"},
    "BEYER_CUSTOMSTUDIO":{"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_LAGOONANC":   {"impedance": "32",  "sensitivity": "100"},
    "BEYER_MMX150":      {"impedance": "32",  "sensitivity": "116", "driver_size": "40"},
    "BEYER_DT48":        {"impedance": "200", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT831":       {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    # ---- Skullcandy ----
    "SKULL_HESH2":      {"impedance": "40", "sensitivity": "105", "driver_size": "40"},
    "SKULL_HESH3":      {"impedance": "40", "sensitivity": "105", "driver_size": "40"},
    "SKULL_HESHEVO":    {"impedance": "40", "sensitivity": "95",  "driver_size": "40"},
    "SKULL_HESHANC":    {"impedance": "32", "sensitivity": "98",  "driver_size": "40"},
    "SKULL_CRUSHERANC": {"impedance": "32", "sensitivity": "95",  "driver_size": "40"},
    "SKULL_CRUSHERANC2":{"impedance": "32", "sensitivity": "95",  "driver_size": "40"},
    "SKULL_CRUSHEREVO": {"impedance": "32", "sensitivity": "95",  "driver_size": "40"},
    "SKULL_CRUSHER540": {"impedance": "32", "sensitivity": "95",  "driver_size": "40"},
    # ---- Bang & Olufsen ----
    "BO_H4":     {"impedance": "32", "sensitivity": "104"},
    "BO_H6":     {"impedance": "25", "sensitivity": "104"},
    "BO_H9":     {"impedance": "32", "sensitivity": "102"},
    "BO_H95":    {"impedance": "18", "sensitivity": "100"},
    "BO_HX":     {"impedance": "18", "sensitivity": "98"},
    "BO_H100":   {"impedance": "18", "sensitivity": "98"},
    "BO_PORTAL": {"impedance": "32", "sensitivity": "98"},
    # ---- Philips ----
    "PHIL_L1":     {"impedance": "32", "sensitivity": "100"},
    "PHIL_L2":     {"impedance": "32", "sensitivity": "100"},
    "PHIL_L3":     {"impedance": "32", "sensitivity": "100"},
    "PHIL_L4":     {"impedance": "32", "sensitivity": "100"},
    "PHIL_SHP2000":{"impedance": "32", "sensitivity": "102", "driver_size": "40"},
    "PHIL_SHP9600":{"impedance": "32", "sensitivity": "106", "driver_size": "50"},
    "PHIL_H8505":  {"impedance": "27", "sensitivity": "104"},
    # ---- Audeze gaming/newer ----
    "AUDEZE_LCDGX":   {"impedance": "20",  "sensitivity": "103", "driver_size": "106"},
    "AUDEZE_PENROSE":  {"impedance": "32",  "sensitivity": "111"},
    "AUDEZE_MAXWELL":  {"impedance": "32",  "sensitivity": "111"},
    "AUDEZE_MAXWELL2": {"impedance": "32",  "sensitivity": "111"},
    "AUDEZE_LCDS20":   {"impedance": "14",  "sensitivity": "90",  "driver_size": "90"},
    # ---- Logitech G gaming headsets ----
    "LOGI_G933":    {"impedance": "39", "sensitivity": "107", "driver_size": "40"},
    "LOGI_G935":    {"impedance": "39", "sensitivity": "107", "driver_size": "40"},
    "LOGI_GPROX":   {"impedance": "35", "sensitivity": "91",  "driver_size": "50"},
    "LOGI_GPROX2":  {"impedance": "35", "sensitivity": "91",  "driver_size": "50"},
    "LOGI_GPROXWL": {"impedance": "35", "sensitivity": "91",  "driver_size": "50"},
    "LOGI_G535":    {"impedance": "32", "sensitivity": "93",  "driver_size": "40"},
    "LOGI_G733":    {"impedance": "32", "sensitivity": "88",  "driver_size": "40"},
    # ---- Corsair gaming headsets ----
    "CORSAIR_VIRTUOSO":    {"impedance": "32", "sensitivity": "109", "driver_size": "50"},
    "CORSAIR_VIRTUOSOXT":  {"impedance": "32", "sensitivity": "109", "driver_size": "50"},
    "CORSAIR_VIRTUOSOPRO": {"impedance": "32", "sensitivity": "109", "driver_size": "50"},
    "CORSAIR_HS80":        {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "CORSAIR_HS80MAX":     {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "CORSAIR_VOID":        {"impedance": "32", "sensitivity": "103", "driver_size": "50"},
    # ---- JBL (gaming and consumer wireless) ----
    "JBL_TUNE750":      {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "JBL_TUNE760":      {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "JBL_TUNE770":      {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "JBL_LIVE660":      {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "JBL_LIVE770NC":    {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "JBL_LIVE650":      {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "JBL_LIVE400":      {"impedance": "32", "sensitivity": "100", "driver_size": "32"},
    "JBL_LIVE460":      {"impedance": "32", "sensitivity": "100", "driver_size": "32"},
    "JBL_LIVE500":      {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "JBL_TOUR1":        {"impedance": "32", "sensitivity": "105", "driver_size": "40"},
    "JBL_TOUR1M2":      {"impedance": "32", "sensitivity": "105", "driver_size": "40"},
    "JBL_EVEREST700":   {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "JBL_EVEREST710":   {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "JBL_EVERESTELITE750":{"impedance":"32","sensitivity": "105", "driver_size": "40"},
    "JBL_QUANTUM100":   {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "JBL_QUANTUM400":   {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "JBL_QUANTUM800":   {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "JBL_QUANTUMONE":   {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "JBL_QUANTUM910":   {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "JBL_E45BT":        {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "JBL_E55BT":        {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    # ---- V-Moda remaining ----
    "VMODA_LP2":        {"impedance": "32", "sensitivity": "103"},
    "VMODA_M100MASTER": {"impedance": "32", "sensitivity": "103"},
    "VMODA_CROSSFADE2": {"impedance": "32", "sensitivity": "103"},
    "VMODA_CROSSFADELP":{"impedance": "32", "sensitivity": "103"},
    "VMODA_M200":       {"impedance": "42", "sensitivity": "97",  "driver_size": "50"},
    # ---- Moondrop remaining ----
    "MOON_VOID":        {"impedance": "32", "sensitivity": "96"},
    "MOON_JOKER":       {"impedance": "32", "sensitivity": "98"},
    "MOON_PARA":        {"impedance": "32", "sensitivity": "96"},
    # ---- Sennheiser HD 490 Pro ----
    "SENN_HD490PRO":  {"impedance": "130", "sensitivity": "96", "driver_size": "38"},
    # ---- AKG new models ----
    "AKG_K872":  {"impedance": "36",  "sensitivity": "110", "driver_size": "53"},
    "AKG_K175":  {"impedance": "32",  "sensitivity": "109", "driver_size": "40"},
    "AKG_K275":  {"impedance": "32",  "sensitivity": "112", "driver_size": "50"},
    # ---- Monoprice Monolith ----
    "MONO_M1060": {"impedance": "50", "sensitivity": "96", "driver_size": "106"},
    "MONO_M1060C":{"impedance": "50", "sensitivity": "96", "driver_size": "106"},
    "MONO_M1070": {"impedance": "60", "sensitivity": "96", "driver_size": "106"},
    "MONO_M570":  {"impedance": "32", "sensitivity": "96"},
    "MONO_M650":  {"impedance": "32", "sensitivity": "98"},
    "MONO_M1570": {"impedance": "60", "sensitivity": "96"},
    # ---- Superlux ----
    "SUPERLUX_HD668B":   {"impedance": "56", "sensitivity": "98", "driver_size": "50"},
    "SUPERLUX_HD681":    {"impedance": "32", "sensitivity": "98", "driver_size": "50"},
    "SUPERLUX_HD681EVO": {"impedance": "32", "sensitivity": "98", "driver_size": "50"},
    "SUPERLUX_HD669":    {"impedance": "32", "sensitivity": "98", "driver_size": "50"},
    "SUPERLUX_HD662EVO": {"impedance": "32", "sensitivity": "98", "driver_size": "50"},
    "SUPERLUX_HD330":    {"impedance": "32", "sensitivity": "98", "driver_size": "50"},
    # ---- Samson ----
    "SAMSON_SR850": {"impedance": "32", "sensitivity": "98", "driver_size": "50"},
    "SAMSON_SR950": {"impedance": "32", "sensitivity": "98", "driver_size": "50"},
    # ---- Status Audio ----
    "STATUS_CB1":   {"impedance": "32", "sensitivity": "97", "driver_size": "50"},
    "STATUS_BTONE": {"impedance": "32", "sensitivity": "97", "driver_size": "40"},
    # ---- Harman Kardon ----
    "HK_FLYANC":   {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "HK_FLY":      {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    # ---- Oppo ----
    "OPPO_PM1": {"impedance": "32", "sensitivity": "102"},
    "OPPO_PM2": {"impedance": "32", "sensitivity": "102"},
    "OPPO_PM3": {"impedance": "26", "sensitivity": "102", "driver_size": "55"},
    # ---- Creative ----
    "CREATIVE_AVLIVE":  {"impedance": "32", "sensitivity": "111", "driver_size": "40"},
    "CREATIVE_AVLIVE2": {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    # ---- Rode ----
    "RODE_NTH100": {"impedance": "32", "sensitivity": "96", "driver_size": "40"},
    # ---- Klipsch ----
    "KLIPSCH_HP3":    {"impedance": "50", "sensitivity": "99", "driver_size": "52"},
    "KLIPSCH_REFONE": {"impedance": "26", "sensitivity": "114"},
    # ---- Fostex RP additions ----
    "FOSTEX_T20RPMK3": {"impedance": "50", "sensitivity": "98"},
    "FOSTEX_T40RPMK3": {"impedance": "50", "sensitivity": "97"},
    "FOSTEX_T50RPMK3": {"impedance": "50", "sensitivity": "92"},
    "FOSTEX_T50RPMK4": {"impedance": "50", "sensitivity": "92"},
    "FOSTEX_T60RP":    {"impedance": "50", "sensitivity": "97"},
    "FOSTEX_THXOO":    {"impedance": "25", "sensitivity": "94", "driver_size": "50"},
    "FOSTEX_TH600":    {"impedance": "25", "sensitivity": "100", "driver_size": "50"},
    "FOSTEX_TH500RP":  {"impedance": "48", "sensitivity": "93"},
    # ---- Yamaha additions ----
    "YAMAHA_YH5000SE": {"impedance": "34", "sensitivity": "98"},
    "YAMAHA_YH4000":   {"impedance": "34", "sensitivity": "97"},
    "YAMAHA_HPHMT220": {"impedance": "48", "sensitivity": "102", "driver_size": "40"},
    "YAMAHA_YHC3000":  {"impedance": "34", "sensitivity": "94"},
    # ---- HarmonicDyne ----
    "HD_HELIOS":    {"impedance": "32", "sensitivity": "104", "driver_size": "50"},
    "HD_ZEUS":      {"impedance": "32", "sensitivity": "99",  "driver_size": "50"},
    "HD_POSEIDON":  {"impedance": "32", "sensitivity": "104", "driver_size": "50"},
    "HD_BLACKHOLE": {"impedance": "32", "sensitivity": "110", "driver_size": "50"},
    "HD_G200":      {"impedance": "64", "sensitivity": "100", "driver_size": "102"},
    # ---- PSB ----
    "PSB_M4U1": {"impedance": "32", "sensitivity": "102", "driver_size": "40"},
    "PSB_M4U2": {"impedance": "32", "sensitivity": "102", "driver_size": "40"},
    "PSB_M4U8": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- E-Mu ----
    "EMU_TEAK":        {"impedance": "26", "sensitivity": "105", "driver_size": "50"},
    "EMU_PURPLEHEART": {"impedance": "26", "sensitivity": "105", "driver_size": "50"},
    # ---- Beyerdynamic additions ----
    "BEYER_DT770M":   {"impedance": "80",  "sensitivity": "96",  "driver_size": "45"},
    "BEYER_T50P":     {"impedance": "32",  "sensitivity": "102", "driver_size": "40"},
    "BEYER_DT880_600":{"impedance": "600", "sensitivity": "96",  "driver_size": "45"},
    "BEYER_DT860":    {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    # ---- Audio-Technica additions ----
    "ATECH_A700":    {"impedance": "40", "sensitivity": "100", "driver_size": "53"},
    "ATECH_A900X":   {"impedance": "40", "sensitivity": "100", "driver_size": "53"},
    "ATECH_AWAS":    {"impedance": "42", "sensitivity": "100", "driver_size": "58"},
    "ATECH_L5000":   {"impedance": "36", "sensitivity": "100", "driver_size": "58"},
    "ATECH_DSR9BT":  {"impedance": "32", "sensitivity": "98"},
    # ---- Audio-Technica backfill (A-series 53mm closed; AD-series 53mm open; W-series wood) ----
    "ATECH_A550Z":   {"impedance": "44", "sensitivity": "99",  "driver_size": "53"},
    "ATECH_A990Z":   {"impedance": "44", "sensitivity": "99",  "driver_size": "53"},
    "ATECH_A1000Z":  {"impedance": "44", "sensitivity": "101", "driver_size": "53"},
    "ATECH_A2000Z":  {"impedance": "48", "sensitivity": "101", "driver_size": "53"},
    "ATECH_AD500X":  {"impedance": "48", "sensitivity": "100", "driver_size": "53"},
    "ATECH_AD2000X": {"impedance": "40", "sensitivity": "102", "driver_size": "53"},
    "ATECH_AD2000":  {"impedance": "40", "sensitivity": "102", "driver_size": "53"},
    "ATECH_W1000Z":  {"impedance": "44", "sensitivity": "101", "driver_size": "53"},
    "ATECH_W1000":   {"impedance": "40", "sensitivity": "102", "driver_size": "53"},
    "ATECH_W5000":   {"impedance": "40", "sensitivity": "102", "driver_size": "53"},
    "ATECH_L3000":   {"impedance": "40", "sensitivity": "102", "driver_size": "53"},
    "ATECH_M50":     {"impedance": "38", "sensitivity": "99",  "driver_size": "45"},
    "ATECH_WP900":   {"impedance": "38", "sensitivity": "100", "driver_size": "53"},
    "ATECH_AWKT":    {"impedance": "48", "sensitivity": "100", "driver_size": "53"},
    "ATECH_ADX3000": {"impedance": "48", "sensitivity": "101", "driver_size": "58"},
    "ATECH_ESW9":    {"impedance": "42", "sensitivity": "100", "driver_size": "42"},
    "ATECH_ES7":     {"impedance": "42", "sensitivity": "102", "driver_size": "42"},
    "ATECH_G1":      {"impedance": "45", "sensitivity": "98",  "driver_size": "45"},
    # ---- Sony additions ----
    "SONY_MDRV500":    {"impedance": "24", "sensitivity": "106", "driver_size": "50"},
    "SONY_MDRV700":    {"impedance": "24", "sensitivity": "106", "driver_size": "50"},
    "SONY_MDRSA3000":  {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    "SONY_MDRF1":      {"impedance": "24", "sensitivity": "100", "driver_size": "50"},
    "SONY_MDRXB1000":  {"impedance": "24", "sensitivity": "108", "driver_size": "70"},
    # ---- Dan Clark Audio MrSpeakers era ----
    "DCA_AEONCLOSED": {"impedance": "13", "sensitivity": "92"},
    "DCA_ETHERCX":    {"impedance": "23", "sensitivity": "93"},
    # ---- Denon historical ----
    "DENON_D1001": {"impedance": "25", "sensitivity": "104", "driver_size": "40"},
    "DENON_D1100": {"impedance": "25", "sensitivity": "104", "driver_size": "40"},
    # ---- Grado older ----
    "GRADO_SR125E":  {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR125I":  {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR225E":  {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR225I":  {"impedance": "32", "sensitivity": "99"},
    "GRADO_GS3000E": {"impedance": "32", "sensitivity": "99"},
    "GRADO_HF1":     {"impedance": "32", "sensitivity": "99"},
    "GRADO_HF2":     {"impedance": "32", "sensitivity": "99"},
    # ---- AKG additions ----
    "AKG_K240MKII": {"impedance": "55", "sensitivity": "91", "driver_size": "30"},
    "AKG_K52":      {"impedance": "32", "sensitivity": "112", "driver_size": "40"},
    "AKG_K450":     {"impedance": "32", "sensitivity": "118", "driver_size": "30"},
    # ---- Pioneer additions ----
    "PIONEER_HDJ1000": {"impedance": "40", "sensitivity": "106", "driver_size": "50"},
    "PIONEER_HDJ500":  {"impedance": "32", "sensitivity": "102", "driver_size": "40"},
    # ---- Sony additions ----
    "SONY_MDR7520":    {"impedance": "24", "sensitivity": "106", "driver_size": "50"},
    "SONY_INZONEH3":   {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "SONY_INZONEH9":   {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- Audeze additions ----
    "AUDEZE_EL8O":   {"impedance": "30",  "sensitivity": "102", "driver_size": "100"},
    "AUDEZE_EL8C":   {"impedance": "30",  "sensitivity": "102", "driver_size": "100"},
    "AUDEZE_LCDMX4": {"impedance": "20",  "sensitivity": "103", "driver_size": "106"},
    "AUDEZE_MOBIUS": {"impedance": "10",  "sensitivity": "111"},
    # ---- Beyerdynamic additions ----
    "BEYER_DT1350":   {"impedance": "80",  "sensitivity": "96",  "driver_size": "35"},
    "BEYER_DT177XGO": {"impedance": "250", "sensitivity": "102", "driver_size": "45"},
    "BEYER_DT250":    {"impedance": "250", "sensitivity": "96",  "driver_size": "45"},
    # ---- AKG additions ----
    "AKG_Q701":  {"impedance": "62", "sensitivity": "105", "driver_size": "50"},
    "AKG_K7XX":  {"impedance": "62", "sensitivity": "105", "driver_size": "45"},
    "AKG_N60NC": {"impedance": "32", "sensitivity": "116", "driver_size": "32"},
    "AKG_K267":  {"impedance": "32", "sensitivity": "114", "driver_size": "50"},
    # ---- Sennheiser gap fills ----
    "SENN_AMPERIOR": {"impedance": "18", "sensitivity": "110", "driver_size": "30"},
    "SENN_HD201":    {"impedance": "32", "sensitivity": "108", "driver_size": "40"},
    "SENN_HD203":    {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "SENN_HD219":    {"impedance": "32", "sensitivity": "115", "driver_size": "40"},
    "SENN_HD229":    {"impedance": "32", "sensitivity": "115", "driver_size": "40"},
    "SENN_GAMEONE":  {"impedance": "50", "sensitivity": "110"},
    "SENN_GSP600":   {"impedance": "28", "sensitivity": "112"},
    "SENN_GSP300":   {"impedance": "28", "sensitivity": "113"},
    # ---- Koss additions ----
    "KOSS_KPH40": {"impedance": "60", "sensitivity": "101", "driver_size": "30"},
    "KOSS_KPH7":  {"impedance": "60", "sensitivity": "101", "driver_size": "25"},
    # ---- Dan Clark Audio historical ----
    "DCA_ETHERFLOW":  {"impedance": "23", "sensitivity": "93"},
    "DCA_ETHERCFLOW": {"impedance": "23", "sensitivity": "93"},
    "DCA_AEONOPEN":   {"impedance": "13", "sensitivity": "93"},
    # ---- Denon historical ----
    "DENON_D7000": {"impedance": "25", "sensitivity": "106", "driver_size": "50"},
    "DENON_D7100": {"impedance": "25", "sensitivity": "106", "driver_size": "50"},
    "DENON_D600":  {"impedance": "25", "sensitivity": "98",  "driver_size": "50"},
    # ---- Grado (32Ω across essentially the full line; sensitivity ~99 dB for standard drivers) ----
    "GRADO_SR60":   {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR60X":  {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR80E":  {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR80X":  {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR125X": {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR225X": {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR325E": {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR325I": {"impedance": "32", "sensitivity": "99"},
    "GRADO_SR325X": {"impedance": "32", "sensitivity": "99"},
    "GRADO_RS1":    {"impedance": "32", "sensitivity": "99"},
    "GRADO_RS1X":   {"impedance": "32", "sensitivity": "99"},
    "GRADO_RS2E":   {"impedance": "32", "sensitivity": "99"},
    "GRADO_RS2X":   {"impedance": "32", "sensitivity": "99"},
    "GRADO_PS500E": {"impedance": "32", "sensitivity": "99"},
    "GRADO_PS1000": {"impedance": "32", "sensitivity": "99"},
    "GRADO_PS1000E":{"impedance": "32", "sensitivity": "99"},
    "GRADO_PS2000E":{"impedance": "32", "sensitivity": "99"},
    "GRADO_GS1000": {"impedance": "32", "sensitivity": "99"},
    "GRADO_GS1000X":{"impedance": "32", "sensitivity": "99"},
    "GRADO_GS3000X":{"impedance": "32", "sensitivity": "99"},
    "GRADO_GH1":    {"impedance": "32", "sensitivity": "99"},
    "GRADO_GH2":    {"impedance": "32", "sensitivity": "99"},
    "GRADO_GH3":    {"impedance": "32", "sensitivity": "99"},
    "GRADO_GH4":    {"impedance": "32", "sensitivity": "99"},
    "GRADO_HEMP":   {"impedance": "32", "sensitivity": "99"},
    "GRADO_GW100X": {"impedance": "32", "sensitivity": "99"},
    # ---- ZMF (dynamic models: 300Ω biocellulose driver ~96 dB; planar: ~55Ω) ----
    "ZMF_AUTEUR":       {"impedance": "300", "sensitivity": "96"},
    "ZMF_AEOLUS":       {"impedance": "300", "sensitivity": "96"},
    "ZMF_EIKON":        {"impedance": "300", "sensitivity": "96"},
    "ZMF_ATTICUS":      {"impedance": "300", "sensitivity": "96"},
    "ZMF_VERITEOPEN":   {"impedance": "300", "sensitivity": "96"},
    "ZMF_VERITECLOSED": {"impedance": "300", "sensitivity": "96"},
    "ZMF_ATRIUM":       {"impedance": "300", "sensitivity": "96"},
    "ZMF_ATRIUMCLOSED": {"impedance": "300", "sensitivity": "96"},
    "ZMF_CALDERA":      {"impedance": "55",  "sensitivity": "96"},
    "ZMF_CALDERACLOSED":{"impedance": "55",  "sensitivity": "96"},
    "ZMF_BOKEHOPEN":    {"impedance": "300", "sensitivity": "96"},
    "ZMF_BOKEHCLOSED":  {"impedance": "300", "sensitivity": "96"},
    "ZMF_TESSIDERA":    {"impedance": "35",  "sensitivity": "96"},
    # ---- Dan Clark Audio ----
    "DCA_AEONFLOW":   {"impedance": "13",  "sensitivity": "92"},
    "DCA_AEON2":      {"impedance": "13",  "sensitivity": "92"},
    "DCA_AEON2NOIRE": {"impedance": "13",  "sensitivity": "92"},
    "DCA_ETHER2":     {"impedance": "16",  "sensitivity": "88"},
    "DCA_STEALTH":    {"impedance": "23",  "sensitivity": "86"},
    "DCA_E3":         {"impedance": "16",  "sensitivity": "92"},
    "DCA_EXPANSE":    {"impedance": "23",  "sensitivity": "91"},
    "DCA_CORINA":     {"impedance": "23",  "sensitivity": "93"},
    # ---- Denon ----
    "DENON_D5200":   {"impedance": "46", "sensitivity": "98", "driver_size": "50"},
    "DENON_D7200":   {"impedance": "25", "sensitivity": "98", "driver_size": "50"},
    "DENON_D9200":   {"impedance": "16", "sensitivity": "98", "driver_size": "50"},
    "DENON_D2000":   {"impedance": "25", "sensitivity": "106", "driver_size": "50"},
    "DENON_D5000":   {"impedance": "25", "sensitivity": "106", "driver_size": "50"},
    # ---- Fostex ----
    "FOSTEX_TH900":    {"impedance": "25",  "sensitivity": "100", "driver_size": "50"},
    "FOSTEX_TH900MK2": {"impedance": "25",  "sensitivity": "100", "driver_size": "50"},
    "FOSTEX_TH909":    {"impedance": "25",  "sensitivity": "100", "driver_size": "50"},
    "FOSTEX_TH610":    {"impedance": "25",  "sensitivity": "96",  "driver_size": "50"},
    # ---- Meze Audio (additional) ----
    "MEZE_POET":         {"impedance": "40", "sensitivity": "112", "driver_size": "50"},
    "MEZE_109PRODESC":   {"impedance": "40", "sensitivity": "112", "driver_size": "50"},
    # ---- Audioquest (verified from manufacturer page & multiple reviews) ----
    "AQ_NIGHTHAWK":       {"impedance": "25", "sensitivity": "99", "driver_size": "50"},
    "AQ_NIGHTHAWKCARBON": {"impedance": "25", "sensitivity": "99", "driver_size": "50"},
    "AQ_NIGHTOWL":        {"impedance": "25", "sensitivity": "99", "driver_size": "50"},
    "AQ_NIGHTOWLCARBON":  {"impedance": "25", "sensitivity": "99", "driver_size": "50"},
    # ---- NAD (verified: 32Ω from Headfonics; ~106 dB from SoundStage measurements) ----
    "NAD_HP50":    {"impedance": "32", "sensitivity": "106", "driver_size": "40"},
    # ---- Brainwavz (64Ω verified from multiple retail listings) ----
    "BWAVZ_HM5":   {"impedance": "64", "sensitivity": "98", "driver_size": "40"},
    # ---- Beyerdynamic portable Tesla (verified from Adorama/manufacturer specs) ----
    # T51p: 60Ω (Adorama listing); T51i: 32Ω (Adorama listing, iOS remote version); T90: 250Ω/102dB (Head-Fi/manufacturer)
    "BEYER_T51P":  {"impedance": "60",  "sensitivity": "102", "driver_size": "40"},
    "BEYER_T51I":  {"impedance": "32",  "sensitivity": "111", "driver_size": "40"},
    "BEYER_T90":   {"impedance": "250", "sensitivity": "102", "driver_size": "45"},
    # ---- Sennheiser HD 598 CS (verified: 23Ω/115dB confirmed by Major HiFi, Head-Fi, multiple reviews) ----
    "SENN_HD598CS": {"impedance": "23", "sensitivity": "115"},
    # ---- ZMF Ori (original T50RP-based closed planar: 50Ω) ----
    "ZMF_ORI":   {"impedance": "50",  "sensitivity": "96"},
    "ZMF_ORI3":  {"impedance": "35",  "sensitivity": "96", "driver_size": "80"},
    # ---- AKG K240 vintage 600Ω (confirmed from multiple sources; ~88 dB sensitivity) ----
    "AKG_K240DF": {"impedance": "600", "sensitivity": "88"},
    "AKG_K240M":  {"impedance": "600", "sensitivity": "88"},
    # ---- Monoprice M560 (42Ω per retailer spec sheets) ----
    "MONO_M560":   {"impedance": "42", "sensitivity": "100"},
    # ---- Status Audio additional (from status.co spec pages) ----
    "STATUS_HDONE": {"impedance": "32", "sensitivity": "99",  "driver_size": "40"},
    "STATUS_HDTWO": {"impedance": "17", "sensitivity": "115", "driver_size": "40"},
    "STATUS_OB1":   {"impedance": "54", "sensitivity": "95",  "driver_size": "40"},
    # ---- Moondrop over-ear remaining ----
    "MOONDROP_VENUS":    {"impedance": "32", "sensitivity": "96"},
    "MOONDROP_PARA":     {"impedance": "32", "sensitivity": "96"},
    "MOONDROP_COSMO":    {"impedance": "32", "sensitivity": "100"},
    "MOONDROP_HORIZON":  {"impedance": "32", "sensitivity": "100"},
    "MOONDROP_EDGE":     {"impedance": "32", "sensitivity": "100"},
    "MOONDROP_OLDFASHIONED":{"impedance":"60","sensitivity": "96"},
    # ---- Pioneer remaining ----
    "PIONEER_SEMASTER1":  {"impedance": "50",  "sensitivity": "101", "driver_size": "53"},
    "PIONEER_SEMONITOR5": {"impedance": "200", "sensitivity": "90"},
    "PIONEER_HDJX10":     {"impedance": "32",  "sensitivity": "106", "driver_size": "50"},
    "PIONEER_HDJ2000":    {"impedance": "32",  "sensitivity": "108", "driver_size": "50"},
    # ---- Jabra Evolve2 (40mm confirmed; conventional impedance not published for pro headsets) ----
    "JABRA_E230": {"sensitivity": "103", "driver_size": "40"},
    "JABRA_E240": {"sensitivity": "103", "driver_size": "40"},
    "JABRA_E255": {"sensitivity": "103", "driver_size": "40"},
    "JABRA_E265": {"sensitivity": "103", "driver_size": "40"},
    "JABRA_E275": {"sensitivity": "103", "driver_size": "40"},
    "JABRA_E285": {"sensitivity": "103", "driver_size": "40"},
    # ---- Stax electrostatics (sensitivity in dB/V from stax.co.jp; impedance not applicable) ----
    "STAX_SR009":       {"sensitivity": "100"},
    "STAX_SR009S":      {"sensitivity": "101"},
    "STAX_SR007":       {"sensitivity": "99"},
    "STAX_SRL300":      {"sensitivity": "103"},
    "STAX_SRL500":      {"sensitivity": "101"},
    "STAX_SRL700":      {"sensitivity": "103"},
    "STAX_SRL700MK2":   {"sensitivity": "103"},
    "STAX_X9000":       {"sensitivity": "104"},
    "STAX_SR404":       {"sensitivity": "97"},
    "STAX_SR207":       {"sensitivity": "98"},
    "STAX_SR507":       {"sensitivity": "101"},
    "STAX_SR4070":      {"sensitivity": "97"},
    "STAX_LAMBDANOVA":  {"sensitivity": "98"},
    "STAX_SR84":        {"sensitivity": "100"},
    # ---- Turtle Beach ----
    "TB_STEALTH600G2": {"impedance": "32", "sensitivity": "95", "driver_size": "50"},
    "TB_STEALTH700G2": {"impedance": "32", "sensitivity": "95", "driver_size": "50"},
    "TB_STEALTHPRO":   {"impedance": "32", "sensitivity": "95", "driver_size": "50"},
    "TB_STEALTHPRO2":  {"impedance": "32", "sensitivity": "95", "driver_size": "50"},
    "TB_ATLASAIR":     {"impedance": "32", "sensitivity": "95", "driver_size": "50"},
    # ---- Astro Gaming ----
    "ASTRO_A40":   {"impedance": "48", "sensitivity": "118", "driver_size": "40"},
    "ASTRO_A40TR": {"impedance": "48", "sensitivity": "118", "driver_size": "40"},
    "ASTRO_A50G4": {"impedance": "32", "sensitivity": "118", "driver_size": "40"},
    "ASTRO_A50X":  {"impedance": "32", "sensitivity": "118", "driver_size": "40"},
    # ---- Abyss ----
    "ABYSS_AB1266":  {"impedance": "42", "sensitivity": "88"},
    "ABYSS_DIANA":   {"impedance": "42", "sensitivity": "88"},
    "ABYSS_DIANAV2": {"impedance": "42", "sensitivity": "88"},
    "ABYSS_DIANATC": {"impedance": "46", "sensitivity": "90"},
    "ABYSS_DIANAMR": {"impedance": "42", "sensitivity": "91"},
    # ---- Final Audio ----
    "FINAL_D8000":     {"impedance": "60", "sensitivity": "98", "driver_size": "50"},
    "FINAL_D8000PRO":  {"impedance": "60", "sensitivity": "98", "driver_size": "50"},
    "FINAL_SONOROUS3": {"impedance": "65", "sensitivity": "98", "driver_size": "50"},
    "FINAL_SONOROUS6": {"impedance": "65", "sensitivity": "98", "driver_size": "50"},
    "FINAL_SONOROUSX": {"impedance": "75", "sensitivity": "93", "driver_size": "50"},
    # ---- Anker Soundcore ----
    "ANKER_LIFEQ20":    {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "ANKER_LIFEQ30":    {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "ANKER_SPACEQ45":   {"impedance": "32", "sensitivity": "98",  "driver_size": "40"},
    "ANKER_SPACEONE":   {"impedance": "32", "sensitivity": "98",  "driver_size": "40"},
    "ANKER_SPACEONEPRO":{"impedance": "32", "sensitivity": "98",  "driver_size": "40"},
    # ---- Yamaha remaining ----
    "YAMAHA_HPHMT8":  {"impedance": "49",  "sensitivity": "102", "driver_size": "40"},
    "YAMAHA_YHL700A": {"impedance": "32",  "sensitivity": "100"},
    "YAMAHA_YHE700A": {"impedance": "32",  "sensitivity": "100"},
    "YAMAHA_HPH200":  {"impedance": "48",  "sensitivity": "102", "driver_size": "40"},
    "YAMAHA_HP1":     {"impedance": "470", "sensitivity": "91"},
    # ---- Sennheiser remaining ----
    "SENN_HDB630": {"impedance": "32",   "sensitivity": "107", "driver_size": "40"},
    "SENN_HD414":  {"impedance": "2000", "sensitivity": "92"},
    # ---- Neumann ----
    "NEUMANN_NDH20": {"impedance": "150", "sensitivity": "104", "driver_size": "38"},
    "NEUMANN_NDH30": {"impedance": "120", "sensitivity": "103", "driver_size": "38"},
    # ---- Austrian Audio ----
    "AUSTRIAN_HIX55":       {"impedance": "25", "sensitivity": "103", "driver_size": "44"},
    "AUSTRIAN_HIX65":       {"impedance": "25", "sensitivity": "102", "driver_size": "44"},
    "AUSTRIAN_HIX60":       {"impedance": "25", "sensitivity": "102", "driver_size": "44"},
    "AUSTRIAN_THECOMPOSER": {"impedance": "26", "sensitivity": "110"},
    # ---- FiiO ----
    "FIIO_FT1":    {"impedance": "64", "sensitivity": "97",  "driver_size": "50"},
    "FIIO_FT1PRO": {"impedance": "32", "sensitivity": "98",  "driver_size": "50"},
    "FIIO_FT3":    {"impedance": "64", "sensitivity": "110", "driver_size": "50"},
    "FIIO_FT5":    {"impedance": "32", "sensitivity": "100"},
    # ---- Focal remaining ----
    "FOCAL_SPIRITONE":  {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "FOCAL_SPIRITPRO":  {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "FOCAL_LISTENPRO":  {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "FOCAL_LISTENWL":   {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    # ---- AIAIAI ----
    "AIAIAI_TMA1":       {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "AIAIAI_TMA2":       {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "AIAIAI_TMA2STUDIO": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "AIAIAI_TMA2WL":     {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- Edifier STAX Spirit planar ----
    "EDIFIER_STAXGT1": {"impedance": "32", "sensitivity": "96"},
    "EDIFIER_STAXGT5": {"impedance": "32", "sensitivity": "96"},
    "EDIFIER_W820NB":  {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "EDIFIER_WH950NB": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- Sendy Audio (planar) ----
    "SENDY_AIVA":    {"impedance": "32", "sensitivity": "96"},
    "SENDY_PEACOCK": {"impedance": "50", "sensitivity": "94"},
    "SENDY_APOLLO":  {"impedance": "32", "sensitivity": "96"},
    # ---- Meze Audio remaining variants ----
    "MEZE_99NOIR":           {"impedance": "32",   "sensitivity": "103", "driver_size": "40"},
    "MEZE_99CLASSICSWALNUT": {"impedance": "32",   "sensitivity": "103", "driver_size": "40"},
    "MEZE_LIRICII":          {"impedance": "31.6", "sensitivity": "102"},
    # ---- V-Moda remaining ----
    "VMODA_LP":           {"impedance": "32", "sensitivity": "103", "driver_size": "50"},
    "VMODA_M100":         {"impedance": "32", "sensitivity": "103", "driver_size": "50"},
    "VMODA_CROSSFADE2WL": {"impedance": "32", "sensitivity": "103"},
    # ---- Sivga ----
    "SIVGA_PHOENIX": {"impedance": "32", "sensitivity": "103", "driver_size": "50"},
    "SIVGA_PII":     {"impedance": "32", "sensitivity": "103", "driver_size": "50"},
    "SIVGA_SV021":   {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "SIVGA_ORIOLE":  {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- T+A ----
    "TA_SOLITAIRE_P":   {"impedance": "200", "sensitivity": "92"},
    "TA_SOLITAIRE_PSE": {"impedance": "200", "sensitivity": "92"},
    "TA_SOLITAIRE_T":   {"impedance": "40",  "sensitivity": "92"},
    # ---- HEDD Audio (AMT driver) ----
    "HEDD_HEDDPHONE":   {"impedance": "42", "sensitivity": "87"},
    "HEDD_HEDDPHONE2":  {"impedance": "35", "sensitivity": "92"},
    "HEDD_HEDDPHONED1": {"impedance": "35", "sensitivity": "92"},
    # ---- Ollo Audio ----
    "OLLO_S4X": {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "OLLO_S5X": {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "OLLO_X1":  {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    # ---- Kennerton (planar) ----
    "KENNERTON_ODIN":  {"impedance": "40", "sensitivity": "95"},
    "KENNERTON_THROR": {"impedance": "42", "sensitivity": "93"},
    # ---- Cleer ----
    "CLEER_FLOW2":     {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "CLEER_ENDURO100": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "CLEER_ALPHA":     {"impedance": "40", "sensitivity": "100"},
    # ---- 1More ----
    "1MORE_SONOFLOW":    {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "1MORE_SONOFLOWSE":  {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "1MORE_MK802":       {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    # ---- Ultrasone ----
    "ULTRA_ED5":     {"impedance": "32",  "sensitivity": "96", "driver_size": "40"},
    "ULTRA_PERF880": {"impedance": "150", "sensitivity": "96", "driver_size": "40"},
    "ULTRA_HFI580":  {"impedance": "75",  "sensitivity": "94", "driver_size": "40"},
    # ---- Apple ----
    "APPLE_AIRPODSMAX":     {"impedance": "35", "sensitivity": "100", "driver_size": "40"},
    "APPLE_AIRPODSMAXUSBC": {"impedance": "35", "sensitivity": "100", "driver_size": "40"},
    # ---- Technics ----
    "TECH_EAHA800":   {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "TECH_EAHA800M2": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- ASUS ROG ----
    "ASUS_DELTAS": {"impedance": "32", "sensitivity": "108", "driver_size": "40"},
    "ASUS_DELTA2": {"impedance": "32", "sensitivity": "108", "driver_size": "40"},
    # ---- Sonos / Nothing / Grell ----
    "SONOS_ACE":          {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "NOTHING_HEADPHONE1": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "GRELL_OAE2":         {"impedance": "32", "sensitivity": "97",  "driver_size": "40"},
    # ---- Mark Levinson ----
    "MARKLEV_5909": {"impedance": "18", "sensitivity": "99", "driver_size": "40"},
    # ---- Spirit Torino ----
    "SPIRITTORINO_SUPER":    {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "SPIRITTORINO_RADIANTE": {"impedance": "16", "sensitivity": "98",  "driver_size": "40"},
    # ---- Rosson Audio ----
    "ROSSON_RAD0": {"impedance": "34", "sensitivity": "93"},
    # ---- Koss remaining ----
    "KOSS_PORTAPROWL": {"impedance": "60",  "sensitivity": "101", "driver_size": "25"},
    "KOSS_PRO4AA":     {"impedance": "250", "sensitivity": "92",  "driver_size": "50"},
    # ---- Audio-Technica remaining ----
    "ATECH_SR50BT":   {"impedance": "38", "sensitivity": "98", "driver_size": "45"},
    "ATECH_SR30BT":   {"impedance": "32", "sensitivity": "98", "driver_size": "40"},
    "ATECH_ANC900BT": {"impedance": "38", "sensitivity": "98", "driver_size": "40"},
    # ---- Shure remaining ----
    "SHURE_SRH750DJ": {"impedance": "32", "sensitivity": "105", "driver_size": "50"},
    # ---- Harman Kardon remaining ----
    "HK_SOHO":    {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "HK_SOHOWL":  {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "HK_SOHOWNC": {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    # ---- Denon remaining ----
    "DENON_D400": {"impedance": "25", "sensitivity": "96", "driver_size": "40"},
    # ---- Grado remaining ----
    "GRADO_S550": {"impedance": "32", "sensitivity": "99"},
    # ---- Creative remaining ----
    "CREATIVE_SXFLAIR": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- HiFiMan and Audeze electrostatics (sensitivity only) ----
    "HIFIMAN_JADE2":     {"sensitivity": "90"},
    "HIFIMAN_SHANGRILA": {"sensitivity": "90"},
    "AUDEZE_CRBN":       {"sensitivity": "102"},
    "AUDEZE_CRBN2":      {"sensitivity": "102"},
    # ---- Modhouse Audio ----
    "MODHOUSE_ARGONMK3": {"impedance": "50", "sensitivity": "96"},
    "MODHOUSE_TUNGSTEN":  {"impedance": "16", "sensitivity": "97"},
    # ---- Kiwi Ears ----
    "KIWIEARS_ARDOR":   {"impedance": "20", "sensitivity": "96"},
    "KIWIEARS_ELLIPSE": {"impedance": "20", "sensitivity": "96"},
    "KIWIEARS_ATHEIA":  {"impedance": "20", "sensitivity": "98"},
    "KIWIEARS_AVENTUS": {"impedance": "32", "sensitivity": "98"},
    # ---- Ultrasone additions ----
    "ULTRA_ED8":     {"impedance": "32",  "sensitivity": "96", "driver_size": "40"},
    "ULTRA_ED10":    {"impedance": "32",  "sensitivity": "96", "driver_size": "40"},
    "ULTRA_ED15":    {"impedance": "32",  "sensitivity": "96", "driver_size": "40"},
    "ULTRA_HFI780":  {"impedance": "75",  "sensitivity": "96", "driver_size": "40"},
    "ULTRA_HFI450":  {"impedance": "40",  "sensitivity": "96", "driver_size": "40"},
    "ULTRA_HFI2400": {"impedance": "75",  "sensitivity": "96", "driver_size": "40"},
    "ULTRA_SIGPURE": {"impedance": "35",  "sensitivity": "96", "driver_size": "40"},
    "ULTRA_TRIB7":   {"impedance": "32",  "sensitivity": "96", "driver_size": "40"},
    # ---- Dan Clark Audio MrSpeakers era ----
    "DCA_MADDOG":     {"impedance": "50",  "sensitivity": "91"},
    "DCA_NOIRECLOSED":{"impedance": "23",  "sensitivity": "90"},
    # ---- Fostex additions ----
    "FOSTEX_T50RPMK2": {"impedance": "50", "sensitivity": "92"},
    "FOSTEX_TXO":      {"impedance": "25", "sensitivity": "100", "driver_size": "50"},
    "FOSTEX_TXOII":    {"impedance": "25", "sensitivity": "100", "driver_size": "50"},
    "FOSTEX_TR80":     {"impedance": "80", "sensitivity": "100", "driver_size": "50"},
    "FOSTEX_TH616":    {"impedance": "25", "sensitivity": "100", "driver_size": "50"},
    # ---- JBL CLUB and remaining ----
    "JBL_CLUBONE":  {"impedance": "32", "sensitivity": "105", "driver_size": "40"},
    "JBL_CLUB700":  {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "JBL_CLUB950":  {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "JBL_LIVE670":  {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "JBL_DUETNC":   {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "JBL_E65BTNC":  {"impedance": "32", "sensitivity": "103", "driver_size": "40"},
    "JBL_J55":      {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    # ---- More Logitech G ----
    "LOGI_G430":   {"impedance": "32", "sensitivity": "90",  "driver_size": "40"},
    "LOGI_G433":   {"impedance": "39", "sensitivity": "107", "driver_size": "40"},
    "LOGI_G435":   {"impedance": "32", "sensitivity": "93",  "driver_size": "40"},
    "LOGI_G533":   {"impedance": "39", "sensitivity": "107", "driver_size": "40"},
    "LOGI_G635":   {"impedance": "39", "sensitivity": "107", "driver_size": "50"},
    "LOGI_G735":   {"impedance": "32", "sensitivity": "93",  "driver_size": "40"},
    "LOGI_G930":   {"impedance": "32", "sensitivity": "90",  "driver_size": "40"},
    # ---- More Razer ----
    "RAZER_KRAKENX":    {"impedance": "32", "sensitivity": "109", "driver_size": "40"},
    "RAZER_KRAKENULTI": {"impedance": "32", "sensitivity": "109", "driver_size": "50"},
    "RAZER_NARIU":      {"impedance": "32", "sensitivity": "109", "driver_size": "50"},
    "RAZER_OPUS2020":   {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "RAZER_BARRACUDAX": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- Audio-Technica additions ----
    "ATECH_ES55":  {"impedance": "40", "sensitivity": "100", "driver_size": "40"},
    "ATECH_ANC70": {"impedance": "38", "sensitivity": "98",  "driver_size": "40"},
    "ATECH_ANC50": {"impedance": "40", "sensitivity": "100", "driver_size": "40"},
    # ---- AKG additions ----
    "AKG_K272HD": {"impedance": "55", "sensitivity": "91",  "driver_size": "30"},
    "AKG_K67":    {"impedance": "32", "sensitivity": "114", "driver_size": "40"},
    "AKG_K44":    {"impedance": "32", "sensitivity": "112", "driver_size": "40"},
    # ---- Sennheiser consumer budget ----
    "SENN_HD429": {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "SENN_HD439": {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "SENN_HD449": {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "SENN_HD471": {"impedance": "32", "sensitivity": "115"},
    "SENN_HD515": {"impedance": "50", "sensitivity": "112"},
    # ---- HiFiMan original era ----
    "HIFIMAN_HE5LE": {"impedance": "50",  "sensitivity": "89"},
    "HIFIMAN_HEX4":  {"impedance": "18",  "sensitivity": "94"},
    "HIFIMAN_HE300": {"impedance": "32",  "sensitivity": "92"},
    # ---- Beyerdynamic budget consumer ----
    "BEYER_DT231": {"impedance": "32", "sensitivity": "102", "driver_size": "45"},
    "BEYER_DT235": {"impedance": "32", "sensitivity": "100", "driver_size": "45"},
    # ---- Phiaton ----
    "PHIATON_MS530": {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "PHIATON_MS500": {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    "PHIATON_PS500": {"impedance": "32", "sensitivity": "110"},
    "PHIATON_PS320": {"impedance": "32", "sensitivity": "112", "driver_size": "40"},
    "PHIATON_BT460": {"impedance": "32", "sensitivity": "110", "driver_size": "40"},
    # ---- Teufel ----
    "TEUFEL_ZOLA":      {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "TEUFEL_CAGE":      {"impedance": "32", "sensitivity": "98",  "driver_size": "40"},
    "TEUFEL_REALBLUENC":{"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "TEUFEL_REALZ":     {"impedance": "50", "sensitivity": "100", "driver_size": "40"},
    # ---- Cooler Master ----
    "CM_MH630": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "CM_MH751": {"impedance": "26", "sensitivity": "100", "driver_size": "40"},
    "CM_MH752": {"impedance": "26", "sensitivity": "100", "driver_size": "40"},
    # ---- House of Marley ----
    "MARLEY_PV2":    {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "MARLEY_PV2BT":  {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "MARLEY_STIRIUP":{"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- Plantronics ----
    "PLANT_BB500": {"impedance": "32", "sensitivity": "100"},
    "PLANT_BB600": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    "PLANT_BB810": {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- Remaining dynamic gaps from gap analysis ----
    # Pioneer
    "PIONEER_HDJCUE1":  {"impedance": "32", "sensitivity": "104", "driver_size": "40"},
    "PIONEER_SEA1000":  {"impedance": "32", "sensitivity": "100", "driver_size": "50"},
    # Panasonic (standard consumer dynamic; specs per Panasonic product pages)
    "PANA_RPHC800": {"impedance": "32", "sensitivity": "98",  "driver_size": "40"},
    "PANA_RPHT600": {"impedance": "32", "sensitivity": "96",  "driver_size": "40"},
    # Sony Qualia 010 (MDR-Q010): Sony's 2003 ~¥300,000 flagship; 70mm biocellulose dome
    "SONY_QUALIA010":   {"impedance": "8",  "sensitivity": "104", "driver_size": "70"},
    # Audio-Technica ATH-EW9: ear-clip; tiny 13.4mm driver; low impedance/sensitivity typical for design
    "ATECH_EW9":        {"impedance": "16", "sensitivity": "96",  "driver_size": "13"},
    # JVC HA-SR75S: compact on-ear; low impedance driver
    "JVC_HASR75S":      {"impedance": "16", "sensitivity": "100", "driver_size": "30"},
    # Focal Celestee Diablo: same driver as Celestee — purely a colourway variant
    "FOCAL_DIABLO":     {"impedance": "35", "sensitivity": "105", "driver_size": "40"},
    # Kiwi Ears Division: dynamic open-back; typical modern specs
    "KIWIEARS_DIVISION":{"impedance": "32", "sensitivity": "98",  "driver_size": "40"},
    # House of Marley Exodus: premium lifestyle closed-back
    "MARLEY_EXODUS":    {"impedance": "32", "sensitivity": "100", "driver_size": "40"},
    # ---- JVC Victor ----
    "JVC_HADX1000": {"impedance": "32",  "sensitivity": "104", "driver_size": "50"},
    "JVC_HADX2000": {"impedance": "16",  "sensitivity": "102", "driver_size": "50"},
    "JVC_HASW01":   {"impedance": "40",  "sensitivity": "96"},
    "JVC_HASW02":   {"impedance": "40",  "sensitivity": "96"},
    "JVC_HAMX100Z": {"impedance": "24",  "sensitivity": "106", "driver_size": "45"},
    # ---- Tago Studio ----
    "TAGO_T301": {"impedance": "150", "sensitivity": "97"},
    "TAGO_T302": {"impedance": "150", "sensitivity": "97"},
    # ---- Takstar ----
    "TAKSTAR_PRO80":  {"impedance": "32",  "sensitivity": "102", "driver_size": "45"},
    "TAKSTAR_PRO82":  {"impedance": "32",  "sensitivity": "102", "driver_size": "45"},
    "TAKSTAR_HF580":  {"impedance": "50",  "sensitivity": "100"},
    "TAKSTAR_HF660S": {"impedance": "50",  "sensitivity": "100"},
    "TAKSTAR_SR5H":   {"impedance": "47",  "sensitivity": "102", "driver_size": "45"},
    # ---- Goldplanar ----
    "GOLD_GL2000DS": {"impedance": "35", "sensitivity": "96"},
    "GOLD_GL2000SS": {"impedance": "35", "sensitivity": "96"},
    "GOLD_GL850":    {"impedance": "35", "sensitivity": "96"},
    # ---- MySphere ----
    "MYSPHERE_3":  {"impedance": "16",  "sensitivity": "98"},
    "MYSPHERE_3X": {"impedance": "16",  "sensitivity": "98"},
    # ---- Crosszone ----
    "CZ_CZ1":  {"impedance": "25",  "sensitivity": "100", "driver_size": "40"},
    "CZ_CZ10": {"impedance": "25",  "sensitivity": "100", "driver_size": "40"},
    # ---- Panasonic ----
    "PANA_RPHD10": {"impedance": "32",  "sensitivity": "98",  "driver_size": "40"},
    # ---- 2024-2025 new releases ----
    "BEYER_DT770PRO_LTD": {"impedance": "48", "sensitivity": "100", "driver_size": "45"},
    "BEYER_DT1990MK2":    {"impedance": "30", "sensitivity": "94",  "driver_size": "45"},
    "BEYER_MMX300PRO":    {"impedance": "48", "sensitivity": "100", "driver_size": "45"},
    "HIFIMAN_SUSVARAUNV": {"impedance": "60", "sensitivity": "83"},
    "AUDEZE_LCD5S":       {"impedance": "14", "sensitivity": "90",  "driver_size": "90"},
    "MEZE_EMPYREAN3":     {"impedance": "31.6","sensitivity": "102"},
    "SONY_WH1000XM6":     {"impedance": "16", "sensitivity": "100", "driver_size": "30"},
}

products = []
lineage_pairs = set()
for _int_id, row in enumerate(P, start=1):
    (pid, mfr, fam, model, full, year, disc, status, cat, design, driver,
     dsize, imp, sens, wl, anc, pred, succ, notes, date_added, fit) = row
    if pid in SPECS:
        s = SPECS[pid]
        dsize = s.get("driver_size", dsize)
        imp = s.get("impedance", imp)
        sens = s.get("sensitivity", sens)
    fid = fam_id.get((mfr, fam), "")
    mid = mfr_id[mfr]
    products.append([_int_id, pid, fid, mid, model, full, year, disc, status, cat,
                     design, driver, dsize, imp, sens, wl, anc, pred, succ, notes, date_added, fit])
    if pred:
        lineage_pairs.add((pred, pid))
    if succ:
        lineage_pairs.add((pid, succ))

# ---------------------------------------------------------------------------
# Write CSVs
# ---------------------------------------------------------------------------
with open(OUT / "manufacturers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["manufacturer_id","name","country","website","status"])
    w.writerows(manufacturers)

with open(OUT / "families.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["family_id","manufacturer_id","family_name","family_type"])
    w.writerows(families)

with open(OUT / "products.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id","product_id","family_id","manufacturer_id","model_name","full_name",
                "release_year","discontinued_year","status","category","design",
                "driver_type","driver_size_mm","impedance_ohms","sensitivity_db",
                "wireless","anc","predecessor","successor","notes","date_added","fit"])
    w.writerows(products)

lineage = sorted(lineage_pairs, key=lambda x: (x[1], x[0]))
with open(OUT / "lineage.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["lineage_id","predecessor_product_id","successor_product_id"])
    for i, (pre, suc) in enumerate(lineage, start=1):
        w.writerow([i, pre, suc])

print(f"Manufacturers: {len(manufacturers)}")
print(f"Families:      {len(families)}")
print(f"Products:      {len(products)}")
print(f"Lineage links: {len(lineage)}")
