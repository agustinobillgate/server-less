#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 25-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Argt_line, Artikel

adhoc_data, Adhoc = create_model("Adhoc", {"acode":string, "artnr":int, "deptnr":int, "bezeich":string, "amount":Decimal, "child1":Decimal, "child2":Decimal, "post_type":int})

def argt_frate_fill_adhocbl(pvilanguage:int, adhoc_code:string, argtnr:int, resnr:int, reslinnr:int, from_date:date, to_date:date, adhoc_data:[Adhoc]):

    prepare_cache ([Argt_line, Artikel])

    argt_list_data = []
    post_type:List[string] = create_empty_list(6,"")
    pers_type:List[string] = create_empty_list(3,"")
    lvcarea:string = "argt-frate"
    reslin_queasy = argt_line = artikel = None

    adhoc = argt_list = None

    argt_list_data, Argt_list = create_model("Argt_list", {"argt_artnr":int, "bezeich":string, "departement":int, "deci1":Decimal, "date1":date, "date2":date, "deci2":Decimal, "deci3":Decimal, "post_type":string, "pers_type":string, "fakt_modus":int, "s_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal argt_list_data, post_type, pers_type, lvcarea, reslin_queasy, argt_line, artikel
        nonlocal pvilanguage, adhoc_code, argtnr, resnr, reslinnr, from_date, to_date


        nonlocal adhoc, argt_list
        nonlocal argt_list_data

        return {"argt-list": argt_list_data}

    def create_adhoc_argt():

        nonlocal argt_list_data, post_type, pers_type, lvcarea, reslin_queasy, argt_line, artikel
        nonlocal pvilanguage, adhoc_code, argtnr, resnr, reslinnr, from_date, to_date


        nonlocal adhoc, argt_list
        nonlocal argt_list_data

        # reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"resnr": [(eq, resnr)],"number2": [(eq, argtnr)],"reslinnr": [(eq, reslinnr)]})
        reslin_queasy = db_session.query(Reslin_queasy).filter((Reslin_queasy.key == "fargt-line") & (Reslin_queasy.char1== "") & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.number2 == argtnr) & (Reslin_queasy.reslinnr == reslinnr)).with_for_update().first()

        while None != reslin_queasy:
            pass
            db_session.delete(reslin_queasy)
            db_session.refresh(reslin_queasy, with_for_update=True)
            # pass

            curr_recid = reslin_queasy._recid
            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.number2 == argtnr) & (Reslin_queasy.reslinnr == reslinnr) & (Reslin_queasy._recid > curr_recid)).with_for_update().first()

        for adhoc in query(adhoc_data, filters=(lambda adhoc: adhoc.acode.lower()  == (adhoc_code).lower())):
            fill_adhoc_argt()


    def fill_adhoc_argt():

        nonlocal argt_list_data, post_type, pers_type, lvcarea, reslin_queasy, argt_line, artikel
        nonlocal pvilanguage, adhoc_code, argtnr, resnr, reslinnr, from_date, to_date


        nonlocal adhoc, argt_list
        nonlocal argt_list_data


        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "fargt-line"
        reslin_queasy.number1 = adhoc.deptnr
        reslin_queasy.number2 = argtnr
        reslin_queasy.number3 = adhoc.artnr
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.deci1 =  to_decimal(adhoc.amount)
        reslin_queasy.date1 = from_date
        reslin_queasy.date2 = to_date
        reslin_queasy.deci2 =  to_decimal(adhoc.child1)
        reslin_queasy.deci3 =  to_decimal(adhoc.child2)

        db_session.refresh(reslin_queasy, with_for_update=True)


    def create_argt_list():

        nonlocal argt_list_data, post_type, pers_type, lvcarea, reslin_queasy, argt_line, artikel
        nonlocal pvilanguage, adhoc_code, argtnr, resnr, reslinnr, from_date, to_date


        nonlocal adhoc, argt_list
        nonlocal argt_list_data

        reslin_queasy_obj_list = {}
        for reslin_queasy, argt_line, artikel in db_session.query(Reslin_queasy, Argt_line, Artikel).join(Argt_line,(Argt_line.argtnr == Reslin_queasy.number2) & (Argt_line.argt_artnr == Reslin_queasy.number3) & (Argt_line.departement == Reslin_queasy.number1)).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                 (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.number2 == argtnr) & (Reslin_queasy.reslinnr == reslinnr)).order_by(Argt_line.argt_artnr, Reslin_queasy.date1).all():
            if reslin_queasy_obj_list.get(reslin_queasy._recid):
                continue
            else:
                reslin_queasy_obj_list[reslin_queasy._recid] = True


            argt_list = Argt_list()
            argt_list_data.append(argt_list)

            argt_list.argt_artnr = argt_line.argt_artnr
            argt_list.bezeich = artikel.bezeich
            argt_list.departement = artikel.departement
            argt_list.deci1 =  to_decimal(reslin_queasy.deci1)
            argt_list.deci2 =  to_decimal(reslin_queasy.deci2)
            argt_list.deci3 =  to_decimal(reslin_queasy.deci3)
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