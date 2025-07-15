#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpchar import htpchar

def htp_admin_check_passwd_webbl(id_str:string, grp_no:int):
    passwd_ok = False
    fchar:string = ""
    pswd_str:string = ""
    nanci:string = ""
    s:string = ""
    i:int = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal passwd_ok, fchar, pswd_str, nanci, s, i
        nonlocal id_str, grp_no

        return {"passwd_ok": passwd_ok}

    def aufbau(i:int, ch:string):

        nonlocal passwd_ok, fchar, pswd_str, nanci, s, id_str, grp_no

        def generate_inner_output():
            return (ch)


        if substring(proversion(), 0, 1) == ("1").lower() :

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

        return generate_inner_output()

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