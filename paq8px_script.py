import os
import argparse
import subprocess
from multiprocessing import Pool
from sys import platform


def set_archive_filename(output: str, paq8px_version: str) -> str:
    basename, ext = os.path.splitext(output)
    if ext == 'paq8px{}'.format(paq8px_version):
        return output
    if ext == 'paq8px':
        return output + paq8px_version
    else:
        return output + '.paq8px' + paq8px_version


def compress_file(file: str, output: str, exe_filename: str, compression_arg: str, paq8px_version: str) -> None:
    output = set_archive_filename(output, paq8px_version)
    if platform == "win32":
        cmd = [exe_filename, compression_arg, file, output]
    else:
        cmd = "{} {} \"{}\" \"{}\"".format(exe_filename, compression_arg, file, output)
    print(cmd)
    subprocess.run(cmd, shell=True)


def test_archive(input_location: str, archive: str, exe_filename: str, paq8px_version: str) -> None:
    archive = set_archive_filename(archive, paq8px_version)
    if platform == "win32":
        cmd = [exe_filename, '-t', archive]
    else:
        cmd = "{} -t \"{}\" \"{}\"".format(exe_filename, archive, input_location)
    print(cmd)
    subprocess.run(cmd, shell=True)


def create_text_file(filelist: list, input_location: str, filename: str) -> str:
    if filelist:
        filelist_path = os.path.join(input_location, filename + '.txt')
        print("Writing filelist.txt")
        txt_file = open(filelist_path, 'w')
        txt_file.write('\n')
        for file in filelist:
            if not os.path.isdir(file):
                txt_file.write(file + '\n')
        txt_file.close()
        return '@' + filelist_path
    else:
        return input_location


def get_output_location(args: argparse) -> str:
    if not args.output:
        output_location = args.input
    else:
        output_location = args.output
    return output_location


def get_exe_filename(paq8px_version: str, nativecpu: bool) -> str:
    exe_filename = 'paq8px_v' + paq8px_version
    if nativecpu:
        exe_filename += "_nativecpu"
    if platform == "win32":
        exe_filename += ".exe"
    elif platform.startswith("linux"):
        exe_filename = "./" + exe_filename
    return exe_filename


def parse_action(args: argparse) -> ():
    action = "compress"
    action_finished = "Compression"
    if args.test and not args.test_only:
        action += " and test"
        action_finished += " and testing"
    if args.test_only:
        action = "test"
        action_finished = "Testing"
    return action, action_finished


def single_threaded_compression(args: argparse, input_location: str, output_location: str, filename: str,
                                exe_filename: str, paq8px_version: str, compression_args: str) -> None:
    filelist = []
    action, _ = parse_action(args)
    if os.path.isdir(input_location):
        print("Listing files to {}".format(action))
        for dir_, _, files in os.walk(input_location):
            for fileName in sorted(files):
                rel_file = os.path.join(fileName)
                filelist.append(rel_file)
                print(rel_file)
        single_file = False
    else:
        print("file to {}".format(action), filename)
        single_file = True

    if (filelist or single_file) and not args.test_only:
        filename = create_text_file(filelist, input_location, filename)
        print("\nStarting compression...\n")
        compress_file(filename, output_location, exe_filename, compression_args, paq8px_version)
    if args.test or args.test_only:
        print("\nVerifying archive...\n")
        test_archive(input_location, output_location, exe_filename, paq8px_version)


def multithreaded_compression(args: argparse, input_location: str, output_location: str, filename: str,
                              exe_filename: str, paq8px_version: str, compression_args: str) -> None:
    if os.path.isdir(input_location):
        print("Compressing each file separately")
        pool = Pool()
        for file in sorted(os.listdir(input_location)):
            file_path = os.path.join(input_location, file)
            pool.apply_async(compress_file, (file_path, file_path, exe_filename, compression_args, paq8px_version))
        pool.close()
        pool.join()
    else:
        print("file to compress:", filename)
        print("\nStarting compression...\n")
        compress_file(input_location, output_location, exe_filename, compression_args, paq8px_version)
    if args.test or args.test_only:
        print("\nVerifying archive is not yet implemented for multi-threaded individual file compression...\n")


def main() -> None:
    """
    This script will generate a filelist file which will be used by paq8px for compressing and testing if you use the
    -t argument.

    Arguments are explained below in the code and in the readme

    If you want to test the archive later, please save the .txt file

    Enjoy!
    """

    parser = argparse.ArgumentParser(description='This script will generate a filelist file which will be used by '
                                                 'paq8px_v207 for compressing. It is also used for testing if you '
                                                 'use the -t or -to argument')
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('-i', '--input', help="Input file or folder to compress. REQUIRED", required=True)
    optional.add_argument('-v', '--version', help='Version of PAQ8PX to use. Example: 207. Default is 207',
                          required=False, default='207')
    optional.add_argument('-l', '--level', help="Compression level and switches. Example: 9a to compress using level 9 "
                                                "and with the 'Adaptive learning rate' switch. Default is 9",
                          required=False, default='9')
    optional.add_argument('-o', '--output', help="Output file to use. If not used, the archive will be saved at the "
                                                 "root of the parent folder where the file/folder to compress is "
                                                 "located. Do not provide extension", required=False, default=None)
    optional.add_argument('-t', '--test', help="Optional flag to test the archive after compressing it. It is "
                                               "recommended to use this option. Default is not to test",
                          required=False, action='store_true')
    optional.add_argument('-to', '--test-only', help="Skip compression and just test the archive.",
                          required=False, action='store_true')
    optional.add_argument('-r', '--remove', help="Deletes the filelist text file. Not recommended unless you plan not "
                                                 "to test the archive later. Default is not to remove", required=False,
                          default=False, action='store_true')
    optional.add_argument('-mt', '--multithread', help="Compresses each file on a separate thread. This creates "
                                                       "individual archives with just one file", required=False,
                          default=False, action='store_true')
    optional.add_argument('-n', '--nativecpu', help="Use the native CPU version. "
                                                    "These versions usually ends with _nativecpu and may provide "
                                                    "performane improvements on your machine over the generic version",
                          required=False,
                          default=False, action='store_true')
    args = parser.parse_args()

    # Variables:
    paq8px_version = args.version
    exe_filename = get_exe_filename(paq8px_version, args.nativecpu)
    compression_args = '-' + args.level
    input_location = args.input
    output_location = get_output_location(args)
    filename = os.path.basename(input_location)

    # Compression
    if not args.multithread:
        single_threaded_compression(args, input_location, output_location, filename,
                                    exe_filename, paq8px_version, compression_args)
    else:
        multithreaded_compression(args, input_location, output_location, filename,
                                  exe_filename, paq8px_version, compression_args)

    # Remove file list if not in multithreaded mode.
    if args.remove and not args.multithread:
        print("\nRemoving the filelist file")
        os.remove(os.path.join(input_location, filename + '.txt'))
    _, action_finished = parse_action(args)
    print("\n{} finished!".format(action_finished))


if __name__ == "__main__":
    main()
