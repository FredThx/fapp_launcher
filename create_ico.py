from PIL import Image


img = Image.open("icon.jpg")
img = img.resize((256,256))
img.save("icon.ico", format='ICO')