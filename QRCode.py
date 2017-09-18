import qrcode
import random 
import string
import os

# Which file are we going to save it in
# FileName = ("EdCom_Dummy","EdCom_Real","Media_Dummy","Media_Real","Social_Media_Real")
# NumberOfCodes = (433,433,308,308,32);
# LengthOfCode  = (8,8,9,9,10,10); 
# FileName = ("Catapult_1","Catapult_2","Catapult_3","Catapult_4","Catapult_5","Catapult_6","Catapult_7","Catapult_8","Catapult_9","Catapult_10","Catapult_11","Catapult_12","Catapult_13","Catapult_14","Catapult_15","Catapult_16");
# NumberOfCodes = (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)
# LengthOfCode  = (7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7); 
FileName = ("EdCom_Real","Media_Real","JYW_First","JYW_Fourth","JYW_Second","JYW_Third");
NumberOfCodes = (72,12,12,12,12,12);
LengthOfCode  = (8,9,7,7,7,7)

# Where we at?
cwd = os.getcwd()

MySQLInput = open(cwd + "\\" + "Results.txt", 'w')

for i in range(0, len(FileName)):
	# Let's make the directory
	os.makedirs(FileName[i]);

	# Keep track of the codes we've made so far
	codes = []

	# Let's open the csv
	outputFile = open(cwd + "\\" + FileName[i] + "\\" + 'codes.csv', 'w')
	
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

		# Save it in the file we need it to be saved in
		img.save(cwd + "\\" + FileName[i] + "\\" + code + ".png")
	outputFile.close();