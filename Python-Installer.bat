@echo off
echo Telechargement de Python...
curl -o python_installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe

echo Installation de Python...
python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
del python_installer.exe

echo Python a ete installe avec succes.

echo Lancez install_package.bat pour telecharger le package
pause