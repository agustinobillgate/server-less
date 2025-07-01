#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Queasy, Artikel, Hoteldpt

def prepare_select_article_drrbl(case_type:int, departement:int):

    prepare_cache ([Htparam, Queasy, Artikel, Hoteldpt])

    c_862:int = 0
    c_892:int = 0
    str1:string = ""
    str2:string = ""
    str3:string = ""
    dept:int = 0
    dept1:int = 0
    food:string = ""
    bev:string = ""
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
    n21:int = 0
    str_list_list = []
    zwkum:int = 0
    zwkum1:int = 0
    htparam = queasy = artikel = hoteldpt = None

    str_list = pay_list = outlet_list = stat_list = None

    str_list_list, Str_list = create_model("Str_list", {"nr":int, "bezeich":string, "used":bool})
    pay_list_list, Pay_list = create_model("Pay_list", {"artnr":int, "flag":bool})
    outlet_list_list, Outlet_list = create_model("Outlet_list", {"artnr":int, "departement":int, "flag":string, "flag_used":bool})
    stat_list_list, Stat_list = create_model("Stat_list", {"artnr":int, "zwkum":int, "flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_862, c_892, str1, str2, str3, dept, dept1, food, bev, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10, st11, st12, st13, st14, st15, st16, st17, st18, st19, st20, st21, st22, n, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, str_list_list, zwkum, zwkum1, htparam, queasy, artikel, hoteldpt
        nonlocal case_type, departement


        nonlocal str_list, pay_list, outlet_list, stat_list
        nonlocal str_list_list, pay_list_list, outlet_list_list, stat_list_list

        return {"str-list": str_list_list}

    zwkum = departement

    htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
    c_862 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 892)]})
    c_892 = htparam.finteger

    queasy = get_cache (Queasy, {"key": [(eq, 265)]})

    if queasy:
        str1 = queasy.char1
        str2 = queasy.char2
        str3 = queasy.char3

    pay_list = query(pay_list_list, first=True)

    if not pay_list:
        for n in range(1,num_entries(str1, ";")  + 1) :
            st1 = entry(n - 1, str1, ";")

            if substring(st1, 0, 9) == ("$payment$").lower()  and substring(st1, 9, 3) == ("YES").lower() :
                st2 = substring(st1, 13)
                for n1 in range(1,num_entries(st2, ",")  + 1) :
                    pay_list = Pay_list()
                    pay_list_list.append(pay_list)

                    pay_list.artnr = to_int(entry(n1 - 1, st2, ","))
                    pay_list.flag = True

            elif substring(st1, 0, 8) == ("$ledger$").lower()  and substring(st1, 8, 3) == ("YES").lower() :
                st3 = substring(st1, 12)
                for n2 in range(1,num_entries(st3, ",")  + 1) :
                    pay_list = Pay_list()
                    pay_list_list.append(pay_list)

                    pay_list.artnr = to_int(entry(n2 - 1, st3, ","))
                    pay_list.flag = True

            elif substring(st1, 0, 6) == ("$cash$").lower()  and substring(st1, 6, 3) == ("YES").lower() :
                st4 = substring(st1, 10)
                for n3 in range(1,num_entries(st4, ",")  + 1) :
                    pay_list = Pay_list()
                    pay_list_list.append(pay_list)

                    pay_list.artnr = to_int(entry(n3 - 1, st4, ","))
                    pay_list.flag = True

            elif substring(st1, 0, 9) == ("$foreign$").lower()  and substring(st1, 9, 3) == ("YES").lower() :
                st5 = substring(st1, 13)
                for n4 in range(1,num_entries(st5, ",")  + 1) :
                    pay_list = Pay_list()
                    pay_list_list.append(pay_list)

                    pay_list.artnr = to_int(entry(n4 - 1, st5, ","))
                    pay_list.flag = True

            elif substring(st1, 0, 9) == ("$deposit$").lower()  and substring(st1, 9, 3) == ("YES").lower() :
                st6 = substring(st1, 13)
                for n5 in range(1,num_entries(st6, ",")  + 1) :
                    pay_list = Pay_list()
                    pay_list_list.append(pay_list)

                    pay_list.artnr = to_int(entry(n5 - 1, st6, ","))
                    pay_list.flag = True

            elif substring(st1, 0, 10) == ("$otherPay$").lower()  and substring(st1, 10, 3) == ("YES").lower() :
                st7 = substring(st1, 14)
                for n6 in range(1,num_entries(st7, ",")  + 1) :
                    pay_list = Pay_list()
                    pay_list_list.append(pay_list)

                    pay_list.artnr = to_int(entry(n6 - 1, st7, ","))
                    pay_list.flag = True
    for n7 in range(1,num_entries(str3, "*")  + 1) :
        st8 = entry(n7 - 1, str3, "*")

        if substring(st8, 0, 9) == ("$FBcover$").lower()  and substring(st8, 9, 3) == ("YES").lower() :
            st13 = substring(st8, 12)


            for n11 in range(1,num_entries(st13, ";")  + 1) :
                st14 = entry(n11 - 1, st13, ";")
                for n12 in range(1,num_entries(st14, "|")  + 1) :
                    st15 = entry(n12 - 1, st14, "|")

                    if n12 == 1 and st15 != "":
                        dept1 = to_int(st15)

                    elif st15 != "" and n12 > 1:
                        for n13 in range(1,num_entries(st15, "-")  + 1) :
                            st16 = entry(n13 - 1, st15, "-")
                            st17 = substring(st16, 1)
                            for n14 in range(1,num_entries(st17, ",")  + 1) :
                                outlet_list = Outlet_list()
                                outlet_list_list.append(outlet_list)

                                outlet_list.departement = dept1
                                outlet_list.artnr = to_int(entry(n14 - 1, st17, ","))
                                outlet_list.flag = "FBcover"
                                outlet_list.flag_used = True

        if substring(st8, 0, 9) == ("$FBsales$").lower()  and substring(st8, 9, 3) == ("YES").lower() :
            st18 = substring(st8, 12)


            for n15 in range(1,num_entries(st18, ",")  + 1) :
                outlet_list = Outlet_list()
                outlet_list_list.append(outlet_list)

                outlet_list.departement = to_int(entry(n15 - 1, st18, ","))
                outlet_list.flag = "FBsales"
                outlet_list.flag_used = True

    if case_type == 1:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 7)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.artnr == artikel.artnr), first=True)

            if pay_list:
                str_list.used = True

    elif case_type == 2:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 2)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.artnr == artikel.artnr), first=True)

            if pay_list:
                str_list.used = True

    elif case_type == 3:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 6) & (Artikel.umsatzart == 0)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.artnr == artikel.artnr), first=True)

            if pay_list:
                str_list.used = True

    elif case_type == 4:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 6) & (Artikel.umsatzart == 4)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.artnr == artikel.artnr), first=True)

            if pay_list:
                str_list.used = True

    elif case_type == 5:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artart == 5)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.artnr == artikel.artnr), first=True)

            if pay_list:
                str_list.used = True

    elif case_type == 6:

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = hoteldpt.num
            str_list.bezeich = hoteldpt.depart

            outlet_list = query(outlet_list_list, filters=(lambda outlet_list: outlet_list.flag.lower()  == ("FBsales").lower()  and outlet_list.departement == hoteldpt.num), first=True)

            if outlet_list:
                str_list.used = True

    elif case_type == 7:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            outlet_list = query(outlet_list_list, filters=(lambda outlet_list: outlet_list.flag.lower()  == ("Outlet").lower()  and outlet_list.artnr == artikel.artnr and outlet_list.departemen == departement), first=True)

            if outlet_list:
                str_list.used = True

    elif case_type == 8:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.endkum == c_862) & (Artikel.departement == departement) & (Artikel.umsatzart == 5)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            outlet_list = query(outlet_list_list, filters=(lambda outlet_list: outlet_list.flag.lower()  == ("FBcover").lower()  and outlet_list.artnr == artikel.artnr and outlet_list.departemen == departement), first=True)

            if outlet_list:
                str_list.used = True

    elif case_type == 9:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.endkum == c_892) & (Artikel.departement == departement) & (Artikel.umsatzart == 6)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            outlet_list = query(outlet_list_list, filters=(lambda outlet_list: outlet_list.flag.lower()  == ("FBcover").lower()  and outlet_list.artnr == artikel.artnr and outlet_list.departemen == departement), first=True)

            if outlet_list:
                str_list.used = True

    elif case_type == 10:

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.umsatzart == 1) & (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 11:

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.umsatzart == 4) & (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

    elif case_type == 12:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.zwkum == 26) & (Artikel.endkum == 36) & (Artikel.departement == departement)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            pay_list = query(pay_list_list, filters=(lambda pay_list: pay_list.artnr == artikel.artnr), first=True)

            if pay_list:
                str_list.used = True

    elif case_type == 13:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.zwkum == zwkum) & (Artikel.departement == 0)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.artnr == artikel.artnr), first=True)

            if stat_list:
                str_list.used = True

    elif case_type == 14:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artnr < 3000) & (Artikel.departement == departement) & (Artikel.umsatzart < 5)).order_by(Artikel._recid).all():
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.nr = artikel.artnr
            str_list.bezeich = artikel.bezeich

            outlet_list = query(outlet_list_list, filters=(lambda outlet_list: outlet_list.flag.lower()  == ("FBcover").lower()  and outlet_list.artnr == artikel.artnr and outlet_list.departemen == departement), first=True)

            if outlet_list:
                str_list.used = True

    return generate_output()