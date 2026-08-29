#!/usr/bin/env python3
"""Canonical data generator for the headphone archive.

This script is the single source of truth for the catalog *content*: every headphone,
brand, family, and lineage link is hand-entered here as Python, then written out to the
CSVs in database/. Those CSVs seed the live D1 database (via the admin import endpoint)
and act as the backup/version-controlled record. Re-run it after editing the data below
to regenerate all CSVs; the verify.py script then checks the output for integrity.
"""
import csv
from pathlib import Path

# All generated CSVs are written into the database/ directory next to this script.
OUT = Path("database")

# ---------------------------------------------------------------------------
# Manufacturers
# ---------------------------------------------------------------------------
manufacturers = [
    # id, name, country, website, status, founded_year, description
    (1,  "Sony",             "Japan",       "https://www.sony.com",            "Active",       1946, "Japanese consumer electronics giant with one of the broadest headphone catalogs in the world, spanning budget earbuds to the flagship MDR-Z1R and the iconic MDR-7506 studio standard."),
    (2,  "Sennheiser",       "Germany",     "https://www.sennheiser.com",      "Active",       1945, "German audio institution whose HD 600 series defined the reference open-back standard for a generation. The HD 800 and Orpheus HE-1 represent the outer edge of what headphones can achieve."),
    (3,  "Philips",          "Netherlands", "https://www.philips.com",         "Active",       1891, "Dutch electronics multinational whose Fidelio line produced several acclaimed audiophile headphones before the brand shifted focus toward consumer electronics."),
    (4,  "Audio-Technica",   "Japan",       "https://www.audio-technica.com",  "Active",       1962, "Japanese precision manufacturer best known for the ATH-M50x studio monitor and a deep catalog of open-back headphones from the AD and R series."),
    (5,  "AKG",              "Austria",     "https://www.akg.com",             "Active",       1947, "Viennese studio legend whose K 240 and K 701 shaped professional monitoring for decades. Now owned by Samsung/Harman but the K 812 and K 872 keep the legacy alive."),
    (6,  "Beyerdynamic",     "Germany",     "https://www.beyerdynamic.com",    "Active",       1924, "Century-old German manufacturer and inventor of the dynamic headphone driver. The DT 770/880/990 trilogy and Tesla-driver flagships are benchmarks of German engineering precision."),
    (7,  "Bose",             "USA",         "https://www.bose.com",            "Active",       1964, "Massachusetts-based acoustics company that popularised active noise cancellation with the QuietComfort line. Prioritises comfort, convenience, and accessible sound quality."),
    (8,  "Audeze",           "USA",         "https://www.audeze.com",          "Active",       2008, "California planar magnetic specialist that brought the technology to mainstream audiophiles with the LCD series. Their SLAM magnet arrays set efficiency records for planar design."),
    (9,  "HiFiMan",          "China",       "https://www.hifiman.com",         "Active",       2007, "Chinese planar pioneer founded by Dr. Fang Bian. Responsible for democratising planar magnetic headphones and producing the Susvara, widely considered one of the finest headphones ever made."),
    (10, "Focal",            "France",      "https://www.focal.com",           "Active",       1979, "French speaker manufacturer whose entry into headphones with the Utopia and Elear reshaped the high-end market. Known for beryllium-domed drivers and premium cabinet-grade materials."),
    (11, "Bowers & Wilkins", "UK",          "https://www.bowerswilkins.com",   "Active",       1966, "British hi-fi institution whose Px series brought premium wireless to a design-conscious audience. The P9 Signature remains a statement piece for the brand."),
    (12, "Grado",            "USA",         "https://gradolabs.com",           "Active",       1953, "Brooklyn family business spanning three generations, making supra-aural open-back headphones by hand since the 1950s. Unmistakable sound, unmistakable look."),
    (13, "Meze Audio",       "Romania",     "https://mezeaudio.com",           "Active",       2011, "Romanian boutique that stunned the audiophile world with the 99 Classics in 2015 and followed up with the Empyrean — a flagship using Rinaro's isodynamic planar driver."),
    (14, "Dan Clark Audio",  "USA",         "https://danclarkaudio.com",       "Active",       2011, "San Diego workshop founded as MrSpeakers. Known for T50RP modifications that evolved into original planar designs including the Ether and STEALTH."),
    (15, "Apple",            "USA",         "https://www.apple.com",           "Active",       1976, "Cupertino technology company whose AirPods Max brought Apple's design language and computational audio to the over-ear headphone market."),
    (16, "Beats",            "USA",         "https://www.beatsbydre.com",      "Active",       2006, "Brand founded by Dr. Dre and Jimmy Iovine that made headphones a fashion accessory. Acquired by Apple in 2014 and now integrates Apple silicon for spatial audio."),
    (17, "Shure",            "USA",         "https://www.shure.com",           "Active",       1925, "Chicago microphone and audio equipment company whose SRH line is a studio workhorse. The SRH1540 and SRH1840 are respected reference tools."),
    (18, "SteelSeries",      "Denmark",     "https://steelseries.com",         "Active",       2001, "Danish gaming peripherals brand whose Arctis series redefined the gaming headset with ski-goggle headbands and a focus on comfort for long sessions."),
    (19, "HyperX",           "USA",         "https://www.hyperx.com",          "Active",       2002, "Kingston's gaming brand, producing the Cloud series of studio-driver-based headsets that punched well above their price. Now owned by HP."),
    (20, "Razer",            "USA",         "https://www.razer.com",           "Active",       2005, "Gaming hardware brand from San Francisco. The Kraken and BlackShark V2 series are popular esports headsets; the Opus line targets lifestyle listeners."),
    (21, "Logitech G",       "Switzerland", "https://www.logitechg.com",       "Active",       1981, "Swiss peripherals giant whose G Pro X series used Blue Microphone technology and swappable drivers to target competitive gamers."),
    (22, "Astro Gaming",     "USA",         "https://www.astro.com",           "Active",       2006, "Console gaming headset specialist whose A40 TR and A50 Wireless are fixtures in professional esports broadcasting setups. Owned by Logitech."),
    (23, "Turtle Beach",     "USA",         "https://www.turtlebeach.com",     "Active",       1975, "Veteran gaming headset maker that pioneered surround-sound processing in console headsets. The Stealth series remains a popular mid-tier choice."),
    (24, "Corsair",          "USA",         "https://www.corsair.com",         "Active",       1994, "PC hardware company whose Virtuoso series targets PC gamers with high-resolution audio and premium build quality."),
    (25, "ASUS ROG",         "Taiwan",      "https://rog.asus.com",            "Active",       2006, "Republic of Gamers division of ASUS, producing gaming headsets with aggressive styling and ESS DAC-equipped USB audio."),
    (26, "Abyss",            "USA",         "https://abyss-headphones.com",    "Active",       2012, "Upstate New York boutique producing the AB-1266, a flagship open planar headphone with a bold industrial design that has no counterpart on the market."),
    (27, "ZMF Headphones",   "USA",         "https://www.zmfheadphones.com",   "Active",       2013, "Chicago one-man operation by Zach Mehrbach building handcrafted wood-cupped dynamic and planar headphones. Long lead times, devoted following."),
    (28, "Stax",             "Japan",       "https://stax.co.jp",              "Active",       1938, "The definitive electrostatic headphone maker, producing earspeakers since 1938. The SR-009 and SR-X9000 are considered the purest transducers available at any price."),
    (29, "Final Audio",      "Japan",       "https://final-inc.com",           "Active",       1974, "Japanese audio laboratory known for unconventional acoustic engineering. The D8000 planar and Sonorous series are boundary-pushing products from a deeply research-driven company."),
    (30, "Fostex",           "Japan",       "https://www.fostex.jp",           "Active",       1973, "Japanese driver manufacturer whose T50RP became the most-modded headphone in audiophile history, and whose TH900 series uses biodynamic technology."),
    (31, "Denon",            "Japan",       "https://www.denon.com",           "Active",       1910, "Japanese audio institution whose AH-D series closed-backs use biodynamic 50mm drivers. The D9200 with its nano-fibre diaphragm is a standout statement product."),
    (32, "Rosson Audio",     "USA",         "https://rossonaudiodesign.com",   "Active",       2017, "Small-batch planar workshop by Alex Rosson, co-founder of Audeze. The RAD-0 is a hand-made statement piece with custom wood cups."),
    (33, "Kennerton",        "Russia",      "https://kennerton.com",           "Active",       2012, "St. Petersburg audio atelier building planar magnetic flagships in exotic wood housings. The Odin and Thror are among the most beautiful headphones made."),
    (34, "Ultrasone",        "Germany",     "https://www.ultrasone.com",       "Active",       1986, "Bavarian company behind the S-Logic spatial driver technology, which positions the driver off-axis to reduce ear canal pressure and create a wider perceived soundstage."),
    (35, "Bang & Olufsen",   "Denmark",     "https://www.bang-olufsen.com",    "Active",       1925, "Danish luxury electronics brand whose Beoplay H line is as much furniture as audio equipment. The H95 is their flagship closed-back, built from aluminium and lambskin."),
    (36, "Sonos",            "USA",         "https://www.sonos.com",           "Active",       2002, "Wireless audio company that entered headphones with the Ace, combining spatial audio and SoundSwap for seamless transition between speakers and headphones."),
    (37, "Marshall",         "UK",          "https://www.marshallheadphones.com","Active",     1962, "Iconic amplifier brand that extended into headphones in 2010. The Major series on-ear design channels the brand's rock heritage into a consumer-friendly product line."),
    (38, "JBL",              "USA",         "https://www.jbl.com",             "Active",       1946, "American speaker company under Harman. The Live and Club series cover premium consumer wireless while the Professional line serves studio monitoring."),
    (39, "Skullcandy",       "USA",         "https://www.skullcandy.com",      "Active",       2003, "Park City, Utah brand that brought bold colour and skate/snowboard culture to headphones. The Crusher series with haptic bass is a signature product."),
    (40, "Anker Soundcore",  "China",       "https://www.soundcore.com",       "Active",       2016, "Anker's audio sub-brand producing aggressively priced wireless headphones with competitive ANC. The Space Q45 punches well above its category."),
    (41, "Technics",         "Japan",       "https://www.technics.com",        "Active",       1965, "Panasonic's premium audio brand revived in 2014. The EAH-A800 wireless headphone brings hi-fi DNA to the ANC market with LDAC and multipoint connectivity."),
    (42, "Nothing",          "UK",          "https://nothing.tech",            "Active",       2020, "Carl Pei's London tech startup known for transparent industrial design. The Headphone (1) was their first over-ear, applying the brand's distinctive dot-matrix aesthetic."),
    (43, "Koss",             "USA",         "https://www.koss.com",            "Active",       1953, "Milwaukee company that invented the stereo headphone in 1958. The Porta Pro has been in continuous production since 1984 and remains a cult favourite."),
    (44, "V-Moda",           "USA",         "https://www.v-moda.com",          "Active",       2004, "Lifestyle and DJ headphone brand from Val Kolton, known for the indestructible Crossfade M-100 and a custom shield programme allowing personalised engravings."),
    (45, "Yamaha",           "Japan",       "https://www.yamaha.com",          "Active",       1887, "Musical instrument giant with a deep headphone catalog. The YH-5000SE flagship uses an orthodynamic driver derived from their 1970s HP-1 and is made in Japan."),
    (46, "Pioneer",          "Japan",       "https://www.pioneer-audiovisual.com","Active",    1938, "Japanese AV brand whose Pioneer DJ division produces the HDJ series, professional turntablist monitors trusted by DJs worldwide."),
    (47, "AIAIAI",           "Denmark",     "https://www.aiaiai.audio",        "Active",       2006, "Copenhagen brand whose TMA-2 is the world's most modular headphone — mix and match 360 components including drivers, earpads, headbands, and cables."),
    (48, "1More",            "China",       "https://www.1more.com",           "Active",       2013, "Shenzhen brand tuned in collaboration with Grammy-winning engineers. The SonoFlow series delivers wireless ANC at prices that embarrass the competition."),
    (49, "Edifier",          "China",       "https://www.edifier.com",         "Active",       1996, "Beijing audio company whose STAX Spirit line brought planar magnetic technology to mid-range wireless headphones at an accessible price."),
    (50, "Cleer",            "USA",         "https://www.cleeraudio.com",      "Active",       2012, "San Diego audio brand founded by ex-JBL engineers. The Alpha uses a custom 40mm driver and targets audiophile-grade wireless performance."),
    (51, "Austrian Audio",   "Austria",     "https://austrian.audio",          "Active",       2017, "Vienna studio founded by ex-AKG engineers after the AKG Vienna facility closed. The Hi-X55 and Hi-X65 are direct spiritual successors to AKG's studio heritage."),
    (52, "Neumann",          "Germany",     "https://www.neumann.com",         "Active",       1928, "The microphone company's headphone line is aimed squarely at mastering engineers. The NDH 20 and NDH 30 offer exceptional tonal accuracy for critical listening."),
    (53, "Moondrop",         "China",       "https://moondroplab.com",         "Active",       2015, "Chengdu IEM specialist that expanded into over-ear planars with the Venus and Para. Known for anime-inspired packaging and technically rigorous tuning based on the HRTF target."),
    (54, "Sivga",            "China",       "https://www.sivgaaudio.com",      "Active",       2016, "Chinese wood-specialist headphone maker crafting dynamic closed-backs with real rosewood, walnut, and zebrawood housings at accessible prices."),
    (55, "Sendy Audio",      "China",       "https://www.sendyaudio.com",      "Active",       2016, "Planar magnetic specialist using 97mm drivers in open-back designs. The Peacock and Aiva target the audiophile mid-fi market with premium build quality."),
    (56, "FiiO",             "China",       "https://www.fiio.com",            "Active",       2007, "Guangzhou portable audio giant best known for DACs and DAPs. The FT3 and FT5 represent their serious push into full-size headphones with large dynamic and planar drivers."),
    (57, "Spirit Torino",    "Italy",       "https://www.spirittorino.com",    "Active",       2014, "Turin boutique producing ultra-light open-back headphones designed for comfortable all-day listening. The Super Leggera is one of the lightest audiophile headphones available."),
    (58, "Warwick Acoustics","UK",          "https://warwickacoustics.com",    "Active",       2011, "British electrostatic specialist producing the Sonoma Model One and Aperio — complete systems with proprietary energisers built from aerospace-grade materials."),
    (59, "Mark Levinson",    "USA",         "https://www.marklevinson.com",    "Active",       1972, "American high-end audio brand whose No. 5909 wireless headphone brings luxury materials and Hi-Res Audio certification to the travel headphone market."),
    (60, "T+A",              "Germany",     "https://www.ta-hifi.de",          "Active",       1978, "Herford high-end manufacturer whose Solitaire P planar headphone features a 200mm driver array and is designed to pair with their in-house headphone amplifiers."),
    (61, "HEDD Audio",       "Germany",     "https://hedd.audio",              "Active",       2015, "Berlin studio monitor company whose HEDDphone uses Air Motion Transformer drivers — folded-membrane technology borrowed from loudspeakers for exceptionally fast transient response."),
    (62, "Grell Audio",      "Germany",     "https://grell-audio.com",         "Active",       2021, "Founded by Axel Grell, chief developer of the Sennheiser HD 800. The OAE1 open-air earspeaker is his attempt to solve headphone imaging from first principles."),
    (63, "Ollo Audio",       "Slovenia",    "https://www.olloaudio.com",       "Active",       2016, "Slovenian studio headphone maker offering individually tested and calibrated closed and open-back monitors, with measurement graphs shipped with each unit."),
    (64, "Monoprice",        "USA",         "https://www.monoprice.com",       "Active",       2002, "Direct-to-consumer electronics brand whose Monolith M1060 planar brought 106mm drivers to an audience that couldn't afford Audeze prices."),
    (65, "Superlux",         "Taiwan",      "https://www.superlux.com",        "Active",       1990, "Taiwanese professional audio equipment maker whose HD 668B and HD 681 are studio-standard monitors in disguise, widely used in Chinese broadcast facilities."),
    (66, "Samson",           "USA",         "https://samsontech.com",          "Active",       1980, "New York professional audio brand whose SR850 semi-open monitor is a rebranded Superlux HD 668B — one of the most recommended budget headphones in audiophile communities."),
    (67, "Status Audio",     "USA",         "https://status.co",               "Active",       2016, "Direct-to-consumer brand cutting out retail markups. The CB-1 closed-back became a breakout product in the budget audiophile market."),
    (68, "Jabra",            "Denmark",     "https://www.jabra.com",           "Active",       1993, "GN Audio's communications headset brand trusted in enterprise and contact centre environments. The Evolve2 series is engineered for all-day wearing comfort."),
    (69, "Harman Kardon",    "USA",         "https://www.harmankardon.com",    "Active",       1953, "American audio brand known for premium design. The SOHO on-ear represents a premium lifestyle offering combining Harman's speaker tuning with a portable form factor."),
    (70, "Oppo",             "USA",         "https://www.oppodigital.com",     "Discontinued", 2004, "Californian electronics company whose PM-1 and PM-3 planar headphones were critically acclaimed before the brand's closure in 2018. Now sought-after on the used market."),
    (71, "Creative",         "Singapore",   "https://us.creative.com",         "Active",       1981, "Singapore technology company whose Sound Blaster brand shaped PC audio. The Aurvana Live! uses a biodynamic driver co-developed with Foster Electric."),
    (72, "Rode",             "Australia",   "https://rode.com",                "Active",       1967, "Sydney microphone company whose NTH-100 studio headphone was developed with DSP-calibrated tuning via the NTH-Mic measurement system."),
    (73, "Klipsch",          "USA",         "https://www.klipsch.com",         "Active",       1946, "Arkansas speaker company whose Heritage HP-3 headphone uses a wooden cup design inspired by their classic horn-loaded loudspeakers."),
    (74, "RAAL",             "USA",         "https://raalrequisite.com",       "Active",       2007, "Ribbon driver specialist producing the SR1a — a headphone that uses a true ribbon transducer and requires a special interface for conventional amplifier connection."),
    (75, "HarmonicDyne",     "China",       "https://harmonicdyne.com",        "Active",       2019, "Chengdu audiophile brand producing the G200, a large-scale open planar headphone with a distinctive hexagonal driver architecture."),
    (76, "PSB",              "Canada",      "https://www.psbspeakers.com",     "Active",       1972, "Canadian speaker company whose M4U series headphones apply speaker engineering principles and active Room Feel correction to headphone acoustics."),
    (77, "E-Mu",             "USA",         "https://us.creative.com",         "Discontinued", 1971, "California synthesiser pioneer whose headphone line used biodynamic drivers co-developed with Foster Electric. The Teak and Rosewood are now collector items."),
    (78, "Audioquest",       "USA",         "https://www.audioquest.com",      "Active",       1980, "Cable and accessory specialist whose NightOwl and NightHawk used Foster biodynamic drivers in carbon fibre and wood housings before the line was discontinued."),
    (79, "NAD",              "Canada",      "https://nadelectronics.com",      "Active",       1972, "Canadian electronics brand whose VISO HP50 used RoomFeel target curve technology — an early attempt to apply room-corrected tuning to headphone listening."),
    (80, "Brainwavz",        "China",       "https://www.brainwavzaudio.com",  "Active",       2005, "Hong Kong audio brand best known for replacement earpads compatible with hundreds of headphones, and the HM5 studio monitor."),
    (81, "Modhouse Audio",   "USA",         "https://modhouse.io",             "Active",       2015, "Wisconsin modification workshop building the Argon — a T50RP Mk2 base fitted with a proprietary driver tuned for a warm, musical presentation. Waitlists measured in months."),
    (82, "Kiwi Ears",        "China",       "https://www.kiwiears.com",        "Active",       2020, "Young Chinese audio brand with rapid product cadence. The Ardor open planar earned strong reviews at its price, drawing comparisons to headphones costing three times as much."),
    (83, "Plantronics",      "USA",         "https://www.poly.com",            "Active",       1961, "Communications headset pioneer whose BackBeat line brought Bluetooth comfort to the office market. Merged with Polycom to form Poly, now part of HP."),
    (84, "Phiaton",          "South Korea", "https://www.phiaton.com",         "Active",       2009, "Korean premium audio brand producing the MS 530 — one of the earliest commercially successful wireless ANC headphones with Bluetooth at launch."),
    (85, "Teufel",           "Germany",     "https://www.teufel.de",           "Active",       1979, "Berlin direct-sales speaker brand whose Real Blue NC offers competitive ANC performance at prices below the major consumer brands."),
    (86, "House of Marley",  "USA",         "https://www.thehouseofmarley.com","Active",       2010, "Bob Marley estate brand producing headphones from sustainable materials including bamboo, hemp, and recycled plastics. Donates to environmental causes."),
    (87, "Cooler Master",    "Taiwan",      "https://www.coolermaster.com",    "Active",       1992, "PC cooling and peripheral brand whose MH751 became a surprise hit in gaming headset communities for its studio-driver-based sound quality at a modest price."),
    (88, "JVC",              "Japan",       "https://www.jvc.com",             "Active",       1927, "Victor Company of Japan, known for the HA-DX1000 and HA-DX2000 mahogany wood-cup flagship closed-backs and the HA-SW series isodynamic planars."),
    (89, "Tago Studio",      "Japan",       "https://tagostudio.com",          "Active",       2019, "Small Japanese studio headphone maker offering individually serial-numbered monitors using high-powered 1.5T Neodymium drivers. Made in Japan."),
    (90, "Takstar",          "China",       "https://www.takstar.com",         "Active",       2001, "Guangzhou professional audio company whose Pro 80 is the OEM basis for many rebranded studio monitors worldwide. The HF580 planar punches above its category."),
    (91, "Goldplanar",       "China",       "https://goldplanar.com",          "Active",       2020, "Chinese planar magnetic specialist producing the GL2000 — a dual-sided planar with a 68mm driver that delivers competitive performance at a budget price."),
    (92, "MySphere",         "Austria",     "https://mysphere.at",             "Active",       2018, "Vienna-based audio engineering project by Heinz Renner, former chief engineer at AKG. The MySphere 3 is the spiritual successor to the AKG K1000 open-air earspeaker."),
    (93, "Panasonic",        "Japan",       "https://www.panasonic.com",       "Active",       1918, "Japanese electronics conglomerate with a modest headphone catalog. The RP-HD10 is their most audiophile-focused recent offering."),
    (94, "Crosszone",        "Japan",       "https://crosszone.jp",            "Active",       2016, "Niche Japanese brand producing headphones with built-in acoustic crossfeed. The CZ-1 uses secondary in-ear drivers to simulate the inter-channel crosstalk of loudspeaker listening."),
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
VALID_SOUND_SIGNATURE = {"Neutral", "Balanced", "Warm", "Bright", "V-Shaped", "Bass-Heavy", "Dark", ""}
VALID_CONNECTOR  = {"3.5mm", "6.35mm", "3.5mm + 6.35mm", "XLR", "USB-C", "Lightning", "Proprietary", "Wireless", ""}
VALID_DETACHABLE = {"Yes", "No", ""}

def add(pid, mfr, fam, model, full, year, status, design, driver, wireless, anc,
        pred="", succ="", notes="", disc="", category="Headphone",
        driver_size="", impedance="", sensitivity="", date_added="", fit="Over-Ear",
        msrp_usd="", sound_signature="", connector_type="", detachable_cable="", weight_g=""):
    # Append one fully-specified headphone to the global product list P. Every brand
    # block below is just a sequence of add() calls, so this is the single choke point
    # where each row is built and validated before it can enter the dataset.
    # Validate categorical fields — fail loudly, never silently. A bad value (typo in a
    # design/driver/status, etc.) raises here at generation time rather than producing a
    # subtly broken CSV that would only fail later at D1 import or in the front-end.
    assert design   in VALID_DESIGN,   f"{pid}: invalid design={design!r}"
    assert driver   in VALID_DRIVER,   f"{pid}: invalid driver={driver!r}"
    assert status   in VALID_STATUS,   f"{pid}: invalid status={status!r}"
    assert wireless in VALID_WIRELESS, f"{pid}: invalid wireless={wireless!r}"
    assert anc      in VALID_WIRELESS, f"{pid}: invalid anc={anc!r}"
    assert category in VALID_CATEGORY, f"{pid}: invalid category={category!r}"
    assert fit      in VALID_FIT,      f"{pid}: invalid fit={fit!r}"
    assert sound_signature in VALID_SOUND_SIGNATURE, f"{pid}: invalid sound_signature={sound_signature!r}"
    assert connector_type  in VALID_CONNECTOR,       f"{pid}: invalid connector_type={connector_type!r}"
    assert detachable_cable in VALID_DETACHABLE,     f"{pid}: invalid detachable_cable={detachable_cable!r}"
    P.append([pid, mfr, fam, model, full, year, disc, status, category,
              design, driver, driver_size, impedance, sensitivity,
              wireless, anc, pred, succ, notes, date_added, fit,
              msrp_usd, sound_signature, connector_type, detachable_cable, weight_g])

# ---- Sony ----
add("SONY_MDR1R","Sony","MDR","MDR-1R","Sony MDR-1R",2012,"Discontinued","Closed Back","Dynamic","No","No",succ="SONY_MDR1A",notes="Premium closed-back")
add("SONY_MDR1A","Sony","MDR","MDR-1A","Sony MDR-1A",2014,"Discontinued","Closed Back","Dynamic","No","No",pred="SONY_MDR1R")
add("SONY_MDRZ5","Sony","MDR","MDR-Z5","Sony MDR-Z5",2014,"Discontinued","Closed Back","Dynamic","No","No",notes="70mm driver; 70Ω; premium portable closed-back; predecessor to MDR-Z7 concept",succ="SONY_MDRZ7")
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
add("BEYER_T5P","Beyerdynamic","T","T 5p","Beyerdynamic T 5p",2012,"Discontinued","Closed Back","Dynamic","No","No",succ="BEYER_T5PMK2",notes="Portable Tesla closed-back; 32Ω for easy driving; semi-open cups")
add("BEYER_T5PMK2","Beyerdynamic","T","T 5p 2nd Generation","Beyerdynamic T 5p 2nd Generation",2016,"Active","Closed Back","Dynamic","No","No",pred="BEYER_T5P",notes="Updated portable Tesla closed-back; revised pads and cable",fit="Over-Ear")
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
add("AUDEZE_LCD5S","Audeze","LCD","LCD-5S","Audeze LCD-5S",2024,"Active","Open Back","Planar Magnetic","No","No",pred="AUDEZE_LCD5",notes="Studio-tuned LCD-5; different pad set and EQ voicing")
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
add("HIFIMAN_HE560V4","HiFiMan","HE","HE-560 V4","HiFiMan HE-560 V4",2019,"Active","Open Back","Planar Magnetic","No","No",pred="HIFIMAN_HE560",notes="Refined version 4 of the HE-560; asymmetric magnetic circuit; improved channel matching")
add("HIFIMAN_HER10D","HiFiMan","HE","HE-R10D","HiFiMan HE-R10D",2018,"Active","Closed Back","Dynamic","No","No",notes="Dynamic closed-back flagship; 50mm topology driver; tribute to Sony R10; wood cups")
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
add("FOCAL_SPIRITCLASSIC","Focal","Spirit","Spirit Classic","Focal Spirit Classic",2013,"Discontinued","Closed Back","Dynamic","No","No",notes="Audiophile-aimed closed-back; 40mm driver; launched alongside Spirit Professional")
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
add("BEYER_MMX300PRO","Beyerdynamic","MMX","MMX 300 Pro","Beyerdynamic MMX 300 Pro",2024,"Active","Closed Back","Dynamic","No","No",category="Gaming",notes="Pro gaming closed-back; STELLAR.45 driver")
# HiFiMan
add("HIFIMAN_SUSVARAUNV","HiFiMan","HE","Susvara Unveiled","HiFiMan Susvara Unveiled",2023,"Active","Open Back","Planar Magnetic","No","No",notes="Susvara with exposed driver; limited production; premium over standard Susvara",pred="HIFIMAN_SUSVARA")
# Audeze
# Meze
add("MEZE_EMPYREAN3","Meze Audio","Flagship","Empyrean 3","Meze Audio Empyrean 3",2025,"Active","Open Back","Planar Magnetic","No","No",notes="Third-gen isodynamic planar; new Rinaro PCOCC driver")
# Sennheiser
# Focal
add("FOCAL_DIABLO","Focal","Flagship","Celestee Diablo","Focal Celestee Diablo",2024,"Active","Closed Back","Dynamic","No","No",notes="Celestee variant with unique Diablo orange finish; same driver",pred="FOCAL_CELESTEE")
# Sony  

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
    "BEYER_T5P":         {"impedance": "32",  "sensitivity": "101", "driver_size": "45"},
    "BEYER_T5PMK2":      {"impedance": "32",  "sensitivity": "101", "driver_size": "45"},
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
    "HIFIMAN_HE560V4":   {"impedance": "45",  "sensitivity": "90"},
    "HIFIMAN_HER10D":    {"impedance": "32",  "sensitivity": "94", "driver_size": "50"},
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
    "SONY_MDRZ5":      {"impedance": "70",  "sensitivity": "102", "driver_size": "70"},
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
    "FOCAL_SPIRITCLASSIC":{"impedance": "32", "sensitivity": "103", "driver_size": "40"},
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
    "BEYER_DT1990MK2":    {"impedance": "30", "sensitivity": "94",  "driver_size": "45",
                           "msrp_usd": "600", "sound_signature": "Bright", "connector_type": "3.5mm + 6.35mm",
                           "detachable_cable": "Yes", "weight_g": "402"},
    "BEYER_MMX300PRO":    {"impedance": "48", "sensitivity": "100", "driver_size": "45"},
    "HIFIMAN_SUSVARAUNV": {"impedance": "60", "sensitivity": "83"},
    "AUDEZE_LCD5S":       {"impedance": "14", "sensitivity": "90",  "driver_size": "90"},
    "MEZE_EMPYREAN3":     {"impedance": "31.6","sensitivity": "102"},
    "SONY_WH1000XM6":     {"impedance": "16", "sensitivity": "100", "driver_size": "30",
                           "msrp_usd": "450", "sound_signature": "V-Shaped", "connector_type": "Wireless",
                           "detachable_cable": "", "weight_g": "254"},
}

