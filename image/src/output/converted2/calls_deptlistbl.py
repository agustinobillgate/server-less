#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Nebenst, Calls, Bediener

cost_list_list, Cost_list = create_model("Cost_list", {"num":int, "name":string})

def calls_deptlistbl(cost_list_list:[Cost_list], sorttype:int, cost_center:int, to_cc:int, price_decimal:int, from_date:date, to_date:date, double_currency:bool):

    prepare_cache ([Calls])

    stattype = 0
    str_list_list = []
    amount1:Decimal = to_decimal("0.0")
    amount2:Decimal = to_decimal("0.0")
    t_local:Decimal = to_decimal("0.0")
    t_ldist:Decimal = to_decimal("0.0")
    t_ovsea:Decimal = to_decimal("0.0")
    curr_bezeich:string = ""
    last_sort:int = 2
    prstr:List[string] = ["False", "True"]
    nebenst = calls = bediener = None

    str_list = cost_list = None

    str_list_list, Str_list = create_model("Str_list", {"nebenstelle":string, "zero_rate":bool, "local":Decimal, "ldist":Decimal, "ovsea":Decimal, "s":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal stattype, str_list_list, amount1, amount2, t_local, t_ldist, t_ovsea, curr_bezeich, last_sort, prstr, nebenst, calls, bediener
        nonlocal sorttype, cost_center, to_cc, price_decimal, from_date, to_date, double_currency


        nonlocal str_list, cost_list
        nonlocal str_list_list

        return {"cost-list": cost_list_list, "stattype": stattype, "str-list": str_list_list}

    def create_list():

        nonlocal stattype, str_list_list, amount1, amount2, t_local, t_ldist, t_ovsea, curr_bezeich, last_sort, prstr, nebenst, calls, bediener
        nonlocal sorttype, cost_center, to_cc, price_decimal, from_date, to_date, double_currency


        nonlocal str_list, cost_list
        nonlocal str_list_list

        last_dept:int = 0
        last_ext:string = ""
        ext_amt1:Decimal = to_decimal("0.0")
        ext_amt2:Decimal = to_decimal("0.0")
        dept_amt1:Decimal = to_decimal("0.0")
        dept_amt2:Decimal = to_decimal("0.0")
        ext_local:Decimal = to_decimal("0.0")
        ext_ldist:Decimal = to_decimal("0.0")
        ext_ovsea:Decimal = to_decimal("0.0")
        dept_local:Decimal = to_decimal("0.0")
        dept_ldist:Decimal = to_decimal("0.0")
        dept_ovsea:Decimal = to_decimal("0.0")
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
        amount1 =  to_decimal("0")
        amount2 =  to_decimal("0")
        t_local =  to_decimal("0")
        t_ldist =  to_decimal("0")
        t_ovsea =  to_decimal("0")

        if last_sort == 2:

            nebenst_obj_list = {}
            for nebenst in db_session.query(Nebenst).filter(
                     (Nebenst.departement != 0)).order_by(Nebenst.departement, Nebenst.nebenstelle).all():
                cost_list = query(cost_list_list, (lambda cost_list: cost_list.num == nebenst.departement and cost_list.num >= from_cost and cost_list.num <= to_cost), first=True)
                if not cost_list:
                    continue

                if nebenst_obj_list.get(nebenst._recid):
                    continue
                else:
                    nebenst_obj_list[nebenst._recid] = True

                if nebenst.nebstart == 0 or nebenst.nebstart == 1:
                    stattype = 1
                else:
                    stattype = 0

                if last_dept != cost_list.num:

                    if last_dept != 0:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.local =  to_decimal(dept_local)
                        str_list.ldist =  to_decimal(dept_ldist)
                        str_list.ovsea =  to_decimal(dept_ovsea)
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
                                str_list.s = str_list.s + to_string(dept_amt2, ">>,>>,>>>,>>9")
                            else:
                                str_list.s = str_list.s + to_string(dept_amt2, ">>>>>>>>>>>>9")
                        str_list = Str_list()
                        str_list_list.append(str_list)

                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,19 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(to_string(cost_list.num, "9999") + " - " + cost_list.name, "x(24)")
                    last_dept = cost_list.num
                    dept_amt1 =  to_decimal("0")
                    dept_amt2 =  to_decimal("0")
                    dept_local =  to_decimal("0")
                    dept_ldist =  to_decimal("0")
                    dept_ovsea =  to_decimal("0")
                last_ext = ""
                ext_amt1 =  to_decimal("0")
                ext_amt2 =  to_decimal("0")
                ext_local =  to_decimal("0")
                ext_ldist =  to_decimal("0")
                ext_ovsea =  to_decimal("0")

                for calls in db_session.query(Calls).filter(
                         (Calls.key == 1) & (Calls.nebenstelle == nebenst.nebenstelle) & (Calls.datum >= from_date) & (Calls.datum <= to_date) & (Calls.zeit >= 0)).order_by(Calls.nebenstelle, Calls.datum.desc(), Calls.zeit.desc()).all():

                    if last_ext == "":
                        last_ext = calls.nebenstelle

                    if last_ext != calls.nebenstelle:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        str_list.local =  to_decimal(ext_local)
                        str_list.ldist =  to_decimal(ext_ldist)
                        str_list.ovsea =  to_decimal(ext_ovsea)
                        for i in range(1,19 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(("TOTAL EXT. - " + last_ext) , "x(40)")

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

                        last_ext = calls.nebenstelle
                        ext_amt1 =  to_decimal("0")
                        ext_amt2 =  to_decimal("0")
                        ext_local =  to_decimal("0")
                        ext_ldist =  to_decimal("0")
                        ext_ovsea =  to_decimal("0")


                    ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                    ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)
                    dept_amt1 =  to_decimal(dept_amt1) + to_decimal(calls.pabxbetrag)
                    dept_amt2 =  to_decimal(dept_amt2) + to_decimal(calls.gastbetrag)

                    if substring(calls.rufnummer, 0, 1) != ("0").lower() :
                        ext_local =  to_decimal(ext_local) + to_decimal(calls.pabxbetrag)
                        dept_local =  to_decimal(dept_local) + to_decimal(calls.pabxbetrag)

                    elif substring(calls.rufnummer, 0, 2) == ("00").lower() :
                        ext_ovsea =  to_decimal(ext_ovsea) + to_decimal(calls.pabxbetrag)
                        dept_ovsea =  to_decimal(dept_ovsea) + to_decimal(calls.pabxbetrag)
                    else:
                        ext_ldist =  to_decimal(ext_ldist) + to_decimal(calls.pabxbetrag)
                        dept_ldist =  to_decimal(dept_ldist) + to_decimal(calls.pabxbetrag)
                    create_record()

                if last_ext != "":
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    str_list.local =  to_decimal(ext_local)
                    str_list.ldist =  to_decimal(ext_ldist)
                    str_list.ovsea =  to_decimal(ext_ovsea)
                    for i in range(1,19 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(("TOTAL EXT. - " + last_ext) , "x(40)")

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

        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.local =  to_decimal(dept_local)
        str_list.ldist =  to_decimal(dept_ldist)
        str_list.ovsea =  to_decimal(dept_ovsea)
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

        str_list.local =  to_decimal(t_local)
        str_list.ldist =  to_decimal(t_ldist)
        str_list.ovsea =  to_decimal(t_ovsea)
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
        nonlocal sorttype, cost_center, to_cc, price_decimal, from_date, to_date, double_currency


        nonlocal str_list, cost_list
        nonlocal str_list_list

        last_dept:int = 0
        last_ext:string = ""
        ext_amt1:Decimal = to_decimal("0.0")
        ext_amt2:Decimal = to_decimal("0.0")
        dept_amt1:Decimal = to_decimal("0.0")
        dept_amt2:Decimal = to_decimal("0.0")
        ext_local:Decimal = to_decimal("0.0")
        ext_ldist:Decimal = to_decimal("0.0")
        ext_ovsea:Decimal = to_decimal("0.0")
        dept_local:Decimal = to_decimal("0.0")
        dept_ldist:Decimal = to_decimal("0.0")
        dept_ovsea:Decimal = to_decimal("0.0")
        from_cost:int = 0
        to_cost:int = 0
        i:int = 0
        usr_amt1:Decimal = to_decimal("0.0")
        usr_amt2:Decimal = to_decimal("0.0")
        it_exist:bool = False
        dept_exist:bool = False
        temp_no:int = 0
        curr_user:string = "Not defined"
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
        amount1 =  to_decimal("0")
        amount2 =  to_decimal("0")
        t_local =  to_decimal("0")
        t_ldist =  to_decimal("0")
        t_ovsea =  to_decimal("0")
        ext_local =  to_decimal("0")
        ext_ldist =  to_decimal("0")
        ext_ovsea =  to_decimal("0")
        ext_amt1 =  to_decimal("0")
        ext_amt2 =  to_decimal("0")

        for calls in db_session.query(Calls).filter(
                 (Calls.key == 1) & (Calls.datum >= from_date) & (Calls.datum <= to_date) & (Calls.zeit >= 0)).order_by(Calls.aufschlag, Calls.datum.desc(), Calls.zeit.desc()).all():

            nebenst = get_cache (Nebenst, {"nebenstelle": [(eq, calls.nebenstelle)]})
            do_it = None != nebenst and nebenst.departement >= from_cost and nebenst.departement <= to_cost

            if do_it:

                bediener = get_cache (Bediener, {"nr": [(eq, to_int(calls.aufschlag))]})
                do_it = None != bediener

            if do_it:

                if bediener:
                    curr_bezeich = bediener.username
                else:
                    curr_bezeich = "Unknown"

                if curr_user.lower()  == ("not defined").lower() :
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
                    dept_local =  to_decimal("0")
                    dept_ldist =  to_decimal("0")
                    dept_ovsea =  to_decimal("0")
                    ext_amt1 =  to_decimal("0")
                    ext_amt2 =  to_decimal("0")


                create_record()
                ext_amt1 =  to_decimal(ext_amt1) + to_decimal(calls.pabxbetrag)
                ext_amt2 =  to_decimal(ext_amt2) + to_decimal(calls.gastbetrag)

                if substring(calls.rufnummer, 0, 1) != ("0").lower() :
                    dept_local =  to_decimal(dept_local) + to_decimal(calls.pabxbetrag)

                elif substring(calls.rufnummer, 0, 2) == ("00").lower() :
                    dept_ovsea =  to_decimal(dept_ovsea) + to_decimal(calls.pabxbetrag)
                else:
                    dept_ldist =  to_decimal(dept_ldist) + to_decimal(calls.pabxbetrag)
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
        nonlocal sorttype, cost_center, to_cc, price_decimal, from_date, to_date, double_currency


        nonlocal str_list, cost_list
        nonlocal str_list_list

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
        amount1 =  to_decimal(amount1) + to_decimal(calls.pabxbetrag)
        amount2 =  to_decimal(amount2) + to_decimal(calls.gastbetrag)

        if substring(calls.rufnummer, 0, 1) != ("0").lower() :
            t_local =  to_decimal(t_local) + to_decimal(calls.pabxbetrag)

        elif substring(calls.rufnummer, 0, 2) == ("00").lower() :
            t_ovsea =  to_decimal(t_ovsea) + to_decimal(calls.pabxbetrag)
        else:
            t_ldist =  to_decimal(t_ldist) + to_decimal(calls.pabxbetrag)

    if sorttype == 0:
        create_list()
    else:
        create_list1()

    return generate_output()