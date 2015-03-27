import sys
import cx_Oracle
import P1


def violation(conString):
        con = cx_Oracle.connect(conString);          
        curs = con.cursor()        
        owner=input('is this driver the primary owner of this vehicle? (y/n)')
        if owner.lower() == 'y':
                sqlcode=record(conString,curs)
                print(sqlcode)
                #con = cx_Oracle.connect(conString);          
                #curs = con.cursor()
                curs.execute(sqlcode)
                con.commit()
                curs.close
        elif owner.lower() == 'n':
                print()
                print('please enter the information of the primary owner of this vehicle')
                print()
                sqlcode1=record(conString,curs)
                print()
                print('please enter the information of the driver of this vehicle')
                print()
                sqlcode2=record(conString,curs)
                #con = cx_Oracle.connect(conString);          
                #curs = con.cursor()
                curs.execute(sqlcode1)
                curs.execute(sqlcode2)
                con.commit()
                curs.close
        else:
                print('Invalid input.')
            

def record(conString,curs):
        end=False
        while end==False:
                ticket_no =input("Enter ticket number :")
                vehicle_id = input("Enter vehicle ID :")
                exist2 =P1.searchSerial(vehicle_id, curs)
                if not exist2:
                        print("The vehicle is not registered. Please register first")
                        P1.regV(conString)                 
                violator_no = input("Enter violator :")
                exist1 = P1.searchSin(violator_no, curs)
                if not exist:
                        print("The person is not registered. Please register first")
                        P1.regPerson(conString)                     
                office_no = input("Enter officer ID :")
                vtype = input("Enter violation type:")
                vdate = input("Enter violation date (DD-Month-YY):")
                place = input("Enter place :")
                description = input("Enter description :")
        
                print("Ticket number: "+ticket_no+" Violator: "+violator_no+" Vehicle ID: "+vehicle_id+" Officer number: "+office_no+" Violation type: "+vtype+"Date: "+vdate+" Place: "+place+" Description: "+description)
                answer = input("If these information are correct, please enter y. If you want to re-enter, please enter n:")
                if answer=='y' or answer=='Y':
                        end=True
        
        statement = "insert into ticket values ('"+ticket_no+"','"+violator_no+"','"+vehicle_id+"','"+office_no+"','"+vtype+"','"+vdate+"','"+place+"','"+description+"')"
        return statement
        