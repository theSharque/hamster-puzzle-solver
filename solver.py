from PIL import Image, ImageDraw
from wx.lib.pubsub.py2and3 import BytesIO

from hamster_bot import logger


def inp():
    print("Enter puzzle in format:")
    print()
    print("  <-> ")
    print("  nn<>")
    print("o=uun ")
    print("n   !n")
    print("!n<>uu")
    print("uu  <>")
    print()
    print("Where <> <-> is horizontal, nu is vertical, o= is the key")

    r = ["", "", "", "", "", ""]
    for i in range(6):
        r[i] = list(input("Row " + str(i) + ": "))
    return r


def rows_to_blocks(rows):
    blocks = []
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if rows[i][j] == "<" and j + 2 < len(rows[i]) and rows[i][j + 2] == ">":
                blocks.append([i, j, "---"])
                rows[i][j + 2] = rows[i][j + 1] = rows[i][j] = " "

            if rows[i][j] == "<" and j + 1 < len(rows[i]) and rows[i][j + 1] == ">":
                blocks.append([i, j, "--"])
                rows[i][j + 1] = rows[i][j] = " "

            if rows[i][j] == "o" and j + 1 < len(rows[i]) and rows[i][j + 1] == "=":
                blocks.append([i, j, "=="])
                rows[i][j + 1] = rows[i][j] = " "

            if rows[i][j] == "n" and i + 2 < len(rows) and rows[i + 2][j] == "u":
                blocks.append([i, j, "!!!"])
                rows[i + 2][j] = rows[i + 1][j] = rows[i][j] = " "

            if rows[i][j] == "n" and i + 1 < len(rows) and rows[i + 1][j] == "u":
                blocks.append([i, j, "!!"])
                rows[i + 1][j] = rows[i][j] = " "

    return blocks


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
            rows[blocks[i][0]][blocks[i][1] + 1] = "-"
            rows[blocks[i][0]][blocks[i][1] + 2] = ">"
        elif blocks[i][2] == "--":
            rows[blocks[i][0]][blocks[i][1]] = "<"
            rows[blocks[i][0]][blocks[i][1] + 1] = ">"
        elif blocks[i][2] == "==":
            rows[blocks[i][0]][blocks[i][1]] = "o"
            rows[blocks[i][0]][blocks[i][1] + 1] = "="
        elif blocks[i][2] == "!!!":
            rows[blocks[i][0]][blocks[i][1]] = "n"
            rows[blocks[i][0] + 1][blocks[i][1]] = "!"
            rows[blocks[i][0] + 2][blocks[i][1]] = "u"
        elif blocks[i][2] == "!!":
            rows[blocks[i][0]][blocks[i][1]] = "n"
            rows[blocks[i][0] + 1][blocks[i][1]] = "u"
    return rows


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


def draw(rows):
    image = Image.new("RGB", (300, 300), "black")
    image_draw = ImageDraw.Draw(image)
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if rows[i][j] == "o" and len(rows[i]) > j + 1 and rows[i][j + 1] == "=":
                image_draw.ellipse((j * 50, i * 50, (j + 1) * 50, (i + 1) * 50), "yellow", "black", 5)
                image_draw.rounded_rectangle((j * 50, i * 50 + 20, (j + 2) * 50, i * 50 + 30), 10, "yellow")
            elif rows[i][j] == "<" and len(rows[i]) > j + 1 and rows[i][j + 1] == ">":
                image_draw.rounded_rectangle((j * 50, i * 50, (j + 2) * 50, (i + 1) * 50), 20, "green", "black", 5)
            elif rows[i][j] == "<" and len(rows[i]) > j + 2 and rows[i][j + 2] == ">":
                image_draw.rounded_rectangle((j * 50, i * 50, (j + 3) * 50, (i + 1) * 50), 20, "green", "black", 5)
            elif rows[i][j] == "n" and len(rows) > i + 2 and rows[i + 2][j] == "u":
                image_draw.rounded_rectangle((j * 50, i * 50, (j + 1) * 50, (i + 3) * 50), 20, "red", "black", 5)
            elif rows[i][j] == "n" and len(rows) > i + 1 and rows[i + 1][j] == "u":
                image_draw.rounded_rectangle((j * 50, i * 50, (j + 1) * 50, (i + 2) * 50), 20, "red", "black", 5)

    return image


def calc(first_rows, filename=None):
    blocks = rows_to_blocks(first_rows)
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
                        logger.info("Found solution...")
                        frames = []
                        rows = blocks_to_rows(blocks)
                        frames.append(draw(rows))
                        key = screens[rows_to_str(rows)]

                        while key != 'init':
                            frames.append(draw(str_to_rows(key)))
                            key = screens[key]

                        frames.reverse()
                        frame_one = frames[0]
                        if filename is None:
                            result = BytesIO()
                            frame_one.save(result, format="GIF", append_images=frames, save_all=True,
                                           duration=500, loop=0)
                            return result.getvalue()
                        else:
                            frame_one.save(filename, format="GIF", append_images=frames, save_all=True,
                                           duration=500, loop=0)
                        return

                    else:
                        blocks[b][1] -= 1
        i += 1


def main():
    inp_rows = inp()
    calc(inp_rows, "solution.gif")


if __name__ == '__main__':
    main()
