# We Out Here 2026 — artist data
# Fields: name, tag, day, time, stage, link (verified mix URL or None), note

VERIFIED = {
    're:ni': 'https://soundcloud.com/mixmag-1/impact-reni-mix',
    'Blawan': 'https://soundcloud.com/platform/blawan-dkmntl',
    'Ivy Lab': 'https://soundcloud.com/mixmag-1/ivy-lab-cover-mix',
    'Shackleton': 'https://soundcloud.com/bleep_bot/bleep-mix-152-shackleton',
    'rRoxymore': 'https://soundcloud.com/rinsefm/rroxymore120325',
    'Ceephax Acid Crew': 'https://soundcloud.com/platform/ceephax-acid-crew',
    'Calibre': 'https://soundcloud.com/calibresignature/sets/calibre-dj-mixes',
    'Nono Gigsta': 'https://soundcloud.com/thelotradio/nono-gigsta-the-lot-radio-06',
    'I-Sha': 'https://soundcloud.com/i-shaa/sets/radio',
    'DJ Flight': 'https://soundcloud.com/platform/dj-flight',
    'Silva Snipa': 'https://soundcloud.com/balamii/silva-snipa-mar-2025',
    'Alix Perez': 'https://soundcloud.com/drumandbassarena/alix-perez-bbc-radio-1-dance-presents-drumbassarena',
    'King Britt': 'https://soundcloud.com/kingbritt/sets/dj-live-performances',
    'Barker': 'https://soundcloud.com/resident-advisor/ra982-barker',
    'Introspekt': 'https://soundcloud.com/user-643553014/spaces-in-between-introspekt',
    'Sadar Bahar': 'https://soundcloud.com/resident-advisor/ra507-sadar-bahar',
    'Ge-ology': 'https://soundcloud.com/gillespeterson/ge-ology-in-the-mix',
    'DJ Spanish Fly': 'https://soundcloud.com/user-643553014/dj-spanish-fly-230724',
    'Elliott Skinner': 'https://soundcloud.com/elliott-reed-skinner',
    'Ehua': 'https://www.factmag.com/2022/02/14/fact-mix-846-ehua/',
    'Wheel Up': 'https://www.mixcloud.com/truthoughts/stay-at-home-sessions-wheelup/',
    'Esa': 'https://soundcloud.com/dkmntl/dekmantel-podcast-037-esa',
    'Juls': 'https://soundcloud.com/platform/juls-london',
}

