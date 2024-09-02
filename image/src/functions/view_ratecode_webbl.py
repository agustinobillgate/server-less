from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Htparam, Prmarket, Prtable, Arrangement, Zimkateg, Waehrung, Ratecode, Reslin_queasy, Artikel, Argt_line, Guest, Guest_pr

def view_ratecode_webbl(pvilanguage:int, gastnr:int, pr_code:str, market_combo:str):
    comments = ""
    t_viewrates_list = []
    t_viewrates_line_list = []
    ci_date:date = None
    current_counter:int = 0
    lvcarea:str = "view_ratecode_web"
    queasy = htparam = prmarket = prtable = arrangement = zimkateg = waehrung = ratecode = reslin_queasy = artikel = argt_line = guest = guest_pr = None

    t_viewrates = t_viewrates_line = select_list = qsy = None

    t_viewrates_list, T_viewrates = create_model("T_viewrates", {"prcode":str, "desc_prcode":str, "currency":str, "market":str, "argt":str, "rmtype":str})
    t_viewrates_line_list, T_viewrates_line = create_model("T_viewrates_line", {"prcode":str, "desc_prcode":str, "currency":str, "market":str, "argt":str, "rmtype":str, "datum":str, "str_aci":str, "aci":str, "str_rate_aci":str, "adult_rate":str, "child_rate":str, "infant_rate":str, "deci4":str})
    select_list_list, Select_list = create_model("Select_list", {"argtnr":int, "zikatnr":int})

    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal comments, t_viewrates_list, t_viewrates_line_list, ci_date, current_counter, lvcarea, queasy, htparam, prmarket, prtable, arrangement, zimkateg, waehrung, ratecode, reslin_queasy, artikel, argt_line, guest, guest_pr
        nonlocal qsy


        nonlocal t_viewrates, t_viewrates_line, select_list, qsy
        nonlocal t_viewrates_list, t_viewrates_line_list, select_list_list
        return {"comments": comments, "t-viewrates": t_viewrates_list, "t-viewrates-line": t_viewrates_line_list}

    def create_list0():

        nonlocal comments, t_viewrates_list, t_viewrates_line_list, ci_date, current_counter, lvcarea, queasy, htparam, prmarket, prtable, arrangement, zimkateg, waehrung, ratecode, reslin_queasy, artikel, argt_line, guest, guest_pr
        nonlocal qsy


        nonlocal t_viewrates, t_viewrates_line, select_list, qsy
        nonlocal t_viewrates_list, t_viewrates_line_list, select_list_list

        marknr1:int = 0
        argt1:int = 0
        zikat1:int = 0
        i:int = 0
        n:int = 0
        ct:str = ""
        st:str = ""
        curr_str:str = ""
        currency:str = ""
        f_date:date = None
        t_date:date = None
        disc_rate:decimal = 0
        rate:decimal = 0
        queasy_exist:bool = False
        fixed_rate:bool = False
        do_it:bool = False
        Qsy = Queasy

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate

        prtable_obj_list = []
        for prtable, prmarket in db_session.query(Prtable, Prmarket).join(Prmarket,(Prmarket.nr == Prtable.marknr) &  (func.lower(Prmarket.bezeich) == (market_combo).lower())).filter(
                (func.lower(Prtable.prcode) == (pr_code).lower())).all():
            if prtable._recid in prtable_obj_list:
                continue
            else:
                prtable_obj_list.append(prtable._recid)


            create_selectlist()

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 18) &  (Qsy.number1 == prmarket.nr)).first()

            if qsy:
                currency = qsy.char3
                fixed_rate = qsy.logi3

            for select_list in query(select_list_list):

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement.argtnr == select_list.argtnr)).first()

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == select_list.zikatnr)).first()
                argt1 = 0
                zikat1 = 0
                queasy_exist = False

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 2) &  (Queasy.char1 == prtable.prcode)).first()

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == queasy.number1)).first()

                t_viewrates = query(t_viewrates_list, filters=(lambda t_viewrates :t_viewrates.prcode.lower()  == (pr_code).lower()  and t_viewrates.argt == arrangement and t_viewrates.rmtype == zimkateg.kurzbez), first=True)

                if not t_viewrates:
                    t_viewrates = T_viewrates()
                    t_viewrates_list.append(t_viewrates)


                    if queasy:
                        t_viewrates.prcode = queasy.char1
                        t_viewrates.desc_prcode = queasy.char2

                    if waehrung:
                        t_viewrates.currency = waehrung.bezeich

                    if currency != "":
                        t_viewrates.market = prmarket.bezeich + " - " + "currency" + "  ==  " + qsy.char3

                    if fixed_rate:
                        t_viewrates.market = prmarket.bezeich + "; " + "Fixed rate for whole stay"
                    t_viewrates.argt = arrangement
                    t_viewrates.rmtype = zimkateg.kurzbez

                for ratecode in db_session.query(Ratecode).filter(
                        (func.lower(Ratecode.code) == (pr_code).lower()) &  (Ratecode.marknr == prtable.marknr) &  (Ratecode.zikatnr == select_list.zikatnr) &  (Ratecode.argtnr == select_list.argtnr)).all():
                    do_it = (ci_date <= ratecode.endperiode)

                    if do_it:
                        t_viewrates_line = T_viewrates_line()
                        t_viewrates_line_list.append(t_viewrates_line)


                        if queasy:
                            t_viewrates_line.prcode = queasy.char1
                            t_viewrates_line.desc_prcode = queasy.char2

                        if waehrung:
                            t_viewrates_line.currency = waehrung.bezeich

                        if currency != "":
                            t_viewrates_line.market = prmarket.bezeich + " - " + "currency" + "  ==  " + qsy.char3

                        if fixed_rate:
                            t_viewrates_line.market = prmarket.bezeich + "; " + "Fixed rate for whole stay"
                        t_viewrates_line.argt = arrangement
                        t_viewrates_line.rmtype = zimkateg.kurzbez
                        t_viewrates_line.datum = to_string(ratecode.startperiode, "99/99/99") +\
                                " - " + to_string(ratecode.endperiode, "99/99/99")
                        t_viewrates_line.str_aci = "Adult/Child/Infant :"
                        t_viewrates_line.aci = to_string(ratecode.erwachs) + "/" + to_string(ratecode.kind1) + "/" +\
                                to_string(ratecode.kind2)
                        t_viewrates_line.str_rate_aci = "Adult rate/Child rate/Infant rate :"
                        t_viewrates_line.adult_rate = trim(to_string(ratecode.zipreis, ">>>,>>>,>>9.99"))
                        t_viewrates_line.child_rate = trim(to_string(ratecode.ch1preis, ">>>,>>>,>>9.99"))
                        t_viewrates_line.infant_rate = trim(to_string(ratecode.ch2preis, ">>>,>>>,>>9.99"))

                        if ratecode.char1[0] != "" or ratecode.char1[1] != "" or ratecode.char1[2] != "" or ratecode.char1[3] != "":

                            if num_entries(ratecode.char1[3], ";") >= 3:
                                t_viewrates_line = T_viewrates_line()
                                t_viewrates_line_list.append(t_viewrates_line)


                                if queasy:
                                    t_viewrates_line.prcode = queasy.char1
                                t_viewrates_line.argt = arrangement
                                t_viewrates_line.rmtype = zimkateg.kurzbez
                                t_viewrates_line.datum = "COMPLIMENT ROOM :"
                                t_viewrates_line.str_aci = "Room Booked / Get Compliment / Tpotal Compliment :"
                                t_viewrates_line.adult_rate = trim(to_string(to_int(entry(0, ratecode.char1[3], ";")) , ">>9"))
                                t_viewrates_line.child_rate = trim(to_string(to_int(entry(1, ratecode.char1[3], ";")) , ">>9"))
                                t_viewrates_line.infant_rate = trim(to_string(to_int(entry(2, ratecode.char1[3], ";")) , ">>9"))

                            if num_entries(ratecode.char1[0], ";") >= 2:
                                t_viewrates_line = T_viewrates_line()
                                t_viewrates_line_list.append(t_viewrates_line)

                                for n in range(1,num_entries(ratecode.char1[0], ";") - 1 + 1) :
                                    ct = entry(n - 1, ratecode.char1[0], ";")
                                    disc_rate = decimal.Decimal(entry(0, ct, ",")) / 100

                                    if queasy:
                                        t_viewrates_line.prcode = queasy.char1
                                    t_viewrates_line.argt = arrangement
                                    t_viewrates_line.rmtype = zimkateg.kurzbez
                                    t_viewrates_line.datum = "EARLY BOOKING :"
                                    t_viewrates_line.str_aci = "Discount% / Advance Minimum Booking (Day) / Minimum Stay / Up To Occupancy"
                                    t_viewrates_line.adult_rate = trim(to_string(disc_rate, ">9.99 "))
                                    t_viewrates_line.child_rate = trim(to_string(to_int(entry(1, ct, ",")) , ">>>>>>>>9"))
                                    t_viewrates_line.infant_rate = trim(to_string(to_int(entry(2, ct, ",")) , ">>>>>9"))
                                    t_viewrates_line.deci4 = trim(to_string(to_int(entry(3, ct, ",")) , ">>>>>>9"))

                            if num_entries(ratecode.char1[1], ";") >= 2:
                                t_viewrates_line = T_viewrates_line()
                                t_viewrates_line_list.append(t_viewrates_line)

                                for n in range(1,num_entries(ratecode.char1[1], ";") - 1 + 1) :
                                    ct = entry(n - 1, ratecode.char1[1], ";")
                                    disc_rate = decimal.Decimal(entry(0, ct, ",")) / 100

                                    if queasy:
                                        t_viewrates_line.prcode = queasy.char1
                                    t_viewrates_line.argt = arrangement
                                    t_viewrates_line.rmtype = zimkateg.kurzbez
                                    t_viewrates_line.datum = "KICKBACK DISCOUNT :"
                                    t_viewrates_line.str_aci = "Discount% / Advance Maximum Booking (Day) / Minimum Stay / Up To Occupancy"
                                    t_viewrates_line.adult_rate = trim(to_string(disc_rate, ">9.99"))
                                    t_viewrates_line.child_rate = trim(to_string(to_int(entry(1, ct, ",")) , ">>>>>>>>9"))
                                    t_viewrates_line.infant_rate = trim(to_string(to_int(entry(2, ct, ",")) , ">>>>>9"))
                                    t_viewrates_line.deci4 = trim(to_string(to_int(entry(3, ct, ",")) , ">>>>>>9"))

                            if num_entries(ratecode.char1[2], ";") >= 2:
                                t_viewrates_line = T_viewrates_line()
                                t_viewrates_line_list.append(t_viewrates_line)

                                for n in range(1,num_entries(ratecode.char1[2], ";") - 1 + 1) :
                                    ct = entry(n - 1, ratecode.char1[2], ";")
                                    f_date = date_mdy(to_int(substring(entry(0, ct, ",") , 4, 2)) , to_int(substring(entry(0, ct, ",") , 6, 2)) , to_int(substring(entry(0, ct, ",") , 0, 4)))
                                    t_date = date_mdy(to_int(substring(entry(1, ct, ",") , 4, 2)) , to_int(substring(entry(1, ct, ",") , 6, 2)) , to_int(substring(entry(1, ct, ",") , 0, 4)))

                                    if queasy:
                                        t_viewrates_line.prcode = queasy.char1
                                    t_viewrates_line.argt = arrangement
                                    t_viewrates_line.rmtype = zimkateg.kurzbez
                                    t_viewrates_line.datum = "STAY/PAY :"
                                    t_viewrates_line.adult_rate = to_string(f_date) + " - " + to_string(t_date)
                                    t_viewrates_line.child_rate = trim(to_string(to_int(entry(2, ct, ",")) , ">>>9"))
                                    t_viewrates_line.infant_rate = trim(to_string(to_int(entry(3, ct, ",")) , ">>>9"))


                        argt1 = ratecode.argtnr
                        zikat1 = ratecode.zikatnr

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (pr_code).lower()) &  (Reslin_queasy.number1 == prtable.marknr) &  (Reslin_queasy.number2 == select_list.argtnr) &  (Reslin_queasy.reslinnr == select_list.zikatnr)).all():
                    queasy_exist = True

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == reslin_queasy.number3) &  (Artikel.departement == reslin_queasy.resnr)).first()

                    argt_line = db_session.query(Argt_line).filter(
                            (Argt_line.argtnr == select_list.argtnr) &  (Argt_line.argt_artnr == artikel.artnr) &  (Argt_line.departement == artikel.departement)).first()

                    if ci_date <= reslin_queasy.date2 and do_it:
                        t_viewrates_line = T_viewrates_line()
                        t_viewrates_line_list.append(t_viewrates_line)

                        t_viewrates_line.prcode = queasy.char1
                        t_viewrates_line.argt = arrangement
                        t_viewrates_line.rmtype = zimkateg.kurzbez
                        t_viewrates_line.datum = to_string(reslin_queasy.date1, "99/99/99") +\
                                " - " + to_string(reslin_queasy.date2, "99/99/99")
                        t_viewrates_line.str_aci = artikel.bezeich
                        t_viewrates_line.aci = "rate : " + trim(to_string(reslin_queasy.deci1, ">>>,>>>,>>9.99"))

                        if argt_line:
                            t_viewrates_line.str_rate_aci = "Posted : " + to_string(argt_line.fakt_modus, "9")

                            if argt_line.fakt_modus == 6:
                                t_viewrates_line.str_rate_aci = t_viewrates_line.str_rate_aci + "/" + to_string(argt_line.intervall, "9")
                            else:
                                t_viewrates_line.adult_rate = "rate Include : " + to_string(argt_line.kind1, "Yes/No")
                            t_viewrates_line.child_rate = "Optional : " + to_string(argt_line.kind2, "Yes/No")

                            if argt_line.betriebsnr == 0:
                                t_viewrates_line.infant_rate = "Qty Always 1 : No"
                            else:
                                t_viewrates_line.infant_rate = "Qty Always 1 : Yes"

                if not queasy_exist:

                    for argt_line in db_session.query(Argt_line).filter(
                            (Argt_line.argtnr == argt1)).all():

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()
                        t_viewrates_line = T_viewrates_line()
                        t_viewrates_line_list.append(t_viewrates_line)

                        t_viewrates_line.prcode = queasy.char1
                        t_viewrates_line.argt = arrangement
                        t_viewrates_line.rmtype = zimkateg.kurzbez

                        if argt_line.vt_percnt == 0:
                            t_viewrates_line.datum = "" + " - " + ""
                            t_viewrates_line.str_aci = artikel.bezeich
                            t_viewrates_line.aci = "Adult rate : " + trim(to_string(argt_line.betrag, ">>>,>>>,>>9.99"))
                            t_viewrates_line.str_rate_aci = "Posted : " + to_string(argt_line.fakt_modus, "9")

                        elif argt_line.vt_percnt == 1:
                            t_viewrates_line.datum = "" + " - " + ""
                            t_viewrates_line.str_aci = artikel.bezeich
                            t_viewrates_line.aci = "Child rate : " + trim(to_string(argt_line.betrag, ">>>,>>>,>>9.99"))
                            t_viewrates_line.str_rate_aci = "Posted : " + to_string(argt_line.fakt_modus, "9")

                        elif argt_line.vt_percnt == 2:
                            t_viewrates_line.datum = "" + " - " + ""
                            t_viewrates_line.str_aci = artikel.bezeich
                            t_viewrates_line.aci = "Infant rate : " + trim(to_string(argt_line.betrag, ">>>,>>>,>>9.99"))
                            t_viewrates_line.str_rate_aci = "Posted : " + to_string(argt_line.fakt_modus, "9")

                        if argt_line.fakt_modus == 6:
                            t_viewrates_line.str_rate_aci = t_viewrates_line.str_rate_aci + "/" + to_string(argt_line.intervall, "9")
                        else:
                            t_viewrates_line.adult_rate = "rate Include : " + to_string(argt_line.kind1, "Yes/No")
                        t_viewrates_line.child_rate = "Optional : " + to_string(argt_line.kind2, "Yes/No")

                        if argt_line.betriebsnr == 0:
                            t_viewrates_line.infant_rate = "Qty Always 1 : No"
                        else:
                            t_viewrates_line.infant_rate = "Qty Always 1 : Yes"

    def create_list():

        nonlocal comments, t_viewrates_list, t_viewrates_line_list, ci_date, current_counter, lvcarea, queasy, htparam, prmarket, prtable, arrangement, zimkateg, waehrung, ratecode, reslin_queasy, artikel, argt_line, guest, guest_pr
        nonlocal qsy


        nonlocal t_viewrates, t_viewrates_line, select_list, qsy
        nonlocal t_viewrates_list, t_viewrates_line_list, select_list_list

        marknr1:int = 0
        argt1:int = 0
        zikat1:int = 0
        i:int = 0
        n:int = 0
        ct:str = ""
        st:str = ""
        curr_str:str = ""
        currency:str = ""
        f_date:date = None
        t_date:date = None
        disc_rate:decimal = 0
        rate:decimal = 0
        queasy_exist:bool = False
        fixed_rate:bool = False
        do_it:bool = False
        Qsy = Queasy

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == gastnr)).first()
        comments = guest.bemerk

        for guest_pr in db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == gastnr)).all():
            pr_code = guest_pr.CODE

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (func.lower(Queasy.char1) == (pr_code).lower())).first()

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == queasy.number1)).first()
            t_viewrates = T_viewrates()
            t_viewrates_list.append(t_viewrates)


            if queasy:
                t_viewrates.prcode = queasy.char1
                t_viewrates.desc_prcode = queasy.char2

            if waehrung:
                t_viewrates.currency = waehrung.bezeich

            prtable_obj_list = []
            for prtable, prmarket in db_session.query(Prtable, Prmarket).join(Prmarket,(Prmarket.nr == Prtable.marknr) &  (func.lower(Prmarket.bezeich) == (market_combo).lower())).filter(
                    (func.lower(Prtable.prcode) == (pr_code).lower())).all():
                if prtable._recid in prtable_obj_list:
                    continue
                else:
                    prtable_obj_list.append(prtable._recid)


                create_selectlist()

                qsy = db_session.query(Qsy).filter(
                        (Qsy.key == 18) &  (Qsy.number1 == prmarket.nr)).first()

                if qsy:
                    currency = qsy.char3
                    fixed_rate = qsy.logi3

                for select_list in query(select_list_list):

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement.argtnr == select_list.argtnr)).first()

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == select_list.zikatnr)).first()
                    argt1 = 0
                    zikat1 = 0
                    queasy_exist = False

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 2) &  (Queasy.char1 == prtable.prcode)).first()

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == queasy.number1)).first()

                    t_viewrates = query(t_viewrates_list, filters=(lambda t_viewrates :t_viewrates.prcode.lower()  == (pr_code).lower()  and t_viewrates.argt == arrangement and t_viewrates.rmtype == zimkateg.kurzbez), first=True)

                    if not t_viewrates:
                        t_viewrates = T_viewrates()
                        t_viewrates_list.append(t_viewrates)


                        if queasy:
                            t_viewrates.prcode = queasy.char1
                            t_viewrates.desc_prcode = queasy.char2

                        if waehrung:
                            t_viewrates.currency = waehrung.bezeich

                        if currency != "":
                            t_viewrates.market = prmarket.bezeich + " - " + "currency" + "  ==  " + qsy.char3

                        if fixed_rate:
                            t_viewrates.market = prmarket.bezeich + "; " + "Fixed rate for whole stay"
                        t_viewrates.argt = arrangement
                        t_viewrates.rmtype = zimkateg.kurzbez

                    for ratecode in db_session.query(Ratecode).filter(
                            (func.lower(Ratecode.code) == (pr_code).lower()) &  (Ratecode.marknr == prtable.marknr) &  (Ratecode.zikatnr == select_list.zikatnr) &  (Ratecode.argtnr == select_list.argtnr)).all():
                        do_it = (ci_date <= ratecode.endperiode)

                        if do_it:
                            t_viewrates_line = T_viewrates_line()
                            t_viewrates_line_list.append(t_viewrates_line)


                            if queasy:
                                t_viewrates_line.prcode = queasy.char1
                                t_viewrates_line.desc_prcode = queasy.char2

                            if waehrung:
                                t_viewrates_line.currency = waehrung.bezeich

                            if currency != "":
                                t_viewrates_line.market = prmarket.bezeich + " - " + "currency" + "  ==  " + qsy.char3

                            if fixed_rate:
                                t_viewrates_line.market = prmarket.bezeich + "; " + "Fixed rate for whole stay"
                            t_viewrates_line.argt = arrangement
                            t_viewrates_line.rmtype = zimkateg.kurzbez
                            t_viewrates_line.datum = to_string(ratecode.startperiode, "99/99/99") +\
                                    " - " + to_string(ratecode.endperiode, "99/99/99")
                            t_viewrates_line.str_aci = "Adult/Child/Infant :"
                            t_viewrates_line.aci = to_string(ratecode.erwachs) + "/" + to_string(ratecode.kind1) + "/" +\
                                    to_string(ratecode.kind2)
                            t_viewrates_line.str_rate_aci = "Adult rate/Child rate/Infant rate :"
                            t_viewrates_line.adult_rate = trim(to_string(ratecode.zipreis, ">>>,>>>,>>9.99"))
                            t_viewrates_line.child_rate = trim(to_string(ratecode.ch1preis, ">>>,>>>,>>9.99"))
                            t_viewrates_line.infant_rate = trim(to_string(ratecode.ch2preis, ">>>,>>>,>>9.99"))

                            if ratecode.char1[0] != "" or ratecode.char1[1] != "" or ratecode.char1[2] != "" or ratecode.char1[3] != "":

                                if num_entries(ratecode.char1[3], ";") >= 3:
                                    t_viewrates_line = T_viewrates_line()
                                    t_viewrates_line_list.append(t_viewrates_line)


                                    if queasy:
                                        t_viewrates_line.prcode = queasy.char1
                                    t_viewrates_line.argt = arrangement
                                    t_viewrates_line.rmtype = zimkateg.kurzbez
                                    t_viewrates_line.datum = "COMPLIMENT ROOM :"
                                    t_viewrates_line.str_aci = "Room Booked / Get Compliment / Tpotal Compliment :"
                                    t_viewrates_line.adult_rate = trim(to_string(to_int(entry(0, ratecode.char1[3], ";")) , ">>9"))
                                    t_viewrates_line.child_rate = trim(to_string(to_int(entry(1, ratecode.char1[3], ";")) , ">>9"))
                                    t_viewrates_line.infant_rate = trim(to_string(to_int(entry(2, ratecode.char1[3], ";")) , ">>9"))

                                if num_entries(ratecode.char1[0], ";") >= 2:
                                    t_viewrates_line = T_viewrates_line()
                                    t_viewrates_line_list.append(t_viewrates_line)

                                    for n in range(1,num_entries(ratecode.char1[0], ";") - 1 + 1) :
                                        ct = entry(n - 1, ratecode.char1[0], ";")
                                        disc_rate = decimal.Decimal(entry(0, ct, ",")) / 100

                                        if queasy:
                                            t_viewrates_line.prcode = queasy.char1
                                        t_viewrates_line.argt = arrangement
                                        t_viewrates_line.rmtype = zimkateg.kurzbez
                                        t_viewrates_line.datum = "EARLY BOOKING :"
                                        t_viewrates_line.str_aci = "Discount% / Advance Minimum Booking (Day) / Minimum Stay / Up To Occupancy"
                                        t_viewrates_line.adult_rate = trim(to_string(disc_rate, ">9.99 "))
                                        t_viewrates_line.child_rate = trim(to_string(to_int(entry(1, ct, ",")) , ">>>>>>>>9"))
                                        t_viewrates_line.infant_rate = trim(to_string(to_int(entry(2, ct, ",")) , ">>>>>9"))
                                        t_viewrates_line.deci4 = trim(to_string(to_int(entry(3, ct, ",")) , ">>>>>>9"))

                                if num_entries(ratecode.char1[1], ";") >= 2:
                                    t_viewrates_line = T_viewrates_line()
                                    t_viewrates_line_list.append(t_viewrates_line)

                                    for n in range(1,num_entries(ratecode.char1[1], ";") - 1 + 1) :
                                        ct = entry(n - 1, ratecode.char1[1], ";")
                                        disc_rate = decimal.Decimal(entry(0, ct, ",")) / 100

                                        if queasy:
                                            t_viewrates_line.prcode = queasy.char1
                                        t_viewrates_line.argt = arrangement
                                        t_viewrates_line.rmtype = zimkateg.kurzbez
                                        t_viewrates_line.datum = "KICKBACK DISCOUNT :"
                                        t_viewrates_line.str_aci = "Discount% / Advance Maximum Booking (Day) / Minimum Stay / Up To Occupancy"
                                        t_viewrates_line.adult_rate = trim(to_string(disc_rate, ">9.99"))
                                        t_viewrates_line.child_rate = trim(to_string(to_int(entry(1, ct, ",")) , ">>>>>>>>9"))
                                        t_viewrates_line.infant_rate = trim(to_string(to_int(entry(2, ct, ",")) , ">>>>>9"))
                                        t_viewrates_line.deci4 = trim(to_string(to_int(entry(3, ct, ",")) , ">>>>>>9"))

                                if num_entries(ratecode.char1[2], ";") >= 2:
                                    t_viewrates_line = T_viewrates_line()
                                    t_viewrates_line_list.append(t_viewrates_line)

                                    for n in range(1,num_entries(ratecode.char1[2], ";") - 1 + 1) :
                                        ct = entry(n - 1, ratecode.char1[2], ";")
                                        f_date = date_mdy(to_int(substring(entry(0, ct, ",") , 4, 2)) , to_int(substring(entry(0, ct, ",") , 6, 2)) , to_int(substring(entry(0, ct, ",") , 0, 4)))
                                        t_date = date_mdy(to_int(substring(entry(1, ct, ",") , 4, 2)) , to_int(substring(entry(1, ct, ",") , 6, 2)) , to_int(substring(entry(1, ct, ",") , 0, 4)))

                                        if queasy:
                                            t_viewrates_line.prcode = queasy.char1
                                        t_viewrates_line.argt = arrangement
                                        t_viewrates_line.rmtype = zimkateg.kurzbez
                                        t_viewrates_line.datum = "STAY/PAY :"
                                        t_viewrates_line.adult_rate = to_string(f_date) + " - " + to_string(t_date)
                                        t_viewrates_line.child_rate = trim(to_string(to_int(entry(2, ct, ",")) , ">>>9"))
                                        t_viewrates_line.infant_rate = trim(to_string(to_int(entry(3, ct, ",")) , ">>>9"))


                            argt1 = ratecode.argtnr
                            zikat1 = ratecode.zikatnr

                    for reslin_queasy in db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (pr_code).lower()) &  (Reslin_queasy.number1 == prtable.marknr) &  (Reslin_queasy.number2 == select_list.argtnr) &  (Reslin_queasy.reslinnr == select_list.zikatnr)).all():
                        queasy_exist = True

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == reslin_queasy.number3) &  (Artikel.departement == reslin_queasy.resnr)).first()

                        argt_line = db_session.query(Argt_line).filter(
                                (Argt_line.argtnr == select_list.argtnr) &  (Argt_line.argt_artnr == artikel.artnr) &  (Argt_line.departement == artikel.departement)).first()

                        if ci_date <= reslin_queasy.date2 and do_it:
                            t_viewrates_line = T_viewrates_line()
                            t_viewrates_line_list.append(t_viewrates_line)

                            t_viewrates_line.prcode = queasy.char1
                            t_viewrates_line.argt = arrangement
                            t_viewrates_line.rmtype = zimkateg.kurzbez
                            t_viewrates_line.datum = to_string(reslin_queasy.date1, "99/99/99") +\
                                    " - " + to_string(reslin_queasy.date2, "99/99/99")
                            t_viewrates_line.str_aci = artikel.bezeich
                            t_viewrates_line.aci = "rate : " + trim(to_string(reslin_queasy.deci1, ">>>,>>>,>>9.99"))

                            if argt_line:
                                t_viewrates_line.str_rate_aci = "Posted : " + to_string(argt_line.fakt_modus, "9")

                                if argt_line.fakt_modus == 6:
                                    t_viewrates_line.str_rate_aci = t_viewrates_line.str_rate_aci + "/" + to_string(argt_line.intervall, "9")
                                else:
                                    t_viewrates_line.adult_rate = "rate Include : " + to_string(argt_line.kind1, "Yes/No")
                                t_viewrates_line.child_rate = "Optional : " + to_string(argt_line.kind2, "Yes/No")

                                if argt_line.betriebsnr == 0:
                                    t_viewrates_line.infant_rate = "Qty Always 1 : No"
                                else:
                                    t_viewrates_line.infant_rate = "Qty Always 1 : Yes"

                    if not queasy_exist:

                        for argt_line in db_session.query(Argt_line).filter(
                                (Argt_line.argtnr == argt1)).all():

                            artikel = db_session.query(Artikel).filter(
                                    (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()
                            t_viewrates_line = T_viewrates_line()
                            t_viewrates_line_list.append(t_viewrates_line)

                            t_viewrates_line.prcode = queasy.char1
                            t_viewrates_line.argt = arrangement
                            t_viewrates_line.rmtype = zimkateg.kurzbez

                            if argt_line.vt_percnt == 0:
                                t_viewrates_line.datum = "" + " - " + ""
                                t_viewrates_line.str_aci = artikel.bezeich
                                t_viewrates_line.aci = "Adult rate : " + trim(to_string(argt_line.betrag, ">>>,>>>,>>9.99"))
                                t_viewrates_line.str_rate_aci = "Posted : " + to_string(argt_line.fakt_modus, "9")

                            elif argt_line.vt_percnt == 1:
                                t_viewrates_line.datum = "" + " - " + ""
                                t_viewrates_line.str_aci = artikel.bezeich
                                t_viewrates_line.aci = "Child rate : " + trim(to_string(argt_line.betrag, ">>>,>>>,>>9.99"))
                                t_viewrates_line.str_rate_aci = "Posted : " + to_string(argt_line.fakt_modus, "9")

                            elif argt_line.vt_percnt == 2:
                                t_viewrates_line.datum = "" + " - " + ""
                                t_viewrates_line.str_aci = artikel.bezeich
                                t_viewrates_line.aci = "Infant rate : " + trim(to_string(argt_line.betrag, ">>>,>>>,>>9.99"))
                                t_viewrates_line.str_rate_aci = "Posted : " + to_string(argt_line.fakt_modus, "9")

                            if argt_line.fakt_modus == 6:
                                t_viewrates_line.str_rate_aci = t_viewrates_line.str_rate_aci + "/" + to_string(argt_line.intervall, "9")
                            else:
                                t_viewrates_line.adult_rate = "rate Include : " + to_string(argt_line.kind1, "Yes/No")
                            t_viewrates_line.child_rate = "Optional : " + to_string(argt_line.kind2, "Yes/No")

                            if argt_line.betriebsnr == 0:
                                t_viewrates_line.infant_rate = "Qty Always 1 : No"
                            else:
                                t_viewrates_line.infant_rate = "Qty Always 1 : Yes"

    def create_selectlist():

        nonlocal comments, t_viewrates_list, t_viewrates_line_list, ci_date, current_counter, lvcarea, queasy, htparam, prmarket, prtable, arrangement, zimkateg, waehrung, ratecode, reslin_queasy, artikel, argt_line, guest, guest_pr
        nonlocal qsy


        nonlocal t_viewrates, t_viewrates_line, select_list, qsy
        nonlocal t_viewrates_list, t_viewrates_line_list, select_list_list

        i:int = 0
        length_str:int = 0
        help_str:str = ""
        product_str:str = ""
        select_list_list.clear()
        for i in range(1,99 + 1) :

            if prtable.product[i - 1] != 0:
                select_list = Select_list()
                select_list_list.append(select_list)

                product_str = to_string(prtable.product[i - 1])

                if len(product_str) == 3:
                    select_list.zikatnr = to_int(substring(product_str, 0, 1))
                    select_list.argtnr = to_int(substring(product_str, 1))

                elif len(product_str) == 4:
                    select_list.zikatnr, select_list.argtnr = get_zikat_argt(prtable.product[i - 1])

                    if select_list.zikatnr == 0 or select_list.argtnr == 0:
                        select_list_list.remove(select_list)

                elif len(product_str) == 5:
                    select_list.zikatnr = to_int(substring(product_str, 0, 2))
                    select_list.argtnr = to_int(substring(product_str, 2))

                elif len(product_str) == 6:
                    select_list.zikatnr = to_int(substring(product_str, 1, 2))
                    select_list.argtnr = to_int(substring(product_str, 3))

                if select_list.zikatnr >= 91:
                    select_list.zikatnr = select_list.zikatnr - 90

    def get_zikat_argt(curr_product:int):

        nonlocal comments, t_viewrates_list, t_viewrates_line_list, ci_date, current_counter, lvcarea, queasy, htparam, prmarket, prtable, arrangement, zimkateg, waehrung, ratecode, reslin_queasy, artikel, argt_line, guest, guest_pr
        nonlocal qsy


        nonlocal t_viewrates, t_viewrates_line, select_list, qsy
        nonlocal t_viewrates_list, t_viewrates_line_list, select_list_list

        i_zikatnr = 0
        i_argtnr = 0
        i:int = 0
        j:int = 0
        k:int = 0
        n:int = 0
        num_found1:int = 0
        num_found2:int = 0
        i_zikatnr1:int = 0
        i_argtnr1:int = 0
        i_zikatnr2:int = 0
        i_argtnr2:int = 0
        found1:bool = False
        found2:bool = False
        str:str = ""

        def generate_inner_output():
            return i_zikatnr, i_argtnr

        if curr_product >= 90000:
            num_found1 = 0
            num_found2 = 0
            str = to_string(curr_product)
            i_zikatnr1 = to_int(substring(str, 0, 2)) - 90
            i_argtnr1 = to_int(substring(str, 2))

        elif curr_product >= 10000:
            num_found1 = 0
            num_found2 = 0
            str = to_string(curr_product)
            i_zikatnr1 = to_int(substring(str, 0, 2))
            i_argtnr1 = to_int(substring(str, 2))


        else:
            num_found1 = 0
            num_found2 = 0
            str = to_string(curr_product)
            i_zikatnr1 = to_int(substring(str, 0, 1))
            i_argtnr1 = to_int(substring(str, 1))

        if i_argtnr1 >= 100:
            for j in range(1,99 + 1) :

                if i_zikatnr1 == prtable.zikatnr[j - 1]:
                    num_found1 = num_found1 + 1
                    j = 999
            for j in range(1,99 + 1) :

                if i_argtnr1 == prtable.argtnr[j - 1]:
                    num_found1 = num_found1 + 2
                    j = 999
        i_zikatnr2 = to_int(substring(str, 0, 2))
        i_argtnr2 = to_int(substring(str, 2))


        for j in range(1,99 + 1) :

            if i_zikatnr2 == prtable.zikatnr[j - 1]:
                num_found2 = num_found2 + 1
                j = 999
        for j in range(1,99 + 1) :

            if i_argtnr2 == prtable.argtnr[j - 1]:
                num_found2 = num_found2 + 2
                j = 999

        if num_found1 == 3 and num_found2 != 3:
            i_zikatnr = i_zikatnr1
            i_argtnr = i_zikatnr1

            return generate_inner_output()

        elif num_found1 != 3 and num_found2 == 3:
            i_zikatnr = i_zikatnr2
            i_argtnr = i_zikatnr2

            return generate_inner_output()
        else:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.CODE == prtable.prcode) &  (Ratecode.zikatnr == i_zikatnr1) &  (Ratecode.argtnr == i_argtnr1)).first()

            if ratecode:
                i_zikatnr = i_zikatnr1
                i_argtnr = i_zikatnr1

                return generate_inner_output()

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.CODE == prtable.prcode) &  (Ratecode.zikatnr == i_zikatnr2) &  (Ratecode.argtnr == i_argtnr2)).first()

            if ratecode:
                i_zikatnr = i_zikatnr2
                i_argtnr = i_zikatnr2


        return generate_inner_output()

    if gastnr > 0:
        create_list()
    else:
        create_list0()

    return generate_output()