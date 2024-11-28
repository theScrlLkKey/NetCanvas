import time
import random
from os import walk
import os
import zlib
import shutil
import pickle
import subprocess
import sys
from pynput.keyboard import Listener, Key
import colorama
import threading
from cryptography.fernet import Fernet
import secrets
import hashlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# menus

main_menu = '''███████████████████████████████████████████████████████████████████
█00:00 AM       WELCOME,                        LIGHT OS MAIN MENU█  
███████████████████████████████████████████████████████████████████
█MENUS:                                                           █
█1. MAIN MENU                                                     █
█2. PROGRAMS                                           7. DEBUG   █
█3. GAMES                                              6. PLUGINS █
█4. DOCUMENTS                                          5. SETTINGS█
███████████████████████████████████████████████████████████████████
█                                                                 █
███████████████████████████████████████████████████████████████████ 
'''
usenmpw_menu = '''███████████████████████████████████████████████████████████████████
█                       ENTER LOGIN DETAILS                       █  
███████████████████████████████████████████████████████████████████
█                                                                 █
█                                                                 █
█                                                                 █
█                                                                 █
█                                                                 █
█                                                                 █ 
█                                                                 █
███████████████████████████████████████████████████████████████████ 
'''
prog_menu = '''███████████████████████████████████████████████████████████████████
█00:00 AM                                                 LIGHT OS█  
███████████████████████████████████████████████████████████████████
█PROGRAMS:                                                        █
█1. MAIN MENU           5. LIGHTTYPE                              █
█2. CHATPY              6. LIGHTCALC                              █
█3. LIGHTMAN            7. LIGHTSTOCKS                            █
█4. LIGHTCRYPTER                                                  █
███████████████████████████████████████████████████████████████████
█                                                                 █
███████████████████████████████████████████████████████████████████ 
'''
games_menu = '''███████████████████████████████████████████████████████████████████
█00:00 AM                                                 LIGHT OS█  
███████████████████████████████████████████████████████████████████
█GAMES:                                                           █
█1. MAIN MENU                                                     █
█2. LIGHTDRAW                                                     █
█3. GRIFFIN QUEST                                                 █
█                                                                 █
███████████████████████████████████████████████████████████████████ 
█                                                                 █
███████████████████████████████████████████████████████████████████
'''
settings_menu = '''███████████████████████████████████████████████████████████████████
█00:00 AM                                                 LIGHT OS█  
███████████████████████████████████████████████████████████████████
█SETTINGS:                                               8.6B-EXTS█
█1. RETURN TO MAIN MENU                                           █
█2. LOAD STARTUP APPS           CURRENT VALUE:                    █
█3. FOUR LEVEL SLIDER           CURRENT VALUE:                    █
█4. CUSTOM MESSAGE              CURRENT VALUE:                    █
███████████████████████████████████████████████████████████████████ 
█                                                                 █
███████████████████████████████████████████████████████████████████
'''
setting_submenu = '''███████████████████████████████████████████████████████████████████
█00:00 AM                                                 LIGHT OS█  
███████████████████████████████████████████████████████████████████
█                                                                 █
█                                                                 █
█                                                                 █
█                                                                 █
█                                                                 █
███████████████████████████████████████████████████████████████████ 
█                                                                 █
███████████████████████████████████████████████████████████████████
'''
loadingscr = '''███████████████████████████████████████████████████████████████████
█                            LIGHT OS                             █  
███████████████████████████████████████████████████████████████████
█                                                                 █
█                                                                 █
█        LIGHT OS HAS NOT CRASHED, DO NOT CLOSE THIS WINDOW       █
█                                                                 █
█                                                                 █
███████████████████████████████████████████████████████████████████ 
█                           LOADING...                            █
███████████████████████████████████████████████████████████████████
'''

doc_menu = '''███████████████████████████████████████████████████████████████████
█00:00 AM                                                 LIGHT OS█  
███████████████████████████████████████████████████████████████████
█OPTIONS:                                                         █
█1. RETURN TO MAIN MENU                                           █
█2. NEW                                                           █
█3. EDIT                                                          █
█4. DELETE                                                        █
███████████████████████████████████████████████████████████████████
█                                                                 █
███████████████████████████████████████████████████████████████████ 
'''

