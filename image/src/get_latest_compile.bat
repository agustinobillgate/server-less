@REM cd D:\docker\app_konversi\input\vhp-master-source
@REM git pull origin develop
@REM git fetch -p
@REM git checkout serverless

@echo off
set source_folder=D:\docker\tmpgit\vhp-master-source\Master
set destination_folder=D:\docker\app_konversi\input\vhp-lite-project-serverless\Master


:: Initialize the counter for missing files
set /a missing_file_count=0

:: Debug: Print source and destination folders
echo Source folder: %source_folder%
echo Destination folder: %destination_folder%

:: Loop through all files in the source folder (recursively)
for /f "delims=" %%A in ('dir "%source_folder%\*" /b /s /a-d') do (
    echo Processing file: %%A
    set source_file=%%A
    set source_filename=%%~nxA

    :: Check if the file exists in the destination
    if not exist "%destination_folder%\%%~nxA" (
        @REM echo File %%~nxA does not exist in destination. Counting...
        set /a missing_file_count+=1

        :: Uncomment the line below for copying files in the future
        :: xcopy "%%A" "%destination_folder%" /y
    ) else (
        @REM echo File %%~nxA already exists in destination.
    )
)

:: Print the total count of missing files
echo Total missing files: %missing_file_count%