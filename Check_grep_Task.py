import time
import subprocess
import re
import sys
import os
import time
verdict_dic={}

test_file_1='stam1'
test_file_2='stam2'
regex='aaa'
start_line_regex="'^a'"
not_valid_regex="'(*&^*&^####'"
options=['-c','-u','-m']

# Usage - copy file to test into this tool directory #

def empty_file_content(log_file_name):
    f = open(log_file_name, 'w')
    f.write('')
    f.close()

def print_in_color(string, color_or_format=None):
    string = str(string)

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    if color_or_format == 'green':
        print(bcolors.OKGREEN + string + bcolors.ENDC)
    elif color_or_format == 'red':
        print(bcolors.FAIL + string + bcolors.ENDC)
    elif color_or_format == 'yellow':
        print(bcolors.WARNING + string + bcolors.ENDC)
    elif color_or_format == 'blue':
        print(bcolors.OKBLUE + string + bcolors.ENDC)
    elif color_or_format == 'bold':
        print(bcolors.BOLD + string + bcolors.ENDC)
    else:
        print(string)

def exec_command_line_command(command):
    try:
        command_as_list = command.split(' ')
        command_as_list = [item.replace(' ', '') for item in command_as_list if item != '']
        result = subprocess.check_output(command, shell=True, encoding='UTF-8', stderr=subprocess.STDOUT, stdin=True)
        json_output = None
        try:
            json_output = json.loads(result.lower())
        except:
            pass
        return {'ReturnCode': 0, 'CommandOutput': result, 'JsonOutput': json_output}
    except subprocess.CalledProcessError as e:
        if 'wget -r' not in command:
            print_in_color(command,'red')
            print_in_color(e.output, 'red')
        return {'ReturnCode': e.returncode, 'CommandOutput': e.output}



def spec_print(string_list,color=None):
    len_list=[]
    for item in string_list:
        len_list.append(len('### '+item.strip()+' ###'))
    max_len=max(len_list)
    print_in_color('',color)
    print_in_color("#"*max_len,color)
    for item in string_list:
        print_in_color("### "+item.strip()+" "*(max_len-len("### "+item.strip())-4)+" ###",color)
    print_in_color("#"*max_len+'\n',color)

def choose_option_from_list(list_object, msg):
    print('')
    try:
        if (len(list_object)==0):
            print("Nothing to choose :( ")
            print("Execution will stop!")
            time.sleep(5)
            exit("Connot continue execution!!!")
            sys.exit(1)
        print(msg)
        counter=1
        for item in list_object:
            print(str(counter)+') - '+item)
            counter=counter+1
        choosed_option=input("Choose option by entering the suitable number! ")
        while (int(choosed_option)<0 or int(choosed_option)> len(list_object)):
            print("No such option - ", choosed_option)
            choosed_option=input("Choose option by entering the suitable number! ")
        print_in_color("Option is: '"+list_object[int(choosed_option)-1]+"'"+'\n','bold')
        return [True,list_object[int(choosed_option)-1]]
    except Exception as e:
        print('*** No such option!!!***', e)
        return[False, str(e)]

def exit(string):
    print_in_color(string,'red')
    sys.exit(1)

def print_dic(dic):
    for k in dic.keys():
        print('~'*80)
        print(k,' --> ',dic[k])

def your_verdict():
    try:
        score = int(input('Enter your score (0-100):'))
    except Exception as e:
        print(e)
        score=your_verdict()
    if score<0 or score>100:
        score = your_verdict()
    return score

### Check if pep8 is installed ###
return_code=exec_command_line_command('pycodestyle -h')['ReturnCode']
if return_code!=0:
    print("You don't have python pycodestyle(pep8) module installed\nFollow https://pypi.org/project/pycodestyle/ to install it")
    exit('Cannot continue execution :(')

### Candidat script file to check ###
files=[fil for fil in os.listdir('.') if fil.endswith('.py') and fil!='Check_grep_Task.py']
test_script=choose_option_from_list(files, "Choose candidate's script file to test:")[1]

### Usage ###
test_name="--- Check script's usage ---"
spec_print([test_name])
com='python3 ' + test_script + ' -h'
print_in_color('--> ' + com, 'blue')
os.system(com)
time.sleep(0.3)
verdict_dic[test_name] = your_verdict()