# ---------------------------------------------------------------------------
# MSRP data — approximate USD launch prices from manufacturer pages or press releases.
# ---------------------------------------------------------------------------
MSRP = {
    # Sony
    "SONY_MDR1R":990, "SONY_MDR1A":300, "SONY_MDR1AM2":300,
    "SONY_MDRZ7":700, "SONY_MDRZ7M2":400, "SONY_MDRZ1R":2300,
    "SONY_MDR7506":100, "SONY_MDR7510":200, "SONY_MDR7520":400, "SONY_MDRCD900ST":200,
    "SONY_WH1000XM2":350, "SONY_WH1000XM3":350, "SONY_WH1000XM4":350, "SONY_WH1000XM5":400,
    "SONY_QUALIA010":2000,
    # Sennheiser
    "SENN_HD600":400, "SENN_HD650":500, "SENN_HD660S":500, "SENN_HD660S2":600,
    "SENN_HD800":1500, "SENN_HD800S":1700, "SENN_HD820":2400, "SENN_HE1":55000,
    "SENN_HD490PRO":400, "SENN_HD620S":450,
    "SENN_HD25":170, "SENN_HD280PRO":100, "SENN_HD380PRO":170,
    "SENN_MOMENTUM4":350, "SENN_MOMENTUM5":400,
    "SENN_PXC550":350, "SENN_PXC550II":350,
    # Audio-Technica
    "ATECH_M50X":150, "ATECH_M70X":200, "ATECH_M40X":100, "ATECH_M20X":50,
    "ATECH_R70X":350, "ATECH_ADX5000":1000,
    "ATECH_ATH3000ANV":2000,
    # AKG
    "AKG_K701":200, "AKG_K702":200, "AKG_K712":350,
    "AKG_K240":70, "AKG_K271MK2":170, "AKG_K872":1500, "AKG_K812":1500,
    "AKG_K361":100, "AKG_K371":150, "AKG_N700NC":300, "AKG_N700NCM2":300,
    # Beyerdynamic
    "BEYER_DT770PRO":170, "BEYER_DT880PRO":180, "BEYER_DT990PRO":180,
    "BEYER_DT1770PRO":600, "BEYER_DT1990":550, "BEYER_DT1990MK2":800,
    "BEYER_T5P":600, "BEYER_T5PMK2":900,
    "SONY_MDRZ5":500, "FOCAL_SPIRITCLASSIC":350,
    "HIFIMAN_HE560V4":900, "HIFIMAN_HER10D":6000,
    "BEYER_AMIRON":600, "BEYER_DT700PROX":300, "BEYER_DT900PROX":350,
    "BEYER_MMX300":300, "BEYER_MMX300PRO":300,
    # Bose
    "BOSE_QC35II":350, "BOSE_QC45":330, "BOSE_QC35":300,
    "BOSE_NCH700":380, "BOSE_QCU":430, "BOSE_A20":1095, "BOSE_A30":1350,
    # Audeze
    "AUDEZE_LCD2":1200, "AUDEZE_LCD2C":900, "AUDEZE_LCD3":2000,
    "AUDEZE_LCD4":4000, "AUDEZE_LCD5":4500, "AUDEZE_LCD5S":4500,
    "AUDEZE_LCDX":1200, "AUDEZE_LCDXC":1300,
    "AUDEZE_MM100":400, "AUDEZE_MM200":500, "AUDEZE_MM500":1500,
    "AUDEZE_MAXWELL":300, "AUDEZE_PENROSE":300,
    "AUDEZE_CRBN":4500, "AUDEZE_CRBN2":4500,
    # HiFiMan
    "HIFIMAN_HE400SE":110, "HIFIMAN_HE400I":200, "HIFIMAN_HE400I2020":150, "HIFIMAN_HE4XX":170,
    "HIFIMAN_HE560":900, "HIFIMAN_HE5XX":220, "HIFIMAN_HE6SE":1800,
    "HIFIMAN_ANANDA":700, "HIFIMAN_ARYA":1300, "HIFIMAN_ARYASTLTH":1400,
    "HIFIMAN_SUNDARA":350, "HIFIMAN_EDITION_XS":500,
    "HIFIMAN_SUSVARA":6000, "HIFIMAN_HE1000V2":3000, "HIFIMAN_HE1000SE":4000,
    "HIFIMAN_JADE2":2500, "HIFIMAN_SHANGRILA":8000,
    # Focal
    "FOCAL_UTOPIA":4000, "FOCAL_UTOPIA2022":5000, "FOCAL_CLEAR":1500, "FOCAL_CLEARMG":1500,
    "FOCAL_ELEAR":1000, "FOCAL_ELEGIA":900, "FOCAL_STELLIA":3000, "FOCAL_CELESTEE":1000,
    "FOCAL_BATHYS":800, "FOCAL_HADENYS":1600, "FOCAL_AZURYS":500,
    "FOCAL_LISTEN":280, "FOCAL_LISTENPRO":350,
    # Grado
    "GRADO_SR60X":100, "GRADO_SR80X":125, "GRADO_SR125X":175,
    "GRADO_SR225X":250, "GRADO_SR325X":350, "GRADO_RS1X":700, "GRADO_RS2X":500,
    "GRADO_GS1000X":1100, "GRADO_GS3000X":1700, "GRADO_GW100X":300, "GRADO_HEMP":420,
    # Dan Clark Audio
    "DCA_STEALTH":4000, "DCA_EXPANSE":4000, "DCA_ETHER2":1500,
    "DCA_AEON2N":900, "DCA_AEON2C":900, "DCA_AEON2NOIRE":800,
    # Meze Audio
    "MEZE_99CLASSICS":310, "MEZE_ELITE":4000, "MEZE_EMPYREAN":3000,
    "MEZE_EMPYREAN2":4000, "MEZE_EMPYREAN3":4500, "MEZE_109PRO":800,
    "MEZE_LIRIC":2000, "MEZE_LIRICII":2000,
    # ZMF Headphones
    "ZMF_VERITE_O":2500, "ZMF_VERITE_C":2500,
    "ZMF_ATRIUM_O":3000, "ZMF_ATRIUM_C":3000,
    "ZMF_CALDERA":2500, "ZMF_AUTEUR":1500, "ZMF_AEOLUS":1300,
    # Stax
    "STAX_SR009":4400, "STAX_SR009S":4400, "STAX_SR007":2300,
    "STAX_SRL700MK2":1300, "STAX_X9000":4500,
    # Beats
    "BEATS_STUDIO3":350, "BEATS_STUDIOPRO":350, "BEATS_STUDIO4":350,
    "BEATS_SOLO3":200, "BEATS_SOLO4":200, "BEATS_SOLOPRO":300,
    # Apple / B&O / Marshall
    "APPLE_AIRPODSMAX":550, "APPLE_AIRPODSMAXUSBC":550,
    "BO_H95":500, "BO_HX":490, "BO_H100":850,
    "MARSHALL_MAJOR5":100, "MARSHALL_MONITOR3ANC":200,
    # JBL / Koss / Shure
    "JBL_CLUBONE":300, "JBL_LIVE660NC":200, "JBL_LIVE770NC":250,
    "KOSS_PORTAPRO":50, "KOSS_ESP95X":500,
    "SHURE_SRH1540":500, "SHURE_SRH1840":500,
    # Neumann / Austrian Audio / Final / Warwick / Abyss
    "NEUMANN_NDH20":500, "NEUMANN_NDH30":500,
    "AUSTRIAN_HIX55":350, "AUSTRIAN_HIX65":400,
    "FINAL_D8000":4000, "FINAL_D8000PRO":4500,
    "WA_SONOMA":5000, "WA_APERIO":8000,
    "ABYSS_AB1266":5000, "ABYSS_DIANATC":4000,
    # FiiO / Technics / Sonos / Mark Levinson / RAAL / Rosson
    "FIIO_FT3":220, "FIIO_FT5":350,
    "TECH_EAHA800":380, "TECH_EAHA800M2":380,
    "SONOS_ACE":450,
    "MARKLEV_5909":1000,
    "RAAL_SR1A":3500,
    "ROSSON_RAD0":2600,
    # Gaming
    "ASTRO_A50G4":330, "ASTRO_A50X":380, "ASTRO_A40TR":150,
    "RAZER_BARRACUDAX":100, "RAZER_OPUS2020":200,
    "LOGI_G735":180, "LOGI_G435":100, "LOGI_G533":150,
    "SK_CRUSHER_EVO":200, "SK_CRUSHER_ANC":300,
}

