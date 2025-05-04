@echo off
chcp 65001
setlocal enabledelayedexpansion

:: 检查是否有参数传入
if "%~1"=="" (
    echo No file path provided.
    pause
    exit /b
)

:: 获取完整的文件路径
set "file_path=%~1"

:: 调用 Python 脚本并传递完整的文件路径
start /b "" "C:\Users\maggie\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe" "D:\Zhangzy\临时\高中\杂项内容\研究性学习\python文件\main.py" "!file_path!"
