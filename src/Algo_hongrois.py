"""

Argument pour dev :

[[65,73,63,57],[67,70,65,58],[68,72,69,55],[67,75,70,59],[71,69,75,57],[69,71,66,59]]
Dos Brasse Papillon Libre
Nageur1 Nageur2 Nageur3 Nageur4 Nageur5 Nageur6

"""


def print_latex(table, colName, lineName, lineZero, colZero, file):
    largeur = len(table[0])
    format = "|c|"
    for x in range(largeur):
        format = format + "c|"

    file.write("\\begin{center}\n")
    file.write("\\begin{tabular}{"+format+"}\n")
    file.write("\\hline\n")
    colNameLatex = ""
    for x in range(len(colName)):
        if x in colZero:
            colNameLatex = colNameLatex + "&\\color{red}" + colName[x]
            continue
        colNameLatex = colNameLatex + "&" + colName[x]
    colNameLatex = colNameLatex + "\\\\"
    file.write(colNameLatex+"\n")
    file.write("\\hline\n")
    for x in range(len(lineName)):
        if x in lineZero:
            line = "\\color{red}" + lineName[x]
        else:
            line = "" + lineName[x]
        for y in range(largeur):
            if x in lineZero or y in colZero:
                line = line + "&\\color{red}" + str(table[x][y])
                continue
            line = line + "&" + str(table[x][y])
        line = line + "\\\\"
        file.write(line+"\n")
        file.write("\\hline\n")

    file.write("\\end{tabular}\n")
    file.write("\\end{center}\n")

#Main
tableStr = input("Entrez le tableau sous forme matricielle ([[],[],[],...]) :")
colNameStr = input("Entrez le nom des colonnes avec des espaces :")
lineNameStr = input("Entrez le nom des lignes avec des espaces :")
fileName = input("Entrez le nom du fichier de sortie :")
file = open("../out/"+fileName,"w",encoding='utf-8')

#Génération de la table
tableInter = tableStr.split("],[")
table = []
for x in range(len(tableInter)):
    tableInter[x] = tableInter[x].split("[")
    tableInter[x] = "".join(tableInter[x])
    tableInter[x] = tableInter[x].split("]")
    tableInter[x] = "".join(tableInter[x])
    tableInter[x] = tableInter[x].split(",")

for x in range(len(tableInter)):
    tempo = []
    for y in range(len(tableInter[0])):
        tempo.append(int(tableInter[x][y]))
    table.append(tempo)

colName = colNameStr.split(" ")
lineName = lineNameStr.split(" ")

largeur = len(table[0])
hauteur = len(table)

file.write("Table original :\n")
print_latex(table, colName, lineName,[],[],file)

#Création de matrice carré
dupNum = 1
while largeur < hauteur:
    for x in range(hauteur):
        table[x].append(0)

    colName.append("Ajout " + str(dupNum))
    dupNum = dupNum + 1
    largeur = largeur + 1

while hauteur < largeur:
    zeros = []
    for x in range(largeur):
        zeros.append(0)
    table.append(zeros)
    lineName.append("Ajout " + str(dupNum))
    dupNum = dupNum + 1
    hauteur = hauteur + 1

file.write("Table carré :\n")
print_latex(table, colName, lineName,[],[],file)

#Soustraction du min des colonnes/lignes
for x in range(hauteur):
    minimum = min(table[x])
    for y in range(largeur):
        table[x][y] = table[x][y] - minimum

for x in range(largeur):
    vert = []
    for y in range(hauteur):
        vert.append(table[y][x])
    minimum = min(vert)
    for y in range(hauteur):
        table[y][x] = table[y][x] - minimum

file.write("Table suite à la soustraction des minimums des lignes et colonnes :\n")

#Nombre minimal de ligne
while True:
    zeroLine = []
    zeroCol = []
    while True:
        minZero = hauteur + 1
        pos = 0
        isLine = True

        for x in range(hauteur):
            hor = []
            for y in range(largeur):
                if x in zeroLine:
                    continue
                if y in zeroCol:
                    continue
                hor.append(table[x][y])
            actualZero = 0
            for y in hor:
                if y == 0:
                    actualZero = actualZero + 1
            if actualZero < minZero and actualZero != 0:
                minZero = actualZero
                isLine = False
                for y in range(largeur):
                    if x in zeroLine:
                        continue
                    if y in zeroCol:
                        continue
                    if table[x][y] == 0:
                        pos = y
                        break

        for x in range(largeur):
            vert = []
            for y in range(hauteur):
                if y in zeroLine:
                    continue
                if x in zeroCol:
                    continue
                vert.append(table[y][x])
            actualZero = 0
            for y in vert:
                if y == 0:
                    actualZero = actualZero + 1
            if actualZero < minZero and actualZero != 0:
                minZero = actualZero
                isLine = True
                for y in range(hauteur):
                    if y in zeroLine:
                        continue
                    if x in zeroCol:
                        continue
                    if table[y][x] == 0:
                        pos = y
                        break

        if minZero == hauteur + 1:
            break

        if isLine:
            zeroLine.append(pos)
        else:
            zeroCol.append(pos)

    print_latex(table, colName, lineName, zeroLine, zeroCol,file)

    zeroLineStr = ""
    zeroColStr = ""
    if len(zeroLine) != 0:
        zeroLineStr = str(zeroLine[0])
        for x in range(len(zeroLine)-1):
            zeroLineStr = zeroLineStr + ", " + str(zeroLine[x+1])

    if len(zeroCol) != 0:
        zeroColStr = str(zeroCol[0])
        for x in range(len(zeroCol)-1):
            zeroColStr = zeroColStr + ", " + str(zeroCol[x+1])

    if len(zeroLine) == 0:
        file.write("Les colonnes nécessaires pour couvrir tous les zéros sont les colonnes " + zeroColStr + ".\n")
    elif len(zeroCol) == 0:
        file.write("Les lignes nécessaires pour couvrir tous les zéros sont les lignes " + zeroLineStr + ".\n")
    else:
        file.write("Les lignes et colonnes nécessaires pour couvrir tous les zéros sont les lignes " + zeroLineStr +
              " et les colonnes " + zeroColStr + ".\n")

    zeroLineCol = len(zeroCol) + len(zeroLine)

    if zeroLineCol < hauteur:
        file.write("On a seulement " + str(zeroLineCol) + " lignes et colonnes, donc on doit continuer l'algorithme.\n")
    else:
        file.write("On a bien qu'il faut au moins " + str(zeroLineCol) + " lignes et colonnes pour couvrir tous les zéros. "+
                                                                    "On peut donc trouver une affectation de coût 0.\n")

    if zeroLineCol >= hauteur:
        break

    minNonZero = 1000000
    for x in range(hauteur):
        for y in range(largeur):
            if x in zeroLine:
                continue
            if y in zeroCol:
                continue

            if table[x][y] < minNonZero:
                minNonZero = table[x][y]

    for x in range(hauteur):
        for y in range(largeur):
            if x in zeroLine:
                if y in zeroCol:
                    table[x][y] = table[x][y] + minNonZero
                continue
            if y in zeroCol:
                continue
            table[x][y] = table[x][y] - minNonZero

    file.write("La valeur minimal qui n'est pas dans une ligne couvrant un zéro est " + str(minNonZero) + ". On soustrait" +
            " cette valeur à chaque élément du tableau, puis on l'ajoute à chaque élément des lignes couvrant les" +
            " zéros. On obtient :\n")

