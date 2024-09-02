from functions.additional_functions import *
import decimal
from datetime import date
from models import Nebenst, Calls, Bediener

str_list_list, Str_list = create_model("Str_list", {"nebenstelle":str, "zero_rate":bool, "local":decimal, "ldist":decimal, "ovsea":decimal, "s":str})
cost_list_list, Cost_list = create_model("Cost_list", {"num":int, "name":str})

def calls_deptlistbl(cost_list:List[Cost_list], sorttype:int, cost_center:int, to_cc:int, price_decimal:int, from_date:date, to_date:date, double_currency:bool):
    stattype = 0
    str_list_list = []
    amount1:decimal = 0
    amount2:decimal = 0
    t_local:decimal = 0
    t_ldist:decimal = 0
    t_ovsea:decimal = 0
    curr_bezeich:str = ""
    last_sort:int = 2
    prstr:str = ""
    nebenst = calls = bediener = None
    str_list = cost_list = cost_list_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stattype, str_list_list, amount1, amount2, t_local, t_ldist, t_ovsea, curr_bezeich, last_sort, prstr, nebenst, calls, bediener
        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list
        return {"stattype": stattype, "str-list": str_list_list , "ver": 1}

    def create_list():
        nonlocal stattype, str_list_list, amount1, amount2, t_local, t_ldist, t_ovsea, curr_bezeich, last_sort, prstr, nebenst, calls, bediener
        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        last_dept:int = 0
        last_ext:str = ""
        ext_amt1:decimal = 0
        ext_amt2:decimal = 0
        dept_amt1:decimal = 0
        dept_amt2:decimal = 0
        ext_local:decimal = 0
        ext_ldist:decimal = 0
        ext_ovsea:decimal = 0
        dept_local:decimal = 0
        dept_ldist:decimal = 0
        dept_ovsea:decimal = 0
        from_cost:int = 0
        to_cost:int = 0
        i:int = 0
        str_list_list.clear()

        if cost_center == 0:
            from_cost = 0
            to_cost = 9999
        else:
            from_cost = cost_center

            if to_cc < cost_center:
                to_cost = cost_center
            else:
                to_cost = to_cc
        amount1 = 0
        amount2 = 0
        t_local = 0
        t_ldist = 0
        t_ovsea = 0

        if last_sort == 2:
            nebenst_obj_list = []
            recs = (
                db_session.query(Nebenst, Cost_list)
                # .join(Cost_list,(Cost_list.num == Nebenst.departement) &  
                #                 (Cost_list.num >= from_cost) &  
                #                 (Cost_list.num <= to_cost))
                .filter(
                    (Nebenst.departement != 0)).all()
            )
            for rec in recs:
                rec_dept = query(Cost_list, filters=(
                            lambda Cost_list: Cost_list.num == rec.department and
                                                Cost_list.num >= from_cost and
                                                Cost_list.num <= to_cost
                            ), first=True)
                if rec_dept:
                    print("RecDept:", rec_dept)

            # for nebenst, cost_list in recs:
            #     if nebenst._recid in nebenst_obj_list:
            #         continue
            #     else:
            #         nebenst_obj_list.append(nebenst._recid)

            #     if nebenst.nebstart == 0 or nebenst.nebstart == 1:
            #         stattype = 1
            #     else:
            #         stattype = 0

            #     if last_dept != cost_list.num:

            #         if last_dept != 0:
            #             str_list = Str_list()
            #             str_list_list.append(str_list)

            #             str_list.local = dept_local
            #             str_list.ldist = dept_ldist
            #             str_list.ovsea = dept_ovsea
            #             for i in range(1,19 + 1) :
            #                 str_list.s = str_list.s + " "
            #             str_list.s = str_list.s + to_string(("TOTAL DEPT - " + to_string(last_dept, "9999")) , "x(40)")

            #             if price_decimal == 0:

            #                 if dept_amt1 <= 999999999:
            #                     str_list.s = str_list.s + to_string(dept_amt1, ">,>>>,>>>,>>9")
            #                 else:
            #                     str_list.s = str_list.s + to_string(dept_amt1, ">>>>>>>>>>>>9")
            #             else:
            #                 str_list.s = str_list.s + to_string(dept_amt1, ">>,>>>,>>9.99")

            #             if double_currency or price_decimal != 0:
            #                 str_list.s = str_list.s + to_string(dept_amt2, ">>,>>>,>>9.99")
            #             else:

            #                 if dept_amt2 <= 999999999:
            #                     str_list.s = str_list.s + to_string(dept_amt2, ">>,>>,>>>,>>9")
            #                 else:
            #                     str_list.s = str_list.s + to_string(dept_amt2, ">>>>>>>>>>>>9")
            #             str_list = Str_list()
            #             str_list_list.append(str_list)

            #         str_list = Str_list()
            #         str_list_list.append(str_list)

            #         for i in range(1,19 + 1) :
            #             str_list.s = str_list.s + " "
            #         str_list.s = str_list.s + to_string(to_string(cost_list.num, "9999") + " - " + cost_list.name, "x(24)")
            #         last_dept = cost_list.num
            #         dept_amt1 = 0
            #         dept_amt2 = 0
            #         dept_local = 0
            #         dept_ldist = 0
            #         dept_ovsea = 0
            #     last_ext = ""
            #     ext_amt1 = 0
            #     ext_amt2 = 0
            #     ext_local = 0
            #     ext_ldist = 0
            #     ext_ovsea = 0

            #     recs = (
            #         db_session.query(Calls).filter(
            #                 (Calls.key == 1) &  
            #                 (Calls.buchflag == stattype) &  
            #                 (Calls.nebenstelle == nebenst) &  
            #                 (Calls.datum >= from_date) &  
            #                 (Calls.datum <= to_date) &  
            #                 (Calls.zeit >= 0)
            #             ).all()
            #     )
            #     for calls in recs:
            #         if last_ext == "":
            #             last_ext = calls.nebenstelle

            #         if last_ext != calls.nebenstelle:
            #             str_list = Str_list()
            #             str_list_list.append(str_list)

            #             str_list.local = ext_local
            #             str_list.ldist = ext_ldist
            #             str_list.ovsea = ext_ovsea
            #             for i in range(1,19 + 1) :
            #                 str_list.s = str_list.s + " "
            #             str_list.s = str_list.s + to_string(("TOTAL EXT. - " + last_ext) , "x(40)")

            #             if price_decimal == 0:

            #                 if ext_amt1 <= 999999999:
            #                     str_list.s = str_list.s + to_string(ext_amt1, ">,>>>,>>>,>>9")
            #                 else:
            #                     str_list.s = str_list.s + to_string(ext_amt1, ">>>>>>>>>>>>9")
            #             else:
            #                 str_list.s = str_list.s + to_string(ext_amt1, ">>,>>>,>>9.99")

            #             if double_currency or price_decimal != 0:
            #                 str_list.s = str_list.s + to_string(ext_amt2, ">>,>>>,>>9.99")
            #             else:

            #                 if ext_amt2 <= 999999999:
            #                     str_list.s = str_list.s + to_string(ext_amt2, ">,>>>,>>>,>>9")
            #                 else:
            #                     str_list.s = str_list.s + to_string(ext_amt2, ">>>>>>>>>>>>9")
            #             str_list = Str_list()
            #             str_list_list.append(str_list)

            #             last_ext = calls.nebenstelle
            #             ext_amt1 = 0
            #             ext_amt2 = 0
            #             ext_local = 0
            #             ext_ldist = 0
            #             ext_ovsea = 0


            #         ext_amt1 = ext_amt1 + calls.pabxbetrag
            #         ext_amt2 = ext_amt2 + calls.gastbetrag
            #         dept_amt1 = dept_amt1 + calls.pabxbetrag
            #         dept_amt2 = dept_amt2 + calls.gastbetrag

            #         if substring(calls.rufnummer, 0, 1) != "0":
            #             ext_local = ext_local + calls.pabxbetrag
            #             dept_local = dept_local + calls.pabxbetrag

            #         elif substring(calls.rufnummer, 0, 2) == "00":
            #             ext_ovsea = ext_ovsea + calls.pabxbetrag
            #             dept_ovsea = dept_ovsea + calls.pabxbetrag
            #         else:
            #             ext_ldist = ext_ldist + calls.pabxbetrag
            #             dept_ldist = dept_ldist + calls.pabxbetrag
            #         create_record()

            #     if last_ext != "":
            #         str_list = Str_list()
            #         str_list_list.append(str_list)

            #         str_list.local = ext_local
            #         str_list.ldist = ext_ldist
            #         str_list.ovsea = ext_ovsea
            #         for i in range(1,19 + 1) :
            #             str_list.s = str_list.s + " "
            #         str_list.s = str_list.s + to_string(("TOTAL EXT. - " + last_ext) , "x(40)")

            #         if price_decimal == 0:

            #             if ext_amt1 <= 999999999:
            #                 str_list.s = str_list.s + to_string(ext_amt1, ">,>>>,>>>,>>9")
            #             else:
            #                 str_list.s = str_list.s + to_string(ext_amt1, ">>>>>>>>>>>>9")
            #         else:
            #             str_list.s = str_list.s + to_string(ext_amt1, ">>,>>>,>>9.99")

            #         if double_currency or price_decimal != 0:
            #             str_list.s = str_list.s + to_string(ext_amt2, ">>,>>>,>>9.99")
            #         else:

            #             if ext_amt2 <= 999999999:
            #                 str_list.s = str_list.s + to_string(ext_amt2, ">,>>>,>>>,>>9")
            #             else:
            #                 str_list.s = str_list.s + to_string(ext_amt2, ">>>>>>>>>>>>9")
            #         str_list = Str_list()
            #         str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.local = dept_local
        str_list.ldist = dept_ldist
        str_list.ovsea = dept_ovsea
        for i in range(1,19 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(("TOTAL DEPT - " + to_string(last_dept, "9999")) , "x(40)")

        if price_decimal == 0:
            if dept_amt1 <= 999999999:
                str_list.s = str_list.s + to_string(dept_amt1, ">,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(dept_amt1, ">>>>>>>>>>>>9")
        else:
            str_list.s = str_list.s + to_string(dept_amt1, ">>,>>>,>>9.99")

        if double_currency or price_decimal != 0:
            str_list.s = str_list.s + to_string(dept_amt2, ">>,>>>,>>9.99")
        else:

            if dept_amt2 <= 999999999:
                str_list.s = str_list.s + to_string(dept_amt2, ">,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(dept_amt2, ">>>>>>>>>>>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.local = t_local
        str_list.ldist = t_ldist
        str_list.ovsea = t_ovsea
        for i in range(1,19 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string("GRAND TOTAL", "x(40)")

        if price_decimal == 0:

            if amount1 <= 999999999:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(amount1, ">>??>>>>>>>>9")
        else:
            str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>9.99")

        if double_currency or price_decimal != 0:
            str_list.s = str_list.s + to_string(amount2, ">>,>>>,>>9.99")
        else:

            if amount2 <= 999999999:
                str_list.s = str_list.s + to_string(amount2, ">,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(amount2, ">>>>>>>>>>>>9")

    def create_list1():
        nonlocal stattype, str_list_list, amount1, amount2, t_local, t_ldist, t_ovsea, curr_bezeich, last_sort, prstr, nebenst, calls, bediener
        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        last_dept:int = 0
        last_ext:str = ""
        ext_amt1:decimal = 0
        ext_amt2:decimal = 0
        dept_amt1:decimal = 0
        dept_amt2:decimal = 0
        ext_local:decimal = 0
        ext_ldist:decimal = 0
        ext_ovsea:decimal = 0
        dept_local:decimal = 0
        dept_ldist:decimal = 0
        dept_ovsea:decimal = 0
        from_cost:int = 0
        to_cost:int = 0
        i:int = 0
        usr_amt1:decimal = 0
        usr_amt2:decimal = 0
        it_exist:bool = False
        dept_exist:bool = False
        temp_no:int = 0
        curr_user:str = "Not defined"
        do_it:bool = False
        str_list_list.clear()

        if cost_center == 0:
            from_cost = 0
            to_cost = 9999
        else:
            from_cost = cost_center

            if to_cc < cost_center:
                to_cost = cost_center
            else:
                to_cost = to_cc
        amount1 = 0
        amount2 = 0
        t_local = 0
        t_ldist = 0
        t_ovsea = 0
        ext_local = 0
        ext_ldist = 0
        ext_ovsea = 0
        ext_amt1 = 0
        ext_amt2 = 0

        
        recs = (
            db_session.query(Calls).filter(
                (Calls.key == 1) &  
                (Calls.datum >= from_date) &  
                (Calls.datum <= to_date) &  
                (Calls.zeit >= 0)).all()
        )
        for calls in recs:

            nebenst = db_session.query(Nebenst).filter(
                    (Calls.Nebenstelle == calls.nebenstelle)).first()
            do_it = None != nebenst and nebenst.departement >= from_cost and nebenst.departement <= to_cost

            if do_it:

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == to_int(calls.aufschlag))).first()
                do_it = None != bediener

            if do_it:

                if bediener:
                    curr_bezeich = bediener.username
                else:
                    curr_bezeich = "Unknown"

                if curr_user.lower()  == "not defined":
                    curr_user = curr_bezeich

                if curr_user.lower()  != (curr_bezeich).lower() :
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.s = fill(" ", 19)
                    str_list.s = str_list.s + to_string(("TOTAL USER - " + curr_user) , "x(40)")

                    if price_decimal == 0:

                        if ext_amt1 <= 999999999:
                            str_list.s = str_list.s + to_string(ext_amt1, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(ext_amt1, ">>>>>>>>>>>>9")
                    else:
                        str_list.s = str_list.s + to_string(ext_amt1, ">>,>>>,>>9.99")

                    if double_currency or price_decimal != 0:
                        str_list.s = str_list.s + to_string(ext_amt2, ">>,>>>,>>9.99")
                    else:

                        if ext_amt2 <= 999999999:
                            str_list.s = str_list.s + to_string(ext_amt2, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(ext_amt2, ">>>>>>>>>>>>9")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    curr_user = curr_bezeich
                    dept_local = 0
                    dept_ldist = 0
                    dept_ovsea = 0
                    ext_amt1 = 0
                    ext_amt2 = 0


                create_record()
                ext_amt1 = ext_amt1 + calls.pabxbetrag
                ext_amt2 = ext_amt2 + calls.gastbetrag

                if substring(calls.rufnummer, 0, 1) != "0":
                    dept_local = dept_local + calls.pabxbetrag

                elif substring(calls.rufnummer, 0, 2) == "00":
                    dept_ovsea = dept_ovsea + calls.pabxbetrag
                else:
                    dept_ldist = dept_ldist + calls.pabxbetrag
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.s = fill(" ", 19)
        str_list.s = str_list.s + to_string(("TOTAL USER - " + curr_user) , "x(40)")

        if price_decimal == 0:

            if ext_amt1 <= 999999999:
                str_list.s = str_list.s + to_string(ext_amt1, ">,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(ext_amt1, ">>>>>>>>>>>>9")

    def create_record():
        nonlocal stattype, str_list_list, amount1, amount2, t_local, t_ldist, t_ovsea, curr_bezeich, last_sort, prstr, nebenst, calls, bediener
        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        i:int = 0

        if calls.betriebsnr == 0:
            i = 1
        else:
            i = 2
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.zero_rate = (calls.pabxbetrag == 0 and calls.gastbetrag == 0)
        str_list.s = to_string(calls.nebenstelle, "x(6)") + to_string(calls.datum) + to_string(calls.zeit, "HH:MM") + to_string(calls.rufnummer, "x(24)") + to_string(calls.satz_id, "x(16)")

        if double_currency:

            if calls.leitung >= 10000:
                str_list.s = str_list.s + to_string(calls.pabxbetrag, ">,>>>,>>>,>>9") + to_string(calls.gastbetrag, ">>,>>>,>>9.99") + to_string(calls.dauer, "HH:MM:SS") + to_string(calls.zinr, "x(6)") + to_string(calls.impulse, ">>>>>9") + to_string(to_string(calls.leitung) , "x(4)") + prstr[i - 1] + to_string(calls.sequence, ">>>>>>9")
            else:
                str_list.s = str_list.s + to_string(calls.pabxbetrag, ">,>>>,>>>,>>9") + to_string(calls.gastbetrag, ">>,>>>,>>9.99") + to_string(calls.dauer, "HH:MM:SS") + to_string(calls.zinr, "x(6)") + to_string(calls.impulse, ">>>>>9") + to_string(calls.leitung, ">>>>") + prstr[i - 1] + to_string(calls.sequence, ">>>>>>9")
        else:

            if price_decimal == 0:
                str_list.s = str_list.s + to_string(calls.pabxbetrag, ">,>>>,>>>,>>9") + to_string(calls.gastbetrag, ">,>>>,>>>,>>9")
            else:
                str_list.s = str_list.s + to_string(calls.pabxbetrag, ">>,>>>,>>9.99") + to_string(calls.gastbetrag, ">>,>>>,>>9.99")

            if calls.leitung >= 10000:
                str_list.s = str_list.s + to_string(calls.dauer, "HH:MM:SS") + to_string(calls.zinr, "x(6)") + to_string(calls.impulse, ">>>>>9") + to_string(to_string(calls.leitung) , "x(4)") + prstr[i - 1] + to_string(calls.sequence, ">>>>>>9")
            else:
                str_list.s = str_list.s + to_string(calls.dauer, "HH:MM:SS") + to_string(calls.zinr, "x(6)") + to_string(calls.impulse, ">>>>>9") + to_string(calls.leitung, ">>>>") + prstr[i - 1] + to_string(calls.sequence, ">>>>>>9")

        if sorttype == 1:

            if bediener:
                str_list.s = str_list.s + " " + bediener.username
        amount1 = amount1 + calls.pabxbetrag
        amount2 = amount2 + calls.gastbetrag

        if substring(calls.rufnummer, 0, 1) != "0":
            t_local = t_local + calls.pabxbetrag

        elif substring(calls.rufnummer, 0, 2) == "00":
            t_ovsea = t_ovsea + calls.pabxbetrag
        else:
            t_ldist = t_ldist + calls.pabxbetrag

    if sorttype == 0:
        create_list()
    else:
        create_list1()

    return generate_output()