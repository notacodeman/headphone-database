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
def add(pid, mfr, fam, model, full, year, status, design, driver, wireless, anc,
        pred="", succ="", notes="", disc="", category="Headphone",
        driver_size="", impedance="", sensitivity=""):
    P.append([pid, mfr, fam, model, full, year, disc, status, category,
              design, driver, driver_size, impedance, sensitivity,
              wireless, anc, pred, succ, notes])

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
add("SONY_WHH900N","Sony","WH","WH-H900N","Sony WH-H900N (h.ear on 2)",2017,"Discontinued","Closed Back","Dynamic","Yes","Yes")
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
add("SENN_HD620S","Sennheiser","HD","HD 620S","Sennheiser HD 620S",2024,"Active","Closed Back","Dynamic","No","No",notes="Closed-back addition to 600 line")
add("SENN_HD550","Sennheiser","HD","HD 550","Sennheiser HD 550",2025,"Active","Open Back","Dynamic","No","No")
add("SENN_MOMENTUM","Sennheiser","Momentum","Momentum","Sennheiser Momentum",2013,"Discontinued","Closed Back","Dynamic","No","No",succ="SENN_MOMENTUM2",notes="Original Momentum over-ear")
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
add("BEYER_AVENTHOW","Beyerdynamic","T-Series","Aventho Wireless","Beyerdynamic Aventho Wireless",2017,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone")
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
add("BW_P5","Bowers & Wilkins","P-Series","P5","Bowers & Wilkins P5",2010,"Discontinued","Closed Back","Dynamic","No","No",notes="First B&W headphone")
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
add("GRADO_SR60X","Grado","Prestige","SR60x","Grado SR60x",2021,"Active","Open Back","Dynamic","No","No",category="Headphone")
add("GRADO_SR80X","Grado","Prestige","SR80x","Grado SR80x",2021,"Active","Open Back","Dynamic","No","No",notes="Longest-running Grado model")
add("GRADO_SR325X","Grado","Prestige","SR325x","Grado SR325x",2021,"Active","Open Back","Dynamic","No","No",notes="Metal housing")
add("GRADO_RS1X","Grado","Reference","RS1x","Grado RS1x",2021,"Active","Open Back","Dynamic","No","No",notes="Tri-wood housing")
add("GRADO_RS2X","Grado","Reference","RS2x","Grado RS2x",2021,"Active","Open Back","Dynamic","No","No")
add("GRADO_GS3000X","Grado","Statement","GS3000x","Grado GS3000x",2021,"Active","Open Back","Dynamic","No","No",notes="Cocobolo flagship")
add("GRADO_HEMP","Grado","Prestige","Hemp","Grado Hemp Headphone",2020,"Discontinued","Open Back","Dynamic","No","No",notes="Limited hemp-housing model")
add("GRADO_GW100X","Grado","GW","GW100x","Grado GW100x",2021,"Active","Open Back","Dynamic","Yes","No",notes="Wireless open-back")

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
add("BEATS_SOLO3","Beats","Solo","Solo 3","Beats Solo 3 Wireless",2016,"Discontinued","Closed Back","Dynamic","Yes","No",succ="BEATS_SOLO4",category="Headphone")
add("BEATS_SOLO4","Beats","Solo","Solo 4","Beats Solo 4",2024,"Active","Closed Back","Dynamic","Yes","No",pred="BEATS_SOLO3",category="Headphone")

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
add("BO_H6","Bang & Olufsen","Beoplay","Beoplay H6","Bang & Olufsen Beoplay H6",2013,"Discontinued","Closed Back","Dynamic","No","No")
# ---- Sonos ----
add("SONOS_ACE","Sonos","Ace","Ace","Sonos Ace",2024,"Active","Closed Back","Dynamic","Yes","Yes",notes="First Sonos headphone")
# ---- Marshall ----
add("MARSHALL_MONITOR2","Marshall","Monitor","Monitor II ANC","Marshall Monitor II ANC",2020,"Active","Closed Back","Dynamic","Yes","Yes")
add("MARSHALL_MAJOR4","Marshall","Monitor","Major IV","Marshall Major IV",2021,"Active","Closed Back","Dynamic","Yes","No",category="Headphone")
add("MARSHALL_MAJOR5","Marshall","Monitor","Major V","Marshall Major V",2024,"Active","Closed Back","Dynamic","Yes","No",category="Headphone")
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
add("SENN_HD598CS","Sennheiser","HD 500-series","HD 598 Cs","Sennheiser HD 598 Cs",2016,"Discontinued","Closed Back","Dynamic","No","No",notes="Closed-back variant")
add("SENN_HD559","Sennheiser","HD 500-series","HD 559","Sennheiser HD 559",2016,"Active","Open Back","Dynamic","No","No",pred="SENN_HD558")
add("SENN_HD569","Sennheiser","HD 500-series","HD 569","Sennheiser HD 569",2016,"Active","Closed Back","Dynamic","No","No")
add("SENN_HD579","Sennheiser","HD 500-series","HD 579","Sennheiser HD 579",2016,"Active","Open Back","Dynamic","No","No")
add("SENN_HD599","Sennheiser","HD 500-series","HD 599","Sennheiser HD 599",2016,"Active","Open Back","Dynamic","No","No",pred="SENN_HD598")
add("SENN_HD505","Sennheiser","HD 500-series","HD 505","Sennheiser HD 505",2025,"Active","Open Back","Dynamic","No","No")
add("SENN_HD25","Sennheiser","HD","HD 25","Sennheiser HD 25",2010,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="On-ear DJ/monitoring standard")
add("SENN_HD250BT","Sennheiser","HD","HD 250BT","Sennheiser HD 250BT",2020,"Active","Closed Back","Dynamic","Yes","No",category="Headphone")
add("SENN_HD350BT","Sennheiser","HD","HD 350BT","Sennheiser HD 350BT",2019,"Active","Closed Back","Dynamic","Yes","No")
add("SENN_HD450BT","Sennheiser","HD","HD 450BT","Sennheiser HD 450BT",2019,"Active","Closed Back","Dynamic","Yes","Yes")
add("SENN_HD4_40BT","Sennheiser","HD","HD 4.40 BT","Sennheiser HD 4.40 BT",2016,"Discontinued","Closed Back","Dynamic","Yes","No")
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
add("SONY_ZX110","Sony","ZX","MDR-ZX110","Sony MDR-ZX110",2014,"Active","Closed Back","Dynamic","No","No",notes="Budget on-ear")
add("SONY_ZX310","Sony","ZX","MDR-ZX310","Sony MDR-ZX310",2014,"Active","Closed Back","Dynamic","No","No")
add("SONY_ZX750BN","Sony","ZX","MDR-ZX750BN","Sony MDR-ZX750BN",2014,"Discontinued","Closed Back","Dynamic","Yes","Yes")
add("SONY_XB650","Sony","XB","MDR-XB650BT","Sony MDR-XB650BT",2016,"Discontinued","Closed Back","Dynamic","Yes","No",notes="Extra Bass")
add("SONY_XB950B1","Sony","XB","MDR-XB950B1","Sony MDR-XB950B1",2016,"Discontinued","Closed Back","Dynamic","Yes","No")
add("SONY_XB900N","Sony","XB","WH-XB900N","Sony WH-XB900N",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="SONY_XB910N",notes="Extra Bass ANC")
add("SONY_XB910N","Sony","XB","WH-XB910N","Sony WH-XB910N",2021,"Active","Closed Back","Dynamic","Yes","Yes",pred="SONY_XB900N")
add("SONY_CH500","Sony","CH","WH-CH500","Sony WH-CH500",2018,"Discontinued","Closed Back","Dynamic","Yes","No")
add("SONY_CH510","Sony","CH","WH-CH510","Sony WH-CH510",2019,"Active","Closed Back","Dynamic","Yes","No")
add("SONY_CH520","Sony","CH","WH-CH520","Sony WH-CH520",2023,"Active","Closed Back","Dynamic","Yes","No")
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
add("AKG_Y50BT","AKG","K-Series","Y50BT","AKG Y50BT",2015,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone")

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

# ---- Bose: on-ear and earlier travel models ----
add("BOSE_QC3","Bose","QuietComfort On-Ear","QuietComfort 3","Bose QuietComfort 3",2006,"Discontinued","Closed Back","Dynamic","No","Yes",notes="On-ear ANC")
add("BOSE_OE2","Bose","AE/SoundLink","OE2","Bose OE2",2011,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone")
add("BOSE_AE2","Bose","AE/SoundLink","AE2","Bose AE2",2010,"Discontinued","Closed Back","Dynamic","No","No")
add("BOSE_SOUNDLINKAE","Bose","AE/SoundLink","SoundLink Around-Ear II","Bose SoundLink Around-Ear II",2015,"Discontinued","Closed Back","Dynamic","Yes","No")
add("BOSE_SOUNDLINKOE","Bose","AE/SoundLink","SoundLink On-Ear","Bose SoundLink On-Ear",2016,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone")

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
add("FOCAL_LISTEN","Focal","Listen","Listen","Focal Listen",2016,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone")
add("FOCAL_LISTENPRO","Focal","Spirit","Listen Professional","Focal Listen Professional",2017,"Active","Closed Back","Dynamic","No","No",category="Studio")
add("FOCAL_LISTENWL","Focal","Listen","Listen Wireless","Focal Listen Wireless",2017,"Discontinued","Closed Back","Dynamic","Yes","No")
add("FOCAL_ELEX","Focal","Clear","Elex","Drop x Focal Elex",2017,"Active","Open Back","Dynamic","No","No",notes="Drop collaboration")
add("FOCAL_CLEARPRO","Focal","Clear","Clear Professional","Focal Clear Professional",2018,"Active","Open Back","Dynamic","No","No",category="Studio")
add("FOCAL_RADIANCE","Focal","Elegia","Radiance","Focal Radiance",2019,"Discontinued","Closed Back","Dynamic","No","No",notes="Bentley edition")
add("FOCAL_CLEARMGPRO","Focal","Clear","Clear MG Professional","Focal Clear MG Professional",2021,"Active","Open Back","Dynamic","No","No",category="Studio")

# ---- Grado: full Prestige/Reference/Statement, i and e generations ----
add("GRADO_SR125X","Grado","Prestige","SR125x","Grado SR125x",2021,"Active","Open Back","Dynamic","No","No")
add("GRADO_SR225X","Grado","Prestige","SR225x","Grado SR225x",2021,"Active","Open Back","Dynamic","No","No")
add("GRADO_SR80E","Grado","Prestige","SR80e","Grado SR80e",2014,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR80X")
add("GRADO_SR325E","Grado","Prestige","SR325e","Grado SR325e",2014,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR325X")
add("GRADO_RS2E","Grado","Reference","RS2e","Grado RS2e",2014,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_RS2X")
add("GRADO_GS1000X","Grado","Statement","GS1000x","Grado GS1000x",2022,"Active","Open Back","Dynamic","No","No")
add("GRADO_PS500E","Grado","Statement-PS","PS500e","Grado PS500e",2014,"Discontinued","Open Back","Dynamic","No","No")
add("GRADO_PS1000E","Grado","Statement-PS","PS1000e","Grado PS1000e",2014,"Active","Open Back","Dynamic","No","No",notes="Pro statement flagship")
add("GRADO_PS2000E","Grado","Statement-PS","PS2000e","Grado PS2000e",2017,"Active","Open Back","Dynamic","No","No",notes="Statement flagship")

# ---- Meze: lower lines + variants ----
add("MEZE_99NOIR","Meze Audio","Classics","99 Classics Noir","Meze 99 Classics Noir",2017,"Active","Closed Back","Dynamic","No","No",notes="All-black variant w/ tuning tweak")
add("MEZE_109PRODESC","Meze Audio","Classics","109 Pro Descenso","Meze 109 Pro Descenso",2024,"Active","Open Back","Dynamic","No","No")
add("MEZE_EMPYREAN2","Meze Audio","Flagship","Empyrean II","Meze Empyrean II",2024,"Active","Open Back","Planar Magnetic","No","No",pred="MEZE_EMPYREAN")
add("MEZE_LIRICII","Meze Audio","Flagship","Liric II","Meze Liric II",2024,"Active","Closed Back","Planar Magnetic","No","No")

# ---- Bowers & Wilkins: earlier on-ear P-series + PX5 ----
add("BW_P3","Bowers & Wilkins","P-Series","P3","Bowers & Wilkins P3",2011,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone")
add("BW_P5S2","Bowers & Wilkins","P-Series","P5 Series 2","Bowers & Wilkins P5 Series 2",2014,"Discontinued","Closed Back","Dynamic","No","No",pred="BW_P5",category="Headphone")
add("BW_P7WIRELESS","Bowers & Wilkins","P-Series","P7 Wireless","Bowers & Wilkins P7 Wireless",2015,"Discontinued","Closed Back","Dynamic","Yes","No")
add("BW_PX5","Bowers & Wilkins","PX","PX5","Bowers & Wilkins PX5",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",category="Headphone",notes="On-ear ANC")

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
add("BO_H4","Bang & Olufsen","Beoplay","Beoplay H4","Bang & Olufsen Beoplay H4",2017,"Discontinued","Closed Back","Dynamic","Yes","No")
add("BO_H9","Bang & Olufsen","Beoplay","Beoplay H9","Bang & Olufsen Beoplay H9",2017,"Discontinued","Closed Back","Dynamic","Yes","Yes")
add("BO_PORTAL","Bang & Olufsen","Beoplay Portal","Beoplay Portal","Bang & Olufsen Beoplay Portal",2021,"Active","Closed Back","Dynamic","Yes","Yes",category="Gaming",notes="Gaming/lifestyle hybrid")
add("JBL_LIVE770NC","JBL","Live","Live 770NC","JBL Live 770NC",2023,"Active","Closed Back","Dynamic","Yes","Yes")
add("JBL_QUANTUM910","JBL","Quantum","Quantum 910 Wireless","JBL Quantum 910 Wireless",2022,"Active","Closed Back","Dynamic","Yes","Yes",category="Gaming")
add("MARSHALL_MIDANC","Marshall","Monitor","Mid ANC","Marshall Mid ANC",2018,"Discontinued","Closed Back","Dynamic","Yes","Yes",category="Headphone")
add("SKULL_HESH3","Skullcandy","Crusher","Hesh 3","Skullcandy Hesh 3",2018,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone")
add("SKULL_CRUSHERANC","Skullcandy","Crusher","Crusher ANC","Skullcandy Crusher ANC",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",succ="SKULL_CRUSHERANC2")

# ============================================================================
# DEEPENING BATCH 3 — Beats history, consumer catalogs, more gaming
# ============================================================================

# ---- Beats: full over-ear/on-ear history ----
add("BEATS_STUDIO2013","Beats","Studio","Studio (2013)","Beats Studio (2013)",2013,"Discontinued","Closed Back","Dynamic","No","Yes",succ="BEATS_STUDIO2",notes="Redesigned wired Studio")
add("BEATS_MIXR","Beats","Pro","Mixr","Beats Mixr",2011,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",notes="DJ on-ear, David Guetta")
add("BEATS_PRO","Beats","Pro","Pro","Beats Pro",2011,"Discontinued","Closed Back","Dynamic","No","No",notes="All-metal over-ear")
add("BEATS_EXECUTIVE","Beats","Executive","Executive","Beats Executive",2012,"Discontinued","Closed Back","Dynamic","No","Yes",notes="Aluminum ANC over-ear")
add("BEATS_SOLO2","Beats","Solo","Solo 2","Beats Solo 2",2014,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",succ="BEATS_SOLO3")
add("BEATS_SOLOPRO","Beats","Solo","Solo Pro","Beats Solo Pro",2019,"Discontinued","Closed Back","Dynamic","Yes","Yes",category="Headphone",notes="On-ear ANC")
add("BEATS_EP","Beats","Solo","EP","Beats EP",2016,"Active","Closed Back","Dynamic","No","No",category="Headphone",notes="Budget wired on-ear")

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
add("MARSHALL_MAJOR2","Marshall","Major","Major II","Marshall Major II",2014,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone",succ="MARSHALL_MAJOR3")
add("MARSHALL_MAJOR3","Marshall","Major","Major III","Marshall Major III",2018,"Discontinued","Closed Back","Dynamic","Yes","No",category="Headphone",pred="MARSHALL_MAJOR2",succ="MARSHALL_MAJOR4")
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
add("SENN_HD25_1","Sennheiser","HD","HD 25-1","Sennheiser HD 25-1",1988,"Legacy Active","Closed Back","Dynamic","No","No",category="Studio",notes="On-ear monitoring/DJ standard")
add("SENN_HD555","Sennheiser","HD 500-series","HD 555","Sennheiser HD 555",2005,"Discontinued","Open Back","Dynamic","No","No",succ="SENN_HD558")
add("SENN_HD595","Sennheiser","HD 500-series","HD 595","Sennheiser HD 595",2005,"Discontinued","Open Back","Dynamic","No","No",succ="SENN_HD598")
add("SENN_HD280PRO","Sennheiser","HD 200-series","HD 280 Pro","Sennheiser HD 280 Pro",2003,"Active","Closed Back","Dynamic","No","No",category="Studio",notes="Studio monitoring staple")
add("SENN_HD202","Sennheiser","HD 200-series","HD 202","Sennheiser HD 202",2003,"Discontinued","Closed Back","Dynamic","No","No")
add("SENN_PX100","Sennheiser","HD Classic","PX 100","Sennheiser PX 100",2003,"Discontinued","Open Back","Dynamic","No","No",category="Headphone",notes="Portable on-ear")
add("SENN_PX200","Sennheiser","HD Classic","PX 200","Sennheiser PX 200",2004,"Discontinued","Closed Back","Dynamic","No","No",category="Headphone")
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
add("GRADO_SR60","Grado","Vintage","SR60","Grado SR60",1991,"Discontinued","Open Back","Dynamic","No","No",notes="The headphone that launched the Prestige line")
add("GRADO_RS1","Grado","Reference","RS1","Grado RS1",1994,"Discontinued","Open Back","Dynamic","No","No",notes="Original mahogany Reference")
add("GRADO_SR325I","Grado","Prestige","SR325i","Grado SR325i",2008,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_SR325E")
add("GRADO_GS1000","Grado","Statement","GS1000","Grado GS1000",2006,"Discontinued","Open Back","Dynamic","No","No",notes="First Statement-series, large bowl pads")
add("GRADO_PS1000","Grado","Statement-PS","PS1000","Grado PS1000",2009,"Discontinued","Open Back","Dynamic","No","No",succ="GRADO_PS1000E")

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
add("KOSS_PORTAPRO","Koss","Porta Pro","Porta Pro","Koss Porta Pro",1984,"Legacy Active","Open Back","Dynamic","No","No",category="Headphone",notes="Iconic on-ear, in production since 1984")
add("KOSS_PORTAPROWL","Koss","Porta Pro","Porta Pro Wireless","Koss Porta Pro Wireless",2020,"Active","Open Back","Dynamic","Yes","No",category="Headphone")
add("KOSS_KSC75","Koss","KSC","KSC75","Koss KSC75",1998,"Active","Open Back","Dynamic","No","No",category="Headphone",notes="Cult-favorite clip-on")
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
add("GRADO_S550","Grado","Statement","Signature S550","Grado Signature S550",2026,"Active","Open Back","Dynamic","No","No",notes="Debuted CanJam NYC 2026")

# ---------------------------------------------------------------------------
# Resolve family ids and build lineage from predecessor/successor links
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# SPECS backfill table — driver size (mm), impedance (ohms), sensitivity (dB)
# Keyed by product_id. Sourced from manufacturer pages / reputable spec sheets.
# Grown brand-by-brand over time; leave a field "" when not reliably published.
# ---------------------------------------------------------------------------
SPECS = {
    # ---- Sennheiser (impedance & sensitivity well published; driver size rarely) ----
    "SENN_HD600":   {"impedance": "300", "sensitivity": "97"},
    "SENN_HD650":   {"impedance": "300", "sensitivity": "103"},
    "SENN_HD660S":  {"impedance": "150", "sensitivity": "104"},
    "SENN_HD660S2": {"impedance": "300", "sensitivity": "104", "driver_size": "38"},
    "SENN_HD800":   {"impedance": "300", "sensitivity": "102", "driver_size": "56"},
    "SENN_HD800S":  {"impedance": "300", "sensitivity": "102", "driver_size": "56"},
    # ---- Beyerdynamic (impedance is the defining spec; DT series use 45mm drivers) ----
    "BEYER_DT770_32":   {"impedance": "32",  "driver_size": "45"},
    "BEYER_DT770_80":   {"impedance": "80",  "sensitivity": "96", "driver_size": "45"},
    "BEYER_DT770_250":  {"impedance": "250", "sensitivity": "96", "driver_size": "45"},
    "BEYER_DT880_250":  {"impedance": "250", "sensitivity": "96", "driver_size": "45"},
    "BEYER_DT990_250":  {"impedance": "250", "sensitivity": "96", "driver_size": "45"},
    "BEYER_DT880_2005": {"impedance": "250", "sensitivity": "96", "driver_size": "45"},
    # ---- HiFiMan (planar) ----
    "HIFIMAN_SUNDARA":  {"impedance": "37", "sensitivity": "94"},
    "HIFIMAN_HE400SE":  {"impedance": "32", "sensitivity": "91"},
    "HIFIMAN_ANANDA":   {"impedance": "25", "sensitivity": "103"},
    # ---- Philips ----
    "PHIL_X2HR":    {"impedance": "30", "sensitivity": "100", "driver_size": "50"},
    "PHIL_SHP9500": {"impedance": "32", "sensitivity": "101", "driver_size": "50"},
    "PHIL_X3":      {"impedance": "30", "sensitivity": "100", "driver_size": "50"},
    # ---- Sony ----
    "SONY_MDR7506":   {"impedance": "63", "sensitivity": "106", "driver_size": "40"},
    "SONY_MDRV6":     {"impedance": "63", "sensitivity": "106", "driver_size": "40"},
    "SONY_MDRZ1R":    {"impedance": "64", "sensitivity": "100", "driver_size": "70"},
    "SONY_MDRMV1":    {"impedance": "24", "sensitivity": "100", "driver_size": "40"},
    "SONY_WH1000XM5": {"driver_size": "30"},
}

products = []
lineage_pairs = set()
for row in P:
    (pid, mfr, fam, model, full, year, disc, status, cat, design, driver,
     dsize, imp, sens, wl, anc, pred, succ, notes) = row
    if pid in SPECS:
        s = SPECS[pid]
        dsize = s.get("driver_size", dsize)
        imp = s.get("impedance", imp)
        sens = s.get("sensitivity", sens)
    fid = fam_id.get((mfr, fam), "")
    mid = mfr_id[mfr]
    products.append([pid, fid, mid, model, full, year, disc, status, cat,
                     design, driver, dsize, imp, sens, wl, anc, pred, succ, notes])
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
    w.writerow(["product_id","family_id","manufacturer_id","model_name","full_name",
                "release_year","discontinued_year","status","category","design",
                "driver_type","driver_size_mm","impedance_ohms","sensitivity_db",
                "wireless","anc","predecessor","successor","notes"])
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
