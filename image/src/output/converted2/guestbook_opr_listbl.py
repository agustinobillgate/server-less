#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guestbook

t_data_list, T_data = create_model("T_data", {"gastnr":int, "infostr":string, "orig_infostr":string})

def guestbook_opr_listbl(instr:string, base64file:string, t_data_list:[T_data]):
    outstr = ""
    mess_result = ""
    tcase:int = 0
    tgastnr:int = 0
    pointer:bytes = None
    guestbook = None

    t_data = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outstr, mess_result, tcase, tgastnr, pointer, guestbook
        nonlocal instr, base64file


        nonlocal t_data

        return {"base64file": base64file, "t-data": t_data_list, "outstr": outstr, "mess_result": mess_result}


    tcase = to_int(entry(0, instr, ";"))

    if num_entries(instr, ";") > 1:
        tgastnr = to_int(entry(1, instr, ";"))

    if tcase == 1:

        t_data = query(t_data_list, first=True)

        if t_data:
            guestbook = Guestbook()
            db_session.add(guestbook)

            guestbook.gastnr = t_data.gastnr
            guestbook.infostr = t_data.infostr
            guestbook.orig_infostr = t_data.orig_infostr


            pointer = base64_decode(base64file)
            guestbook.imagefile = pointer
            base64file = ""
            mess_result = "1 - Successfully Created"
        t_data_list.clear()
    elif tcase == 2:

        t_data = query(t_data_list, first=True)

        if t_data:

            guestbook = get_cache (Guestbook, {"gastnr": [(eq, t_data.gastnr)]})

            if guestbook:
                guestbook.infostr = t_data.infostr
                guestbook.orig_infostr = t_data.orig_infostr

                if base64file != "":
                    pointer = base64_decode(base64file)
                    guestbook.imagefile = pointer
                mess_result = "21 - Successfully Updated"
            else:
                guestbook = Guestbook()
                db_session.add(guestbook)

                guestbook.gastnr = t_data.gastnr
                guestbook.infostr = t_data.infostr
                guestbook.orig_infostr = t_data.orig_infostr


                pointer = base64_decode(base64file)
                guestbook.imagefile = pointer
                mess_result = "22 - Successfully Created"
            base64file = ""
        t_data_list.clear()
    elif tcase == 3:
        t_data_list.clear()

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, tgastnr)]})

        if guestbook:
            t_data = T_data()
            t_data_list.append(t_data)

            t_data.gastnr = guestbook.gastnr
            t_data.infostr = guestbook.infostr
            t_data.orig_infostr = guestbook.orig_infostr


            pointer = guestbook.imagefile
            base64file = base64_encode(pointer)
            mess_result = "3 - Successfully Loaded"
        else:
            t_data_list.clear()
    elif tcase == 4:

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, tgastnr)]})

        if guestbook:
            db_session.delete(guestbook)
            mess_result = "4 - Successfully Deleted"
        t_data_list.clear()
    elif tcase == 5:

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, tgastnr)]})

        if guestbook:
            outstr = guestbook.orig_infostr
            mess_result = "5 - Successfully Generated MD5"
        t_data_list.clear()

    return generate_output()