import os
import sys
import Image
#The pilow library is required
print("Please cut the picture to the size you want in advance!")
fileName = input("Enter the file name (the file needs to be in the same directory):")
im=Image.open(fileName)
hight = im.size[1]
width = im.size[0]
msg = "Image Width:%d ,Height:%d" % (width, hight)
print(msg)
print("Transcoding...")
arrlen = hight * width *2
with open("img.h","w") as headf:
	print("#ifndef _IMG_H_",file = headf)
	print("#define _IMG_H_",file = headf)
	print("//The code is used for MCU of MCS-51 core. If it is used for MCU of other cores, please modify the code yourself",file = headf)
	print("const unsigned char code gImage_img[];",file = headf)
	print("#endif",file = headf)
headf.close()
with open("img.c","w") as f:
	print('#include "img.h"',file = f)
	print("const unsigned char code gImage_img[%d]={" % (arrlen),file = f)
	pix = im.load()  #load pixel array
	len = 0
	for h in range(hight):
		for w in range(width):
			if w < im.size[0]:
				R=pix[w,h][0]>>3
				G=pix[w,h][1]>>2
				B=pix[w,h][2]>>3
				rgb = (R<<11)|(G<<5)|B
				rgbH = (rgb>>8) & 0xff
				rgbL = rgb&0xff
				datH = "0x%x," % (rgbH)
				datL = "0x%x," % (rgbL)
				if rgbH&0xF0 == 0:
					datH =  "0x0%x," % (rgbH)
				if rgbL&0xF0 == 0:
					datL =  "0x0%x," % (rgbL)
				print(datL,end="",file = f)
				print(datH,end="",file = f)
			else:
				rgb = 0
				print("0x00,",end="",file = f)
			len+=1
			if len == 8:
				print("",end="\n",file = f)
				len = 0
	print("};",file = f)
f.close()
print("Done!")
os.system("pause")