# Blurbs written for this site, for acts the festival has not written up itself.
# These are shown labelled as ours, never as the festival's. Keep every claim
# traceable to something in 'sources' and do not pad them out with adjectives.
BLURBS = {
    'Ehua': {
        'text': (
            "Ehua is Italian-Ivorian, grew up in Pisa and has been in London for over a decade. "
            "She builds tracks out of drums rather than melody: custom percussion samples, "
            "intricate patterns, and a lot of sound design, sitting somewhere between hard drum, "
            "bass music and experimental techno. Her first track 'New Moon' came out on femme "
            "culture in 2018, followed the same November by the 'Diplozoon' EP.\n\n"
            "'Aquamarine' on Nervous Horizon (23 April 2021) is the one to start with. Six "
            "tracks built around the colour and movement of water, running 95 to 140bpm, from "
            "sludgy broken beats through to drone techno, with her own voice on 'Black' as "
            "spoken Italian played backwards.\n\n"
            "She holds a long-running residency on Rinse FM, and before that a show on Radio "
            "Raheem in Milan where she brought in Scratchclart, KG, TSVI and Air Max '97. Away "
            "from music she co-runs GRIOT and co-edits GRIOTmag, which covers art, music and "
            "fashion from Africa and the diaspora. Worth knowing before the weekend: she has "
            "named gqom as a direct influence and singled out DJ Lag, who is also on this bill."
        ),
        'sources': [
            ('Fact', 'https://www.factmag.com/2022/02/14/fact-mix-846-ehua/'),
            ('DJ Mag', 'https://djmag.com/content/fresh-kicks-91-ehua'),
            ('Bandcamp', 'https://ehua.bandcamp.com/album/aquamarine-ep'),
            ('Rinse FM', 'https://www.rinse.fm/shows/ehua'),
        ],
    },
    'Wheel Up': {
        'text': (
            "Danny Wheeler, who styles the name WheelUP, is from West London and is of "
            "Zimbabwean and British descent. He spent years in jungle and drum & bass under his "
            "own name, running the W10 Records label, before turning to the broken beat scene "
            "that grew up in the same part of the city. Afronaut, who founded Bugz in the Attic "
            "and helped invent the sound, gave him the WheelUP name, and Bugz in the Attic later "
            "made him an honorary member. The lineage he plays in runs back through them to "
            "4hero.\n\n"
            "Bruk is broken beat: syncopated, off-grid drums at house tempo, with jazz and "
            "boogie harmony over the top. His first record under the name was 'Self Healing "
            "Machine' for Tru Thoughts, and the albums 'Good Love' (2021), 'We Are The Magic' "
            "(2023) and 'Inner Light' followed on the same label, pulling in hip-hop, neo-soul "
            "and nu-jazz and featuring Afronaut, Kaidi Tatham, Abacus and Tiawa among others."
        ),
        'sources': [
            ('Tru Thoughts', 'https://tru-thoughts.co.uk/artists/wheelup/'),
            ('Tru Thoughts, new signing',
             'https://tru-thoughts.co.uk/new-signing-wheelup-danny-wheelers-bruk-moniker/'),
            ('Resident Advisor', 'https://ra.co/dj/wheelup/biography'),
        ],
    },
    'DJ Lag': {
        'text': (
            "Lwazi Asanda Gwala grew up in Clermont, a township outside Durban, and is one of "
            "the handful of producers who built gqom in the first place. The word is Zulu for a "
            "drum or a hit, which tells you where the emphasis goes: the kick is broken up "
            "rather than four to the floor, the arrangements are stripped back, and the whole "
            "thing leans on drums and space instead of melody. He made the early tracks on "
            "FruityLoops while he was still at school, and from 2012 Durban taxi drivers played "
            "them to pull in passengers, which is how the sound got around the city before any "
            "label was involved.\n\n"
            "A 2015 Boiler Room session took it well beyond Durban, and London's Goon Club "
            "Allstars released his self-titled EP in 2016. 'Ice Drop' and 'Umlilo' did the rest, "
            "and the video for 'Ice Drop', shot around Clermont and KwaDabeka, ended up in the "
            "Design Museum's electronic music exhibition in London. In 2019 he produced 'My "
            "Power' for Beyoncé's 'The Lion King: The Gift', worked up from a track of his "
            "called 'Drumming'.\n\n"
            "His debut album 'Meeting With The King' (2022) is where he started calling it gqom "
            "2.0, pulling amapiano, Afro house and Afro tech into the same room. 'Raptor', the "
            "lead single, is a collaboration with Sinjin Hawke. 'Something Different' is on "
            "there, and so is 'Yasho Leyonto' with Dladla Mshunqisi. It was nominated for Best "
            "Gqom Album at the 2023 South African Music Awards. If you only know 'Ice Drop', the "
            "album is where he opened the sound out, and it is the better preparation for a late "
            "set."
        ),
        'sources': [
            ('blackmajor.co.za', 'https://blackmajor.co.za/artist/dj-lag/'),
            ('Wikipedia', 'https://en.wikipedia.org/wiki/DJ_Lag'),
            ('DJ Mag', 'https://djmag.com/features/album-month-dj-lag-meeting-king'),
            ('Resident Advisor', 'https://ra.co/reviews/34713'),
        ],
    },
}

