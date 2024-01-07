import numpy as np


# OPTIONS

# Name of the Inn, appears in the title
inn_name = "The Cool Testers Inn"
# Inn Quality, sets the prize range can be 0 (cheap), 1 (moderate) or 2 (expensive)
inn_quality = 2
# How many snack options are included on the menu
snack_options = 5
# How many main options are included on the menu
main_options = 6
# How many veggie options are included on the menu
veg_options = 4
# How many desserts are included on the menu
dessert_options = 4
# How many drinks, in addition to "house wine" are included on the menu
drinks_options = 9
# should maritime food options be included
inclued_maritime_options = True
# only if maritime options are included: should normal options be excluded?
exclude_normal_options = True

#-------------------------------------------------------------------------------------------------------------------------------------

DOCUMENT_STR = """\\documentclass[letterpaper,openany,nodeprecatedcode, 14pt]{dndbook}


\\usepackage[english]{babel}
% For further options (multilanguage documents, hypenations, language environments...)
% please refer to babel/polyglossia's documentation.

\\usepackage[utf8]{inputenc}
\\usepackage[singlelinecheck=false]{caption}
\\usepackage{lipsum}
\\usepackage{listings}
\\usepackage{shortvrb}
\\usepackage{stfloats}
\\usepackage{tabularx}
\\usepackage{fancyhdr}
\\MakeShortVerb{|}

\\newcolumntype{b}{>{\\large\\raggedleft\\arraybackslash\hsize=.5\\hsize}X}
\\newcolumntype{s}{>{\large\\raggedright\\arraybackslash\hsize=1.5\\hsize}X}
\\newcolumntype{j}{>{\large\\raggedright\\arraybackslash\hsize=1\\hsize}X}
\\newcolumntype{k}{>{\large\\raggedleft\\arraybackslash\hsize=.5\\hsize}X}

%% Commands for food and drinks
%%
% Food: command example use \\foodEntry{foodName}{foodPrice}
\\newcommand{\\foodEntry}[2]{ #1 & #2 \\\\ \\noalign{\\vspace{4pt}} }
% Drinks: command example use \\drinkEntry{drinkName}{sizeName1}{price1}{sizeName2}{price2}
\\newcommand{\\drinkEntry}[5]{ #1 & #2 & #3 \\\\ & #4 & #5 \\\\ \\noalign{\\vspace{4pt}} }

\\lstset{%
  basicstyle=\\ttfamily,
  language=[LaTeX]{TeX},
  breaklines=true,
}

\\begin{document}
\\chapter*{:InnName}
\\section{Menu}

\\subsection{}

\\subsection{Mains}
\\noindent
\\begin{tabularx}{\\textwidth}{ s b }
:FoodEntries
\\end{tabularx}

\\vspace{0.5mm}

\\subsection{}
\\subsection{Drinks}


\\begin{tabularx}{\\textwidth}{ j k b }
:DrinkEntries
\\end{tabularx}


\\fancyfoot{} 
\\fancyfoot[LE,RO]{Tap water caraffe for free.}
\\fancyfoot[LO,CE]{All products are collected fresh from the region.}
\\end{document}
"""

class menu_item:
    
    def __init__(self) -> None:
        self.name = "" #Menu Item Name
        self.prize = 2 #menu ITem prize in SP

    def __init__(self, name, prize) -> None:
        self.name = name
        self.prize = round(prize,1)
        
    def _get_prize_str(self):
        if self.prize < 1:
            return f"{self.prize * 10} CP"
        elif self.prize > 10:
            return f"{round(self.prize / 10, 1)} GP"
        else:
            return f"{self.prize} SP"

    #prints latex version of this menu item
    def print(self):
        return f"\\foodEntry{chr(123)}{self.name}{chr(125)}{chr(123)}{self._get_prize_str()}{chr(125)}"

class food_item(menu_item):
    def __init__(self, name, sides, prize) -> None:
        super().__init__(name, prize)
        self.sides = sides

    def _get_sides_str(self):
        if len(self.sides) > 1:
            sides_str = ", ".join(self.sides[:-1])
            sides_str += f" and {self.sides[-1]}"
        else:
            sides_str = self.sides[0]
        return sides_str

    def print(self):
        name_str =  f"{self.name} served with {self._get_sides_str()}"
        return f"\\foodEntry{chr(123)}{name_str}{chr(125)}{chr(123)}{self._get_prize_str()}{chr(125)}"

class drink_item(menu_item):
    def __init__(self, name, prize) -> None:
        super().__init__(name, prize)

    def _get_cup_prize_str(self):
        if self.prize < 1:
            return f"{self.prize * 10} CP"
        elif self.prize > 10:
            return f"{round(self.prize / 10, 1)} GP"
        else:
            return f"{self.prize} SP"
        
    def _get_bottle_prize_str(self):
        old_prize = self.prize
        self.prize = self.prize * np.random.randint(4,6)
        pr_str = self._get_cup_prize_str()
        self.prize = old_prize
        return pr_str

    def print(self):
        return f"\\drinkEntry{chr(123)}{self.name}{chr(125)}{chr(123)}Cup{chr(125)}{chr(123)}{self._get_cup_prize_str()}{chr(125)}{chr(123)}Jug{chr(125)}{chr(123)}{self._get_bottle_prize_str()}{chr(125)}"

