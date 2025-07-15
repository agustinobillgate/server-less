#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.htpdate import htpdate
from models import Bediener

def gl_linkar_checkbl(pvilanguage:int, user_init:string, array_nr:int, expected_nr:int):

    prepare_cache ([Bediener])

    flag_msg = 0
    msg_str = ""
    zugriff:bool = True
    flogical:bool = False
    n:int = 0
    perm:List[int] = create_empty_list(120,0)
    s1:string = ""
    s2:string = ""
    fdate:date = None
    lvcarea:string = "gl-linkar-check"
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_msg, msg_str, zugriff, flogical, n, perm, s1, s2, fdate, lvcarea, bediener
        nonlocal pvilanguage, user_init, array_nr, expected_nr

        return {"flag_msg": flag_msg, "msg_str": msg_str}

    flogical = get_output(htplogic(2000))

    if flogical == False:
        msg_str = translateExtended ("No License for this module.", lvcarea, "") + chr_unicode(13) + chr_unicode(10) +\
                translateExtended ("Please contact our local Technical Support for further information.", lvcarea, "")
        flag_msg = 1

        return generate_output()
    else:

        if user_init == " ":
            msg_str = translateExtended ("User not defined.", lvcarea, "")
            flag_msg = 1
            zugriff = False

            return generate_output()
        else:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                for n in range(1,length(bediener.permissions)  + 1) :
                    perm[n - 1] = to_int(substring(bediener.permissions, n - 1, 1))

                if perm[array_nr - 1] < expected_nr:
                    zugriff = False
                    s1 = to_string(array_nr, "999")
                    s2 = to_string(expected_nr)
                    msg_str = translateExtended ("Sorry, No Access Right.", lvcarea, "") + chr_unicode(13) + chr_unicode(10) +\
                            translateExtended ("Access Code =", lvcarea, "") + " " + s1 + s2
                    flag_msg = 1

                    return generate_output()

        if zugriff:
            fdate = get_output(htpdate(1014))

            if fdate == None:
                msg_str = translateExtended ("Last transfer date in (parameter 1014) not yet defined.", lvcarea, "")
                flag_msg = 1

                return generate_output()
            else:
                msg_str = translateExtended ("Do you really want to transfer A/R Payments to GL Journals?", lvcarea, "")
                flag_msg = 2

                return generate_output()

    return generate_output()