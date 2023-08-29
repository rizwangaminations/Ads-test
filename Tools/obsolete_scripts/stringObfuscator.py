import os, sys
import argparse
import print_utils
import io, re
import hashlib
import string
import collections

sys.setrecursionlimit(3500)

LOGGER = print_utils.Logger()
Blue = print_utils.bcolors.OKBLUE
WARNING = print_utils.bcolors.WARNING
Fail = print_utils.bcolors.FAIL
BOLD = print_utils.bcolors.BOLD
okGreen = print_utils.bcolors.OKGREEN

fileNames_list = []
header_list = []
add_header_later_in_file_list = []
obfuscatorHeader = ''
assertCounter = 0

ignore_string_list = ['\", \"' , '\",\"', '\" \"', '\"\"', '\".\"']
# ignore_line_list = ['.AddMember', 'extern', '**', "LevelConfigHandler::initializeLevelConfig"] old ignore list
ignore_line_list = [ "#import", "private:", "public:", "#endif", '**', "#ifndef", "#include", "LevelConfigHandler::initializeLevelConfig", "dec2hex", "CS_NSLOG", "CCASSERT","CCAssert"]
assert_string_list = ['assert', 'CCASSERT', 'CC_ASSERT']
file_extention_list = ['.cpp', '.mm', '.h']

left_pairs  = ['(','[','{']
right_pairs = [')',']','}']
file_lines_dict = {}
balancedLines = []

format_specifier_list = ['%c', '%d', '%e', '%E', '%f', '%g', '%G', '%hi', '%hu', '%i', '%ld', '%li', '%lf', '%Lf', '%lu', '%lli', '%lld', '%lu', '%l', '%o', '%p', '%s', '%u', '%x', '%X', '%n', '%%', '%@']
substrings_list = []

commentReg = re.compile(r'''(//[^\n]*(?:\n|$))''', re.VERBOSE)
# re.compile(r'''(//[^\n]*(?:\n|$))|(/\*.*?\*/)''', re.VERBOSE)

StringReg = re.compile(r'""|"\\""|"(.*?[^\\"])"')
# re.compile(r'"(?<=\").*?(?=\")"') working
#re.compile(r'"(?<=\").*?[^\\"](?=\")"')

def join_path(*args):
    return os.path.normpath(os.path.join(*args))

def is_valid_line(line):
    trim_line = line.strip()
    for ignore_line in ignore_line_list:
        if trim_line.startswith(ignore_line):
            return False

    if not is_line_header(line) and not is_comments(line) and is_not_already_obfuscated(line):
        return True
    return False

def is_line_header(line):
    trim_line = line.strip()
    if trim_line.startswith("#include"):
        header_list.append(line)
        return True

    if trim_line.startswith("#import"):
        return True
    return False

def is_comments(content):
    return commentReg.search(content)

def is_not_already_obfuscated(content):
    if content.find("") == -1 and content.find("CS_ASSERT") == -1 and content.find("CCLOG") == -1:
        return True
    return False

def is_valid_string(content):
    if len(content) < 3:
        return False
    content = "\"" + content + "\""
    for ignore_string in ignore_string_list:
        if content == ignore_string:
            return False
    return True

def get_real_line(line, string):
    result = line.index(string)
    postfix = ""
    prevBrak1Count = 0
    prevBrak2Count = 0
    prevBrak3Count = 0
    for i in range(result + len(string), len(line)) :
        # prevIndex = i-1
        if (line[i] == ')' and prevBrak1Count <= 0) or (line[i] == ']' and prevBrak2Count <= 0) or (line[i] == '}' and prevBrak3Count <= 0):
            break
        elif line[i] == '(':
            prevBrak1Count += 1
            postfix += line[i]
        elif line[i] == '[':
            prevBrak2Count += 1
            postfix += line[i]
        elif line[i] == '{':
            prevBrak3Count += 1
            postfix += line[i]

        elif line[i] == ')':
            prevBrak1Count -= 1
            postfix += line[i]
        elif line[i] == ']':
            prevBrak2Count -= 1
            postfix += line[i]
        elif line[i] == '}':
            prevBrak3Count -= 1
            postfix += line[i]

        else :
            postfix += line[i]

    return string + postfix

