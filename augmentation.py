import numpy as np
import random
import cv2
from numpy.lib.type_check import imag

def do_random_hflip(image, mask):
    if np.random.rand()>0.5:
        image = cv2.flip(image,1)
        mask = cv2.flip(mask,1)
    return image, mask


# #--- geometric ---
def do_random_rotate(image, mask, mag=15 ):
    angle = np.random.uniform(-1, 1)*mag

    height, width = image.shape[:2]
    cx, cy = width // 2, height // 2

    transform = cv2.getRotationMatrix2D((cx, cy), -angle, 1.0)
    image = cv2.warpAffine(image, transform, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    mask = cv2.warpAffine(mask, transform, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

    return image, mask


def do_random_scale( image, mask, mag=0.1 ):
    s = 1 + np.random.uniform(-1, 1)*mag
    height, width = image.shape[:2]
    w,h = int(s*width), int(s*height)
    if (h,w)==image.shape[:2]:
        return image, mask

    dst = np.array([
        [0,0],[width,height], [width,0], #[0,height],
    ]).astype(np.float32)

    if s>1:
        dx = np.random.choice(w-width)
        dy = np.random.choice(h-height)
        src = np.array([
            [-dx,-dy],[-dx+w,-dy+h], [-dx+w,-dy],#[-dx,-dy+h],#
        ]).astype(np.float32)
    if s<1:
        dx = np.random.choice(width-w)
        dy = np.random.choice(height-h)
        src = np.array([
            [dx,dy], [dx+w,dy+h], [dx+w,dy],#
        ]).astype(np.float32)

    transform = cv2.getAffineTransform(src, dst)
    image = cv2.warpAffine( image, transform, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    mask = cv2.warpAffine( mask, transform, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return image, mask


def do_random_stretch_y( image, mask, mag=0.25 ):
    s = 1 + np.random.uniform(-1, 1)*mag
    height, width = image.shape[:2]
    h = int(s*height)
    w = width
    if h==height:
        return image, mask

    dst = np.array([
        [0,0],[width,height], [width,0], #[0,height],
    ]).astype(np.float32)


    if s>1:
        dx = 0#np.random.choice(w-width)
        dy = np.random.choice(h-height)
        src = np.array([
            [-dx,-dy],[-dx+w,-dy+h], [-dx+w,-dy],#[-dx,-dy+h],#
        ]).astype(np.float32)
    if s<1:
        dx = 0#np.random.choice(width-w)
        dy = np.random.choice(height-h)
        src = np.array([
            [dx,dy], [dx+w,dy+h], [dx+w,dy],#
        ]).astype(np.float32)

    transform = cv2.getAffineTransform(src, dst)
    image = cv2.warpAffine( image, transform, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    mask = cv2.warpAffine( mask, transform, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return image, mask



def do_random_stretch_x( image, mask, mag=0.25 ):
    s = 1 + np.random.uniform(-1, 1)*mag
    height, width = image.shape[:2]
    h = height
    w = int(s*width)
    if w==width:
        return image, mask

    dst = np.array([
        [0,0],[width,height], [width,0], #[0,height],
    ]).astype(np.float32)

    if s>1:
        dx = np.random.choice(w-width)
        dy = 0#np.random.choice(h-height)
        src = np.array([
            [-dx,-dy],[-dx+w,-dy+h], [-dx+w,-dy],#[-dx,-dy+h],#
        ]).astype(np.float32)
    if s<1:
        dx = np.random.choice(width-w)
        dy = 0#np.random.choice(height-h)
        src = np.array([
            [dx,dy], [dx+w,dy+h], [dx+w,dy],#
        ]).astype(np.float32)

    transform = cv2.getAffineTransform(src, dst)
    image = cv2.warpAffine( image, transform, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT, borderValue=0)
    mask = cv2.warpAffine( mask, transform, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT, borderValue=0)
    return image, mask


def do_random_shift( image, mask, mag=32 ):
    b = mag
    height, width = image.shape[:2]

    image = cv2.copyMakeBorder(image, b,b,b,b, borderType=cv2.BORDER_CONSTANT, value=0)
    mask  = cv2.copyMakeBorder(mask, b,b,b,b, borderType=cv2.BORDER_CONSTANT, value=0)
    x = np.random.randint(0,2*b)
    y = np.random.randint(0,2*b)
    image = image[y:y+height,x:x+width]
    mask = mask[y:y+height,x:x+width]

    return image, mask
def do_random_clahe(image, mag=[[2,4],[6,12]]):
    l = np.random.uniform(*mag[0])
    g = np.random.randint(*mag[1])
    clahe = cv2.createCLAHE(clipLimit=l, tileGridSize=(g, g))

    image = clahe.apply(image)
    return image

def agument(r):
    image = r['image']
    mask = r['mask']
    if 1:
        for fn in np.random.choice([
            lambda image, mask : do_random_scale(image, mask, mag=0.20),
            lambda image, mask : do_random_stretch_y(image, mask, mag=0.50),
            lambda image, mask : do_random_stretch_x(image, mask, mag=0.40),
            # lambda image, mask : do_random_shift(image, mask, mag=0.3),
            
            lambda image, mask : (image, mask)
        ],1):
            image, mask = fn(image, mask)

        for fn in np.random.choice([
            lambda image, mask : do_random_rotate(image, mask, mag=60),
            lambda image, mask : do_random_hflip(image, mask),
            lambda image, mask : (image, mask)
        ],1):
            image, mask = fn(image, mask)
        

    r['image'] = image
    r['mask'] = mask
    return r