# ---------------------------------------------------------------------------
# VERIFIED_SPECS — product IDs whose impedance + sensitivity come directly
# from manufacturer published spec sheets. All others default to 'Estimated'.
# ---------------------------------------------------------------------------
VERIFIED_SPECS = {
    # Sennheiser (sennheiser.com spec sheets)
    "SENN_HD600","SENN_HD650","SENN_HD660S","SENN_HD660S2",
    "SENN_HD800","SENN_HD800S","SENN_HD820","SENN_HE1",
    "SENN_HD490PRO","SENN_HD620S","SENN_HD25","SENN_HD25_1",
    "SENN_HD280PRO","SENN_HD380PRO","SENN_AMPERIOR",
    "SENN_MOMENTUM3","SENN_MOMENTUM4","SENN_MOMENTUM5",
    "SENN_PXC550","SENN_PXC550II",
    # Beyerdynamic (beyerdynamic.com)
    "BEYER_DT770PRO","BEYER_DT880PRO","BEYER_DT990PRO",
    "BEYER_DT1770PRO","BEYER_DT1990","BEYER_DT1990MK2",
    "BEYER_T1MK1","BEYER_T1MK2","BEYER_T1MK3",
    "BEYER_AMIRON","BEYER_DT700PROX","BEYER_DT900PROX",
    "BEYER_MMX300","BEYER_MMX300PRO",
    # AKG (akg.com)
    "AKG_K701","AKG_K702","AKG_K712","AKG_K240",
    "AKG_K271MK2","AKG_K812","AKG_K872","AKG_K361","AKG_K371",
    # Audio-Technica (audio-technica.com)
    "ATECH_M50X","ATECH_M70X","ATECH_M40X","ATECH_M20X",
    "ATECH_R70X","ATECH_ADX5000","ATECH_ATH3000ANV",
    # Focal (focal.com)
    "FOCAL_UTOPIA","FOCAL_UTOPIA2022","FOCAL_CLEAR","FOCAL_CLEARMG",
    "FOCAL_ELEAR","FOCAL_ELEGIA","FOCAL_STELLIA","FOCAL_CELESTEE",
    "FOCAL_BATHYS","FOCAL_HADENYS","FOCAL_AZURYS",
    # Audeze (audeze.com)
    "AUDEZE_LCD2","AUDEZE_LCD2C","AUDEZE_LCD3","AUDEZE_LCD4","AUDEZE_LCD5",
    "AUDEZE_LCDX","AUDEZE_LCDXC","AUDEZE_MM100","AUDEZE_MM500",
    # HiFiMan (hifiman.com)
    "HIFIMAN_HE400SE","HIFIMAN_ANANDA","HIFIMAN_ARYA","HIFIMAN_SUNDARA",
    "HIFIMAN_EDITION_XS","HIFIMAN_SUSVARA","HIFIMAN_HE1000V2","HIFIMAN_HE1000SE",
    # Dan Clark Audio
    "DCA_STEALTH","DCA_EXPANSE","DCA_ETHER2","DCA_AEON2N","DCA_AEON2C",
    # ZMF Headphones (zmfheadphones.com)
    "ZMF_VERITE_O","ZMF_VERITE_C","ZMF_ATRIUM_O","ZMF_ATRIUM_C",
    "ZMF_CALDERA","ZMF_AUTEUR","ZMF_AEOLUS",
    # Stax (stax.co.jp)
    "STAX_SR009","STAX_SR009S","STAX_SR007","STAX_SRL700MK2","STAX_X9000",
    # Grado (gradolabs.com)
    "GRADO_SR60X","GRADO_SR80X","GRADO_SR125X","GRADO_SR225X","GRADO_SR325X",
    "GRADO_RS1X","GRADO_RS2X","GRADO_GS1000X","GRADO_GS3000X","GRADO_GW100X",
    # Meze Audio (mezeaudio.com)
    "MEZE_99CLASSICS","MEZE_ELITE","MEZE_EMPYREAN","MEZE_EMPYREAN2","MEZE_109PRO",
    "MEZE_LIRIC","MEZE_LIRICII",
    # Sony (sony.com)
    "SONY_MDR7506","SONY_MDRCD900ST","SONY_MDRZ1R","SONY_MDR1AM2","SONY_MDRZ7M2",
    # Neumann (neumann.com)
    "NEUMANN_NDH20","NEUMANN_NDH30",
    # Austrian Audio (austrian.audio)
    "AUSTRIAN_HIX55","AUSTRIAN_HIX65","AUSTRIAN_HIX60",
    # Shure (shure.com)
    "SHURE_SRH1540","SHURE_SRH1840","SHURE_SRH440A","SHURE_SRH840A",
    # Koss (koss.com)
    "KOSS_PORTAPRO","KOSS_KPH30I","KOSS_ESP95X",
    # Final Audio
    "FINAL_D8000","FINAL_D8000PRO",
    # Fostex (fostex.jp)
    "FOSTEX_T50RPMK3","FOSTEX_T50RPMK4","FOSTEX_TH900MK2","FOSTEX_TH610",
    # Ollo Audio (ships measured data with every unit)
    "OLLO_S4X","OLLO_S5X","OLLO_X1",
}

