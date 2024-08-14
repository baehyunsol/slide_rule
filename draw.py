import math
import pygame
from pygame.surface import Surface
import sys
from typing import Tuple

pygame.init()

# NOTE: it works best when SCREEN_SIZE is 2880
SCREEN_SIZE = 2880
HALF_SCREEN = SCREEN_SIZE // 2
UNIT_LENGTH = SCREEN_SIZE // 72
UNIT_RADIUS = SCREEN_SIZE // 480

font = pygame.font.Font(None, UNIT_LENGTH * 2)

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
    corner = (HALF_SCREEN + r * math.cos(angle) - w // 2, HALF_SCREEN + r * math.sin(angle) - h // 2)

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
        (HALF_SCREEN, HALF_SCREEN),
        (HALF_SCREEN + r * math.cos(angle), HALF_SCREEN + r * math.sin(angle)),
        UNIT_RADIUS * 2,
    )
    pygame.draw.circle(
        surface,
        (192, 32, 192),
        (HALF_SCREEN + r * math.cos(angle), HALF_SCREEN + r * math.sin(angle)),
        UNIT_RADIUS,
    )
    pygame.draw.circle(
        surface,
        (0, 0, 0),
        (HALF_SCREEN, HALF_SCREEN),
        UNIT_RADIUS * 6,
    )

def draw_disk(
    rotate_result: float = 0.0,
    zoom: float = 1.0,
    draw_log: bool = False,
    draw_sqrt: bool = False,
):
    result = pygame.surface.Surface((SCREEN_SIZE, SCREEN_SIZE))
    result.fill((255, 255, 255))
    pygame.draw.circle(result, (255, 255, 255), (HALF_SCREEN, HALF_SCREEN), HALF_SCREEN)
    pygame.draw.circle(result, (0, 0, 0), (HALF_SCREEN, HALF_SCREEN), UNIT_RADIUS * 6)

    linear_scale, marked_linear_scale = get_linear_scale()

    for scale in linear_scale:
        f_scale = scale / 1000
        r_start = HALF_SCREEN - UNIT_LENGTH

        if scale % 1000 == 0:
            r_start = HALF_SCREEN - 3 * UNIT_LENGTH

        elif scale % 500 == 0 or\
            scale % 100 == 0 and scale < 2000 or\
            scale % 250 == 0 and 2000 < scale < 4000 or\
            scale % 50 == 0 and scale < 1400:
            r_start = HALF_SCREEN - 2 * UNIT_LENGTH

        angle = (math.log10(f_scale) - 0.25) * 6.283185307179586

        pygame.draw.line(
            result,
            (0, 0, 0),
            (HALF_SCREEN + r_start * math.cos(angle), HALF_SCREEN + r_start * math.sin(angle)),
            (HALF_SCREEN + HALF_SCREEN * math.cos(angle), HALF_SCREEN + HALF_SCREEN * math.sin(angle)),
            UNIT_RADIUS,
        )

        if scale in marked_linear_scale:
            blit_text_at(
                result,
                font.render(str(f_scale), True, (0, 0, 0)),
                HALF_SCREEN - 4 * UNIT_LENGTH,
                angle,
            )

    # TODO: repeated code
    if draw_log:
        log_scale, marked_log_scale = get_log_scale()

        for scale in log_scale:
            f_scale = scale / 1000
            angle = (f_scale - 0.25) * 6.283185307179586
            r = UNIT_RADIUS

            if scale % 100 == 0:
                r = 3 * UNIT_RADIUS

            elif scale % 50 == 0:
                r = 2 * UNIT_RADIUS

            pygame.draw.circle(
                result,
                (0, 0, 0),
                (HALF_SCREEN + (HALF_SCREEN - 7 * UNIT_LENGTH) * math.cos(angle), HALF_SCREEN + (HALF_SCREEN - 7 * UNIT_LENGTH) * math.sin(angle)),
                r,
            )

            if scale in marked_log_scale:
                blit_text_at(
                    result,
                    font.render(str(f_scale), True, (0, 0, 0)),
                    HALF_SCREEN - 9 * UNIT_LENGTH,
                    angle,
                )

    if draw_sqrt:
        sqrt_scale, marked_sqrt_scale = get_sqrt_scale()

        for scale in sqrt_scale:
            f_scale = scale / 1000
            angle = (math.log10(f_scale ** 2) - 0.25) * 6.283185307179586
            r = UNIT_RADIUS

            if scale % 100 == 0 or\
                scale % 50 == 0 and scale < 1300:
                r = UNIT_RADIUS * 3

            pygame.draw.circle(
                result,
                (0, 0, 0),
                (HALF_SCREEN + (HALF_SCREEN - 12 * UNIT_LENGTH) * math.cos(angle), HALF_SCREEN + (HALF_SCREEN - 12 * UNIT_LENGTH) * math.sin(angle)),
                r,
            )

            if scale in marked_sqrt_scale:
                blit_text_at(
                    result,
                    font.render(str(f_scale), True, (0, 0, 0)),
                    HALF_SCREEN - 14 * UNIT_LENGTH,
                    angle,
                )

    if rotate_result != 0.0:
        rotated = pygame.transform.rotate(result, -rotate_result)
        r_w, r_h = rotated.get_size()
        result.fill((255, 255, 255))
        result.blit(rotated, (0, 0), ((r_w - SCREEN_SIZE) // 2, (r_h - SCREEN_SIZE) // 2, SCREEN_SIZE, SCREEN_SIZE))

    if zoom != 1.0:
        zoomed = pygame.transform.scale_by(result, zoom)
        z_w, z_h = zoomed.get_size()
        result.fill((255, 255, 255))
        result.blit(zoomed, ((SCREEN_SIZE - z_w) // 2, (SCREEN_SIZE - z_h) // 2))

    result.set_colorkey((255, 255, 255))
    return result

background = pygame.surface.Surface((SCREEN_SIZE, SCREEN_SIZE))
background.fill((255, 255, 255))
background.set_colorkey((255, 255, 255))

angle1 = float(sys.argv[1])
angle2 = float(sys.argv[2])

draw_hand(
    background,
    angle2,
    HALF_SCREEN - UNIT_LENGTH,
)

# main disk
disk1 = draw_disk(
    rotate_result=0.0,
    zoom=1.0,
)

# sub disk
disk2 = draw_disk(
    rotate_result=angle1,
    zoom=0.85,
    draw_log=True,
    draw_sqrt=True,
)

background.blit(disk1, (0, 0))
background.blit(disk2, (0, 0))

pygame.image.save(background, "slide_rule.png")