plugin_menu = '''███████████████████████████████████████████████████████████████████
█00:00 AM                                                 LIGHT OS█  
███████████████████████████████████████████████████████████████████
█PLUGINS:                                                         █
█                                                                 █
█                                                                 █
█                                                                 █
█                                           1. RETURN TO MAIN MENU█
███████████████████████████████████████████████████████████████████ 
█                                                                 █
███████████████████████████████████████████████████████████████████
'''

init_setup = '''███████████████████████████████████████████████████████████████████
█                         LIGHT OS SETUP                          █  
███████████████████████████████████████████████████████████████████
'''

external_prog = '''███████████████████████████████████████████████████████████████████
█00:00 AM                                                 LIGHT OS█  
███████████████████████████████████████████████████████████████████
'''
# defs
name = 'USER'
colorama.init()
def write_key():
    """
    Generates a key and save it into a file
    """
    k = Fernet.generate_key()
    nbkey = k.decode("utf-8")
    return k
enckey = write_key()

versionstr = '8.6B-EXTS'

def console_log(log_text):
    if 'enableconsolelog' in str(sys.argv):
        try:
            with open('log/log.txt', 'a+') as data:
                data.write(log_text + '\n')
        except:
            pass
    else:
        pass



def on_press(key):
    # old code for a interactive version where you could move cursor with arrow keys like a mouse
    # menu key will try to exit to the main menu (dosn't work in external programs)
    global key_jp
    if hasattr(key, 'char'):  # Write the character pressed if available
         key_jp = str(key.char)
    # elif key == Key.space:  # If space was pressed, write a space
    #     inputchar(' ')
    # elif key == Key.enter:  # If enter was pressed, write a new line
    #     key_jp = 'select'
    # elif key == Key.tab:  # If tab was pressed, write a tab
    #     inputchar('\t')
    # elif key == Key.left:
    #     inputchar('\033[1D')
    # elif key == Key.right:
    #     inputchar('\033[1C')
    # elif key == Key.up:
    #     inputchar('\033[1A')
    # elif key == Key.down:
    #     inputchar('\033[1B')
    elif key == Key.menu:
        switchscr('1')
    # elif key == Key.backspace:
    #     inputchar('\033[1D \033[1D')
    # elif key == Key.delete:
    #     inputchar('\b\27[127\b')
    # else:  # If anything else was pressed, write [<key_name>]
    #     pass

def getact(snm):
    rtrn = input(snm)
    return rtrn

