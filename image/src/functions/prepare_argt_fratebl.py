from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Arrangement, Artprice, Artikel, Argt_line, Reslin_queasy

def prepare_argt_fratebl(pvilanguage:int, resnr:int, reslinnr:int, argt:str, ankunft:date, abreise:date):
    argtnr = 0
    adhoc_list = []
    argt_list_list = []
    post_type:str = ""
    pers_type:str = ""
    lvcarea:str = "argt_frate"
    arrangement = artprice = artikel = argt_line = reslin_queasy = None

    adhoc = argt_list = None

    adhoc_list, Adhoc = create_model("Adhoc", {"acode":str, "artnr":int, "deptnr":int, "bezeich":str, "amount":decimal, "child1":decimal, "child2":decimal, "post_type":int})
    argt_list_list, Argt_list = create_model("Argt_list", {"argt_artnr":int, "bezeich":str, "departement":int, "deci1":decimal, "date1":date, "date2":date, "deci2":decimal, "deci3":decimal, "post_type":str, "pers_type":str, "fakt_modus":int, "vt_percnt":int, "s_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal argtnr, adhoc_list, argt_list_list, post_type, pers_type, lvcarea, arrangement, artprice, artikel, argt_line, reslin_queasy


        nonlocal adhoc, argt_list
        nonlocal adhoc_list, argt_list_list
        return {"argtnr": argtnr, "adhoc": adhoc_list, "argt-list": argt_list_list}

    def create_browseb2():

        nonlocal argtnr, adhoc_list, argt_list_list, post_type, pers_type, lvcarea, arrangement, artprice, artikel, argt_line, reslin_queasy


        nonlocal adhoc, argt_list
        nonlocal adhoc_list, argt_list_list

        from_date:date = None
        to_date:date = None
        i:int = 0

        for artprice in db_session.query(Artprice).filter(
                (Artprice.artnr == argtnr)).all():
            from_date = date_mdy(to_int(substring(to_string(start_time) , 4, 2)) , to_int(substring(to_string(start_time) , 6, 2)) , to_int(substring(to_string(start_time) , 0, 4)))
            to_date = date_mdy(to_int(substring(to_string(end_time) , 4, 2)) , to_int(substring(to_string(end_time) , 6, 2)) , to_int(substring(to_string(end_time) , 0, 4)))

            if from_date <= ankunft and to_date >= abreise:
                for i in range(2,(num_entries(artprice.bezeich, ";") - 1)  + 1) :
                    adhoc = Adhoc()
                    adhoc_list.append(adhoc)

                    adhoc.acode = entry(0, artprice.bezeich, ";")
                    adhoc.artnr = to_int(entry(1, entry(i - 1, artprice.bezeich, ";") , ","))
                    adhoc.deptnr = to_int(entry(0, entry(i - 1, artprice.bezeich, ";") , ","))
                    adhoc.amount = to_int(entry(2, entry(i - 1, artprice.bezeich, ";") , ",")) / 100
                    adhoc.child1 = to_int(entry(3, entry(i - 1, artprice.bezeich, ";") , ",")) / 100
                    adhoc.child2 = to_int(entry(4, entry(i - 1, artprice.bezeich, ";") , ",")) / 100
                    adhoc.post_type = to_int(entry(5, entry(i - 1, artprice.bezeich, ";") , ","))

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == adhoc.artnr) &  (Artikel.departement == adhoc.deptnr)).first()

                    if artikel:
                        adhoc.bezeich = artikel.bezeich

    def create_argt_list():

        nonlocal argtnr, adhoc_list, argt_list_list, post_type, pers_type, lvcarea, arrangement, artprice, artikel, argt_line, reslin_queasy


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
            argt_list.vt_percnt = to_int(reslin_queasy.char2)
            argt_list.s_recid = to_int(reslin_queasy._recid)
            argt_list.post_type = post_type[argt_line.fakt_modus - 1]

            if reslin_queasy.deci1 != 0:
                argt_list.pers_type = "Adult"

            elif reslin_queasy.deci1 == 0 and reslin_queasy.deci2 != 0 and reslin_queasy.deci3 != 0:
                argt_list.pers_type = "Child"

            elif reslin_queasy.deci1 == 0 and reslin_queasy.deci2 == 0 and reslin_queasy.deci3 != 0:
                argt_list.pers_type = "Child2"

    post_type[0] = translateExtended ("Daily", lvcarea, "")
    post_type[1] = translateExtended ("CI Day", lvcarea, "")
    post_type[2] = translateExtended ("2nd Day", lvcarea, "")
    post_type[3] = translateExtended ("Mon 1st Day", lvcarea, "")
    post_type[4] = translateExtended ("Mon LastDay", lvcarea, "")
    post_type[5] = translateExtended ("Special", lvcarea, "")


    pers_type[0] = translateExtended ("Adult", lvcarea, "")
    pers_type[1] = translateExtended ("Child", lvcarea, "")
    pers_type[2] = translateExtended ("Ch2", lvcarea, "")

    arrangement = db_session.query(Arrangement).filter(
            (func.lower(Arrangement) == (argt).lower())).first()
    argtnr = arrangement.argtnr


    create_browseb2()
    create_argt_list()

    return generate_output()