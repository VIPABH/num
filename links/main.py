# main.py
from code.module1 import some_function
from code.module2 import function2
from links import ABH  # استيراد ABH من links/__init__.py

def main():
    print("This is the main program!")
    some_function()
    function2()

if __name__ == "__main__":
    main()
