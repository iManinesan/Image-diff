from wand.image import Image



def diff(image1,image2):
    img1 = Image(filename=image1)
    img2 = Image(filename=image2)
    img3 = img1.compare(img2)
    return img3[0]
