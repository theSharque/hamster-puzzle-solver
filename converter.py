import logging
from io import BytesIO
from PIL import Image, ImageFilter

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def is_red_pixel(pixel):
    return pixel[0] > 64 and pixel[1] < pixel[0] // 2 and pixel[2] < pixel[0] // 2


def is_green_pixel(pixel):
    return pixel[1] > 64 and pixel[0] < pixel[1] // 2 and pixel[2] < pixel[1] // 2


def check_pixel(pixel):
    return is_red_pixel(pixel) or is_green_pixel(pixel)


def find_top(image) -> int:
    for y in range(image.height):
        found = 0
        for x in range(image.width):
            if check_pixel(image.getpixel((x, y))):
                found += 1
        if found > image.width // 4:
            return y


def find_bottom(image) -> int:
    for y in range(image.height - 1, 0, -1):
        found = 0
        for x in range(image.width):
            if check_pixel(image.getpixel((x, y))):
                found += 1
        if found > image.width // 4:
            return y


def find_left(image) -> int:
    for x in range(image.width):
        found = 0
        for y in range(image.height):
            if check_pixel(image.getpixel((x, y))):
                found += 1
        if found > image.height // 8:
            return x


def find_right(image) -> int:
    for x in range(image.width - 1, 0, -1):
        found = 0
        for y in range(image.height):
            if check_pixel(image.getpixel((x, y))):
                found += 1
        if found > image.height // 8:
            return x


def prepare_image(image_data: BytesIO):
    puzzle = Image.open(image_data)
    top = find_top(puzzle)
    logger.debug("Top row: {}".format(top))
    bottom = find_bottom(puzzle)
    logger.debug("Bottom row: {}".format(bottom))
    left = find_left(puzzle)
    logger.debug("Left row: {}".format(left))
    right = find_right(puzzle)
    logger.debug("Right row: {}".format(right))

    puzzle = puzzle.crop((left, top - 1, right, bottom + 1))
    puzzle = puzzle.resize((300, 300))
    # puzzle.save("puzzle.jpg", "JPEG")

    contour = puzzle.filter(ImageFilter.SHARPEN)
    contour = contour.filter(ImageFilter.CONTOUR)
    # contour.save("puzzle2.jpg", "JPEG")

    return puzzle, contour


def is_white_pixel(pixel):
    return pixel[0] > 128 and pixel[1] > 128 and pixel[2] > 128


def follow_green(contour, x, y):
    sx = x
    while x < contour.width:
        x += 1
        pixel = contour.getpixel((x, y))
        if not is_white_pixel(pixel):
            break

    return (x - sx) // 50


def follow_red(contour, x, y):
    sy = y
    while y < contour.height:
        y += 1
        pixel = contour.getpixel((x, y))
        if not is_white_pixel(pixel):
            break

    return (y - sy) // 50


def is_yellow_pixel(pixel):
    return pixel[0] > 64 and pixel[1] > 64 and pixel[2] < pixel[0] // 2 and pixel[2] < pixel[1] // 2


def collect_rows(puzzle, contour):
    rows = [[" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "]]

    for y in range(6):
        for x in range(6):
            if rows[y][x] == " ":
                x_point = x * 50 + 25
                y_point = y * 50 + 25
                pixel = puzzle.getpixel((x_point, y_point))
                if is_green_pixel(pixel):
                    green_len = follow_green(contour, x_point, y_point)
                    rows[y][x] = "<"
                    if green_len == 1:
                        rows[y][x + 1] = ">"
                    elif green_len == 2:
                        rows[y][x + 1] = "-"
                        rows[y][x + 2] = ">"
                elif is_red_pixel(pixel):
                    red_len = follow_red(contour, x_point, y_point)
                    rows[y][x] = "n"
                    if red_len == 1:
                        rows[y + 1][x] = "u"
                    elif red_len == 2:
                        rows[y + 1][x] = "!"
                        rows[y + 2][x] = "u"
                elif is_yellow_pixel(pixel):
                    rows[y][x] = "o"
                    rows[y][x + 1] = "="
    return rows


def translate_to_rows(image_data: BytesIO):
    puzzle, contour = prepare_image(image_data)
    rows = collect_rows(puzzle, contour)

    logger.debug(rows)

    return rows


def main():
    # user_photo.jpg - is a screenshot of puzzle (not included) for debug
    with open("user_photo.jpg", "rb") as fh:
        buf = BytesIO(fh.read())
        translate_to_rows(buf)


if __name__ == "__main__":
    main()
