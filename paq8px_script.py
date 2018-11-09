import os
import argparse
import subprocess

filelist = []

'''
This script will generate a filelist file which will be used by paq8px for compressing and testing if you use the -t argument.

Arguments are explained below in the code and in the readme

If you want to test the archive later, please save the .txt file

Enjoy!
'''

parser = argparse.ArgumentParser(description='This script will generate a filelist file which will be used by paq8px_v142.exe for compressing. It is also used for testing if you use the -t argument')
optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
required.add_argument('-i', '--input', help="Input file or folder to compress. REQUIRED", required=True)
optional.add_argument('-v', '--version', help='Version of PAQ8PX to use. Example: 170. Default is 170', required=False, default='170')
optional.add_argument('-l', '--level', help="Compression level and switches. Example: 9a to compress using level 9 and with the 'Adaptive learning rate' switch. Default is 9a", required=False, default='9a')
optional.add_argument('-o', '--output', help="Output file to use. If not used, the archive will be saved at the root of the parent folder where the file/folder to compress is located. Do not provide extension", required=False, default=None)
optional.add_argument('-t', '--test', help="Optional flag to test the archive after compressing it. It is recommended to use this option. Default is not to test", required=False, action='store_true')
optional.add_argument('-r', '--remove', help="Deletes the filelist text file. Not recommended unless you plan not to test the archive later. Default is not to remove", required=False, default=False, action='store_true')
parser._action_groups.append(optional)
args = parser.parse_args()

#variables:
compression_arg = '-' + args.level
input_location = args.input
if not args.output:
    output_location = args.input
else:
    output_location = args.output
filename = os.path.basename(input_location)
paq8px_version = args.version
exe_filename = 'paq8px_v' + paq8px_version + '.exe'

#generates the list
single_file = False
if os.path.isdir(input_location):
    print("Listing files to compress")
    for dir_, _, files in os.walk(input_location):
        for fileName in files:
            relDir = os.path.relpath(dir_, os.path.dirname(input_location))
            relFile = os.path.join(relDir, fileName)
            filelist.append(relFile)
            print(relFile)
else:
    print("file to compress:", filename)
    single_file = True

if filelist or single_file:
    if filelist:
        print("Writing filelist.txt")
        txt_file = open(os.path.dirname(input_location) + '/' + filename + '.txt', 'w')
        txt_file.write('\n')
        for file in filelist:
            if not os.path.isdir(file):
                txt_file.write(file + '\n')
        txt_file.close()
        input_file = '@' + os.path.dirname(input_location) + '/' + filename + '.txt'
    else:
        input_file = filename
    print("\nStarting compression...\n")
    cmd = [exe_filename, compression_arg, input_file, output_location + '.paq8px' + paq8px_version]
    subprocess.run(cmd, shell=True)
    if args.test:
        print("\nVerifying archive...\n")
        if not os.path.dirname(output_location):
            archive_to_test = os.path.dirname(os.path.realpath(__file__)) + '/' + output_location
        else:
            archive_to_test = output_location
        cmd = [os.path.dirname(os.path.realpath(__file__)) + '/' + exe_filename, '-t', archive_to_test + '.paq8px' + paq8px_version]
        subprocess.run(cmd, shell=True, cwd=os.path.dirname(input_location))
    if args.remove:
        print("\nRemoving the filelist file")
        os.remove(os.path.dirname(input_location) + '/' + filename + '.txt')
print("\nCompression finished!")
