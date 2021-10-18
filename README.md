# Copy Paste positive polyp using poisson image blending for medical image segmentation

### According [poisson image blending](https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf) I've completely used it for biomedical image segmentation to increase dataset. Because Polyps segementation dataset does not enough have. <br> Wheares there are many tasks in medical using image to diagnose. This will help the doctors reduce time and pressure 💪
------------------------------------
### 1. Some examples of PIB copy paste

![image](https://user-images.githubusercontent.com/80585483/137695944-26c1efe6-cf51-4e5c-8d33-1acb435507b3.png)

• I think this type is so cool! <br> You can see new image after copy paste really like a real picture 😄

-----------------------------------
### 2. How to run
```
git clone https://github.com/hungk64it1x/PIB-for-medical-image
```
#### install requirements
```
pip install -r requirements.txt
```
or for Linux
```
sudo apt install -r requirements.txt
```
after that you should modify the image source (contain positive region) in file run.py from line 84 -> 89 because my implement that for Kvasir, Colon, Etis, Clinic and EndoScene dataset.
<br>Finally run run.py to generate copy image:
```
python3 run.py --image_dir [directory of image] --mask_dir [directory of mask] --save_image_dir [path save images] --save_mask_dir [path save masks] --num_images [number of image to generate]
```
------------------------------------

### 3. Acknowledgement
This research was implemented when I was in a research group funded by Vingroup Innovation Foundation conducted by PhD Sang D.V in HUST😄

-----------------------------------
### 4. References
- [Poisson image editing](https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf)
- [HarDnet-MSEG](https://github.com/james128333/HarDNet-MSEG)
- Specially thank to [github](https://github.com/yskmt/pb)
