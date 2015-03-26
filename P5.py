import sys
import cx_Oracle

def search_option1():
    statement = "SELECT p.name, l.licence_no, p.addr, p.birthday, l.class, dc.description, l.expiring_date FROM people p, drive_licence l, driving_condition dc, restriction r WHERE p.sin = l.sin AND l.licence_no = r.licence_no AND r.r_id = dc.c_id AND "
    choose=input("Please choose the way you want to search? (1: name. 2:drive licence number)")

    if choose == "1":
        name=input("Please input driver`s name: ")
        statement += "p.name = '"+name+"'"
        return statement
            
        
    elif choose == "2":
        number=input("Please input drive licence number: ")
        statement += "l.licence_no = '"+number+"'"
        return statement

def search_option2():
    statement="SELECT t.*,tt.fine FROM ticket t,ticket_type tt,drive_licence l WHERE t.vtype=tt.vtype AND "
    choose=input("Please choose the way you want to search? (1: sin of person. 2:drive licence number)")

    if choose == "1":
        sin=input("Please input sin of person: ")
        statement += "l.sin = '"+sin+"'"  
        return statement
        
    elif choose == "2":
        number=input("Please input drive licence number: ")
        statement += "l.licence_no = '"+number+"'"
        return statement
    
def search_option3():
    serial = input("Enter vehicle's serial number :")
    statement= "SELECT v.serial_no, count( DISTINCT a.transaction_id ), AVG( a.price ), count( DISTINCT t.ticket_no) FROM vehicle v, auto_sale a, ticket t WHERE t.vehicle_id (+)= v.serial_no AND a.vehicle_id (+)= v.serial_no And v.serial_no='"+serial+"' GROUP BY v.serial_no"
    return statement

def search_engine(conString):
    print()
    print("please follow the instructions to search.")
    print("(Press <ENTER> to continue)")
    input("")     
    con = cx_Oracle.connect(conString);          
    curs = con.cursor()
    while True:
        print()
        print("Search Menu")
        print()
        print("1.basis information of a driver")
        print("2.violation records of a person")
        print("3.vehicle history of a vehicle")
        print()
        user_input = input ("Please enter the search option number, or enter r to return to main menu: ")
        if user_input.lower() == 'r':
            return
        elif user_input == '1':
            sqlcode = search_option1()
        elif user_input == '2':
            sqlcode = search_option2()
        elif user_input == '3':
            sqlcode = search_option3()
        else:
            print()
            print('Invalid input.')
            continue
        #print(sqlcode)
        curs.execute(sqlcode)
        rows = curs.fetchall()
        #print(rows)
        if len(rows) == 0:
            print("No matches.")
        else:    
            for row in rows:
                for item in row:
                    print(item,end=" ")
                print()            
            
        print('Press <ENTER> to continue')
        input("")
        return_check=input("Enter n to start a new search, or r to return to return to Main Menu (n/r): ")
        if return_check.lower() == "r":
            return                     
    curs.close()    
    con.close()     
    
if __name__ == "__main__":
    search_engine()