# (name, tag, day, time, stage)
ELECTRONIC = [
    ('Scientist', 'Dub', 'Sat', '14:00-15:30', 'The Bowl'),
    ('Blawan (Live)', 'Techno', 'Sat', '01:00-02:00', 'The Grove'),
    ('Barker (Live)', 'Techno', 'Thu', '23:00-00:00', 'The Grove'),
    ('Actress', 'Techno', 'Thu', '20:20-21:20', 'Lush Life'),
    ('Herbert & Momoko', 'House / Experimental', 'Sun', '17:20-18:20', 'Lush Life'),
    ('Adam F', 'Drum & Bass', 'Fri', '20:40-21:50', 'Lush Life'),
    ('Da Lata', 'Broken Beat / Brazilian club', 'Sun', '12:00-13:00', 'Main Stage'),
    ('Lone (Live)', 'House / Techno', 'Thu', '22:00-23:00', 'The Grove'),
    ('Musclecars (Live)', 'House', 'Sat', '17:50-18:50', 'Main Stage'),
    ('Jazzanova "In Between"', 'Nu-jazz / House', 'Sat', '16:20-17:20', 'Main Stage'),
    ('HVYWGHT & The Outlook Orchestra', 'Dub / Bass', 'Thu', '21:20-23:00', 'Main Stage'),
    ('A Grime Supreme', 'Grime', 'Sun', '18:30-19:30', "Tomorrow's Warriors Big Top"),
    ('James Alexander Bright (Live)', 'Electronic', 'Thu', '19:30-20:30', 'Brawnswood'),
    ('Credable & MC Stiffler', 'Garage / Bass', 'Fri', '17:30-18:30', 'Lemon Lounge'),
    ('SETWUN', 'Electronic', 'Thu', '14:00-14:40', 'Lush Life'),
    ('Shackleton (Live)', 'Dub-techno', 'Sat', '22:00-23:00', 'The Grove'),
    ('Ehua', 'Afro-house', 'Thu', '20:30-22:00', 'The Grove'),
    ('Toribio', 'House / Disco', 'Thu', '17:30-19:00', 'The Bowl'),
    ('Glenn Underground', 'House', 'Thu', '22:00-00:00', 'The Bowl'),
    ('Nightmares on Wax b2b Trojan Sound System b2b Daddy G', 'Dub / Downtempo', 'Thu', '20:00-00:00', "Love Dancin'"),
    ('AliA', 'Eclectic / UK Bass', 'Thu', '19:30-20:30', 'Lemon Lounge'),
    ('Giles Smith & Alexander Nut', 'Broken Beat / Eclectic', 'Thu', '20:00-22:30', 'Roller Rink'),
    ('Atjazz', 'House', 'Thu', '22:30-00:00', 'Roller Rink'),
    ('re:ni', 'Techno', 'Sat', '23:00-01:00', 'The Grove'),
    ('V.I.V.E.K', 'Dub', 'Thu', '16:00-17:30', 'Carhartt WIP'),
    ('Introspekt', 'Techno', 'Thu', '19:00-20:30', 'Carhartt WIP'),
    ('Alexander Nut', 'Broken Beat / Eclectic', 'Sat', '14:00-15:00', 'Lemon Lounge'),
    ('Alix Perez ft SP:MC', 'Drum & Bass', 'Sat', '22:30-00:00', 'Rhythm Corner'),
    ('Beatrice M. & AliA', 'Dubstep / UK Bass', 'Fri', '19:00-21:30', 'The Bowl'),
    ('Bryan Gee (Old Skool Set)', 'Jungle / Drum & Bass', 'Sun', '20:30-22:00', 'The Grove'),
    ('Calibre ft SP:MC', 'Drum & Bass', 'Sat', '00:00-02:00', 'Rhythm Corner'),
    ('Charlie Dark', 'Broken Beat / Eclectic', 'Sun', '13:00-14:50', 'The Bowl'),
    ('Coco Maria', 'Global / Eclectic', 'Sat', '16:00-17:00', 'Lemon Lounge'),
    ("Colleen 'Cosmo' Murphy", 'Disco / House', 'Sat', '23:00-01:30', "Love Dancin'"),
    ('Cosmo Sofi', 'House / Disco', 'Sat', '23:00-00:30', 'Roller Rink'),
    ('dBridge', 'Drum & Bass / Halftime', 'Sun', '23:00-00:00', 'The Grove'),
    ('Dom Servini', 'Broken Beat / Eclectic', 'Fri', '00:00-01:00', 'Near Mint Record Store'),
    ('Double O', 'Jungle / Drum & Bass', 'Sun', '19:30-20:30', 'The Grove'),
    ('Dr Banana', 'House / Disco', 'Sun', '15:30-17:15', 'Rhythm Corner'),
    ('Lev & Faro', 'House / Disco', 'Sat', '21:30-23:00', 'The Bowl'),
    ('DJ Flight', 'Jungle / Drum & Bass', 'Sat', '19:00-21:00', 'Rhythm Corner'),
    ('Guedra Guedra', 'North African club', 'Sat', '00:30-02:00', 'Carhartt WIP'),
    ('Iration Steppas', 'Dub / Steppers', 'Fri', '15:00-17:00', 'The Bowl'),
    ('IZCO', 'Garage / Dub', 'Sat', '00:00-02:00', 'Brawnswood'),
    ('Jamz Supernova', 'Broken Beat / Global bass', 'Thu', '22:30-00:00', 'Rhythm Corner'),
    ('JKriv', 'Disco / House', 'Sat', '00:30-02:00', 'Roller Rink'),
    ('Josey Rebelle', 'Techno / House', 'Fri', '23:00-00:30', 'The Bowl'),
    ('Facta & K-Lone', 'UK Bass / Garage', 'Fri', '00:30-02:30', 'The Bowl'),
    ('Yushh', 'UK Bass / Techno', 'Fri', '22:00-23:00', 'Lemon Lounge'),
    ('Kenny Dope', 'House', 'Fri', '00:30-02:30', 'The Grove'),
    ('King Britt', 'House / Disco / Techno', 'Sat', '17:00-20:00', 'The Bowl'),
    ('Lovie', 'House / Disco', 'Sun', '14:50-16:10', 'The Bowl'),
    ('Luke Una', 'House / Balearic', 'Fri', '01:00-04:00', 'Rhythm Corner'),
    ('Mantra', 'Jungle / Drum & Bass', 'Sun', '22:00-23:00', 'The Grove'),
    ('Marcia Carr', 'Dancehall / Bass', 'Fri', '17:30-19:00', 'Rhythm Corner'),
    ('Mr. Disco Kid', 'Disco', 'Fri', '01:00-03:00', 'Roller Rink'),
    ('Mr Scruff, DJ Spinna & Vanessa Freeman', 'House / Breaks / Eclectic', 'Fri', '15:00-21:00', "Love Dancin'"),
    ('Nightmares On Wax', 'Downtempo / House', 'Fri', '19:00-20:30', 'Rhythm Corner'),
    ('Nono Gigsta', 'Genre-warping (jungle/house/dub)', 'Sat', '02:00-04:00', 'The Grove'),
    ('Palms Trax', 'House', 'Fri', '23:00-01:00', 'Rhythm Corner'),
    ('Pariah', 'Techno / Bass', 'Fri', '21:30-23:00', 'The Bowl'),
    ('DJ Perception', 'UK Garage', 'Fri', '23:00-00:30', "Tomorrow's Warriors Big Top"),
    ('Poly-Ritmo', 'Afro-Latin club', 'Sat', '15:00-17:00', "Love Dancin'"),
    ('Ruby Savage', 'Disco / House', 'Sun', '18:00-20:00', 'Beat Hotel x Ilegal Mezcal'),
    ('Sadar Bahar', 'Disco / House digger', 'Sat', '02:00-04:00', 'The Bowl'),
    ('Salute', 'UK Bass / Broken Beat', 'Sun', '19:00-21:00', 'Rhythm Corner'),
    ('Shy One', 'Eclectic / Broken Beat', 'Fri', '00:30-02:30', "Love Dancin'"),
    ('Tama Sumo & Lakuti', 'House / Techno', 'Fri', '20:30-23:00', 'Rhythm Corner'),
    ('Tasha', 'Drum & Bass / Techno', 'Fri', '02:30-04:00', 'The Bowl'),
    ('Tone B Nimble', 'Broken Beat', 'Sun', '16:10-17:40', 'The Bowl'),
    ('Trafford (Nick Williams memorial set)', 'House / Disco', 'Sat', '13:00-15:00', "Love Dancin'"),
    ('Wookie', 'UK Garage', 'Fri', '02:00-04:00', "Tomorrow's Warriors Big Top"),
    ('Yoofee', 'Jazz / Electronic', 'Fri', '15:00-16:00', 'Rhythm Corner'),
    ('rRoxymore', 'Techno / House', 'Sat', '02:00-04:00', "Tomorrow's Warriors Big Top"),
    ('Ivy Lab', 'Bass / Halftime', 'Sat', '02:00-04:00', 'Rhythm Corner'),
    ('I-Sha', 'Experimental electronic', 'Sat', '20:00-22:00', 'The Grove'),
    ('Silva Snipa', 'Jungle / Drum & Bass', 'Sat', '21:00-22:30', 'Rhythm Corner'),
    ('Ceephax Acid Crew (Live)', 'Acid techno', 'Sat', '21:30-23:00', 'Lemon Lounge'),
    ('Mad Professor', 'Dub', 'Sun', '22:30-00:00', 'The Bowl'),
    ('DJ Lag', 'Gqom', 'Sat', '23:00-00:30', 'Carhartt WIP'),
    ('Channel One', 'Dub / Reggae soundsystem', 'Fri', '13:00-15:00', 'The Bowl'),
    ('Gilles Peterson', 'Eclectic / Global', 'Fri', '11:00-13:00', 'The Bowl'),
    ('Emma-Jean Thackray', 'Jazz-electronic', 'Sun', '19:40-21:00', 'The Bowl'),
    ('Greg Wilson', 'Disco / Electro', 'Sun', '20:30-22:00', 'Roller Rink'),
    ('Winston Hazel & Josey Rebelle', 'House / Techno', 'Sun', '18:00-19:30', 'The Grove'),
    ("Another Sunday Afternoon At Dingwall's", 'Eclectic / Balearic', 'Sun', '11:00-00:00', "Love Dancin'"),
    ('Esa', 'Afro-house / Techno', 'Sat', '20:00-22:00', 'Beat Hotel x Ilegal Mezcal'),
    ('Anz b2b Commodo', 'UK Bass / Club', 'Thu', '22:00-00:00', 'Carhartt WIP'),
    ('DJ Plead', 'Percussive club / Lebanese', 'Thu', '22:00-23:00', 'Lemon Lounge'),
    ('Wheel Up', 'Broken Beat / Bruk', 'Sun', '21:30-22:30', 'Near Mint Record Store'),
    ('Pamoja Disco Club', 'Disco / House / Global', 'Sun', '22:00-23:00', 'Once In A Blue Moon'),
    ('Juls', 'Afrobeats / Highlife', 'Thu', '20:30-22:30', 'Rhythm Corner'),
]

