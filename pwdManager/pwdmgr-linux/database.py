"Using SQLite3 database for storing the data locally on the machine"
import sqlite3
import os
"Importing the Encrypt class for encryption and decryption of databases"
from encrypt import Encrypt

class UserBase(): 
    """
        This UserBase() class contains all the methods/functions to manipulate
        the databases using the SQLite3 commands.Also contains some usefull 
        functions to delete the old and temporary databases.
    """

    def getdir(self):
        """
            Uses OS library module to detect the current working directory.That is used 
            to store the databases of different users.
            It returns the path->(str) Current working Directory whenever it is called.
        """
        return os.getcwd()

    def removeTemp(self,userName):
        """
            This module takes the username & self.path variable and remove any 
            temporary data that is not being used. 
            Thus the old databases is cleared successfully.
        """
        path = self.getdir() + '/'+ userName + '.db'
        os.remove(path)

    def removeOldDatabase(self,userName):
        path = self.getdir() + '/'+ userName + '.db.crypt'
        os.remove(path)

    def connectionEstablish(self,userName):
        self.conn = sqlite3.connect(userName+'.db')
        self.cursor = self.conn.cursor()

    def connectionEnd(self,userName):
        self.conn.commit()
        self.conn.close()

    def verify(self,userName,userPassword):
        try:
            Encrypt().decryptdata(userName,userPassword)
        except:
            return False
        else:
            path = self.getdir() + '/'+ userName + '.db'
            os.remove(path)
            return True

    def createUserAccount(self,userName,userPassword):
        conn = sqlite3.connect(userName+'.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE USER(SITE CHAR(50),USERNAME CHAR(50),PASSWORD CHAR(50))''')
        conn.commit()
        conn.close()
        Encrypt().encryptdata(userName,userPassword)
        self.removeTemp(userName)

    def showAllPassword(self,userName,userPassword):
        Encrypt().decryptdata(userName,userPassword)
        self.removeOldDatabase(userName)
        conn = sqlite3.connect(userName+'.db')
        cursor = conn.cursor()
        query = "SELECT * FROM USER"
        result = cursor.execute(query)
        print("Website\t  \tUser ID \t \tPassword \n")
        for i in result:
            print(i[0],end='')
            print("\t->\t",end='')
            print(i[1],end='')
            print("\t->\t",end='')
            print(i[2],end='\n')
        conn.commit()
        conn.close()
        Encrypt().encryptdata(userName,userPassword)
        self.removeTemp(userName)

    def displaySearchedPassword(self):
        pass
        
    def addEntry(self,userName,userPassword,site,id,password):
        Encrypt().decryptdata(userName,userPassword)
        self.removeOldDatabase(userName)
        self.connectionEstablish(userName)
        query = "INSERT INTO USER(SITE,USERNAME,PASSWORD) VALUES('"+site+"','"+id+"','"+password+"')"
        self.cursor.execute(query)
        self.connectionEnd(userName)
        Encrypt().encryptdata(userName,userPassword)
        self.removeTemp(userName)
        
if __name__ == "__main__":
    obj=UserBase()
    # obj.createUserAccount("utsav","123")
    # obj.addEntry("utsav","123","bbbb","bbbb","bbbbb")
    # obj.showAllPassword("utsav","123")
