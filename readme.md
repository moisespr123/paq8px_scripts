# PAQ8PX file/folder compression + testing script:

This script will compress files and folders by generating a filelist file which will be used by paq8px for compressing. It is also used for testing if you use the -t argument.

If you want to test the archive later, please save the .txt file

# Requirements:
* You'll need a paq8px (latest as of this readme is `paq8px_v207`) executable in the same location as the script. You can download paq8px v207 Linux builds from here: [https://moisescardona.me/paq8px_downloads](https://moisescardona.me/paq8px_downloads)
* You'll also need Python installed in your machine. This script was tested using Python 3.10.6. Get Python at https://www.python.org/

# Usage:

```
usage: paq8px_script.py [-h] -i INPUT [-v VERSION] [-l LEVEL] [-o OUTPUT] [-t] [-to] [-r] [-mt]
                        [-n]

This script will generate a filelist file which will be used by paq8px_v207 for compressing. It is
also used for testing if you use the -t or -to argument

options:
  -h, --help            show this help message and exit

required arguments:
  -i INPUT, --input INPUT
                        Input file or folder to compress. REQUIRED

optional arguments:
  -v VERSION, --version VERSION
                        Version of PAQ8PX to use. Example: 207. Default is 207
  -l LEVEL, --level LEVEL
                        Compression level and switches. Example: 9a to compress using level 9 and
                        with the 'Adaptive learning rate' switch. Default is 9
  -o OUTPUT, --output OUTPUT
                        Output file to use. If not used, the archive will be saved at the root of
                        the parent folder where the file/folder to compress is located. Do not
                        provide extension
  -t, --test            Optional flag to test the archive after compressing it. It is recommended
                        to use this option. Default is not to test
  -to, --test-only      Skip compression and just test the archive.
  -r, --remove          Deletes the filelist text file. Not recommended unless you plan not to
                        test the archive later. Default is not to remove
  -mt, --multithread    Compresses each file on a separate thread. This creates individual
                        archives with just one file
  -n, --nativecpu       Use the native CPU version. These versions usually ends with _nativecpu
                        and may provideperformane improvements on your machine over the generic
                        version
```

You can run the `paq8px_v207` executable for more information. Please note that the script only does compression using paq8px compression level and switches and also does testing by providing the -t argument. Nothing else is implemented in this script.

To extract a file, simply use the paq8px executable.

Please note PAQ8PX is an experimental compression software and is in active development by the folks at the https://encode.ru forum.

It is highly recommended that you test your archives.

# Links:
* PAQ8PX Forum thread: [https://encode.ru/threads/342-paq8px](https://encode.ru/threads/342-paq8px)
* PAQ8PX repository: [https://github.com/hxim/paq8px](https://github.com/hxim/paq8px)

# License:

```
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details at
    Visit <http://www.gnu.org/copyleft/gpl.html>.


    For a summary of your rights and obilgations in plain laguage visit
    https://tldrlegal.com/license/gnu-general-public-license-v2
 ```

## Enjoy!