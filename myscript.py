import sys
import re

try:
    from colorama import Fore, Back, Style, init
    init()
except ImportError:  # запасной вариант, чтобы импортированные классы всегда существовали
    class ColorFallback():
        __getattr__ = lambda self, name: ''
    Fore = Back = Style = ColorFallback()


def function_name(filestoprocess):
    logs_list = []
    for input_logs in filestoprocess:
        print("Processing %s" % input_logs)
        with open(input_logs, 'r') as afile:
            f = afile.readlines()
            logs_list.append(f)
    return function_pairs(logs_list)


def function_pairs(logs_list):
    import itertools
    for pair in itertools.combinations(logs_list, r=2):
        print("======================================================")
        function_compare(pair)


def function_compare(pair):
    import difflib
    a_sample = pair[0]
    b_sample = pair[1]
    diff = difflib.ndiff(a_sample, b_sample)
    diff = color_diff(diff)
    print(''.join(diff), end="\n")


date_regex = re.compile(
    r"(?<!\d)(?:0?[1-9]|[12][0-9]|3[01])-(?:0?[1-9]|1[0-2])-(?:19[0-9][0-9]|20[0-2][0-9])(?!\d)")
path_regex = re.compile(
    r"(?:[A-Z]:|[\\\.{0,2}\w+]+\\|\/{0,1}[\.{0,2}\w+]+\/)[^\s\n\,\"\)]+")


def color_diff(diff):
    date_comment = False
    path_comment = False
    other_diff_comment = False
    for line in diff:
        if line.startswith('+'):
            if re.search(date_regex, line):
                date_comment = True
                yield Fore.CYAN + line + Fore.RESET
                if re.search(path_regex, line):
                    path_comment = True
                    yield Fore.CYAN + line + Fore.RESET
            elif re.search(path_regex, line):
                path_comment = True
                yield Fore.CYAN + line + Fore.RESET
            else:
                other_diff_comment = True
                yield Fore.GREEN + line + Fore.RESET
        elif line.startswith('-'):
            if re.search(date_regex, line):
                date_comment = True
                yield Fore.CYAN + line + Fore.RESET
                if re.search(path_regex, line):
                    path_comment = True
                    yield Fore.CYAN + line + Fore.RESET
            elif re.search(path_regex, line):
                path_comment = True
                yield Fore.CYAN + line + Fore.RESET
            else:
                other_diff_comment = True
                yield Fore.RED + line + Fore.RESET
        elif line.startswith('?'):
            yield "" # возможно обозначить как служебную строку yield Fore.BLUE + line + Fore.RESET
        else:
            yield line
    function_comment(date_comment, path_comment, other_diff_comment)


def function_comment(date_comment, path_comment, other_diff_comment):
    if date_comment == True and path_comment == False and other_diff_comment == False:
        print("\n====== Файлы отличаются только временем сборки. ======\n\n")
    if date_comment == False and path_comment == True and other_diff_comment == False:
        print("\n====== Файлы отличаются только местом сборки. ======\n\n")
    if date_comment == True and path_comment == True and other_diff_comment == False:
        print("\n====== Файлы отличаются только временем и местом сборки. ======\n\n")
    if other_diff_comment == True:
        print("\n====== Файлы сильно отличаются. ======\n\n")
    if date_comment == False and path_comment == False and other_diff_comment == False:
        print("\n====== Файлы не имеют отличий. ======\n\n")


function_name(sys.argv[1:])
