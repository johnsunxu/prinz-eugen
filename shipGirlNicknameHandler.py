def getNickname(arg):
    nicknameDic = {
        "fdg" : "Friedrich der Große",
        "freddy" : "Friedrich der Große",
        "bad" : "Izumo",
        "warcorgi" : "Warspite",
        "warpoi" : "Warspite",
        "nanoda" : "Yukikaze",
        "yuki" : "Yukikaze",
        "ykkz" : "Yukikaze",
        "graf" : "Graf Zeppelin",
        "enty" : "Enterprise",
        "owari da" : "Enterprise",
        "st louis" : "St. louis",
        "sanrui" : "Saint Louis",
        "jesus" : "Juneau",
        "sandy" : "San Diego",
        "bisko" : "Bismarck",
        "bisco" : "Bismarck",
        "kgv" : "King George V",
        "clevebro" : "Cleveland",
        "pow" : "Prince of Wales",
        "doy" : "Duke of York",
        "qe" : "Queen Elizabeth",
        "bulin" : "Universal Bulin",
        "purin" : "Prototype Bulin MKII",
        "urin" : "Specialized Bulin Custom MKIII",
        "ur bulin" : "Specialized Bulin Custom MKIII",
        "rainbow bulin" : "Specialized Bulin Custom MKIII",
        "hipper" : "Admiral Hipper",
        "hipper muse" : "Admiral Hipper μ",
        "spee" : "Graf Spee",
        "indy" : "Indianapolis",
        "177013" : "Marblehead",
        'prinz' : "Prinz Eugen",
        'sara' : "Saratoga",
        'iroha' : "I-168",
        "lolicon" : "Ark Royal",
        "massa" : "Massachusetts",
        "poi" : "Yuudachi",
        "lusty" : "Illustrious",
        "ayaya" : "Ayanami",
        "nimi" : "Z23",
        "monty" : "Montpelier",
        "pamiat" : "Pamiat' Merkuria",
        "rossiya" : "Sovetskaya Rossiya",
        "kaga (bb)" : "Kaga(BB)",
        "kaga bb" : "Kaga(BB)",
        "jb" : "Jean Bart",
        "desuland" : "Deutschland",
        "richy" : "Richelieu",
        "formi" : "Formidable",
        "sheffy" : "Sheffield",
        "hms neptune" : "Neptune",
        "maki" : "Makinami",
        "sodak" : "South Dakota",
        "<:roon_seal:773751304861253662>" : "Roon μ",
        "biscuit" : "Bismarck",
        "spee" : "Admiral Graf Spee",
        "suzu" : "Suzutsuki",
        'balti' : "Baltimore",
        'duca' : "Duca degli Abruzzi",
        'vv' : "Vittorio Veneto",
        'veneto' : "Vittorio Veneto",

        #german ships
        "konigsberg" : "Königsberg",
        "koln" : "Köln",
        "nurnberg" : "Nürnberg",

        #french ships
        "algerie" : "Algérie",
        "la galissonniere" : "La Galissonnière",
        "l'opiniatre" : "L'Opiniâtre",
        "le Temeraire" : "Le Téméraire",
        "emile bertin" : "Émile Bertin",

        #muse ships
        "roon muse" : "Roon μ",
        "ruse": "Roon μ",
        "gascogne muse" : "Gascogne μ",
        "cleveland muse" : "Cleveland μ",
        "admiral Hipper muse" : "Admiral Hipper μ",
        "akagi muse" : "Akagi μ",
        "sheffield muse" : "Sheffield μ",
        "illustrious muse" : "Illustrious μ",
        "le malin muse" : "Le Malin μ",
        "dido muse" : "Dido μ",
        "taihou muse" : "Taihou μ",
        "tashkent muse" : "Tashkent μ",
        "albacore muse" : "Albacore μ",
        "baltimore muse" : "Baltimore μ",
        "balti muse" : "Baltimore μ"




    }

    #if answer is a nickname, replace answer with ship it is referencing.
    if arg in nicknameDic:
        arg = nicknameDic[arg].lower();

    return arg;
