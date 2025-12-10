#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 23-10-2025 
# Issue : 
# - New compile program
# - Fix space in string
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import Paramtext, Htparam, Nightaudit, Nitestor, Hoteldpt, Artikel, Umsatz

def nt_foumsz():

    prepare_cache ([Paramtext, Htparam, Nightaudit, Hoteldpt, Artikel, Umsatz])

    long_digit:bool = False
    line:string = ""
    progname:string = "nt-foumsz.p"
    vat_artnr:int = 0
    price_decimal:int = 0
    n:int = 0
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    p_width:int = 121
    p_length:int = 56
    index_nr:int = 0
    from_date:date = None
    to_date:date = None
    htl_name:string = ""
    htl_adr:string = ""
    htl_tel:string = ""
    paramtext = htparam = nightaudit = nitestor = hoteldpt = artikel = umsatz = None

    output_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"nr":int, "flag":string, "artnr":int, "dept":int, "bezeich":string, "dnet":Decimal, "proz1":Decimal, "dgros":Decimal, "proz2":Decimal, "mnet":Decimal, "proz3":Decimal, "mgros":Decimal, "proz4":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, line, progname, vat_artnr, price_decimal, n, night_type, reihenfolge, line_nr, p_width, p_length, index_nr, from_date, to_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, hoteldpt, artikel, umsatz


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        return {}

    def umsatz_list():

        nonlocal long_digit, line, progname, vat_artnr, price_decimal, n, night_type, reihenfolge, line_nr, p_width, p_length, index_nr, from_date, to_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, hoteldpt, artikel, umsatz


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,45 + 1) :
            line = line + " "
        
        # Rulita,
        # - Fix space in string
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + "  " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,45 + 1) :
            line = line + " "
        line = line + "Bill-Date :" + " " + to_string(to_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,45 + 1) :
            line = line + " "

        # Rulita,
        # - Fix space in string
        line = line + "Page      :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Turnover Report by department"
        add_line(line)
        line = ""
        add_line(" ")
        add_line(" ")
        add_line("##end-header")

        for cl_list in query(cl_list_data, sort_by=[("nr",False)]):
            it_exist = True

            if cl_list.flag.lower()  == ("*").lower() :
                line = to_string(cl_list.artnr, ">>>9") + " " + to_string(cl_list.bezeich)
                add_line(line)
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "-"
                add_line(line)

                # Rulita,
                # - Fix space in string
                line = " " + "Art Description                 DAY NET       %       DAY GROS" \
                    + " " + "       %         " + "MONTH NET       %       MONTH GROS       %"
                add_line(line)
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "-"
                add_line(line)

            elif cl_list.flag == "":

                if not long_digit and price_decimal == 2:
                    line = to_string(cl_list.artnr, ">>>9") + " " + to_string(cl_list.bezeich, "x(20)") + " " + to_string(cl_list.dnet, "->>,>>>,>>9.99") + " " + to_string(cl_list.proz1, "->>9.99") + " " + to_string(cl_list.dgros, "->>,>>>,>>9.99") + " " + to_string(cl_list.proz2, "->>9.99") + " " + to_string(cl_list.mnet, " ->>>,>>>,>>9.99") + " " + to_string(cl_list.proz3, "->>9.99") + " " + to_string(cl_list.mgros, " ->>>,>>>,>>9.99") + " " + to_string(cl_list.proz4, "->>9.99")
                else:
                    line = to_string(cl_list.artnr, ">>>9") + " " + to_string(cl_list.bezeich, "x(20)") + " " + to_string(cl_list.dnet, "->,>>>,>>>,>>9") + " " + to_string(cl_list.proz1, "->>9.99") + " " + to_string(cl_list.dgros, "->,>>>,>>>,>>9") + " " + to_string(cl_list.proz2, "->>9.99") + " " + to_string(cl_list.mnet, "->>>,>>>,>>>,>>9") + " " + to_string(cl_list.proz3, "->>9.99") + " " + to_string(cl_list.mgros, "->>>,>>>,>>>,>>9") + " " + to_string(cl_list.proz4, "->>9.99")
                add_line(line)

            elif cl_list.flag.lower()  == ("**").lower() :
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "-"
                add_line(line)
                line = ""
                for i in range(1,5 + 1) :
                    line = line + " "

                if not long_digit and price_decimal == 2:
                    line = line + to_string(cl_list.bezeich, "x(20)") + " " + to_string(cl_list.dnet, "->>,>>>,>>9.99") + " " + to_string(cl_list.proz1, "->>9.99") + " " + to_string(cl_list.dgros, "->>,>>>,>>9.99") + " " + to_string(cl_list.proz2, "->>9.99") + " " + to_string(cl_list.mnet, " ->>>,>>>,>>9.99") + " " + to_string(cl_list.proz3, "->>9.99") + " " + to_string(cl_list.mgros, " ->>>,>>>,>>9.99") + " " + to_string(cl_list.proz4, "->>9.99")
                else:
                    line = line + to_string(cl_list.bezeich, "x(20)") + " " + to_string(cl_list.dnet, "->,>>>,>>>,>>9") + " " + to_string(cl_list.proz1, "->>9.99") + " " + to_string(cl_list.dgros, "->,>>>,>>>,>>9") + " " + to_string(cl_list.proz2, "->>9.99") + " " + to_string(cl_list.mnet, "->>>,>>>,>>>,>>9") + " " + to_string(cl_list.proz3, "->>9.99") + " " + to_string(cl_list.mgros, "->>>,>>>,>>>,>>9") + " " + to_string(cl_list.proz4, "->>9.99")
                add_line(line)
                add_line(" ")
                add_line(" ")
        add_line("##end-of-file")


    def add_line(s:string):

        nonlocal long_digit, line, progname, vat_artnr, price_decimal, n, night_type, reihenfolge, line_nr, p_width, p_length, index_nr, from_date, to_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, hoteldpt, artikel, umsatz


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


    def create_umsatz():

        nonlocal long_digit, line, progname, vat_artnr, price_decimal, n, night_type, reihenfolge, line_nr, p_width, p_length, index_nr, from_date, to_date, htl_name, htl_adr, htl_tel, paramtext, htparam, nightaudit, nitestor, hoteldpt, artikel, umsatz


        nonlocal output_list, cl_list
        nonlocal output_list_data, cl_list_data

        dnet:Decimal = to_decimal("0.0")
        dgros:Decimal = to_decimal("0.0")
        mnet:Decimal = to_decimal("0.0")
        mgros:Decimal = to_decimal("0.0")
        tdnet:Decimal = to_decimal("0.0")
        tdgros:Decimal = to_decimal("0.0")
        tmnet:Decimal = to_decimal("0.0")
        tmgros:Decimal = to_decimal("0.0")
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        it_exist:bool = False
        serv_vat:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical
        tdnet =  to_decimal("0")
        tdgros =  to_decimal("0")
        tmnet =  to_decimal("0")
        tmgros =  to_decimal("0")

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt.num).all():
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            index_nr = index_nr + 1
            cl_list.nr = index_nr
            cl_list.flag = "*"
            cl_list.artnr = hoteldpt.num
            cl_list.bezeich = hoteldpt.depart


            dnet =  to_decimal("0")
            dgros =  to_decimal("0")
            mnet =  to_decimal("0")
            mgros =  to_decimal("0")

            for artikel in db_session.query(Artikel).filter(
                     ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.departement == hoteldpt.num)).order_by(Artikel.artnr).all():
                it_exist = False

                for umsatz in db_session.query(Umsatz).filter(
                         (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum >= from_date) & (Umsatz.datum <= to_date)).order_by(Umsatz.datum).all():
                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, umsatz.datum))

                    if not it_exist:
                        it_exist = True
                        cl_list = Cl_list()
                        cl_list_data.append(cl_list)

                        index_nr = index_nr + 1
                        cl_list.nr = index_nr
                        cl_list.artnr = umsatz.artnr
                        cl_list.dept = umsatz.departement
                        cl_list.bezeich = artikel.bezeich

                    if umsatz.datum == to_date:

                        if artikel.artnr == vat_artnr and artikel.departement == 0:
                            pass
                        else:
                            cl_list.dnet =  to_decimal(umsatz.betrag) / to_decimal(fact)
                            dnet =  to_decimal(dnet) + to_decimal(cl_list.dnet)
                            tdnet =  to_decimal(tdnet) + to_decimal(cl_list.dnet)
                        cl_list.dgros =  to_decimal(umsatz.betrag)
                        dgros =  to_decimal(dgros) + to_decimal(cl_list.dgros)
                        tdgros =  to_decimal(tdgros) + to_decimal(cl_list.dgros)

                    if artikel.artnr == vat_artnr and artikel.departement == 0:
                        pass
                    else:
                        cl_list.mnet =  to_decimal(cl_list.mnet) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        mnet =  to_decimal(mnet) + to_decimal(umsatz.betrag) / to_decimal(fact)
                        tmnet =  to_decimal(tmnet) + to_decimal(umsatz.betrag) / to_decimal(fact)
                    cl_list.mgros =  to_decimal(cl_list.mgros) + to_decimal(umsatz.betrag)
                    mgros =  to_decimal(mgros) + to_decimal(umsatz.betrag)
                    tmgros =  to_decimal(tmgros) + to_decimal(umsatz.betrag)

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.dept == hoteldpt.num)):

                if dnet != 0:
                    cl_list.proz1 =  to_decimal(cl_list.dnet) / to_decimal(dnet) * to_decimal("100")

                if dgros != 0:
                    cl_list.proz2 =  to_decimal(cl_list.dgros) / to_decimal(dgros) * to_decimal("100")
                cl_list.proz3 =  to_decimal(cl_list.mnet) / to_decimal(mnet) * to_decimal("100")
                cl_list.proz4 =  to_decimal(cl_list.mgros) / to_decimal(mgros) * to_decimal("100")
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            index_nr = index_nr + 1
            cl_list.nr = index_nr
            cl_list.flag = "**"
            cl_list.bezeich = "T O T A L"
            cl_list.dnet =  to_decimal(dnet)
            cl_list.dgros =  to_decimal(dgros)
            cl_list.mnet =  to_decimal(mnet)
            cl_list.proz3 =  to_decimal("100")
            cl_list.mgros =  to_decimal(mgros)
            cl_list.proz4 =  to_decimal("100")

            if dnet != 0:
                cl_list.proz1 =  to_decimal("100")

            if dgros != 0:
                cl_list.proz2 =  to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        index_nr = index_nr + 1
        cl_list.nr = index_nr
        cl_list.flag = "**"
        cl_list.bezeich = "GRAND TOTAL"
        cl_list.dnet =  to_decimal(tdnet)
        cl_list.dgros =  to_decimal(tdgros)
        cl_list.mnet =  to_decimal(tmnet)
        cl_list.proz3 =  to_decimal("100")
        cl_list.mgros =  to_decimal(tmgros)
        cl_list.proz4 =  to_decimal("100")

        if tdnet != 0:
            cl_list.proz1 =  to_decimal("100")

        if tdgros != 0:
            cl_list.proz2 =  to_decimal("100")

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})
    vat_artnr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    nightaudit = get_cache (Nightaudit, {"programm": [(eq, progname)]})

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge

        for nitestor in db_session.query(Nitestor).filter(
                 (Nitestor.night_type == night_type) & (Nitestor.reihenfolge == reihenfolge)).with_for_update().order_by(Nitestor._recid).all():
            
            db_session.delete(nitestor)
            
        create_umsatz()
        umsatz_list()

    return generate_output()