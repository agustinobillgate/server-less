from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from models import Htparam, Hoteldpt, H_artikel, H_umsatz

def resumz_list_btn_gobl(ldry_flag:bool, ldry:int, dstore:int, from_dept:int, to_dept:int, from_date:date, to_date:date, detailed:bool, long_digit:bool):
    output_list_list = []
    htparam = hoteldpt = h_artikel = h_umsatz = None

    output_list = cl_list = None

    output_list_list, Output_list = create_model("Output_list", {"mqty":int, "str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":str, "artnr":int, "dept":int, "bezeich":str, "dnet":decimal, "proz1":decimal, "dgros":decimal, "proz2":decimal, "mqty":int, "mnet":decimal, "proz3":decimal, "mgros":decimal, "proz4":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, htparam, hoteldpt, h_artikel, h_umsatz


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list
        return {"output-list": output_list_list}

    def create_h_umsatz():

        nonlocal output_list_list, htparam, hoteldpt, h_artikel, h_umsatz


        nonlocal output_list, cl_list
        nonlocal output_list_list, cl_list_list

        dnet:decimal = 0
        dgros:decimal = 0
        mnet:decimal = 0
        mgros:decimal = 0
        vat:decimal = 0
        serv:decimal = 0
        it_exist:bool = False
        serv_vat:bool = False
        fact:decimal = 0
        mqty:int = 0
        curr_ldry:int = 0
        curr_dstore:int = 0
        do_it:bool = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical
        output_list_list.clear()
        cl_list_list.clear()

        if ldry_flag:
            curr_ldry = ldry
            curr_dstore = dstore

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= from_dept) &  (Hoteldpt.num <= to_dept) &  (Hoteldpt.num != curr_ldry) &  (Hoteldpt.num != curr_dstore)).all():
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.flag = "*"
            cl_list.bezeich = to_string(hoteldpt.num) + " - " + hoteldpt.depart
            dnet = 0
            dgros = 0
            mnet = 0
            mgros = 0
            mqty = 0

            for h_artikel in db_session.query(H_artikel).filter(
                    ((H_artikel.artart == 0) |  (H_artikel.artart == 8)) &  (H_artikel.departement == hoteldpt.num)).all():
                it_exist = False
                serv = 0
                vat = 0

                for h_umsatz in db_session.query(H_umsatz).filter(
                        (H_umsatz.artnr == h_artikel.artnr) &  (H_umsatz.departement == h_artikel.departement) &  (H_umsatz.datum >= from_date) &  (H_umsatz.datum <= to_date)).all():
                    serv, vat = get_output(calc_servvat(h_umsatz.departement, h_umsatz.artnr, h_umsatz.datum, h_artikel.service_code, h_artikel.mwst_code))
                    fact = 1.00 + serv + vat

                    if not it_exist:
                        it_exist = True
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.artnr = h_umsatz.artnr
                        cl_list.dept = h_umsatz.departement
                        cl_list.bezeich = h_artikel.bezeich

                    if h_umsatz.datum == to_date:
                        cl_list.dnet = h_umsatz.betrag / fact
                        cl_list.dgros = h_umsatz.betrag
                        dnet = dnet + cl_list.dnet
                        dgros = dgros + cl_list.dgros
                    cl_list.mnet = cl_list.mnet + h_umsatz.betrag / fact
                    cl_list.mgros = cl_list.mgros + h_umsatz.betrag
                    cl_list.mqty = cl_list.mqty + h_umsatz.anzahl
                    mnet = mnet + h_umsatz.betrag / fact
                    mgros = mgros + h_umsatz.betrag
                    mqty = mqty + h_umsatz.anzahl

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num)):

                if dnet != 0:
                    cl_list.proz1 = cl_list.dnet / dnet * 100

                if dgros != 0:
                    cl_list.proz2 = cl_list.dgros / dgros * 100
                cl_list.proz3 = cl_list.mnet / mnet * 100
                cl_list.proz4 = cl_list.mgros / mgros * 100
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.flag = "**"
            cl_list.bezeich = "T O T A L"
            cl_list.dnet = dnet

            if dnet != 0:
                cl_list.proz1 = 100
            cl_list.dgros = dgros

            if dgros != 0:
                cl_list.proz2 = 100
            cl_list.mnet = mnet
            cl_list.proz3 = 100
            cl_list.mgros = mgros
            cl_list.proz4 = 100
            cl_list.mqty = mqty

        for cl_list in query(cl_list_list):

            if cl_list.flag.lower()  == "*":
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = to_string(cl_list.artnr, ">>>>>>>>>") + to_string(cl_list.bezeich, "x(24)")

            elif cl_list.flag == "":
                do_it = False

                if detailed or cl_list.mgros != 0:
                    do_it = True

                if do_it:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.mqty = cl_list.mqty

                    if not long_digit:
                        output_list.str = to_string(cl_list.artnr, ">>>>>>>>>") + to_string(cl_list.bezeich, "x(24)") + to_string(cl_list.dnet, "->>,>>>,>>9.99") + to_string(cl_list.dgros, "->>,>>>,>>9.99")

                        if cl_list.proz2 > 999 or cl_list.proz2 < -999:
                            output_list.str = output_list.str + to_string(cl_list.proz2, "->>,>>9")
                        else:
                            output_list.str = output_list.str + to_string(cl_list.proz2, "->>9.99")
                        output_list.str = output_list.str + to_string(cl_list.mnet, "->>>,>>>,>>9.99") + to_string(cl_list.mgros, "->>>,>>>,>>9.99")

                        if cl_list.proz4 > 999 or cl_list.proz4 < -999:
                            output_list.str = output_list.str + to_string(cl_list.proz4, "->>,>>9")
                        else:
                            output_list.str = output_list.str + to_string(cl_list.proz4, "->>9.99")
                    else:
                        output_list.str = to_string(cl_list.artnr, ">>>>>>>>>") + to_string(cl_list.bezeich, "x(24)") + to_string(cl_list.dnet, "->,>>>,>>>,>>9") + to_string(cl_list.dgros, "->,>>>,>>>,>>9") + to_string(cl_list.proz2, "->>9.99") + to_string(cl_list.mnet, "->>,>>>,>>>,>>9") + to_string(cl_list.mgros, "->>,>>>,>>>,>>9") + to_string(cl_list.proz4, "->>9.99")

            elif cl_list.flag.lower()  == "**":
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.mqty = cl_list.mqty

                if not long_digit:
                    output_list.str = to_string(cl_list.artnr, ">>>>>>>>>") + to_string(cl_list.bezeich, "x(24)") + to_string(cl_list.dnet, "->>,>>>,>>9.99") + to_string(cl_list.dgros, "->>,>>>,>>9.99")

                    if cl_list.proz2 > 999 or cl_list.proz2 < -999:
                        output_list.str = output_list.str + to_string(cl_list.proz2, "->>,>>9")
                    else:
                        output_list.str = output_list.str + to_string(cl_list.proz2, "->>9.99")
                    output_list.str = output_list.str + to_string(cl_list.mnet, "->>>,>>>,>>9.99") + to_string(cl_list.mgros, "->>>,>>>,>>9.99")

                    if cl_list.proz4 > 999 or cl_list.proz4 < -999:
                        output_list.str = output_list.str + to_string(cl_list.proz4, "->>,>>9")
                    else:
                        output_list.str = output_list.str + to_string(cl_list.proz4, "->>9.99")
                else:
                    output_list.str = to_string(cl_list.artnr, ">>>>>>>>>") + to_string(cl_list.bezeich, "x(24)") + to_string(cl_list.dnet, "->,>>>,>>>,>>9") + to_string(cl_list.dgros, "->,>>>,>>>,>>9") + to_string(cl_list.proz2, "->>9.99") + to_string(cl_list.mnet, "->>,>>>,>>>,>>9") + to_string(cl_list.mgros, "->>,>>>,>>>,>>9") + to_string(cl_list.proz4, "->>9.99")
                output_list = Output_list()
                output_list_list.append(output_list)


    create_h_umsatz()

    return generate_output()