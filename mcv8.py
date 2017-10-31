#!/usr/bin/python3.5
import os, shutil, sys, re, pyperclip, argparse, binascii, math

#Brutal Cipher v1
#Formally known as Master Crypt
#By, codeDirtyToMe
#Started 26 Feb 2017
"""This application will use a number of XOR ciphers and transposition ciphers. This will be my
first attempt at doing a serious bitwise cipher."""

#Notes#########################################################################################################
"""24 September 2017 : Added options and arguments. Started putting the menu system together."""
"""I really need to create a flow chart for this as the menu is starting to get out of control."""

"""25 September 2017 : Started a flowchart. It has helped a ton. Using a lot of global
variables. That's not recommended, but it's the best way I can think of doing it considering
the application will only be enciphering or deciphering at any one time. I suppose there's a
slight chance of an old key or message hanging around if the application is used to encipher
or decipher more than one message in a single session. Actually, the likelyhood is probably
the same. Ascii to binary function created and working. The key and plain/cipher texts can and
will be converted to binary."""

"""9 October 2017 : Started to use classes to cut down on the number of global variables. I
have it working for the plainText variable assigned to class message() and the passKey variable
assigned to the class key. The intent is to only use two main variables; one of class type 
message and one of class type key. I really need to sharpen my flowchart game before continuing.
This code is starting to get a bit unwieldy."""

"""10 October 2017 : Encryption works with a basic XOR cipher as long as the password is <= to
the length of the message. I still need to be able to cut excess bits of the password in the
rare occasion when the password is longer than the message. Perhaps I should just return a 
condescending message if this occurs."""

#Set up the options.
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filein", type=str, help="\"message to be enciphered or deciphered.\"")
parser.add_argument("-k", "--key", type=str, help="Encryption/Decryption key. Put in quotes if white space is included.")
parser.add_argument("-e", "--encrypt", help="encrypt the message", action="store_true")
parser.add_argument("-d", "--decrypt", help="decrypt the message", action="store_true")
parser.add_argument("-c", "--clip", help="output to clipboard", action="store_true")
parser.add_argument("-t", "--trans", help="apply transposition or de-transposition", action="store_true")
parser.add_argument("-n", "--nooutput", help="Do NOT output to file", action="store_true")
parser.add_argument("-z", "--noclip", help="Do NOT output to clipboard", action="store_true")
arguments = parser.parse_args()

#Parse the options and arguments.
argFileIn = arguments.filein
argEncrypt = arguments.encrypt
argDecrypt = arguments.decrypt
argClip = arguments.clip
argTrans = arguments.trans
argKey = arguments.key
argNoOutput = arguments.nooutput
argNoClip = arguments.noclip

#Global Variables################################################################################################
class key() :
    def __init__(self, plain = "", bin = "", ext_bin = "", decimal = "") :
        self.plain = plain
        self.bin = bin
        self.ext_bin = ext_bin
        self.decimal = decimal

    def decVal(self) : #Method for converting key to base 10 IOT be used with Collatz conjecture.
        if self.ext_bin != '' :
            return int(self.ext_bin, 2)
        elif self.bin != '' :
            return int(self.bin, 2)
        else :
            print("Your key length is < the message. What is wrong with you?")
            exit(1) #Should only happen if message is less than key. Not likely.

class message() :
    def __init__(self, plainText = "", cipherText = "", plainBin = "", cipherBin = ""):
        self.plainText = plainText
        self.cipherText = cipherText
        self.plainBin = plainBin
        self.cipherBin = cipherBin

plainText = message()
passKey = key()
cipherText = message()
mainMenuChoice = str()

#Functions########################################################################################################

#Banner###########################################################################################################
def banner() :
    print("--------Brutal Cipher v1-----------")
    return

#Key Input########################################################################################################
def keyCollection() :
    os.system('clear')
    banner()
    passKey.plain = input("\nEnter the key \u2192 ") #Manual key collection.
    os.system('clear')
    return passKey.plain

#Input Menu#######################################################################################################
def inputMenu(choiceFromMainMenu) :
    #Allow global assigning.
    global mainMenuChoice

    #Display menu and as for file or interactive input.
    os.system('clear')
    banner()
    print("\u2192 F : File input                  |")
    print("\u2192 I : Interactive input           |")
    print("\u2192 X : Exit                        |")
    print("-----------------------------------")
    inputChoice = input("Choice \u2192 ")

    #Test for correct input.
    if inputChoice == "F" or inputChoice == "f" or inputChoice == "I" or inputChoice == "i" or inputChoice == "X" or inputChoice == "x" :
        if inputChoice == "I" or inputChoice == "i" :
            if mainMenuChoice == "E" or mainMenuChoice == "e" :
                plainText.plainText = input("Enter your message: ")
                return plainText.plainText
            elif mainMenuChoice == "D" or mainMenuChoice == "i" :
                cipherText.cipherText = input("Enter the ciphertext: ")
                return cipherText.cipherText
            else :
                print("Major Error: exit 1")
                exit(1)

        elif inputChoice == "f" or inputChoice == "F" :
            print()
            exit(0)
            #fileMenu()
        elif inputChoice == "X" or inputChoice == "x" :
            exit(0)
    else:
        print("Error : Invalid selection.")
        os.system('clear')
        inputMenu()

