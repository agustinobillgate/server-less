@echo off
REM Check if version parameter is provided
if "%1"=="" (
    echo Usage: ./compile.bat [version]
    exit /b 1
)

REM Build the Docker image
docker build -t fastapi_ec2:d%1 .
docker save -o fastapi_ec2.tar fastapi_ec2:d%1
