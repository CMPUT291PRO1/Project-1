import sys
import cx_Oracle
import getpass

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
		ongoing = False
		print("===========================================================")
		print("Make a new auto transaction, enter 'N'.\n ")
            
		if input() == 'N':
            
            # connecting to database
			con = cx_Oracle.connect(conString);
			curs=con.cursor();	
		
			# check if the vehicle exists
			vehicle_id = input("\nPlease enter vehicle id:")
			curs.execute("SELECT serial_no FROM vehicle WHERE serial_no = '{}'".format(vehicle_id))
			try:	
				curs.fetchone()
			except:
				print("Vehicle Not Registered")
				
			seller_id = input("Seller_id:") 
			# check if the seller exists
			curs.execute("SELECT sin FROM people WHERE sin = '{}'".format(seller_id)  )
			try:
				curs.fetchone()
			except:	
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
				print("This seller does not own car '{}'".format(vehicle_id))
				break
			
			buyer_id = [] # in case there are more buyers
			buyer_id.append(input("Buyer_id:") )
			# check if the buyer_id exists
			if not curs.execute("SELECT sin FROM people WHERE sin = '{}'".format(seller_id)):
				print("Buyer not registered.")
				ch = input("Would you like to register a new buyer? y/n \n")
				if ch == 'n':
					print("Going back to main menu...")
				if ch == 'y':
					# register a new person into people database
					P3.regPerson(conString, curs)
				
				
            # check if this buyer is the primary owner
			is_primary = input("Is this a primary owner? y/n\n")			
			if is_primary == 'n':
				num = input("How many other owners? Enter the number:")
				for i in range(int(num)):
					buyer_id.append( input("Buyer_id:"))
                    
			# obtain date and price
			s_date = "'"+input("Sale Date:(YYYY-MM-DD)")+"'"
			price = input("Price:")
			
			# obtain the largest transaction_id			
			curs.execute("SELECT MAX(transaction_id) FROM auto_sale")			
			largest = curs.fetchone()
			transaction_id = int(largest[0]) + 1
			
            # add informatio to table auto_sale
			#curs.bindarraysize = 1
			#curs.setinputsizes(int, 15, 15, 15, date, float)
			statement = "INSERT INTO auto_sale VALUES ({}, {}, {}, {}, TO_DATE({},'YYYY-MM-DD'), {})"\
						.format(transaction_id, seller_id, buyer_id[0], vehicle_id, s_date, price) 
			curs.execute(statement)
			
			# add information to the new owner
			for i in range(len(buyer_id)):
				if i == 0:
					add = "INSERT INTO owner VALUES ('{}', '{}', '{}')"\
						.format(buyer_id[i], vehicle_id, 'y')
				else:
					add = "INSERT INTO owner VALUES ('{}', '{}', '{}')"\
						.format(buyer_id[i], vehicle_id, 'n')  
				curs.execute(add)

            # remove from old one
			curs.execute("DELETE FROM owner WHERE vehicle_id = '{}'".format(seller_id) )
			
			c = input("Would you like another transaction? y/n\n")
			if c == 'n':
                # close database connection
				con.commit()
				curs.close()
				return

		ongoing  = True
				
			
# for testing
#if __name__ == "__main__":
#	while(1):
#		AutoTransaction()		
	
		
		
	

    
    
	
	
