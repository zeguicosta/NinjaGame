import os
import pygame

# Preset the initial path
BASE_IMG_PATH = 'data/images/'

# Function to load images
def load_image(path):
    # .convert converts the internal representation of the image in pygame
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    # Turning black to transparent
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    # This will become the list of all our images after the for below
    images = []
    # os.listdir takes a path and gives all the files that are on that path
    # sorted() makes sure the images are in order
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images
