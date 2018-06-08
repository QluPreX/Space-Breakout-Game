import sys,os
from cx_Freeze import setup, Executable
os.environ['TCL_LIBRARY'] = r'C:\Users\karel\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\karel\AppData\Local\Programs\Python\Python36\tcl\tk8.6'
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","pygame","sys","random"],"include_files" : ["Assets/ball_normal_big.png","Assets/ball.png","Assets/bat_lang.png","Assets/bg.png","Assets/bg1.jpg","Assets/brick_blue_special.png","Assets/brick.png","Assets/upgrade1.png"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
setup(  name = "guifoo",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("bricks.py")])