### Single file - basic tests ###
for opt in options:
    test_name='--- Basic test - single file + '+opt+' option ---'
    spec_print([test_name])
    expected_output='File:'+test_file_1+'\n'+exec_command_line_command('grep -n -E '+regex+' '+test_file_1)['CommandOutput']
    print_in_color('Identical grep result:\n'+expected_output,'green')
    print_in_color('\nActual output is:\n','bold')
    com='python3 ' + test_script + ' -f ' + test_file_1 + ' -r '+regex+' '+opt
    print_in_color('--> ' + com, 'blue')
    os.system(com)
    time.sleep(0.3)
    verdict_dic[test_name]=your_verdict()

### Two files - basic tests ###
for opt in options:
    test_name='--- Basic test - two files + '+opt+' option ---'
    spec_print([test_name])
    expected_output=exec_command_line_command('grep -n -E '+regex+' '+test_file_1+' '+test_file_2)['CommandOutput']
    print_in_color('Identical grep result:\n'+expected_output,'green')
    com='python3 ' +test_script+' -f '+test_file_1+' '+test_file_2+' -r '+regex+' '+opt
    print_in_color('--> ' + com, 'blue')
    os.system(com)
    time.sleep(0.3)
    verdict_dic[test_name]=your_verdict()


### All lines starts with given by regex character ###
for opt in options:
    test_name='--- All lines started with: ('+start_line_regex+') '+opt+' option ---'
    spec_print([test_name])
    expected_output='File:'+test_file_1+'\n'+exec_command_line_command('grep -n -E '+start_line_regex+' '+test_file_1)['CommandOutput']
    print_in_color('Identical grep result:\n'+expected_output,'green')
    print_in_color('\nActual output is:\n','bold')
    com='python3 ' + test_script + ' -f ' + test_file_1 + ' -r '+start_line_regex+' '+opt
    print_in_color('--> ' + com, 'blue')
    os.system(com)
    time.sleep(0.3)
    verdict_dic[test_name]=your_verdict()


### PEP8 Validator ###
test_name='--- PEP8 - Validation ---'
spec_print([test_name])
os.system('pycodestyle '+test_script)
time.sleep(0.3)
verdict_dic[test_name]=your_verdict()

### Negative - no file option is provided ###
test_name="--- STDIN test - file option (-f --file) is not in use ---"
spec_print([test_name])
print_in_color('Expected: STDIN should to be used to get the file/s name','yellow')
print_in_color('Note: available test files to use as input file/s are: "stam1" and "stam2"','yellow')
com='python3 ' +test_script+' -r '+regex+' -u'
print_in_color('--> '+com,'blue')
os.system(com)
time.sleep(0.3)
verdict_dic[test_name]=your_verdict()

### Negative - not valid REGEX ###
test_name='--- Negative test case - no file option is provided ---'
spec_print([test_name])
com='python3 ' + test_script + ' -f ' + test_file_1 + ' -r '+not_valid_regex
print_in_color('--> '+com,'blue')
os.system(com)
time.sleep(0.3)
verdict_dic[test_name]=your_verdict()

### Negative - not existing file ###
test_name='--- Negative test case - not existing input file ---'
spec_print([test_name])
com='python3 '+test_script+' -f ZABABUN -r '+regex+' -u'
print_in_color('--> '+com,'blue')
time.sleep(0.3)
os.system(com)
verdict_dic[test_name]=your_verdict()




### Test if other modules are imported ###
test_name='--- Check if other Python files are imported inside the main one ---'
spec_print([test_name])
all_files=[fil for fil in os.listdir('.') if fil.endswith('.py')]
tool_files=[]
script_lines=open(test_script,'r').readlines()
for line in script_lines:
        for fil in all_files:
            if fil.split('.py')[0] in line:
                tool_files.append(fil)
if len(tool_files)>=1:
    print_in_color('OK - Import of: '+str(tool_files)+' modules detected','green')
else:
    print_in_color('Fail - single script based tool','red')
verdict_dic[test_name]=your_verdict()

### Test if OOP ###
test_name = '--- Check if code is OOP ---'
tool_files.append(test_script)
classes=[]
for fil in tool_files:
    for line in open(fil, 'r').readlines():
        if line.startswith('class')==True:
            classes.append(line.strip())
if len(classes)>0:
    print_in_color('OK - OOP detected, used classes are: ' + str(classes), 'green')
else:
    print_in_color('Fail - no OOP detected', 'red')
verdict_dic[test_name] = your_verdict()

### Result ###
print_in_color('\n\n\n--- Executed test cases ---','green')
print_dic(verdict_dic)
score=sum([int(verdict_dic[key]) for key in verdict_dic.keys()])/len(verdict_dic)
if score<60:
    print_in_color('The final grade is:'+str(score),'red')
else:
    print_in_color('The final grade is:' + str(score), 'green')
