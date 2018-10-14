from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import os
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
    output_command = " ".join([EXEC_PATH])
    code_output = subprocess.check_output(output_command,shell=True).decode("utf-8")
    context = {"output": code_output}
    return render (request,"online_compiler/evaluate.html",context)