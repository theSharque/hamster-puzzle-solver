from idlelib.run import flush_stdout
from time import sleep


def inp():
    # print("Enter puzzle in format:")
    # print()
    # print("  <-> ")
    # print("  nn<>")
    # print("o=uun ")
    # print("n   !n")
    # print("!n<>uu")
    # print("uu  <>")
    # print()
    # print("Where <> <-> is horizontal, nu is vertical, o= is the key")

    r = ["", "", "", "", "", ""]
    # for i in range(6):
    #     r[i] = list(input("Row " + str(i) + ": "))

    r[0] = list("nn  n ")
    r[1] = list("uu<>! ")
    r[2] = list("o=n u ")
    r[3] = list("n u<>n")
    r[4] = list("u<>n !")
    r[5] = list("<> u u")

    # r[0] = list("  --- ")
    # r[1] = list("  !!--")
    # r[2] = list("==!!! ")
    # r[3] = list("!   !!")
    # r[4] = list("!!--!!")
    # r[5] = list("!!  --")
    return r


def rows_to_blocks(rows):
    blocks = set()
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if rows[i][j] == "<" and j + 2 < len(rows[i]) and rows[i][j + 1] == ">" and rows[i][j + 2] == ">":
                blocks.add((i, j, "---"))
                rows[i][j] = " "
                rows[i][j + 1] = " "
                rows[i][j + 2] = " "
            elif rows[i][j] == "<" and j + 1 < len(rows[i]) and rows[i][j + 1] == ">":
                blocks.add((i, j, "--"))
                rows[i][j] = " "
                rows[i][j + 1] = " "
            elif rows[i][j] == "o" and j + 1 < len(rows[i]) and rows[i][j + 1] == "=":
                blocks.add((i, j, "=="))
                rows[i][j] = " "
                rows[i][j + 1] = " "
            elif rows[i][j] == "n" and i + 2 < len(rows) and rows[i + 1][j] == "u" and rows[i + 2][j] == "u":
                blocks.add((i, j, "!!!"))
                rows[i][j] = " "
                rows[i + 1][j] = " "
                rows[i + 2][j] = " "
            elif rows[i][j] == "n" and i + 1 < len(rows) and rows[i + 1][j] == "u":
                blocks.add((i, j, "!!"))
                rows[i][j] = " "
                rows[i + 1][j] = " "
    return list(blocks)
def blocks_to_rows(blocks):
    rows = [[" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "]]

    for i in range(len(blocks)):
        if blocks[i][2] == "---":
            rows[blocks[i][0]][blocks[i][1]] = "<"
            rows[blocks[i][0]][blocks[i][1] + 1] = "═"
            rows[blocks[i][0]][blocks[i][1] + 2] = ">"
        elif blocks[i][2] == "--":
            rows[blocks[i][0]][blocks[i][1]] = "<"
            rows[blocks[i][0]][blocks[i][1] + 1] = ">"
        elif blocks[i][2] == "==":
            rows[blocks[i][0]][blocks[i][1]] = "o"
            rows[blocks[i][0]][blocks[i][1] + 1] = "="
        elif blocks[i][2] == "!!!":
            rows[blocks[i][0]][blocks[i][1]] = "n"
            rows[blocks[i][0] + 1][blocks[i][1]] = "║"
            rows[blocks[i][0] + 2][blocks[i][1]] = "u"
        elif blocks[i][2] == "!!":
            rows[blocks[i][0]][blocks[i][1]] = "n"
            rows[blocks[i][0] + 1][blocks[i][1]] = "u"
    return rows


def show(rows):
    res = "╔" + "═" * (len(rows[0]) * 2 - 1) + "╗\n"
    
    for i in range(len(rows)):
        res += "║"
        for j in range(len(rows[i])):
            char = rows[i][j]
            if char == " ":
                res += " "
            elif char == "<":
                res += "╺"
            elif char == ">":
                res += "╸"
            elif char == "═":
                res += "━"
            elif char == "n":
                res += "╻"
            elif char == "u":
                res += "╹"
            elif char == "║":
                res += "┃"
            elif char == "o":
                res += "O"
            elif char in ["<", "═", "o"]:
                res += "━"
            else:
                res += " "
        res += "║\n"
    
    res += "╚" + "═" * (len(rows[0]) * 2 - 1) + "╝\n"
    return res
