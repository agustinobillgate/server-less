#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Htparam, Zimkateg

def if_bookeng_update_aribl(rcode:string, curr_task:string):

    prepare_cache ([Queasy, Zimkateg])

    cat_flag:bool = False
    zikat_nr:int = 0
    rcode1:string = ""
    rm_typ:string = ""
    queasy = htparam = zimkateg = None

    qsy = None

    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cat_flag, zikat_nr, rcode1, rm_typ, queasy, htparam, zimkateg
        nonlocal rcode, curr_task
        nonlocal qsy


        nonlocal qsy

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if curr_task.lower()  == ("avail").lower() :

        if rcode != "":

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.char1 == (rcode).lower())).first()
            while None != queasy:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi1 = False
                    qsy.logi3 = False


                    pass
                    pass

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 171) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.char1 == (rcode).lower()) & (Queasy._recid > curr_recid)).first()

        elif rcode == "":

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & ((Queasy.logi1) | (Queasy.logi3))).first()
            while None != queasy:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi1 = False
                    qsy.logi3 = False


                    pass
                    pass

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 171) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy._recid > curr_recid)).first()

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 175) & ((Queasy.logi1) | (Queasy.logi3))).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = False
                qsy.logi3 = False
                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 175) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy._recid > curr_recid)).first()

    elif curr_task.lower()  == ("availAll").lower() :

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 171) & ((Queasy.logi1) | (Queasy.logi3))).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = False
                qsy.logi3 = False


                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy._recid > curr_recid)).first()

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 175) & ((Queasy.logi1) | (Queasy.logi3))).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = False
                qsy.logi3 = False
                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 175) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy._recid > curr_recid)).first()

    elif curr_task.lower()  == ("availbyrmtype").lower() :

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        if cat_flag:

            queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, rcode)]})

            if queasy:
                zikat_nr = queasy.number1
        else:

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rcode)]})

            if zimkateg:
                zikat_nr = zimkateg.zikatnr

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 171) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.number1 == zikat_nr)).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = False
                qsy.logi3 = False


                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.number1 == zikat_nr) & (Queasy._recid > curr_recid)).first()

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 175) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.number1 == zikat_nr)).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = False
                qsy.logi3 = False
                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 175) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.number1 == zikat_nr) & (Queasy._recid > curr_recid)).first()

    elif curr_task.lower()  == ("rate").lower() :

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 170) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.char1 == (rcode).lower())).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = False
                qsy.logi3 = False


                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 170) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.char1 == (rcode).lower()) & (Queasy._recid > curr_recid)).first()

    elif curr_task.lower()  == ("rateAll").lower() :

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 170) & ((Queasy.logi1) | (Queasy.logi3))).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = False
                qsy.logi3 = False
                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 170) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy._recid > curr_recid)).first()

    elif curr_task.lower()  == ("ratebyrmtype").lower() :
        rcode1 = entry(0, rcode, ";")
        rm_typ = entry(1, rcode, ";")

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        if cat_flag:

            queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, rm_typ)]})

            if queasy:
                zikat_nr = queasy.number1
        else:

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rm_typ)]})

            if zimkateg:
                zikat_nr = zimkateg.zikatnr

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 170) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.char1 == (rcode1).lower()) & (Queasy.number1 == zikat_nr)).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = False
                qsy.logi3 = False


                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 170) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy.char1 == (rcode1).lower()) & (Queasy.number1 == zikat_nr) & (Queasy._recid > curr_recid)).first()

    elif curr_task.lower()  == ("restriction").lower() :

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 175) & ((Queasy.logi1) | (Queasy.logi3))).first()
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi1 = False
                qsy.logi3 = False
                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 175) & ((Queasy.logi1) | (Queasy.logi3)) & (Queasy._recid > curr_recid)).first()

    elif curr_task.lower()  == ("push-all-restriction").lower() :

        queasy = get_cache (Queasy, {"key": [(eq, 175)]})
        while None != queasy:

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi3 = True
                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 175) & (Queasy._recid > curr_recid)).first()

    return generate_output()