#!/usr/bin/python3.5
import os, shutil, sys, re, pyperclip, argparse, binascii
from time import sleep

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
#Strings
passKey = str()
plainText = str()
cipherText = str()
mainMenuChoice = str()

#Lists
cipherTextBin = list()
plainTextBin = list()
passKeyBin = list()

#Functions########################################################################################################
#Banner###########################################################################################################
def banner() :
    print("--------Brutal Cipher v1-----------")
    return

#Key Input########################################################################################################
def keyCollection() :
    global passKey
    os.system('clear')
    banner()
    passKey = input("\nEnter the key \u2192 ") #Manual key collection.
    os.system('clear')
    return

#Input Menu#######################################################################################################
def inputMenu(choiceFromMainMenu) :
    #Allow global assigning.
    global mainMenuChoice
    global plainText
    global cipherText

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
                plainText = input("Enter the plaintext: ")
                return plainText
            elif mainMenuChoice == "D" or mainMenuChoice == "i" :
                cipherText = input("Enter the ciphertext: ")
                return cipherText
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
"""
Things that are converted to binary:
    passKey
    plainText or cipherText
"""
def asciiToBin() :
    #Allow global variables to be reassigned.
    global cipherText
    global plainText
    global passKey
    global mainMenuChoice
    global plainTextBin
    global cipherTextBin
    global passKeyBin
    
    #Convert the passKey to binary representation of characters.
    passKeyBin = list()
    for q in passKey :
        passKeyBin.append(bin(ord(q)))
    #Remove the '0b' from each char.
    passKeyBin = zeroBStripper(passKeyBin)
    
    #Determin if user is enciphering or deciphering data.
    if mainMenuChoice == "E" or mainMenuChoice == "e" :
        #Convert plainText to binary representation of characters.
        for e in plainText :
            plainTextBin.append(bin(ord(e)))
        plainTextBin = zeroBStripper(plainTextBin)
    elif mainMenuChoice == "D" or mainMenuChoice == "d" :
        #Convert cipherText to binary representation of characters.
        for d in cipherText :
            cipherTextBin.append(bin(ord(d)))
        cipherTextBin = zeroBStripper(cipherTextBin)
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

    return workingList

#Brutal Cipher Encryption#####################################################################################
def brutalEncipher() :
    global plainTextBin
    global passKeyBin

    print("The plain text in binary is: " + str("".join(plainTextBin)))
    print("The key in binary is : " + str("".join(passKeyBin)))

    #Ideas for this algorithm.
        #Split into 256 bit block size
        #transpose
        #XOR
        #split into 128 bit block size
        #transpose based on some sort of password attribute like len(passKey) % 2 != 0
        #XOR
        #Transpose key at some point?
    exit(0)

#Collatz Sequencer############################################################################################
def collatzSequencer() : #This is working as a test. If one wants to see how it works, uncomment it below and comment out everything else
    limit = 999999
    startingX =999900

    while startingX <= limit :
        x = startingX
        counter = 0
        while x != 1 :
            counter += 1
            if x % 2 != 0 :
                x = (x * 3) + 1
            else :
                x = x / 2
        print("The #" + str(startingX) + " takes " + str(counter) + " times.")
        startingX += 1

#Main#########################################################################################################
def main() : #Old habit...
    mainMenu()
    keyCollection()
    asciiToBin()
    #collatzSequencer()
    brutalEncipher()
    exit(0)
main()
