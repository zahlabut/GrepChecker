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
        print bcolors.OKGREEN + string + bcolors.ENDC
    elif color_or_format == 'red':
        print bcolors.FAIL + string + bcolors.ENDC
    elif color_or_format == 'yellow':
        print bcolors.WARNING + string + bcolors.ENDC
    elif color_or_format == 'blue':
        print bcolors.OKBLUE + string + bcolors.ENDC
    elif color_or_format == 'bold':
        print bcolors.BOLD + string + bcolors.ENDC
    else:
        print string

def exec_command_line_command(command):
    try:
        command_as_list = command.split(' ')
        command_as_list = [item.replace(' ', '') for item in command_as_list if item != '']
        result = subprocess.check_output(command, shell=True)
        return {'ReturnCode': 0, 'CommandOutput': result}
    except subprocess.CalledProcessError as e:
        print_in_color(str(e),'red')
        return {'ReturnCode': e.returncode, 'CommandOutput': str(e)}

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
    print ''
    try:
        if (len(list_object)==0):
            print "Nothing to choose :( "
            print "Execution will stop!"
            time.sleep(5)
            exit("Connot continue execution!!!")
            sys.exit(1)
        print msg
        counter=1
        for item in list_object:
            print str(counter)+') - '+item
            counter=counter+1
        choosed_option=raw_input("Choose option by entering the suitable number! ")
        while (int(choosed_option)<0 or int(choosed_option)> len(list_object)):
            print "No such option - ", choosed_option
            choosed_option=raw_input("Choose option by entering the suitable number! ")
        print_in_color("Option is: '"+list_object[int(choosed_option)-1]+"'"+'\n','bold')
        return [True,list_object[int(choosed_option)-1]]
    except Exception, e:
        print '*** No such option!!!***', e
        return[False, str(e)]

def exit(string):
    print_in_color(string,'red')
    sys.exit(1)

def print_dic(dic):
    for k in dic.keys():
        print '~'*80
        print k,' --> ',dic[k]

def your_verdict():
    verdict=choose_option_from_list(['Fail', 'OK'], 'Enter your verdict?')[1]
    if verdict == 'Fail':
        verdict = raw_input('Explain why: ')
    return verdict

### Check if pep8 is installed ###
return_code=exec_command_line_command('pycodestyle -h')['ReturnCode']
if return_code!=0:
    print "You don't have python pycodestyle(pep8) module installed\nFollow https://pypi.org/project/pycodestyle/ to install it"
    exit('Cannot continue execution :(')

### Candidat script file to check ###
files=[fil for fil in os.listdir('.') if fil.endswith('.py') and fil!='Check_grep_Task.py']
test_script=choose_option_from_list(files, 'Choose file to test:')[1]

### Usage ###
test_name='Check usage'
spec_print([test_name])
com='python ' + test_script + ' -h'
print_in_color('--> ' + com, 'blue')
os.system(com)
time.sleep(1)
verdict_dic[test_name] = your_verdict()

### Single file - basic tests ###
for opt in options:
    test_name='Basic test - single file + '+opt+' option'
    spec_print([test_name])
    expected_output='File:'+test_file_1+'\n'+exec_command_line_command('grep -n -E '+regex+' '+test_file_1)['CommandOutput']
    print_in_color('Expected lines in output:\n'+expected_output,'green')
    print_in_color('\nActual output is:\n','bold')
    com='python ' + test_script + ' -f ' + test_file_1 + ' -r '+regex+' '+opt
    print_in_color('--> ' + com, 'blue')
    os.system(com)
    time.sleep(1)
    verdict_dic[test_name]=your_verdict()

### Two files - basic tests ###
for opt in options:
    test_name='Basic test - two files + '+opt+' option'
    spec_print([test_name])
    expected_output=exec_command_line_command('grep -n -E '+regex+' '+test_file_1+' '+test_file_2)['CommandOutput']
    print_in_color('Expected lines in output:\n'+expected_output,'green')
    com='python ' +test_script+' -f '+test_file_1+' '+test_file_2+' -r '+regex+' -c'
    print_in_color('--> ' + com, 'blue')
    os.system(com)
    time.sleep(1)
    verdict_dic[test_name]=your_verdict()


### All lines starts with given by regex character ###
for opt in options:
    test_name='All lines started with: ('+start_line_regex+') '+opt+' option'
    spec_print([test_name])
    expected_output='File:'+test_file_1+'\n'+exec_command_line_command('grep -n -E '+start_line_regex+' '+test_file_1)['CommandOutput']
    print_in_color('Expected lines in output:\n'+expected_output,'green')
    print_in_color('\nActual output is:\n','bold')
    com='python ' + test_script + ' -f ' + test_file_1 + ' -r '+regex+' '+opt
    print_in_color('--> ' + com, 'blue')
    os.system(com)
    time.sleep(1)
    verdict_dic[test_name]=your_verdict()


### PEP8 Validator ###
test_name='PEP8 - Validation'
spec_print([test_name])
os.system('pycodestyle '+test_script)
time.sleep(1)
verdict_dic[test_name]=your_verdict()

### Negative - no file option is provided ###
test_name='PEP8 - no file option is provided'
spec_print([test_name])
print_in_color('Expect: Standard input supposed to be used','yellow')
print_in_color('Note: available test files to use as input file/s are: "stam1" and "stam2"','yellow')
com='python ' +test_script+' -r '+regex+' -u'
print_in_color('--> '+com,'blue')
os.system(com)
time.sleep(1)
verdict_dic[test_name]=your_verdict()

### Negative - not valid REGEX ###
test_name='Negative test case - no file option is provided'
spec_print([test_name])
com='python ' + test_script + ' -f ' + test_file_1 + ' -r '+not_valid_regex
print_in_color('--> '+com,'blue')
os.system(com)
time.sleep(1)
verdict_dic[test_name]=your_verdict()

### Negative - not existing file ###
test_name='Negative test case - not existing input file'
spec_print([test_name])
com='python '+test_script+' -f ZABABUN -r '+regex+' -u'
print_in_color('--> '+com,'blue')
time.sleep(1)
os.system(com)
verdict_dic[test_name]=your_verdict()


print_dic(verdict_dic)
score=len([key for key in verdict_dic.keys() if verdict_dic[key]=='OK'])*100/len(verdict_dic)
spec_print(['The final grade is:',str(score)])