#reads a table at the given file path and returns an array
#assumes table entries are in the form: No. ITEM_NAME: ITEM_DESC
def read_table(file_path):
    items = []

    with open(file_path, 'r') as file:
        for line in file:
            item, bp = line.strip().split(";")
            items.append({'item': item, "bp": int(bp)})

    return items

#returns a randomly generated tavern name
def generate_tavern_name():
    pass

#generates a random entry on a menu from the tables read
def generate_food_item(main, sides, pm):
        prize = np.average([main['bp']] + [p['bp'] for p in sides]) + 1.5*pm + 0.5 + 0.1 * len(sides) + np.random.rand()
        sides_names = [item['item'] for item in sides]
        name_str = f"{main['item']}"
        return food_item(name_str,sides_names, prize)

#generates food menu
def generate_food_menu(bp, snack_size, main_size, veg_size, dessert_size):
    main_options = np.random.choice([main for main in mains if main['bp'] <= bp], size=main_size - veg_size, replace=False).tolist()
    main_options += np.random.choice([main for main in veg_mains if main['bp'] <= bp], size=veg_size, replace=False).tolist()
    menu = []
    snack_options = np.random.choice([main for main in snacks if main['bp'] <= bp], size=snack_size, replace=False).tolist()
    for snack in snack_options:
        menu.append( menu_item(snack['item'], bp + 0.5 + np.random.rand()))
    for main in main_options:
        poss_sides = [side for side in sides if side['bp'] <= main['bp'] or np.random.random() > 0.7]
        chos_sides = np.random.choice(poss_sides, size=np.random.randint(1,4), replace=False)
        menu.append( generate_food_item(main, chos_sides, bp))
    desert_options = np.random.choice([main for main in deserts if main['bp'] <= bp], size=dessert_size, replace=False).tolist()
    for desert in desert_options:
        menu.append( menu_item(desert['item'], bp + 0.5 + np.random.rand()))
    return menu

#generates food menu
def generate_drinks_menu(bp, drikns_size):
    drikns_options = np.random.choice([main for main in drinks if main['bp'] <= bp], size=drikns_size, replace=False).tolist()
    house_prize = (0.5+3*bp + np.random.rand()) / 5
    menu = [drink_item("House Wine", house_prize) ]
    for drink in drikns_options:
        prize = (0.5+3*bp+drink['bp'] + np.random.rand()) / 5
        menu.append( drink_item(drink['item'], prize) )
    return menu

#writes the latex file based on the input (input tbd)
def write_tex(fmenu, dmenu):
    fstrs = [item.print().replace("&", "\\&") for item in fmenu]
    dstrs = [item.print().replace("&", "\\&") for item in dmenu]
    output_str = DOCUMENT_STR.replace(":FoodEntries", "\n".join(fstrs))
    output_str = output_str.replace(":DrinkEntries", "\n".join(dstrs))
    output_str = output_str.replace(":InnName", inn_name)
    f = open("MenuMaker.tex", "a")
    f.write(output_str)
    f.close()

#calls pdflatex via OS module to render the latex file at the given path
def render_tex(file_path):
    import os
    print("Compiling PDF from tex... (this can take a couple of seconnds)")
    print(file_path)
    os.system("pdflatex "+file_path+".tex")
    os.system("pdflatex "+file_path+".tex >/dev/null 2>&1")
    print("Cleaning up output files...")
    os.system("mv "+file_path+".pdf "+inn_name.replace(" ", "_")+".pdf")
    os.system("mv "+file_path+".tex "+inn_name.replace(" ", "_")+".tex")
    os.system("rm -rf " + file_path + ".*")
    print("Done!")

mains = []
if not (exclude_normal_options and inclued_maritime_options): mains += read_table("./Tables/Main_Meat.txt")
if inclued_maritime_options: mains += read_table("./Tables/Mains_Maritime.txt")
veg_mains = read_table("./Tables/Mains_Veggie.txt")
snacks = read_table("./Tables/Snacks.txt")
deserts = read_table("./Tables/Deserts.txt")
drinks = read_table("./Tables/Drinks.txt")
sides = []
if not (exclude_normal_options and inclued_maritime_options): sides += read_table("./Tables/Sides_General.txt")
if inclued_maritime_options: sides += read_table("./Tables/Sides_Maritime.txt")

menu = generate_food_menu(inn_quality, snack_options, main_options, veg_options, dessert_options)
drinks_menu = generate_drinks_menu(inn_quality, drinks_options)
write_tex(menu, drinks_menu)
render_tex("./MenuMaker")