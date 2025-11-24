#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 31/7/2025
# gitlab: 512
# requery, handle recid none
# num_entries
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from sqlalchemy.orm.attributes import flag_modified
from models import Ratecode, Queasy, Htparam, Bediener, Res_history, Zimkateg, Guest_pr, Guest, Prtable, Arrangement, Artikel, Waehrung

tb3_data, Tb3 = create_model_like(Ratecode, {"s_recid":int})
p_list_data, P_list = create_model_like(Tb3, {"rmcat_str":string, "wday_str":string, "adult_str":string, "child_str":string})
early_discount_data, Early_discount = create_model("Early_discount", {"disc_rate":Decimal, "min_days":int, "min_stay":int, "max_occ":int, "from_date":date, "to_date":date})
kickback_discount_data, Kickback_discount = create_model("Kickback_discount", {"disc_rate":Decimal, "max_days":int, "min_stay":int, "max_occ":int})
stay_pay_data, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})

def ratecode_adm_writebl(mode_str:string, markno:int, prcode:string, argtno:int, user_init:string, book_room:int, 
                         comp_room:int, max_room:int, p_list_data:[P_list], early_discount_data:[Early_discount], 
                         kickback_discount_data:[Kickback_discount], stay_pay_data:[Stay_pay]):

    prepare_cache ([Ratecode, Queasy, Htparam, Bediener, Res_history, Zimkateg, Guest_pr, Guest, Arrangement, Artikel, Waehrung])

    tb3_data = []
    error_flag = False
    tb3buff_data = []
    zikatno:int = 0
    wday:int = 0
    adult:int = 0
    child1:int = 0
    curr_1:int = 0
    curr_2:int = 0
    curr_3:int = 0
    curr_4:int = 0
    mesval:string = ""
    ci_date:date = None
    round_betrag:int = 0
    round_method:int = 0
    length_round:int = 0
    adjust_value:Decimal = to_decimal("0.0")
    in_percent:bool = False
    tax_included:bool = False
    curr_time:string = ""
    ratecode = queasy = htparam = bediener = res_history = zimkateg = guest_pr = guest = prtable = arrangement = artikel = waehrung = None

    tb3 = tb3buff = p_list = t_ratecode = q_list = early_discount = kickback_discount = stay_pay = child_list = child_ratecode = product_list = rbuff = q_curr = None

    tb3buff_data, Tb3buff = create_model_like(Tb3)
    t_ratecode_data, T_ratecode = create_model_like(Ratecode, {"s_recid":int})
    q_list_data, Q_list = create_model("Q_list", {"rcode":string, "dcode":string})
    child_list_data, Child_list = create_model("Child_list", {"child_code":string, "true_child":bool, "in_percent":bool, "adjust_value":Decimal}, {"true_child": True})
    child_ratecode_data, Child_ratecode = create_model_like(Ratecode)
    product_list_data, Product_list = create_model("Product_list", {"market":int, "i_product":[int,99], "prcode":string})

    Rbuff = create_buffer("Rbuff",Ratecode)
    Q_curr = create_buffer("Q_curr",Queasy)


    db_session = local_storage.db_session

    mode_str = mode_str.strip()
    prcode = prcode.strip()
    
    def generate_output():
        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data

        return {"error_flag": error_flag, "tb3buff": tb3buff_data}

    def delete_old_childrate():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data

        curr_i:int = 0

        p_list = query(p_list_data, first=True)

        child_list = query(child_list_data, first=True)
        while None != child_list:

            ratecode = get_cache (Ratecode, {"code": [(eq, child_list.child_code)],"startperiode": [(eq, p_list.startperiode)],"endperiode": [(eq, p_list.endperiode)],"wday": [(eq, p_list.wday)],"erwachs": [(eq, p_list.erwachs)],"argtnr": [(eq, p_list.argtnr)],"zikatnr": [(eq, p_list.zikatnr)]})

            if ratecode:
                pass
                db_session.delete(ratecode)
                pass

            child_list = query(child_list_data, next=True)

        child_list = query(child_list_data, first=True)
        while None != child_list:

            # prtable = get_cache (Prtable, {"prcode": [(eq, child_list.child_code)]})
            prtable = db_session.query(Prtable).filter(Prtable.prcode == child_list.child_code).first()
            while None != prtable :
                product_list = Product_list()
                product_list_data.append(product_list)

                product_list.market = prtable.marknr
                product_list.prcode = prtable.prcode


                for curr_i in range(1,99 + 1) :

                    # if prtable.product[curr_i - 1] == 0:
                    #     return
                    # if prtable.product[curr_i - 1] == 0:
                    #     continue

                    if prtable.product[curr_i - 1] >= 90001:

                        rbuff = db_session.query(Rbuff).filter(
                                 (Rbuff.code == prtable.prcode) & (Rbuff.marknr == prtable.marknr) & (((90 + Rbuff.zikatnr) * 1000 + Rbuff.argtnr) == prtable.product[curr_i - 1])).first()

                    elif prtable.product[curr_i - 1] >= 10001:

                        rbuff = db_session.query(Rbuff).filter(
                                 (Rbuff.code == prtable.prcode) & (Rbuff.marknr == prtable.marknr) & ((Rbuff.zikatnr * 1000 + Rbuff.argtnr) == prtable.product[curr_i - 1])).first()
                    else:

                        rbuff = db_session.query(Rbuff).filter(
                                 (Rbuff.code == prtable.prcode) & (Rbuff.marknr == prtable.marknr) & ((Rbuff.zikatnr * 100 + Rbuff.argtnr) == prtable.product[curr_i - 1])).first()

                    if rbuff:
                        product_list.i_product[curr_i - 1] = prtable.product[curr_i - 1]


                pass
                db_session.delete(prtable)
                pass

                curr_recid = prtable._recid
                prtable = db_session.query(Prtable).filter(
                         (Prtable.prcode == child_list.child_code) & (Prtable._recid > curr_recid)).first()

            child_list = query(child_list_data, next=True)
            flag_modified(prtable, "product")


    def create_childrate():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data

        prbuff = None
        curr_i:int = 0
        rounded_rate:Decimal = to_decimal("0.0")
        Prbuff =  create_buffer("Prbuff",Prtable)

        p_list = query(p_list_data, first=True)

        for child_list in query(child_list_data):

            for ratecode in db_session.query(Ratecode).filter(
                     (Ratecode.code == (prcode)) & (Ratecode.startperiode == p_list.startperiode) & (Ratecode.endperiode == p_list.endperiode)).order_by(Ratecode._recid).all():

                rbuff = get_cache (Ratecode, {"code": [(eq, child_list.child_code)],"startperiode": [(eq, ratecode.startperiode)],"endperiode": [(eq, ratecode.endperiode)],"wday": [(eq, ratecode.wday)],"erwachs": [(eq, ratecode.erwachs)],"argtnr": [(eq, ratecode.argtnr)],"zikatnr": [(eq, ratecode.zikatnr)]})

                if not rbuff:
                    rbuff = Ratecode()
                    db_session.add(rbuff)

                    buffer_copy(ratecode, rbuff,except_fields=["ratecode.code","ratecode.argtnr"])
                    rbuff.code = child_list.child_code
                    rbuff.argtnr = argtno
                    db_session.commit()

                    if child_list.in_percent:
                        rbuff.zipreis =  to_decimal(rbuff.zipreis) * to_decimal((1) + to_decimal(child_list.adjust_value) * to_decimal(0.01))

                        if round_betrag != 0 and rbuff.zipreis >= (round_betrag * 10):
                            rounded_rate = round_it(round_method, round_betrag, rbuff.zipreis)
                            rbuff.zipreis =  to_decimal(rounded_rate)
                    else:
                        rbuff.zipreis =  to_decimal(rbuff.zipreis) + to_decimal(child_list.adjust_value)

        child_list = query(child_list_data, first=True)
        while None != child_list:

            # prtable = get_cache (Prtable, {"prcode": [(eq, prcode)]})
            # while None != prtable:
            for prtable in db_session.query(Prtable).filter(Prtable.prcode == prcode).order_by(Prtable._recid).all():
                prbuff = Prtable()
                db_session.add(prbuff)
                db_session.commit()

                buffer_copy(prtable, prbuff,except_fields=["prcode"])
                prbuff.prcode = child_list.child_code

                product_list = query(product_list_data, filters=(lambda product_list: product_list.market == prbuff.marknr and product_list.prcode == prbuff.prcode), first=True)

                if product_list:
                    for curr_i in range(1,99 + 1) :

                        if prbuff.product[curr_i - 1] == 0:
                            prbuff.product[curr_i - 1] = product_list.i_product[curr_i - 1]


                    product_list_data.remove(product_list)
                    
                flag_modified(prbuff, "product")
                # curr_recid = prtable._recid
                # prtable = db_session.query(Prtable).filter(
                #          (Prtable.prcode == (prcode)) & (Prtable._recid > curr_recid)).first()

            child_list = query(child_list_data, next=True)
            

    def check_overlapping():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data


        for curr_1 in range(1,num_entries(p_list.rmcat_str, ",")  + 1) :
            mesval = trim(entry(curr_1 - 1, p_list.rmcat_str, ","))
            if mesval != "":

                zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, mesval)]})
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

                                        ratecode = get_cache (Ratecode, {"marknr": [(eq, markno)],"code": [(eq, prcode)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, zikatno)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, p_list.kind2)],"wday": [(eq, wday)],"startperiode": [(ge, p_list.endperiode)],"endperiode": [(lt, p_list.startperiode)]})

                                        if ratecode:
                                            error_flag = True

                                            return


    def create_child_list():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data

        # Rd 14/8/2025
        # for queasy in db_session.query(Queasy).filter(
        #          (Queasy.key == 2) & not_ (Queasy.logi2) & 
        #          (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (prcode))).order_by(Queasy._recid).all():
        for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 2) & not_ (Queasy.logi2)).order_by(Queasy._recid).all():
            if (num_entries(queasy.char3, ";") > 2) & (entry(1, queasy.char3, ";") == (prcode)):
                child_list = Child_list()
                child_list_data.append(child_list)

                child_list.child_code = queasy.char1
                child_list.in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
                child_list.adjust_value = to_decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100


    def create_records():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data


        for curr_1 in range(1,num_entries(p_list.rmcat_str, ",")  + 1) :
            mesval = trim(entry(curr_1 - 1, p_list.rmcat_str, ","))
            if mesval != "":

                zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, mesval)]})
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

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data


        ratecode = Ratecode()
        db_session.add(ratecode)
        db_session.commit()

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
        tb3buff = Tb3buff()
        tb3buff_data.append(tb3buff)

        buffer_copy(ratecode, tb3buff)
        tb3buff.s_recid = to_int(ratecode._recid)

        flag_modified(ratecode, "char1")


    def update_child_rate_dates():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data

        beg_datum:date = None
        end_datum:date = None
        parent_code:string = ""
        rbuff = None
        Rbuff =  create_buffer("Rbuff",Ratecode)

        for tb3buff in query(tb3buff_data):

            for child_list in query(child_list_data):

                queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, child_list.child_code)]})
                parent_code = entry(1, queasy.char3, ";")
                in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
                adjust_value = to_decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

                for ratecode in db_session.query(Ratecode).filter(
                         (Ratecode.marknr == markno) & (Ratecode.code == child_list.child_code) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == tb3buff.zikatnr) & (Ratecode.erwachs == tb3buff.erwachs) & (Ratecode.kind1 == tb3buff.kind1) & (Ratecode.kind2 == tb3buff.kind2) & (Ratecode.wday == tb3buff.wday) & not_ (Ratecode.endperiode < tb3buff.startperiode) & not_ (Ratecode.startperiode > tb3buff.endperiode)).order_by(Ratecode._recid).all():

                    if ratecode.startperiode < tb3buff.startperiode:

                        if ratecode.endperiode <= tb3buff.endperiode:
                            end_datum = ratecode.endperiode
                            ratecode.endperiode = tb3buff.startperiode - timedelta(days=1)


                            child_ratecode = Child_ratecode()
                            child_ratecode_data.append(child_ratecode)

                            buffer_copy(tb3buff, child_ratecode,except_fields=["CODE","endperiode"])
                            child_ratecode.code = child_list.child_code
                            child_ratecode.endperiode = end_datum


                            set_child_rate()
                        else:
                            child_ratecode = Child_ratecode()
                            child_ratecode_data.append(child_ratecode)

                            buffer_copy(tb3buff, child_ratecode,except_fields=["CODE"])
                            child_ratecode.code = child_list.child_code


                            set_child_rate()
                            child_ratecode = Child_ratecode()
                            child_ratecode_data.append(child_ratecode)

                            buffer_copy(ratecode, child_ratecode,except_fields=["startperiode"])
                            ratecode.endperiode = tb3buff.startperiode - timedelta(days=1)
                            child_ratecode.startperiode = tb3buff.endperiode + timedelta(days=1)

                    elif (ratecode.startperiode >= tb3buff.startperiode) and (ratecode.endperiode <= tb3buff.endperiode):
                        set_child_rate_1()

                    elif (ratecode.startperiode >= tb3buff.startperiode) and (ratecode.endperiode > tb3buff.endperiode):
                        beg_datum = ratecode.startperiode
                        ratecode.startperiode = tb3buff.endperiode + timedelta(days=1)


                        child_ratecode = Child_ratecode()
                        child_ratecode_data.append(child_ratecode)

                        buffer_copy(tb3buff, child_ratecode,except_fields=["CODE","startperiode"])
                        child_ratecode.code = child_list.child_code
                        child_ratecode.startperiode = beg_datum


                        set_child_rate()

        for child_ratecode in query(child_ratecode_data):
            ratecode = Ratecode()
            db_session.add(ratecode)
            db_session.commit()

            buffer_copy(child_ratecode, ratecode)
            child_ratecode_data.remove(child_ratecode)


    def update_ratecode_dates():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data

        beg_datum:date = None
        end_datum:date = None
        parent_code:string = ""
        rbuff = None
        Rbuff =  create_buffer("Rbuff",Ratecode)

        # for tb3buff in query(tb3buff_data):

            # for ratecode in db_session.query(Ratecode).filter(
            #          (Ratecode.marknr == markno) & (Ratecode.code == (prcode)) & (Ratecode.argtnr == argtno) & 
            #          (Ratecode.zikatnr == tb3buff.zikatnr) & (Ratecode.erwachs == tb3buff.erwachs) & 
            #          (Ratecode.kind1 == tb3buff.kind1) & (Ratecode.kind2 == tb3buff.kind2) & 
            #          (Ratecode.wday == tb3buff.wday) & not_ (Ratecode.endperiode < tb3buff.startperiode) & 
            #          not_ (Ratecode.startperiode > tb3buff.endperiode) & (to_int(Ratecode._recid) != tb3buff.s_recid)).order_by(Ratecode._recid).all():
            
            # Rd 31/7/2025
            # requery _recid null

        for tb3buff in tb3buff_data:
            recid = tb3buff.s_recid
            if not recid or str(recid).strip() == '':
                recid = None

            query = db_session.query(Ratecode).filter(
                (Ratecode.marknr == markno) &
                (Ratecode.code == prcode) &
                (Ratecode.argtnr == argtno) &
                (Ratecode.zikatnr == tb3buff.zikatnr) &
                (Ratecode.erwachs == tb3buff.erwachs) &
                (Ratecode.kind1 == tb3buff.kind1) &
                (Ratecode.kind2 == tb3buff.kind2) &
                (Ratecode.wday == tb3buff.wday) &
                not_(Ratecode.endperiode < tb3buff.startperiode) &
                not_(Ratecode.startperiode > tb3buff.endperiode)
            )

            if recid is not None:
                query = query.filter(Ratecode._recid != str(recid))

            results = query.order_by(Ratecode._recid).all()

            for ratecode in results:
                if ratecode.startperiode < tb3buff.startperiode:

                    if ratecode.endperiode <= tb3buff.endperiode:
                        ratecode.endperiode = tb3buff.startperiode - timedelta(days=1)


                    else:
                        rbuff = Ratecode()
                        db_session.add(rbuff)
                        db_session.commit()

                        buffer_copy(ratecode, rbuff,except_fields=["startperiode"])
                        ratecode.endperiode = tb3buff.startperiode - timedelta(days=1)
                        rbuff.startperiode = tb3buff.endperiode + timedelta(days=1)


                        pass
                else:

                    if ratecode.endperiode <= tb3buff.endperiode:
                        db_session.delete(ratecode)
                    else:
                        ratecode.startperiode = tb3buff.endperiode + timedelta(days=1)


    def set_child_rate():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data

        rounded_rate:Decimal = to_decimal("0.0")

        if in_percent:
            child_ratecode.zipreis =  to_decimal(child_ratecode.zipreis) * to_decimal((1) + to_decimal(adjust_value) * to_decimal(0.01))

            if round_betrag != 0 and child_ratecode.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(round_method, round_betrag, child_ratecode.zipreis)
                child_ratecode.zipreis =  to_decimal(rounded_rate)
        else:
            child_ratecode.zipreis =  to_decimal(child_ratecode.zipreis) + to_decimal(adjust_value)


    def set_child_rate_1():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data

        rounded_rate:Decimal = to_decimal("0.0")

        if in_percent:
            ratecode.zipreis =  to_decimal(ratecode.zipreis) * to_decimal((1) + to_decimal(adjust_value) * to_decimal(0.01))

            if round_betrag != 0 and ratecode.zipreis >= (round_betrag * 10):
                rounded_rate = round_it(round_method, round_betrag, ratecode.zipreis)
                ratecode.zipreis =  to_decimal(rounded_rate)
        else:
            ratecode.zipreis =  to_decimal(ratecode.zipreis) + to_decimal(adjust_value)


    def update_bookengine_config():

        nonlocal tb3_data, error_flag, tb3buff_data, zikatno, wday, adult, child1, curr_1, curr_2, curr_3, curr_4, mesval, ci_date, round_betrag, round_method, length_round, adjust_value, in_percent, tax_included, curr_time, ratecode, queasy, htparam, bediener, res_history, zimkateg, guest_pr, guest, prtable, arrangement, artikel, waehrung
        nonlocal mode_str, markno, prcode, argtno, user_init, book_room, comp_room, max_room
        nonlocal rbuff, q_curr


        nonlocal tb3, tb3buff, p_list, t_ratecode, q_list, early_discount, kickback_discount, stay_pay, child_list, child_ratecode, product_list, rbuff, q_curr
        nonlocal tb3_data, tb3buff_data, t_ratecode_data, q_list_data, child_list_data, child_ratecode_data, product_list_data

        cm_gastno:int = 0
        qsy = None
        bqueasy = None
        zbuff = None
        iftask:string = ""
        mestoken:string = ""
        mesvalue:string = ""
        tokcounter:int = 0
        datum:date = None
        cat_flag:bool = False
        roomnr:int = 0
        dyna:string = ""
        loopi:int = 0
        loopj:int = 0
        loopk:int = 0
        currency:string = ""
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        str:string = ""
        tqueasy = None
        Qsy =  create_buffer("Qsy",Queasy)
        Bqueasy =  create_buffer("Bqueasy",Queasy)
        Zbuff =  create_buffer("Zbuff",Zimkateg)
        Tqueasy =  create_buffer("Tqueasy",Queasy)

        qsy = get_cache (Queasy, {"key": [(eq, 152)]})

        if qsy:
            cat_flag = True

        for qsy in db_session.query(Qsy).filter(
                 (Qsy.key == 2) & (Qsy.logi2)).order_by(Qsy._recid).all():

            for ratecode in db_session.query(Ratecode).filter(
                     (Ratecode.code == qsy.char1)).order_by(Ratecode._recid).all():
                iftask = ratecode.char1[4]
                for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                    if mestoken == "RC":

                        if mesvalue  == (prcode) :
                            dyna = dyna + qsy.char1 + ";"
        for curr_1 in range(1,num_entries(p_list.rmcat_str, ",")  + 1) :
            mesval = trim(entry(curr_1 - 1, p_list.rmcat_str, ","))

            if mesval != "":

                zbuff = get_cache (Zimkateg, {"kurzbez": [(eq, mesval)]})

                if zbuff:
                    roomnr = 0

                    if cat_flag:
                        roomnr = zbuff.typ

                        queasy = get_cache (Queasy, {"key": [(eq, 152)],"number1": [(eq, roomnr)]})

                        if queasy:
                            str = queasy.char1
                    else:
                        roomnr = zbuff.zikatnr
                        str = zbuff.kurzbez

                    if dyna != "":
                        for tokcounter in range(1,num_entries(dyna, ";")  + 1) :
                            mesvalue = trim(entry(tokcounter - 1, dyna, ";"))

                            if mesvalue != "":
                                for datum in date_range(p_list.startperiode,p_list.endperiode) :

                                    queasy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, mesvalue)]})

                                    if queasy:

                                        qsy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, mesvalue)]})
                                        while None != qsy:

                                            bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                                            if bqueasy:
                                                bqueasy.logi2 = True


                                                pass
                                                pass

                                            curr_recid = qsy._recid
                                            qsy = db_session.query(Qsy).filter(
                                                     (Qsy.key == 170) & (Qsy.date1 == datum) & (Qsy.number1 == roomnr) & (Qsy.char1 == mesvalue) & (Qsy._recid > curr_recid)).first()

                                    elif not queasy:
                                        for loopi in range(1,num_entries(p_list.adult_str, ",")  + 1) :

                                            if p_list.child_str != "":
                                                for loopj in range(1,num_entries(p_list.child_str, ",")  + 1) :

                                                    queasy = db_session.query(Queasy).filter(
                                                             (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str))).first()
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
                                                        queasy.char2 = p_list.code
                                                        db_session.commit()

                                                        arrangement = get_cache (Arrangement, {"argtnr": [(eq, p_list.argtnr)]})

                                                        if arrangement:

                                                            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)]})

                                                            if artikel:
                                                                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                                                        if tax_included:
                                                            queasy.deci1 =  to_decimal(p_list.zipreis)
                                                        else:
                                                            queasy.deci1 = to_decimal(round(to_decimal(p_list.zipreis * (1 + serv + vat)) , 0))

                                                        bqueasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, markno)]})

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
                                                                 (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str)) & (Queasy._recid > curr_recid)).first()
                                            else:

                                                queasy = db_session.query(Queasy).filter(
                                                         (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str))).first()
                                                while None != queasy:
                                                    queasy = Queasy()
                                                    db_session.add(queasy)

                                                    queasy.key = 170
                                                    queasy.date1 = datum
                                                    queasy.char1 = mesvalue
                                                    queasy.number1 = roomnr
                                                    queasy.number2 = to_int(entry(loopi - 1, p_list.adult_str, ","))
                                                    queasy.logi2 = True
                                                    queasy.char2 = p_list.code
                                                    db_session.commit()

                                                    arrangement = get_cache (Arrangement, {"argtnr": [(eq, p_list.argtnr)]})

                                                    if arrangement:

                                                        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)]})

                                                        if artikel:
                                                            serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                                                    if tax_included:
                                                        queasy.deci1 =  to_decimal(p_list.zipreis)
                                                    else:
                                                        queasy.deci1 = to_decimal(round(to_decimal(p_list.zipreis * (1 + serv + vat)) , 0))

                                                    bqueasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, markno)]})

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
                                                             (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str)) & (Queasy._recid > curr_recid)).first()
                    else:
                        for datum in date_range(p_list.startperiode,p_list.endperiode) :

                            queasy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, prcode)]})

                            if queasy:

                                qsy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, prcode)]})
                                while None != qsy:

                                    bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                                    if bqueasy:
                                        bqueasy.logi2 = True


                                        pass
                                        pass

                                    curr_recid = qsy._recid
                                    qsy = db_session.query(Qsy).filter(
                                             (Qsy.key == 170) & (Qsy.date1 == datum) & (Qsy.number1 == roomnr) & (Qsy.char1 == (prcode)) & (Qsy._recid > curr_recid)).first()

                            elif not queasy:
                                for loopi in range(1,num_entries(p_list.adult_str, ",")  + 1) :

                                    if p_list.child_str != "":
                                        for loopj in range(1,num_entries(p_list.child_str, ",")  + 1) :

                                            queasy = db_session.query(Queasy).filter(
                                                     (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == (prcode)) & (entry(2, Queasy.char1, ";") == (str))).first()
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
                                                db_session.commit()

                                                arrangement = get_cache (Arrangement, {"argtnr": [(eq, p_list.argtnr)]})

                                                if arrangement:

                                                    artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)]})

                                                    if artikel:
                                                        serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                                                if tax_included:
                                                    queasy.deci1 =  to_decimal(p_list.zipreis)
                                                else:
                                                    queasy.deci1 = to_decimal(round(to_decimal(p_list.zipreis * (1 + serv + vat)) , 0))

                                                bqueasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, markno)]})

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
                                                         (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str)) & (Queasy._recid > curr_recid)).first()
                                    else:

                                        queasy = db_session.query(Queasy).filter(
                                                 (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == (prcode)) & (entry(2, Queasy.char1, ";") == (str))).first()
                                        while None != queasy:
                                            queasy = Queasy()
                                            db_session.add(queasy)

                                            queasy.key = 170
                                            queasy.date1 = datum
                                            queasy.char1 = prcode
                                            queasy.number1 = roomnr
                                            queasy.number2 = to_int(entry(loopi - 1, p_list.adult_str, ","))
                                            queasy.logi2 = True
                                            db_session.commit()

                                            arrangement = get_cache (Arrangement, {"argtnr": [(eq, p_list.argtnr)]})

                                            if arrangement:

                                                artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)]})

                                                if artikel:
                                                    serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, datum, artikel.service_code, artikel.mwst_code))

                                            if tax_included:
                                                queasy.deci1 =  to_decimal(p_list.zipreis)
                                            else:
                                                queasy.deci1 = to_decimal(round(to_decimal(p_list.zipreis * (1 + serv + vat)) , 0))

                                            bqueasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, markno)]})

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
                                                     (Queasy.key == 161) & (entry(0, Queasy.char1, ";") == mesvalue) & (entry(2, Queasy.char1, ";") == (str)) & (Queasy._recid > curr_recid)).first()


    p_list = query(p_list_data, first=True)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if mode_str  == ("insert") :
        check_overlapping()

    if error_flag:
        return generate_output()
    
    create_records()
    
    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "RateCode"
        db_session.commit()

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, p_list.zikatnr)]})

        if zimkateg:
            res_history.aenderung = "Create Contract Rate, Code: " + prcode + " RmType : " + zimkateg.kurzbez +\
                " start:" + to_string(p_list.startperiode) + "|end:" + to_string(p_list.endperiode) +\
                "|adult:" + to_string(adult) + "|rate:" + to_string(p_list.zipreis)


        else:
            res_history.aenderung = "Create Contract Rate, Code: " + prcode +\
                " start:" + to_string(p_list.startperiode) + "|end:" + to_string(p_list.endperiode) +\
                "|adult:" + to_string(adult) + "|rate:" + to_string(p_list.zipreis)


        pass
        pass

    if mode_str  == ("update") :

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1013)]})

        if htparam.feldtyp == 1:
            round_betrag = htparam.finteger
            length_round = length(to_string(round_betrag))

        elif htparam.feldtyp == 5 and num_entries(htparam.fchar, ";") > 1:
            round_betrag = to_int(entry(0, htparam.fchar, ";"))
            length_round = length(to_string(round_betrag))
            round_method = to_int(entry(1, htparam.fchar, ";"))


        create_child_list()
        update_child_rate_dates()
    update_ratecode_dates()
    create_child_list()
    curr_time = to_string(get_current_time_in_seconds(), "HH:MM:SS")


    delete_old_childrate()
    create_childrate()

    for guest_pr in db_session.query(Guest_pr).filter(
             (Guest_pr.code == (prcode))).order_by(Guest_pr._recid).all():

        guest = get_cache (Guest, {"gastnr": [(eq, guest_pr.gastnr)]})

        if guest.endperiode == None or guest.endperiode < p_list.endperiode:
            pass
            guest.endperiode = p_list.endperiode


            pass
    update_bookengine_config()

    return generate_output()