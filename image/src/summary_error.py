import re

error_list = []
erFile = "D:/docker/app_konversi/output/log/run_1_Housekeeping_Main-Overview_241015_2250_Total_33_err_29.txt"
f = open(erFile, "r")

file_content = f.read()

for scenario in file_content.split("Scenario"):
    matches = (re.findall(r"Error Message:",scenario,re.IGNORECASE))
    
    if matches:
        # print(matches)
        error_str = "\n".join(scenario.split("\n")[1:]).split("--------------------------------------------------------------")[0]
        if not error_str in error_list:
            error_list.append(error_str)

all_error = "\n".join(error_list)

print(all_error)