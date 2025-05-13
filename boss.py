import pygame
import os

class Boss:
    def __init__(self, images,left,right,idle, x=80, y=400,health = 100,maxHP = 100):
        self.images = images        # Lưu list hình ảnh   # Frame hiện tại cho animation
        self.x = x
        self.y = y
        self.left = left
        self.right = right
        self.idle = idle
        self.rect = images[0].get_rect(topleft=(x, y))
        self.health = health
        self.maxHP = maxHP
        self.hitbox = (self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
        self.bottom = self.y + self.images[0].get_height()
    def get_base_position(self):
        return self._initial_bottom