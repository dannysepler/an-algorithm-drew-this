from pathlib import Path
from random import randint
from typing import Iterable, Tuple

from PIL import Image, ImageDraw, ImageFont

Color = Tuple[int, int, int]

black = (0, 0, 0)
comic_sans = ImageFont.truetype("ComicSansMS.ttf", 400)
MODE = 'RGBA'


def random_color(min: int = 0, max: int = 255) -> Color:
    # the lower the numbers, the darker it'll be
    # the higher the numbers, the lighter it'll be
    return (randint(min, max), randint(min, max), randint(min, max))


def random_gradient(difference_delta=40) -> Tuple[Color, Color]:
    # This generates a random gradient, forcing the colors to be different
    # enough to be visually noticeable
    start = random_color()
    end = random_color()

    while any(s - e <= difference_delta for s, e in zip(start, end)):
        start = random_color()
        end = random_color()

    return (start, end)


def interpolate(
    from_color: Color, to_color: Color, interval: int
) -> Iterable[Color]:
    # approach borrowed from
    # https://gist.github.com/weihanglo/1e754ec47fdd683a42fdf6a272904535
    det_co = [(t - f) / interval for f, t in zip(from_color, to_color)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(from_color, det_co)]


def add_gradient(original: Image) -> Image:
    gradient = Image.new(MODE, original.size, color=0)
    draw = ImageDraw.Draw(gradient)

    from_color, to_color = random_gradient()
    for i, color in enumerate(
        interpolate(from_color, to_color, original.width * 2)
    ):
        draw.line([(i, 0), (0, i)], tuple(color), width=1)

    im_composite = Image.alpha_composite(gradient, original)
    return im_composite


def add_text(*, img: Image, text: str) -> None:
    draw = ImageDraw.Draw(img)
    draw.text(
        (250, 500),
        text,
        fill=random_color(min=200),
        font=comic_sans,
        stroke_width=5,
        stroke_fill=black,
    )


def main() -> None:
    img_dir = Path(__file__).parent / "images"
    img_dir.mkdir()

    for i in range(10):
        print(f"Creating image {i}")
        img = Image.new(MODE, (5000, 1600))
        add_text(img=img, text="An algorithm drew this")

        img_with_gradient = add_gradient(img)
        img_with_gradient.save(f"images/image{i}.png")


if __name__ == "__main__":
    main()
