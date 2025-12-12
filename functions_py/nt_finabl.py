#using conversion tools version: 1.0.0.117

# =================================================
# Rulita, 23-10-2025 
# Issue : 
# - New compile program
# - Fixing issue condition if with modulo

# Rulita, 30-10-2025 
# Fixing miss table name datum -> segmentstat.datum
# Fixing miss table name datum -> nationstat.datum

# Rahman, 06-11-2025
#   - fixing space on long string
#   - fixing ("string").lower() to only lowercase string

# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext, Nightaudit, Nitestor, Zimmer, Artikel, Umsatz, Hoteldpt, Uebertrag, Segment, Segmentstat, Nation, Nationstat, Zinrstat, Zimkateg, Zkstat

def nt_finabl():
    prepare_cache ([Htparam, Paramtext, Nightaudit, Artikel, Umsatz, Hoteldpt, Uebertrag, Segment, Segmentstat, Nation, Nationstat, Zinrstat, Zimkateg, Zkstat])

    pvilanguage:int = 0
    lvcarea:str = "nt-fina"
    long_digit:bool = False
    n:int = 0
    price_decimal:int = 0
    progname:str = "nt-fina.p"
    night_type:int = 0
    reihenfolge:int = 0
    line_nr:int = 0
    line:str = ""
    p_width:int = 119
    p_length:int = 56
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    from_date:date = None
    to_date:date = None
    loop_i:int = 0
    htparam = paramtext = nightaudit = nitestor = zimmer = artikel = umsatz = hoteldpt = uebertrag = segment = segmentstat = nation = nationstat = zinrstat = zimkateg = zkstat = None

    output_list = cl_list = info_list = cl_list1 = None

    output_list_data, Output_list = create_model(
        "Output_list",
        {
            "str": str
        })
    cl_list_data, Cl_list = create_model(
        "Cl_list",
        {
            "flag": int,
            "proz": int,
            "bezeich": str,
            "dgros": Decimal,
            "mgros": Decimal,
            "ygros": Decimal,
            "lmgros": Decimal,
            "lygros": Decimal
        })
    info_list_data, Info_list = create_model(
        "Info_list",
        {
            "flag": int,
            "room": int,
            "avrm": int,
            "ocrm": int,
            "rcom": int,
            "vacant": int,
            "ooo": int,
            "pers": int,
            "com": int,
            "arrival": int,
            "dayuse": int,
            "lodging": Decimal
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pvilanguage, lvcarea, long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat
        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_data, cl_list_data, info_list_data

        return {}

    def umsatz_list():
        nonlocal pvilanguage, lvcarea, long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat
        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_data, cl_list_data, info_list_data

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,42 + 1) :
            line = line + " "
        line = line + translateExtended ("Date/Time :", lvcarea, "") + " " + to_string(get_current_date()) + " " + to_string(get_current_time_in_seconds(), "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,42 + 1) :
            line = line + " "
        line = line + translateExtended ("Bill-Date :", lvcarea, "") + " " + to_string(to_date)
        add_line(line)
        line = translateExtended ("Tel", lvcarea, "") + " " + to_string(htl_tel, "x(36)")
        for i in range(1,42 + 1) :
            line = line + " "
        line = line + translateExtended("Page      :", lvcarea, "") + " " + "##page"  # Rahman - fix spacing on long string
        add_line(line)
        add_line(" ")
        line = translateExtended ("Finance Recapitulation Report", lvcarea, "")
        add_line(line)
        add_line(" ")
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "_"
        add_line(line)
        line = "                             " + translateExtended(
            "Current year Current year Current year Previous year Previous year", lvcarea, "")  # Rahman - fix spacing on long string
        add_line(line)
        line = "                            " + translateExtended(
            "Effective-day Effective-month Effective-year Effective-month Effective-year", lvcarea, "")  # Rahman - fix spacing on long string
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        line = ""
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_data):
            it_exist = True

            if cl_list.flag == 1:
                fill_line()
                line = ""
                for i in range(1,p_width + 1) :
                    line = line + "-"
                add_line(line)

            elif cl_list.flag >= 2:
                if cl_list.bezeich == "":
                    add_line(" ")

                elif cl_list.bezeich.lower() == "*":
                    cl_list.bezeich = ""
                    fill_line()
                else:
                    fill_line()
        add_line("##end-of-file")


    def fill_line():
        nonlocal pvilanguage, lvcarea, long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat
        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_data, cl_list_data, info_list_data

# Rahman - start fixing space on long string
        if (price_decimal == 2 and cl_list.proz == 0) or cl_list.proz == 1:
            line = to_string(cl_list.bezeich, "x(24)") + " " + \
                to_string(cl_list.dgros, " ->>>,>>>,>>9.99") + " " + \
                to_string(cl_list.mgros, " ->>>,>>>,>>9.99") + " " + \
                to_string(cl_list.ygros, "   ->>>>,>>>,>>9.99") + " " + \
                to_string(cl_list.lmgros, "   ->>>,>>>,>>9.99") + " " + \
                to_string(cl_list.lygros, "   ->>>>,>>>,>>9.99")

        elif cl_list.proz == 2:
            line = to_string(cl_list.bezeich, "x(24)") + " " + \
                to_string(cl_list.dgros, " ->>>,>>>,>>9   ") + " " + \
                to_string(cl_list.mgros, "   ->>>,>>>,>>9   ") + " " + \
                to_string(cl_list.ygros, "   ->>>>,>>>,>>9   ") + " " + \
                to_string(cl_list.lmgros, "   ->>>,>>>,>>9   ") + " " + \
                to_string(cl_list.lygros, "   ->>>>,>>>,>>9   ")
        else:
            line = to_string(cl_list.bezeich, "x(24)") + " " + \
                to_string(cl_list.dgros, "->>>,>>>,>>>,>>9") + " " + \
                to_string(cl_list.mgros, "->,>>>,>>>,>>>,>>9") + " " + \
                to_string(cl_list.ygros, "->>,>>>,>>>,>>>,>>9") + " " + \
                to_string(cl_list.lmgros, "->,>>>,>>>,>>>,>>9") + " " + \
                to_string(cl_list.lygros, "->>,>>>,>>>,>>>,>>9")
        add_line(line)
# end fixing space on long string

    def add_line(s:str):
        nonlocal pvilanguage, lvcarea, long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat
        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_data, cl_list_data, info_list_data

        if s == "":
            s = " "

        nitestor = get_cache (
            Nitestor, {"night_type": [(eq, night_type)],"reihenfolge": [(eq, reihenfolge)],"line_nr": [(eq, line_nr)]})

        if not nitestor:
            nitestor = Nitestor()
            db_session.add(nitestor)

            nitestor.night_type = night_type
            nitestor.reihenfolge = reihenfolge
            nitestor.line_nr = line_nr
        nitestor.line = s
        line_nr = line_nr + 1


    def create_fina():
        nonlocal pvilanguage, lvcarea, long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat
        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_data, cl_list_data, info_list_data

        d:int = 0
        m:int = 0
        y:int = 0
        lm:int = 0
        ly:int = 0
        danz:int = 0
        manz:int = 0
        yanz:int = 0
        lmanz:int = 0
        lyanz:int = 0
        anzroom:int = 0
        i:int = 0
        dgros:Decimal = to_decimal("0.0")
        mgros:Decimal = to_decimal("0.0")
        ygros:Decimal = to_decimal("0.0")
        lmgros:Decimal = to_decimal("0.0")
        lygros:Decimal = to_decimal("0.0")
        outstand:Decimal = to_decimal("0.0")
        jan1:date = None
        ljan1:date = None
        lfdate:date = None
        ltdate:date = None
        datum:date = None
        art1:int = 0
        art2:int = 0
        dd:int = 0
        yy:int = 0
        curr_dept:int = -1
        Cl_list1 = Cl_list
        cl_list1_data = cl_list_data
        dd = get_day(to_date)
        yy = get_year(to_date) - 1
        jan1 = date_mdy(1, 1, get_year(to_date))

        # Rulita
        # - Fixing convert get year - 1 variable ljan1 & lfdate
        ljan1 = date_mdy(1, 1, get_year(to_date) - 1)
        lfdate = date_mdy(get_month(from_date) , get_day(from_date) , get_year(from_date) - 1)

        # Rulita,
        # - Fixing issue condition if with modulo
        # if dd == 29 and (yy modulo 4 != 0):
        #     dd = 28
        if dd == 29 and (yy % 4 != 0):
            dd = 28
        
        ltdate = date_mdy(get_month(to_date) , dd, yy)
        anzroom = 0

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            anzroom = anzroom + 1
        for i in range(1,5 + 1) :
            info_list = Info_list()
            info_list_data.append(info_list)

            info_list.flag = i

        umsatz_obj_list = {}
        umsatz = Umsatz()
        artikel = Artikel()
        for umsatz.betrag, umsatz.datum, umsatz._recid, artikel.departement, artikel.bezeich, artikel.artnr, artikel._recid in db_session.query(Umsatz.betrag, Umsatz.datum, Umsatz._recid, Artikel.departement, Artikel.bezeich, Artikel.artnr, Artikel._recid).join(Artikel,(Artikel.artnr == Umsatz.artnr) & (Artikel.departement == Umsatz.departement) & ((Artikel.artart == 0) | (Artikel.artart == 8))).filter(
                 (((Umsatz.datum >= ljan1) & (Umsatz.datum <= lfdate)) | ((Umsatz.datum >= jan1) & (Umsatz.datum <= to_date)))).order_by(Artikel.departement, Artikel.artnr, Umsatz.datum).all():
            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            if curr_dept != artikel.departement:
                if curr_dept != -1:
                    cl_list.dgros =  to_decimal(dgros)
                    cl_list.mgros =  to_decimal(mgros)
                    cl_list.ygros =  to_decimal(ygros)
                    cl_list.lmgros =  to_decimal(lmgros)
                    cl_list.lygros =  to_decimal(lygros)
                curr_dept = artikel.departement

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.flag = 1
                cl_list.bezeich = hoteldpt.depart
                dgros =  to_decimal("0")
                mgros =  to_decimal("0")
                ygros =  to_decimal("0")
                lmgros =  to_decimal("0")
                lygros =  to_decimal("0")

            if umsatz.datum == to_date:
                dgros =  to_decimal(dgros) + to_decimal(umsatz.betrag)

            if umsatz.datum >= from_date:
                mgros =  to_decimal(mgros) + to_decimal(umsatz.betrag)

            if umsatz.datum >= jan1:
                ygros =  to_decimal(ygros) + to_decimal(umsatz.betrag)

            if umsatz.datum >= lfdate and umsatz.datum <= ltdate:
                lmgros =  to_decimal(lmgros) + to_decimal(umsatz.betrag)

            if umsatz.datum >= ljan1 and umsatz.datum <= ltdate:
                lygros =  to_decimal(lygros) + to_decimal(umsatz.betrag)

        if cl_list:
            cl_list.dgros =  to_decimal(dgros)
            cl_list.mgros =  to_decimal(mgros)
            cl_list.ygros =  to_decimal(ygros)
            cl_list.lmgros =  to_decimal(lmgros)
            cl_list.lygros =  to_decimal(lygros)


        dgros =  to_decimal("0")
        mgros =  to_decimal("0")
        ygros =  to_decimal("0")
        lmgros =  to_decimal("0")
        lygros =  to_decimal("0")

        for cl_list in query(cl_list_data):
            dgros =  to_decimal(dgros) + to_decimal(cl_list.dgros)
            mgros =  to_decimal(mgros) + to_decimal(cl_list.mgros)
            ygros =  to_decimal(ygros) + to_decimal(cl_list.ygros)
            lmgros =  to_decimal(lmgros) + to_decimal(cl_list.lmgros)
            lygros =  to_decimal(lygros) + to_decimal(cl_list.lygros)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 2
        cl_list.bezeich = "*"
        cl_list.dgros =  to_decimal(dgros)
        cl_list.mgros =  to_decimal(mgros)
        cl_list.ygros =  to_decimal(ygros)
        cl_list.lmgros =  to_decimal(lmgros)
        cl_list.lygros =  to_decimal(lygros)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 2

        uebertrag = get_cache (Uebertrag, {"datum": [(eq, to_date - timedelta(days=1))]})

        if uebertrag:
            outstand =  to_decimal(uebertrag.betrag)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 3
        cl_list.bezeich = translateExtended ("YESTERDAY OUTSTANDING", lvcarea, "")
        cl_list.dgros =  to_decimal(outstand)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 3

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 2) | (Artikel.artart == 5) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.departement == 0)).order_by(Artikel.artart, Artikel.bezeich).all():
            dgros =  to_decimal("0")
            mgros =  to_decimal("0")
            ygros =  to_decimal("0")
            lmgros =  to_decimal("0")
            lygros =  to_decimal("0")
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = 4
            cl_list.bezeich = artikel.bezeich

            for umsatz in db_session.query(Umsatz).filter(
                     (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (((Umsatz.datum >= ljan1) & (Umsatz.datum <= lfdate)) | ((Umsatz.datum >= jan1) & (Umsatz.datum <= to_date)))).order_by(Umsatz.datum).all():
                if umsatz.datum == to_date:
                    dgros =  to_decimal(dgros) + to_decimal(umsatz.betrag)

                if umsatz.datum >= from_date:
                    mgros =  to_decimal(mgros) + to_decimal(umsatz.betrag)

                if umsatz.datum >= jan1:
                    ygros =  to_decimal(ygros) + to_decimal(umsatz.betrag)

                if umsatz.datum >= lfdate and umsatz.datum <= ltdate:
                    lmgros =  to_decimal(lmgros) + to_decimal(umsatz.betrag)

                if umsatz.datum >= ljan1 and umsatz.datum <= ltdate:
                    lygros =  to_decimal(lygros) + to_decimal(umsatz.betrag)
            cl_list.dgros =  to_decimal(dgros)
            cl_list.mgros =  to_decimal(mgros)
            cl_list.ygros =  to_decimal(ygros)
            cl_list.lmgros =  to_decimal(lmgros)
            cl_list.lygros =  to_decimal(lygros)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 4
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 5
        cl_list.bezeich = translateExtended ("TODAY OUTSTANDING", lvcarea, "")

        for cl_list1 in query(cl_list1_data, filters=(lambda cl_list1: cl_list1.flag >= 2 and cl_list1.flag <= 4)):
            cl_list.dgros =  to_decimal(cl_list.dgros) + to_decimal(cl_list1.dgros)

        uebertrag = get_cache (Uebertrag, {"datum": [(eq, to_date)]})

        if not uebertrag:
            uebertrag = Uebertrag()
            db_session.add(uebertrag)

            uebertrag.datum = to_date
        uebertrag.betrag =  to_decimal(cl_list.dgros)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 5
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 5

        htparam = get_cache (
            Htparam, {"paramnr": [(eq, 120)]})
        art1 = htparam.finteger

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 6)) & (Artikel.departement == 0)).order_by(Artikel.artart, Artikel.bezeich).all():
            dgros =  to_decimal("0")
            mgros =  to_decimal("0")
            ygros =  to_decimal("0")
            lmgros =  to_decimal("0")
            lygros =  to_decimal("0")
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = 6
            cl_list.bezeich = artikel.bezeich

            for umsatz in db_session.query(Umsatz).filter(
                     (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (((Umsatz.datum >= ljan1) & (Umsatz.datum <= lfdate)) | ((Umsatz.datum >= jan1) & (Umsatz.datum <= to_date)))).order_by(Umsatz.datum).all():

                if umsatz.datum == to_date:
                    dgros =  to_decimal(dgros) + to_decimal(umsatz.betrag)

                if umsatz.datum >= from_date:
                    mgros =  to_decimal(mgros) + to_decimal(umsatz.betrag)

                if umsatz.datum >= jan1:
                    ygros =  to_decimal(ygros) + to_decimal(umsatz.betrag)

                if umsatz.datum >= lfdate and umsatz.datum <= ltdate:
                    lmgros =  to_decimal(lmgros) + to_decimal(umsatz.betrag)

                if umsatz.datum >= ljan1 and umsatz.datum <= ltdate:
                    lygros =  to_decimal(lygros) + to_decimal(umsatz.betrag)
            cl_list.dgros =  - to_decimal(dgros)
            cl_list.mgros =  - to_decimal(mgros)
            cl_list.ygros =  - to_decimal(ygros)
            cl_list.lmgros =  - to_decimal(lmgros)
            cl_list.lygros =  - to_decimal(lygros)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 6
        dgros =  to_decimal("0")
        mgros =  to_decimal("0")
        ygros =  to_decimal("0")
        lmgros =  to_decimal("0")
        lygros =  to_decimal("0")

        for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.flag == 6)):
            dgros =  to_decimal(dgros) + to_decimal(cl_list.dgros)
            mgros =  to_decimal(mgros) + to_decimal(cl_list.mgros)
            ygros =  to_decimal(ygros) + to_decimal(cl_list.ygros)
            lmgros =  to_decimal(lmgros) + to_decimal(cl_list.lmgros)
            lygros =  to_decimal(lygros) + to_decimal(cl_list.lygros)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 7
        cl_list.bezeich = translateExtended ("BANK REMITTANCE", lvcarea, "")
        cl_list.dgros =  to_decimal(dgros)
        cl_list.mgros =  to_decimal(mgros)
        cl_list.ygros =  to_decimal(ygros)
        cl_list.lmgros =  to_decimal(lmgros)
        cl_list.lygros =  to_decimal(lygros)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 7
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 7

        for segment in db_session.query(Segment).order_by(Segment._recid).all():
            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.segmentcode == segment.segmentcode) & (((Segmentstat.datum >= ljan1) & (Segmentstat.datum <= lfdate)) | ((Segmentstat.datum >= jan1) & (Segmentstat.datum <= to_date)))).order_by(Segmentstat._recid).all():

                if segmentstat.datum == to_date:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

                if segmentstat.datum >= from_date:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

                if segmentstat.datum >= jan1:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

                # Rulita
                # Fixing miss table name datum -> segmentstat.datum
                if segmentstat.datum >= lfdate and segmentstat.datum <= ltdate:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

                # Rulita
                # Fixing miss table name datum -> segmentstat.datum
                if segmentstat.datum >= ljan1 and segmentstat.datum <= ltdate:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation._recid).all():
            for nationstat in db_session.query(Nationstat).filter(
                     (Nationstat.nationnr == nation.nationnr) & (Nationstat.argtart == 2) & (((Nationstat.datum >= ljan1) & (Nationstat.datum <= lfdate)) | ((Nationstat.datum >= jan1) & (Nationstat.datum <= to_date)))).order_by(Nationstat._recid).all():
                if nationstat.datum == to_date:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

                if nationstat.datum >= from_date:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

                if nationstat.datum >= jan1:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

                # Rulita
                # Fixing miss table name datum -> nationstat.datum
                if nationstat.datum >= lfdate and nationstat.datum <= ltdate:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

                if nationstat.datum >= ljan1 and nationstat.datum <= ltdate:
                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

        for zinrstat in db_session.query(Zinrstat).filter(
                 (Zinrstat.zinr == "vacant") & (((Zinrstat.datum >= ljan1) & (Zinrstat.datum <= lfdate)) | ((Zinrstat.datum >= jan1) & (Zinrstat.datum <= to_date)))).order_by(Zinrstat.datum).all():  # Rahman -  fix ("string").lower()
            if zinrstat.datum == to_date:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

            if zinrstat.datum >= from_date:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

            if zinrstat.datum >= jan1:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

            if zinrstat.datum >= lfdate and zinrstat.datum <= ltdate:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

            if zinrstat.datum >= ljan1 and zinrstat.datum <= ltdate:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

        for zinrstat in db_session.query(Zinrstat).filter(
                 (Zinrstat.zinr == ("ooo").lower()) & (((Zinrstat.datum >= ljan1) & (Zinrstat.datum <= lfdate)) | ((Zinrstat.datum >= jan1) & (Zinrstat.datum <= to_date)))).order_by(Zinrstat.datum).all():

            if zinrstat.datum == to_date:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz

            if zinrstat.datum >= from_date:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz

            if zinrstat.datum >= jan1:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz

            if zinrstat.datum >= lfdate and zinrstat.datum <= ltdate:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz

            if zinrstat.datum >= ljan1 and zinrstat.datum <= ltdate:
                info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz
        loop_i = 0

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            loop_i = loop_i + 1

            anzroom = 0

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.zikatnr == zimkateg.zikatnr)).order_by(Zimmer._recid).all():
                anzroom = anzroom + 1
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = 8
            cl_list.proz = 2
            cl_list.bezeich = zimkateg.kurzbez
            d = 0
            m = 0
            y = 0
            lm = 0
            ly = 0
            dgros =  to_decimal("0")
            mgros =  to_decimal("0")
            ygros =  to_decimal("0")
            lmgros =  to_decimal("0")
            lygros =  to_decimal("0")

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.zikatnr == zimkateg.zikatnr) & (((Zkstat.datum >= ljan1) & (Zkstat.datum <= lfdate)) | ((Zkstat.datum >= jan1) & (Zkstat.datum <= to_date)))).order_by(Zkstat.datum).all():
                zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "tot-rm")],"datum": [(eq, zkstat.datum)]})

                if zkstat.datum == to_date:
                    dgros =  to_decimal(dgros) + to_decimal(zkstat.zimmeranz)
                    d = d + zkstat.anz100
                    danz = danz + zkstat.anz100

                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
                    info_list.avrm = info_list.avrm + zkstat.anz100
                    info_list.ocrm = info_list.ocrm + zkstat.zimmeranz
                    info_list.pers = info_list.pers + zkstat.personen
                    info_list.dayuse = info_list.dayuse + zkstat.anz_abr
                    info_list.arrival = info_list.arrival + zkstat.anz_ankunft
                    info_list.rcom = info_list.rcom + zkstat.betriebsnr

                    if loop_i == 1:
                        if zinrstat:
                            info_list.room = info_list.room + zinrstat.zimmeranz
                        else:
                            info_list.room = info_list.room + anzroom

                if zkstat.datum >= from_date:
                    mgros =  to_decimal(mgros) + to_decimal(zkstat.zimmeranz)
                    m = m + zkstat.anz100
                    manz = manz + zkstat.anz100

                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
                    info_list.avrm = info_list.avrm + zkstat.anz100
                    info_list.ocrm = info_list.ocrm + zkstat.zimmeranz
                    info_list.pers = info_list.pers + zkstat.personen
                    info_list.dayuse = info_list.dayuse + zkstat.anz_abr
                    info_list.arrival = info_list.arrival + zkstat.anz_ankunft
                    info_list.rcom = info_list.rcom + zkstat.betriebsnr

                    if loop_i == 1:
                        if zinrstat:
                            info_list.room = info_list.room + zinrstat.zimmeranz
                        else:
                            info_list.room = info_list.room + anzroom

                if zkstat.datum >= jan1:
                    ygros =  to_decimal(ygros) + to_decimal(zkstat.zimmeranz)
                    y = y + zkstat.anz100
                    yanz = yanz + zkstat.anz100

                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
                    info_list.avrm = info_list.avrm + zkstat.anz100
                    info_list.ocrm = info_list.ocrm + zkstat.zimmeranz
                    info_list.pers = info_list.pers + zkstat.personen
                    info_list.dayuse = info_list.dayuse + zkstat.anz_abr
                    info_list.arrival = info_list.arrival + zkstat.anz_ankunft
                    info_list.rcom = info_list.rcom + zkstat.betriebsnr

                    if loop_i == 1:
                        if zinrstat:
                            info_list.room = info_list.room + zinrstat.zimmeranz
                        else:
                            info_list.room = info_list.room + anzroom

                if zkstat.datum >= lfdate and zkstat.datum <= ltdate:
                    lmgros =  to_decimal(lmgros) + to_decimal(zkstat.zimmeranz)
                    lm = lm + zkstat.anz100
                    lmanz = lmanz + zkstat.anz100

                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
                    info_list.avrm = info_list.avrm + zkstat.anz100
                    info_list.ocrm = info_list.ocrm + zkstat.zimmeranz
                    info_list.pers = info_list.pers + zkstat.personen
                    info_list.dayuse = info_list.dayuse + zkstat.anz_abr
                    info_list.arrival = info_list.arrival + zkstat.anz_ankunft
                    info_list.rcom = info_list.rcom + zkstat.betriebsnr

                    if loop_i == 1:
                        if zinrstat:
                            info_list.room = info_list.room + zinrstat.zimmeranz
                        else:
                            info_list.room = info_list.room + anzroom

                if zkstat.datum >= ljan1 and zkstat.datum <= ltdate:
                    lygros =  to_decimal(lygros) + to_decimal(zkstat.zimmeranz)
                    ly = ly + zkstat.anz100
                    lyanz = lyanz + zkstat.anz100

                    info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
                    info_list.avrm = info_list.avrm + zkstat.anz100
                    info_list.ocrm = info_list.ocrm + zkstat.zimmeranz
                    info_list.pers = info_list.pers + zkstat.personen
                    info_list.dayuse = info_list.dayuse + zkstat.anz_abr
                    info_list.arrival = info_list.arrival + zkstat.anz_ankunft
                    info_list.rcom = info_list.rcom + zkstat.betriebsnr

                    if loop_i == 1:
                        if zinrstat:
                            info_list.room = info_list.room + zinrstat.zimmeranz
                        else:
                            info_list.room = info_list.room + anzroom
            cl_list.dgros =  to_decimal(dgros)
            cl_list.mgros =  to_decimal(mgros)
            cl_list.ygros =  to_decimal(ygros)
            cl_list.lmgros =  to_decimal(lmgros)
            cl_list.lygros =  to_decimal(lygros)
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = 8
            cl_list.proz = 1
            cl_list.bezeich = zimkateg.kurzbez

            if d != 0:
                cl_list.dgros =  to_decimal(dgros) / to_decimal(d) * to_decimal("100")

            if m != 0:
                cl_list.mgros =  to_decimal(mgros) / to_decimal(m) * to_decimal("100")

            if y != 0:
                cl_list.ygros =  to_decimal(ygros) / to_decimal(y) * to_decimal("100")

            if lm != 0:
                cl_list.lmgros =  to_decimal(lmgros) / to_decimal(lm) * to_decimal("100")

            if ly != 0:
                cl_list.lygros =  to_decimal(lygros) / to_decimal(ly) * to_decimal("100")
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.flag = 8
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 8
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("TOTAL ROOMS", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.room)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.room)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.room)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.room)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.room)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("SALEABLE ROOMS", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.avrm)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.avrm)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.avrm)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.avrm)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.avrm)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("OCCUPIED PAYING ROOMS", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("COMPLIMENTARY ROOMS", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.rcom)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.rcom)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.rcom)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.rcom)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.rcom)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("TOTAL OCCUPIED ROOMS", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.ocrm)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.ocrm)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.ocrm)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.ocrm)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.ocrm)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 1
        cl_list.bezeich = translateExtended ("TOTAL OCCUPANCY IN", lvcarea, "") + " %"

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)

        if info_list.avrm != 0:
            cl_list.dgros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)

        if info_list.avrm != 0:
            cl_list.mgros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)

        if info_list.avrm != 0:
            cl_list.ygros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)

        if info_list.avrm != 0:
            cl_list.lmgros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)

        if info_list.avrm != 0:
            cl_list.lygros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("VACANT ROOMS", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.vacant)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.vacant)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.vacant)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.vacant)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.vacant)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("OUT OF ORDER ROOMS", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.ooo)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.ooo)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.ooo)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.ooo)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.ooo)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("PAYING GUESTS", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.pers)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.pers)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.pers)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.pers)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.pers)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("COMPLIMENTARY", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.com)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.com)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.com)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.com)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.com)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("ARRIVAL GUESTS", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.arrival)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.arrival)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.arrival)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.arrival)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.arrival)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = translateExtended ("DAY USE", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.dayuse)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.dayuse)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.dayuse)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.dayuse)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.dayuse)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.bezeich = translateExtended ("LODGING TURNOVER", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.lodging)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.lodging)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.lodging)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.lodging)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.lodging)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.bezeich = translateExtended ("AVERAGE RATE (PERSON)", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)

        if info_list.pers != 0:
            cl_list.dgros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)

        if info_list.pers != 0:
            cl_list.mgros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)

        if info_list.pers != 0:
            cl_list.ygros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)

        if info_list.pers != 0:
            cl_list.lmgros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)

        if info_list.pers != 0:
            cl_list.lygros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 9
        cl_list.bezeich = translateExtended ("AVERAGE RATE (ROOM)", lvcarea, "")

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 1), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.dgros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 2), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.mgros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 3), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.ygros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 4), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.lmgros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))

        info_list = query(info_list_data, filters=(lambda info_list: info_list.flag == 5), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.lygros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))

    htparam = get_cache (
        Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    paramtext = get_cache (
        Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (
        Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr = paramtext.ptexte

    paramtext = get_cache (
        Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte

    htparam = get_cache (
        Htparam, {"paramnr": [(eq, 110)]})
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = get_cache (
        Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    nightaudit = get_cache (
        Nightaudit, {"programm": [(eq, progname)]})

    if nightaudit:
        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge

        for nitestor in db_session.query(Nitestor).filter(
                 (Nitestor.night_type == night_type) & (Nitestor.reihenfolge == reihenfolge)).order_by(Nitestor._recid).with_for_update().all():
            db_session.delete(nitestor)
        create_fina()
        umsatz_list()

    return generate_output()