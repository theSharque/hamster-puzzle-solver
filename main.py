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
    # Initialize the rows matrix with empty spaces
    rows = [[" " for _ in range(6)] for _ in range(6)]
    
    # Define a mapping from block types to characters
    block_map = {
        "---": lambda row, col: (row, col),
        "--": lambda row, col: (row, col),
        "==": lambda row, col: (row, col),
        "!!!": lambda row, col: (row, col),
        "!!": lambda row, col: (row, col)
    }
    
    # Define the character mappings for each block type
    char_map = {
        "---": ("<", "═", ">"),
        "--": ("<", ">"),
        "==": ("o", "="),
        "!!!": ("n", "║", "u"),
        "!!": ("n", "u")
    }
    
    # Iterate over the blocks and place characters in the rows matrix
    for block in blocks:
        row, col = block[0], block[1]
        char_type = block[2]
        
        if char_type in char_map:
            chars = char_map[char_type]
            if len(chars) == 3:
                rows[row][col] = chars[0]
                rows[row][col + 1] = chars[1]
                rows[row][col + 2] = chars[2]
            elif len(chars) == 2:
                rows[row][col] = chars[0]
                rows[row][col + 1] = chars[1]
    
    return rows
def show(rows):
    res = "╔═════════════╗\n"
    for i in range(len(rows)):
        res += "║ "
        for j in range(len(rows[i])):
            if rows[i][j] == " ":
                res += " "
            if rows[i][j] == "<":
                res += "╺"
            elif rows[i][j] == ">":
                res += "╸"
            elif rows[i][j] == "═":
                res += "━"
            elif rows[i][j] == "n":
                res += "╻"
            elif rows[i][j] == "u":
                res += "╹"
            elif rows[i][j] == "║":
                res += "┃"
            elif rows[i][j] == "o":
                res += "O"
            elif rows[i][j] == "=":
                res += "━"

            if rows[i][j] == "<" or rows[i][j] == "═" or rows[i][j] == "o":
                res += "━"
            else:
                res += " "
        res += "║\n"

    res += "╚═════════════╝\n"
    return res


def rows_to_str(rows):
    res = ""
    for i in rows:
        for j in i:
            res += j
        res += ','
    return res[:-1]


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