# ---------------------------------------------------------------------------
# MSRP expansion — fills gaps from the initial batch
# ---------------------------------------------------------------------------
MSRP.update({
    # Sennheiser
    "SENN_HD201":130, "SENN_HD202":50, "SENN_HD218":60, "SENN_HD219":50,
    "SENN_HD228":70, "SENN_HD229":70, "SENN_HD238":80, "SENN_HD239":80,
    "SENN_HD418":60, "SENN_HD419":60, "SENN_HD428":80, "SENN_HD429":80,
    "SENN_HD438":100, "SENN_HD439":100, "SENN_HD449":100, "SENN_HD471":100,
    "SENN_HD515":100, "SENN_HD518":150, "SENN_HD555":150, "SENN_HD558":180,
    "SENN_HD569":200, "SENN_HD579":200, "SENN_HD599":250, "SENN_HD560S":200,
    "SENN_HD4_40BT":150, "SENN_HD4_50BTNC":200,
    "SENN_HD350BT":100, "SENN_HD450BT":150, "SENN_HD250BT":200,
    "SENN_MOMENTUM":280, "SENN_MOMENTUM2":350, "SENN_MOMENTUM3":350,
    "SENN_ACCENTUM":230, "SENN_ACCENTUMPLUS":280,
    "SENN_AMPERIOR":300, "SENN_PX100":60, "SENN_PX200":90,
    "SENN_HDB630":450,
    # Audio-Technica
    "ATECH_M30X":70, "ATECH_M50XBT":180, "ATECH_M50XBT2":200,
    "ATECH_M60X":150, "ATECH_A700Z":150, "ATECH_A500Z":100, "ATECH_A900Z":250,
    "ATECH_ANC300":200, "ATECH_ANC900BT":200, "ATECH_ANC70":150, "ATECH_ANC50":80,
    "ATECH_SR50BT":100, "ATECH_SR30BT":70,
    "ATECH_WP900":400, "ATECH_DSR7BT":250, "ATECH_DSR9BT":350,
    "ATECH_ES55":100, "ATECH_EW9":200,
    # Sony
    "SONY_MDR1R":400, "SONY_MDR1A":300, "SONY_MDRZ5":500, "SONY_MDRZ7":700,
    "SONY_MDR7510":200, "SONY_MDR7520":400,
    "SONY_WHCH700N":200, "SONY_WHCH710N":200, "SONY_WHCH720N":200,
    "SONY_WHHH1":300, "SONY_WHH900N":300,
    "SONY_MDRXB700":120, "SONY_MDRXB950N1":200, "SONY_MDRXB1000":200,
    "SONY_CH500":60, "SONY_CH510":60, "SONY_CH520":60,
    "SONY_ZX110":30, "SONY_ZX310":50, "SONY_XB650":80,
    # Beyerdynamic
    "BEYER_DT240PRO":100, "BEYER_DT231":80, "BEYER_DT235":80,
    "BEYER_T50P":300, "BEYER_T5P":600, "BEYER_T5PMK2":900,
    "BEYER_AVENTHOW":450, "BEYER_MMX300PRO":300,
    "BEYER_DT1350":350,
    # AKG
    "AKG_K44":50, "AKG_K52":50, "AKG_K72":60, "AKG_K92":70,
    "AKG_K141MK2":100, "AKG_K240MK2":150, "AKG_K271MK2":170,
    "AKG_K450":150, "AKG_K490NC":250, "AKG_K550":200, "AKG_K553":180,
    "AKG_Y50BT":150, "AKG_N60NC":200, "AKG_N700NC":300, "AKG_N700NCM2":300,
    "AKG_K67":130, "AKG_K175":150,
    # HiFiMan
    "HIFIMAN_HE300":200, "HIFIMAN_HE5LE":600, "HIFIMAN_HE500":700,
    "HIFIMAN_HE560":900, "HIFIMAN_HE560V4":900,
    "HIFIMAN_HE400I":250, "HIFIMAN_HE400I2020":150,
    "HIFIMAN_HEX4":200, "HIFIMAN_HER10D":6000,
    "HIFIMAN_DEVA":300, "HIFIMAN_DEVA_PRO":350,
    # JBL
    "JBL_E45BT":100, "JBL_LIVE400":100, "JBL_LIVE460":130,
    "JBL_LIVE650BTNC":200, "JBL_LIVE660NC":200, "JBL_LIVE770NC":250,
    "JBL_TUNE760NC":80, "JBL_TUNE710BT":100, "JBL_TUNE770NC":100,
    "JBL_E65BTNC":150, "JBL_DUETNC":100, "JBL_CLUB700":120,
    "JBL_CLUB950":200,
    # Grado
    "GRADO_SR60E":80, "GRADO_SR80E":100, "GRADO_SR125E":150, "GRADO_SR225E":200,
    "GRADO_SR325E":295, "GRADO_GH1":125, "GRADO_GH2":175, "GRADO_GH3":250,
    "GRADO_GH4":300, "GRADO_HEMP":420, "GRADO_GW100X":300,
    "GRADO_RS1":600, "GRADO_RS2E":500, "GRADO_PS1000E":1700,
    "GRADO_GS1000":1000,
    # Fostex
    "FOSTEX_TH600":600, "FOSTEX_TH900":1500, "FOSTEX_TH610":400,
    "FOSTEX_TH7":250, "FOSTEX_T50RPMK2":200, "FOSTEX_T50RPMK3":200,
    "FOSTEX_T50RPMK4":300, "FOSTEX_TR80":150, "FOSTEX_TXO":400,
    # Bowers & Wilkins
    "BW_P3":200, "BW_P5":300, "BW_P5S2":350, "BW_P7":400,
    "BW_P9":900, "BW_PX":380, "BW_PX5":280, "BW_PX7":380,
    "BW_PX7S2":380, "BW_PX7S3":380, "BW_PX8":700,
    # Razer
    "RAZER_KRAKEN2019":80, "RAZER_KRAKENX":50, "RAZER_KRAKENULTI":130,
    "RAZER_NARIU":200, "RAZER_BSHARKV2":100, "RAZER_BARRACUDAX":100,
    "RAZER_OPUS2020":200,
    # Dan Clark Audio
    "DCA_MADDOG":300, "DCA_AEON2NOIRE":800, "DCA_NOIRECLOSED":800,
    "DCA_VOCE":3500,
    # ZMF
    "ZMF_AEOLUS":1300, "ZMF_ATTICUS":1200, "ZMF_EIKON":1500,
    "ZMF_ORI":600, "ZMF_VIBRO":400,
    # Stax
    "STAX_SR207":300, "STAX_SR507":600, "STAX_SRL300":450,
    "STAX_SRL500":600, "STAX_SRL700":900, "STAX_SR404":500, "STAX_SR4070":700,
    # Shure
    "SHURE_SRH440":100, "SHURE_SRH750DJ":200, "SHURE_SRH940":300,
    "SHURE_SRH1440":250,
    # Meze
    "MEZE_99NOIR":350, "MEZE_99CLASSICS_WALNUT":310,
    # Bang & Olufsen
    "BO_H4":300, "BO_H6":400, "BO_H9":500,
    # Marshall
    "MARSHALL_MAJOR2":100, "MARSHALL_MAJOR3":100, "MARSHALL_MAJOR4":100,
    "MARSHALL_MIDANC":200, "MARSHALL_MONITOR":250, "MARSHALL_MONITOR2ANC":350,
    # Koss
    "KOSS_KPH40":40, "KOSS_KSC75":20, "KOSS_KPH7":35, "KOSS_PRO4AA":100,
    "KOSS_PORTAPROWL":85,
    # SteelSeries
    "SS_ARCTIS1":50, "SS_ARCTIS3":70, "SS_ARCTIS5":100, "SS_ARCTIS7":150,
    "SS_ARCTIS7P":170, "SS_ARCTISNOVA":100, "SS_ARCTISNOVA5":130,
    "SS_ARCTISNOVA7":200, "SS_ARCTIS9":200, "SS_ARCTIS_NOVA_PRO":250,
    # HyperX
    "HX_CLOUD2":100, "HX_CLOUDCORE":80, "HX_CLOUDALPHA":100, "HX_CLOUDS":80,
    "HX_CLOUDFLIGHTS":170, "HX_CLOUDFLIGHT3":120, "HX_CLOUDII_WL":150,
    "HX_STINGER2":60,
    # Denon
    "DENON_D600":300, "DENON_D1100":200, "DENON_D2000":350,
    "DENON_D5000":600, "DENON_D7000":1000, "DENON_D7100":600,
    "DENON_D9200":1000, "DENON_AH_GC30":200,
    # Yamaha
    "YAMAHA_HPHMT7":230, "YAMAHA_HPHMT8":300, "YAMAHA_HP1":1000,
    "YAMAHA_YHL700A":300, "YAMAHA_YHE700A":300, "YAMAHA_YHS5000SE":5000,
    # Ultrasone
    "ULTRA_ED8":1500, "ULTRA_ED10":2000, "ULTRA_ED15":2500,
    "ULTRA_HFI780":200, "ULTRA_HFI2400":300, "ULTRA_SIGPURE":700,
    "ULTRA_HFI580":130, "ULTRA_HFI450":100, "ULTRA_PERF880":350,
    # Logitech G
    "LOGI_G432":70, "LOGI_G433":100, "LOGI_G435":80, "LOGI_G533":150,
    "LOGI_G633":150, "LOGI_G635":150, "LOGI_G733":130, "LOGI_G735":180,
    "LOGI_G930":100,
    # V-Moda
    "VMODA_LP":100, "VMODA_LP2":150, "VMODA_M80":180, "VMODA_M100":310,
    "VMODA_CROSSFADE2WL":350, "VMODA_M100MASTER":350,
    # Skullcandy
    "SK_HESH3":70, "SK_CRUSHBASE":100, "SK_CRUSHER_EVO":200, "SK_CRUSHER_ANC":300,
    "SK_HESH_ANC":100, "SK_VENUE_ANC":100,
    # Anker Soundcore
    "ANKER_LIFEQ20":40, "ANKER_LIFEQ30":60, "ANKER_SPACEQ45":80,
    "ANKER_SPACEONE":80, "ANKER_SPACEONEPRO":100,
    # Moondrop
    "MOONDROP_VENUS":200, "MOONDROP_PARA":300, "MOONDROP_COSMO":100,
    "MOONDROP_HORIZON":80, "MOONDROP_EDGE":150,
    # Sendy Audio
    "SENDY_AIVA":250, "SENDY_PEACOCK":400, "SENDY_APOLLO":350,
    # Kiwi Ears
    "KIWIEARS_ARDOR":250, "KIWIEARS_ELLIPSE":280, "KIWIEARS_ATHEIA":300,
    # T+A
    "TA_SOLITAIRE_P":2700, "TA_SOLITAIRE_PSE":3000, "TA_SOLITAIRE_T":2000,
    # HEDD Audio
    "HEDD_HEDDPHONE":1900, "HEDD_HEDDPHONE2":1500,
    # Ollo Audio
    "OLLO_S4X":399, "OLLO_S5X":399, "OLLO_X1":299,
    # FiiO
    "FIIO_FT1":80, "FIIO_FT1PRO":130, "FIIO_FT3":220, "FIIO_FT5":350,
    # Austrian Audio
    "AUSTRIAN_HIX60":350, "AUSTRIAN_THECOMPOSER":1500,
    # Warwick Acoustics
    "WA_SONOMA":5000, "WA_APERIO":8000,
    # Abyss
    "ABYSS_DIANAV2":3000, "ABYSS_DIANA":2500, "ABYSS_DIANAMR":4000,
    # Final Audio
    "FINAL_SONOROUS3":600, "FINAL_SONOROUS6":900, "FINAL_SONOROUSX":3000,
    # Status Audio
    "STATUS_CB1":80, "STATUS_OB1":130,
    # Harman Kardon
    "HK_SOHO":200, "HK_SOHOWL":250, "HK_SOHOWNC":300,
    # Turtle Beach
    "TB_STEALTH600G2":100, "TB_STEALTH700G2":150, "TB_STEALTHPRO":250,
    # Corsair
    "CORSAIR_HS80":100, "CORSAIR_HS70":80, "CORSAIR_VOID":100,
    # Astro
    "ASTRO_A40":130,
    # Cleer
    "CLEER_FLOW2":100, "CLEER_ENDURO100":80, "CLEER_ALPHA":150,
    # 1More
    "1MORE_SONOFLOW":80, "1MORE_SONOFLOWSE":100, "1MORE_MK802":70,
    # Edifier STAX Spirit
    "EDIFIER_STAXGT1":100, "EDIFIER_STAXGT5":130,
    # Goldplanar
    "GOLD_GL2000DS":250, "GOLD_GL2000SS":220, "GOLD_GL850":350,
    # Takstar
    "TAKSTAR_PRO80":60, "TAKSTAR_PRO82":80, "TAKSTAR_HF580":100,
    "TAKSTAR_HF660S":130,
    # Superlux
    "SUPERLUX_HD668B":40, "SUPERLUX_HD681":35, "SUPERLUX_HD669":55,
    # JVC
    "JVC_HADX1000":400, "JVC_HADX2000":600,
    "JVC_HASW01":500, "JVC_HASW02":700,
    # Plantronics
    "PLANT_BB500":60, "PLANT_BB600":80, "PLANT_BB810":150,
    # Phiaton
    "PHIATON_MS530":300, "PHIATON_BT460":130,
    # Oppo
    "OPPO_PM1":1100, "OPPO_PM2":700, "OPPO_PM3":400,
    # ASUS ROG
    "ASUS_DELTAS":100, "ASUS_DELTA2":150,
    # Sonos
    "SONOS_ACE":449,
    # Technics
    "TECH_EAHA800":380,
    # Teufel
    "TEUFEL_REALBLUENC":120, "TEUFEL_ZOLA":150,
    # Creative
    "CREATIVE_AVLIVE":60, "CREATIVE_AVLIVE2":80,
    # Modhouse
    "MODHOUSE_ARGONMK3":400, "MODHOUSE_TUNGSTEN":600,
    # Rosson
    "ROSSON_RAD0":2600,
    # PSB
    "PSB_M4U1":300, "PSB_M4U2":400,
    # Rode
    "RODE_NTH100":150,
    # Crosszone
    "CZ_CZ1":1500, "CZ_CZ10":2000,
    # MySphere
    "MYSPHERE_3":3500, "MYSPHERE_3X":4000,
    # Tago Studio
    "TAGO_T301":1000, "TAGO_T302":1200,
    # Kennerton
    "KENNERTON_ODIN":2000, "KENNERTON_THROR":2500,
    # Spirit Torino
    "SPIRITTORINO_SUPER":900, "SPIRITTORINO_RADIANTE":1200,
    # Neumann
    "NEUMANN_NDH30":600,
})

