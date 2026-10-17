from functions.run_python_file import run_python_file

#Print calc usage instructions
print(run_python_file("calculator", "main.py"))

#Runs calc
print(run_python_file("calculator", "main.py", ["3 + 5"]))

#runs test success
print(run_python_file("calculator", "tests.py"))

#Error
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))
print(run_python_file("calculator", "lorem.txt"))
