#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Zwkum

def main_fs_readequipment_webbl():

    prepare_cache ([Htparam, Zwkum])

    text_p2_list_list = []
    lvcval:string = ""
    lvi:int = 0
    lvicnt:int = 0
    dept:int = 0
    cdelimiter:string = ";"
    htparam = zwkum = None

    text_p2_list = None

    text_p2_list_list, Text_p2_list = create_model("Text_p2_list", {"nr":int, "bezeich":string, "bg_col":int, "fg_col":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal text_p2_list_list, lvcval, lvi, lvicnt, dept, cdelimiter, htparam, zwkum


        nonlocal text_p2_list
        nonlocal text_p2_list_list

        return {"text-p2-list": text_p2_list_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})
    dept = htparam.finteger

    if dept == 0:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 902)]})

    if htparam.fchar == "":

        return generate_output()

    if matches(htparam.fchar,r"*,*"):
        cdelimiter = ","
    lvicnt = num_entries(htparam.fchar, cdelimiter)
    for lvi in range(1,lvicnt + 1) :
        lvcval = ""


        lvcval = trim(entry(lvi - 1, htparam.fchar, cdelimiter))

        if lvcval != "":

            zwkum = get_cache (Zwkum, {"zknr": [(eq, to_int(lvcval))],"departement": [(eq, dept)]})

            if zwkum and (lvi <= 6):
                text_p2_list = Text_p2_list()
                text_p2_list_list.append(text_p2_list)

                text_p2_list.nr = lvi
                text_p2_list.bezeich = zwkum.bezeich
                text_p2_list.bg_col = 9
                text_p2_list.fg_col = 15

    return generate_output()