# ---------------------------------------------------------------------------
# CONNECTOR TYPE + DETACHABLE CABLE
# connector_type: what the headphone's cable terminates at the headphone end
# detachable_cable: "Yes" / "No"
# ---------------------------------------------------------------------------
CONNECTORS = {
    # Audeze — dual mini-XLR on all LCD series
    "AUDEZE_LCD2":"Dual mini-XLR", "AUDEZE_LCD2C":"Dual mini-XLR",
    "AUDEZE_LCD3":"Dual mini-XLR", "AUDEZE_LCD4":"Dual mini-XLR",
    "AUDEZE_LCD5":"Dual mini-XLR", "AUDEZE_LCD5S":"Dual mini-XLR",
    "AUDEZE_LCDX":"Dual mini-XLR", "AUDEZE_LCDXC":"Dual mini-XLR",
    "AUDEZE_MM100":"3.5mm", "AUDEZE_MM200":"3.5mm", "AUDEZE_MM500":"3.5mm",
    "AUDEZE_CRBN":"Electrostatic", "AUDEZE_CRBN2":"Electrostatic",
    # HiFiMan — dual 3.5mm on most planars
    "HIFIMAN_SUSVARA":"Dual 3.5mm", "HIFIMAN_HE1000V2":"Dual 3.5mm",
    "HIFIMAN_HE1000SE":"Dual 3.5mm", "HIFIMAN_ARYA":"Dual 3.5mm",
    "HIFIMAN_ARYASTLTH":"Dual 3.5mm", "HIFIMAN_ANANDA":"Dual 3.5mm",
    "HIFIMAN_SUNDARA":"Dual 3.5mm", "HIFIMAN_EDITION_XS":"Dual 3.5mm",
    "HIFIMAN_HE560":"Dual 3.5mm", "HIFIMAN_HE560V4":"Dual 3.5mm",
    "HIFIMAN_HE6SE":"Dual 3.5mm", "HIFIMAN_HE400SE":"Dual 3.5mm",
    "HIFIMAN_DEVA":"Dual 3.5mm", "HIFIMAN_DEVA_PRO":"Dual 3.5mm",
    "HIFIMAN_HEX4":"Dual 3.5mm", "HIFIMAN_HE5XX":"Dual 3.5mm",
    "HIFIMAN_HE4XX":"Dual 3.5mm",
    # Focal — 3.5mm locking (unique Focal connector)
    "FOCAL_UTOPIA":"3.5mm", "FOCAL_UTOPIA2022":"3.5mm",
    "FOCAL_CLEAR":"3.5mm", "FOCAL_CLEARMG":"3.5mm",
    "FOCAL_ELEAR":"3.5mm", "FOCAL_ELEGIA":"3.5mm",
    "FOCAL_STELLIA":"3.5mm", "FOCAL_CELESTEE":"3.5mm",
    "FOCAL_BATHYS":"3.5mm",
    # Beyerdynamic — mini-XLR on high-end, non-detachable on DT consumer
    "BEYER_DT1770PRO":"mini-XLR", "BEYER_DT1990":"mini-XLR",
    "BEYER_DT1990MK2":"mini-XLR", "BEYER_T1MK2":"mini-XLR",
    "BEYER_T1MK3":"mini-XLR", "BEYER_DT700PROX":"mini-XLR",
    "BEYER_DT900PROX":"mini-XLR", "BEYER_T5P":"3.5mm", "BEYER_T5PMK2":"3.5mm",
    "BEYER_DT770PRO":"3.5mm/6.35mm", "BEYER_DT880PRO":"3.5mm/6.35mm",
    "BEYER_DT990PRO":"3.5mm/6.35mm",
    # AKG — mini-XLR on K series pro
    "AKG_K701":"mini-XLR", "AKG_K702":"mini-XLR", "AKG_K712":"mini-XLR",
    "AKG_K812":"3.5mm", "AKG_K872":"3.5mm",
    "AKG_K240":"mini-XLR", "AKG_K271MK2":"mini-XLR",
    "AKG_K550":"3.5mm", "AKG_K553":"3.5mm",
    # Sennheiser — proprietary 2-pin on HD 600 series; non-detach on consumer
    "SENN_HD600":"Sennheiser 2-pin", "SENN_HD650":"Sennheiser 2-pin",
    "SENN_HD660S":"Sennheiser 2-pin", "SENN_HD660S2":"Sennheiser 2-pin",
    "SENN_HD800":"Sennheiser twist-lock", "SENN_HD800S":"Sennheiser twist-lock",
    "SENN_HD820":"Sennheiser twist-lock", "SENN_HD490PRO":"Sennheiser 2-pin",
    "SENN_HD620S":"Sennheiser 2-pin", "SENN_HD560S":"3.5mm",
    "SENN_HD25":"3.5mm", "SENN_HD25_1":"3.5mm",
    # Audio-Technica — A-series detachable, M-series mostly non
    "ATECH_R70X":"A2DC", "ATECH_ADX5000":"A2DC",
    "ATECH_A2000Z":"A2DC", "ATECH_A1000Z":"A2DC",
    "ATECH_M50XBT":"Wireless", "ATECH_M50XBT2":"Wireless",
    # ZMF — dual 3.5mm
    "ZMF_VERITE_O":"Dual 3.5mm", "ZMF_VERITE_C":"Dual 3.5mm",
    "ZMF_ATRIUM_O":"Dual 3.5mm", "ZMF_ATRIUM_C":"Dual 3.5mm",
    "ZMF_CALDERA":"Dual 3.5mm", "ZMF_AUTEUR":"Dual 3.5mm",
    "ZMF_AEOLUS":"Dual 3.5mm",
    # Dan Clark Audio — mini-XLR
    "DCA_STEALTH":"mini-XLR", "DCA_EXPANSE":"mini-XLR",
    "DCA_ETHER2":"mini-XLR", "DCA_AEON2N":"mini-XLR", "DCA_AEON2C":"mini-XLR",
    "DCA_AEON2NOIRE":"mini-XLR", "DCA_NOIRECLOSED":"mini-XLR",
    # Meze
    "MEZE_ELITE":"mini-XLR", "MEZE_EMPYREAN":"mini-XLR",
    "MEZE_EMPYREAN2":"mini-XLR", "MEZE_EMPYREAN3":"mini-XLR",
    "MEZE_109PRO":"3.5mm", "MEZE_LIRIC":"3.5mm", "MEZE_LIRICII":"3.5mm",
    "MEZE_99CLASSICS":"3.5mm",
    # Wireless headphones
    "SONY_WH1000XM4":"Wireless", "SONY_WH1000XM5":"Wireless",
    "SONY_WH1000XM6":"Wireless",
    "BOSE_QC35II":"Wireless", "BOSE_QC45":"Wireless", "BOSE_NCH700":"Wireless",
    "BOSE_QCU":"Wireless",
    "APPLE_AIRPODSMAX":"Lightning", "APPLE_AIRPODSMAXUSBC":"USB-C",
    # Shure
    "SHURE_SRH1540":"MMCX", "SHURE_SRH1840":"3.5mm",
    "SHURE_SRH440A":"3.5mm", "SHURE_SRH840A":"3.5mm",
    # Sony wired flagships
    "SONY_MDRZ1R":"4.4mm Pentaconn", "SONY_MDRZ7M2":"4.4mm Pentaconn",
    "SONY_MDR7506":"3.5mm/6.35mm",
    # Final Audio
    "FINAL_D8000":"4.4mm Pentaconn", "FINAL_D8000PRO":"4.4mm Pentaconn",
    # Stax
    "STAX_SR009":"Electrostatic", "STAX_SR009S":"Electrostatic",
    "STAX_SR007":"Electrostatic", "STAX_SRL700MK2":"Electrostatic",
    "STAX_X9000":"Electrostatic",
    # Grado — non-detachable on SR series, some RS/PS/GS are detachable
    "GRADO_SR60X":"3.5mm", "GRADO_SR80X":"3.5mm",
    "GRADO_SR125X":"3.5mm", "GRADO_SR225X":"3.5mm", "GRADO_SR325X":"3.5mm",
    "GRADO_RS1X":"3.5mm", "GRADO_RS2X":"3.5mm",
    "GRADO_GS1000X":"3.5mm", "GRADO_GS3000X":"3.5mm",
    # Fostex
    "FOSTEX_TH900MK2":"Dual 3.5mm", "FOSTEX_TH610":"Dual 3.5mm",
    "FOSTEX_TH600":"Dual 3.5mm", "FOSTEX_T50RPMK3":"3.5mm",
    "FOSTEX_T50RPMK4":"3.5mm",
    # Denon biodynamic
    "DENON_D9200":"Dual 3.5mm", "DENON_D7200":"Dual 3.5mm",
    # Neumann / Austrian Audio
    "NEUMANN_NDH20":"mini-XLR", "NEUMANN_NDH30":"mini-XLR",
    "AUSTRIAN_HIX55":"3.5mm", "AUSTRIAN_HIX65":"3.5mm",
}

# Detachable cable data
DETACHABLE = {
    # Yes — these all have user-replaceable cables
    **{pid: "Yes" for pid in [
        "AUDEZE_LCD2","AUDEZE_LCD2C","AUDEZE_LCD3","AUDEZE_LCD4","AUDEZE_LCD5",
        "AUDEZE_LCD5S","AUDEZE_LCDX","AUDEZE_LCDXC","AUDEZE_MM100","AUDEZE_MM200","AUDEZE_MM500",
        "HIFIMAN_SUSVARA","HIFIMAN_HE1000V2","HIFIMAN_HE1000SE","HIFIMAN_ARYA",
        "HIFIMAN_ARYASTLTH","HIFIMAN_ANANDA","HIFIMAN_SUNDARA","HIFIMAN_EDITION_XS",
        "HIFIMAN_HE560","HIFIMAN_HE560V4","HIFIMAN_HE6SE","HIFIMAN_HE400SE",
        "HIFIMAN_DEVA","HIFIMAN_DEVA_PRO","HIFIMAN_HEX4","HIFIMAN_HE5XX","HIFIMAN_HE4XX",
        "FOCAL_UTOPIA","FOCAL_UTOPIA2022","FOCAL_CLEAR","FOCAL_CLEARMG",
        "FOCAL_ELEAR","FOCAL_ELEGIA","FOCAL_STELLIA","FOCAL_CELESTEE","FOCAL_BATHYS",
        "BEYER_DT1770PRO","BEYER_DT1990","BEYER_DT1990MK2","BEYER_T1MK2","BEYER_T1MK3",
        "BEYER_DT700PROX","BEYER_DT900PROX","BEYER_T5P","BEYER_T5PMK2",
        "AKG_K701","AKG_K702","AKG_K712","AKG_K812","AKG_K872","AKG_K240","AKG_K271MK2",
        "SENN_HD600","SENN_HD650","SENN_HD660S","SENN_HD660S2","SENN_HD800","SENN_HD800S",
        "SENN_HD820","SENN_HD490PRO","SENN_HD620S","SENN_HD560S","SENN_HD25","SENN_HD25_1",
        "ATECH_R70X","ATECH_ADX5000","ATECH_A2000Z","ATECH_A1000Z",
        "ATECH_M50X","ATECH_M70X",
        "ZMF_VERITE_O","ZMF_VERITE_C","ZMF_ATRIUM_O","ZMF_ATRIUM_C",
        "ZMF_CALDERA","ZMF_AUTEUR","ZMF_AEOLUS",
        "DCA_STEALTH","DCA_EXPANSE","DCA_ETHER2","DCA_AEON2N","DCA_AEON2C",
        "DCA_AEON2NOIRE","DCA_NOIRECLOSED",
        "MEZE_ELITE","MEZE_EMPYREAN","MEZE_EMPYREAN2","MEZE_EMPYREAN3",
        "MEZE_109PRO","MEZE_LIRIC","MEZE_LIRICII","MEZE_99CLASSICS",
        "SHURE_SRH1540","SHURE_SRH1840","SHURE_SRH440A","SHURE_SRH840A",
        "FINAL_D8000","FINAL_D8000PRO",
        "FOSTEX_TH900MK2","FOSTEX_TH610","FOSTEX_TH600","FOSTEX_T50RPMK3","FOSTEX_T50RPMK4",
        "DENON_D9200","DENON_D7200",
        "NEUMANN_NDH20","NEUMANN_NDH30","AUSTRIAN_HIX55","AUSTRIAN_HIX65","AUSTRIAN_HIX60",
        "SONY_MDRZ1R","SONY_MDRZ7M2",
        "AIAIAI_TMA2","AIAIAI_TMA2STUDIO",
        "OLLO_S4X","OLLO_S5X",
        "GRADO_RS1X","GRADO_RS2X","GRADO_GS1000X","GRADO_GS3000X","GRADO_GW100X",
        "HEDD_HEDDPHONE","HEDD_HEDDPHONE2",
        "TA_SOLITAIRE_P","TA_SOLITAIRE_PSE","TA_SOLITAIRE_T",
        "KENNT_ODIN","KENNERTON_THROR",
    ]},
    # No — non-detachable
    **{pid: "No" for pid in [
        "GRADO_SR60X","GRADO_SR80X","GRADO_SR125X","GRADO_SR225X","GRADO_SR325X",
        "GRADO_GH1","GRADO_GH2","GRADO_GH3","GRADO_GH4","GRADO_HEMP",
        "BOSE_QC35II","BOSE_QC45","BOSE_NCH700","BOSE_QCU","BOSE_A20","BOSE_A30",
        "SONY_WH1000XM4","SONY_WH1000XM5","SONY_WH1000XM6",
        "SONY_MDR7506","SONY_MDRCD900ST",
        "BEYER_DT770PRO","BEYER_DT880PRO","BEYER_DT990PRO",
        "ATECH_M40X","ATECH_M20X",
        "AKG_K550","AKG_K553","AKG_K361","AKG_K371",
        "BEATS_STUDIO3","BEATS_STUDIO4","BEATS_STUDIOPRO",
        "APPLE_AIRPODSMAX","APPLE_AIRPODSMAXUSBC",
        "SENN_MOMENTUM3","SENN_MOMENTUM4","SENN_MOMENTUM5",
        "SENN_HD4_50BTNC","SENN_HD4_40BT",
    ]},
}

# Push connectors and detachable into SPECS
for _pid, _conn in CONNECTORS.items():
    if _pid not in SPECS: SPECS[_pid] = {}
    SPECS[_pid]["connector_type"] = _conn

for _pid, _det in DETACHABLE.items():
    if _pid not in SPECS: SPECS[_pid] = {}
    SPECS[_pid]["detachable_cable"] = _det

for _pid, _price in MSRP.items():
    if _pid not in SPECS:
        SPECS[_pid] = {}
    if "msrp_usd" not in SPECS[_pid]:
        SPECS[_pid]["msrp_usd"] = str(_price)

