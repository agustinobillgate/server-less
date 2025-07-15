#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Queasy

def prepare_setup_new_drr():

    prepare_cache ([Hoteldpt, Queasy])

    resto_list_data = []
    fbcover_list_data = []
    paxcover_list_data = []
    pay_list_data = []
    statistic_list_data = []
    outlets_list_data = []
    gsheet_link = ""
    str1:string = ""
    str2:string = ""
    str3:string = ""
    st1:string = ""
    st2:string = ""
    st3:string = ""
    st4:string = ""
    st5:string = ""
    st6:string = ""
    st7:string = ""
    st8:string = ""
    st9:string = ""
    st10:string = ""
    st11:string = ""
    st12:string = ""
    st13:string = ""
    st14:string = ""
    st15:string = ""
    st16:string = ""
    st17:string = ""
    st18:string = ""
    st19:string = ""
    st20:string = ""
    st21:string = ""
    st22:string = ""
    n:int = 0
    n1:int = 0
    n2:int = 0
    n3:int = 0
    n4:int = 0
    n5:int = 0
    n6:int = 0
    n7:int = 0
    n8:int = 0
    n9:int = 0
    n10:int = 0
    n11:int = 0
    n12:int = 0
    n13:int = 0
    n14:int = 0
    n15:int = 0
    n16:int = 0
    n17:int = 0
    n18:int = 0
    n19:int = 0
    n20:int = 0
    hoteldpt = queasy = None

    resto_list = fbcover_list = paxcover_list = setup_list = pay_list = statistic_list = outlets_list = outlets_info = fbcover_info = None

    resto_list_data, Resto_list = create_model("Resto_list", {"deptnr":int, "departement":string, "artikel":string, "resto_info":string})
    fbcover_list_data, Fbcover_list = create_model("Fbcover_list", {"deptnr":int, "departement":string, "food":string, "beverage":string, "material":string})
    paxcover_list_data, Paxcover_list = create_model("Paxcover_list", {"deptnr":int, "departement":string, "artikel":string})
    setup_list_data, Setup_list = create_model("Setup_list", {"payment":string, "statistic":string, "outlets":string})
    pay_list_data, Pay_list = create_model("Pay_list", {"payment_flag":string, "ledger_flag":string, "cash_flag":string, "foreign_flag":string, "deposit_flag":string, "other_pay_flag":string, "artnr_payment":string, "artnr_ledger":string, "artnr_cash":string, "artnr_foreign":string, "artnr_deposit":string, "artnr_other_pay":string})
    statistic_list_data, Statistic_list = create_model("Statistic_list", {"fo_rev_flag":string, "other_income_flag":string, "segment_rev_flag":string, "statistic_flag":string, "artnr_fo":string, "artnr_other":string, "fo_info":string, "other_info":string, "segmentcode":string, "segment_info":string, "statistic_zwkum":string, "statistic_artnr":string, "statistic_info":string})
    outlets_list_data, Outlets_list = create_model("Outlets_list", {"outlets_flag":string, "fbcover_flag":string, "fbsales_flag":string, "outlets_info":string, "fbcover_info":string, "fbsales_info":string})
    outlets_info_data, Outlets_info = create_model("Outlets_info", {"deptnr":int, "artnr":string, "otls_info":string})
    fbcover_info_data, Fbcover_info = create_model("Fbcover_info", {"deptnr":int, "food":string, "beverage":string, "material":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resto_list_data, fbcover_list_data, paxcover_list_data, pay_list_data, statistic_list_data, outlets_list_data, gsheet_link, str1, str2, str3, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, hoteldpt, queasy


        nonlocal resto_list, fbcover_list, paxcover_list, setup_list, pay_list, statistic_list, outlets_list, outlets_info, fbcover_info
        nonlocal resto_list_data, fbcover_list_data, paxcover_list_data, setup_list_data, pay_list_data, statistic_list_data, outlets_list_data, outlets_info_data, fbcover_info_data

        return {"resto-list": resto_list_data, "fbcover-list": fbcover_list_data, "paxcover-list": paxcover_list_data, "pay-list": pay_list_data, "statistic-list": statistic_list_data, "outlets-list": outlets_list_data, "gsheet_link": gsheet_link}

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num != 0)).order_by(Hoteldpt._recid).all():
        resto_list = Resto_list()
        resto_list_data.append(resto_list)

        resto_list.deptnr = hoteldpt.num
        resto_list.departement = hoteldpt.depart


        fbcover_list = Fbcover_list()
        fbcover_list_data.append(fbcover_list)

        fbcover_list.deptnr = hoteldpt.num
        fbcover_list.departement = hoteldpt.depart


        paxcover_list = Paxcover_list()
        paxcover_list_data.append(paxcover_list)

        paxcover_list.deptnr = hoteldpt.num
        paxcover_list.departement = hoteldpt.depart

    queasy = get_cache (Queasy, {"key": [(eq, 265)]})

    if queasy:
        str1 = queasy.char1
        str2 = queasy.char2
        str3 = queasy.char3

    pay_list = query(pay_list_data, first=True)

    if not pay_list:
        pay_list = Pay_list()
        pay_list_data.append(pay_list)

        for n in range(1,num_entries(str1, ";")  + 1) :
            st1 = entry(n - 1, str1, ";")

            if substring(st1, 0, 9) == ("$payment$").lower()  and substring(st1, 9, 3) == ("YES").lower() :
                pay_list.payment_flag = substring(st1, 9, 3)
                pay_list.artnr_payment = substring(st1, 13)

            elif substring(st1, 0, 8) == ("$ledger$").lower()  and substring(st1, 8, 3) == ("YES").lower() :
                pay_list.ledger_flag = substring(st1, 8, 3)
                pay_list.artnr_ledger = substring(st1, 12)

            elif substring(st1, 0, 6) == ("$cash$").lower()  and substring(st1, 6, 3) == ("YES").lower() :
                pay_list.cash_flag = substring(st1, 6, 3)
                pay_list.artnr_cash = substring(st1, 10)

            elif substring(st1, 0, 9) == ("$foreign$").lower()  and substring(st1, 9, 3) == ("YES").lower() :
                pay_list.foreign_flag = substring(st1, 9, 3)
                pay_list.artnr_foreign = substring(st1, 13)

            elif substring(st1, 0, 9) == ("$deposit$").lower()  and substring(st1, 9, 3) == ("YES").lower() :
                pay_list.deposit_flag = substring(st1, 9, 3)
                pay_list.artnr_deposit = substring(st1, 13)

            elif substring(st1, 0, 10) == ("$otherPay$").lower()  and substring(st1, 10, 3) == ("YES").lower() :
                pay_list.other_pay_flag = substring(st1, 10, 3)
                pay_list.artnr_other = substring(st1, 14)

            elif substring(st1, 0, 8) == ("$Gsheet$").lower() :
                gsheet_link = substring(st1, 8)

    statistic_list = query(statistic_list_data, first=True)

    if not statistic_list:
        statistic_list = Statistic_list()
        statistic_list_data.append(statistic_list)

        for n1 in range(1,num_entries(str2, ";")  + 1) :
            st2 = entry(n1 - 1, str2, ";")

            if substring(st2, 0, 11) == ("$FOrevenue$").lower()  and substring(st2, 11, 3) == ("YES").lower() :
                statistic_list.fo_rev_flag = substring(st2, 11, 3)
                statistic_list.fo_info = substring(st2, 15)


                st3 = substring(st2, 15, 9999)
                for n2 in range(1,num_entries(st3, ",")  + 1) :
                    st4 = entry(n2 - 1, st3, ",")
                    statistic_list.artnr_fo = statistic_list.artnr_fo + entry(0, st4, "-") + ","

            if substring(st2, 0, 13) == ("$otherincome$").lower()  and substring(st2, 13, 3) == ("YES").lower() :
                statistic_list.other_income_flag = substring(st2, 13, 3)
                statistic_list.other_info = substring(st2, 17)


                st5 = substring(st2, 17, 9999)
                for n3 in range(1,num_entries(st5, ",")  + 1) :
                    st6 = entry(n3 - 1, st5, ",")
                    statistic_list.artnr_other = statistic_list.artnr_other + entry(0, st6, "-") + ","

            if substring(st2, 0, 9) == ("$segment$").lower()  and substring(st2, 9, 3) == ("YES").lower() :
                statistic_list.segment_rev_flag = substring(st2, 9, 3)
                statistic_list.segment_info = substring(st2, 13)


                st13 = substring(st2, 13)
                for n11 in range(1,num_entries(st13, ",")  + 1) :
                    st14 = entry(n11 - 1, st13, ",")
                    statistic_list.segmentcode = statistic_list.segmentcode + entry(0, st14, "-") + ","

            if substring(st2, 0, 11) == ("$statistic$").lower()  and substring(st2, 11, 3) == ("YES").lower() :
                statistic_list.statistic_flag = substring(st2, 11, 3)
                st16 = substring(st2, 15)


                statistic_list.statistic_zwkum = entry(0, st16, "/")
                st17 = entry(1, st16, "/")
                statistic_list.statistic_info = st17
                for n14 in range(1,num_entries(st17, ",")  + 1) :
                    st18 = entry(n14 - 1, st17, ",")

                    if entry(0, st18, "-") != "":
                        statistic_list.statistic_artnr = statistic_list.statistic_artnr + entry(0, st18, "-") + ","

    outlets_list = query(outlets_list_data, first=True)

    if not outlets_list:
        outlets_list = Outlets_list()
        outlets_list_data.append(outlets_list)

        for n4 in range(1,num_entries(str3, "*")  + 1) :
            st7 = entry(n4 - 1, str3, "*")

            if substring(st7, 0, 16) == ("$revenueOutlets$").lower()  and substring(st7, 16, 3) == ("YES").lower() :
                outlets_list.outlets_flag = substring(st7, 16, 3)
                outlets_list.outlets_info = substring(st7, 19)


                for n6 in range(1,num_entries(outlets_list.outlets_info, ";")  + 1) :
                    st8 = entry(n6 - 1, outlets_list.outlets_info, ";")
                    for n7 in range(1,num_entries(st8, "|")  + 1) :
                        st9 = entry(n7 - 1, st8, "|")

                        if st9 != "" and n7 == 1:
                            outlets_info = Outlets_info()
                            outlets_info_data.append(outlets_info)

                            outlets_info.deptnr = to_int(st9)

                        elif st9 != "" and n7 != 1:
                            outlets_info.otls_info = st9


                            for n13 in range(1,num_entries(st9, ",")  + 1) :
                                st15 = entry(n13 - 1, st9, ",")
                                outlets_info.artnr = outlets_info.artnr + entry(0, st15, "-") + ","

            if substring(st7, 0, 9) == ("$FBcover$").lower()  and substring(st7, 9, 3) == ("YES").lower() :
                outlets_list.fbcover_flag = substring(st7, 9, 3)
                outlets_list.fbcover_info = substring(st7, 12)


                for n8 in range(1,num_entries(fbcover_info, ";")  + 1) :
                    st10 = entry(n8 - 1, fbcover_info, ";")
                    fbcover_info = Fbcover_info()
                    fbcover_info_data.append(fbcover_info)

                    for n9 in range(1,num_entries(st10, "|")  + 1) :
                        st11 = entry(n9 - 1, st10, "|")

                        if n9 == 1:
                            fbcover_info.deptnr = to_int(st11)

                        if n9 != 1:
                            for n10 in range(1,num_entries(st11, "-")  + 1) :
                                st12 = entry(n10 - 1, st11, "-")

                                if substring(st12, 0, 1) == ("F").lower() :
                                    fbcover_info.food = substring(st12, 1, 9999)

                                elif substring(st12, 0, 1) == ("B").lower() :
                                    fbcover_info.beverage = substring(st12, 1, 9999)

                                elif substring(st12, 0, 1) == ("M").lower() :
                                    fbcover_info.material = substring(st12, 1, 9999)

            if substring(st7, 0, 9) == ("$FBsales$").lower()  and substring(st7, 9, 3) == ("YES").lower() :
                outlets_list.fbsales_flag = substring(st7, 9, 3)
                outlets_list.fbsales_info = substring(st7, 12)

    for resto_list in query(resto_list_data):

        outlets_info = query(outlets_info_data, filters=(lambda outlets_info: outlets_info.deptnr == resto_list.deptnr), first=True)

        if outlets_info:
            resto_list.artikel = outlets_info.artnr
            resto_list.resto_info = outlets_info.otls_info

    for fbcover_list in query(fbcover_list_data):

        fbcover_info = query(fbcover_info_data, filters=(lambda fbcover_info: fbcover_info.deptnr == fbcover_list.deptnr), first=True)

        if fbcover_info:
            fbcover_list.food = fbcover_info.food
            fbcover_list.beverage = fbcover_info.beverage
            fbcover_list.material = fbcover_info.material

    return generate_output()