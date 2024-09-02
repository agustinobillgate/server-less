from functions.additional_functions import *
import decimal
from datetime import date

def ratecode_adm_fill_plist_webbl(tb3_char1_1:str, tb3_char1_2:str, tb3_char1_3:str, tb3_char1_4:str):
    book_room = 0
    comp_room = 0
    max_room = 0
    early_discount_list = []
    kickback_discount_list = []
    stay_pay_list = []
    n:int = 0
    ct:str = ""
    fdatum:date = None
    tdatum:date = None
    i:int = 0

    early_discount = kickback_discount = stay_pay = None

    early_discount_list, Early_discount = create_model("Early_discount", {"disc_rate":decimal, "min_days":int, "min_stay":int, "max_occ":int, "from_date":date, "to_date":date})
    kickback_discount_list, Kickback_discount = create_model("Kickback_discount", {"disc_rate":decimal, "max_days":int, "min_stay":int, "max_occ":int})
    stay_pay_list, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal book_room, comp_room, max_room, early_discount_list, kickback_discount_list, stay_pay_list, n, ct, fdatum, tdatum, i


        nonlocal early_discount, kickback_discount, stay_pay
        nonlocal early_discount_list, kickback_discount_list, stay_pay_list
        return {"book_room": book_room, "comp_room": comp_room, "max_room": max_room, "early-discount": early_discount_list, "kickback-discount": kickback_discount_list, "stay-pay": stay_pay_list}

    def init_buff():

        nonlocal book_room, comp_room, max_room, early_discount_list, kickback_discount_list, stay_pay_list, n, ct, fdatum, tdatum, i


        nonlocal early_discount, kickback_discount, stay_pay
        nonlocal early_discount_list, kickback_discount_list, stay_pay_list

        for early_discount in query(early_discount_list):
            early_discount.disc_rate = 0
            early_discount.min_days = 0
            early_discount.min_stay = 0
            early_discount.max_occ = 0
            early_discount.from_date = None
            early_discount.to_date = None

        for kickback_discount in query(kickback_discount_list):
            kickback_discount.disc_rate = 0
            kickback_discount.max_days = 0
            kickback_discount.min_stay = 0
            kickback_discount.max_occ = 0

        for stay_pay in query(stay_pay_list):
            stay_pay.f_date = None
            stay_pay.t_date = None
            stay_pay.stay = 0
            stay_pay.pay = 0


    for i in range(1,10 + 1) :
        kickback_discount = Kickback_discount()
        kickback_discount_list.append(kickback_discount)

    for i in range(1,20 + 1) :
        early_discount = Early_discount()
        early_discount_list.append(early_discount)

    for i in range(1,30 + 1) :
        stay_pay = Stay_pay()
        stay_pay_list.append(stay_pay)

    init_buff()

    if num_entries(tb3_char1_1, ";") >= 2:
        for n in range(1,num_entries(tb3_char1_1, ";") - 1 + 1) :
            ct = entry(n - 1, tb3_char1_1, ";")

            early_discount = query(early_discount_list, filters=(lambda early_discount :early_discount.disc_rate == 0), first=True)
            early_discount.disc_rate = to_int(entry(0, ct, ",")) / 100
            early_discount.min_days = to_int(entry(1, ct, ","))
            early_discount.min_stay = to_int(entry(2, ct, ","))
            early_discount.max_occ = to_int(entry(3, ct, ","))

            if num_entries(ct, ",") >= 5 and trim(entry(4, ct, ",")) != "":
                early_discount.from_date = date_mdy(to_int(substring(entry(4, ct, ",") , 4, 2)) , to_int(substring(entry(4, ct, ",") , 6, 2)) , to_int(substring(entry(4, ct, ",") , 0, 4)))

            if num_entries(ct, ",") >= 6 and trim(entry(5, ct, ",")) != "":
                early_discount.to_date = date_mdy(to_int(substring(entry(5, ct, ",") , 4, 2)) , to_int(substring(entry(5, ct, ",") , 6, 2)) , to_int(substring(entry(5, ct, ",") , 0, 4)))

    if num_entries(tb3_char1_2, ";") >= 2:
        for n in range(1,num_entries(tb3_char1_2, ";") - 1 + 1) :
            ct = entry(n - 1, tb3_char1_2, ";")

            kickback_discount = query(kickback_discount_list, filters=(lambda kickback_discount :kickback_discount.disc_rate == 0), first=True)
            kickback_discount.disc_rate = to_int(entry(0, ct, ",")) / 100
            kickback_discount.max_days = to_int(entry(1, ct, ","))
            kickback_discount.min_stay = to_int(entry(2, ct, ","))
            kickback_discount.max_occ = to_int(entry(3, ct, ","))

    if num_entries(tb3_char1_3, ";") >= 2:
        for n in range(1,num_entries(tb3_char1_3, ";") - 1 + 1) :
            ct = entry(n - 1, tb3_char1_3, ";")

            stay_pay = query(stay_pay_list, filters=(lambda stay_pay :stay_pay.stay == 0), first=True)
            fdatum = date_mdy(to_int(substring(entry(0, ct, ",") , 4, 2)) , to_int(substring(entry(0, ct, ",") , 6, 2)) , to_int(substring(entry(0, ct, ",") , 0, 4)))
            tdatum = date_mdy(to_int(substring(entry(1, ct, ",") , 4, 2)) , to_int(substring(entry(1, ct, ",") , 6, 2)) , to_int(substring(entry(1, ct, ",") , 0, 4)))
            stay_pay.f_date = fdatum
            stay_pay.t_date = tdatum
            stay_pay.stay = to_int(entry(2, ct, ","))
            stay_pay.pay = to_int(entry(3, ct, ","))

    if num_entries(tb3_char1_4, ";") >= 3:
        book_room = to_int(entry(0, tb3_char1_4, ";"))
        comp_room = to_int(entry(1, tb3_char1_4, ";"))
        max_room = to_int(entry(2, tb3_char1_4, ";"))

    return generate_output()