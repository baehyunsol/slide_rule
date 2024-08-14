import math
import pygame
from pygame.surface import Surface
import sys
from typing import Tuple

pygame.init()

# TODO: make font sizes adjustable
font = pygame.font.Font(None, 96)

# div by 1000 to get f_scale (which is 1.0 ~ 10.0)
def get_linear_scale() -> Tuple[list[int], list[int]]:  # (all scale, marked scale)
    return (
        list(range(1000, 1400, 10)) + list(range(1400, 2000, 25)) + list(range(2000, 4000, 50)) + list(range(4000, 10000, 100)),
        list(range(1000, 10000, 1000)) + list(range(1000, 2000, 100)) + list(range(2000, 4000, 250)),
    )

# div by 1000 to get f_scale (which is 0.0 ~ 1.0)
def get_log_scale() -> Tuple[list[int], list[int]]:  # (all scale, marked scale)
    return (
        list(range(0, 1000, 10)),
        list(range(0, 1000, 50)),
    )

def get_sqrt_scale() -> Tuple[list[int], list[int]]:  # (all scale, marked scale)
    return (
        list(range(1000, 1300, 10)) + list(range(1300, 2000, 25)) + list(range(2000, 3051, 50)),
        list(range(1000, 1300, 50)) + list(range(1000, 3001, 100)),
    )

def blit_text_at(
    surface: Surface,
    text: Surface,
    r: int,
    angle: float,
):
    text = pygame.transform.rotate(text, -angle * 180 / math.pi - 90)
    w, h = text.get_size()
    corner = (1440 + r * math.cos(angle) - w // 2, 1440 + r * math.sin(angle) - h // 2)

    surface.blit(
        text,
        corner,
    )

def draw_hand(
    surface: Surface,
    angle: float,
    r: float,
):
    angle -= 90
    angle /= 180 / math.pi
    pygame.draw.line(
        surface,
        (192, 32, 192),
        (1440, 1440),
        (1440 + r * math.cos(angle), 1440 + r * math.sin(angle)),
        12,
    )
    pygame.draw.circle(
        surface,
        (192, 32, 192),
        (1440 + r * math.cos(angle), 1440 + r * math.sin(angle)),
        6,
    )
    pygame.draw.circle(
        surface,
        (0, 0, 0),
        (1440, 1440),
        40,
    )

def draw_disk(
    rotate_result: float = 0.0,
    zoom: float = 1.0,
    draw_log: bool = False,
    draw_sqrt: bool = False,
):
    result = pygame.surface.Surface((2880, 2880))
    result.fill((255, 255, 255))
    pygame.draw.circle(result, (255, 255, 255), (1440, 1440), 1440)
    pygame.draw.circle(result, (0, 0, 0), (1440, 1440), 40)

    linear_scale, marked_linear_scale = get_linear_scale()

    for scale in linear_scale:
        f_scale = scale / 1000
        r_start = 1400

        if scale % 1000 == 0:
            r_start = 1320

        elif scale % 500 == 0 or\
            scale % 100 == 0 and scale < 2000 or\
            scale % 250 == 0 and 2000 < scale < 4000 or\
            scale % 50 == 0 and scale < 1400:
            r_start = 1360

        angle = (math.log10(f_scale) - 0.25) * 6.283185307179586

        pygame.draw.line(
            result,
            (0, 0, 0),
            (1440 + r_start * math.cos(angle), 1440 + r_start * math.sin(angle)),
            (1440 + 1440 * math.cos(angle), 1440 + 1440 * math.sin(angle)),
            4,
        )

        if scale in marked_linear_scale:
            blit_text_at(
                result,
                font.render(str(f_scale), True, (0, 0, 0)),
                1280,
                angle,
            )

    # TODO: repeated code
    if draw_log:
        log_scale, marked_log_scale = get_log_scale()

        for scale in log_scale:
            f_scale = scale / 1000
            angle = (f_scale - 0.25) * 6.283185307179586
            r = 8

            if scale % 100 == 0:
                r = 24

            elif scale % 50 == 0:
                r = 16

            pygame.draw.circle(
                result,
                (0, 0, 0),
                (1440 + 1150 * math.cos(angle), 1440 + 1150 * math.sin(angle)),
                r,
            )

            if scale in marked_log_scale:
                blit_text_at(
                    result,
                    font.render(str(f_scale), True, (0, 0, 0)),
                    1080,
                    angle,
                )

    if draw_sqrt:
        sqrt_scale, marked_sqrt_scale = get_sqrt_scale()

        for scale in sqrt_scale:
            f_scale = scale / 1000
            angle = (math.log10(f_scale ** 2) - 0.25) * 6.283185307179586
            r = 8

            if scale % 100 == 0 or\
                scale % 50 == 0 and scale < 1300:
                r = 16

            pygame.draw.circle(
                result,
                (0, 0, 0),
                (1440 + 960 * math.cos(angle), 1440 + 960 * math.sin(angle)),
                r,
            )

            if scale in marked_sqrt_scale:
                blit_text_at(
                    result,
                    font.render(str(f_scale), True, (0, 0, 0)),
                    890,
                    angle,
                )

    if rotate_result != 0.0:
        rotated = pygame.transform.rotate(result, -rotate_result)
        r_w, r_h = rotated.get_size()
        result.fill((255, 255, 255))
        result.blit(rotated, (0, 0), ((r_w - 2880) // 2, (r_h - 2880) // 2, 2880, 2880))

    if zoom != 1.0:
        zoomed = pygame.transform.scale_by(result, zoom)
        z_w, z_h = zoomed.get_size()
        result.fill((255, 255, 255))
        result.blit(zoomed, ((2880 - z_w) // 2, (2880 - z_h) // 2))

    result.set_colorkey((255, 255, 255))
    return result

background = pygame.surface.Surface((2880, 2880))
background.fill((255, 255, 255))
background.set_colorkey((255, 255, 255))

angle1 = float(sys.argv[1])
angle2 = float(sys.argv[2])

draw_hand(
    background,
    angle2,
    1400.0,
)

# main disk
disk1 = draw_disk(
    rotate_result=0.0,
    zoom=1.0,
)

# sub disk
disk2 = draw_disk(
    rotate_result=angle1,
    zoom=0.83,
    draw_log=True,
    draw_sqrt=True,
)

background.blit(disk1, (0, 0))
background.blit(disk2, (0, 0))

pygame.image.save(background, "slide_rule.png")
