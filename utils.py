import math, numpy, sys, decimal, os
import random

character_limit = 5000
powerLow = None
powerHigh = None


def Miller_Rabin(n,k):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def checkPremier(n):
    if n<7:
        if n in (2,3,5):
            return True
        else:
            return False
    # si n est pair et >2 (=2: cas traité ci-dessus), il ne peut pas être premier
    if n % 2 == 0:
        return False
    # autres cas
    k=3
    r=int(decimal.Decimal(n).sqrt())
    while k<=r:
        if n % k == 0:
            return False
        k+=2
    return True

def checkPremiers(n,m):
    a = n if n < m else m
    b = m if n < m else n
    while a%b != 0:
        c = a%b
        a = b
        b = c

    if b == 1:
        return True
    return False

def getE(psi):
    rand = random.randint(1, psi-1)
    while (not checkPremiers(psi, rand)):
        rand = random.randint(1, psi-1)
    return rand

def randomPremier():
    rand = 4
    while rand % 2 == 0:
        rand = random.randint(powerLow, powerHigh)
    while not Miller_Rabin(rand,40):
        rand = rand+2
    return rand

def getN():
    p = 0
    q = 0
    while (p == q):
        p = randomPremier()
        q = randomPremier()
    return p, q

def getModule(n):
    return n[0]*n[1]

def getPsi(n):
    return (n[0]-1)*(n[1]-1)

def getD_recursif(a,b):
    (r, u, v, r1, u1, v1) = (a, 1, 0, b, 0, 1)

    while r1 !=0:
        q = r//r1
        (r, u, v, r1, u1, v1) = (r1, u1, v1, r - q *r1, u - q*u1, v - q*v1)

    return r,u,v

def getD(psi,e):

    decomp = euclide(psi, e)
    dict = {}
    #pour chaque ligne de decomp, on va avoir une équation type r = a - b*c
    #on prend la dernière ligne, on cherche dans a,b et c si on trouve un a (ou b ou c)=r d'une ligne précédente
    #on replace ce r par ce qu'il vaut (a1-b1*c1)
    #on cherche dans a1,b1,c1 siu on trouyve un r1 d'une ligne précédente
    #ax,bx,cx à la fin ==> ax = d

    for obj in decomp:
        dict[obj[3]]= f" {obj[0]} - {obj[1]} * {obj[2]} "

    base = decomp[-1]
    base = f" {base[0]} - {base[1]} * {base[2]} "
    done = True

    dict.pop(psi, None)
    dict.pop(e,None)
    dict.pop(1,None)

    while done:
        done = False
        toDelete = []
        for key in sorted(dict):
            for item in base.replace("-","+").replace("*","+").replace("(","").replace(")","").split("+"):

                if item == " "+str(key)+" ":
                    proceed = True
                    strI = str(item)

                    try:
                        if base[base.find(strI)+len(strI)].isdigit():
                            proceed = False
                    except IndexError:
                        pass

                    try:
                        if base[base.find(strI)-1].isdigit():
                            proceed = False
                    except IndexError:
                        pass

                    if proceed:
                        base = base.replace(strI,"("+dict[key]+")")
                        toDelete.append(key)
                    done = True
            for k in toDelete:
                dict.pop(k, None)
    d = int(eval(base.replace(str(psi),"0"))/e)
    if d<0:
        d = int(eval(base.replace(str(e),"0"))/psi)
    return (d)

def getKeys(strenght):
    global powerHigh
    global powerLow
    powerHigh = pow(10,strenght+1)
    powerLow = pow(10,strenght)

    d = -1
    while d < 0:
        os.system('clear')
        print("[*] -------- Generating RSA Keys process initialized -------- ")
        print("[-] Finding p and q...")
        n = getN()
        print("[i] p = %e "%n[0]+" , q = %e"%n[1])
        print("[-] Computing encryption module...")
        module = int(getModule(n))
        print("[i] Done ! ")
        print("[-] Computing Euler's totient... (strenght of the encryption)")
        psi = getPsi(n)
        print("[i] Euler's totient value: %e "%decimal.Decimal(psi))
        print("[-] Computing public key exponent...")
        e = getE(psi)
        print("[i] public key exponent: e = %e"%decimal.Decimal(e))
        print("Computing private key exponent...")
        r,u,v = getD_recursif(e,psi)
        d = int(u)
        print("[i] private key exponent: d = %e"%decimal.Decimal(d))
    print("[*] -------- Generating RSA Keys process finished -------- ")
    #print("\n")
    #print(f"private key: d={d}\n n={module}\n")
    #print(f"public key: e={e}\n n={module}")
    #print("\n")
    return (module,e), (module,d) # Public then private

def encryptChar(char, public_key):
    return (int(pow(ord(char), public_key[1], public_key[0])))

def decryptChar(n, private_key):
    return chr(pow(n, private_key[1] , private_key[0]))

def euclide(psi, num):
    decomp = []
    a = psi
    b = num
    while a%b != 0:
        decomp.append([a, a//b, b, a%b])
        c = a%b
        a = b
        b = c
    return decomp
