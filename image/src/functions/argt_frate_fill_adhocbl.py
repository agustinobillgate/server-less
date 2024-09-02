from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Reslin_queasy, Argt_line, Artikel

def argt_frate_fill_adhocbl(pvilanguage:int, adhoc_code:str, argtnr:int, resnr:int, reslinnr:int, from_date:date, to_date:date, adhoc:[Adhoc]):
    argt_list_list = []
    post_type:str = ""
    pers_type:str = ""
    lvcarea:str = "argt_frate"
    reslin_queasy = argt_line = artikel = None

    adhoc = argt_list = None

    adhoc_list, Adhoc = create_model("Adhoc", {"acode":str, "artnr":int, "deptnr":int, "bezeich":str, "amount":decimal, "child1":decimal, "child2":decimal, "post_type":int})
    argt_list_list, Argt_list = create_model("Argt_list", {"argt_artnr":int, "bezeich":str, "departement":int, "deci1":decimal, "date1":date, "date2":date, "deci2":decimal, "deci3":decimal, "post_type":str, "pers_type":str, "fakt_modus":int, "s_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal argt_list_list, post_type, pers_type, lvcarea, reslin_queasy, argt_line, artikel


        nonlocal adhoc, argt_list
        nonlocal adhoc_list, argt_list_list
        return {"argt-list": argt_list_list}

    def create_adhoc_argt():

        nonlocal argt_list_list, post_type, pers_type, lvcarea, reslin_queasy, argt_line, artikel


        nonlocal adhoc, argt_list
        nonlocal adhoc_list, argt_list_list

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.number2 == argtnr) &  (Reslin_queasy.reslinnr == reslinnr)).first()
        while None != reslin_queasy:

            reslin_queasy = db_session.query(Reslin_queasy).first()
            db_session.delete(reslin_queasy)


            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.number2 == argtnr) &  (Reslin_queasy.reslinnr == reslinnr)).first()

        for adhoc in query(adhoc_list, filters=(lambda adhoc :adhoc.acode.lower()  == (adhoc_code).lower())):
            fill_adhoc_argt()

    def fill_adhoc_argt():

        nonlocal argt_list_list, post_type, pers_type, lvcarea, reslin_queasy, argt_line, artikel


        nonlocal adhoc, argt_list
        nonlocal adhoc_list, argt_list_list


        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "fargt_line"
        reslin_queasy.number1 = adhoc.deptnr
        reslin_queasy.number2 = argtnr
        reslin_queasy.number3 = adhoc.artnr
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.deci1 = adhoc.amount
        reslin_queasy.date1 = from_date
        reslin_queasy.date2 = to_date
        reslin_queasy.deci2 = adhoc.child1
        reslin_queasy.deci3 = adhoc.child2

    def create_argt_list():

        nonlocal argt_list_list, post_type, pers_type, lvcarea, reslin_queasy, argt_line, artikel


        nonlocal adhoc, argt_list
        nonlocal adhoc_list, argt_list_list

        reslin_queasy_obj_list = []
        for reslin_queasy, argt_line, artikel in db_session.query(Reslin_queasy, Argt_line, Artikel).join(Argt_line,(Argt_line.argtnr == Reslin_queasy.number2) &  (Argt_line.argt_artnr == Reslin_queasy.number3) &  (Argt_line.departement == Reslin_queasy.number1)).join(Artikel,(Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).filter(
                (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.number2 == argtnr) &  (Reslin_queasy.reslinnr == reslinnr)).all():
            if reslin_queasy._recid in reslin_queasy_obj_list:
                continue
            else:
                reslin_queasy_obj_list.append(reslin_queasy._recid)


            argt_list = Argt_list()
            argt_list_list.append(argt_list)

            argt_list.argt_artnr = argt_line.argt_artnr
            argt_list.bezeich = artikel.bezeich
            argt_list.departement = artikel.departement
            argt_list.deci1 = reslin_queasy.deci1
            argt_list.deci2 = reslin_queasy.deci2
            argt_list.deci3 = reslin_queasy.deci3
            argt_list.date1 = reslin_queasy.date1
            argt_list.date2 = reslin_queasy.date2
            argt_list.fakt_modus = argt_line.fakt_modus
            argt_list.s_recid = to_int(reslin_queasy._recid)
            argt_list.post_type = post_type[argt_line.fakt_modus - 1]
            argt_list.pers_type = pers_type[to_int(argt_line.vt_percnt) + 1 - 1]

    post_type[0] = translateExtended ("Daily", lvcarea, "")
    post_type[1] = translateExtended ("CI Day", lvcarea, "")
    post_type[2] = translateExtended ("2nd Day", lvcarea, "")
    post_type[3] = translateExtended ("Mon 1st Day", lvcarea, "")
    post_type[4] = translateExtended ("Mon LastDay", lvcarea, "")
    post_type[5] = translateExtended ("Special", lvcarea, "")


    pers_type[0] = translateExtended ("Adult", lvcarea, "")
    pers_type[1] = translateExtended ("Child", lvcarea, "")
    pers_type[2] = translateExtended ("Ch2", lvcarea, "")


    create_adhoc_argt()
    create_argt_list()

    return generate_output()