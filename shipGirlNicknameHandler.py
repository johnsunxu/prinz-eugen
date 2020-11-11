def getNickname(arg):
    nicknameDic = {
        "fdg" : "Friedrich der Große",
        "bad" : "Izumo",
        "warcorgi" : "Warspite",
        "warpoi" : "Warspite",
        "nanoda" : "Yukikaze",
        "yuki" : "Yukikaze",
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
        "hipper" : "Admiral Hipper",
        "hipper muse" : "Admiral Hipper µ",
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
        "pamiat" : "Pamiat Merkuria",
        "rossiya" : "Sovetskaya Rossiya",
        "kaga (bb)" : "Kaga (Battleship)",
        "kaga bb" : "Kaga (Battleship)",
        "jb" : "Jean Bart",
        "desuland" : "Deutschland",
        "richy" : "Richelieu",
        "formi" : "Formidable",
        "sheffy" : "Sheffield",
        "hms neptune" : "Neptune",
        "maki" : "Makinami"


    }

    #if answer is a nickname, replace answer with ship it is referencing.
    if arg in nicknameDic:
        arg = nicknameDic[arg].lower();

    return arg;
