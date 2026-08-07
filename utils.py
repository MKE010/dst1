import os

def clrScrn():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def wait():
    input("Press ENTER to continue...")

def header(t, sub=None):
    print("================================================")
    print(f"{t:^48}")
    if sub != None:
        print(f"{sub:^48}")
    print("================================================\n")