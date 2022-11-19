import re
from sort_themes import sort_themes

# ===================== Regex =====================
r_in_angle = r"(?<=<)(.*?)(?=>)"
def r_in_square(text): return r"(?<=\[" + text + r"\])(.*?)(?=\n)"

# ===================== List handlers =====================
def theme_list_handler(_, genres):
    print(text_themes_en)
    for index,theme in enumerate(text_themes_en):
        for genre_id in re.findall(r_in_angle, text_themes_ge[index]):
            if genre_id.find("M") == -1: #M1, M2 and M3 are age rating modifiers, which we don't include in the guide
                if "THEMES" not in genres[int(genre_id)]:
                    genres[int(genre_id)]["THEMES"] = []
                genres[int(genre_id)]["THEMES"].append(theme)
    for genre in genres:
        print(genre)
        genre["THEMES"] = ", ".join(genre["THEMES"])
    return None

def tgroup_list_handler(genre, genres):
    text = ""
    for group in genre["TGROUP"]:
        text += group.replace("KID", "Children").replace("TEEN", "Teenagers").replace("ADULT", "Adults").replace("OLD", "Seniors") + ", "
    if len(genre["TGROUP"]) == 4:
        text += "All"
    else:
        text = text[:-2]
    return text

def subgenre_list_handler(genre, genres):
    text = ""
    for group in genre["GENRE COMB"]:
        text += genres[int(group)]["NAME EN"] + ", "
    text = text[:-2]
    return text

# ===================== Genre parameters =====================
genre_params = [
    {"name": "NAME EN",    "list": False,},
    {"name": "DATE",       "list": False,},
    {"name": "THEMES",     "list": True, "list_handler": theme_list_handler,},
    {"name": "TGROUP",     "list": True, "list_handler": tgroup_list_handler,},
    {"name": "GENRE COMB", "list": True, "list_handler": subgenre_list_handler,},
    {"name": "FOCUS0",     "list": False,},
    {"name": "FOCUS1",     "list": False,},
    {"name": "FOCUS2",     "list": False,},
    {"name": "FOCUS3",     "list": False,},
    {"name": "FOCUS4",     "list": False,},
    {"name": "FOCUS5",     "list": False,},
    {"name": "FOCUS6",     "list": False,},
    {"name": "FOCUS7",     "list": False,},
    {"name": "ALIGN0",     "list": False,},
    {"name": "ALIGN1",     "list": False,},
    {"name": "ALIGN2",     "list": False,},
    {"name": "GAMEPLAY",   "list": False,},
    {"name": "GRAPHIC",    "list": False,},
    {"name": "SOUND",      "list": False,},
    {"name": "CONTROL",    "list": False,},
]

# ===================== Code itself =====================
if __name__ == "__main__":
    # Sorting lists to use later
    text_themes_en, text_themes_ge = sort_themes()

    # Reading all the required files
    with open("genres.txt", "r", encoding='utf-8', errors='ignore') as file:
        text_genres = file.read()

    genres = []
    # creating spots where all the genres will go
    for id in re.findall(r_in_square("ID"), text_genres):
        genres.insert(int(id), {})

    # filling the list by going through all possible params and adding them to genres
    for param in genre_params:
        # getting param
        values = re.findall(r_in_square(param['name']), text_genres)
        # if param is empty, we fill the whole list with ""
        if len(values) == 0:
            values = [""] * len(genres)
        # start going through all genres
        for index,genre in enumerate(genres):
            # if param is a list, we call its list_handler
            if (param['list']):
                genre[param['name']] = re.findall(r_in_angle, values[index])
                result = param['list_handler'](genre, genres)
                # if handler doesn't return anything, then it means it filled the whole list itself
                if result == None:
                    break
                genre[param['name']] = result
            else:
                genre[param['name']] = values[index]

    groups = [
        {"group": "Game info", "data":         [{"name": "DATE",       "desc": "Unlocks",},
                                                {"name": "THEMES",     "desc": "Themes",},
                                                {"name": "TGROUP",     "desc": "Target Audience",},
                                                {"name": "GENRE COMB", "desc": "Supporting Genres",}]},
        {"group": "Design focus", "data":      [{"name": "FOCUS0",     "desc": "Game length",},
                                                {"name": "FOCUS1",     "desc": "Game depth",},
                                                {"name": "FOCUS2",     "desc": "Beginner friendliness",},
                                                {"name": "FOCUS3",     "desc": "Innovation",},
                                                {"name": "FOCUS4",     "desc": "Story",},
                                                {"name": "FOCUS5",     "desc": "Character Design",},
                                                {"name": "FOCUS6",     "desc": "Level Design",},
                                                {"name": "FOCUS7",     "desc": "Mission design",}]},
        {"group": "Design direction", "data":  [{"name": "ALIGN0",     "desc": "Core/Casual",},
                                                {"name": "ALIGN1",     "desc": "Violence",},
                                                {"name": "ALIGN2",     "desc": "Easy/Hard",}]},
        {"group": "Design Priority", "data":   [{"name": "GAMEPLAY",   "desc": "Gameplay",},
                                                {"name": "GRAPHIC",    "desc": "Graphic",},
                                                {"name": "SOUND",      "desc": "Sound",},
                                                {"name": "CONTROL",    "desc": "Technics",}]},
    ]

    for genre in genres:
        print("----------------{}--------------------".format(genre["NAME EN"]))
        toPrint = ""
        for group in groups:
            toPrint += '[table][tr][th]{}[/th][th][/th][/tr]'.format(group["group"])
            for i in group["data"]:
                toPrint += '[tr][th]{}[/th][td]{}[/td][/tr]'.format(i["desc"], genre[i["name"]])
            toPrint += '[/table]\n\n'
        print(toPrint)
        input()