@echo off
REM Check if version parameter is provided
if "%1"=="" (
    echo Usage: ./compile.bat [version]
    exit /b 1
)

REM Build the Docker image
docker build -t fastapi-lambda-image:v%1 .

REM Tag the Docker image
docker tag fastapi-lambda-image:v%1 618733377538.dkr.ecr.ap-southeast-1.amazonaws.com/fastapi-vhp:v%1

REM Push the Docker image to ECR
docker push 618733377538.dkr.ecr.ap-southeast-1.amazonaws.com/fastapi-vhp:v%1

aws lambda update-function-code --function-name docker-demo-lambda-image --image-uri 618733377538.dkr.ecr.ap-southeast-1.amazonaws.com/fastapi-vhp:v%1 >./null 

del null