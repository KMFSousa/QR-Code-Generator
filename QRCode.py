#QR Code Generator for Waterloo Engineering Orientation
#Initially created by Awn Duquom for OWeek 2017
#Edited by Kristopher Sousa for further OWeeks

import qrcode
import random 
import string
import os
from PIL import Image, ImageFont, ImageDraw 
import numpy as np

#### To Do List.... ####
# Save to a single PDF per sticker type
# Make QR code size variable
# Make # of QR codes per strip/sheet vary based on their size
# Consider relating data like details = [[File_name, NumOfCodes, LenOfCodes],[File_name, NumOfCodes, LenOfCodes],[File_name, NumOfCodes, LenOfCodes], ...] 
# Make font size varry based on length of code (figure out a good ratio with a fixed char width font [times?]) 
# Make it so you can added more sticker without deleting the current ones
	# New sheet, append to SQL .txt, append to .csv
# Build GUI
	# Varible number of sticker types (input for name, and number, and length)
	# save_each, _png and _pdf options
	# Size of QR codes in pxiels (try to provide a cm conversion ratio)


#### Functions ####
def concate_img_vert(list_im, filename=None):
	imgs = list_im
	#imgs      = [ Image.open(i) for i in list_im ]

	# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
	min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]

	#Convert the images to one image
	imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
	
	#Convert the numpy array to an Image
	imgs_comb = Image.fromarray( imgs_comb, mode='L').convert('1')

	#Save the image
	#imgs_comb.save( filename )
	return imgs_comb

def concate_img_horz(list_im, filename=None):
	imgs = list_im
	#imgs      = [ Image.open(i) for i in list_im ]

	# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
	min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]

	#Convert the images to one image
	imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
	
	#Convert the numpy array to an Image
	imgs_comb = Image.fromarray( imgs_comb, mode='L').convert('1')

	#Save the image
	#imgs_comb.save( filename )
	return imgs_comb

#### Main Program ####
# Fill remaining strip/sheet with blanks using Image.new(blah)
# Which file are we going to save it in
# FileName = ("EdCom_Dummy","EdCom_Real","Media_Dummy","Media_Real","Social_Media_Real")
# NumberOfCodes = (433,433,308,308,32);
# LengthOfCode  = (8,8,9,9,10,10); 
# FileName = ("Catapult_1","Catapult_2","Catapult_3","Catapult_4","Catapult_5","Catapult_6","Catapult_7","Catapult_8","Catapult_9","Catapult_10","Catapult_11","Catapult_12","Catapult_13","Catapult_14","Catapult_15","Catapult_16");
# NumberOfCodes = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)
# LengthOfCode  = (7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7); 

FileName = ("EdCom_Real","Media_Real")#,"JYW_First","JYW_Fourth","JYW_Second","JYW_Third");
NumberOfCodes = (20, 12)#,12,12,12,12);
LengthOfCode  = (8,9)#,7,7,7,7)

# Some Temp lists so we don't have to save/load every image
img_list = []
img_strips = []
img_sheets = []

# Where we at?
cwd = os.getcwd()

# Make ...\QRCodes if it doesn't already exist
if not os.path.exists("QRCodes"):
	os.makedirs("QRCodes")

#Appends to the .txt instead of overwriting each time
MySQLInput = open(cwd + "\\" + "QRCodes" + "\\" + "Database Code.txt", 'a')

for i in range(0, len(FileName)):
	# Let's make the directory (If it exists delete it's contects)
	if not os.path.exists("QRCodes" + "\\" + FileName[i]):
		os.makedirs("QRCodes" + "\\" + FileName[i])
	else:
		import shutil
		shutil.rmtree("QRCodes" + "\\" + FileName[i], ignore_errors=True) #Requires that you do not have that folder open
		os.makedirs("QRCodes" + "\\" + FileName[i])

	# Keep track of the codes we've made so far
	codes = []

	# Let's open the csv
	outputFile = open(cwd + "\\" + "QRCodes" + "\\" + FileName[i] + "\\" + FileName[i]+ ' Codes.csv', 'w')
	
	code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(LengthOfCode[i]))

	for x in range(0, NumberOfCodes[i]):
		# Make our object
		qr = qrcode.QRCode(
			version=1,
			error_correction=qrcode.constants.ERROR_CORRECT_L,
			border=2,
		)
		# Make the Code
		while( code in codes ):
			code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(LengthOfCode[i]))
			
		# Add it to the list
		codes.append(code)
		
		# Write the code into the file
		outputFile.write(code + ",\n");
		MySQLInput.write("INSERT INTO QRCodes (QRCode,Submitted,Type) VALUES ('" + code + "', 0,'" + FileName[i] + "'); \n\n")
		
		# Let's make the QRCode
		qr.add_data("engorientation.uwaterloo.ca/submitPoint.php?ID=" + code)
		qr.make()
		img = qr.make_image()

		# Let's make the QR code border bigger 
		new_img = Image.new("L", (370, 420), "white")
		new_img.paste(img, (0,0))
		img = new_img
		w, h = img.size# For centering text
		
		# Let's add the QR Code's name below it
		draw = ImageDraw.Draw(img)
		# font = ImageFont.truetype(<font-file>, <font-size>)
		font = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", 48)
		# draw.text((x, y),"Sample Text",(r,g,b)) 
		t_w, t_h = font.getsize(code) # For centering text
		draw.text(((w-t_w)/2,360),code,font=font, fill="black")
		
		# Image Concatenation into...
		img_list.append(img)
		# strips
		if len(img_list) == 5:
			img_strips.append(concate_img_horz(img_list))
			img_list = []
		
		# sheets
		if len(img_strips) == 6:
			img_sheets.append(concate_img_vert(img_strips))
			img_strips = []
		
		# the remaining QR Codes with blank pictures
		if x == NumberOfCodes[i] - 1:
			#Fill remaining strip with blanks
			if len(img_lsit) != 0:
				pass
			
			#Fill remaining sheet with blanks
			if len(img_strips) != 0:
				pass


		if save_each:
			img.save(cwd + "\\" + "QRCodes" + "\\" + FileName[i] + "\\" + code + ".png")

		if save_png:
			for j, s in enumerate(img_sheets):
				print "Saved sheet in " + FileName[i] + " " + str(i)
				s.save(cwd + "\\" + "QRCodes" + "\\" + FileName[i] + "\\" + "Sheet_"+ str(i) + ".png")

		if save_pdf:
			pass

		# Let's make the images into a PDF 
			#Once this is done we can stop savin each QR code seperatly and maybe stop deleting the folder	
	
	#Reset the temp variables
	img_list = []
	img_strips = []
	img_sheets = []

	outputFile.close()