def get_replacement_line_for_assert(line, string, fileName, objC_line):
    realLine = line
    rString = get_real_line(line, string)
    if not objC_line:
        content = string[1:-1]
    else:
        content = string[2:-1]
    generate_new_sub_strings(content)
    existing_specifiers_list = generate_existing_format_specifier(rString.replace(string, ""))

    newline = ""
    rString2 = rString
    count = 0
    variableName_list = []
    leading_spaces = get_leading_Spaces(line)
    for substring in substrings_list:
        count = count + 1

        variableName = (fileName[:4] + get_current_var_counter() + str(count)).lower()
        variableName_list.append(variableName)
        if not objC_line:
            newline = newline + leading_spaces + "const std::string " + variableName + " = std::string(STR_RENAME(\"" + substring + "\")).c_str();\n"
        else:
            newline = newline + leading_spaces + "const NSString* " + variableName + " = @(std::string(STR_RENAME(\"" + substring + "\")).c_str());\n"
        rString2 = rString2.replace(substring, "%+")

    del substrings_list[:]

    if not variableName_list:
        return line

    strings = get_strings(rString2)
    rline = ""
    for subString in strings:
        if subString.find('%') != -1:
            rline = get_new_line(subString, existing_specifiers_list, variableName_list, objC_line)
        else:
            print("i am here")
            # return replace_string_in_line(line, fileName)

    line = newline + line.replace(rString, rline)
    return line

def get_simple_replacement_line(line, string, rStringSimple):
    if line.find("NSLog") != -1:
        return line.replace("NSLog", "CS_NSLOG")
    else:
        return line.replace(string, rStringSimple)

def generate_new_sub_strings(content):
    for x in format_specifier_list:
        if content.find(x) != -1:
            contentlist = content.split(x)
            for subContent in contentlist:
                if subContent.find('%') != -1:
                    generate_new_sub_strings(subContent)
                elif not subContent.isspace() and not subContent == '' and not len(subContent) == 1 and not subContent == ", ":
                    substrings_list.append(subContent)
            break
 
def generate_existing_format_specifier(line):
    specifiers = line.split(',')
    specifiers_list = []
    for x in specifiers:
        specifiers_list.append(x.lstrip())

    while '' in specifiers_list:
        specifiers_list.remove('')
    return specifiers_list

def get_new_line(mapString, exitingSpecifiers, newSpecifiers, objC_line):
    line = "#^1&@"
    positions = mapString.split('%')
    indexN = 0
    indexE = 0
    for position in positions:
        if position == '+':
            if not objC_line:
                line = line + ", " + newSpecifiers[indexN] + ".c_str()"
            else:
                line = line + ", " + newSpecifiers[indexN]
            indexN = indexN+1
        elif position != "":
            try:
                line = line + ", " + exitingSpecifiers[indexE]
                indexE = indexE+1
            except IndexError:
                LOGGER.e("Index out of range %s" % str(indexE) , 0 , Fail)
                pass
            continue
    if not objC_line:
        mapString = mapString.replace("+", "s")
        return line.replace("#^1&@", "\"" + mapString + "\"")
    else:
        mapString = mapString.replace("+", "@")
        return line.replace("#^1&@", "@\"" + mapString + "\"")

def get_strings(content):
    return StringReg.findall(content)

def add_header_in_file(outFile):
    if not any(obfuscatorHeader in header for header in header_list):
        codeFile = open(outFile).read()
        lines = codeFile.splitlines()
        try:
            result = lines.index(header_list[0])
        except IndexError:
            result = -1
        
        lines.insert(result+1, obfuscatorHeader)

        f = open(outFile, "w")

        for line in lines:
            f.write(line+"\n")
        f.close()
    del header_list[:]

def get_leading_Spaces(line):
    trim_line = line.strip()
    leading_spaces_count = len(line) - len(trim_line.lstrip())
    leading_spaces = ""

    for s in range(0,leading_spaces_count):
        leading_spaces = leading_spaces + " "

    return leading_spaces

def get_current_var_counter():
    global assertCounter
    assertCounter = assertCounter+1
    return str(assertCounter)

def add_header_later_in_file():
    del header_list[:]
    newList = list(dict.fromkeys(add_header_later_in_file_list))
    
    for file in newList:
        LOGGER.i("Adding header in file: %s" % file, 0 , BOLD)
        codeFile = open(file).read()
        lines = codeFile.splitlines()
        for line in lines:
            is_line_header(line)
        add_header_in_file(file)
    
    LOGGER.i("Header added" , 0 , okGreen)
    del header_list[:]

