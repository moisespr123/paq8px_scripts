import os
import argparse
import subprocess
from multiprocessing import Pool


def extract_file(file: str, output: str, exe_filename: str) -> None:
    cmd = [exe_filename, '-d', file, os.path.join(os.path.dirname(output), os.path.splitext(output)[0])]
    print(cmd)
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":

    '''
    This script will extract paq8px files inside a folder.

    Arguments are explained below.

    Enjoy!
    '''

    parser = argparse.ArgumentParser(description='This script will generate a filelist file which will be used by '
                                                 'paq8px_v185.exe for compressing. It is also used for testing if '
                                                 'you use the -t argument')
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', '--input', help="Input folder to compress. REQUIRED", required=True)
    optional.add_argument('-v', '--version', help='Version of PAQ8PX to use. Example: 185. Default is 185',
                          required=False, default='185')
    parser._action_groups.append(optional)
    args = parser.parse_args()

    input_location = args.input
    filename = os.path.basename(input_location)
    paq8px_version = args.version
    exe_filename = 'paq8px_v' + paq8px_version + '.exe'

    # generates the list

    single_file = False
    if os.path.isdir(input_location):
        print("Extracting each file separately")
        pool = Pool(processes=12)
        for file in os.listdir(input_location):
            file_path = os.path.join(input_location, file)
            pool.apply_async(extract_file, (file_path, file_path, exe_filename,))
        pool.close()
        pool.join()
    print("\nExtraction finished!")
