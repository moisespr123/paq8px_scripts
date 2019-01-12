# PAQ8PX file/folder compression + testing script:

This script will compress files and folders by generating a filelist file which will be used by paq8px_v177.exe for compressing. It is also used for testing if you use the -t argument.

If you want to test the archive later, please save the .txt file

# Requirements:
* You'll need a paq8px (latest as of this readme is `paq8px_v177.exe`) executable in the same location as the script. You can download paq8px v177 from here: [https://moisescardona.me/paq8px_downloads](https://moisescardona.me/paq8px_downloads)
* You'll also need Python installed in your machine. This script was tested using Python 3.6.5. Get Python at https://www.python.org/

# Usage:

To compress a file:

```
python paq8px_script.py -i C:\My_file -t
```

The above will use PAQ8PX v177 to compress a file called `My_file` which is in `C:\` into an archive named `My_file.paq8pxv177` which is stored at the same directory as the file, using compression level 9 and using the 'Adaptive learning rate' switch. It will then test the archive because we passed the `-t` argument.

If you want to compress a folder, the command is similar, but you point to a folder/directory:

```
python paq8px_script.py C:\My_folder -t
```

## Arguments:

```
required arguments:
  -i INPUT, --input INPUT
                        Input file or folder to compress. REQUIRED

optional arguments:
  -h, --help            show this help message and exit
  -v VERSION, --version VERSION
                        Version of PAQ8PX to use. Example: 177. Default is 177
  -l LEVEL, --level LEVEL
                        Compression level and switches. Example: 9a to
                        compress using level 9 and with the 'Adaptive learning
                        rate' switch. Default is 9a
  -o OUTPUT, --output OUTPUT
                        Output file to use. If not used, the archive will be
                        saved at the root of the parent folder where the
                        file/folder to compress is located. Do not provide
                        extension
  -t, --test            Optional flag to test the archive after compressing
                        it. It is recommended to use this option. Default is
                        not to test
  -r, --remove          Deletes the filelist text file. Not recommended unless
                        you plan not to test the archive later. Default is not
                        to remove

```

The compression argument is exactly the same as in the paq8px. We are just passing it to the cmd process.

From the paq8px_v177 executable, valid levels and switches are the following:

```
 -LEVEL:
      -0 = store (uses 30 MB)
      -1 -2 -3 = faster (uses 60, 69, 88 MB)
      -4 -5 -6 -7 -8 -9 = smaller (uses 202, 330, 586, 1099, 2125, 4177 MB)
    The listed memory requirements are indicative, actual usage may vary
    depending on several factors including need for temporary files,
    temporary memory needs of some preprocessing (transformations), etc.

    Optional compression SWITCHES:
      b = Brute-force detection of DEFLATE streams
      e = Pre-train x86/x64 model
      t = Pre-train main model with word and expression list
          (english.dic, english.exp)
      a = Adaptive learning rate
      s = Skip the color transform, just reorder the RGB channels
```

You can run `paq8px_v177.exe` for more information. Please note that the script only does compression using paq8px compression level and switches and also does testing by providing the -t argument. Nothing else is implemented in this script.

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