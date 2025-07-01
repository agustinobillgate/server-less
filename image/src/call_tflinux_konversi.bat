@echo off
echo ------------------------------------------------
echo program memanggil program konversi Pak Tofer
echo dengan environment /lenv/ 
echo prosedur ini harus jalan di environment linux/mac, 
echo issue / atau \
echo ------------------------------------------------

wsl bash -c "source /mnt/d/docker_linux/app_konversi/lenv/bin/activate && python /mnt/d/docker_linux/app_konversi/input/vhp-serverless/image/src/tflinux_p_py_converter.py"

robocopy "D:\docker\app_konversi\input\vhp-serverless\image\src\output\converted2" "D:\docker\pixcdk\image\src\functions"  /NFL /NDL /NJH /NJS


