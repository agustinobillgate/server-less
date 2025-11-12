#using conversion tools version: 1.0.0.117

# ========================================================
# Rulita, 21-10-2025 
# Issue :
# - Fix space in string 
# ========================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Htparam, Paramtext, Nightaudit, Nitestor, Hoteldpt, H_artikel, Artikel, H_umsatz

def nt_resumsz():

    prepare_cache ([Htparam, Paramtext, Nightaudit, Nitestor, Hoteldpt, H_artikel, Artikel, H_umsatz])

    long_digit:bool = False
    progname:string = "nt-resumsz.p"
    line:string = ""
    price_decimal:int = 0
    n:int = 0
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    p_width:int = 139
    p_length:int = 56
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    from_date:date = None
    to_date:date = None
    htparam = paramtext = nightaudit = nitestor = hoteldpt = h_artikel = artikel = h_umsatz = None

    output_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":string, "artnr":int, "dept":int, "bezeich":string, "price":Decimal, "anzahl":int, "dnet":Decimal, "proz1":Decimal, "dgros":Decimal, "proz2":Decimal, "mnet":Decimal, "proz3":Decimal, "mgros":Decimal, "proz4":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, progname, line, price_decimal, n, night_type, reihenfolge, line_nr, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, htparam, paramtext, nightaudit, nitestor, hoteldpt, h_artikel, artikel, h_umsatz


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        return {}

    def h_umsatz_list():

        nonlocal long_digit, progname, line, price_decimal, n, night_type, reihenfolge, line_nr, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, htparam, paramtext, nightaudit, nitestor, hoteldpt, h_artikel, artikel, h_umsatz


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,60 + 1) :
            line = line + " "

        # Rulita,
        # - Fix space in string
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + "  " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,60 + 1) :
            line = line + " "
        line = line + "Bill-Date :" + " " + to_string(to_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,60 + 1) :
            line = line + " "
        
        
        # Rulita,
        # - Fix space in string
        line = line + "Page      :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Restaurants Turnover Report by department"
        add_line(line)
        line = ""
        add_line(" ")
        add_line(" ")
        add_line("##end-header")

        for cl_list in query(cl_list_data):
            it_exist = True

            if cl_list.flag.lower()  == ("*").lower() :
                line = to_string(cl_list.artnr, ">>>>9") + " " + to_string(cl_list.bezeich)
                add_line(line)
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "-"
                add_line(line)
                
                # Rulita,
                # - Fix space in string
                line = " " + "Qty ArtNo Description                 Price        DAY NET      %       DAY GROS" + "  " + "     %       " + "MONTH NET      %      MONTH GROS" + "      %"
                add_line(line)
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "-"
                add_line(line)

            elif cl_list.flag == "":

                if not long_digit:
                    line = to_string(cl_list.anzahl, "->>>9") + " " + to_string(cl_list.artnr, ">>>>9") + " " + to_string(cl_list.bezeich, "x(20)") + " " + to_string(cl_list.price, ">,>>>,>>9.99") + " " + to_string(cl_list.dnet, "->>,>>>,>>9.99") + " "

                    if cl_list.proz1 > 999 or cl_list.proz1 < -999:
                        line = line + to_string(cl_list.proz1, "->,>>9") + " "
                    else:
                        line = line + to_string(cl_list.proz1, "->>9.9") + " "
                    line = line + to_string(cl_list.dgros, "->>,>>>,>>9.99") + " "

                    if cl_list.proz2 > 999 or cl_list.proz2 < -999:
                        line = line + to_string(cl_list.proz2, "->,>>9") + " "
                    else:
                        line = line + to_string(cl_list.proz2, "->>9.9") + " "
                    line = line + to_string(cl_list.mnet, "->>>,>>>,>>9.99") + " "

                    if cl_list.proz3 > 999 or cl_list.proz3 < -999:
                        line = line + to_string(cl_list.proz3, "->,>>9") + " "
                    else:
                        line = line + to_string(cl_list.proz3, "->>9.9") + " "
                    line = line + to_string(cl_list.mgros, "->>>,>>>,>>9.99") + " "

                    if cl_list.proz4 > 999 or cl_list.proz4 < -999:
                        line = line + to_string(cl_list.proz4, "->,>>9") + " "
                    else:
                        line = line + to_string(cl_list.proz4, "->>9.9") + " "
                else:
                    line = to_string(cl_list.anzahl, "->>>9") + " " + to_string(cl_list.artnr, ">>>>9") + " " + to_string(cl_list.bezeich, "x(20)") + " " + to_string(cl_list.price, ">>>>,>>>,>>9") + " " + to_string(cl_list.dnet, "->,>>>,>>>,>>9") + " " + to_string(cl_list.proz1, "->>9.9") + " " + to_string(cl_list.dgros, "->,>>>,>>>,>>9") + " " + to_string(cl_list.proz2, "->>9.9") + " " + to_string(cl_list.mnet, "->>,>>>,>>>,>>9") + " " + to_string(cl_list.proz3, "->>9.9") + " " + to_string(cl_list.mgros, "->>,>>>,>>>,>>9") + " " + to_string(cl_list.proz4, "->>9.9")
                add_line(line)

            elif cl_list.flag.lower()  == ("**").lower() :
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "-"
                add_line(line)
                line = ""
                for i in range(1,12 + 1) :
                    line = line + " "

                if not long_digit:
                    
                    # Rulita,
                    # - Fix space in string
                    line = line + to_string(cl_list.bezeich, "x(20)") + "              " + to_string(cl_list.dnet, "->>,>>>,>>9.99") + " "

                    if cl_list.proz1 > 999 or cl_list.proz1 < -999:
                        line = line + to_string(cl_list.proz1, "->,>>9") + " "
                    else:
                        line = line + to_string(cl_list.proz1, "->>9.9") + " "
                    line = line + to_string(cl_list.dgros, "->>,>>>,>>9.99") + " "

                    if cl_list.proz2 > 999 or cl_list.proz2 < -999:
                        line = line + to_string(cl_list.proz2, "->,>>9") + " "
                    else:
                        line = line + to_string(cl_list.proz2, "->>9.9") + " "
                    line = line + to_string(cl_list.mnet, "->>>,>>>,>>9.99") + " "

                    if cl_list.proz3 > 999 or cl_list.proz3 < -999:
                        line = line + to_string(cl_list.proz3, "->,>>9") + " "
                    else:
                        line = line + to_string(cl_list.proz3, "->>9.9") + " "
                    line = line + to_string(cl_list.mgros, "->>>,>>>,>>9.99") + " "

                    if cl_list.proz4 > 999 or cl_list.proz4 < -999:
                        line = line + to_string(cl_list.proz4, "->,>>9") + " "
                    else:
                        line = line + to_string(cl_list.proz4, "->>9.9") + " "
                else:
                    # Rulita,
                    # - Fix space in string
                    line = line + to_string(cl_list.bezeich, "x(20)") + "              " + to_string(cl_list.dnet, "->,>>>,>>>,>>9") + " " + to_string(cl_list.proz1, "->>9.9") + " " + to_string(cl_list.dgros, "->,>>>,>>>,>>9") + " " + to_string(cl_list.proz2, "->>9.9") + " " + to_string(cl_list.mnet, "->>,>>>,>>>,>>9") + " " + to_string(cl_list.proz3, "->>9.9") + " " + to_string(cl_list.mgros, "->>,>>>,>>>,>>9") + " " + to_string(cl_list.proz4, "->>9.9")
                add_line(line)
                add_line(" ")
                add_line(" ")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal long_digit, progname, line, price_decimal, n, night_type, reihenfolge, line_nr, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, htparam, paramtext, nightaudit, nitestor, hoteldpt, h_artikel, artikel, h_umsatz


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        nitestor = get_cache (Nitestor, {"night_type": [(eq, night_type)],"reihenfolge": [(eq, reihenfolge)],"line_nr": [(eq, line_nr)]})

        if not nitestor:
            nitestor = Nitestor()
            db_session.add(nitestor)

            nitestor.night_type = night_type
            nitestor.reihenfolge = reihenfolge
            nitestor.line_nr = line_nr
        nitestor.line = s
        line_nr = line_nr + 1
        pass


    def create_h_umsatz():

        nonlocal long_digit, progname, line, price_decimal, n, night_type, reihenfolge, line_nr, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, htparam, paramtext, nightaudit, nitestor, hoteldpt, h_artikel, artikel, h_umsatz


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        dnet:Decimal = to_decimal("0.0")
        dgros:Decimal = to_decimal("0.0")
        mnet:Decimal = to_decimal("0.0")
        mgros:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        it_exist:bool = False
        serv_vat:bool = False
        fact:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= 1)).order_by(Hoteldpt.num).all():
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = "*"
            cl_list.artnr = hoteldpt.num
            cl_list.bezeich = hoteldpt.depart
            dnet =  to_decimal("0")
            dgros =  to_decimal("0")
            mnet =  to_decimal("0")
            mgros =  to_decimal("0")

            for h_artikel in db_session.query(H_artikel).filter(
                     (H_artikel.artart == 0) & (H_artikel.departement == hoteldpt.num)).order_by(H_artikel.artnr).all():

                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, to_date))
                it_exist = False

                for h_umsatz in db_session.query(H_umsatz).filter(
                         (H_umsatz.artnr == h_artikel.artnr) & (H_umsatz.departement == h_artikel.departement) & (H_umsatz.datum >= from_date) & (H_umsatz.datum <= to_date)).order_by(H_umsatz.datum).all():

                    if not it_exist:
                        it_exist = True
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        cl_list.artnr = h_umsatz.artnr
                        cl_list.dept = h_umsatz.departement
                        cl_list.bezeich = h_artikel.bezeich

                    if h_umsatz.datum == to_date:
                        cl_list.anzahl = h_umsatz.anzahl
                        cl_list.price =  to_decimal(h_artikel.epreis1)
                        cl_list.dnet =  to_decimal(h_umsatz.betrag) / to_decimal(fact)
                        cl_list.dgros =  to_decimal(h_umsatz.betrag)
                        dnet =  to_decimal(dnet) + to_decimal(cl_list.dnet)
                        dgros =  to_decimal(dgros) + to_decimal(cl_list.dgros)
                    cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                    cl_list.mgros =  to_decimal(cl_list.mgros) + to_decimal(h_umsatz.betrag)
                    mnet =  to_decimal(mnet) + to_decimal(h_umsatz.betrag) / to_decimal(fact)
                    mgros =  to_decimal(mgros) + to_decimal(h_umsatz.betrag)

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num)):

                if dnet != 0:
                    cl_list.proz1 =  to_decimal(cl_list.dnet) / to_decimal(dnet) * to_decimal("100")

                if dgros != 0:
                    cl_list.proz2 =  to_decimal(cl_list.dgros) / to_decimal(dgros) * to_decimal("100")
                cl_list.proz3 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")
                cl_list.proz4 =  to_decimal(cl_list.mgros) / to_decimal(mgros) * to_decimal("100")
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
            cl_list.proz3 =  to_decimal("100")
            cl_list.mgros =  to_decimal(mgros)
            cl_list.proz4 =  to_decimal("100")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge
        create_h_umsatz()
        h_umsatz_list()

    return generate_output()