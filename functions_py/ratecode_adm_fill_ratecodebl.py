#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 31/7/2025
# gitlab: 313
# add if available
# Rd 15/8/2025, erwach -> erwachs
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.link_ratecodebl import link_ratecodebl
from functions.calc_servvat import calc_servvat
from models import Ratecode, Queasy, Htparam, Zimkateg, Bediener, Res_history, Guest_pr, Guest, Arrangement, Artikel, Waehrung

early_discount_data, Early_discount = create_model("Early_discount", {"disc_rate":Decimal, "min_days":int, "min_stay":int, "max_occ":int, "from_date":date, "to_date":date})
kickback_discount_data, Kickback_discount = create_model("Kickback_discount", {"disc_rate":Decimal, "max_days":int, "min_stay":int, "max_occ":int})
stay_pay_data, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})
p_list_data, P_list = create_model_like(Ratecode, {"s_recid":int})

def ratecode_adm_fill_ratecodebl(user_init:string, prcode:string, market_nr:int, zikatnr:int, argtnr:int, book_room:int, comp_room:int, max_room:int, early_discount_data:[Early_discount], kickback_discount_data:[Kickback_discount], stay_pay_data:[Stay_pay], p_list_data:[P_list]):

    prepare_cache ([Queasy, Htparam, Zimkateg, Bediener, Res_history, Guest_pr, Guest, Arrangement, Artikel, Waehrung])

    ci_date:date = None
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    parent_code:string = ""
    adjust_value:Decimal = to_decimal("0.0")
    in_percent:bool = False
    chg_allot:bool = False
    iftask:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    tokcounter:int = 0
    cat_flag:bool = False
    bef_start:date = None
    bef_end:date = None
    bef_pax:int = 0
    bef_rate:Decimal = to_decimal("0.0")
    tax_included:bool = False
    ratecode = queasy = htparam = zimkateg = bediener = res_history = guest_pr = guest = arrangement = artikel = waehrung = None

    p_list = early_discount = kickback_discount = stay_pay = child_list = child_ratecode = q_list = r_list = qsy = rbuff = q_curr = tb3_buff = None

    child_list_data, Child_list = create_model("Child_list", {"child_code":string, "true_child":bool, "argt_no":int, "zikat_no":int}, {"true_child": True})
    child_ratecode_data, Child_ratecode = create_model_like(Ratecode)
    q_list_data, Q_list = create_model("Q_list", {"rcode":string, "dcode":string})
    r_list_data, R_list = create_model_like(Q_list)

    Qsy = create_buffer("Qsy",Queasy)
    Rbuff = create_buffer("Rbuff",Ratecode)
    Q_curr = create_buffer("Q_curr",Queasy)
    Tb3_buff = create_buffer("Tb3_buff",Ratecode)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal user_init, prcode, market_nr, zikatnr, argtnr, book_room, comp_room, max_room
        nonlocal qsy, rbuff, q_curr, tb3_buff


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3_buff
        nonlocal child_list_data, child_ratecode_data, q_list_data, r_list_data
        # Rd 15/8/2025
        db_session.commit()
        return {"p-list": p_list_data}

    def create_child_list():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal user_init, prcode, market_nr, zikatnr, argtnr, book_room, comp_room, max_room
        nonlocal qsy, rbuff, q_curr, tb3_buff


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3_buff
        nonlocal child_list_data, child_ratecode_data, q_list_data, r_list_data

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2) & not_ (Queasy.logi2) & (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (prcode).lower())).order_by(Queasy._recid).all():
            child_list = Child_list()
            child_list_data.append(child_list)

            child_list.child_code = queasy.char1


    def fill_ratecode():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal user_init, prcode, market_nr, zikatnr, argtnr, book_room, comp_room, max_room
        nonlocal qsy, rbuff, q_curr, tb3_buff


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3_buff
        nonlocal child_list_data, child_ratecode_data, q_list_data, r_list_data

        to_date:date = None
        pcode1 = None
        ori_allot:int = 0
        log_flag:string = ""
        tmp_kurzbez:string = ""
        Pcode1 =  create_buffer("Pcode1",Ratecode)
        to_date = date_mdy(1, 1, 1990)

        if p_list.s_recid != 0:

            ratecode = get_cache (Ratecode, {"_recid": [(eq, p_list.s_recid)]})

            if ratecode:
                bef_start = ratecode.startperiode
                bef_end = ratecode.endperiode
                # Rd 15/8/2025
                # erwach -> erwachs
                bef_pax = ratecode.erwachs
                bef_rate =  to_decimal(ratecode.zipreis)


        else:
            ratecode = Ratecode()
            db_session.add(ratecode)
            # Rd 15/8/2025
            db_session.commit()


        if p_list.s_recid != 0:

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, prcode)]})

            if num_entries(queasy.char3, ";") > 2:
                ratecode.startperiode = p_list.startperiode
                ratecode.endperiode = p_list.endperiode

                return

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, p_list.zikatnr)]})

        if zimkateg:
            tmp_kurzbez = zimkateg.kurzbez
        else:
            tmp_kurzbez = ""

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Modify Contract Rate, Code: " + prcode + " RmType : " + tmp_kurzbez +\
                    ", FROM : start:" + to_string(bef_start) + "|end:" + to_string(bef_end) + "|adult:" + to_string(bef_pax) + "|rate:" + to_string(bef_rate) +\
                    ", TO : start:" + to_string(p_list.startperiode) + "|end:" + to_string(p_list.endperiode) + "|adult:" + to_string(p_list.erwachs) + "|rate:" + to_string(p_list.zipreis)


            res_history.action = "RateCode"
            # Rd 15/8/2025
            db_session.commit()
            pass
            pass

        # buffer_copy(p_list, ratecode,except_fields=["p_list.argtnr","p_list.zikatnr"])
        # add if available
        if p_list is not None and ratecode is not None:
            buffer_copy(p_list, ratecode, except_fields=["argtnr", "zikatnr"])
            
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

            for early_discount in query(early_discount_data, filters=(lambda early_discount: early_discount.disc_rate != 0)):
                ratecode.char1[0] = ratecode.char1[0] + to_string(early_discount.disc_rate * 100) + "," + to_string(early_discount.min_days) + "," + to_string(early_discount.min_stay) + "," + to_string(early_discount.max_occ) + ","

                if early_discount.from_date != None:
                    ratecode.char1[0] = ratecode.char1[0] + to_string(get_year(early_discount.from_date) , "9999") + to_string(get_month(early_discount.from_date) , "99") + to_string(get_day(early_discount.from_date) , "99") + ","
                else:
                    ratecode.char1[0] = ratecode.char1[0] + " ,"

                if early_discount.to_date != None:
                    ratecode.char1[0] = ratecode.char1[0] + to_string(get_year(early_discount.to_date) , "9999") + to_string(get_month(early_discount.to_date) , "99") + to_string(get_day(early_discount.to_date) , "99") + ";"
                else:
                    ratecode.char1[0] = ratecode.char1[0] + " ;"

            for kickback_discount in query(kickback_discount_data, filters=(lambda kickback_discount: kickback_discount.disc_rate != 0)):
                ratecode.char1[1] = ratecode.char1[1] + to_string(kickback_discount.disc_rate * 100) + "," + to_string(kickback_discount.max_days) + "," + to_string(kickback_discount.min_stay) + "," + to_string(kickback_discount.max_occ) + ";"

            for stay_pay in query(stay_pay_data, filters=(lambda stay_pay: stay_pay.stay != 0)):
                ratecode.char1[2] = ratecode.char1[2] + to_string(get_year(stay_pay.f_date) , "9999") + to_string(get_month(stay_pay.f_date) , "99") + to_string(get_day(stay_pay.f_date) , "99") + "," + to_string(get_year(stay_pay.t_date) , "9999") + to_string(get_month(stay_pay.t_date) , "99") + to_string(get_day(stay_pay.t_date) , "99") + "," + to_string(stay) + "," + to_string(pay) + ";"

            for pcode1 in db_session.query(Pcode1).filter(
                    (Pcode1.code == (prcode).lower())).order_by(Pcode1._recid).all():

                if pcode1.endperiode != None and to_date != None:

                    if pcode1.endperiode > to_date:
                        to_date = pcode1.endperiode

            if to_date != date_mdy(1, 1, 1990):

                for guest_pr in db_session.query(Guest_pr).filter(
                        (Guest_pr.code == (prcode).lower())).order_by(Guest_pr._recid).all():

                    guest = get_cache (Guest, {"gastnr": [(eq, guest_pr.gastnr)]})
                    guest.endperiode = to_date
                    pass

            tb3_buff = db_session.query(Tb3_buff).filter(
                    (Tb3_buff._recid == ratecode._recid)).first()
            buffer_copy(ratecode, p_list)

            if p_list.s_recid == 0:
                p_list.s_recid = to_int(ratecode._recid)


    def update_child_ratecode():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal user_init, prcode, market_nr, zikatnr, argtnr, book_room, comp_room, max_room
        nonlocal qsy, rbuff, q_curr, tb3_buff


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3_buff
        nonlocal child_list_data, child_ratecode_data, q_list_data, r_list_data

        beg_datum:date = None
        end_datum:date = None
        rbuff = None
        Rbuff =  create_buffer("Rbuff",Ratecode)

        for child_list in query(child_list_data, filters=(lambda child_list: child_list.true_child == False)):

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, child_list.child_code)]})
            parent_code = entry(1, queasy.char3, ";")
            in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
            adjust_value = to_decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

            for ratecode in db_session.query(Ratecode).filter(
                     (Ratecode.marknr == tb3_buff.marknr) & (Ratecode.code == child_list.child_code) & (Ratecode.argtnr == tb3_buff.argtnr) & (Ratecode.zikatnr == tb3_buff.zikatnr) & (Ratecode.erwachs == tb3_buff.erwachs) & (Ratecode.kind1 == tb3_buff.kind1) & (Ratecode.kind2 == tb3_buff.kind2) & (Ratecode.wday == tb3_buff.wday) & not_ (Ratecode.endperiode < tb3_buff.startperiode) & not_ (Ratecode.startperiode > tb3_buff.endperiode)).order_by(Ratecode._recid).all():

                if ratecode.startperiode < tb3_buff.startperiode:

                    if ratecode.endperiode <= tb3_buff.endperiode:
                        end_datum = ratecode.endperiode
                        ratecode.endperiode = tb3_buff.startperiode - timedelta(days=1)


                        child_ratecode = Child_ratecode()
                        child_ratecode_data.append(child_ratecode)

                        buffer_copy(tb3_buff, child_ratecode,except_fields=["CODE","endperiode"])
                        child_ratecode.code = child_list.child_code
                        child_ratecode.endperiode = end_datum


                        set_child_rate()
                    else:
                        child_ratecode = Child_ratecode()
                        child_ratecode_data.append(child_ratecode)

                        buffer_copy(ratecode, child_ratecode,except_fields=["startperiode"])
                        ratecode.endperiode = tb3_buff.startperiode - timedelta(days=1)
                        child_ratecode.startperiode = tb3_buff.endperiode + timedelta(days=1)

                elif (ratecode.startperiode >= tb3_buff.startperiode) and (ratecode.endperiode <= tb3_buff.endperiode):
                    set_child_rate_1()

                elif (ratecode.startperiode >= tb3_buff.startperiode) and (ratecode.endperiode > tb3_buff.endperiode):
                    beg_datum = ratecode.startperiode
                    ratecode.startperiode = tb3_buff.endperiode + timedelta(days=1)


                    child_ratecode = Child_ratecode()
                    child_ratecode_data.append(child_ratecode)

                    buffer_copy(tb3_buff, child_ratecode,except_fields=["CODE","startperiode"])
                    child_ratecode.code = child_list.child_code
                    child_ratecode.startperiode = beg_datum


                    set_child_rate()

        for child_ratecode in query(child_ratecode_data):
            ratecode = Ratecode()
            db_session.add(ratecode)

            buffer_copy(child_ratecode, ratecode)
            child_ratecode_data.remove(child_ratecode)
            # Rd 15/8/2025
            db_session.commit()

        for child_list in query(child_list_data, filters=(lambda child_list: child_list.true_child)):

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, child_list.child_code)]})
            parent_code = entry(1, queasy.char3, ";")
            in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
            adjust_value = to_decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100


            get_output(link_ratecodebl(child_list.child_code, parent_code, queasy.char3, in_percent, adjust_value))


    def set_child_rate():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal user_init, prcode, market_nr, zikatnr, argtnr, book_room, comp_room, max_room
        nonlocal qsy, rbuff, q_curr, tb3_buff


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3_buff
        nonlocal child_list_data, child_ratecode_data, q_list_data, r_list_data

        rounded_rate:Decimal = to_decimal("0.0")

        if in_percent:
            child_ratecode.zipreis =  to_decimal(tb3_buff.zipreis) * to_decimal((1) + to_decimal(adjust_value) * to_decimal(0.01))

            if round_betrag != 0 and child_ratecode.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(round_method, round_betrag, child_ratecode.zipreis)
                child_ratecode.zipreis =  to_decimal(rounded_rate)
        else:
            child_ratecode.zipreis =  to_decimal(tb3_buff.zipreis) + to_decimal(adjust_value)


    def set_child_rate_1():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal user_init, prcode, market_nr, zikatnr, argtnr, book_room, comp_room, max_room
        nonlocal qsy, rbuff, q_curr, tb3_buff


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3_buff
        nonlocal child_list_data, child_ratecode_data, q_list_data, r_list_data

        rounded_rate:Decimal = to_decimal("0.0")

        if in_percent:
            ratecode.zipreis =  to_decimal(tb3_buff.zipreis) * to_decimal((1) + to_decimal(adjust_value) * to_decimal(0.01))

            if round_betrag != 0 and ratecode.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(round_method, round_betrag, ratecode.zipreis)
                ratecode.zipreis =  to_decimal(rounded_rate)
        else:
            ratecode.zipreis =  to_decimal(tb3_buff.zipreis) + to_decimal(adjust_value)


    def update_bookengine_config():

        nonlocal ci_date, round_betrag, round_method, length_round, parent_code, adjust_value, in_percent, chg_allot, iftask, mestoken, mesvalue, tokcounter, cat_flag, bef_start, bef_end, bef_pax, bef_rate, tax_included, ratecode, queasy, htparam, zimkateg, bediener, res_history, guest_pr, guest, arrangement, artikel, waehrung
        nonlocal user_init, prcode, market_nr, zikatnr, argtnr, book_room, comp_room, max_room
        nonlocal qsy, rbuff, q_curr, tb3_buff


        nonlocal p_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, q_list, r_list, qsy, rbuff, q_curr, tb3_buff
        nonlocal child_list_data, child_ratecode_data, q_list_data, r_list_data

        bqueasy = None
        zbuff = None
        datum:date = None
        cm_gastno:int = 0
        roomnr:int = 0
        dyna:string = ""
        loopi:int = 0
        currency:string = ""
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        str:string = ""
        tqueasy = None
        Bqueasy =  create_buffer("Bqueasy",Queasy)
        Zbuff =  create_buffer("Zbuff",Zimkateg)
        Tqueasy =  create_buffer("Tqueasy",Queasy)

        zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, p_list.zikatnr)]})

        if cat_flag:
            roomnr = zbuff.typ

            queasy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, roomnr)]})

            if queasy:
                str = queasy.char1
        else:
            roomnr = zbuff.zikatnr
            str = zbuff.kurzbez

        for qsy in db_session.query(Qsy).filter(
                 (Qsy.key == 2) & (Qsy.logi2)).order_by(Qsy._recid).all():

            for ratecode in db_session.query(Ratecode).filter(
                     (Ratecode.code == qsy.char1)).order_by(Ratecode._recid).all():
                iftask = ratecode.char1[4]
                for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                    if mestoken == "RC":

                        if mesvalue.lower()  == (prcode).lower() :
                            dyna = dyna + qsy.char1 + ";"

        if dyna != "":
            for tokcounter in range(1,num_entries(dyna, ";")  + 1) :
                mesvalue = trim(entry(tokcounter - 1, dyna, ";"))

                if mesvalue != "":

                    if p_list.startperiode != None and p_list.endperiode != None:
                        for datum in date_range(p_list.startperiode,p_list.endperiode) :

                            queasy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, mesvalue)],"number2": [(eq, p_list.erwachs)],"number3": [(eq, p_list.kind1)]})

                            if queasy:

                                qsy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, mesvalue)],"number2": [(eq, p_list.erwachs)],"number3": [(eq, p_list.kind1)]})

                                if qsy and qsy.deci1 != p_list.zipreis and qsy.logi1 == False and qsy.logi2 == False:

                                    bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                                    if bqueasy:
                                        bqueasy.logi2 = True


                                        pass
                                        pass

                            elif not queasy:

                                queasy = db_session.query(Queasy).filter(
                                         (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str).lower())).first()
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
                                    queasy.char2 = p_list.code

                                    arrangement = get_cache (Arrangement, {"argtnr": [(eq, p_list.argtnr)]})

                                    if arrangement:

                                        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)]})

                                        if artikel:
                                            serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                                    if tax_included:
                                        queasy.deci1 =  to_decimal(p_list.zipreis)
                                    else:
                                        queasy.deci1 = to_decimal(round(to_decimal(p_list.zipreis * (1 + serv + vat)) , 0))

                                    bqueasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, market_nr)]})

                                    if bqueasy:

                                        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, bqueasy.char3)]})

                                    if waehrung:

                                        q_curr = get_cache (Queasy, {"char1": [(eq, waehrung.wabkurz)],"key": [(eq, 164)],"char2": [(ne, "")]})

                                        if q_curr:
                                            currency = q_curr.char2
                                        else:
                                            currency = "IDR"
                                    else:
                                        currency = "IDR"
                                    queasy.char3 = currency

                                    curr_recid = queasy._recid
                                    queasy = db_session.query(Queasy).filter(
                                             (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str).lower()) & (Queasy._recid > curr_recid)).first()
        else:

            if p_list.startperiode != None and p_list.endperiode != None:
                for datum in date_range(p_list.startperiode,p_list.endperiode) :

                    queasy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, prcode)],"number2": [(eq, p_list.erwachs)],"number3": [(eq, p_list.kind1)]})

                    if queasy:

                        qsy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, prcode)],"number2": [(eq, p_list.erwachs)],"number3": [(eq, p_list.kind1)]})

                        if qsy and qsy.deci1 != p_list.zipreis and qsy.logi1 == False and qsy.logi2 == False:

                            bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                            if bqueasy:
                                bqueasy.logi2 = True


                                pass
                                pass

                    elif not queasy:

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == (prcode).lower()) & (entry(2, Queasy.char1, ";") == (str).lower())).first()
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

                            arrangement = get_cache (Arrangement, {"argtnr": [(eq, p_list.argtnr)]})

                            if arrangement:

                                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)]})

                                if artikel:
                                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                            if tax_included:
                                queasy.deci1 =  to_decimal(p_list.zipreis)
                            else:
                                queasy.deci1 = to_decimal(round(to_decimal(p_list.zipreis * (1 + serv + vat)) , 0))

                            bqueasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, market_nr)]})

                            if bqueasy:

                                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, bqueasy.char3)]})

                            if waehrung:

                                q_curr = get_cache (Queasy, {"char1": [(eq, waehrung.wabkurz)],"key": [(eq, 164)],"char2": [(ne, "")]})

                                if q_curr:
                                    currency = q_curr.char2
                                else:
                                    currency = "IDR"
                            else:
                                currency = "IDR"
                            queasy.char3 = currency

                            curr_recid = queasy._recid
                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str).lower()) & (Queasy._recid > curr_recid)).first()

    p_list = query(p_list_data, first=True)

    qsy = get_cache (Queasy, {"key": [(eq, 152)]})

    if qsy:
        cat_flag = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1013)]})

    if htparam.feldtyp == 1:
        round_betrag = htparam.finteger
        length_round = length(to_string(round_betrag))

    elif htparam.feldtyp == 5 and num_entries(htparam.fchar, ";") > 1:
        round_betrag = to_int(entry(0, htparam.fchar, ";"))
        length_round = length(to_string(round_betrag))
        round_method = to_int(entry(1, htparam.fchar, ";"))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})

    if htparam:
        tax_included = htparam.flogical
    create_child_list()
    fill_ratecode()
    update_child_ratecode()
    update_bookengine_config()

    return generate_output()