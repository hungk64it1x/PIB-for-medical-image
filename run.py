import os
import pandas as pd
from skimage import data, io
from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from process import poisson_copy_paste
from utils import string2tuple
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--image-dir", type=Path, help="Path to images")
parser.add_argument("--mask-dir", type=Path, help="Path to masks")
parser.add_argument("--save-image-dir", type=str, help="Path to images")
parser.add_argument("--save-mask-dir", type=str, help="Path to masks")
parser.add_argument("--num-images", type=int, help="Number of images to gen")

args = parser.parse_args()

def single_generate_poisson(pos, tar, num_loop):
    offset = (40, 10)
    image_dir = "D:\Data\Polyps\TrainDataset\TrainDataset\image"
    mask_dir = "D:\Data\Polyps\TrainDataset\TrainDataset\mask"
    for i in tqdm(range(num_loop)):

        positive_img_path = f"{image_dir}/{pos}.png"
        positive_mask_path = f"{mask_dir}/{pos}.png"
        target_img_path = f"{image_dir}/{tar}.png"
        target_mask_path = f"{mask_dir}/{tar}.png"
        result = poisson_copy_paste(positive_img_path, positive_mask_path, target_img_path, target_mask_path, offset=offset)
        image = result['image']
        mask = result['mask']
        save_image_dir = "D:\Data\Polyps\poisson-gen\images"
        save_mask_dir = "D:\Data\Polyps\poisson-gen\masks"
        io.imsave(f'{save_image_dir}/{pos}_{tar}_{offset}.png', image)
        cv2.imwrite(f'{save_mask_dir}/{pos}_{tar}_{offset}.png', mask)

def random_generate_poisson(src, target, num_loop):
    for i in tqdm(range(num_loop)):
        pos = np.random.choice(src)
        tar = np.random.choice(target)
        a = np.random.randint(-50, 50)
        b = np.random.randint(-50, 50)
        offset = tuple((a, b))
        positive_img_path = f"{args.image_dir}/{pos}.png"
        positive_mask_path = f"{args.mask_dir}/{pos}.png"
        target_img_path = f"{args.image_dir}/{tar}.png"
        target_mask_path = f"{args.mask_dir}/{tar}.png"
        result = poisson_copy_paste(positive_img_path, positive_mask_path, target_img_path, target_mask_path, offset=offset)
        image = result['image']
        mask = result['mask']
        
        io.imsave(f'{args.save_image_dir}/{pos}_{tar}_{offset}.png', image)
        cv2.imwrite(f'{args.save_mask_dir}/{pos}_{tar}_{offset}.png', mask)

def random_generate_poisson_2(src, target, num_loop):
    
    target_img_path = r'D:\Data\Polyps\checked-poisson'
    names = os.listdir(f'{target_img_path}/images')
    
    for i in tqdm(range(num_loop)):
        pt = np.random.choice(names)
        image_id = pt.split('.')[0]
        pos = np.random.choice(src)
        
        a = np.random.randint(-50, 60)
        b = np.random.randint(-50, 60)
        offset = tuple((a, b))
        positive_img_path = f"{args.image_dir}/{pos}.png"
        positive_mask_path = f"{args.mask_dir}/{pos}.png"
        tg_img_path = f'{target_img_path}/images/{pt}'
        tg_mask_path = f'{target_img_path}/masks/{pt}'
        
        result = poisson_copy_paste(positive_img_path, positive_mask_path, tg_img_path, tg_mask_path, offset=offset)
        image = result['image']
        mask = result['mask']
        
        io.imsave(f'{args.save_image_dir}/{pos}_{image_id}_{offset}.png', image)
        cv2.imwrite(f'{args.save_mask_dir}/{pos}_{image_id}_{offset}.png', mask)

if __name__ == '__main__':
    
    df = pd.read_csv(r"D:\Data\Polyps\train.csv")
    src = df[df['area'] <= 90000]
    target = df.loc[~df.index.isin(src.index)]
    list_src = src['image_id'].values.tolist()
    list_target = target['image_id'].values.tolist()
    list_target = df['image_id'].values.tolist()
    random_generate_poisson(list_src, list_target, args.num_images)
    

    