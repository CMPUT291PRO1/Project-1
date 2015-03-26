import sys
import cx_Oracle

conString = 'nmcarrol/mo4ZX5uW82@gwynne.cs.ualberta.ca:1521/CRS'
con = cx_Oracle.connect(conString);
curs = con.cursor();

file_name = input("Please enter your photo file name with suffix:")
photo_id  = open(file_name,'rb')
image  = photo_id.read()
# prepare memory for operation parameters
curs.setinputsizes(image=cx_Oracle.LONG_BINARY)


insert = """insert into test (image)
   values (:image)"""
curs.execute(insert,{'image':image})

con.commit()
curs.close()
con.close()