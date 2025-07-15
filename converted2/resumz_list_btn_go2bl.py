#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, Hoteldpt, H_artikel, H_umsatz

def resumz_list_btn_go2bl(ldry_flag:bool, ldry:int, dstore:int, from_dept:int, to_dept:int, from_date:date, to_date:date, detailed:bool, long_digit:bool):

    prepare_cache ([Htparam, Hoteldpt, H_artikel, H_umsatz])

    turn_reportlist_data = []
    htparam = hoteldpt = h_artikel = h_umsatz = None

    output_list = turn_reportlist = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"dqty":int, "mqty":int, "yqty":int, "bezeich":string, "str":string})
    turn_reportlist_data, Turn_reportlist = create_model("Turn_reportlist", {"artno":int, "descr":string, "day_net":Decimal, "day_gros":Decimal, "day_proz":Decimal, "todate_mnet":Decimal, "todate_mgros":Decimal, "todate_mproz":Decimal, "todate_ynet":Decimal, "todate_ygros":Decimal, "todate_yproz":Decimal, "dqty":int, "mqty":int, "yqty":int})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "artnr":int, "dept":int, "bezeich":string, "dnet":Decimal, "proz1":Decimal, "dgros":Decimal, "proz2":Decimal, "dqty":int, "mqty":int, "mnet":Decimal, "proz3":Decimal, "mgros":Decimal, "proz4":Decimal, "yqty":int, "ynet":Decimal, "proz5":Decimal, "ygros":Decimal, "proz6":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal turn_reportlist_data, htparam, hoteldpt, h_artikel, h_umsatz
        nonlocal ldry_flag, ldry, dstore, from_dept, to_dept, from_date, to_date, detailed, long_digit


        nonlocal output_list, turn_reportlist, cl_list
        nonlocal output_list_data, turn_reportlist_data, cl_list_data

        return {"turn-reportlist": turn_reportlist_data}

    def create_h_umsatz():

        nonlocal turn_reportlist_data, htparam, hoteldpt, h_artikel, h_umsatz
        nonlocal ldry_flag, ldry, dstore, from_dept, to_dept, from_date, to_date, detailed, long_digit


        nonlocal output_list, turn_reportlist, cl_list
        nonlocal output_list_data, turn_reportlist_data, cl_list_data

        dnet:Decimal = to_decimal("0.0")
        dgros:Decimal = to_decimal("0.0")
        mnet:Decimal = to_decimal("0.0")
        mgros:Decimal = to_decimal("0.0")
        ynet:Decimal = to_decimal("0.0")
        ygros:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        it_exist:bool = False
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")
        dqty:int = 0
        mqty:int = 0
        yqty:int = 0
        curr_ldry:int = 0
        curr_dstore:int = 0
        do_it:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical
        output_list_data.clear()
        cl_list_data.clear()

        if ldry_flag:
            curr_ldry = ldry
            curr_dstore = dstore

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept) & (Hoteldpt.num != curr_ldry) & (Hoteldpt.num != curr_dstore)).order_by(Hoteldpt.num).all():
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = "*"
            cl_list.bezeich = to_string(hoteldpt.num) + " - " + hoteldpt.depart
            dqty = 0
            dnet =  to_decimal("0")
            dgros =  to_decimal("0")
            mnet =  to_decimal("0")
            mgros =  to_decimal("0")
            mqty = 0
            ynet =  to_decimal("0")
            ygros =  to_decimal("0")
            yqty = 0

            for h_artikel in db_session.query(H_artikel).filter(
                     ((H_artikel.artart == 0) | (H_artikel.artart == 8)) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.artnr).all():
                it_exist = False
                serv =  to_decimal("0")
                vat =  to_decimal("0")

                for h_umsatz in db_session.query(H_umsatz).filter(
                         (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date)).order_by(H_umsatz.datum).all():
                    serv, vat = get_output(calc_servvat(h_umsatz.departement, h_umsatz.artnr, h_umsatz.datum, h_artikel.service_code, h_artikel.mwst_code))
                    fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

                    if not it_exist:
                        it_exist = True
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.artnr = h_umsatz.artnr
                        cl_list.dept = h_umsatz.departement
                        cl_list.bezeich = h_artikel.bezeich

                    if h_umsatz.datum == to_date:
                        cl_list.dqty = h_umsatz.anzahl
                        cl_list.dnet =  to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        cl_list.dgros =  to_decimal(h_umsatz.betrag)
                        dqty = dqty + cl_list.dqty
                        dnet =  to_decimal(dnet) + to_decimal(cl_list.dnet)
                        dgros =  to_decimal(dgros) + to_decimal(cl_list.dgros)

                    if get_month(h_umsatz.datum) == get_month(to_date) and get_year(h_umsatz.datum) == get_year(to_date):
                        cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        cl_list.mgros =  to_decimal(cl_list.mgros) + to_decimal(h_umsatz.betrag)
                        cl_list.mqty = cl_list.mqty + h_umsatz.anzahl
                        mnet =  to_decimal(mnet) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        mgros =  to_decimal(mgros) + to_decimal(h_umsatz.betrag)
                        mqty = mqty + h_umsatz.anzahl
                    cl_list.ynet =  to_decimal(cl_list.ynet) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                    cl_list.ygros =  to_decimal(cl_list.ygros) + to_decimal(h_umsatz.betrag)
                    cl_list.yqty = cl_list.yqty + h_umsatz.anzahl
                    ynet =  to_decimal(ynet) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                    ygros =  to_decimal(ygros) + to_decimal(h_umsatz.betrag)
                    yqty = yqty + h_umsatz.anzahl

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num)):

                if dnet != 0:
                    cl_list.proz1 =  to_decimal(cl_list.dnet) / to_decimal(dnet) * to_decimal("100")

                if dgros != 0:
                    cl_list.proz2 =  to_decimal(cl_list.dgros) / to_decimal(dgros) * to_decimal("100")

                if mnet != 0:
                    cl_list.proz3 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")

                if mgros != 0:
                    cl_list.proz4 =  to_decimal(cl_list.mgros) / to_decimal(mgros) * to_decimal("100")

                if ynet != 0:
                    cl_list.proz5 =  to_decimal(cl_list.ynet) / to_decimal(ynet) * to_decimal("100")

                if ygros != 0:
                    cl_list.proz6 =  to_decimal(cl_list.ygros) / to_decimal(ygros) * to_decimal("100")
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = "**"
            cl_list.bezeich = "T O T A L"
            cl_list.dnet =  to_decimal(dnet)

            if dnet != 0:
                cl_list.proz1 =  to_decimal("100")
            cl_list.dgros =  to_decimal(dgros)

            if dgros != 0:
                cl_list.proz2 =  to_decimal("100")
            cl_list.mnet =  to_decimal(mnet)

            if mnet != 0:
                cl_list.proz3 =  to_decimal("100")
            cl_list.mgros =  to_decimal(mgros)

            if mgros != 0:
                cl_list.proz4 =  to_decimal("100")
            cl_list.dqty = dqty
            cl_list.mqty = mqty
            cl_list.ynet =  to_decimal(ynet)

            if ynet != 0:
                cl_list.proz5 =  to_decimal("100")
            cl_list.ygros =  to_decimal(ygros)

            if ygros != 0:
                cl_list.proz6 =  to_decimal("100")
            cl_list.yqty = yqty

        for cl_list in query(cl_list_data):

            if cl_list.flag.lower()  == ("*").lower() :
                turn_reportlist = Turn_reportlist()
                turn_reportlist_data.append(turn_reportlist)

                turn_reportlist.artno = to_int(to_string(cl_list.artnr, ">>>>>>>>>"))

            elif cl_list.flag == "":
                do_it = False

                if detailed or cl_list.mgros != 0:
                    do_it = True

                if do_it:
                    turn_reportlist = Turn_reportlist()
                    turn_reportlist_data.append(turn_reportlist)

                    turn_reportlist.dqty = cl_list.dqty
                    turn_reportlist.mqty = cl_list.mqty
                    turn_reportlist.yqty = cl_list.yqty

                    if not long_digit:
                        turn_reportlist.artno = to_int(to_string(cl_list.artnr, ">>>>>>>>>"))
                        turn_reportlist.day_net =  to_decimal(to_decimal(to_string(cl_list.dnet , "->>,>>>,>>9.99")))
                        turn_reportlist.day_gros =  to_decimal(to_decimal(to_string(cl_list.dgros , "->>,>>>,>>9.99")))
                        turn_reportlist.descr = cl_list.bezeich

                        if cl_list.proz2 > 999 or cl_list.proz2 < -999:
                            turn_reportlist.day_proz =  to_decimal(to_decimal(to_string(cl_list.proz2 , "->>,>>9")))
                        else:
                            turn_reportlist.day_proz =  to_decimal(to_decimal(to_string(cl_list.proz2 , "->>9.99")))
                        turn_reportlist.todate_mnet =  to_decimal(to_decimal(to_string(cl_list.mnet , "->>>,>>>,>>9.99")))
                        turn_reportlist.todate_mgros =  to_decimal(to_decimal(to_string(cl_list.mgros , "->>>,>>>,>>9.99")))

                        if cl_list.proz4 > 999 or cl_list.proz4 < -999:
                            turn_reportlist.todate_mproz =  to_decimal(to_decimal(to_string(cl_list.proz4 , "->>,>>9")))
                        else:
                            turn_reportlist.todate_mproz =  to_decimal(to_decimal(to_string(cl_list.proz4 , "->>9.99")))
                        turn_reportlist.todate_ynet =  to_decimal(to_decimal(to_string(cl_list.ynet , "->>>,>>>,>>9.99")))
                        turn_reportlist.todate_ygros =  to_decimal(to_decimal(to_string(cl_list.ygros , "->>>,>>>,>>9.99")))

                        if cl_list.proz6 > 999 or cl_list.proz6 < -999:
                            turn_reportlist.todate_yproz =  to_decimal(to_decimal(to_string(cl_list.proz6 , "->>,>>9")))
                        else:
                            turn_reportlist.todate_yproz =  to_decimal(to_decimal(to_string(cl_list.proz6 , "->>9.99")))
                    else:
                        turn_reportlist.artno = to_int(to_string(cl_list.artnr, ">>>>>>>>>"))
                        turn_reportlist.descr = cl_list.bezeich
                        turn_reportlist.day_net =  to_decimal(to_decimal(to_string(cl_list.dnet , "->,>>>,>>>,>>9")))
                        turn_reportlist.day_gros =  to_decimal(to_decimal(to_string(cl_list.dgros , "->,>>>,>>>,>>9")))
                        turn_reportlist.day_proz =  to_decimal(to_decimal(to_string(cl_list.proz2 , "->>9.99")))
                        turn_reportlist.todate_mnet =  to_decimal(to_decimal(to_string(cl_list.mnet , "->>,>>>,>>>,>>9")))
                        turn_reportlist.todate_mgros =  to_decimal(to_decimal(to_string(cl_list.mgros , "->>,>>>,>>>,>>9")))
                        turn_reportlist.todate_mproz =  to_decimal(to_decimal(to_string(cl_list.proz4 , "->>9.99")))
                        turn_reportlist.todate_ynet =  to_decimal(to_decimal(to_string(cl_list.ynet , "->>,>>>,>>>,>>9")))
                        turn_reportlist.todate_ygros =  to_decimal(to_decimal(to_string(cl_list.ygros , "->>,>>>,>>>,>>9")))
                        turn_reportlist.todate_yproz =  to_decimal(to_decimal(to_string(cl_list.proz6 , "->>9.99")))

            elif cl_list.flag.lower()  == ("**").lower() :
                turn_reportlist = Turn_reportlist()
                turn_reportlist_data.append(turn_reportlist)

                turn_reportlist.dqty = cl_list.dqty
                turn_reportlist.mqty = cl_list.mqty
                turn_reportlist.yqty = cl_list.yqty

                if not long_digit:
                    turn_reportlist.artno = to_int(to_string(cl_list.artnr, ">>>>>>>>>"))
                    turn_reportlist.day_net =  to_decimal(to_decimal(to_string(cl_list.dnet , "->>,>>>,>>9.99")))
                    turn_reportlist.day_gros =  to_decimal(to_decimal(to_string(cl_list.dgros , "->>,>>>,>>9.99")))
                    turn_reportlist.descr = cl_list.bezeich

                    if cl_list.proz2 > 999 or cl_list.proz2 < -999:
                        turn_reportlist.day_proz =  to_decimal(to_decimal(to_string(cl_list.proz2 , "->>,>>9")))
                    else:
                        turn_reportlist.day_proz =  to_decimal(to_decimal(to_string(cl_list.proz2 , "->>9.99")))
                    turn_reportlist.todate_mnet =  to_decimal(to_decimal(to_string(cl_list.mnet , "->>>,>>>,>>9.99")))
                    turn_reportlist.todate_mgros =  to_decimal(to_decimal(to_string(cl_list.mgros , "->>>,>>>,>>9.99")))

                    if cl_list.proz4 > 999 or cl_list.proz4 < -999:
                        turn_reportlist.todate_mproz =  to_decimal(to_decimal(to_string(cl_list.proz4 , "->>,>>9")))
                    else:
                        turn_reportlist.todate_mproz =  to_decimal(to_decimal(to_string(cl_list.proz4 , "->>9.99")))
                    turn_reportlist.todate_ynet =  to_decimal(to_decimal(to_string(cl_list.ynet , "->>>,>>>,>>9.99")))
                    turn_reportlist.todate_ygros =  to_decimal(to_decimal(to_string(cl_list.ygros , "->>>,>>>,>>9.99")))

                    if cl_list.proz6 > 999 or cl_list.proz6 < -999:
                        turn_reportlist.todate_yproz =  to_decimal(to_decimal(to_string(cl_list.proz6 , "->>,>>9")))
                    else:
                        turn_reportlist.todate_yproz =  to_decimal(to_decimal(to_string(cl_list.proz6 , "->>9.99")))
                else:
                    turn_reportlist.artno = to_int(to_string(cl_list.artnr, ">>>>>>>>>"))
                    turn_reportlist.descr = cl_list.bezeich
                    turn_reportlist.day_net =  to_decimal(to_decimal(to_string(cl_list.dnet , "->,>>>,>>>,>>9")))
                    turn_reportlist.day_gros =  to_decimal(to_decimal(to_string(cl_list.dgros , "->,>>>,>>>,>>9")))
                    turn_reportlist.day_proz =  to_decimal(to_decimal(to_string(cl_list.proz2 , "->>9.99")))
                    turn_reportlist.todate_mnet =  to_decimal(to_decimal(to_string(cl_list.mnet , "->>,>>>,>>>,>>9")))
                    turn_reportlist.todate_mgros =  to_decimal(to_decimal(to_string(cl_list.mgros , "->>,>>>,>>>,>>9")))
                    turn_reportlist.todate_mproz =  to_decimal(to_decimal(to_string(cl_list.proz4 , "->>9.99")))
                    turn_reportlist.todate_ynet =  to_decimal(to_decimal(to_string(cl_list.ynet , "->>,>>>,>>>,>>9")))
                    turn_reportlist.todate_ygros =  to_decimal(to_decimal(to_string(cl_list.ygros , "->>,>>>,>>>,>>9")))
                    turn_reportlist.todate_yproz =  to_decimal(to_decimal(to_string(cl_list.proz6 , "->>9.99")))
                turn_reportlist = Turn_reportlist()
                turn_reportlist_data.append(turn_reportlist)


    from_date = date_mdy(1, 1, get_year(to_date))
    turn_reportlist_data.clear()
    create_h_umsatz()

    return generate_output()