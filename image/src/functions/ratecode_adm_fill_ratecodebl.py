from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.link_ratecodebl import link_ratecodebl
from functions.calc_servvat import calc_servvat
from models import Ratecode, Queasy, Htparam, Zimkateg, Bediener, Res_history, Guest_pr, Guest, Arrangement, Artikel, Waehrung

def ratecode_adm_fill_ratecodebl(user_init:str, prcode:str, market_nr:int, zikatnr:int, argtnr:int, book_room:int, comp_room:int, max_room:int, early_discount:[Early_discount], kickback_discount:[Kickback_discount], stay_pay:[Stay_pay], p_list:[P_list]):
    ci_date:date = None
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    parent_code:str = ""
    adjust_value:decimal = 0
    in_percent:bool = False
    chg_allot:bool = False
    iftask:str = ""
    mestoken:str = ""
    mesvalue:str = ""
    tokcounter:int = 0
    cat_flag:bool = False
    bef_start:date = None
    bef_end:date = None
    bef_pax:int = 0
    bef_rate:decimal = 0
    tax_included:bool = False
    ratecode = queasy = htparam = zimkateg = bediener = res_history = guest_pr = guest = arrangement = artikel = waehrung = None

    p_list = early_discount = kickback_discount = stay_pay = child_list = child_ratecode = q_list = r_list = qsy = rbuff = q_curr = tb3buff = pcode1 = bqueasy = zbuff = tqueasy = None

    p_list_list, P_list = create_model_like(Ratecode, {"s_recid":int})
    early_discount_list, Early_discount = create_model("Early_discount", {"disc_rate":decimal, "min_days":int, "min_stay":int, "max_occ":int, "from_date":date, "to_date":date})
    kickback_discount_list, Kickback_discount = create_model("Kickback_discount", {"disc_rate":decimal, "max_days":int, "min_stay":int, "max_occ":int})
    stay_pay_list, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})
    child_list_list, Child_list = create_model("Child_list", {"child_code":str, "true_child":bool}, {"true_child": True})
    child_ratecode_list, Child_ratecode = create_model_like(Ratecode)
    q_list_list, Q_list = create_model("Q_list", {"rcode":str, "dcode":str})
    r_list_list, R_list = create_model_like(Q_list)

    Qsy = Queasy
    Rbuff = Ratecode
    Q_curr = Queasy
    Tb3buff = Ratecode
    Pcode1 = Ratecode
    Bqueasy = Queasy
    Zbuff = Zimkateg
    Tqueasy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy
        nonlocal p_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, q_list_list, r_list_list
        return {}

    def create_child_list():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy
        nonlocal p_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, q_list_list, r_list_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (not Queasy.logi2) &  (num_entries(Queasy.char3, ";") > 2) &  (entry(1, Queasy.char3, ";") == (prcode).lower())).all():
            child_list = Child_list()
            child_list_list.append(child_list)

            child_list.child_code = queasy.char1

            for ratecode in db_session.query(Ratecode).filter(
                    (Ratecode.CODE == queasy.char1) &  (Ratecode.endperiode >= ci_date)).all():

                rbuff = db_session.query(Rbuff).filter(
                        (Rbuff.marknr == ratecode.marknr) &  (func.lower(Rbuff.code) == (prcode).lower()) &  (Rbuff.argtnr == ratecode.argtnr) &  (Rbuff.zikatnr == ratecode.zikatnr) &  (Rbuff.erwachs == ratecode.erwachs) &  (Rbuff.kind1 == ratecode.kind1) &  (Rbuff.kind2 == ratecode.kind2) &  (Rbuff.wday == ratecode.wday) &  (Rbuff.startperiode == ratecode.startperiode) &  (Rbuff.endperiode == ratecode.endperiode)).first()

                if not rbuff:
                    child_list.true_child = False


                    break

    def fill_ratecode():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy
        nonlocal p_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, q_list_list, r_list_list

        to_date:date = 01/01/1990
        ori_allot:int = 0
        log_flag:str = ""
        Pcode1 = Ratecode

        if p_list.s_recid != 0:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode._recid == p_list.s_recid)).first()

            if ratecode:
                bef_start = ratecode.startperiode
                bef_end = ratecode.endperiode
                bef_pax = ratecode.erwach
                bef_rate = ratecode.zipreis


        else:
            ratecode = Ratecode()
        db_session.add(ratecode)


        if p_list.s_recid != 0:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (func.lower(Queasy.char1) == (prcode).lower())).first()

            if num_entries(queasy.char3, ";") > 2:
                ratecode.startperiode = p_list.startperiode
                ratecode.endperiode = p_list.endperiode

                return

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == p_list.zikatnr)).first()

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Modify Contract Rate, Code: " + prcode + " RmType : " + zimkateg.kurzbez +\
                    ", FROM : start:" + to_string(bef_start) + "|end:" + to_string(bef_end) + "|adult:" + to_string(bef_pax) + "|rate:" + to_string(bef_rate) +\
                    ", TO : start:" + to_string(p_list.startperiode) + "|end:" + to_string(p_list.endperiode) + "|adult:" + to_string(p_list.erwach) + "|rate:" + to_string(p_list.zipreis)


            res_history.action = "RateCode"

            res_history = db_session.query(Res_history).first()

        buffer_copy(p_list, ratecode,except_fields=["p_list.argtnr","p_list.zikatnr"])
        ratecode.marknr = market_nr
        ratecode.code = prcode
        ratecode.argtnr = argtnr
        ratecode.zikatnr = zikatnr
        ratecode.char1[0] = ""
        ratecode.char1[1] = ""
        ratecode.char1[2] = ""
        ratecode.char1[3] = ""
        ratecode.char1[4] = user_init

        if book_room > 0:
            ratecode.char1[3] = to_string(book_room) + ";" + to_string(comp_room) + ";" + to_string(max_room) + ";"
        else:
            ratecode.char1[3] = ""

        for early_discount in query(early_discount_list, filters=(lambda early_discount :early_discount.disc_rate != 0)):
            ratecode.char1[0] = ratecode.char1[0] + to_string(early_discount.disc_rate * 100) + "," + to_string(early_discount.min_days) + "," + to_string(early_discount.min_stay) + "," + to_string(early_discount.max_occ) + ","

            if early_discount.from_date != None:
                ratecode.char1[0] = ratecode.char1[0] + to_string(get_year(early_discount.from_date) , "9999") + to_string(get_month(early_discount.from_date) , "99") + to_string(get_day(early_discount.from_date) , "99") + ","
            else:
                ratecode.char1[0] = ratecode.char1[0] + " ,"

            if early_discount.to_date != None:
                ratecode.char1[0] = ratecode.char1[0] + to_string(get_year(early_discount.to_date) , "9999") + to_string(get_month(early_discount.to_date) , "99") + to_string(get_day(early_discount.to_date) , "99") + ";"
            else:
                ratecode.char1[0] = ratecode.char1[0] + " ;"

        for kickback_discount in query(kickback_discount_list, filters=(lambda kickback_discount :kickback_discount.disc_rate != 0)):
            ratecode.char1[1] = ratecode.char1[1] + to_string(kickback_discount.disc_rate * 100) + "," + to_string(kickback_discount.max_days) + "," + to_string(kickback_discount.min_stay) + "," + to_string(kickback_discount.max_occ) + ";"

        for stay_pay in query(stay_pay_list, filters=(lambda stay_pay :stay_pay.stay != 0)):
            ratecode.char1[2] = ratecode.char1[2] + to_string(get_year(stay_pay.f_date) , "9999") + to_string(get_month(stay_pay.f_date) , "99") + to_string(get_day(stay_pay.f_date) , "99") + "," + to_string(get_year(stay_pay.t_date) , "9999") + to_string(get_month(stay_pay.t_date) , "99") + to_string(get_day(stay_pay.t_date) , "99") + "," + to_string(stay) + "," + to_string(pay) + ";"

        for pcode1 in db_session.query(Pcode1).filter(
                (func.lower(Pcode1.code) == (prcode).lower())).all():

            if pcode1.endperiode > to_date:
                to_date = pcode1.endperiode

        if to_date != 01/01/1990:

            for guest_pr in db_session.query(Guest_pr).filter(
                    (func.lower(Guest_pr.code) == (prcode).lower())).all():

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == guest_pr.gastnr)).first()
                guest.endperiode = to_date

                guest = db_session.query(Guest).first()

        tb3buff = db_session.query(Tb3buff).filter(
                (tb3Buff._recid == ratecode._recid)).first()
        buffer_copy(ratecode, p_list)

        if p_list.s_recid == 0:
            p_list.s_recid = to_int(ratecode._recid)

    def update_child_ratecode():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy
        nonlocal p_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, q_list_list, r_list_list

        beg_datum:date = None
        end_datum:date = None
        Rbuff = Ratecode

        for child_list in query(child_list_list, filters=(lambda child_list :child_list.true_child == False)):

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (Queasy.char1 == child_list.child_code)).first()
            parent_code = entry(1, queasy.char3, ";")
            in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
            adjust_value = decimal.Decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

            for ratecode in db_session.query(Ratecode).filter(
                    (Ratecode.marknr == tb3Buff.marknr) &  (Ratecode.code == child_list.child_code) &  (Ratecode.argtnr == tb3Buff.argtnr) &  (Ratecode.zikatnr == tb3Buff.zikatnr) &  (Ratecode.erwachs == tb3Buff.erwachs) &  (Ratecode.kind1 == tb3Buff.kind1) &  (Ratecode.kind2 == tb3Buff.kind2) &  (Ratecode.wday == tb3Buff.wday) &  (not Ratecode.endperiode < tb3Buff.startperiode) &  (not Ratecode.startperiode > tb3Buff.endperiode)).all():

                if ratecode.startperiode < tb3Buff.startperiode:

                    if ratecode.endperiode <= tb3Buff.endperiode:
                        end_datum = ratecode.endperiode
                        ratecode.endperiode = tb3Buff.startperiode - 1


                        child_ratecode = Child_ratecode()
                        child_ratecode_list.append(child_ratecode)

                        buffer_copy(tb3Buff, child_ratecode,except_fields=["CODE","endperiode"])
                        child_ratecode.CODE = child_list.child_code
                        child_ratecode.endperiode = end_datum


                        set_child_rate()
                    else:
                        child_ratecode = Child_ratecode()
                        child_ratecode_list.append(child_ratecode)

                        buffer_copy(ratecode, child_ratecode,except_fields=["startperiode"])
                        ratecode.endperiode = tb3Buff.startperiode - 1
                        child_ratecode.startperiode = tb3Buff.endperiode + 1

                elif (ratecode.startperiode >= tb3Buff.startperiode) and (ratecode.endperiode <= tb3Buff.endperiode):
                    set_child_rate_1()

                elif (ratecode.startperiode >= tb3Buff.startperiode) and (ratecode.endperiode > tb3Buff.endperiode):
                    beg_datum = ratecode.startperiode
                    ratecode.startperiode = tb3Buff.endperiode + 1


                    child_ratecode = Child_ratecode()
                    child_ratecode_list.append(child_ratecode)

                    buffer_copy(tb3Buff, child_ratecode,except_fields=["CODE","startperiode"])
                    child_ratecode.CODE = child_list.child_code
                    child_ratecode.startperiode = beg_datum


                    set_child_rate()

        for child_ratecode in query(child_ratecode_list):
            ratecode = Ratecode()
            db_session.add(ratecode)

            buffer_copy(child_ratecode, ratecode)
            child_ratecode_list.remove(child_ratecode)

        for child_list in query(child_list_list, filters=(lambda child_list :child_list.true_child)):

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (Queasy.char1 == child_list.child_code)).first()
            parent_code = entry(1, queasy.char3, ";")
            in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
            adjust_value = decimal.Decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100


            get_output(link_ratecodebl(child_list.child_code, parent_code, queasy.char3, in_percent, adjust_value))

    def set_child_rate():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy
        nonlocal p_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, q_list_list, r_list_list

        rounded_rate:decimal = 0

        if in_percent:
            child_ratecode.zipreis = tb3buff.zipreis * (1 + adjust_value * 0.01)

            if round_betrag != 0 and child_ratecode.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(child_ratecode.zipreis)
                child_ratecode.zipreis = rounded_rate
        else:
            child_ratecode.zipreis = tb3buff.zipreis + adjust_value

    def set_child_rate_1():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy
        nonlocal p_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, q_list_list, r_list_list

        rounded_rate:decimal = 0

        if in_percent:
            ratecode.zipreis = tb3buff.zipreis * (1 + adjust_value * 0.01)

            if round_betrag != 0 and ratecode.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(ratecode.zipreis)
                ratecode.zipreis = rounded_rate
        else:
            ratecode.zipreis = tb3buff.zipreis + adjust_value

    def update_bookengine_config():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3buff, pcode1, bqueasy, zbuff, tqueasy
        nonlocal p_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, q_list_list, r_list_list

        datum:date = None
        cm_gastno:int = 0
        roomnr:int = 0
        dyna:str = ""
        loopi:int = 0
        currency:str = ""
        serv:decimal = 0
        vat:decimal = 0
        str:str = ""
        Bqueasy = Queasy
        Zbuff = Zimkateg
        Tqueasy = Queasy

        zbuff = db_session.query(Zbuff).filter(
                (Zbuff.zikatnr == p_list.zikatnr)).first()

        if cat_flag:
            roomnr = zbuff.typ

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 152) &  (Queasy.number1 == roomnr)).first()

            if queasy:
                str = queasy.char1
        else:
            roomnr = zbuff.zikatnr
            str = zbuff.kurzbez

        for qsy in db_session.query(Qsy).filter(
                (Qsy.key == 2) &  (Qsy.logi2)).all():

            for ratecode in db_session.query(Ratecode).filter(
                    (Ratecode.CODE == qsy.char1)).all():
                iftask = ratecode.char1[4]
                for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                    if mestoken == "RC":

                        if mesvalue.lower()  == (prcode).lower() :
                            dyna = dyna + qsy.char1 + ";"


    p_list = query(p_list_list, first=True)

    qsy = db_session.query(Qsy).filter(
            (Qsy.key == 152)).first()

    if qsy:
        cat_flag = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1013)).first()

    if htparam.feldtyp == 1:
        round_betrag = htparam.finteger
        length_round = len(to_string(round_betrag))

    elif htparam.feldtyp == 5 and num_entries(htparam.fchar, ";") > 1:
        round_betrag = to_int(entry(0, htparam.fchar, ";"))
        length_round = len(to_string(round_betrag))
        round_method = to_int(entry(1, htparam.fchar, ";"))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 127)).first()

    if htparam:
        tax_included = htparam.flogical
    create_child_list()
    fill_ratecode()
    update_child_ratecode()
    update_bookengine_config()

    if dyna != "":
        for tokcounter in range(1,num_entries(dyna, ";")  + 1) :
            mesvalue = trim(entry(tokcounter - 1, dyna, ";"))

            if mesvalue != "":
                for datum in range(p_list.startperiode,p_list.endperiode + 1) :

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 170) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (Queasy.char1 == mesvalue) &  (Queasy.number2 == p_list.erwachs) &  (Queasy.number3 == p_list.kind1)).first()

                    if queasy:

                        qsy = db_session.query(Qsy).filter(
                                (Qsy.key == 170) &  (Qsy.date1 == datum) &  (Qsy.number1 == roomnr) &  (Qsy.char1 == mesvalue) &  (Qsy.number2 == p_list.erwachs) &  (Qsy.number3 == p_list.kind1)).first()

                        if qsy and qsy.deci1 != p_list.zipreis and qsy.logi1 == False and qsy.logi2 == False:

                            bqueasy = db_session.query(Bqueasy).filter(
                                    (Bqueasy._recid == qsy._recid)).first()

                            if bqueasy:
                                bqueasy.logi2 = True

                                bqueasy = db_session.query(Bqueasy).first()


                    elif not queasy:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 161) &  (entry(0, Queasy.char1, ";") == mesvalue) &  (entry(2, Queasy.char1, ";") == (str).lower())).first()
                        while None != queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 170
                            queasy.date1 = datum
                            queasy.char1 = mesvalue
                            queasy.number1 = roomnr
                            queasy.number2 = p_list.erwachs
                            queasy.number3 = p_list.kind1
                            queasy.logi2 = True
                            queasy.char2 = p_list.CODE

                            arrangement = db_session.query(Arrangement).filter(
                                    (Arrangement.argtnr == p_list.argtnr)).first()

                            if arrangement:

                                artikel = db_session.query(Artikel).filter(
                                        (Artikel.artnr == arrangement.argt_artikelnr)).first()

                                if artikel:
                                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                            if tax_included:
                                queasy.deci1 = p_list.zipreis
                            else:
                                queasy.deci1 = round(decimal.Decimal(p_list.zipreis * (1 + serv + vat)) , 0)

                            bqueasy = db_session.query(Bqueasy).filter(
                                    (Bqueasy.key == 18) &  (Bqueasy.number1 == market_nr)).first()

                            if bqueasy:

                                waehrung = db_session.query(Waehrung).filter(
                                        (Waehrung.wabkurz == bqueasy.char3)).first()

                            if waehrung:

                                q_curr = db_session.query(Q_curr).filter(
                                        (Q_curr.char1 == waehrung.wabkurz) &  (Q_curr.key == 164) &  (Q_curr.char2 != "")).first()

                                if q_curr:
                                    currency = q_curr.char2
                                else:
                                    currency = "IDR"
                            else:
                                currency = "IDR"
                            queasy.char3 = currency

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 161) &  (entry(0, Queasy.char1, ";") == mesvalue) &  (entry(2, Queasy.char1, ";") == (str).lower())).first()
    else:
        for datum in range(p_list.startperiode,p_list.endperiode + 1) :

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 170) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (func.lower(Queasy.char1) == (prcode).lower()) &  (Queasy.number2 == p_list.erwachs) &  (Queasy.number3 == p_list.kind1)).first()

            if queasy:

                qsy = db_session.query(Qsy).filter(
                        (Qsy.key == 170) &  (Qsy.date1 == datum) &  (Qsy.number1 == roomnr) &  (func.lower(Qsy.char1) == (prcode).lower()) &  (Qsy.number2 == p_list.erwachs) &  (Qsy.number3 == p_list.kind1)).first()

                if qsy and qsy.deci1 != p_list.zipreis and qsy.logi1 == False and qsy.logi2 == False:

                    bqueasy = db_session.query(Bqueasy).filter(
                            (Bqueasy._recid == qsy._recid)).first()

                    if bqueasy:
                        bqueasy.logi2 = True

                        bqueasy = db_session.query(Bqueasy).first()


            elif not queasy:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 161) &  (entry(0, Queasy.char1, ";") == (prcode).lower()) &  (entry(2, Queasy.char1, ";") == (str).lower())).first()
                while None != queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 170
                    queasy.date1 = datum
                    queasy.char1 = prcode
                    queasy.number1 = roomnr
                    queasy.number2 = p_list.erwachs
                    queasy.number3 = p_list.kind1
                    queasy.logi2 = True

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement.argtnr == p_list.argtnr)).first()

                    if arrangement:

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == arrangement.argt_artikelnr)).first()

                        if artikel:
                            serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                    if tax_included:
                        queasy.deci1 = p_list.zipreis
                    else:
                        queasy.deci1 = round(decimal.Decimal(p_list.zipreis * (1 + serv + vat)) , 0)

                    bqueasy = db_session.query(Bqueasy).filter(
                            (Bqueasy.key == 18) &  (Bqueasy.number1 == market_nr)).first()

                    if bqueasy:

                        waehrung = db_session.query(Waehrung).filter(
                                (Waehrung.wabkurz == bqueasy.char3)).first()

                    if waehrung:

                        q_curr = db_session.query(Q_curr).filter(
                                (Q_curr.char1 == waehrung.wabkurz) &  (Q_curr.key == 164) &  (Q_curr.char2 != "")).first()

                        if q_curr:
                            currency = q_curr.char2
                        else:
                            currency = "IDR"
                    else:
                        currency = "IDR"
                    queasy.char3 = currency

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 161) &  (entry(0, Queasy.char1, ";") == mesvalue) &  (entry(2, Queasy.char1, ";") == (str).lower())).first()

    return generate_output()