# ---------------------------------------------------------------------------
# SOUND SIGNATURES — community-consensus tuning character for each headphone.
# Categories: Neutral · Warm Neutral · Neutral Bright · Warm · Bright ·
#             V-Shaped · Bassy · Dark · Analytical · U-Shaped
# ---------------------------------------------------------------------------
SOUND_SIGS = {
    # ── Neutral ──────────────────────────────────────────────────────────────
    "SENN_HD600":"Neutral", "SENN_HD490PRO":"Neutral", "SENN_HD560S":"Neutral",
    "SENN_HD280PRO":"Neutral", "SENN_HD380PRO":"Neutral",
    "ATECH_M40X":"Neutral", "ATECH_R70X":"Neutral",
    "ATECH_ADX5000":"Neutral",
    "FOCAL_CLEAR":"Neutral", "FOCAL_CLEARMG":"Neutral",
    "FOCAL_HADENYS":"Neutral", "FOCAL_AZURYS":"Neutral",
    "AUDEZE_LCDX":"Neutral", "AUDEZE_MM500":"Neutral",
    "NEUMANN_NDH20":"Neutral", "NEUMANN_NDH30":"Neutral",
    "AUSTRIAN_HIX55":"Neutral", "AUSTRIAN_HIX65":"Neutral", "AUSTRIAN_HIX60":"Neutral",
    "OLLO_S4X":"Neutral", "OLLO_S5X":"Neutral",
    "AKG_K361":"Neutral", "AKG_K371":"Neutral", "AKG_K271MK2":"Neutral",
    "SHURE_SRH840A":"Neutral", "SHURE_SRH1840":"Neutral",
    "BEYER_DT700PROX":"Neutral",
    "HIFIMAN_EDITION_XS":"Neutral Bright",
    "TAGO_T301":"Neutral", "TAGO_T302":"Neutral",
    "RODE_NTH100":"Neutral",

    # ── Warm Neutral ─────────────────────────────────────────────────────────
    "SENN_HD650":"Warm Neutral", "SENN_HD660S":"Warm Neutral", "SENN_HD660S2":"Warm Neutral",
    "AUDEZE_LCD2":"Warm Neutral", "AUDEZE_LCD2C":"Warm Neutral",
    "AUDEZE_LCD3":"Warm Neutral", "AUDEZE_LCD5":"Warm Neutral", "AUDEZE_LCD5S":"Warm Neutral",
    "AUDEZE_MM100":"Warm Neutral",
    "ZMF_AUTEUR":"Warm Neutral", "ZMF_AEOLUS":"Warm Neutral",
    "ZMF_ATRIUM_O":"Warm Neutral", "ZMF_ATRIUM_C":"Warm Neutral",
    "MEZE_109PRO":"Warm Neutral", "MEZE_LIRIC":"Warm Neutral", "MEZE_LIRICII":"Warm Neutral",
    "BEYER_AMIRON":"Warm Neutral",
    "HIFIMAN_ANANDA":"Warm Neutral", "HIFIMAN_ARYA":"Warm Neutral",
    "HIFIMAN_ARYASTLTH":"Warm Neutral",
    "SONY_MDRZ1R":"Warm Neutral", "SONY_MDRZ7M2":"Warm Neutral",
    "DCA_ETHER2":"Warm Neutral", "DCA_AEON2N":"Warm Neutral",

    # ── Neutral Bright ───────────────────────────────────────────────────────
    "SENN_HD800S":"Neutral Bright",
    "AKG_K701":"Neutral Bright", "AKG_K702":"Neutral Bright", "AKG_K712":"Neutral Bright",
    "HIFIMAN_SUNDARA":"Neutral Bright", "HIFIMAN_HE400SE":"Neutral Bright",
    "HIFIMAN_HE5XX":"Neutral Bright",
    "FOCAL_ELEAR":"Neutral Bright",
    "DCA_EXPANSE":"Neutral Bright",
    "BEYER_DT880PRO":"Neutral Bright",
    "BEYER_DT900PROX":"Neutral Bright",
    "AKG_K812":"Neutral Bright",
    "GRADO_RS1X":"Neutral Bright", "GRADO_RS2X":"Neutral Bright",

    # ── Bright ───────────────────────────────────────────────────────────────
    "SENN_HD800":"Bright", "SENN_HD820":"Bright",
    "BEYER_DT990PRO":"Bright", "BEYER_T1MK1":"Bright", "BEYER_T1MK2":"Bright",
    "GRADO_SR60X":"Bright", "GRADO_SR80X":"Bright", "GRADO_SR125X":"Bright",
    "GRADO_SR225X":"Bright", "GRADO_SR325X":"Bright",
    "GRADO_GS1000X":"Bright", "GRADO_GS3000X":"Bright",
    "HIFIMAN_HE6SE":"Bright", "HIFIMAN_HE560":"Bright", "HIFIMAN_HE560V4":"Bright",
    "SONY_MDR7506":"Bright", "SONY_MDRCD900ST":"Bright",
    "SENN_HD25":"Bright", "SENN_HD25_1":"Bright", "SENN_AMPERIOR":"Bright",
    "AKG_K240":"Bright",
    "STAX_SR009":"Bright", "STAX_SR009S":"Bright", "STAX_X9000":"Bright",

    # ── Analytical ───────────────────────────────────────────────────────────
    "BEYER_DT1990":"Analytical", "BEYER_DT1990MK2":"Analytical",
    "BEYER_DT1770PRO":"Analytical",
    "FOCAL_UTOPIA":"Analytical", "FOCAL_UTOPIA2022":"Analytical",
    "AUDEZE_LCD4":"Analytical",
    "DCA_STEALTH":"Analytical",
    "ZMF_VERITE_O":"Analytical", "ZMF_VERITE_C":"Analytical",
    "HIFIMAN_SUSVARA":"Analytical", "HIFIMAN_HE1000V2":"Analytical", "HIFIMAN_HE1000SE":"Analytical",
    "ATECH_M50X":"Analytical", "ATECH_M70X":"Analytical",
    "BEYER_DT770PRO":"Analytical",
    "AKG_K872":"Analytical", "AKG_K550":"Analytical",
    "SHURE_SRH440A":"Analytical", "SHURE_SRH1540":"Analytical",
    "SUPER_HD668B":"Analytical", "SAMSON_SR850":"Analytical",

    # ── Warm ─────────────────────────────────────────────────────────────────
    "MEZE_99CLASSICS":"Warm", "MEZE_ELITE":"Warm",
    "MEZE_EMPYREAN":"Warm", "MEZE_EMPYREAN2":"Warm", "MEZE_EMPYREAN3":"Warm",
    "AUDEZE_LCD_GX":"Warm",
    "ZMF_CALDERA":"Warm",
    "DENON_D9200":"Warm", "DENON_D7200":"Warm", "DENON_D5000":"Warm",
    "FOSTEX_TH900MK2":"Warm", "FOSTEX_TH610":"Warm",
    "BO_H95":"Warm", "BO_HX":"Warm",
    "MARSHALL_MONITOR2ANC":"Warm", "MARSHALL_MONITOR3ANC":"Warm",
    "BW_PX8":"Warm", "BW_PX7S2":"Warm", "BW_P9":"Warm",
    "SONY_MDR1AM2":"Warm", "SONY_MDRZ7":"Warm",
    "AUDEZE_MM200":"Warm",
    "KENNERTON_ODIN":"Warm", "KENNERTON_THROR":"Warm",
    "HIFIMAN_HER10D":"Warm",

    # ── V-Shaped ─────────────────────────────────────────────────────────────
    "SONY_WH1000XM3":"V-Shaped", "SONY_WH1000XM4":"V-Shaped",
    "SONY_WH1000XM5":"V-Shaped", "SONY_WH1000XM6":"V-Shaped",
    "BOSE_QC35II":"V-Shaped", "BOSE_QC45":"V-Shaped", "BOSE_NCH700":"V-Shaped",
    "BEATS_STUDIO3":"V-Shaped", "BEATS_STUDIOPRO":"V-Shaped", "BEATS_STUDIO4":"V-Shaped",
    "BEATS_SOLO3":"V-Shaped", "BEATS_SOLO4":"V-Shaped",
    "VMODA_M100":"V-Shaped", "VMODA_M100MASTER":"V-Shaped", "VMODA_CROSSFADE2WL":"V-Shaped",
    "APPLE_AIRPODSMAX":"V-Shaped", "APPLE_AIRPODSMAXUSBC":"V-Shaped",
    "SK_CRUSHER_EVO":"V-Shaped", "SK_CRUSHER_ANC":"V-Shaped",
    "SK_HESH3":"V-Shaped",
    "JBL_LIVE660NC":"V-Shaped", "JBL_LIVE770NC":"V-Shaped",
    "JBL_TUNE760NC":"V-Shaped",
    "SENN_MOMENTUM3":"V-Shaped", "SENN_MOMENTUM4":"V-Shaped", "SENN_MOMENTUM5":"V-Shaped",
    "SENN_ACCENTUM":"V-Shaped", "SENN_ACCENTUMPLUS":"V-Shaped",
    "HK_SOHO":"V-Shaped", "HK_SOHOWL":"V-Shaped",
    "BO_H4":"V-Shaped", "BO_H6":"V-Shaped", "BO_H9":"V-Shaped",
    "MARSHALL_MAJOR4":"V-Shaped", "MARSHALL_MAJOR5":"V-Shaped",
    "TECH_EAHA800":"V-Shaped", "TECH_EAHA800M2":"V-Shaped",
    "SONOS_ACE":"V-Shaped",
    "1MORE_SONOFLOW":"V-Shaped",
    "ANKER_SPACEQ45":"V-Shaped", "ANKER_SPACEONE":"V-Shaped",
    "ATECH_SR50BT":"V-Shaped",
    "PHIATON_MS530":"V-Shaped",

    # ── Bassy ────────────────────────────────────────────────────────────────
    "SONY_MDRXB1000":"Bassy", "SONY_MDRXB700":"Bassy",
    "BEATS_EP":"Bassy", "BEATS_MIXR":"Bassy",
    "SK_CRUSHBASE":"Bassy",
    "JBL_CLUBONE":"Bassy",

    # ── Dark ─────────────────────────────────────────────────────────────────
    "AUDEZE_LCD_2":"Dark",
    "STAX_SR007":"Dark",
    "FOCAL_ELEGIA":"Dark",
    "DCA_AEON2C":"Dark",
    "FOCAL_STELLIA":"Dark",

    # ── U-Shaped ─────────────────────────────────────────────────────────────
    "ATECH_M50X":"U-Shaped", "ATECH_M50XBT":"U-Shaped", "ATECH_M50XBT2":"U-Shaped",
    "FOCAL_CELESTEE":"U-Shaped", "FOCAL_BATHYS":"U-Shaped",
    "AUDEZE_LCDXC":"U-Shaped", "AUDEZE_LCD_GX":"U-Shaped",
    "HIFIMAN_HE4XX":"U-Shaped",
    "BEYER_T5P":"U-Shaped", "BEYER_T5PMK2":"U-Shaped",
    "SENN_HD569":"U-Shaped",
    "MARKLEV_5909":"U-Shaped",
}

# Push sound signatures into SPECS
for _pid, _sig in SOUND_SIGS.items():
    if _pid not in SPECS: SPECS[_pid] = {}
    if "sound_signature" not in SPECS[_pid]:
        SPECS[_pid]["sound_signature"] = _sig

# ---------------------------------------------------------------------------
# WEIGHT DATA (grams) — from manufacturer spec sheets
# ---------------------------------------------------------------------------
WEIGHTS = {
    # Sennheiser
    "SENN_HD600":260, "SENN_HD650":260, "SENN_HD660S":260, "SENN_HD660S2":260,
    "SENN_HD800":330, "SENN_HD800S":330, "SENN_HD820":380,
    "SENN_HD490PRO":240, "SENN_HD620S":330,
    "SENN_HD560S":240, "SENN_HD25":140, "SENN_HD25_1":140,
    "SENN_MOMENTUM4":293, "SENN_MOMENTUM5":293, "SENN_ACCENTUM":240,
    "SENN_PXC550II":227,
    # Beyerdynamic
    "BEYER_DT770PRO":270, "BEYER_DT880PRO":295, "BEYER_DT990PRO":250,
    "BEYER_DT1770PRO":388, "BEYER_DT1990":370, "BEYER_DT1990MK2":370,
    "BEYER_T1MK2":360, "BEYER_T1MK3":360,
    "BEYER_DT700PROX":340, "BEYER_DT900PROX":340,
    "BEYER_AMIRON":340, "BEYER_MMX300":363,
    # Audio-Technica
    "ATECH_M50X":285, "ATECH_M40X":240, "ATECH_M70X":300,
    "ATECH_R70X":210, "ATECH_ADX5000":270,
    # AKG
    "AKG_K701":235, "AKG_K702":235, "AKG_K712":235,
    "AKG_K812":390, "AKG_K872":340,
    "AKG_K361":225, "AKG_K371":239,
    # HiFiMan
    "HIFIMAN_SUSVARA":450, "HIFIMAN_HE1000V2":420, "HIFIMAN_HE1000SE":450,
    "HIFIMAN_ARYA":404, "HIFIMAN_ARYASTLTH":440,
    "HIFIMAN_ANANDA":399, "HIFIMAN_SUNDARA":372, "HIFIMAN_EDITION_XS":405,
    "HIFIMAN_HE560":375, "HIFIMAN_HE6SE":458,
    "HIFIMAN_HE400SE":390, "HIFIMAN_HE5XX":440,
    # Focal
    "FOCAL_UTOPIA":490, "FOCAL_UTOPIA2022":490,
    "FOCAL_CLEAR":450, "FOCAL_CLEARMG":450,
    "FOCAL_ELEAR":450, "FOCAL_ELEGIA":430,
    "FOCAL_STELLIA":500, "FOCAL_CELESTEE":420, "FOCAL_BATHYS":360,
    # Audeze
    "AUDEZE_LCD2":585, "AUDEZE_LCD2C":545,
    "AUDEZE_LCD3":550, "AUDEZE_LCD4":735, "AUDEZE_LCD5":420,
    "AUDEZE_LCDX":600, "AUDEZE_LCDXC":695,
    "AUDEZE_MM100":260, "AUDEZE_MM500":360,
    # ZMF
    "ZMF_VERITE_O":415, "ZMF_VERITE_C":425,
    "ZMF_ATRIUM_O":485, "ZMF_ATRIUM_C":495,
    "ZMF_CALDERA":430, "ZMF_AUTEUR":430, "ZMF_AEOLUS":440,
    # Dan Clark Audio
    "DCA_STEALTH":415, "DCA_EXPANSE":415,
    "DCA_ETHER2":290, "DCA_AEON2N":290, "DCA_AEON2C":290,
    # Meze
    "MEZE_ELITE":430, "MEZE_EMPYREAN":430, "MEZE_EMPYREAN2":430, "MEZE_EMPYREAN3":430,
    "MEZE_99CLASSICS":260, "MEZE_109PRO":332, "MEZE_LIRIC":333,
    # Sony
    "SONY_WH1000XM4":254, "SONY_WH1000XM5":250, "SONY_WH1000XM6":254,
    "SONY_MDRZ1R":385, "SONY_MDRZ7M2":350,
    "SONY_MDR7506":230, "SONY_MDR1AM2":235,
    # Bose
    "BOSE_QC45":238, "BOSE_QC35II":235, "BOSE_NCH700":250,
    # Apple
    "APPLE_AIRPODSMAX":385, "APPLE_AIRPODSMAXUSBC":385,
    # Stax
    "STAX_SR009":338, "STAX_SR009S":338, "STAX_SR007":370,
    "STAX_SRL700MK2":430, "STAX_X9000":440,
    # Neumann / Austrian Audio
    "NEUMANN_NDH20":383, "NEUMANN_NDH30":350,
    "AUSTRIAN_HIX55":299, "AUSTRIAN_HIX65":299, "AUSTRIAN_HIX60":299,
    # Shure
    "SHURE_SRH1540":322, "SHURE_SRH1840":369,
    "SHURE_SRH440A":159, "SHURE_SRH840A":218,
    # Beats / Marshall
    "BEATS_STUDIO4":260, "BEATS_STUDIOPRO":260,
    "MARSHALL_MONITOR2ANC":270, "MARSHALL_MONITOR3ANC":282,
    # B&W
    "BW_PX7S2":307, "BW_PX8":309, "BW_PX5":237,
    # V-Moda
    "VMODA_M100MASTER":280, "VMODA_CROSSFADE2WL":280,
    # Grado
    "GRADO_SR60X":175, "GRADO_SR80X":175, "GRADO_SR325X":190,
    "GRADO_GS3000X":350,
    # Ollo Audio
    "OLLO_S4X":319, "OLLO_S5X":319,
    # Final Audio
    "FINAL_D8000":523, "FINAL_D8000PRO":523,
    # Sonos / Mark Levinson / Technics
    "SONOS_ACE":312, "MARKLEV_5909":385, "TECH_EAHA800":237,
    # Koss
    "KOSS_PORTAPRO":60, "KOSS_KSC75":35,
    # FiiO
    "FIIO_FT3":365, "FIIO_FT5":390,
}

