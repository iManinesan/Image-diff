from PIL import Image, ImageChops, ImageStat
import sys
import os



def diff(img1, img2):
    im1 = Image.open(img1)
    im2 = Image.open(img2)
    filename, file_extension = os.path.splitext(img1)
    diff_img_file = 'diff'+file_extension
    diff_img = ImageChops.difference(im1,im2)
    print 'Saving diff image as',diff_img_file
    diff_img.convert('RGB').save(diff_img_file)


def main():
    try:
        diff(sys.argv[1], sys.argv[2])
    except Exception as e:
        return e
    return 0

if __name__ == "__main__":
    sys.exit(main())
