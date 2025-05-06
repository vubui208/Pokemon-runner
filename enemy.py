import pygame
import os

class Enemy:
    def __init__(self, images,left,right, x=80, y=400):
        self.images = images        # Lưu list hình ảnh
        self.current_frame = 0      # Frame hiện tại cho animation
        self.x = x
        self.y = y
        self.left = left
        self.right = right
        self.rect = images[0].get_rect(topleft=(x, y))
        # Lưu giá trị bottom ban đầu để làm mặt đất
        self.image_height = images[0].get_height()
        self.bottom = self.y + images[0].get_height()
    
  
    
    
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
        self.bottom = self.y + self.images[0].get_height()
    def get_base_position(self):
        return self._initial_bottom