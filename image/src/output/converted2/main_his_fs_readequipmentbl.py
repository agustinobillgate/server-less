#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Zwkum

def main_his_fs_readequipmentbl():

    prepare_cache ([Htparam, Zwkum])

    text_p2 = ["", "", "", "", "", ""]
    htparam = zwkum = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal text_p2, htparam, zwkum

        return {"text_p2": text_p2}

    def readequipment():

        nonlocal text_p2, htparam, zwkum

        lvcval:string = ""
        lvi:int = 0
        lvicnt:int = 0
        dept:int = 0
        cdelimiter:string = ";"

        htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})
        dept = htparam.finteger

        if dept == 0:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 902)]})

        if htparam.fchar == "":

            return

        if matches(htparam.fchar,r"*,*"):
            cdelimiter = ","
        lvicnt = num_entries(htparam.fchar, cdelimiter)
        for lvi in range(1,lvicnt + 1) :
            lvcval = ""


            lvcval = trim(entry(lvi - 1, htparam.fchar, cdelimiter))

            if lvcval != "":

                zwkum = get_cache (Zwkum, {"departement": [(eq, dept)],"zknr": [(eq, to_int(lvcval))]})

                if zwkum and (lvi <= 6):

                    if lvi == 1:
                        text_p2[0] = zwkum.bezeich

                    elif lvi == 2:
                        text_p2[1] = zwkum.bezeich

                    elif lvi == 3:
                        text_p2[2] = zwkum.bezeich

                    elif lvi == 4:
                        text_p2[3] = zwkum.bezeich

                    elif lvi == 5:
                        text_p2[4] = zwkum.bezeich

                    elif lvi == 6:
                        text_p2[5] = zwkum.bezeich