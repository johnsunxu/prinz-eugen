# This file is part of Prinz Eugen.

# Prinz Eugen is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# Prinz Eugen is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with Prinz
# Eugen. If not, see <https://www.gnu.org/licenses/>.

nicknames = {
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
    "pamiat merkuria" : "Pamiat' Merkuria",
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

    #Duca pepelaugh
    'abruzzi' : "Duca degli Abruzzi",
    'duca' : "Duca degli Abruzzi",
    'luigi' : "Duca degli Abruzzi",
    'dda' : "Duca degli Abruzzi",
    'luigi di savoia duca degli abruzzi' : "Duca degli Abruzzi",
    'a literal page worth of aliases' : "Duca degli Abruzzi",

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
    "admiral hipper muse" : "Admiral Hipper μ",
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

def getNickname(arg):
    #if answer is a nickname, replace answer with ship it is referencing.
    if arg.lower() in nicknames:
        arg = nicknames[arg.lower()]

    return arg
