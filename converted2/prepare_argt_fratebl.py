#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Arrangement, Artprice, Artikel, Argt_line, Reslin_queasy

def prepare_argt_fratebl(pvilanguage:int, resnr:int, reslinnr:int, argt:string, ankunft:date, abreise:date):

    prepare_cache ([Arrangement, Artprice, Artikel, Argt_line, Reslin_queasy])

    argtnr = 0
    adhoc_data = []
    argt_list_data = []
    post_type:List[string] = create_empty_list(6,"")
    pers_type:List[string] = create_empty_list(3,"")
    lvcarea:string = "argt-frate"
    arrangement = artprice = artikel = argt_line = reslin_queasy = None

    adhoc = argt_list = None

    adhoc_data, Adhoc = create_model("Adhoc", {"acode":string, "artnr":int, "deptnr":int, "bezeich":string, "amount":Decimal, "child1":Decimal, "child2":Decimal, "post_type":int})
    argt_list_data, Argt_list = create_model("Argt_list", {"argt_artnr":int, "bezeich":string, "departement":int, "deci1":Decimal, "date1":date, "date2":date, "deci2":Decimal, "deci3":Decimal, "post_type":string, "pers_type":string, "fakt_modus":int, "vt_percnt":int, "s_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal argtnr, adhoc_data, argt_list_data, post_type, pers_type, lvcarea, arrangement, artprice, artikel, argt_line, reslin_queasy
        nonlocal pvilanguage, resnr, reslinnr, argt, ankunft, abreise


        nonlocal adhoc, argt_list
        nonlocal adhoc_data, argt_list_data

        return {"argtnr": argtnr, "adhoc": adhoc_data, "argt-list": argt_list_data}

    def create_browseb2():

        nonlocal argtnr, adhoc_data, argt_list_data, post_type, pers_type, lvcarea, arrangement, artprice, artikel, argt_line, reslin_queasy
        nonlocal pvilanguage, resnr, reslinnr, argt, ankunft, abreise


        nonlocal adhoc, argt_list
        nonlocal adhoc_data, argt_list_data

        from_date:date = None
        to_date:date = None
        i:int = 0

        for artprice in db_session.query(Artprice).filter(
                 (Artprice.artnr == argtnr)).order_by(Artprice._recid).all():
            from_date = date_mdy(to_int(substring(to_string(start_time) , 4, 2)) , to_int(substring(to_string(start_time) , 6, 2)) , to_int(substring(to_string(start_time) , 0, 4)))
            to_date = date_mdy(to_int(substring(to_string(end_time) , 4, 2)) , to_int(substring(to_string(end_time) , 6, 2)) , to_int(substring(to_string(end_time) , 0, 4)))

            if from_date <= ankunft and to_date >= abreise:
                for i in range(2,(num_entries(artprice.bezeich, ";") - 1)  + 1) :
                    adhoc = Adhoc()
                    adhoc_data.append(adhoc)

                    adhoc.acode = entry(0, artprice.bezeich, ";")
                    adhoc.artnr = to_int(entry(1, entry(i - 1, artprice.bezeich, ";") , ","))
                    adhoc.deptnr = to_int(entry(0, entry(i - 1, artprice.bezeich, ";") , ","))
                    adhoc.amount =  to_decimal(to_int(entry(2 , entry(i) - to_decimal(1 , artprice.bezeich , ";") , ","))) / to_decimal("100")
                    adhoc.child1 =  to_decimal(to_int(entry(3 , entry(i) - to_decimal(1 , artprice.bezeich , ";") , ","))) / to_decimal("100")
                    adhoc.child2 =  to_decimal(to_int(entry(4 , entry(i) - to_decimal(1 , artprice.bezeich , ";") , ","))) / to_decimal("100")
                    adhoc.post_type = to_int(entry(5, entry(i - 1, artprice.bezeich, ";") , ","))

                    artikel = get_cache (Artikel, {"artnr": [(eq, adhoc.artnr)],"departement": [(eq, adhoc.deptnr)]})

                    if artikel:
                        adhoc.bezeich = artikel.bezeich


    def create_argt_list():

        nonlocal argtnr, adhoc_data, argt_list_data, post_type, pers_type, lvcarea, arrangement, artprice, artikel, argt_line, reslin_queasy
        nonlocal pvilanguage, resnr, reslinnr, argt, ankunft, abreise


        nonlocal adhoc, argt_list
        nonlocal adhoc_data, argt_list_data

        reslin_queasy_obj_list = {}
        reslin_queasy = Reslin_queasy()
        argt_line = Argt_line()
        artikel = Artikel()
        for reslin_queasy.deci1, reslin_queasy.deci2, reslin_queasy.deci3, reslin_queasy.date1, reslin_queasy.date2, reslin_queasy.char2, reslin_queasy._recid, argt_line.argt_artnr, argt_line.fakt_modus, argt_line._recid, artikel.bezeich, artikel.departement, artikel._recid in db_session.query(Reslin_queasy.deci1, Reslin_queasy.deci2, Reslin_queasy.deci3, Reslin_queasy.date1, Reslin_queasy.date2, Reslin_queasy.char2, Reslin_queasy._recid, Argt_line.argt_artnr, Argt_line.fakt_modus, Argt_line._recid, Artikel.bezeich, Artikel.departement, Artikel._recid).join(Argt_line,(Argt_line.argtnr == Reslin_queasy.number2) & (Argt_line.argt_artnr == Reslin_queasy.number3) & (Argt_line.departement == Reslin_queasy.number1)).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
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

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, argt)]})
    argtnr = arrangement.argtnr


    create_browseb2()
    create_argt_list()

    return generate_output()