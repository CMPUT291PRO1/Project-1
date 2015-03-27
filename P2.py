import sys
import cx_Oracle
import getpass
import P3

# for testing---------------------------------------------
#def AutoTransaction():
# testing ends--------------------------------------------
def AutoTransaction(conString):
	"""
	This component is used to complete an auto transaction. 
	Your program shall allow the officer to enter all necessary information to complete this task, 
	including the details about the seller, the buyer, the date, and the price. 
	The component shall also remove the relevant information of the previous ownership.
	
	auto_sale (transaction_id,seller_id,buyer_id,vehicle_id,s_date,price);
	"""
	# for testing-------------------------------------------
	#user = input("Username {} ".format(getpass.getuser()))
	#if not user:
	#	user = getpass.getuser()
	#pw = getpass.getpass()
	#conString = ''+user+'/'+pw+'@gwynne.cs.ualberta.ca:1521/CRS'
	# testing ends------------------------------------------	
	
	ongoing = True
	while(ongoing):
		print("===========================================================")
		print("Make a new auto transaction, enter 'N'.\n ")
            
		if input() == 'N':
            
            # connecting to database
			con = cx_Oracle.connect(conString);
			curs=con.cursor();	
		
			# check if the vehicle exists
			checking = True
			while(checking):
				checking = False
				vehicle_id = input("\nPlease enter vehicle id:")
				try:
					val = str(vehicle_id)
				except ValueError:
					print("Invalid Input Type. Try Again.")
				curs.execute("SELECT serial_no FROM vehicle WHERE serial_no = '{}'".format(vehicle_id))
				if not curs.fetchone():
					print("Vehicle Not Registered")
					checking = True
				
			checking = True
			while(checking):		
				checking = False		
				seller_id = input("Seller_id:") 
				# check if the seller exists
				curs.execute("SELECT sin FROM people WHERE sin = '{}'".format(seller_id)  )
				if not curs.fetchone():
					print("Seller not registered.")		
							
				# check if the seller owns the vehicle
				curs.execute("SELECT vehicle_id FROM owner WHERE owner_id = '{}'".format(seller_id))
				vehicles = []
				row = curs.fetchone()
				while row:
					vehicles.append(row[0].strip())
					row = curs.fetchone()
				#print(vehicles)
				if not vehicle_id in vehicles:
					print("This seller does not own car '{}'\n".format(vehicle_id))
					checking = True
				
			checking = True
			all_owners = []
			while(checking):
				checking = False
				buyer_id = [] # in case there are more buyers
				buyer_id.append(input("Buyer_id:") )
				# check if the buyer_id exists
				curs.execute("SELECT sin FROM people WHERE sin = '{}'".format(buyer_id[0]))
				if not curs.fetchone():
					print("Buyer not registered.")
					ch = input("Would you like to register a new buyer? y/n \n")
					if ch == 'y':
						# register a new person into people database
						P3.regPerson(conString, curs,buyer_id[0])
					if ch == 'n':
						print("See you next time!")
						return
				# check if the buyer is an owner
				curs.execute("SELECT owner_id FROM owner WHERE vehicle_id = '{}'".format(vehicle_id))
				owners = []
				row = curs.fetchone()
				while row:
					owners.append(row[0].strip())
					row = curs.fetchone()	
				if buyer_id[0] in owners:
					print("Buyer owns car {}, enter buyer ID again.".format(vehicle_id))
					checking = True		
				else: all_owners = owners
				
				
            # check if this buyer is the primary owner
			is_primary = input("Are there any secondary owners? y/n\n")
		
			if is_primary == 'y':
				num = input("How many other owners? Enter the number:")
				for i in range(int(num)):
					checking = True
					while(checking):
						checking = False
						bid = input("Buyer_id:")
						if bid in all_owners:
							print("Buyer owns car {}, enter buyer ID again.".format(vehicle_id))
							checking = True
						if bid == buyer_id[0]:
							print("Invalid secondary buyer ID. Enter again.")
							checking = True
						curs.execute("SELECT sin FROM people WHERE sin = '{}'".format(bid))
						if not curs.fetchone():
							print("Buyer not registered.")
							checking = True
						else:
							buyer_id.append(bid)

                    
			# obtain date and price
			s_date = "'"+input("Sale Date:(YYYY-MM-DD )")+"'"
			checking = True
			while(checking):
				checking = False
				try:		
					price = float(input("Price:"))
				except ValueError:
					print("Invalid input!")
					checking = True
									
		
			# obtain the largest transaction_id			`
			curs.execute("SELECT MAX(transaction_id) FROM auto_sale")			
			largest = curs.fetchone()
			transaction_id = int(largest[0]) + 1
			
            # add informatio to table auto_sale
			#curs.bindarraysize = 1
			#curs.setinputsizes(int, 15, 15, 15, date, float)

			statement = "INSERT INTO auto_sale VALUES ('{}', '{}', '{}', '{}', TO_DATE({},'YYYY-MM-DD'), {})"\
						.format(transaction_id, seller_id, buyer_id[0], vehicle_id, s_date, price) 
			curs.execute(statement)
			
			# add information to the new owner
			# I assumed that the first buyer id entered to be primary owner
			for i in range(len(buyer_id)):
				if i == 0:
					add = "INSERT INTO owner VALUES ('{}', '{}', '{}')"\
						.format(buyer_id[i], vehicle_id, 'y')
				else:
					add = "INSERT INTO owner VALUES ('{}', '{}', '{}')"\
						.format(buyer_id[i], vehicle_id, 'n')  
				curs.execute(add)

            # remove from old one
			curs.execute("DELETE FROM owner WHERE owner_id = '{}'".format(seller_id) )
			
			c = input("Would you like another transaction? y/n\n")
			if c == 'n':
                # close database connection
				con.commit()
				curs.close()
				ongoing = False
			else:
				ongoing  = True
				
			
# for testing
#if __name__ == "__main__":
#	while(1):
#		AutoTransaction()		
	