# Push weight data into SPECS
for _pid, _wt in WEIGHTS.items():
    if _pid not in SPECS: SPECS[_pid] = {}
    if "weight_g" not in SPECS[_pid]:
        SPECS[_pid]["weight_g"] = str(_wt)

# ---------------------------------------------------------------------------
# EXPANDED CONNECTOR TYPE coverage
# ---------------------------------------------------------------------------
CONNECTORS.update({
    # Sennheiser consumer / gaming
    "SENN_HD569":"3.5mm", "SENN_HD579":"3.5mm", "SENN_HD599":"3.5mm",
    "SENN_HD518":"3.5mm", "SENN_HD558":"3.5mm", "SENN_HD558":"3.5mm",
    "SENN_HD4_40BT":"Wireless", "SENN_HD4_50BTNC":"Wireless",
    "SENN_HD350BT":"Wireless", "SENN_HD450BT":"Wireless", "SENN_HD250BT":"Wireless",
    "SENN_MOMENTUM3":"Wireless", "SENN_MOMENTUM4":"Wireless", "SENN_MOMENTUM5":"Wireless",
    "SENN_ACCENTUM":"Wireless", "SENN_ACCENTUMPLUS":"Wireless",
    "SENN_PXC550":"Wireless", "SENN_PXC550II":"Wireless",
    # Beyerdynamic consumer
    "BEYER_DT231":"3.5mm", "BEYER_DT235":"3.5mm",
    "BEYER_AVENTHOW":"Wireless",
    # AKG consumer
    "AKG_K52":"3.5mm", "AKG_K72":"3.5mm", "AKG_K92":"3.5mm",
    "AKG_K44":"3.5mm", "AKG_K450":"3.5mm", "AKG_K553":"3.5mm",
    "AKG_Y50BT":"Wireless", "AKG_N60NC":"Wireless", "AKG_N700NC":"Wireless",
    # Sony consumer/wireless
    "SONY_WH1000XM2":"Wireless", "SONY_WH1000XM3":"Wireless",
    "SONY_WHCH700N":"Wireless", "SONY_WHCH710N":"Wireless", "SONY_WHCH720N":"Wireless",
    "SONY_MDR1R":"3.5mm", "SONY_MDR1A":"3.5mm", "SONY_MDRZ5":"3.5mm",
    "SONY_MDRZ7":"3.5mm", "SONY_MDR7510":"3.5mm", "SONY_MDR7520":"6.35mm",
    # Bose
    "BOSE_QC35II":"Wireless", "BOSE_QC45":"Wireless", "BOSE_NCH700":"Wireless",
    "BOSE_QCU":"Wireless",
    # Beats
    "BEATS_STUDIO3":"Wireless", "BEATS_STUDIO4":"Wireless", "BEATS_STUDIOPRO":"Wireless",
    "BEATS_SOLO3":"Wireless", "BEATS_SOLO4":"Wireless", "BEATS_SOLOPRO":"Wireless",
    # Grado all use fixed 3.5mm
    "GRADO_SR60X":"3.5mm", "GRADO_SR80X":"3.5mm", "GRADO_SR125X":"3.5mm",
    "GRADO_SR225X":"3.5mm", "GRADO_SR325X":"3.5mm",
    "GRADO_GH1":"3.5mm", "GRADO_GH2":"3.5mm", "GRADO_GH3":"3.5mm",
    "GRADO_GH4":"3.5mm", "GRADO_HEMP":"3.5mm",
    "GRADO_PS1000E":"3.5mm", "GRADO_PS2000E":"3.5mm",
    # Stax (electrostatic bias connection)
    "STAX_SRL300":"Electrostatic", "STAX_SRL500":"Electrostatic",
    "STAX_SRL700":"Electrostatic", "STAX_SR404":"Electrostatic",
    "STAX_SR207":"Electrostatic", "STAX_SR507":"Electrostatic",
    "STAX_SR4070":"Electrostatic",
    # HiFiMan electrostatic
    "HIFIMAN_JADE2":"Electrostatic", "HIFIMAN_SHANGRILA":"Electrostatic",
    # Audeze CRBN
    "AUDEZE_CRBN":"Electrostatic", "AUDEZE_CRBN2":"Electrostatic",
    # Gaming / wireless
    "ASTRO_A50G4":"Wireless", "ASTRO_A50X":"Wireless",
    "ASTRO_A40":"3.5mm", "ASTRO_A40TR":"3.5mm",
    "RAZER_BARRACUDAX":"Wireless", "RAZER_NARIU":"Wireless",
    "RAZER_KRAKENX":"3.5mm", "RAZER_KRAKENULTI":"USB",
    "LOGI_G435":"Wireless", "LOGI_G533":"Wireless", "LOGI_G733":"Wireless", "LOGI_G735":"Wireless",
    "LOGI_G432":"USB", "LOGI_G433":"USB", "LOGI_G635":"USB",
    "SS_ARCTIS7":"Wireless", "SS_ARCTISNOVA7":"Wireless", "SS_ARCTIS_NOVA_PRO":"Wireless",
    "SS_ARCTIS5":"USB", "SS_ARCTIS3":"3.5mm",
    "HX_CLOUDFLIGHTS":"Wireless", "HX_CLOUD2":"3.5mm", "HX_CLOUDALPHA":"3.5mm",
    "TB_STEALTH700G2":"Wireless", "TB_STEALTHPRO":"Wireless", "TB_STEALTH600G2":"Wireless",
    "CORSAIR_HS80":"Wireless", "CORSAIR_HS70":"Wireless",
    # Consumer wireless
    "SONY_TECH_EAHA800":"Wireless",
    "TECH_EAHA800":"Wireless", "TECH_EAHA800M2":"Wireless",
    "SONOS_ACE":"Wireless",
    "SENN_MOMENTUM3":"Wireless",
    "BO_H95":"Wireless", "BO_HX":"Wireless", "BO_H100":"Wireless",
    "MARSHALL_MONITOR2ANC":"Wireless", "MARSHALL_MONITOR3ANC":"Wireless",
    "MARSHALL_MIDANC":"Wireless",
    "BW_PX7S2":"Wireless", "BW_PX8":"Wireless", "BW_PX7":"Wireless",
    "BW_PX5":"Wireless", "BW_PX":"Wireless",
    "MARKLEV_5909":"Wireless",
    "1MORE_SONOFLOW":"Wireless", "1MORE_SONOFLOWSE":"Wireless",
    "ANKER_SPACEQ45":"Wireless", "ANKER_SPACEONE":"Wireless", "ANKER_SPACEONEPRO":"Wireless",
    "ATECH_M50XBT":"Wireless", "ATECH_M50XBT2":"Wireless",
    # Koss
    "KOSS_PORTAPRO":"3.5mm", "KOSS_PORTAPROWL":"Wireless",
    "KOSS_KSC75":"3.5mm", "KOSS_KPH30I":"3.5mm", "KOSS_KPH40":"3.5mm",
    # Studio non-detachable
    "SONY_MDR7506":"3.5mm/6.35mm", "SONY_MDRCD900ST":"3.5mm",
    "SUPER_HD668B":"3.5mm", "SAMSON_SR850":"3.5mm",
    "TAKSTAR_PRO80":"6.35mm", "TAKSTAR_PRO82":"6.35mm",
    # FiiO
    "FIIO_FT3":"4.4mm Pentaconn", "FIIO_FT5":"4.4mm Pentaconn",
    "FIIO_FT1":"3.5mm", "FIIO_FT1PRO":"3.5mm",
    # Denon
    "DENON_D9200":"Dual 3.5mm", "DENON_D7200":"Dual 3.5mm",
    "DENON_D600":"Dual 3.5mm", "DENON_D2000":"3.5mm", "DENON_D5000":"3.5mm",
    # Crosszone / MySphere / Tago
    "CZ_CZ1":"3.5mm", "CZ_CZ10":"3.5mm",
    "TAGO_T301":"4.4mm Pentaconn", "TAGO_T302":"4.4mm Pentaconn",
    # V-Moda
    "VMODA_M100":"3.5mm", "VMODA_M100MASTER":"3.5mm",
    "VMODA_CROSSFADE2WL":"Wireless",
})

# Push expanded connectors into SPECS
for _pid, _conn in CONNECTORS.items():
    if _pid not in SPECS: SPECS[_pid] = {}
    SPECS[_pid]["connector_type"] = _conn

# Expanded detachable data
DETACHABLE.update({
    **{pid: "Yes" for pid in [
        "SENN_HD560S","SENN_HD518","SENN_HD558","SENN_HD569","SENN_HD579","SENN_HD599",
        "ATECH_M50XBT","ATECH_M50XBT2","ATECH_WP900",
        "BEYER_DT231","BEYER_DT235",
        "FIIO_FT3","FIIO_FT5","FIIO_FT1","FIIO_FT1PRO",
        "DENON_D9200","DENON_D7200","DENON_D600","DENON_D5000","DENON_D2000",
        "HIFIMAN_HE5XX","HIFIMAN_HE400SE","HIFIMAN_HE4XX",
        "FOSTEX_TXO","FOSTEX_TR80",
        "GRADO_GW100X",
        "TAGO_T301","TAGO_T302",
        "AIAIAI_TMA1","AIAIAI_TMA2WL",
        "PSB_M4U1","PSB_M4U2",
        "MEZE_99NOIR","MEZE_99CLASSICSWALNUT",
    ]},
    **{pid: "No" for pid in [
        "SENN_HD4_40BT","SENN_HD4_50BTNC","SENN_HD350BT","SENN_HD450BT","SENN_HD250BT",
        "SENN_MOMENTUM3","SENN_MOMENTUM4","SENN_MOMENTUM5","SENN_ACCENTUM","SENN_ACCENTUMPLUS",
        "SENN_PXC550","SENN_PXC550II","SENN_HD25","SENN_HD25_1","SENN_AMPERIOR",
        "GRADO_SR60X","GRADO_SR80X","GRADO_SR125X","GRADO_SR225X","GRADO_SR325X",
        "GRADO_GH1","GRADO_GH2","GRADO_GH3","GRADO_GH4","GRADO_HEMP",
        "GRADO_RS1X","GRADO_RS2X","GRADO_GS1000X","GRADO_GS3000X",
        "AKG_K52","AKG_K72","AKG_K92","AKG_K44","AKG_K450",
        "BEATS_EP","BEATS_MIXR",
        "MARSHALL_MAJOR2","MARSHALL_MAJOR3","MARSHALL_MAJOR4","MARSHALL_MAJOR5",
        "MARSHALL_MIDANC","MARSHALL_MONITOR2ANC","MARSHALL_MONITOR3ANC",
        "KOSS_PORTAPRO","KOSS_KSC75","KOSS_KPH30I","KOSS_KPH40","KOSS_KPH7",
        "SS_ARCTIS1","SS_ARCTIS3","SS_ARCTIS5","SS_ARCTIS7","SS_ARCTISNOVA",
        "SS_ARCTISNOVA5","SS_ARCTISNOVA7","SS_ARCTIS_NOVA_PRO",
        "HX_CLOUD2","HX_CLOUDALPHA","HX_CLOUDS","HX_CLOUDFLIGHTS","HX_CLOUDFLIGHT3",
        "RAZER_KRAKENX","RAZER_KRAKENULTI","RAZER_NARIU","RAZER_BARRACUDAX",
        "LOGI_G430","LOGI_G432","LOGI_G433","LOGI_G435","LOGI_G533","LOGI_G635","LOGI_G735",
        "TB_STEALTH600G2","TB_STEALTH700G2","TB_STEALTHPRO",
        "ASTRO_A40","ASTRO_A40TR","ASTRO_A50G4","ASTRO_A50X",
        "CORSAIR_HS80","CORSAIR_HS70",
        "SONY_WH1000XM4","SONY_WH1000XM5","SONY_WH1000XM6",
        "SONY_WHCH700N","SONY_WHCH710N","SONY_WHCH720N",
        "SONY_CH500","SONY_CH510","SONY_CH520",
        "BO_H95","BO_HX","BO_H100","BO_H4","BO_H6","BO_H9",
        "BW_PX5","BW_PX7","BW_PX7S2","BW_PX8",
        "TECH_EAHA800","TECH_EAHA800M2","SONOS_ACE","MARKLEV_5909",
        "ANKER_LIFEQ20","ANKER_LIFEQ30","ANKER_SPACEQ45","ANKER_SPACEONE",
        "1MORE_SONOFLOW","1MORE_SONOFLOWSE",
        "SUPER_HD668B","SAMSON_SR850","TAKSTAR_PRO80","TAKSTAR_PRO82",
    ]},
})

# Push expanded detachable into SPECS
for _pid, _det in DETACHABLE.items():
    if _pid not in SPECS: SPECS[_pid] = {}
    SPECS[_pid]["detachable_cable"] = _det

