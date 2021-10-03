import os
import re
import shutil

textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))


def str_regex_list_match(string, regex_list):
    temp = '|'.join(regex_list)
    if re.match(temp, string):
        return True


def get_bin_files(directory, skip_dir=None, skip_files=None):
    binfilelist = []
    listfiles(directory, binfilelist, skip_dir, skip_files)
    return binfilelist


def listfiles(directory, binfilelist, skip_dir=None, skip_files=None):
    for filename in os.listdir(directory):
        if skip_dir is not None:
            if filename in skip_dir:
                continue
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            if skip_files is not None:
                if str_regex_list_match(filename, skip_files):
                    continue
            is_bin = is_binary_string(open(f, 'rb').read(1024))
            if is_bin:
                binfilelist.append(f)
        else:
            listfiles(f, binfilelist, skip_dir, skip_files)



if __name__ == '__main__':
    # get_bin_files('c:/tmp', ['.git', '.idea', '.gradle'], [".*jar"])
    files = get_bin_files('c:\\tmp\\sample-aap', ['.git', '.idea', '.gradle'])
    for file in files:
        print(file)
        newpath = file.replace('sample-aap', 'newapp')
        os.makedirs(os.path.dirname(newpath), exist_ok=True)
        shutil.copy(file, newpath)
