#
#    Copyright (C) {2015}  {Nicholas Carroll}

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import cx_Oracle
import getpass
import P1
import P2
import P3
import P4
import P5
import sys


run = True
login = True


while(login):
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user=getpass.getuser()
    pwd = getpass.getpass()
    
    conString = user + '/' + pwd + '@gwynne.cs.ualberta.ca:1521/CRS'
    
    try:
        con = cx_Oracle.connect(conString);
        
        login = False
    except:
        print("Wrong username or password.")

#This is to enable testing for myself.
#stdin = sys.stdin
#sys.stdin = open('simulatedInput.txt','r') 



while(run):

    
    print("\n1. New Vehicle Registration")
    print("2. Auto Transaction")
    print("3. Driver License Registration")
    print("4. Violation Record")
    print("5. Search Engine")
    selection = input("Please select your program number or 'exit':\n")
    
    
    try:
        digit = int(selection)
        if digit == 1:
            P1.regV(conString)
        elif digit == 2:
            P2.AutoTransaction(conString)
        elif digit == 3:
            P3.DriverLiRegis(conString)
        elif digit == 4:
            P4.violation(conString)
        elif digit == 5:
            P5.search_engine(conString)
        else:
            print("Must be between 1 and 5")
                
    except ValueError:
        if selection == 'exit':
            run = False
        else:
            print("Please enter a digit or 'exit'")
    
                 