SOUL_JAZZ = [
    ('LOWXND', 'Jazz / Live bass', 'Fri', '15:20-16:00', "Tomorrow's Warriors Big Top"),
    ('Gary Bartz', 'Jazz', 'Sun', '21:15-22:30', 'Main Stage'),
    ('Joy Crookes', 'Soul', 'Fri', '19:50-20:50', 'Main Stage'),
    ('Stereolab', 'Live / Alt', 'Sun', '19:30-20:30', 'Main Stage'),
    ('Digable Planets', 'Hip-hop', 'Thu', '19:20-20:30', 'Main Stage'),
    ('Shabaka', 'Jazz', 'Sun', '15:50-16:40', 'Lush Life'),
    ('Kofi Stone', 'UK Rap / Soul', 'Sat', '20:30-21:30', 'Lush Life'),
    ('Sampa The Great', 'Hip-hop / Soul', 'Fri', '19:10-20:00', 'Lush Life'),
    ('Mike', 'Underground hip-hop', 'Sat', '18:50-19:50', 'Lush Life'),
    ('Aja Monet', 'Poet / Soul', 'Sat', '15:40-16:30', 'Lush Life'),
    ('Yukimi', 'Soul-pop', 'Fri', '17:30-18:20', 'Lush Life'),
    ('james K', 'Experimental pop', 'Sun', '19:00-19:50', 'Lush Life'),
    ('Corto.Alto', 'Jazz-funk', 'Fri', '16:40-17:30', 'Main Stage'),
    ('Yazmin Lacey', 'Soul', 'Sun', '20:30-21:30', 'Lush Life'),
    ('John Glacier', 'Alt hip-hop', 'Fri', '16:00-16:50', 'Lush Life'),
    ('Butcher Brown', 'Funk / Jazz band', 'Thu', '17:30-18:30', 'Main Stage'),
    ('Cleo Reed', 'Jazz-soul', 'Fri', '13:25-14:15', 'Main Stage'),
    ('Amaro Freitas', 'Jazz piano', 'Sat', '12:00-12:50', 'Main Stage'),
    ("Kahil El'Zabar presents A Love Supreme", 'Jazz', 'Sun', '18:00-19:00', 'Main Stage'),
    ('Anaiis', 'Soul / Alt', 'Fri', '18:10-19:10', 'Main Stage'),
    ('Gena feat Liv.e & Karriem Riggins', 'Hip-hop / Jazz', 'Sat', '17:00-18:00', 'Lush Life'),
    ('The Heliocentrics', 'Psych-funk-jazz', 'Fri', '14:10-15:10', 'Lush Life'),
    ('Momoko Gill', 'Jazz-soul vocalist', 'Sat', '13:30-14:20', 'Main Stage'),
    ('Rogê', 'Brazilian soul', 'Fri', '22:20-23:00', 'Lush Life'),
    ('Bel Cobain', 'Soul / R&B', 'Fri', '12:20-13:00', 'Main Stage'),
    ('The Zawose Queens', 'Tanzanian / Global', 'Thu', '14:40-15:30', 'Main Stage'),
    ('Ana Frango Elétrico', 'Brazilian pop', 'Sun', '16:30-17:30', 'Main Stage'),
    ('Natural Information Society', 'Minimalist jazz', 'Sun', '14:20-15:10', 'Lush Life'),
    ('Joshua Idehen', 'Poet / Jazz', 'Sun', '13:30-14:30', 'Main Stage'),
    ('Speakers Corner Quartet: The Music of Arthur Russell', 'Experimental / Classical', 'Thu', '18:20-19:20', 'Lush Life'),
    ("Dave Okumu presents DVTN: A Prayer for D'Angelo", 'Soul tribute', 'Fri', '14:50-16:00', 'Main Stage'),
    ('Cara O Sextet', 'Jazz sextet', 'Sat', '12:35-13:15', "Tomorrow's Warriors Big Top"),
    ('Cube Legacy Band', 'Jazz', 'Sat', '16:20-17:05', "Tomorrow's Warriors Big Top"),
    ('Femi Koleoso', 'Jazz / DJ crossover', 'Thu', '18:30-20:30', 'Rhythm Corner'),
    ('Peven Everett', 'Soulful house vocalist (live)', 'Sat', '21:40-22:50', 'Main Stage'),
    ('SALIMATA', 'Rap / Poet', 'Sat', '22:20-23:00', "Tomorrow's Warriors Big Top"),
    ('Steam Down', 'Jazz collective', 'Sat', '14:10-15:00', 'Lush Life'),
    ('Thundercat', 'Funk / Jazz-fusion', 'Fri', '21:40-22:50', 'Main Stage'),
    ('Tom Skinner', 'Jazz drummer', 'Thu', '16:00-16:50', 'Main Stage'),
    ("Your Brother's Keeper & Gary Bartz", 'Jazz collab', 'Sat', '20:00-21:00', 'Brawnswood'),
    ('Zena x Mereba x Kibrom Birhane', 'Soul / Global', 'Sun', '15:00-16:00', 'Main Stage'),
    ('Ge-ology', 'Hip-hop crate-digger', 'Sat', '23:00-02:00', 'The Bowl'),
    ('DJ Spanish Fly (Live)', 'Memphis rap pioneer', 'Sat', '19:30-20:30', 'Lemon Lounge'),
    ('Elliott Skinner', 'Soul (Ninja Tune)', 'Sat', '21:00-21:55', "Tomorrow's Warriors Big Top"),
    ('Olive Jones', 'Jazz vocalist', 'Fri', '12:50-13:30', 'Lush Life'),
    ('Dave Okumu & Tom Skinner', 'Jazz', 'Sat', '13:00-14:00', 'Brawnswood'),
    ('Marina & Yazmin Lacey', 'Soul', 'Sat', '21:00-22:30', 'Brawnswood'),
    ('Arthur Verocai with Nu Civilisation Orchestra', 'Orchestral / Brazilian', 'Sat', '19:40-21:00', 'Main Stage'),
    ('Klara Devlin', "Tomorrow's Warriors showcase", 'Sat', '13:40-14:20', "Tomorrow's Warriors Big Top"),
    ('BXL x LDN Interplay III', "Tomorrow's Warriors showcase", 'Sat', '14:50-15:50', "Tomorrow's Warriors Big Top"),
    ('Kassa GJ Quartet', "Tomorrow's Warriors showcase", 'Sat', '17:30-18:15', "Tomorrow's Warriors Big Top"),
    ('Mali Sheard', "Tomorrow's Warriors showcase", 'Sat', '18:45-19:30', "Tomorrow's Warriors Big Top"),
    ('Finka', "Tomorrow's Warriors showcase", 'Fri', '12:20-12:50', "Tomorrow's Warriors Big Top"),
    ('Holly Reinhardt', "Tomorrow's Warriors showcase", 'Fri', '14:15-14:55', "Tomorrow's Warriors Big Top"),
    ('Jobsearch', "Tomorrow's Warriors showcase", 'Fri', '17:35-18:15', "Tomorrow's Warriors Big Top"),
    ('Plumm', "Tomorrow's Warriors showcase", 'Fri', '19:50-20:40', "Tomorrow's Warriors Big Top"),
    ('Knats', "Tomorrow's Warriors showcase", 'Fri', '21:00-21:45', "Tomorrow's Warriors Big Top"),
    ('afromerm', 'Electronic / Live', 'Sat', '11:00-12:00', 'Lemon Lounge'),
]

NOTE = ("This is a hand-picked selection, not the full programme. The official schedule has 565 sets "
        "across 18 stages and we list 143 of them, so treat this as a shortlist for deciding who to "
        "listen to, and the festival's own set-times page as the authority on where to stand. Four "
        "stages are missing entirely (Once In A Blue Moon, Worldwide FM presents: WOH Radio, "
        "Love-Serve Bar, Passenger Presents: Ground Tempo) and the stages that are here are not "
        "complete either. Every day, time and stage below was checked against the official set times "
        "on 15 Aug 2026 and all 143 agree; run verify.py to recheck, because the festival does move "
        "things. The lists show one slot per artist, but click any name for the festival's own "
        "write-up and every set that artist plays, which for 31 of them is more than one. Genres "
        "are our own shorthand for filtering rather than anything official, so treat them as a "
        "rough steer and read the write-up if it matters.")
