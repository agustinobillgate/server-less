from functions.additional_functions import *
import decimal
from functions.htpchar import htpchar

def htp_admin_check_passwd_webbl(id_str:str, grp_no:int):
    passwd_ok = False
    fchar:str = ""
    pswd_str:str = ""
    nanci:str = ""
    s:str = ""
    i:int = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal passwd_ok, fchar, pswd_str, nanci, s, i


        return {"passwd_ok": passwd_ok}

    def aufbau(i:int, ch:str):

        nonlocal passwd_ok, fchar, pswd_str, nanci, s, i

        if substring(PROVERSION, 0, 1) == "1":

            if i == 1:
                ch = ch + "g"

            elif i == 2 or i == 4:
                ch = ch + "e"

            elif i == 3:
                ch = ch + "h"

            elif i == 5 or i == 8:
                ch = ch + "i"

            elif i == 6 or i == 7:
                ch = ch + "n"

            elif i == 9:
                ch = ch + "s"
        else:

            if i == 1:
                ch = ch + "g"

            elif i == 2 or i == 4:
                ch = ch + "e"

            elif i == 3:
                ch = ch + "h"

            elif i == 5 or i == 8:
                ch = ch + "i"

            elif i == 6 or i == 7:
                ch = ch + "m"

            elif i == 9:
                ch = ch + "s"


    if grp_no == 10:
        fchar = get_output(htpchar(1071))

        if trim(fchar) == "":
            passwd_ok = True

            return generate_output()
        pswd_str = fchar

    if grp_no == 10:
        nanci = pswd_str

    elif grp_no == 99:
        for i in range(1,9 + 1) :
            nanci = aufbau(i, nanci)
        s = s + substring(to_string(get_month(get_current_date()) , "99") , 1, 1) + substring(to_string(get_month(get_current_date()) , "99") , 0, 1) + substring(to_string(get_day(get_current_date()) , "99") , 1, 1) + substring(to_string(get_day(get_current_date()) , "99") , 0, 1)
        nanci = nanci + s

    if nanci.lower()  == (id_str).lower() :
        passwd_ok = True

    return generate_output()