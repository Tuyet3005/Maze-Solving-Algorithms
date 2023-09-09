from hashlib import new
from lib2to3.pgen2.token import STAR
import os
import threading  # ------------------- xoa file

import pygame
from PIL import Image  # --------------------tao gif
a = [-1, -1, -1]


class Video:
    BLOCK_SIZE = 21
    BACKGROUND_COLOR = [255, 255, 255]
    BONUS_IMG = pygame.image.load("imgs/bonus.png")
    CROSS_IMG = pygame.image.load("imgs/cross.png")
    OPEN_IMG = pygame.image.load("imgs/open.png")
    CLOSE_IMG = pygame.image.load("imgs/close.png")
    STAR_IMG = pygame.image.load("imgs/star.png")
    EXIT_IMG = pygame.image.load("imgs/exit.png")
    TELE0_IMG = pygame.image.load("imgs/teleport0.png")
    TELE1_IMG = pygame.image.load("imgs/teleport1.png")
    TELE2_IMG = pygame.image.load("imgs/teleport2.png")
    TELE3_IMG = pygame.image.load("imgs/teleport3.png")
    TELE4_IMG = pygame.image.load("imgs/teleport4.png")

    frames = []
    map_2d = []
    num_open = 0
    window = None

    @classmethod
    def start(cls, map_2d):
        pygame.init()
        cls.frames = []
        cls.map_2d = [row[:] for row in map_2d]
        cls.window = pygame.display.set_mode(
            (len(cls.map_2d[0]) * Video.BLOCK_SIZE, len(cls.map_2d) * Video.BLOCK_SIZE)
        )

    @classmethod
    def draw(cls, open, close):
        cls.window.fill(tuple(cls.BACKGROUND_COLOR))

        map_2d = []
        for i in range(len(cls.map_2d)):
            row = []
            for j in range(len(cls.map_2d[0])):
                row.append(cls.map_2d[i][j])
            map_2d.append(row)

       
        for x, y in open:
            if map_2d[x][y] != 'S':
                map_2d[x][y] = 'O'
        for x, y in close:
            if map_2d[x][y] != 'S':
                map_2d[x][y] = 'C'

        # Đoạn code này dùng để đếm số lượng node đã được mở trước khi tìm ra được đường đi
        # cls.num_open = 0
        # for i in range(len(map_2d)):
        #     for j in range(len(map_2d[0])):
        #         if map_2d[i][j] == 'C' or map_2d[i][j] == 'O' or \
        #         map_2d[i][j] == 'S' or map_2d[i][j] == 'E':
        #             cls.num_open += 1

        for y, row in enumerate(map_2d):
            for x, col in enumerate(row):
                if col == "+":
                    cls.window.blit(Video.BONUS_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == "x":
                    cls.window.blit(Video.CROSS_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == "O":
                    cls.window.blit(Video.OPEN_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == "C":
                    cls.window.blit(Video.CLOSE_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == 'S':
                    cls.window.blit(Video.STAR_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == 'E':
                    cls.window.blit(Video.EXIT_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == '0':
                    cls.window.blit(Video.TELE0_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == '1':
                    cls.window.blit(Video.TELE1_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == '2':
                    cls.window.blit(Video.TELE2_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == '3':
                    cls.window.blit(Video.TELE3_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))
                elif col == '4':
                    cls.window.blit(Video.TELE4_IMG, (x * Video.BLOCK_SIZE, y * Video.BLOCK_SIZE))

        pygame.display.update()
        img_name = f"frame-{len(cls.frames)}.jpg"
        pygame.image.save(cls.window, img_name)
        cls.frames.append(img_name)

    @classmethod
    def create_gif(cls, filename="video.gif"):
        pygame.quit()
        # print(cls.num_open) # số lượng node đã được mở trước khi tìm ra đường đi
        try:
            images_dict = {}
            threads = []

            for index, frame in enumerate(cls.frames):
                threads.append(threading.Thread(target=add_frame, args=(images_dict, index, frame)))
                threads[-1].start()

            for thread in threads:
                thread.join()

            images = [images_dict[i] for i in range(len(images_dict))]
            images[0].save(filename, save_all=True, append_images=images[1:], duration=100, loop=0, optimize=True)

            for frame in cls.frames:
                threading.Thread(target=os.remove, args=(frame,)).start()
        except Exception:
            print('ERROR CREATING GIF !!!')

def add_frame(images_dict, index, frame):
    images_dict[index] = Image.open(frame).convert("P")
