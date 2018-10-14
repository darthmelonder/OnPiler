from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import os
import time
import subprocess
# Create your views here.
def index (request):
    context={}
    return render (request,"online_compiler/index.html",context)

def evaluate (request):
    lang = request.POST.get('language')
    cmd="gcc"
    extension=".c"
    if (lang=="C++"):
        cmd = "g++"
        extension=".cpp"

    '''
        language C and C++ -> shell commands: gcc and g++;
        language C and C++ -> extensions: .c and .cpp;
    '''

    code_area = request.POST.get('code_area')
    CODE_DIR = os.path.join(settings.BASE_DIR,"UserCodes")
    FILE_PATH = os.path.join(CODE_DIR,"usercode"+extension)
    EXEC_PATH = os.path.join(CODE_DIR,"usercode")
    with open(FILE_PATH,'w') as f:
        f.write(code_area)
    f.close()

    '''
        took code from code_area and wrote it into file present at FILE_PATH above 
    '''

    input_area = request.POST.get('input')
    IN_FILE_PATH = os.path.join(CODE_DIR,"usercode.txt")
    with open (IN_FILE_PATH,'w') as f:
        f.write(input_area)
    f.close()

    '''
        took code from input_area and wrote it into file present ar IN_FILE_PATH
    '''

    shell_command = " ".join([cmd,"-o",EXEC_PATH, FILE_PATH])
    try:
        compile_status = subprocess.check_output(shell_command,shell=True,stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as e:
        '''
            any error in compilation will lead to here
        '''
        error_stack = e.output.decode("utf-8")
        error_stack = error_stack.replace(FILE_PATH,"\n")
        context = {"error": error_stack}
        return render(request,"online_compiler/evaluate.html",context)
    '''
        compilation is successful now. 
        Need to run the exectuable now
    '''
    output_command = " ".join([EXEC_PATH,"<",IN_FILE_PATH])
    code_pipe = subprocess.Popen(output_command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    '''
        check for a standard 5 second time limit while running executable
    '''

    try:
        start = time.time()
        code_output = code_pipe.communicate(timeout=5)
        elapsed = time.time()
        code_output=code_output[0].decode("utf-8")
    except Exception as e:
        '''
            time limit has been exceeded
        '''
        context = {"error": "Time Limit Exceeeded (5 seconds)"}
        return render(request,"online_compiler/evaluate.html",context)

    if (code_pipe.returncode or code_pipe.returncode!=0):
        '''
            Handling other runtime errors
        '''
        try:
            output = subprocess.check_output(output_command,shell=True,stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            error_stack = "Runtime Error: \n" + str(e)
            error_stack = error_stack.replace(EXEC_PATH,"\n")
            context = {"error": error_stack}
            return render(request,"online_compiler/evaluate.html",context)

    context = {"output": code_output,"time": str(elapsed-start)}
    return render (request,"online_compiler/evaluate.html",context)