#Main Menu######################################################################################################
def mainMenu() :
    global mainMenuChoice
    
    #Display main menu and ask for input.
    banner()
    print("\u2192 E : Encipher                    |")
    print("\u2192 D : Decipher                    |")
    print("\u2192 X : Exit                        |")
    print("-----------------------------------")
    mainMenuChoice = input("Choice \u2192 ")

    #Test for correct entry
    if mainMenuChoice == "E" or mainMenuChoice == "e" or mainMenuChoice == "D" or mainMenuChoice == "d" :
        if argFileIn is not None : #If a file argument was given, go to file selection.
            print("not empty")
        else : #Encipher or Decipher was chosen.
            inputMenu(mainMenuChoice)
            return
    elif mainMenuChoice == "X" or mainMenuChoice == "x" :
        exit(0)
    else :
        print("Error : Invalid selection.")
        os.system('clear')
        mainMenu()

#Convert ascii to binary######################################################################################
def asciiToBin() : #Add this functionality to the class.
    #Allow global variables to be reassigned.
    global mainMenuChoice
    
    #Convert the passKey to binary representation of characters.
    passKey.bin = list() #Add this functionality to the class.
    for q in passKey.plain :
        passKey.bin.append(bin(ord(q)))
    #Remove the '0b' from each char.
    passKey.bin = zeroBStripper(passKey.bin)
    
    #Determine if user is enciphering or deciphering data.
    if mainMenuChoice == "E" or mainMenuChoice == "e" :
        #Convert plainText to binary representation of characters.
        plainText.plainBin = list()
        for e in plainText.plainText :
            plainText.plainBin.append(bin(ord(e)))
        plainText.plainBin = zeroBStripper(plainText.plainBin)
    elif mainMenuChoice == "D" or mainMenuChoice == "d" :
        #Convert cipherText to binary representation of characters.
        cipherText.cipherBin = list()
        for d in cipherText.cipherText :
            cipherText.cipherBin.append(bin(ord(d)))    #None of these variables exist
        cipherText.cipherBin = zeroBStripper(cipherText.cipherBin)
    else :
        print("Error. Exit 1")
        exit(1)

    return

#0b Stripper##################################################################################################
def zeroBStripper(workingList) :
    for z in range(len(workingList)) :
        zHolder = list(workingList[z])
        del zHolder[0:2] #Delete the '0b'
        del workingList[z] #Remove the original '0b' containing value.
        workingList.insert(z, "".join(zHolder)) #Replace old '0b' value with non-0b binary value.
    workingList = "".join(workingList)

    return workingList

#Exclusive OR#################################################################################################
def XOR(binKey, binMessage) :
    print("Binary key: " + str(binKey))#delete me                   #XOR
    print("Binary msg: " + str(binMessage))#delete me            #0 & 0 = 0
    binKey = list(binKey)                                        #0 & 1 = 1
    binMessage = list(binMessage)                                #1 & 0 = 1
    cipher = []                                                  #1 & 1 = 0

    for z in range(len(binKey)) : #My super-noob XOR cipher. There's another way of doing this - var1 ^ var2,
        if binKey[z] == str(0) and binMessage[z] == str(0) : #except that it requires the use of decimals for
            cipher.append(str(0))                                 #some reason. Fuck it, we'll do it live!
        elif binKey[z] == str(0) and binMessage[z] == str(1) :
            cipher.append(str(1))
        elif binKey[z] == str(1) and binMessage[z] == str(0) :
            cipher.append(str(1))
        elif binKey[z] == str(1) and binMessage[z] == str(1) :
            cipher.append(str(0))
        else :
            print("Error: None binary value passed to XOR().")
            exit(1)

    return cipher

#Brutal Cipher Encryption#####################################################################################
def keyLengthMatching() :
    #Duplicate key to match size of plaintext if necessary.
    if len(passKey.bin) < len(plainText.plainBin) :
        keyDifference = math.ceil(float(len(plainText.plainBin) / len(passKey.bin)))
        passKey.ext_bin = passKey.bin * keyDifference

        if len("".join(passKey.ext_bin)) > len("".join(plainText.plainBin)) :
            binKeyDifference = int(len("".join(passKey.ext_bin)) - len("".join(plainText.plainBin)))
            #Remove the excess bits from the key.
            #Gotta make a working list first.
            passKeyList = list("".join(passKey.ext_bin))
            for x in range(binKeyDifference) : #Delete the last index value of the list x times based on the key difference.
                del passKeyList[-1]

            passKey.ext_bin = "".join(passKeyList) #Reset the value of the extended binary key.
            return passKey.ext_bin

        elif len("".join(passKey.ext_bin)) == len("".join(plainText.plainBin)) :
            pass
        else :
            exit(1)
    elif len(passKey.bin) > len(plainText.plainBin) :
        #Need to remove the excess bits just like I added above.
        #This should be an exceedingly rare occurence. It can wait.
        exit(0)
    else : #Key is already the same length as the message. Unlikely, but possible.
        return passKey.bin

    exit(0)

#Collatz Sequencer############################################################################################
def collatzSequencer(decimal) : 
    counter = 0
    x = decimal

    while x != 1:
        counter += 1
        if x % 2 != 0:
            x = (x * 3) + 1
        else:
            x = x / 2

    return counter

#The meat & potatoes##########################################################################################
#The intention here is to have the steps in called via a loop based, the order of which is based on the
#collatz sequence. This will take a hot minute.
def brutalCipher(ky, msg) :
    cipherText.cipherBin = XOR(ky, msg)
    print("Binary cip: " + str("".join(cipherText.cipherBin))) #Delete me.
    passKey.decimal = passKey.decVal()
    print("Key decimal val: " + str(passKey.decimal))
    print("The Collatz val of the key: " + str(collatzSequencer(passKey.decimal)) + " iterations.")
    return

#Main#########################################################################################################
def main() : #Old habit...
    mainMenu()
    keyCollection()
    asciiToBin()
    #collatzSequencer()
    brutalCipher(keyLengthMatching(), plainText.plainBin)
    exit(0)
main()
