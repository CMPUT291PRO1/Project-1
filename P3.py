import sys
import cx_Oracle
import time
import random

# for testing---------------------------------------------
#def DriverLiRegis():
# testing ends--------------------------------------------
def DriverLiRegis(conString):
	"""
	This component is used to record the information needed to issuing a drive licence, 
	including the personal information and a picture for the driver. 
	You may assume that all the image files are stored in a local disk system.
	
	drive_licence( licence_no,sin,class,photo,issuing_date,expiring_date)
	"""
	ongoing = True
	while(ongoing):
		# for testing-------------------------------------------
		#user = input("Username {} ".format(getpass.getuser()))
		#if not user:
		#	user = getpass.getuser()
		#pw = getpass.getpass()
		#conString = ''+user+'/'+pw+'@gwynne.cs.ualberta.ca:1521/CRS'
		# testing ends------------------------------------------		

		ongoing = False
		print("===========================================================")        
		print("Make a Driver Licence Registration, Enter 'N'.\n")
		
		if input() == 'N':
			# connecting to database
			con = cx_Oracle.connect(conString);
			curs=con.cursor();	
			"""   
			# generate a random num that does not exist in database
			print("Generating your licence number...")			
			l_num = ''.join(random.choice('ABCDEF') for i in range(3))+'-'+''.join(str(random.randint(1,9)) for i in range(4))
			print("Your licence number is: {}".format(l_num))
			"""
			checking = True
			while(checking):
				checking = False
				l_num = input("Your licence number is: (15 digits) ")
				curs.execute("SELECT licence_no FROM drive_licence WHERE licence_no = '{}'".format(l_num))
				if curs.fetchone():
					print("Licence exists.")
					checking = True
			
			checking = True
			while(checking):
				checking = False
				sin = input("Please enter your SIN:")
				#if sin.isalnum() or sin.isalalpha():
				#	checking = True
				curs.execute("SELECT sin FROM people where sin = '{}'".format(sin))
				# check if the person exists in people
				if not curs.fetchone():
					print("Person does not exist.")
					# if the person does not exist
					# ask user if to add new one or not
					ch = input("Would you like to register a new person? y/n \n")
					if ch == 'y':
						# register a new person into people database
						regPerson(conString, curs,sin)
					if ch == 'n':
						print("See you next time!")
						return
				
				# check if the driver has already got a licence
				# if so, raise error value
				curs.execute("SELECT sin FROM drive_licence WHERE sin = '{}'".format(sin))
				if curs.fetchone():
					print("Driver already registered.")
					checking = True
				
			l_class = input("Please enter the licence class:")
			
			# obtain a photo from disk
			file_name = input("Please enter your photo file name with suffix:")

			
			# check if all inputs are valid:
			if not l_num or not sin or not l_class or not file_name:
				print("\nAt least one of the input is none. Try again.")
				
			else:
				# open the photo
				photo_id  = open(file_name,'rb')
				photo  = photo_id.read()
				# prepare memory for operation parameters
				curs.setinputsizes(photo=cx_Oracle.LONG_BINARY)
				
				# Obtain current time as issuing time
				# expiring_date = issuing_date + 5 years
				issuing_date = time.strftime("%Y-%m-%d")
				e_year = int(time.strftime("%Y"))+5
				expiring_date = str(e_year) +'-'+time.strftime("%m-%d")
			
				state ="INSERT INTO drive_licence VALUES(:licence_no, :sin, :class, :photo, to_date(:issuing_date, 'YYYY-MM-DD'), to_date(:expiring_date,'YYYY-MM-DD'))"			
				curs.execute(state, {'licence_no':l_num, 'sin':sin, 'class':l_class, 'photo':photo, 'issuing_date':issuing_date, 'expiring_date':expiring_date})

			
			c = input("Would you like another registration? y/n\n")
			if c == 'n':
				# close database connection
				con.commit()
				curs.close()
			else:
				ongoing  = True

def regPerson(conString, curs, sin):
	run =True
	while(run):
		verify = False
		while(not verify):
			#sin = input("Enter sin number: ").lower()
			name = input("Enter Name: ").lower()
			height =  input("Height: ").lower()
			weight = input("Weight :").lower()
			eyeColor = input("Eye Colour: ").lower()
			hairColor = input("Hair Colour: ").lower()
			addr = input("Address: ").lower()
			gender = input("Gender (m/f): ").lower()
			birthday = input("Birthdate (YYYY-MM-DD): ")
	        
			verify = (sin.isalnum() and name.isalpha() and height.isdigit() and weight.isdigit() and eyeColor.isalpha() and hairColor.isalpha() and addr.isalnum() and (gender == 'm' or gender =='f'))      
			
			if(not verify):
				print("\nError in entry, please ensure all data is correct")
				print("Sin #: "+sin+" "+ str(sin.isalnum()))
				print("Name: "+name + " " + str(name.isalpha()))
				print("Height#: "+ height + " " + str(height.isdigit()))
				print(" Weight: " + weight+ " " + str(weight.isdigit()))
				print(" Eye Color: " +eyeColor + " "+ str(eyeColor.isalpha()))
				print("Hair Color: " + hairColor+" " + str(hairColor.isalpha()))
				print("Address: " + addr + str(addr.isalnum()))
				print("Gender: " + gender + str(gender == 'm' or gender =='f'))
				print("Birthday: " + birthday + "\n")
	
		statement = "insert into people values('"+sin+"','"+name+"',"+height+","+weight+", '"+eyeColor+"', '"+hairColor+"', '"+addr+"','"+gender+"',to_date('"+birthday+"','YYYY-MM-DD') )"
		#try:
		curs.execute(statement)
		run=False
		#except:
		#	cont = input("SQL Error, retry? Y/N").lower()
		#	if(cont != 'y'):
		#		run = False
				
		
				
# for testing-----------------------------------
#if __name__ == '__main__':
#	while(1):
#		DriverLiRegis()
#testing ends-----------------------------------
                
