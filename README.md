# OnPiler
OnPiler is a simple server based online compiler. Currently it supports only two languages (C and C++),
but it can be easily be extended to support many more. The time limit of running the source code is also 
taken as standard 5 second one. There is still no multithreading support to support multiple server requests 
at a time simultaneously.I am still currently working on it. There are still many modifications that can be done on it. 
I have listed a few of them below. Feel free to contribute anytime you like.

<b>Modifications that can be done : </b>
1. Modifying timelimit based on user input/request.
2. Multithreading support to support multiple requests at one time.
3. Using JavaScript and Ajax to run the source code and display output . dynamically rathar than Post requesting through form 
   each time.
4. Multi Language support. 

Feel free to modify these changes :)

<b> Requirements for OnPiler: </b>
     Read "Requirements.txt" and install all modules mentioned in it.

<b> Installation/Running Guide for OnPiler Project: </b>
1. Copy OnPiler Project directory in your working directory.
2. Open terminal and navigate to your project directory in terminal.
3. In terminal, run command "python manage.py runserver" .
4. Open "http://127.0.0.1:8000" in your browser to run OnPiler.

