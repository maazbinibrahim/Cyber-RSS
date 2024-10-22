@echo off

::Checks if python is installed
:check
python --version 3>NUL
if errorlevel 1 goto errorNoPython

::If python is installed then it runs the program
start <python progam>
exit

::Installes python
:errorNoPython
python
timeout /t 60
goto check