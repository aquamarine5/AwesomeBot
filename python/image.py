from PIL import Image,ImageDraw,ImageFont
import sys

if(len(sys.argv)==3):
    if(sys.argv[1]=="yz"):
        text=sys.argv[2]
        fontSize=100
        if (len(text))>5:
            fontSize=80
        if(len(text))>6:
            fontSize=70
        if(len(text))>7:
            fontSize=60
        if(len(text))>8:
            fontSize=40
        font=ImageFont.truetype(r"C:\Windows\Fonts\simfang.ttf",fontSize)
        fillColor="#FFFFFF"
        fileIn=r"D:\Program Source\QQBOT\python\Source\yz.jpg"
        fileOut=r"D:\Program Source\QQBOT\python\Temp\temp.jpg"
        image=Image.open(fileIn)
        draw=ImageDraw.Draw(image)
        draw.text((9,457),text,font=font,fill = (0,0,0),direction=None)
        image.save(fileOut)
else:
    print("参数不够")