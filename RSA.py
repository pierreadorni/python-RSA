from utils import *
import sys, json, numpy
help="""
args:
--encrypt fileName
--decrypt fileName
--genkeys fileName [strenght]

optional:
-k file (for --encrypt and --decrypt)

"""

def decryptText(textFile,keyFile):
    with open(textFile,'r') as file:
        encrypted_list = file.read().split('.')
    with open(keyFile,'r') as file:
        key_dict = json.loads(file.read())
    key = (key_dict["module"],key_dict["d"])
    plain_text = "".join([decryptChar(int(n),key) for n in encrypted_list])

    with open(textFile.replace('-encrypted',''),'w') as file:
        file.write(plain_text)

def encryptText(textFile,keyFile):
    with open(textFile,'r') as file:
        plain_text = file.read()
    with open(keyFile,'r') as file:
        key_dict = json.loads(file.read())
    key = (key_dict["module"],key_dict["e"])
    encrypted_text = ".".join([str(encryptChar(char,key)) for char in plain_text])

    nameSplit = textFile.split(".")
    with open(nameSplit[0]+"-encrypted"+"."+nameSplit[1],'w') as file:
        file.write(encrypted_text)


def generateKeys(keyFile,strenght):
    publicKey, privateKey = getKeys(strenght)
    with open(keyFile+'-private.key','w') as file:
        json.dump({"module":privateKey[0],"d":privateKey[1]},file)

    with open(keyFile+'-public.key','w') as file:
        json.dump({"module":publicKey[0],"e":publicKey[1]},file)
    print('keys generated.')
    return keyFile+'-private.key',keyFile+'-public.key'


if __name__ == "__main__":

    k = None
    canDecrypt = False
    strenght = 154

    if "-s" in sys.argv:
        strenght = int(sys.argv[sys.argv.index("-s")+1])

    if "--genkeys" in sys.argv:
        generateKeys(sys.argv[sys.argv.index("--genkeys")+1],strenght)
        sys.exit()

    if "-k" in sys.argv:
        k = sys.argv[sys.argv.index("-k")+1]
        canDecrypt = True
    else:
        k = generateKeys("key",strenght)


    if "--encrypt" in sys.argv:
        if type(k) != str:
            k = k[1]
        encryptText(sys.argv[sys.argv.index("--encrypt")+1],k)
        sys.exit()

    if "--decrypt" in sys.argv:
        if type(k) != str:
            print(help)
            sys.exit()
        decryptText(sys.argv[sys.argv.index("--decrypt")+1],k)
        sys.exit()
    print(help)
