# coding=utf-8
from PIL import Image
import numpy as np
import os


def is_image_file(filename):
    postfixes = ['.jpg', '.png', 'jpeg']

    if filename:
        filename_lower = filename.lower()
        for postfix in postfixes:
            if filename_lower.endswith(postfix):
                return True
    return False


def find_images(path):
    return [os.path.join(path, filename) for filename in os.listdir(path) if is_image_file(filename)]


SAVE_DIR = '/Users/zijiao/Documents/Books/English/words_merged'
SOURCE_DIR = '/Users/zijiao/Documents/Books/English/words'
OFFSET_L = 50
OFFSET_T = 51
OFFSET_R = 50
OFFSET_B = 45
SCALE = 1.
ROW = 6
COLUMN = 7

if __name__ == '__main__':
    images = find_images(SOURCE_DIR)
    n_images = len(images)
    print('%d images' % n_images)

    if COLUMN == 0:
        COLUMN = ROW

    n_images_per_page = ROW * COLUMN
    n_pages = n_images // n_images_per_page + int(bool(n_images % n_images_per_page))
    print('%d pages' % n_pages)
    item_shape = None

    for page in range(n_pages):
        page_data = []
        for row in range(ROW):
            row_data = []
            for column in range(COLUMN):
                index = page * n_images_per_page + row * COLUMN + column
                if index < n_images:
                    image = images[index]
                    im = Image.open(image)
                    im = im.crop([OFFSET_L, OFFSET_T, 1240 - OFFSET_R, 1754 - OFFSET_B])
                    if SCALE and SCALE != 1.:
                        width, height = im.size
                        im = im.resize((int(width * SCALE), int(height * SCALE)))
                    im_data = np.asarray(im)
                    if not item_shape:
                        item_shape = im_data.shape
                else:
                    im_data = np.full(item_shape, 255, dtype=np.uint8)
                row_data.append(im_data)
            row_im_data = np.hstack(row_data)
            page_data.append(row_im_data)
        page_im_data = np.vstack(page_data)
        page_im = Image.fromarray(page_im_data)
        page_im.show()
        page_im.save(os.path.join(SAVE_DIR, 'page%d.jpg' % page))
