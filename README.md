# python RSA

A quick python script to create RSA keys and encrypt/decrypt files

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Usage](#setup)

## General info
With this script, you can:
* Create RSA Keys of any strenght 
* Encrypt/Decrypt Files
	
## Technologies
Uses the [Miller-Rabin primality test](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test), written in python by [Ayrx](https://github.com/Ayrx), to find big prime numbers (154 digits by default)
and  the [Extended Euclidean Algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm) to compute them into RSA Keys that are **indestructible** with today's computing power

	
## Usage

### with files
To **create RSA Keys**, run RSA&#46;py as following:

```
$ python RSA.py --genkeys filename
```
It will create two files, *filename-public.key* and *filename-private.key*

You can **set the strenght** of your key as following:
```
$ python RSA.py --genkeys filename -s 15
```
The above command will specifically ask the program to find **15 digits long** prime numbers (154 digits long by default)

You can also encrypt or decrypt files as following:
```
$ python RSA.py --encrypt file -k key-public.key
$ python RSA.py --decrypt file-encrypted -k key-private.key
```
the encryption of *file.txt will result in the creation (or update) of *file-encrypted.txt, and the decryption of a *file-encrypted.txt will be written in *file.txt* (it will try to remove the -encrypted in the name, if it can't find it will overwrite the encrypted file)

### inside a script
you can also use this script inside yours by calling the **getKeys(strenght)** function of utils&#46;py.
the strenght is an int, **use 154** if you want a strong key

The **getKeys()** function returns two tuples as following:
````
>>> public_key, private_key = getKeys(154)
````
with public_key = ( module , encryption_exponent )
and private_key = ( module , decryption_exponent )

you can then use **encryptChar()** and **decryptChar()** as following:
```
>>> encrypted_a = encryptChar('a',public_key)
>>> decryptChar(encrypted_a,private_key)
'a'
```
where *encrypted_a* is a **long int**

To import the function, you can use the following method:
```
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/python-RSA')
from utils import getKeys,encryptChar,decryptChar
```