def rows_to_str(rows):
    # Use a list comprehension to join all elements in each sublist with ','
    # Then join all sublists with '\n' (or any other delimiter you prefer)
    return ',\n'.join([''.join(row) for row in rows])
def str_to_rows(key: str):
    raws = list(key.split(','))
    raws = [list(x) for x in raws]
    return raws


def main():
    rows = inp()
    blocks = rows_to_blocks(rows)
    rows = blocks_to_rows(blocks)
    screens = {rows_to_str(rows): 'init'}

    i = 0
    while i < len(screens.keys()):
        parent_key = list(screens.keys())[i]
        blocks = rows_to_blocks(str_to_rows(parent_key))
        rows = str_to_rows(parent_key)

        for b in range(len(blocks)):
            if blocks[b][2] == "!!!":
                if blocks[b][0] - 1 >= 0 and rows[blocks[b][0] - 1][blocks[b][1]] == " ":
                    blocks[b][0] -= 1
                    key = rows_to_str(blocks_to_rows(blocks))
                    if not key in screens.keys():
                        screens[key] = parent_key
                    blocks[b][0] += 1
                if blocks[b][0] + 3 < 6 and rows[blocks[b][0] + 3][blocks[b][1]] == " ":
                    blocks[b][0] += 1
                    key = rows_to_str(blocks_to_rows(blocks))
                    if not key in screens.keys():
                        screens[key] = parent_key
                    blocks[b][0] -= 1

            elif blocks[b][2] == "!!":
                if blocks[b][0] - 1 >= 0 and rows[blocks[b][0] - 1][blocks[b][1]] == " ":
                    blocks[b][0] -= 1
                    key = rows_to_str(blocks_to_rows(blocks))
                    if not key in screens.keys():
                        screens[key] = parent_key
                    blocks[b][0] += 1
                if blocks[b][0] + 2 < 6 and rows[blocks[b][0] + 2][blocks[b][1]] == " ":
                    blocks[b][0] += 1
                    key = rows_to_str(blocks_to_rows(blocks))
                    if not key in screens.keys():
                        screens[key] = parent_key
                    blocks[b][0] -= 1

            elif blocks[b][2] == "---":
                if blocks[b][1] - 1 >= 0 and rows[blocks[b][0]][blocks[b][1] - 1] == " ":
                    blocks[b][1] -= 1
                    key = rows_to_str(blocks_to_rows(blocks))
                    if not key in screens.keys():
                        screens[key] = parent_key
                    blocks[b][1] += 1
                if blocks[b][1] + 3 < 6 and rows[blocks[b][0]][blocks[b][1] + 3] == " ":
                    blocks[b][1] += 1
                    key = rows_to_str(blocks_to_rows(blocks))
                    if not key in screens.keys():
                        screens[key] = parent_key
                    blocks[b][1] -= 1

            elif blocks[b][2] == "==" or blocks[b][2] == "--":
                if blocks[b][1] - 1 >= 0 and rows[blocks[b][0]][blocks[b][1] - 1] == " ":
                    blocks[b][1] -= 1
                    key = rows_to_str(blocks_to_rows(blocks))
                    if not key in screens.keys():
                        screens[key] = parent_key
                    blocks[b][1] += 1
                if blocks[b][1] + 2 < 6 and rows[blocks[b][0]][blocks[b][1] + 2] == " ":
                    blocks[b][1] += 1
                    key = rows_to_str(blocks_to_rows(blocks))
                    if not key in screens.keys():
                        screens[key] = parent_key

                    if blocks[b][2] == "==" and blocks[b][1] == 4:
                        print("Found solution...")
                        shows = []
                        rows = blocks_to_rows(blocks)
                        shows.append(show(rows))
                        key = screens[rows_to_str(rows)]

                        while key != 'init':
                            shows.append(show(str_to_rows(key)))
                            key = screens[key]

                        while True:
                            for n in range(len(shows)):
                                print("\033[0;0H")
                                print(shows[len(shows) - 1 - n])
                                flush_stdout()
                                sleep(0.3)

                    else:
                        blocks[b][1] -= 1

        i += 1


if __name__ == '__main__':
    main()
