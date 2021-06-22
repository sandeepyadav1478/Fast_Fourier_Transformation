from PIL import Image, ImageDraw
from json import load

def cordtoimage(size = (500,500), dotSize = 2,file_path="coordinate.txt",color = "black"):
    img = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(img)

    file= open(file_path,"r")
    coords = load(file)
    if len(coords) > 0:
        for (x,y) in coords:
            draw.rectangle([x,y,x+dotSize-1,y+dotSize-1], fill=color)
        img.show()
        return "Successfully Printed."
    else:
        return "No pixels available."
# cordtoimage()