def is_line_balanced(case):
    count = 0
    for char in left_pairs:
        count += case.count(char)
    for char in right_pairs:
        count -= case.count(char)

    if count == 0 or count % 1:
        return True
    else:
        return False

def is_valid_single_line(line):
    line = line.strip()
    strings = get_strings(line)
    if strings:
        for string in strings:
            line = line.replace("\""+string+"\"","")
    if len(line) > 0:
        return True
    return False

def isObjC_line(line,string):
    string = "\"" + string + "\""
    index = line.index(string)
    if index-1 != -1 and line[index-1] == '@':
        return True
    else: 
        False
#++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++

def replace_string_in_line(line, fileName):
    strings = list(dict.fromkeys(get_strings(line)))
    leadingSpaces = get_leading_Spaces(line)
    if strings and is_valid_line(line):
        for string in strings:
            if is_valid_string(string):
                objC_line = isObjC_line(line,string)
                
                if objC_line:
                    rStringSimple = "@((\"%s\"))" %string
                    string = "@\"" + string + "\""
                else:
                    rStringSimple = "(\"%s\")" %string
                    string = "\"" + string + "\""

                trim_line = line.strip()
                if string.find('%') != -1:
                    newline = line.replace(string,rStringSimple)
                    return newline
                    # line = get_replacement_line_for_assert(line, string, fileName, objC_line)

                elif any(subAssert in trim_line for subAssert in assert_string_list):
                    ignore_dir_list = line.split('(')
                    newline = replaceLast(line, "&&", ",", replacements=1)
                    newline = newline.replace(ignore_dir_list[0],"CS_ASSERT")
                    # print ignore_dir_list[0]
                    return leadingSpaces+newline
                    # variableName = (fileName[:4] + get_current_var_counter()).lower()
                    # newline = line.replace(string, variableName + ".c_str()")
                    # newline = line.replace(string, variableName + ".c_str()")
                    # line = newline
        
                else:
                    return get_simple_replacement_line(line, string, rStringSimple)
    return line

def replaceLast(source, target, replacement, replacements=1):
    return replacement.join(source.rsplit(target, replacements))

def get_one_balanced(line):
    if len(balancedLines) > 0:
        balancedLines.sort(key=len)
        for x in balancedLines:
            if x.find(line) != -1 and x[-1] == ';':
                lineBreak = x.split('\n')
                totalLines = len(lineBreak)
                linestoSkip = 0
                count = 0
                for subLine in lineBreak:
                    if subLine.find(line) != -1:
                        linestoSkip = count
                    count+=1
                    pass
                return (x,totalLines-linestoSkip)
           
    del balancedLines[:]
    return ("",0)

def get_line_farward(lines, centerIndex, farwad):
    currline = lines[centerIndex]
    if farwad == 0:
        return currline
        pass
    for x in range(1,farwad):
        currline = currline + "\n" + lines[centerIndex+x]
        pass
    return currline

def get_line_backward(lines, centerIndex, backward):
    currline = ""
    if backward == centerIndex:
        return ""
        pass
    for x in range(backward,centerIndex):
        currline = currline + lines[x] + "\n"
        pass
    return currline
    
def generate_balanced_lines(currline, file, index):
    codeFile = open(file).read()
    lines = codeFile.splitlines()
    total_lines = len(lines)

    if index+1 != total_lines:
        nLine = currline + "\n" + lines[index+1]
        if is_line_balanced(nLine) and nLine[-1] == ';':
            balancedLines.append(nLine)
            return

    if index-1 != -1:
        bLine = lines[index-1] + "\n" + currline
        if is_line_balanced(bLine) and bLine[-1] == ';':
            balancedLines.append(bLine)
            return

    for forward in range(index,total_lines):
        currline = get_line_farward(lines, index, forward-index)

        backwardIndex = index
        backline = currline

        if not is_line_balanced(currline):
            while backwardIndex > -1:
                backline = get_line_backward(lines, index, backwardIndex) + currline

                if is_line_balanced(backline):
                    balancedLines.append(backline)
                    backwardIndex = -1

                backwardIndex-=1
                pass
        else:
            balancedLines.append(backline)
            break

