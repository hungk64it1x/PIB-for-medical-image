import matplotlib.pyplot as plt
import numpy as np
import albumentations as A
import cv2
from augmentation import agument
from numpy.core.defchararray import count

def plot_augment(r, num_gen=12):
    nrows = 4
    ncols = 3
    f, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(40, 40))
    count = 0
    for i in range(nrows):
        for j in range(ncols):
            image = agument(r)['image']
            ax[i][j].imshow(image)
            ax[i][j].set_title(count)
            ax[i][j].axis('off')
            count += 1
    plt.show()

def plot_src_tar(source, des):
    f, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 20))
    ax[0].imshow(source)
    ax[0].set_title('source')
    ax[1].imshow(des)
    ax[1].set_title('new')

def plot_img_mask(image, mask):
    f, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 15))
    ax[0].imshow(image)
    ax[0].set_title('image')
    ax[1].imshow(mask, cmap='gray')
    ax[1].set_title('mask')

def string2tuple(x):
    return tuple((int(x[0]), int(x[1])))


def pad_images_to_same_size(images):
    """
    :param images: sequence of images
    :return: list of images padded so that all images have same width and height (max width and height are used)
    """
    width_max = 224
    height_max = 224
    for img in images:
        h, w = img.shape[:2]
        width_max = max(width_max, w)
        height_max = max(height_max, h)

    images_padded = []
    for img in images:
        h, w = img.shape[:2]
        diff_vert = height_max - h
        pad_top = diff_vert//2
        pad_bottom = diff_vert - pad_top
        diff_hori = width_max - w
        pad_left = diff_hori//2
        pad_right = diff_hori - pad_left
        img_padded = cv2.copyMakeBorder(img, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=0)
        assert img_padded.shape[:2] == (height_max, width_max)
        images_padded.append(img_padded)

    return images_padded

def check_overlap(src, des):
    area1 = cv2.countNonZero(src)
    area2 = cv2.countNonZero(des)
    area = area1 + area2 
    fusion = src + des
    area3 = cv2.countNonZero(fusion)
    if area == area3:
        return True
    return False

