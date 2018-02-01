#QR Code Generator for Waterloo Engineering Orientation
#Initially created by Awn Duquom for OWeek 2017
#Further developed by Kristopher Sousa for further OWeeks

import qrcode
import random 
import string
import os
from PIL import Image, ImageFont, ImageDraw 
import numpy as np


#### To Do List.... ####
# Adjust qr settings to have a higher quality QR code for the same size 
# Make QR code size variable
# Make # of QR codes per strip/sheet vary based on their size
# Consider relating data like details = [[File_name, NumOfCodes, LenOfCodes],[File_name, NumOfCodes, LenOfCodes],[File_name, NumOfCodes, LenOfCodes], ...] 
# Make font size vary based on length of code (figure out a good ratio with a fixed char width font [times?]) 
# Adjustable PDF border size
# Make it so you can added more sticker without deleting the current ones
	# New sheet, append to SQL .txt, append to .csv
# Build GUI
	# Varible number of sticker types (input for name, and number, and length)
	# save_each, _png and _pdf options
	# Size of QR codes in pxiels (try to provide a cm conversion ratio)


#### Functions ####
def concate_img_vert(imgs, filename=None):
	#imgs = list_im
	#imgs      = [ Image.open(i) for i in list_im ]

	# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
	min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]

	#Convert the images to one image
	imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
	
	#Convert the numpy array to an Image
	imgs_comb = Image.fromarray( imgs_comb, mode='L').convert('1')

	#Save the image
	if filename != None:
		imgs_comb.save( filename )
	
	return imgs_comb

def concate_img_horz(imgs, filename=None):
	#imgs = list_im
	#imgs      = [ Image.open(i) for i in list_im ]

	# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
	min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]

	#Convert the images to one image
	imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
	
	#Convert the numpy array to an Image
	imgs_comb = Image.fromarray( imgs_comb, mode='L').convert('1')

	#Save the image
	if filename != None:
		imgs_comb.save( filename )
	
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
NumberOfCodes = (2, 3)#,12,12,12,12);
LengthOfCode  = (8,9)#,7,7,7,7)

# Program Settings
code_width = 5
code_height = 6
save_each = True
save_png = True
save_pdf = False


# Some Temp lists so we don't have to save/load every image
img_list = []
img_strips = []
img_sheets = []

# Get the current directory of this code
cwd = os.getcwd()

# Make ...\QRCodes if it doesn't already exist
if not os.path.exists("QRCodes"):
	os.makedirs("QRCodes")

#Appends to the .txt instead of overwriting each time
MySQLInput = open(cwd + "\\" + "QRCodes" + "\\" + "Database Code.txt", 'a')

#For each type of QR Code
for i in xrange(0, len(FileName)):
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
	
	code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(LengthOfCode[i]))

	# For each code of the given type 
	for x in xrange(0, NumberOfCodes[i]):

		# Make the Code
		while( code in codes ):
			code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in xrange(LengthOfCode[i]))
			
		# Add it to the list
		codes.append(code)
		
		# Write the code into the file
		outputFile.write(code + ",\n");
		MySQLInput.write("INSERT INTO QRCodes (QRCode,Submitted,Type) VALUES ('" + code + "', 0,'" + FileName[i] + "'); \n\n")
		
		# Let's make the QRCode
			# Make our object
		qr = qrcode.QRCode(
			# Note: Modules here are the black/white boxes that make up the QR Code
			#version=1, 		#How Many modules is is square ie: Version 1 is 21 by 21 modules 2 is 25 by 25 modules etc
			error_correction=qrcode.constants.ERROR_CORRECT_Q, #Percent of error that can be corrected. Q is 25%  
			box_size=10, 	#How many pixels per module
			border=5,		#How many modules the border is made up of
		)
			#Insert Data
		#qr.add_data("engorientation.uwaterloo.ca/submitPoint.php?ID=" + code)
		qr.add_data(1)
		qr.make()
		img = qr.make_image()
		

		
		# # Let's make the QR code border bigger 
		# new_img = Image.new("1", (370, 420), "white")
		# new_img.paste(img, (0,0))
		# img = new_img
		w, h = img.size# For centering text

		img.show()
		print w, h
		import time
		time.sleep(10)
		
		# Let's add the QR Code's name below it
		draw = ImageDraw.Draw(img)
		# font = ImageFont.truetype(<font-file>, <font-size>)
		font = ImageFont.truetype("C:\Windows\Fonts\cour.ttf", 48)
		# draw.text((x, y),"Sample Text",(r,g,b)) 
		t_w, t_h = font.getsize(code) # For centering text
		draw.text(((w-t_w)/2,360),code,font=font, fill="black")

		# Image Concatenation into...
		img_list.append(img)
		# strips
		if len(img_list) == code_width:
			img_strips.append(concate_img_horz(img_list))
			img_list = []
		
		# sheets
		if len(img_strips) == code_height:
			img_sheets.append(concate_img_vert(img_strips))
			img_strips = []
		
		#Save each QR Codes as a PNG
		if save_each:
			img.save(cwd + "\\" + "QRCodes" + "\\" + FileName[i] + "\\" + code + ".png")

		pass #End of Loop

	#Fill remaining strip with blanks
	if len(img_list) != 0:
		#Create blank squares and add them to the list
		for _ in xrange(len(img_list), code_width):
			new_img = Image.new("1", (370, 420), "white")
			img_list.append(new_img)
		#Concat into a strip and save
		img_strips.append(concate_img_horz(img_list))

	#Fill remaining sheet with blanks
	if len(img_strips) != 0:
		#Create blank strip
		new_img = Image.new("1", (code_width*370, 420), "white")
		#Fill the rest of the strips with blank strips
		for _ in xrange(len(img_strips), code_height):
			img_strips.append(new_img)
		#Concat into a sheet and Save in img_sheets
		img_sheets.append(concate_img_vert(img_strips))

	#Save sheets as PNGs	
	if save_png:
		for j, s in enumerate(img_sheets):
			print "Saved sheet in " + FileName[i] + " " + str(j)
			s.save(cwd + "\\" + "QRCodes" + "\\" + FileName[i] + "\\" + "Sheet_"+ str(j) + ".png")

	#Save Sheets as PDFs
	if save_pdf:
		from reportlab.pdfgen import canvas
		from reportlab.lib.units import inch, cm
		from reportlab.lib.utils import ImageReader
		from reportlab.lib.pagesizes import letter

		c = canvas.Canvas(cwd + "\\" + "QRCodes" + "\\" + FileName[i] + "\\" + FileName[i] + ".pdf", pagesize=letter) #FIX LOCATION OF SAVE
		
		for j, s in enumerate(img_sheets):
			img = ImageReader(s)
			c.drawImage(img, 0.25*inch, 0.25*inch, 8*inch, 10.5*inch) #Allowed for a 0.25 inch border by placing it at point 0.25 inch 0.25 inch and making it width 8.5 - 0.25*2 inch and height 11 - 0.25*2 inch
			c.showPage()
		c.save()
	
	#Reset the temp variables
	img_list = []
	img_strips = []
	img_sheets = []

	#Close CSV
	outputFile.close()