def get_strings_fixed(line):
    realLine = line
    strings = list(dict.fromkeys(get_strings(line)))
    indINString = {}
    indexPairs = {}
    btwStr = ""

    newStrings = {}
    chunks = []
    totalStr = len(strings)
    if strings:
        for x in range(0,totalStr):
            indINString[x] = line.index(strings[x])  
    
        indINString = sorted(list(indINString.items()), key = lambda kv:(kv[1], kv[0]))

        for x in range(0,totalStr):
            indexPairs[((indINString[x])[1])-1] = ((indINString[x])[1]) + len(strings[(indINString[x])[0]]) + 1
        
        indexPairs = sorted(list(indexPairs.items()), key = lambda kv:(kv[1], kv[0]))
        
        cCount = 0
        for x in range(0,totalStr):
            if x + 1 < totalStr:
                start = indexPairs[x][1]
                end = indexPairs[x+1][0]
                for y in range(start, end):
                    btwStr = btwStr+line[y]

            indlist = list(indINString)
            btwStr = btwStr.rstrip()
            btwStr = btwStr.rstrip(" ")
            btwStr = btwStr.rstrip("\n")
            if len(btwStr) > 0:
                chunks.append((cCount, (indlist[x])[0]))     
                cCount += 1
            else:
                chunks.append((cCount, (indlist[x])[0]))     
            btwStr = ""

    for x in chunks:
        line = line.replace("\""+strings[x[1]]+"\"", "%"+str(x[0])+"$")
        if x[0] in newStrings:
            newStrings[x[0]] = newStrings[x[0]] + " " + strings[x[1]]
        else:
            newStrings[x[0]] = strings[x[1]]

    for x ,y in list(newStrings.items()):
        subString = "%"+str(x)+"$"
        count = line.count(subString)
        if count > 1 :
            line = line.replace(subString,"",count-1)

        if line.find(subString)!= -1:
            line = line.replace(subString, "\""+y+"\"")

    if realLine != line or 1 == 1:
        subLines = line.split('\n')
        line = ""
        for x in subLines:
            x = x.rstrip()
            x = x.rstrip(" ")
            x = x.rstrip("\n")
            if x != '' or len(x) != 0:
                line = line + x + "\n"

    return line

def checkAndReportNotObfuscatedStrings():
    StringCount = 0
    StringCountInFile = 0
    for file in fileNames_list:
        # LOGGER.i("Checking strings in file: %s" % file, 0 , BOLD)
        del header_list[:]

        codeFile = open(file).read()
        lines = codeFile.splitlines()

        lineIndex = 0
        if StringCountInFile > 0:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        StringCountInFile = 0

        while lineIndex < len(lines):
            line = lines[lineIndex]
            start = lineIndex
            if is_valid_line(line):
                strings = list(dict.fromkeys(get_strings(line)))
                if strings:
                    for string in strings:
                        if is_valid_string(string) and string != "":
                            fixedline = line
                            keyLine = (fixedline,0)
                            if not is_line_balanced(line):
                                generate_balanced_lines(line, file, lineIndex)
                                keyLine = get_one_balanced(line)
                                lineIndex = lineIndex + keyLine[1]
                                fixedline = get_strings_fixed(keyLine[0])
                                fixedline = fixedline[:-1]
                            else:
                                if not is_valid_single_line(fixedline):
                                    LOGGER.i("Incompatible line: %s" %fixedline, 0 , Fail)
                                    break
                            if fixedline.find('CS_ASSERT') == -1 and len(fixedline) > 0 and fixedline[-1] == ";":
                                StringCountInFile += 1
                                StringCount += 1
                                if StringCountInFile > 0:
                                    LOGGER.i("In file: "+ file , 0 , BOLD)
                                LOGGER.i("String not obfuscated at line number: "+ str(start) , 0 , Blue)
                                # LOGGER.i("File: \""+filename+"\"" , 0 , BOLD)
                                LOGGER.i("Line : \""+fixedline.strip()+"\"" , 0 , BOLD)
                            break
            
            if start == lineIndex:
                lineIndex+=1 

    if StringCount > 0:
        LOGGER.i("Total not obfuscated string Count: "+ str(StringCount), 0 , Fail)
    else:
        LOGGER.i("No string found to obfuscte", 0 , Blue)

    pass

