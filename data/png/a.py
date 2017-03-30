from wand.image import Image

with Image(filename='1.png') as img:
    img.format = 'jpeg'
    img.save(filename='pikachu.jpg')
