import os
import sys
import subprocess
filelist = []

'''
This script will generate a filelist file which will be used by paq8px_v142.exe for compressing. It is also used for testing if you use the -t argument.
Args:
1. The argument you want to use for compression
2. The path of the file or folder you want to compress
3. optionally, pass -t to test the archive after testing.

If you want to test the archive later, please save the .txt file

Enjoy!
'''

if len(sys.argv) > 2:
    #variables:
    compression_arg = sys.argv[1]
    location = sys.argv[2]
    filename = os.path.basename(location)

    #generates the list
    if os.path.isdir(location):
        print("Listing files to compress")
        for dir_, _, files in os.walk(location):
            for fileName in files:
                relDir = os.path.relpath(dir_, os.path.dirname(location))
                relFile = os.path.join(relDir, fileName)
                filelist.append(relFile)
                print(relFile)
    else:
        print("file to compress:", filename)
        filelist.append(filename)

    if filelist:
        print("Writing filelist.txt")
        txt_file = open(os.path.dirname(location) + '/' + filename + '.txt', 'w')
        txt_file.write('\n')
        for file in filelist:
            if not os.path.isdir(file):
                txt_file.write(file + '\n')
        txt_file.close()
        print("Starting compression...")
        cmd = ['paq8px_v142.exe', compression_arg, '@' + os.path.dirname(location) + '/' + filename + '.txt', location + '.paq8pxv142']
        subprocess.run(cmd, shell=True)
        if len(sys.argv) > 3:
            if sys.argv[3] == '-t':
                print("Verifying archive")
                cmd = [os.path.dirname(os.path.realpath(__file__)) + '/paq8px_v142.exe', '-t', location + '.paq8pxv142']
                print(os.path.dirname(os.path.realpath(__file__)) + '/paq8px_v142.exe', '-t', location + '.paq8pxv142')
                subprocess.run(cmd, shell=True, cwd=os.path.dirname(location))

