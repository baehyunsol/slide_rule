# NOTE: this code is largely incomplete

import pygame
import subprocess

angle1 = 0
angle2 = 40

pygame.init()

font = pygame.font.Font(None, 24)
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

while True:
    clock.tick(30)
    screen.fill((255, 255, 255))
    screen.blit(
        font.render(f"Angle 1: {angle1}", True, (0, 0, 0)),
        (10, 10),
    )
    screen.blit(
        font.render(f"Angle 2: {angle2}", True, (0, 0, 0)),
        (10, 30),
    )
    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

        elif e.type == pygame.KEYDOWN:
            is_shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
            is_ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL
            new_angle = angle1 if is_shift_pressed else angle2
            d_angle = 1 if is_ctrl_pressed else 10

            if e.key == pygame.K_LEFT:
                if new_angle < 90 or new_angle > 270:
                    new_angle -= d_angle

                else:
                    new_angle += d_angle

            elif e.key == pygame.K_RIGHT:
                if new_angle < 90 or new_angle > 270:
                    new_angle += d_angle

                else:
                    new_angle -= d_angle

            elif e.key == pygame.K_UP:
                if new_angle < 180:
                    new_angle -= d_angle

                else:
                    new_angle += d_angle

            elif e.key == pygame.K_DOWN:
                if new_angle < 180:
                    new_angle += d_angle

                else:
                    new_angle -= d_angle

            if new_angle > 360:
                new_angle -= 360

            elif new_angle < 0:
                new_angle += 360

            if is_shift_pressed:
                angle1 = new_angle

            else:
                angle2 = new_angle

            subprocess.run(["python3", "draw.py", "--angle1", str(angle1), "--angle2", str(angle2)])