def obfuscate_File(file, lineIndex, isChanged):
    codeFile = open(file).read()
    lines = codeFile.splitlines()
    
    filename, extension = os.path.splitext(file)

    while lineIndex < len(lines):
        line = lines[lineIndex]
        start = lineIndex
        if is_valid_line(line):
            strings = list(dict.fromkeys(get_strings(line)))
            if strings:
                for string in strings:
                    if is_valid_string(string):
                        fixedline = line
                        keyLine = (fixedline,0)
                        if not is_line_balanced(line):
                            generate_balanced_lines(line, file, lineIndex)
                            keyLine = get_one_balanced(line)
                            lineIndex = lineIndex + keyLine[1]
                            fixedline = get_strings_fixed(keyLine[0])
                            fixedline = fixedline[:-1]
                        else:
                            if not is_valid_single_line(fixedline):
                                LOGGER.i("Incompatible line: %s" %fixedline, 0 , Fail)
                                break
                        newline = replace_string_in_line(fixedline.rstrip(), os.path.splitext(os.path.basename(filename))[0])
                        if keyLine[0] != newline:
                            LOGGER.i("Replacing: \"%s\"" %string , 0 , Blue)
                            LOGGER.i("In Line: %s" %fixedline, 0 , BOLD)
                            isChanged = True
                            file_lines_dict[keyLine[0]] = newline 
                        break
        
        if start == lineIndex:
            lineIndex+=1          
        # return obfuscate_File(file, lineIndex, isChanged)
    
    return isChanged

def obfuscate_strings_in_File():
    for file in fileNames_list:
        LOGGER.i("obfuscating file: %s" % file, 0 , BOLD)
        del header_list[:]

        codeFile = open(file).read()
        lines = codeFile.splitlines()
        
        global assertCounter
        assertCounter = 0
        filename, extension = os.path.splitext(file)

        isUpated = False
        isUpated = obfuscate_File(file, 0, False)

        with open(file, 'r') as fStr:
            content = fStr.read()

        outFile = open(file,"w")

        for key, value in file_lines_dict.items():
            content = content.replace(key, value)

        outFile.write(content)
        file_lines_dict.clear()
        
        outFile.close()

        if isUpated:
            # add_header_in_file(obfuscatedFileName)
            LOGGER.i("Obfuscation done", 0 , okGreen)
            
            if extension == file_extention_list[0] or extension == file_extention_list[1]:
                file_with_extention = filename + file_extention_list[2]
                if not any(file_with_extention in added_files for added_files in add_header_later_in_file_list):
                    add_header_later_in_file_list.append(file)
                    
            else : 
                file_with_extention = filename + file_extention_list[0]
                if any(file_with_extention in added_files for added_files in add_header_later_in_file_list):
                    add_header_later_in_file_list.remove(file_with_extention)

                file_with_extention = filename + file_extention_list[1]
                if any(file_with_extention in added_files for added_files in add_header_later_in_file_list):
                    add_header_later_in_file_list.remove(file_with_extention)

                add_header_later_in_file_list.append(file)
        else:
            LOGGER.i("No changes added", 0 , WARNING)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--dir', type=str, default="", help="working files directory")
    arg_parser.add_argument('-id', '--ignoreDir', type=str, default="", help="working files directory")
    args = arg_parser.parse_args()
    dir_string = args.dir
    dir_list = dir_string.split(',')

    ignore_dir_string = args.ignoreDir
    ignore_dir_list_actual = []
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    if ignore_dir_string != "":
        ignore_dir_list = ignore_dir_string.split(',')
        for dir_to_scan in ignore_dir_list:
            ignore_dir_list_actual.append(join_path(script_dir, dir_to_scan))
            pass
    
    # r=root, d=directories, f = files
    for dir_to_scan in dir_list:
        output_root_dir = join_path(script_dir, dir_to_scan)
        LOGGER.i("Scaning Dir: %s" % dir_to_scan, 0 , BOLD)
        for r, d, f in os.walk(output_root_dir):
            if not ignore_dir_list_actual or not any(r.find(ignore_dir) != -1 for ignore_dir in ignore_dir_list_actual):
                for file in f:
                    if file.endswith('.DS_Store'):
                        path = join_path(r, file)
                        os.remove(path)
                        continue
                    extension = os.path.splitext(file)[1]
                    if any(extension == file_extention for file_extention in file_extention_list):
                        fileNames_list.append(os.path.join(r, file))

    if fileNames_list:
        # obfuscate_strings_in_File()
        # add_header_later_in_file()
        checkAndReportNotObfuscatedStrings()
