@echo off
REM Check if version parameter is provided
if "%1"=="" (
    echo Usage: ./compile.bat [version]
    exit /b 1
)
echo on
REM Build the Docker image
docker build -t vhplite_arys:v%1 .

REM Tag the Docker image
docker tag vhplite_arys:v%1 995253731843.dkr.ecr.ap-southeast-1.amazonaws.com/vhplite_arys:v%1

REM Push the Docker image to ECR
docker push 995253731843.dkr.ecr.ap-southeast-1.amazonaws.com/vhplite_arys:v%1

aws lambda update-function-code --function-name docker_vhplite_arys --image-uri 995253731843.dkr.ecr.ap-southeast-1.amazonaws.com/vhplite_arys:v%1>./null 

del null