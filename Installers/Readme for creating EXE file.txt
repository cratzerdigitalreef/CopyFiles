Readme for creating EXE file:

main.spec file is for configuring the exe file creation

1)
Go to file:
...\SMPP-Transmitter-python\smpptransmitter\libs\algos.py

In run.bat the following works fine:
# get library from: pip install pycryptodome 
# https://onboardbase.com/blog/aes-encryption-decryption
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

But generating the exe file, it should be updated to:
# get library from: pip install pycryptodome 
# https://onboardbase.com/blog/aes-encryption-decryption
#COMENTED SO THAT EXE FILE CAN BE GENERATED
#from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes

2)
Execute file 
...\SMPP-Transmitter-python\smpptransmitter\create_exe.bat

3)
When it is finished the process, the exe file is under "dist":
...\SMPP-Transmitter-python\smpptransmitter\dist\SMPP-Transmitter-Python.exe