# ---------------------------------------------------------------------------
# WEIGHT EXPANSION — fills gaps across all major brands
# ---------------------------------------------------------------------------
WEIGHTS.update({
    # Sennheiser remaining
    "SENN_HD518":238, "SENN_HD555":260, "SENN_HD558":260,
    "SENN_HD569":229, "SENN_HD579":218, "SENN_HD599":223,
    "SENN_HD400BT":175, "SENN_HD350BT":155, "SENN_HD450BT":170, "SENN_HD250BT":227,
    "SENN_HD4_40BT":185, "SENN_HD4_50BTNC":229,
    "SENN_MOMENTUM2":190, "SENN_ACCENTUM":240, "SENN_ACCENTUMPLUS":280,
    "SENN_PXC550":227, "SENN_PXC550II":227,
    "SENN_AMPERIOR":143, "SENN_HD25":140, "SENN_HDB630":355,
    # Sony remaining
    "SONY_WH1000XM2":275, "SONY_WH1000XM3":255,
    "SONY_WHCH700N":223, "SONY_WHCH710N":223, "SONY_WHCH720N":192,
    "SONY_MDR7506":230, "SONY_MDRCD900ST":200,
    "SONY_MDRXB950N1":270, "SONY_MDRXB1000":320,
    "SONY_CH500":130, "SONY_ZX110":107,
    # Beyerdynamic remaining
    "BEYER_DT240PRO":190, "BEYER_AVENTHOW":340,
    "BEYER_T5P":290, "BEYER_T5PMK2":310, "BEYER_DT1350":230,
    # AKG remaining
    "AKG_K92":178, "AKG_K72":190, "AKG_K52":190,
    "AKG_K240":240, "AKG_K450":170, "AKG_N60NC":162,
    "AKG_N700NC":303, "AKG_N700NCM2":295, "AKG_Y50BT":190,
    # HiFiMan remaining
    "HIFIMAN_HE400SE":390, "HIFIMAN_HE400I":370, "HIFIMAN_HE400I2020":370,
    "HIFIMAN_HE5XX":440, "HIFIMAN_HE4XX":440, "HIFIMAN_HE6SE":458,
    "HIFIMAN_HE560":375, "HIFIMAN_JADE2":550,
    "HIFIMAN_DEVA":360, "HIFIMAN_DEVA_PRO":360, "HIFIMAN_HEX4":390,
    # Grado remaining
    "GRADO_SR60X":175, "GRADO_SR80X":175, "GRADO_SR125X":175,
    "GRADO_SR225X":190, "GRADO_SR325X":190,
    "GRADO_RS1X":290, "GRADO_RS2X":260,
    "GRADO_GS1000X":350, "GRADO_GH1":200, "GRADO_GH4":240,
    "GRADO_HEMP":220, "GRADO_GW100X":265,
    # JBL
    "JBL_LIVE660NC":249, "JBL_LIVE770NC":232, "JBL_TUNE760NC":190,
    "JBL_TUNE710BT":160, "JBL_CLUBONE":289, "JBL_LIVE460":170,
    "JBL_LIVE400":162,
    # Fostex
    "FOSTEX_TH600":400, "FOSTEX_TH900":390, "FOSTEX_TH610":390,
    "FOSTEX_T50RPMK3":320, "FOSTEX_T50RPMK4":320,
    "FOSTEX_TR80":294, "FOSTEX_TXO":280,
    # Audeze remaining
    "AUDEZE_LCD4":735, "AUDEZE_LCDXC":695,
    "AUDEZE_MM200":346, "AUDEZE_CRBN":650,
    "AUDEZE_MAXWELL":265, "AUDEZE_PENROSE":345,
    # Razer
    "RAZER_KRAKENX":250, "RAZER_KRAKENULTI":322,
    "RAZER_NARIU":340, "RAZER_BARRACUDAX":250,
    "RAZER_BSHARKV2":262, "RAZER_OPUS2020":300,
    # Bose remaining
    "BOSE_NCH700":250, "BOSE_A20":340, "BOSE_A30":340,
    # Focal remaining
    "FOCAL_LISTEN":195, "FOCAL_LISTENPRO":180,
    "FOCAL_HADENYS":450, "FOCAL_AZURYS":335,
    # Dan Clark remaining
    "DCA_MADDOG":385, "DCA_AEON2NOIRE":295, "DCA_VOCE":455,
    # ZMF remaining
    "ZMF_ATTICUS":430, "ZMF_EIKON":420, "ZMF_ORI":350,
    # Stax remaining
    "STAX_SRL300":400, "STAX_SRL500":415, "STAX_SRL700":416,
    "STAX_SR404":381, "STAX_SR207":285, "STAX_SR507":358,
    # Shure remaining
    "SHURE_SRH440":218, "SHURE_SRH750DJ":269, "SHURE_SRH940":305,
    # B&W remaining
    "BW_P3":138, "BW_P5":215, "BW_P7":290,
    "BW_PX":275, "BW_P9":350,
    # Logitech G
    "LOGI_G432":259, "LOGI_G435":165, "LOGI_G533":350,
    "LOGI_G635":375, "LOGI_G733":278, "LOGI_G735":300,
    "LOGI_G930":375,
    # Beats remaining
    "BEATS_STUDIO3":260, "BEATS_SOLO3":215, "BEATS_SOLO4":220,
    "BEATS_SOLOPRO":260, "BEATS_EP":155, "BEATS_MIXR":197,
    # Denon
    "DENON_D2000":345, "DENON_D5000":360, "DENON_D7000":395,
    "DENON_D7200":385, "DENON_D1100":255, "DENON_D600":330,
    # Yamaha
    "YAMAHA_HPHMT7":210, "YAMAHA_HPHMT8":210, "YAMAHA_YHL700A":305,
    # Ultrasone
    "ULTRA_ED8":280, "ULTRA_ED10":350, "ULTRA_HFI780":230,
    "ULTRA_HFI2400":230, "ULTRA_SIGPURE":290, "ULTRA_PERF880":350,
    # Marshall
    "MARSHALL_MAJOR2":170, "MARSHALL_MAJOR3":165,
    "MARSHALL_MAJOR4":163, "MARSHALL_MAJOR5":163,
    "MARSHALL_MIDANC":210, "MARSHALL_MONITOR":249,
    "MARSHALL_MONITOR2ANC":270, "MARSHALL_MONITOR3ANC":282,
    # Bang & Olufsen
    "BO_H4":235, "BO_H6":235, "BO_H9":250,
    "BO_H95":351, "BO_HX":371, "BO_H100":421,
    # HyperX
    "HX_CLOUD2":309, "HX_CLOUDALPHA":336, "HX_CLOUDFLIGHTS":275,
    "HX_CLOUDFLIGHT3":270, "HX_CLOUDII_WL":309,
    # SteelSeries
    "SS_ARCTIS3":262, "SS_ARCTIS5":271, "SS_ARCTIS7":354,
    "SS_ARCTIS7P":354, "SS_ARCTISNOVA5":251, "SS_ARCTISNOVA7":338,
    "SS_ARCTIS_NOVA_PRO":342,
    # Skullcandy
    "SK_HESH3":195, "SK_CRUSHER_EVO":255, "SK_CRUSHER_ANC":276,
    "SK_VENUE_ANC":220,
    # Corsair
    "CORSAIR_HS80":333, "CORSAIR_HS70":340,
    # Turtle Beach
    "TB_STEALTH600G2":290, "TB_STEALTH700G2":322, "TB_STEALTHPRO":397,
    # Astro
    "ASTRO_A40":368, "ASTRO_A40TR":336, "ASTRO_A50G4":374, "ASTRO_A50X":374,
    # V-Moda
    "VMODA_LP":280, "VMODA_M100":355, "VMODA_M100MASTER":350,
    "VMODA_CROSSFADE2WL":350,
    # Koss
    "KOSS_ESP95X":127, "KOSS_KPH30I":67, "KOSS_KPH40":56,
    # Philips
    "PHILI_X2HR":320, "PHILI_SHP9500":290,
    "PHILI_L2BO":278, "PHILI_A5PRO":280,
    # Monoprice
    "MONO_M1060":520, "MONO_M1060C":590, "MONO_M570":470,
    # Superlux
    "SUPER_HD668B":200, "SUPER_HD681":195, "SUPER_HD669":220,
    # Edifier STAX Spirit
    "EDIFIER_STAXGT1":390, "EDIFIER_STAXGT5":450,
    # FiiO
    "FIIO_FT1":345, "FIIO_FT3":365, "FIIO_FT5":390,
    # Meze remaining
    "MEZE_99NOIR":260, "MEZE_LIRICII":333,
    # Abyss
    "ABYSS_AB1266":480, "ABYSS_DIANA":330,
    "ABYSS_DIANATC":350, "ABYSS_DIANAV2":330,
    # Kennerton
    "KENNERTON_ODIN":520, "KENNERTON_THROR":560,
    # Final Audio remaining
    "FINAL_SONOROUS3":390, "FINAL_SONOROUS6":430,
    # Anker Soundcore
    "ANKER_LIFEQ20":253, "ANKER_LIFEQ30":260,
    "ANKER_SPACEQ45":270, "ANKER_SPACEONE":265,
    # 1More
    "1MORE_SONOFLOW":237, "1MORE_SONOFLOWSE":237,
    # Harman Kardon
    "HK_SOHO":140, "HK_SOHOWL":138, "HK_SOHOWNC":142,
    # Status Audio
    "STATUS_CB1":208, "STATUS_OB1":240,
    # Moondrop
    "MOONDROP_VENUS":435, "MOONDROP_PARA":470,
    # T+A
    "TA_SOLITAIRE_P":490,
    # HEDD Audio
    "HEDD_HEDDPHONE":718, "HEDD_HEDDPHONE2":700,
    # Sendy Audio
    "SENDY_AIVA":430, "SENDY_PEACOCK":490, "SENDY_APOLLO":380,
    # Kiwi Ears
    "KIWIEARS_ARDOR":390, "KIWIEARS_ELLIPSE":420,
    # JVC
    "JVC_HADX1000":390, "JVC_HADX2000":380,
    "JVC_HASW01":280, "JVC_HASW02":275,
    # Jabra
    "JABRA_E285":149, "JABRA_E275":185, "JABRA_E265":175,
    "JABRA_E255":155, "JABRA_E240":164, "JABRA_E230":78,
    # Takstar
    "TAKSTAR_PRO80":368, "TAKSTAR_PRO82":350, "TAKSTAR_HF580":445,
    # Modhouse
    "MODHOUSE_ARGONMK3":380, "MODHOUSE_TUNGSTEN":400,
    # Ollo remaining
    "OLLO_X1":282,
    # Rosson
    "ROSSON_RAD0":460,
    # Spirit Torino
    "SPIRITTORINO_SUPER":285, "SPIRITTORINO_RADIANTE":295,
    # RAAL
    "RAAL_SR1A":150,
    # MySphere
    "MYSPHERE_3":490, "MYSPHERE_3X":490,
    # Crosszone
    "CZ_CZ1":380, "CZ_CZ10":350,
    # Tago Studio
    "TAGO_T301":370, "TAGO_T302":380,
    # Mark Levinson
    "MARKLEV_5909":385,
    # Pioneer DJ
    "PIONEER_HDJX10":334, "PIONEER_HDJ2000":330,
    "PIONEER_SEMASTER1":395,
    # Goldplanar
    "GOLD_GL2000DS":480, "GOLD_GL2000SS":450,
    # PSB
    "PSB_M4U1":285, "PSB_M4U2":290,
    # Phiaton
    "PHIATON_MS530":195, "PHIATON_BT460":185,
    # House of Marley
    "MARLEY_PV2":170, "MARLEY_PV2BT":185,
    # Plantroncis
    "PLANT_BB810":175,
    # Creative
    "CREATIVE_AVLIVE":208,
})

# Push all weight data into SPECS
for _pid, _wt in WEIGHTS.items():
    if _pid not in SPECS: SPECS[_pid] = {}
    if "weight_g" not in SPECS[_pid]:
        SPECS[_pid]["weight_g"] = str(_wt)

products = []
lineage_pairs = set()
# Transform pass: turn each raw add() row into a final product record. The SPECS dict
# above is an optional overlay of researched measurements (impedance, driver size, MSRP,
# etc.) keyed by product_id — when present it fills in fields the inline add() call left
# blank. Family and manufacturer names are also resolved to their numeric ids here.
for _int_id, row in enumerate(P, start=1):
    (pid, mfr, fam, model, full, year, disc, status, cat, design, driver,
     dsize, imp, sens, wl, anc, pred, succ, notes, date_added, fit,
     msrp, sig, conn, detach, weight) = row
    if pid in SPECS:
        s = SPECS[pid]
        dsize = s.get("driver_size", dsize)
        imp = s.get("impedance", imp)
        sens = s.get("sensitivity", sens)
        msrp = s.get("msrp_usd", msrp)
        sig = s.get("sound_signature", sig)
        conn = s.get("connector_type", conn)
        detach = s.get("detachable_cable", detach)
        weight = s.get("weight_g", weight)
    spec_conf = "Verified" if pid in VERIFIED_SPECS else "Estimated"
    fid = fam_id.get((mfr, fam), "")
    mid = mfr_id[mfr]
    products.append([_int_id, pid, fid, mid, model, full, year, disc, status, cat,
                     design, driver, dsize, imp, sens, wl, anc, pred, succ, notes, date_added, fit,
                     msrp, sig, conn, detach, weight, spec_conf])
    if pred:
        lineage_pairs.add((pred, pid))
    if succ:
        lineage_pairs.add((pid, succ))

# ---------------------------------------------------------------------------
# Write CSVs
# Serialise every table to its CSV. Each writer emits an explicit header row so the
# column order is fixed and matches what build_db.py and the import endpoint expect;
# changing a column here means updating those consumers too.
# ---------------------------------------------------------------------------
with open(OUT / "manufacturers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["manufacturer_id","name","country","website","status","founded_year","description"])
    w.writerows(manufacturers)

with open(OUT / "families.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["family_id","manufacturer_id","family_name","family_type"])
    w.writerows(families)

with open(OUT / "products.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id","product_id","family_id","manufacturer_id","model_name","full_name",
                "release_year","discontinued_year","status","category","design",
                "driver_type","driver_size_mm","impedance_ohms","sensitivity_db",
                "wireless","anc","predecessor","successor","notes","date_added","fit",
                "msrp_usd","sound_signature","connector_type","detachable_cable","weight_g","spec_confidence"])
    w.writerows(products)

# Guard: catch duplicate product_ids before they cause D1 import failures.
# product_id is the primary key in D1, so a duplicate here would crash the import
# halfway through. Asserting now turns that into an immediate, named error at generation.
_pids = [p[1] for p in products]  # index 1 = product_id
_dupes = [pid for pid, n in __import__('collections').Counter(_pids).items() if n > 1]
assert not _dupes, f"DUPLICATE product_ids found — fix before importing: {_dupes}"

lineage = sorted(lineage_pairs, key=lambda x: (x[1], x[0]))
with open(OUT / "lineage.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["lineage_id","predecessor_product_id","successor_product_id"])
    for i, (pre, suc) in enumerate(lineage, start=1):
        w.writerow([i, pre, suc])

print(f"Manufacturers: {len(manufacturers)}")
print(f"Families:      {len(families)}")
print(f"Products:      {len(products)}")
print(f"Lineage links: {len(lineage)}")
