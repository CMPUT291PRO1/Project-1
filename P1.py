import cx_Oracle
import P3

curs = None
con = None

def regV(conString):
    
    verify = False
    while(not verify):
        serialNo = input("Enter serial number: ").lower()
        maker = input("Enter Maker: ").lower()
        typeId =  input("Type ID#: ").lower()
        model = input("Enter Model: ").lower()
        year = input("Enter Year: ").lower()
        color = input("Enter color: ").lower()
        pOwner = None
        secondaryOwner = []
        primaryOwner = []
        
        verify = serialNo.isalnum() and maker.isalpha() and typeId.isdigit() and model.isalnum() and year.isdigit() and color.isalpha()
        if(not verify):
            
            print("\nError in entry, please ensure all data is correct")
            print("Serial: "+serialNo+" "+ str(serialNo.isalnum()))
            print("Maker: "+maker + " " + str(maker.isalpha()))
            print("Type ID#: "+ typeId + " " + str(typeId.isdigit()))
            print(" Model: " + model+ " " + str(model.isalnum()))
            print(" Year: " + year + " "+ str(year.isdigit()))
            print("Color: " + color+" " + str(color.isalpha()) +"\n")
            
    
    con = cx_Oracle.connect(conString);
    curs = con.cursor();
    if(searchSerial(serialNo, curs)):
        print("Vehicle already registered. Returning to main menu")
    else:
        count = int(input("How many drivers?"))
        x = 0
        while(x<count):
            ownerId = input("Enter owner SIN: ").lower()
            primary = input("Is primary owner? (y/n): ").lower()
            if(not(searchSin(ownerId, curs))):
                print("Person not found")
                P3.regPerson(conString, curs)
                
            if(primary=="y"):
                primaryOwner.append(ownerId)
            else:
                secondaryOwner.append(ownerId)
            x+=1   
        
            
        statement = " insert into vehicle values('" + serialNo + "','" + maker +"','" + model + "'," + year + ",'" + color + "'," + typeId + ")"
        try:
            curs.execute(statement)
        except:
            print("Sql error, try again.")
        
        for x in primaryOwner:
            print("PRIMARY: ")
            print(x)
            statement2 =" insert into owner values('" + x +"','" + serialNo +"','y')"
            try:
                curs.execute(statement2)
            except:
                print("Sql error, try again.")
                break
        
        for x in secondaryOwner:
            print("SECONDARY: ")
            print(x)
            statement3 =" insert into owner values('" + x +"','" + serialNo +"','n' )"
            try:
                curs.execute(statement3)
            except:
                print("Sql error, try again.")
                break
            
    con.commit()
    curs.close()
    con.close()
        
def searchSerial(serialNo, curs):
    query = "select * from vehicle where serial_no =" + serialNo
    try:
        curs.execute(query)
        curs.fetchall()
    
        x = curs.rowcount
        print(x)
        
        if(x>0):
            return True
        else:
            return False
    except:
        return False
    
def searchSin(ownerId, curs):
    query = "select * from people where sin =" + ownerId
    try:
        curs.execute(query)
        curs.fetchall()
        
        x = curs.rowcount
        print(x)
        
        if(x>0):
            return True
        else:
            return False
    except:
        return False
    
    