def switchscr(scrnum):
    global curmen
    global tuploc
    global prognm
    global mes_setting
    global onoff_setting
    global fo_setting
    global startup_setting
    if scrnum == '1':
        inputchar('\033[2J')
        type(main_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type(name)
        tuploc = '10;19H'
        tmup(tuploc)
        curmen = 'main'
    if scrnum.lower() == 'exit':
        os._exit(0)
    elif scrnum == '2' and curmen == 'main':
        inputchar('\033[2J')
        type(prog_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('PROGRAM LAUNCHER')
        tuploc = '10;19H'
        tmup(tuploc)
        curmen = 'prog'
    elif scrnum == '2' and curmen == 'prog':
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('CHATPY')
        tuploc = '*'
        inputchar('\033[4;2H')
        curmen = 'ex_prog'
        inputchar('\033[4;2H')
        prognm = 'CHATPY  '
        # progtmu = threading.Thread(target=progtimup, args=())
        # progtmu.start()
        tmup('10;19H')
        inputchar('\033[4;1H')
        stprog("chatpy/chatpy2.py")
        time.sleep(0.5)
    elif scrnum == '3' and curmen == 'prog':
        inputchar('\033[1;1H')
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTMAN')
        tuploc = '*'
        inputchar('\033[4;2H')
        curmen = 'ex_prog'
        inputchar('\033[4;2H')
        prognm = 'CHATPY  '
        # progtmu = threading.Thread(target=progtimup, args=())
        # progtmu.start()
        tmup('10;19H')
        inputchar('\033[4;1H')
        stprog("LightMan.py")
        time.sleep(0.5)
    elif scrnum == '4' and curmen == 'prog':
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTCRYPTER')
        tuploc = '*'
        inputchar('\033[4;2H')
        curmen = 'ex_prog'
        inputchar('\033[4;2H')
        prognm = 'CHATPY  '
        # progtmu = threading.Thread(target=progtimup, args=())
        # progtmu.start()
        tmup('10;19H')
        inputchar('\033[4;1H')
        stprog("LightEncrypter.py")
        time.sleep(0.5)
    elif scrnum == '5' and curmen == 'prog':
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTTYPE')
        tuploc = '*'
        inputchar('\033[4;2H')
        curmen = 'ex_prog'
        inputchar('\033[4;2H')
        prognm = 'CHATPY  '
        # progtmu = threading.Thread(target=progtimup, args=())
        # progtmu.start()
        tmup('10;19H')
        inputchar('\033[4;1H')
        stprog("LightType.py")
        time.sleep(0.5)
    elif scrnum == '6' and curmen == 'prog':
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTCALC')
        tuploc = '*'
        inputchar('\033[4;2H')
        curmen = 'ex_prog'
        inputchar('\033[4;2H')
        prognm = 'CHATPY  '
        # progtmu = threading.Thread(target=progtimup, args=())
        # progtmu.start()
        tmup('10;19H')
        inputchar('\033[4;1H')
        stprog("LightCalc.py")
        time.sleep(0.5)
    elif scrnum == '8' and curmen == 'prog':
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('PYBASIC')
        tuploc = '*'
        inputchar('\033[4;2H')
        curmen = 'ex_prog'
        inputchar('\033[4;2H')
        prognm = 'CHATPY  '
        # progtmu = threading.Thread(target=progtimup, args=())
        # progtmu.start()
        tmup('10;19H')
        inputchar('\033[4;1H')
        stprog("basic/interpreter.py")
        time.sleep(0.5)
    elif scrnum == '7' and curmen == 'prog':
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTSTOCKS')
        tuploc = '*'
        inputchar('\033[4;2H')
        curmen = 'ex_prog'
        inputchar('\033[4;2H')
        prognm = 'CHATPY  '
        # progtmu = threading.Thread(target=progtimup, args=())
        # progtmu.start()
        tmup('10;19H')
        inputchar('\033[4;1H')
        stprog("LightStonks.py")
        time.sleep(0.5)

    elif scrnum == '3' and curmen == 'main':
        inputchar('\033[2J')
        type(games_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('GAMES')
        tuploc = '10;19H'
        tmup(tuploc)
        curmen = 'games'
    elif scrnum == '2' and curmen == 'games':
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTDRAW')
        tuploc = '*'
        inputchar('\033[4;2H')
        curmen = 'ex_prog'
        inputchar('\033[4;2H')
        prognm = 'CHATPY  '
        # progtmu = threading.Thread(target=progtimup, args=())
        # progtmu.start()
        tmup('10;19H')
        inputchar('\033[4;1H')
        stprog("lightbreakout.py")
        time.sleep(0.5)
    elif scrnum == '3' and curmen == 'games':
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('GRIFFIN QUEST')
        tuploc = '*'
        inputchar('\033[4;2H')
        curmen = 'ex_prog'
        inputchar('\033[4;2H')
        prognm = 'CHATPY  '
        # progtmu = threading.Thread(target=progtimup, args=())
        # progtmu.start()
        tmup('10;19H')
        inputchar('\033[4;1H')
        stprog("griffin_quest.py")
        time.sleep(0.5)
    elif scrnum == '4' and curmen == 'main':
        inputchar('\033[2J')
        type(doc_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;30H')
        type('NOTES')
        tuploc = '10;19H'
        tmup(tuploc)
        curmen = 'note'
    elif scrnum == '2' and curmen == 'note':
        inputchar('\033[2J')
        type(loadingscr)
        inputchar('\033[11A')
        inputchar('\033[10;39H')
        encrypt_emb2(f'{name}_notes.txt', '', enckey, f'gtadYYDA6adAD87AD6dayHFG9B7gf{str(zlib.crc32(str(passwd).encode("utf-8")))}')
        encrypt(f'{name}_notes.txt', enckeyff)

        inputchar('\033[2J')
        type(doc_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;30H')
        type('NOTES')
        tmup(tuploc)

    elif scrnum == '3' and curmen == 'note':
        inputchar('\033[2J')
        type(loadingscr)
        inputchar('\033[11A')
        inputchar('\033[10;39H')
        with open(f'{name}_notes.txt', "r") as file:
            encfdataf = file.read()
        try:
            try:
                encfdata = decrypt(encfdataf.encode("utf-8"), enckeyff)
            except:
                pass

            with open('notesdec.txt', "wb") as file:
                file.write(decrypt_emb2(encfdata.decode("utf-8"), f'gtadYYDA6adAD87AD6dayHFG9B7gf{str(zlib.crc32(str(passwd).encode("utf-8")))}').encode("utf-8"))
        except Exception as err:
            console_log(str(err))
            inputchar('\033[2J')
            print('Incorrect password or data.txt corrupt.')
            print('Fatal error occurred. Press enter to continue, then select 1.')
            input()
            exit()
        inputchar('\033[2J')
        type(loadingscr)
        inputchar('\033[11A')
        inputchar('\033[10;22H')
        type('DOCUMENT OPEN IN NOTEPAD')
        tuploc = '*'
        subprocess.call(['notepad.exe', 'notesdec.txt'])

        inputchar('\033[2J')
        type(loadingscr)
        inputchar('\033[11A')
        inputchar('\033[10;39H')
        with open('notesdec.txt', "r") as file:
            decfdata = file.read()
        encrypt_emb2(f'{name}_notes.txt', decfdata, enckey, f'gtadYYDA6adAD87AD6dayHFG9B7gf{str(zlib.crc32(str(passwd).encode("utf-8")))}')
        encrypt(f'{name}_notes.txt', enckeyff)
        with open('notesdec.txt', "wb") as file:
            file.write(''.encode("utf-8"))

        inputchar('\033[2J')
        type(doc_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;30H')
        type('NOTES')
        tuploc = '10;19H'
        tmup(tuploc)

    elif scrnum == '4' and curmen == 'note':
        inputchar('\033[2J')
        type(loadingscr)
        inputchar('\033[11A')
        inputchar('\033[10;39H')
        with open(f'{name}_notes.txt', "wb") as file:
            file.write(''.encode("utf-8"))
        inputchar('\033[2J')
        type(doc_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;30H')
        type('NOTES')
        tmup(tuploc)

    elif scrnum == '7' and curmen == 'main':
        inputchar('\033[2J')
        type(external_prog)
        inputchar('\033[11A')
        inputchar('\033[3C')

        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('PYTHON PROMPT')
        tuploc = '4;1H'
        tmup(tuploc)
        tuploc = '*'
        curmen = 'py_dbg'
        while True:
            try:
                exec(input('>>> '))
            except KeyboardInterrupt:
                break
            except:
                print('?SYNTAXERROR')

    elif scrnum == '5' and curmen == 'main':
        inputchar('\033[2J')
        type(settings_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTOS SETTINGS')
        inputchar('\033[6;48H')
        if startup_setting:
            type('ON')
        elif not startup_setting:
            type('OFF')
        else:
            type('')
        inputchar('\033[7;48H')
        if fo_setting == 1:
            type('OFF')
        elif fo_setting == 2:
            type('LOW')
        elif fo_setting == 3:
            type('MEDIUM')
        elif fo_setting == 4:
            type('HIGH')
        else:
            type('')
        inputchar('\033[8;48H')
        type(str(mes_setting))
        tuploc = '10;19H'
        tmup(tuploc)
        curmen = 'set'
    elif scrnum == '2' and curmen == 'set':
        inputchar('\033[2J')
        type(setting_submenu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LOAD STARTUP APPS')
        inputchar('\033[5;2H')
        type('1. ON')
        inputchar('\033[7;2H')
        type('2. OFF')
        tuploc = '10;13H'
        tmup(tuploc)
        inputchar('\033[10;2H')
        settocg = input('SELECTION: ')
        if settocg == '1':
            startup_setting = True
        elif settocg == '2':
            startup_setting = False
        inputchar('\033[2J')
        type(loadingscr)
        inputchar('\033[11A')
        inputchar('\033[10;39H')

        with open(f'{name}_settings.lset', 'wb') as f:
            pickle.dump([onoff_setting, fo_setting, mes_setting, startup_setting], f)

        inputchar('\033[2J')
        type(settings_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTOS SETTINGS')
        inputchar('\033[6;48H')
        if startup_setting:
            type('ON')
        elif not startup_setting:
            type('OFF')
        else:
            type('')
        inputchar('\033[7;48H')
        if fo_setting == 1:
            type('OFF')
        elif fo_setting == 2:
            type('LOW')
        elif fo_setting == 3:
            type('MEDIUM')
        elif fo_setting == 4:
            type('HIGH')
        else:
            type('')
        inputchar('\033[8;48H')
        type(str(mes_setting))
        tuploc = '10;19H'
        tmup(tuploc)
        curmen = 'set'


    elif scrnum == '3' and curmen == 'set':
        inputchar('\033[2J')
        type(setting_submenu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('FOUR OPTION SETTING')
        inputchar('\033[5;2H')
        type('1. OFF')
        inputchar('\033[6;2H')
        type('2. LOW')
        inputchar('\033[7;2H')
        type('3. MEDIUM')
        inputchar('\033[8;2H')
        type('4. HIGH')
        tuploc = '10;13H'
        tmup(tuploc)
        inputchar('\033[10;2H')
        settocg = input('SELECTION: ')
        if settocg == '1':
            fo_setting = 1
        elif settocg == '2':
            fo_setting = 2
        elif settocg == '3':
            fo_setting = 3
        elif settocg == '4':
            fo_setting = 4
        else:
            fo_setting = 0

        inputchar('\033[2J')
        type(loadingscr)
        inputchar('\033[11A')
        inputchar('\033[10;39H')
        with open(f'{name}_settings.lset', 'wb') as f:
            pickle.dump([onoff_setting, fo_setting, mes_setting, startup_setting], f)

        inputchar('\033[2J')
        type(settings_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTOS SETTINGS')
        inputchar('\033[6;48H')
        if startup_setting:
            type('ON')
        elif not startup_setting:
            type('OFF')
        else:
            type('')
        inputchar('\033[7;48H')
        if fo_setting == 1:
            type('OFF')
        elif fo_setting == 2:
            type('LOW')
        elif fo_setting == 3:
            type('MEDIUM')
        elif fo_setting == 4:
            type('HIGH')
        else:
            type('')
        inputchar('\033[8;48H')
        type(str(mes_setting))
        tuploc = '10;19H'
        tmup(tuploc)
        curmen = 'set'

    elif scrnum == '4' and curmen == 'set':
        inputchar('\033[2J')
        type(setting_submenu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('GENERIC MESSAGE SETTING')
        tuploc = '10;13H'
        tmup(tuploc)
        inputchar('\033[10;2H')
        settocg = input('CUSTOM MESSAGE: ')
        mes_setting = str(settocg).upper()
        inputchar('\033[2J')
        type(loadingscr)
        inputchar('\033[11A')
        inputchar('\033[10;39H')
        with open(f'{name}_settings.lset', 'wb') as f:
            pickle.dump([onoff_setting, fo_setting, mes_setting, startup_setting], f)

        inputchar('\033[2J')
        inputchar('\033[2J')
        type(settings_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('LIGHTOS SETTINGS')
        inputchar('\033[6;48H')
        inputchar('\033[6;48H')
        if startup_setting:
            type('ON')
        elif not startup_setting:
            type('OFF')
        else:
            type('')
        inputchar('\033[7;48H')
        if fo_setting == 1:
            type('OFF')
        elif fo_setting == 2:
            type('LOW')
        elif fo_setting == 3:
            type('MEDIUM')
        elif fo_setting == 4:
            type('HIGH')
        else:
            type('')
        inputchar('\033[8;48H')
        type(str(mes_setting))
        tuploc = '10;19H'
        tmup(tuploc)
        curmen = 'set'

    elif scrnum == '6' and curmen == 'main':
        inputchar('\033[2J')
        type(plugin_menu)
        inputchar('\033[11A')
        inputchar('\033[3C')
        inputchar('\033[2B')
        inputchar('\033[2;26H')
        type('PLUGIN MENU')
        tuploc = '10;19H'
        tmup(tuploc)
        curmen = 'plug'
        os.chdir('plugins')
        cwd = os.getcwd()
        files = []
        for (dirpath, dirnames, filenames) in walk(cwd):
            files.extend(filenames)
            break
        filenumls = {}
        j = 2
        for file in files:
            filenumls[str(j)] = file
            j += 1
        j = 5
        i = 2
        for file in files:
            try:
                console_log('plugin menu '+str(j)+str(i))
                dummy, plugn = filenumls[str(i)].split('--')
                if j > 13:
                    inputchar(f'\033[{j-10};45H')
                elif j > 8:
                    inputchar(f'\033[{j-5};23H')
                else:
                    inputchar(f'\033[{j};2H')
                plugntr = plugn.replace(".py","")[:16]
                type(f'{j-3}. {plugntr}')
                j += 1
                i += 1
            except:
                i += 1


        while True:
            inputchar('\033[10;2H')
            ussl = input('ENTER SELECTION: ')
            inputchar('\033[10;1H')
            type('█                                                                 █')
            if ussl == '1':
                switchscr('1')
                cwd = os.getcwd()
                cmd = os.path.dirname(cwd)
                os.chdir(cmd)
                break
            elif ussl.upper() == 'EXIT':
                os._exit(0)
            elif ussl in filenumls:
                console_log('running plugin')
                inputchar('\033[2J')
                type(loadingscr)
                inputchar('\033[11A')
                inputchar('\033[10;22H')
                type('PLUGIN LOADING...')
                try:
                    tuploc = '*'
                    subprocess.call(['python', filenumls[ussl]])
                except:
                    continue
                curmen = 'main'
                cwd = os.getcwd()
                cmd = os.path.dirname(cwd)
                os.chdir(cmd)
                switchscr('6')
                break
            else:
                continue






def inputchar(key):
    sys.stdout.write(key)
    sys.stdout.flush()

def type(t):
    inputchar(t)
    # for l in t:
    #     sys.stdout.write(l)
    #     sys.stdout.flush()
    #     # j = 0
    #     # while j != 10000:
    #     #     j+=1
def strtlstn():
    with Listener(on_press=on_press) as listener:
        listener.join()
def strttmup():
    global tuploc
    while True:
        if tuploc != '*':
            t = time.localtime()
            current_time = time.strftime("%I:%M %p", t)
            inputchar('\033[2;2H')
            type(current_time)
            inputchar(f'\033[{tuploc}')
            console_log('clock.update('+current_time+') done')
            time.sleep(30)
def tmup(tul):
    t = time.localtime()
    current_time = time.strftime("%I:%M %p", t)
    inputchar('\033[2;2H')
    type(current_time)
    inputchar(f'\033[{tul}')
    console_log('clock.update() done temp')

def stprog(pnm):
    try:
        subprocess.call(['python', pnm])
    except:
        # switchscr('1')
        pass
    switchscr('1')

def progtimup():
    global curmen
    global prognm
    while curmen == 'chat':
        try:
            time.sleep(30)
            t = time.localtime()
            current_time = time.strftime("%I:%M %p", t)
            inputchar('\033[H')
            tts = f'''███████████████████████████████████████████████████████████████████
█{current_time}                                                 LIGHT OS█
███████████████████████████████████████████████████████████████████'''
            type(tts)
            inputchar('\033[2;26H')
            type(prognm)
            inputchar('\033[11;1H')
        except:
            continue




backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)






def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    try:
        with open(filename, "rb") as file:
            # read all file data
            file_data = file.read()
    except FileNotFoundError:
        print('File does not exist!')
        exit()
    except MemoryError:
        print('Gah. Your file is too big!(999Mb max)')
        exit()
    except:
        print('A error occurred.')
        exit()

    # encrypt data
    try:
        encrypted_data = f.encrypt(file_data)
        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)
    except:
        print('A error occurred.')


def decrypt(encrypted_data, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    # decrypt data
    try:
        decrypted_data = f.decrypt(encrypted_data)
        # write the original file
        return decrypted_data
    except:
        return encrypted_data

def encrypt_emb2(filename, data, key, password):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    try:
        file_data = data.encode("utf-8")
    except MemoryError:
        print('How have you done this? There are too many users!')
        exit()
    except:
        print('A error occurred.')
        exit()

    # encrypt data
    try:
        encrypted_data = f.encrypt(file_data)
        password_enc = f.encrypt(password.encode("utf-8"))
        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)
        with open(filename, "a") as file:
            file.write('`-`' + key.decode("utf-8"))
        with open(filename, "a") as file:
            file.write(',-,' + password_enc.decode("utf-8"))
    except:
        print('A error occurred.')
        exit()


def decrypt_emb2(data, password):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    data = data.encode("utf-8")
    sep = '`-`'
    sep = sep.encode("utf-8")
    sep2 = ',-,'
    sep2 = sep2.encode("utf-8")
    encrypted_data, file_data = data.split(sep)
    key, rpassword = file_data.split(sep2)
    f = Fernet(key)
    # decrypt data
    try:
        decrypted_data = f.decrypt(encrypted_data)
        password_dec = f.decrypt(rpassword)
        # write the original file
        if password_dec.decode("utf-8") == password:
                rdat = decrypted_data.decode("utf-8")
        else:
            print('data.txt corrupt.')
            exit()
    except:
        print('A error occurred.')
        exit()
    return rdat

# fallback mainloop if loaded one breaks
def mainloop():
    timup.start()
    time.sleep(0.1)
    while True:
        try:
            while curmen != 'ex_prog':
                inputchar('\033[10;2H')
                usrsel = input('ENTER SELECTION: ')
                inputchar('\033[10;1H')
                type('█                                                                 █')
                if usrsel.lower() == 'antigravity':
                    import antigravity
                console_log('running program')
                switchscr(str(usrsel))
                console_log('done running '+usrsel)
        except:
            pass


# wtf is this????????
#boot
# print('Initializing Display Drivers')
# i = 16
# while i > 0:
#     sys.stdout.write('.')
#     sys.stdout.flush()
#     time.sleep(random.uniform(0.2, 0.9))
#     i -= 1
# print('\nDone! \n')
#
# print('Initializing Basic I/O')
# i = 16
# while i > 0:
#     sys.stdout.write('.')
#     sys.stdout.flush()
#     time.sleep(random.uniform(0.2, 0.9))
#     i -= 1
# print('\nDone! \n')
#
# print('Initializing Human Input Devices')
# i = 16
# while i > 0:
#     sys.stdout.write('.')
#     sys.stdout.flush()
#     time.sleep(random.uniform(0.2, 0.9))
#     i -= 1
# print('\nDone! \n')
#
# print('Starting LightOS')
# i = 16
# while i > 0:
#     sys.stdout.write('.')
#     sys.stdout.flush()
#     time.sleep(random.uniform(0.2, 0.9))
#     i -= 1
# print('\nDone! \n')

time.sleep(0.8)


usenmls = {}
# passwords
try:
    with open('data.txt', 'r') as data:
        decdat = decrypt_emb2(data.read(), 'gtTfs7Adh6G3j835GkdsJFYU86389llke')
        exec(decdat)
except:
    decdat = ''
    with open('data.txt', 'w+') as data:
        data.write('')
    encrypt_emb2('data.txt', '', enckey, 'gtTfs7Adh6G3j835GkdsJFYU86389llke')




console_log('drawing password screen')
type(usenmpw_menu)
inputchar('\033[11A')
inputchar('\033[5;23H')
name = input('USERNAME: ').upper()
inputchar('\033[7;23H')
passwd = input('PASSWORD: ')
inputchar('\033[2J')
type(loadingscr)
inputchar('\033[11A')
inputchar('\033[10;39H')

if name + '_pwh' in usenmls:
    if usenmls[name + '_pwh'] != str(zlib.crc32(passwd.encode("utf-8"))):
        inputchar('\033[8;23H')
        type(f'WRONG PASSWORD FOR {name}!')
        console_log('password for '+name+'was not correct')
        inputchar('\033[10;23H')
        input('PRESS ENTER TO EXIT')
        exit()
else:
    console_log('making account for ' + name)
    inputchar('\033[2J')
    type(loadingscr)
    inputchar('\033[11A')
    inputchar('\033[10;39H')

    # set up user directory
    # os.mkdir(f'{str(zlib.crc32(name.encode("utf-8")))}')
    # os.mkdir(f'{str(zlib.crc32(name.encode("utf-8")))}/userdir')
    # os.mkdir(f'{str(zlib.crc32(name.encode("utf-8")))}/apps')
    # # os.mkdir(f'{str(zlib.crc32(name.encode("utf-8")))}/log')
    # os.mkdir(f'{str(zlib.crc32(name.encode("utf-8")))}/plugins')
    # os.mkdir(f'{str(zlib.crc32(name.encode("utf-8")))}/startup')


    encrypt_emb2('data.txt', decdat + f'usenmls["{name}_pwh"] = "{zlib.crc32(passwd.encode("utf-8"))}" \n', enckey, 'gtTfs7Adh6G3j835GkdsJFYU86389llke')
    with open('data.txt', 'r') as data:
        decdat = decrypt_emb2(data.read(), 'gtTfs7Adh6G3j835GkdsJFYU86389llke')
        exec(decdat)
    # not used, guess why:
    # with open('data.txt', 'a') as data:
    #     data.write(f'usenmls["{name}_pw"] = "{passwd}" \n')
console_log('password for ' + name + 'was correct')

# store key
try:
    with open(f'{str(zlib.crc32(name.encode("utf-8")))}.kdt', 'r') as data:
        enckeyffte = decrypt_emb2(data.read(), 'hjsgadfjhsfaAHGFYJ7986278KJHhfsK')
        try:
            enckeyff = password_decrypt(enckeyffte.encode("utf-8"), hashlib.sha256(passwd.encode("utf-8")).hexdigest()).decode("utf-8")
        except:
            enckeyff = enckeyffte
            enckeyfftf = password_encrypt(enckeyff.encode("utf-8"), hashlib.sha256(passwd.encode("utf-8")).hexdigest()).decode("utf-8")
            encrypt_emb2(f'{str(zlib.crc32(name.encode("utf-8")))}.kdt', enckeyfftf, enckey, 'hjsgadfjhsfaAHGFYJ7986278KJHhfsK')
        console_log(f'hash of key is: {str(zlib.crc32(enckeyff.encode("utf-8")))}')

except FileNotFoundError:
    enckeyff = write_key().decode("utf-8")
    with open(f'{str(zlib.crc32(name.encode("utf-8")))}.kdt', 'w+') as data:
        data.write('')
    enckeyfftf = password_encrypt(enckeyff.encode("utf-8"), hashlib.sha256(passwd.encode("utf-8")).hexdigest()).decode("utf-8")
    encrypt_emb2(f'{str(zlib.crc32(name.encode("utf-8")))}.kdt', enckeyfftf, enckey, 'hjsgadfjhsfaAHGFYJ7986278KJHhfsK')
    console_log(f'hash of key is: {str(zlib.crc32(enckeyff.encode("utf-8")))}')



# load settings (old way, not used as this is raw code being stored as a text file)
# try:
#     with open(f'{name}_settings.txt', 'r') as sett:
#         exec(sett.read())
# except:
#     with open(f'{name}_settings.txt', 'w+') as sett:
#         sett.write('''mes_setting = ''
# onoff_setting = False
# fo_setting = 1 ''')
#     mes_setting = ''
#     onoff_setting = False
#     fo_setting = 1

# new way, uses pickle
try:
    with open(f'{name}_settings.lset', 'rb') as f:
        onoff_setting, fo_setting, mes_setting, startup_setting = pickle.load(f)
except:
    # try to load legacy settings file and convert, also start with extensions disabled
    startup_setting = False
    try:
        with open(f'{name}_settings.txt', 'r') as sett:
            exec(sett.read())
        # delete legacy setting
        os.remove(f'{name}_settings.txt')
    except:
        startup_setting = False
        mes_setting = ''
        onoff_setting = False
        fo_setting = 1
    with open(f'{name}_settings.lset', 'wb') as f:
        pickle.dump([onoff_setting, fo_setting, mes_setting, startup_setting], f)


# load startup plugins/apps
if 'noloadstartups' in str(sys.argv):
    pass
elif 'loadstartups' in str(sys.argv) or startup_setting:
    files = []
    for (dirpath, dirnames, filenames) in walk('startup'):
        files.extend(filenames)
        break
    filenumls = {}
    startloadloop1 = 0
    for file in files:
        filenumls[str(startloadloop1)] = file
        startloadloop1 += 1
    startloadloop2 = 0
    if startloadloop1 > 0:
        inputchar('\033[12;1H')
    for file in files:
        try:
            dummy, plugn = filenumls[str(startloadloop2)].split('--')
            plugntr = plugn.replace(".py", "")
            # input(f'Press enter to load {plugntr}...')
            type(f'Loading {plugntr}...')
            with open(f'startup/{filenumls[str(startloadloop2)]}', 'r', encoding='utf8') as load:
                loaddat = load.read()
            try:
                exec(loaddat)
                print(f' ({plugntr} loaded!)')
            except Exception as err:
                print(f' ({plugntr} not started, {str(err)})')
            startloadloop2 += 1
        except:
            startloadloop2 += 1
    if startloadloop2 > 0:
        # input(f'Press enter to load LightOS with {startloadloop2} plugins started...')
        print(f'Loading LightOS with {startloadloop2} plugins active... ')

    time.sleep(2)
    filenumls = {}
    files = []
else:
    pass




inputchar('\033[2J')
type(main_menu)
inputchar('\033[11A')
inputchar('\033[3C')
inputchar('\033[2B')
inputchar('\033[2;26H')
type(name)
inputchar('\033[2;49H')
type('TYPE EXIT TO QUIT ')
tuploc = '10;19H'
timup = threading.Thread(target=strttmup, args=())

# sys.stdout.write('\033[10;2H ENTER SELECTION: ')
# usrsel = str(sys.stdin.read(2))
curmen = 'main'

#main
lisn = threading.Thread(target=strtlstn, args=())
lisn.start()
console_log('now in main loop')

mainloop()

