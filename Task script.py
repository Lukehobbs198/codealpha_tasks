import os
import sys
import shutil
import socket

def help():
    print("A script to backup of user files.\nIt can upload and download previous backup from a cloud server.")
    print("\nUsage: ./script.py <operation>")
    print("Operations:\n\t--backup\tBacks up the user directory into an archive")
    print("\t--help\t\tDisplay this help menu")
    print("\t--upload\tUpload files to specified server")
    print("\t--download\tDownloads the files from server")
    print("\t--address\tProvide address of the backup server")
    print("\nExample: ./script.py --upload backup.zip --address server.org")

def backup():
    path = f"{os.environ['HOMEDRIVE']}/{os.environ['HOMEPATH']}"
    try:
        shutil.make_archive('backup', 'zip', path)
        print("[*] Message: Backup successful.")
    except:
        print("[*] Error: Backup failed.")

if len(sys.argv) < 2:
    print("[*] Error: Insufficient arguments.")
    help()
    exit()

if sys.argv[1] == '--help':
    help()
    exit()

if sys.argv[1] == '--backup':
    backup()
    exit()

if '--upload' in sys.argv:
    if len(sys.argv) < (sys.argv.index('--upload') + 2):
        print("[*] Message: Taking backup.zip as the file to upload")
        file = 'backup.zip'
    else:
        if sys.argv.index('--upload') + 1 != sys.argv.index('--address'):
            file = sys.argv[sys.argv.index('--upload') + 1]
        else:
            file = 'backup.zip'

    if '--address' not in sys.argv:
        print("[*] Error: No address is provided")
        exit()
 
    if len(sys.argv) < (sys.argv.index('--address') + 2):
        print("[*] Error: No address is provided")
        exit()
 
    server = sys.argv[sys.argv.index('--address') + 1]
    
    try:
        with open(file, 'rb') as fp: 
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((server, 1028))
                print("[*] Message: Uploading")
                client.send(str("UPLOAD " + file).encode())
                client.recv(1024) 
                data = fp.read(1024)
                while data:
                    client.send(data)
                    data = fp.read(1024)

                client.close()
                print("[*] Message: Upload successful")
            except:
               print("[*] Error: Connection failed") 

    except:
        print("[*] Error: Cannot read file.")
    finally:
        exit()

elif '--download' in sys.argv: 
    if len(sys.argv) < (sys.argv.index('--download') + 2):
        print("[*] Message: Downloading latest backup")
        file = 'backup.zip'
    else:
        if sys.argv.index('--download') + 1 != sys.argv.index('--address'):
            file = sys.argv[sys.argv.index('--download') + 1]
        else:
            file = 'backup.zip'

    if '--address' not in sys.argv:
        print("[*] Error: No address is provided")
        exit()
 
    if len(sys.argv) < (sys.argv.index('--address') + 2):
        print("[*] Error: No address is provided")
        exit()

    server = sys.argv[sys.argv.index('--address') + 1]
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server, 1028))

        with open(file, 'wb') as fp:
            print("[*] Message: Downloading...")
            
            client.send(str("DOWNLOAD " + file).encode())
            data = client.recv(1024)
            while data:
                fp.write(data)
                data = client.recv(1024)
        client.close()
        print("[*] Message: Download complete") 
    except:
        print("Error: Connection failed")
    finally:
        exit()
