import os
from cryptography.fernet import Fernet
from pathlib import Path

print ("  ______ _ _        ______                             _             ")
print (" |  ____(_) |      |  ____|                           | |            ")
print (" | |__   _| | ___  | |__   _ __   ___ _ __ _   _ _ __ | |_ ___ _ __  ")
print (" |  __| | | |/ _ \\ |  __| | '_ \\ / __| '__| | | | '_ \\| __/ _ \\ '__| ")
print (" | |    | | |  __/ | |____| | | | (__| |  | |_| | |_) | ||  __/ |    ")
print (" |_|    |_|_|\\___| |______|_| |_|\\___|_|   \\__, | .__/ \\__\\___|_|    ")
print ("                                            __/ | |                  ")
print ("                                           |___/|_|                  ")
print ("File Ecrypter 1.0 by cuenca125")
print ("")
print ("")
print ("")
print ("")

#Print Options.
print ("Please select an option:")
enc = "1.Encrypt files"
dec = "2.Decrypt files"
print (enc)
print (dec)

#Ask User to input his option choise.
print("")
option = int(input("Option number: "))

#Checks if the option chosen is valid, (crashes if it's not a number).
def option_check():
    global option
    global enc
    global dec
    while option != 1 and option != 2:
        print("")
        print ("please select a valid option")
        print (enc)
        print (dec)
        print("")
        option = int(input("Option number: "))
    return True    

#Prints the option chosen and checks if it's valid again.   
if option_check () == True:
    if option == 1:
        print ("You have selected to encrypt files")
        #Ask user for a file or directory to Encrypt.
        path = input("Path of files or directory to encrypt:")
    elif option == 2:
        print ("You have selected to decrypt files")
        #Ask user for a file or directory to Decrypt.
        path = input("Path of files or directory to decrypt:")
    else:
        print ("Your option doesn't exist, pass the check first.")
        option_check()

#Check if path entered is a valid file or directory.
def path_check():
    global path
    obj = Path(path)
    if obj.exists() == True:
        return True
    elif obj.exists() == False:
        return False
    

#In case the path is wrong or doesnt exist, ask again until given a valid path.
while path_check() == False:
    path = input("Please enter a valid path:")
    path_check()

#Check to see if its a directory
def dir_check():
    obj = Path(path)
    if obj.is_dir() == True:
        return True

#Check to see if its a file
def file_check():
    obj = Path(path)
    if obj.is_file() == True:
        return True
    
#Checks if there is already a keyfile on the user directory.
exist = False

def check_key_exist():
    global exist
    user = os.path.expanduser('~') + "\\"
    print("Searching for key...")
    for root, dirs, files in os.walk(user):
        for file in files:
            if file.endswith('.key'):
                print("")
                keyfile = root + "\\" + str(file)
                print(f"Key file found: {keyfile}")
                exist = True
                return exist
    
check_key_exist()

if exist == False:
    print("No key file was found, creating new key...")
    key = Fernet.generate_key()
    with open('keyfile.key', 'wb') as keyfile:
        keyfile.write(key)
        keyfile_path = f"{Path.cwd()}" + "\\" + "filekey.key"
        print(f"Created key succesfully: {keyfile_path}")
    
with open('keyfile.key', 'rb') as filekey:
    key = filekey.read()
    fernet = Fernet(key)

#When Path exists and encryption is chosen, test for directory or file and encrypt.
if path_check() == True and option == 1:
    obj = Path(path)
    
    #Encrypt file
    if file_check() == True:
        print("")
        print(f"Encrypting file: \"{obj}\"")
        
        #Encrypts the file
        with open(f'{obj}', 'rb') as file:
            original = file.read()
            
        #encripts the file
        encrypted = fernet.encrypt(original)
        with open(f'{obj}', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
            
        #Renames file
        newname = f"{obj}" + ".enc"
        os.rename(f'{obj}',f'{newname}')
        print("Encrypted Successfully \n")
        print(f"Saved as {newname}")
        print("")
        
        
        
        
    #Encrypt Directory files
    if dir_check() == True:
        print("")
        print(f"Encrypting directory: \"{obj}\"")
        print("")
        
        for file in obj.glob("*"):
            file_path = f"{obj}" + "\\" + f"{file.name}"
            oldname = file.name
            print(f"Opened {oldname}")
            
            #Encrypts the file
            with open(f'{file_path}', 'rb') as file:
                original = file.read()
            
            #encripts the file
            encrypted = fernet.encrypt(original)
            with open(f'{file_path}', 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
            
            #Renames file
            newname = f"{file.name}" + ".enc"
            os.rename(f'{file.name}',f'{newname}')
            print("Encrypted Successfully")
            print(f"Saved as {newname} \n")
            
            
#When Path exists and decryption is chosen, test for directory or file and decrypt.
if path_check() == True and option == 2:
    obj = Path(path)
    
    #Decrypt file
    if file_check() == True:
        print("")
        print(f"Decrypting file: \"{obj}\"")
        
        #decrypts the file
        with open(f'{obj}', 'rb') as enc_file:
            encrypted = enc_file.read()
            
        #decripts the file
        decrypted = fernet.decrypt(encrypted)
        with open(f'{file_path}', 'wb') as dec_file:
            dec_file.write(decrypted)
            
        #Renames file
        oldname = obj
        idx = oldname.find(".enc")
        if idx != -1:
            newname = oldname[:idx]
        os.rename(oldname, newname)
        print("Decryption Successfull \n")
        print(f"Saved as {newname}")
        print("")
        
        
        
        
    #Decrypt Directory files
    if dir_check() == True:
        print("")
        print(f"Decrypting directory: \"{obj}\"")
        print("")
        
        for file in obj.glob("*"):
            file_path = f"{obj}" + "\\" + f"{file.name}"  
            oldname = file.name
            print(f"Opened {oldname}")
            
            #Decrypts the file
            with open(f'{file_path}', 'rb') as enc_file:
                encrypted = enc_file.read()
            
            #Decripts the file
            decrypted = fernet.decrypt(encrypted)
            with open(f'{file_path}', 'wb') as dec_file:
                dec_file.write(decrypted)
            
            #Renames file
            oldname = file_path
            idx = oldname.find(".enc")
            if idx != -1:
                newname = oldname[:idx]
            os.rename(oldname, newname)
            print("Decryption Successfull")
            print(f"Saved as {newname} \n")
            
#22/05/2025
#To do:
# - work some way to stop using absolute paths
# - implement a key.file selection (for files encripted with diferent keys)
# - idk make it better?
# - be proud of yourself
# - thank the users for using it <3