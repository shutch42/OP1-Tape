import pygame


def play_pressed(key):
    return key == pygame.K_SPACE


def stop_pressed(key):
    return key == pygame.K_BACKSPACE


def record_pressed(key):
    return key == pygame.K_r


def shift_pressed(mods):
    return mods & pygame.KMOD_SHIFT


def left_pressed(key):
    return key == pygame.K_LEFT


def right_pressed(key):
    return key == pygame.K_RIGHT