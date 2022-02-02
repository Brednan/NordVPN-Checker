from cx_Freeze import executable, setup, Executable

setup(
    name='NordVPN Account Checker',
    version='1.0',
    description='Check a list of acount credentials and see which ones work on NordVPN',
    executables=[Executable('GUI.py', base='Win32GUI')]
)