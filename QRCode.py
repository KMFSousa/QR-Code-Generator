#QR Code Generator for Waterloo Engineering Orientation
#Initially created by Awn Duquom for OWeek 2017
#Edited by Kristopher Sousa for further OWeeks

import qrcode
import random 
import string
import os
from PIL import Image, ImageFont, ImageDraw 

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
		print x
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
		new_img = Image.new("RGB", (370, 420), "white")
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

		# Save it in the file we need it to be saved in
		img.save(cwd + "\\" + "QRCodes" + "\\" + FileName[i] + "\\" + code + ".png")
	outputFile.close()