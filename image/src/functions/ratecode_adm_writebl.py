from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from models import Ratecode, Queasy, Htparam, Bediener, Res_history, Zimkateg, Guest_pr, Guest, Prtable, Arrangement, Artikel, Waehrung

def ratecode_adm_writebl(mode_str:str, markno:int, prcode:str, argtno:int, user_init:str, book_room:int, comp_room:int, max_room:int, p_list:[P_list], early_discount:[Early_discount], kickback_discount:[Kickback_discount], stay_pay:[Stay_pay]):
    error_flag = False
    tb3buff_list = []
    zikatno:int = 0
    wday:int = 0
    adult:int = 0
    child1:int = 0
    curr_1:int = 0
    curr_2:int = 0
    curr_3:int = 0
    curr_4:int = 0
    mesval:str = ""
    ci_date:date = None
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    adjust_value:decimal = 0
    in_percent:bool = False
    tax_included:bool = False
    curr_time:str = ""
    ratecode = queasy = htparam = bediener = res_history = zimkateg = guest_pr = guest = prtable = arrangement = artikel = waehrung = None

    tb3 = tb3buff = p_list = t_ratecode = q_list = early_discount = kickback_discount = stay_pay = child_list = child_ratecode = product_list = rbuff = q_curr = prbuff = qsy = bqueasy = zbuff = tqueasy = None

    tb3_list, Tb3 = create_model_like(Ratecode, {"s_recid":int})
    tb3buff_list, Tb3buff = create_model_like(Tb3)
    p_list_list, P_list = create_model_like(Tb3, {"rmcat_str":str, "wday_str":str, "adult_str":str, "child_str":str})
    t_ratecode_list, T_ratecode = create_model_like(Ratecode, {"s_recid":int})
    q_list_list, Q_list = create_model("Q_list", {"rcode":str, "dcode":str})
    early_discount_list, Early_discount = create_model("Early_discount", {"disc_rate":decimal, "min_days":int, "min_stay":int, "max_occ":int, "from_date":date, "to_date":date})
    kickback_discount_list, Kickback_discount = create_model("Kickback_discount", {"disc_rate":decimal, "max_days":int, "min_stay":int, "max_occ":int})
    stay_pay_list, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})
    child_list_list, Child_list = create_model("Child_list", {"child_code":str, "true_child":bool, "in_percent":bool, "adjust_value":decimal}, {"true_child": True})
    child_ratecode_list, Child_ratecode = create_model_like(Ratecode)
    product_list_list, Product_list = create_model("Product_list", {"market":int, "i_product":[int, 99], "prcode":str})

    Rbuff = Ratecode
    Q_curr = Queasy
    Prbuff = Prtable
    Qsy = Queasy
    Bqueasy = Queasy
    Zbuff = Zimkateg
    Tqueasy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list
        return {"error_flag": error_flag, "tb3Buff": tb3buff_list}

    def delete_old_childrate():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list

        curr_i:int = 0

        p_list = query(p_list_list, first=True)

        child_list = query(child_list_list, first=True)
        while None != child_list:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.CODE == child_list.child_code) &  (Ratecode.startperiode == p_list.startperiode) &  (Ratecode.endperiode == p_list.endperiode) &  (Ratecode.wday == p_list.wday) &  (Ratecode.erwachs == p_list.erwachs) &  (Ratecode.argtnr == p_list.argtnr) &  (Ratecode.zikatnr == p_list.zikatnr)).first()

            if ratecode:

                ratecode = db_session.query(Ratecode).first()
                db_session.delete(ratecode)


            child_list = query(child_list_list, next=True)

        child_list = query(child_list_list, first=True)
        while None != child_list:

            prtable = db_session.query(Prtable).filter(
                    (Prtable.prcode == child_list.child_code)).first()
            while None != prtable :
                product_list = Product_list()
                product_list_list.append(product_list)

                product_list.market = prtable.marknr
                product_list.prcode = prtable.prcode


                for curr_i in range(1,99 + 1) :

                    if prtable.product[curr_i - 1] == 0:
                        return

                    if prtable.product[curr_i - 1] >= 90001:

                        rbuff = db_session.query(Rbuff).filter(
                                (Rbuff.CODE == prtable.prcode) &  (Rbuff.marknr == prtable.marknr) &  (((90 + Rbuff.zikatnr) * 1000 + Rbuff.argtnr) == prtable.product[curr_i - 1])).first()

                    elif prtable.product[curr_i - 1] >= 10001:

                        rbuff = db_session.query(Rbuff).filter(
                                (Rbuff.CODE == prtable.prcode) &  (Rbuff.marknr == prtable.marknr) &  ((Rbuff.zikatnr * 1000 + Rbuff.argtnr) == prtable.product[curr_i - 1])).first()
                    else:

                        rbuff = db_session.query(Rbuff).filter(
                                (Rbuff.CODE == prtable.prcode) &  (Rbuff.marknr == prtable.marknr) &  ((Rbuff.zikatnr * 100 + Rbuff.argtnr) == prtable.product[curr_i - 1])).first()

                    if rbuff:
                        product_list.i_product[curr_i - 1] = prtable.product[curr_i - 1]

                prtable = db_session.query(Prtable).first()
                db_session.delete(prtable)


                prtable = db_session.query(Prtable).filter(
                        (Prtable.prcode == child_list.child_code)).first()

            child_list = query(child_list_list, next=True)

    def create_childrate():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list

        curr_i:int = 0
        rounded_rate:decimal = 0
        Prbuff = Prtable

        p_list = query(p_list_list, first=True)

        for child_list in query(child_list_list):

            for ratecode in db_session.query(Ratecode).filter(
                    (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.startperiode == p_list.startperiode) &  (Ratecode.endperiode == p_list.endperiode)).all():

                rbuff = db_session.query(Rbuff).filter(
                        (Rbuff.CODE == child_list.child_code) &  (Rbuff.startperiode == ratecode.startperiode) &  (Rbuff.endperiode == ratecode.endperiode) &  (Rbuff.wday == ratecode.wday) &  (Rbuff.erwachs == ratecode.erwachs) &  (Rbuff.argtnr == ratecode.argtnr) &  (Rbuff.zikatnr == ratecode.zikatnr)).first()

                if not rbuff:
                    rbuff = Rbuff()
                    db_session.add(rbuff)

                    buffer_copy(ratecode, rbuff,except_fields=["ratecode.CODE","ratecode.argtnr"])
                    rbuff.CODE = child_list.child_code
                    rbuff.argtnr = argtno

                    if child_list.in_percent:
                        rbuff.zipreis = rbuff.zipreis * (1 + child_list.adjust_value * 0.01)

                        if round_betrag != 0 and rbuff.zipreis >= (round_betrag * 10):
                            rounded_rate = round_it(rbuff.zipreis)
                            rbuff.zipreis = rounded_rate
                    else:
                        rbuff.zipreis = rbuff.zipreis + child_list.adjust_value

        child_list = query(child_list_list, first=True)
        while None != child_list:

            prtable = db_session.query(Prtable).filter(
                    (func.lower(Prtable.(prcode).lower()) == (prcode).lower())).first()
            while None != prtable:
                prbuff = Prbuff()
                db_session.add(prbuff)

                buffer_copy(prtable, prbuff,except_fields=["prcode"])
                prbuff.prcode = child_list.child_code

                product_list = query(product_list_list, filters=(lambda product_list :product_list.market == prbuff.marknr and product_list.prcode == prbuff.prcode), first=True)

                if product_list:
                    for curr_i in range(1,99 + 1) :

                        if prbuff.product[curr_i - 1] == 0:
                            prbuff.product[curr_i - 1] = product_list.i_product[curr_i - 1]


                    product_list_list.remove(product_list)

                prtable = db_session.query(Prtable).filter(
                        (func.lower(Prtable.(prcode).lower()) == (prcode).lower())).first()

            child_list = query(child_list_list, next=True)

    def check_overlapping():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list


        for curr_1 in range(1,num_entries(p_list.rmcat_str, ",")  + 1) :
            mesval = trim(entry(curr_1 - 1, p_list.rmcat_str, ","))

            if mesval != "":

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.kurzbez == mesval)).first()
                zikatno = zimkateg.zikatnr
                for curr_2 in range(1,num_entries(p_list.wday_str, ",")  + 1) :
                    mesval = trim(entry(curr_2 - 1, p_list.wday_str, ","))

                    if mesval != "":
                        wday = to_int(mesval)
                        for curr_3 in range(1,num_entries(p_list.adult_str, ",")  + 1) :
                            mesval = trim(entry(curr_3 - 1, p_list.adult_str, ","))

                            if mesval != "":
                                adult = to_int(mesval)
                                for curr_4 in range(1,num_entries(p_list.child_str, ",")  + 1) :
                                    mesval = trim(entry(curr_4 - 1, p_list.child_str, ","))

                                    if mesval != "":
                                        child1 = to_int(mesval)

                                        ratecode = db_session.query(Ratecode).filter(
                                                (Ratecode.marknr == markno) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == p_list.kind2) &  (Ratecode.wday == wday) &  (not Ratecode.startperiod >= p_list.endperiode) &  (not Ratecode.endperiod < p_list.startperiode)).first()

                                        if ratecode:
                                            error_flag = True

                                            return

    def create_child_list():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (not Queasy.logi2) &  (num_entries(Queasy.char3, ";") > 2) &  (entry(1, Queasy.char3, ";") == (prcode).lower())).all():
            child_list = Child_list()
            child_list_list.append(child_list)

            child_list.child_code = queasy.char1
            child_list.in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
            child_list.adjust_value = decimal.Decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

    def create_records():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list


        for curr_1 in range(1,num_entries(p_list.rmcat_str, ",")  + 1) :
            mesval = trim(entry(curr_1 - 1, p_list.rmcat_str, ","))

            if mesval != "":

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.kurzbez == mesval)).first()
                zikatno = zimkateg.zikatnr
                for curr_2 in range(1,num_entries(p_list.wday_str, ",")  + 1) :
                    mesval = trim(entry(curr_2 - 1, p_list.wday_str, ","))

                    if mesval != "":
                        wday = to_int(mesval)
                        for curr_3 in range(1,num_entries(p_list.adult_str, ",")  + 1) :
                            mesval = trim(entry(curr_3 - 1, p_list.adult_str, ","))

                            if mesval != "":
                                adult = to_int(mesval)
                                for curr_4 in range(1,num_entries(p_list.child_str, ",")  + 1) :
                                    mesval = trim(entry(curr_4 - 1, p_list.child_str, ","))

                                    if mesval != "":
                                        child1 = to_int(mesval)
                                        create_ratecode()

    def create_ratecode():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list


        ratecode = Ratecode()
        db_session.add(ratecode)

        buffer_copy(p_list, ratecode,except_fields=["p_list.argtnr","p_list.zikatnr"])
        ratecode.marknr = markno
        ratecode.code = prcode
        ratecode.argtnr = argtno
        ratecode.zikatnr = zikatno
        ratecode.wday = wday
        ratecode.erwachs = adult
        ratecode.kind1 = child1
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
        tb3buff = Tb3buff()
        tb3buff_list.append(tb3buff)

        buffer_copy(ratecode, tb3buff)
        tb3Buff.s_recid = to_int(ratecode._recid)

    def update_child_rate_dates():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list

        beg_datum:date = None
        end_datum:date = None
        parent_code:str = ""
        Rbuff = Ratecode

        for tb3buff in query(tb3buff_list):

            for child_list in query(child_list_list):

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 2) &  (Queasy.char1 == child_list.child_code)).first()
                parent_code = entry(1, queasy.char3, ";")
                in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
                adjust_value = decimal.Decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

                for ratecode in db_session.query(Ratecode).filter(
                        (Ratecode.marknr == markno) &  (Ratecode.code == child_list.child_code) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == tb3Buff.zikatnr) &  (Ratecode.erwachs == tb3Buff.erwachs) &  (Ratecode.kind1 == tb3Buff.kind1) &  (Ratecode.kind2 == tb3Buff.kind2) &  (Ratecode.wday == tb3Buff.wday) &  (not Ratecode.endperiode < tb3Buff.startperiode) &  (not Ratecode.startperiode > tb3Buff.endperiode)).all():

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

                            buffer_copy(tb3Buff, child_ratecode,except_fields=["CODE"])
                            child_ratecode.CODE = child_list.child_code


                            set_child_rate()
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

    def update_ratecode_dates():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list

        beg_datum:date = None
        end_datum:date = None
        parent_code:str = ""
        Rbuff = Ratecode

        for tb3buff in query(tb3buff_list):

            for ratecode in db_session.query(Ratecode).filter(
                    (Ratecode.marknr == markno) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == tb3Buff.zikatnr) &  (Ratecode.erwachs == tb3Buff.erwachs) &  (Ratecode.kind1 == tb3Buff.kind1) &  (Ratecode.kind2 == tb3Buff.kind2) &  (Ratecode.wday == tb3Buff.wday) &  (not Ratecode.endperiode < tb3Buff.startperiode) &  (not Ratecode.startperiode > tb3Buff.endperiode) &  (to_int(Ratecode._recid) != tb3Buff.s_recid)).all():

                if ratecode.startperiode < tb3Buff.startperiode:

                    if ratecode.endperiode <= tb3Buff.endperiode:
                        ratecode.endperiode = tb3Buff.startperiode - 1


                    else:
                        rbuff = Rbuff()
                        db_session.add(rbuff)

                        buffer_copy(ratecode, rbuff,except_fields=["startperiode"])
                        ratecode.endperiode = tb3Buff.startperiode - 1
                        rbuff.startperiode = tb3Buff.endperiode + 1

                        rbuff = db_session.query(Rbuff).first()
                else:

                    if ratecode.endperiode <= tb3Buff.endperiode:
                        db_session.delete(ratecode)
                    else:
                        ratecode.startperiode = tb3Buff.endperiode + 1

    def set_child_rate():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list

        rounded_rate:decimal = 0

        if in_percent:
            child_ratecode.zipreis = child_ratecode.zipreis * (1 + adjust_value * 0.01)

            if round_betrag != 0 and child_ratecode.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(child_ratecode.zipreis)
                child_ratecode.zipreis = rounded_rate
        else:
            child_ratecode.zipreis = child_ratecode.zipreis + adjust_value

    def set_child_rate_1():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list

        rounded_rate:decimal = 0

        if in_percent:
            ratecode.zipreis = ratecode.zipreis * (1 + adjust_value * 0.01)

            if round_betrag != 0 and ratecode.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(ratecode.zipreis)
                ratecode.zipreis = rounded_rate
        else:
            ratecode.zipreis = ratecode.zipreis + adjust_value

    def update_bookengine_config():

        nonlocal error_flag, tb3buff_list, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr, prbuff, qsy, bqueasy, zbuff, tqueasy
        nonlocal tb3_list, tb3buff_list, p_list_list, t_ratecode_list, q_list_list, early_discount_list, kickback_discount_list, stay_pay_list, child_list_list, child_ratecode_list, product_list_list

        cm_gastno:int = 0
        iftask:str = ""
        mestoken:str = ""
        mesvalue:str = ""
        tokcounter:int = 0
        datum:date = None
        cat_flag:bool = False
        roomnr:int = 0
        dyna:str = ""
        loopi:int = 0
        loopj:int = 0
        loopk:int = 0
        currency:str = ""
        serv:decimal = 0
        vat:decimal = 0
        str:str = ""
        Qsy = Queasy
        Bqueasy = Queasy
        Zbuff = Zimkateg
        Tqueasy = Queasy

        qsy = db_session.query(Qsy).filter(
                (Qsy.key == 152)).first()

        if qsy:
            cat_flag = True

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

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if mode_str.lower()  == "insert":
        check_overlapping()

    if error_flag:

        return generate_output()
    create_records()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "RateCode"

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == p_list.zikatnr)).first()

        if zimkateg:
            res_history.aenderung = "Create Contract Rate, Code: " + prcode + " RmType : " + zimkateg.kurzbez +\
                " start:" + to_string(p_list.startperiode) + "|end:" + to_string(p_list.endperiode) +\
                "|adult:" + to_string(adult) + "|rate:" + to_string(p_list.zipreis)


        else:
            res_history.aenderung = "Create Contract Rate, Code: " + prcode +\
                " start:" + to_string(p_list.startperiode) + "|end:" + to_string(p_list.endperiode) +\
                "|adult:" + to_string(adult) + "|rate:" + to_string(p_list.zipreis)

        res_history = db_session.query(Res_history).first()


    if mode_str.lower()  == "update":

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1013)).first()

        if htparam.feldtyp == 1:
            round_betrag = htparam.finteger
            length_round = len(to_string(round_betrag))

        elif htparam.feldtyp == 5 and num_entries(htparam.fchar, ";") > 1:
            round_betrag = to_int(entry(0, htparam.fchar, ";"))
            length_round = len(to_string(round_betrag))
            round_method = to_int(entry(1, htparam.fchar, ";"))


        create_child_list()
        update_child_rate_dates()
    update_ratecode_dates()
    create_child_list()
    curr_time = to_string(get_current_time_in_seconds(), "HH:MM:SS")


    delete_old_childrate()
    create_childrate()

    for guest_pr in db_session.query(Guest_pr).filter(
            (func.lower(Guest_pr.code) == (prcode).lower())).all():

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == guest_pr.gastnr)).first()

        if guest.endperiode == None or guest.endperiode < p_list.endperiode:

            guest = db_session.query(Guest).first()
            guest.endperiode = p_list.endperiode

            guest = db_session.query(Guest).first()
    update_bookengine_config()
    for curr_1 in range(1,num_entries(p_list.rmcat_str, ",")  + 1) :
        mesval = trim(entry(curr_1 - 1, p_list.rmcat_str, ","))

        if mesval != "":

            zbuff = db_session.query(Zbuff).filter(
                    (Zbuff.kurzbez == mesval)).first()

            if zbuff:
                roomnr = 0

                if cat_flag:
                    roomnr = zbuff.typ

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 152) &  (Queasy.number1 == roomnr)).first()

                    if queasy:
                        str = queasy.char1
                else:
                    roomnr = zbuff.zikatnr
                    str = zbuff.kurzbez

                if dyna != "":
                    for tokcounter in range(1,num_entries(dyna, ";")  + 1) :
                        mesvalue = trim(entry(tokcounter - 1, dyna, ";"))

                        if mesvalue != "":
                            for datum in range(p_list.startperiode,p_list.endperiode + 1) :

                                queasy = db_session.query(Queasy).filter(
                                        (Queasy.key == 170) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (Queasy.char1 == mesvalue)).first()

                                if queasy:

                                    qsy = db_session.query(Qsy).filter(
                                            (Qsy.key == 170) &  (Qsy.date1 == datum) &  (Qsy.number1 == roomnr) &  (Qsy.char1 == mesvalue)).first()
                                    while None != qsy:

                                        bqueasy = db_session.query(Bqueasy).filter(
                                                (Bqueasy._recid == qsy._recid)).first()

                                        if bqueasy:
                                            bqueasy.logi2 = True

                                            bqueasy = db_session.query(Bqueasy).first()


                                        qsy = db_session.query(Qsy).filter(
                                                (Qsy.key == 170) &  (Qsy.date1 == datum) &  (Qsy.number1 == roomnr) &  (Qsy.char1 == mesvalue)).first()

                                elif not queasy:
                                    for loopi in range(1,num_entries(p_list.adult_str, ",")  + 1) :

                                        if p_list.child_str != "":
                                            for loopj in range(1,num_entries(p_list.child_str, ",")  + 1) :

                                                queasy = db_session.query(Queasy).filter(
                                                        (Queasy.key == 161) &  (entry(0, Queasy.char1, ";") == mesvalue) &  (entry(2, Queasy.char1, ";") == (str).lower())).first()
                                                while None != queasy:
                                                    queasy = Queasy()
                                                    db_session.add(queasy)

                                                    queasy.key = 170
                                                    queasy.date1 = datum
                                                    queasy.char1 = mesvalue
                                                    queasy.number1 = roomnr
                                                    queasy.number2 = to_int(entry(loopi - 1, p_list.adult_str, ","))
                                                    queasy.number3 = to_int(entry(loopj - 1, p_list.child_str, ","))
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
                                                            (Bqueasy.key == 18) &  (Bqueasy.number1 == markno)).first()

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

                                            queasy = db_session.query(Queasy).filter(
                                                    (Queasy.key == 161) &  (entry(0, Queasy.char1, ";") == mesvalue) &  (entry(2, Queasy.char1, ";") == (str).lower())).first()
                                            while None != queasy:
                                                queasy = Queasy()
                                                db_session.add(queasy)

                                                queasy.key = 170
                                                queasy.date1 = datum
                                                queasy.char1 = mesvalue
                                                queasy.number1 = roomnr
                                                queasy.number2 = to_int(entry(loopi - 1, p_list.adult_str, ","))
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
                                                        (Bqueasy.key == 18) &  (Bqueasy.number1 == markno)).first()

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
                                (Queasy.key == 170) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (func.lower(Queasy.char1) == (prcode).lower())).first()

                        if queasy:

                            qsy = db_session.query(Qsy).filter(
                                    (Qsy.key == 170) &  (Qsy.date1 == datum) &  (Qsy.number1 == roomnr) &  (func.lower(Qsy.char1) == (prcode).lower())).first()
                            while None != qsy:

                                bqueasy = db_session.query(Bqueasy).filter(
                                        (Bqueasy._recid == qsy._recid)).first()

                                if bqueasy:
                                    bqueasy.logi2 = True

                                    bqueasy = db_session.query(Bqueasy).first()


                                qsy = db_session.query(Qsy).filter(
                                        (Qsy.key == 170) &  (Qsy.date1 == datum) &  (Qsy.number1 == roomnr) &  (func.lower(Qsy.char1) == (prcode).lower())).first()

                        elif not queasy:
                            for loopi in range(1,num_entries(p_list.adult_str, ",")  + 1) :

                                if p_list.child_str != "":
                                    for loopj in range(1,num_entries(p_list.child_str, ",")  + 1) :

                                        queasy = db_session.query(Queasy).filter(
                                                (Queasy.key == 161) &  (entry(0, Queasy.char1, ";") == (prcode).lower()) &  (entry(2, Queasy.char1, ";") == (str).lower())).first()
                                        while None != queasy:
                                            queasy = Queasy()
                                            db_session.add(queasy)

                                            queasy.key = 170
                                            queasy.date1 = datum
                                            queasy.char1 = prcode
                                            queasy.number1 = roomnr
                                            queasy.number2 = to_int(entry(loopi - 1, p_list.adult_str, ","))
                                            queasy.number3 = to_int(entry(loopj - 1, p_list.child_str, ","))
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
                                                    (Bqueasy.key == 18) &  (Bqueasy.number1 == markno)).first()

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

                                    queasy = db_session.query(Queasy).filter(
                                            (Queasy.key == 161) &  (entry(0, Queasy.char1, ";") == (prcode).lower()) &  (entry(2, Queasy.char1, ";") == (str).lower())).first()
                                    while None != queasy:
                                        queasy = Queasy()
                                        db_session.add(queasy)

                                        queasy.key = 170
                                        queasy.date1 = datum
                                        queasy.char1 = prcode
                                        queasy.number1 = roomnr
                                        queasy.number2 = to_int(entry(loopi - 1, p_list.adult_str, ","))
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
                                                (Bqueasy.key == 18) &  (Bqueasy.number1 == markno)).first()

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