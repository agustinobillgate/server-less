from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Paramtext, Nightaudit, Nitestor, Zimmer, Artikel, Umsatz, Hoteldpt, Uebertrag, Segment, Segmentstat, Nation, Nationstat, Zinrstat, Zimkateg, Zkstat

def nt_fina():
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

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "proz":int, "bezeich":str, "dgros":decimal, "mgros":decimal, "ygros":decimal, "lmgros":decimal, "lygros":decimal})
    info_list_list, Info_list = create_model("Info_list", {"flag":int, "room":int, "avrm":int, "ocrm":int, "rcom":int, "vacant":int, "ooo":int, "pers":int, "com":int, "arrival":int, "dayuse":int, "lodging":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat


        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_list, cl_list_list, info_list_list

        return {}

    def umsatz_list():

        nonlocal long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat


        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_list, cl_list_list, info_list_list

        i:int = 0
        it_exist:bool = False
        line = to_string(p_width) + "," + to_string(p_length)
        add_line(line)
        add_line("##header")
        line = to_string(htl_name, "x(40)")
        for i in range(1,42 + 1) :
            line = line + " "
        line = line + "Date/Time :" + " " + to_string(get_current_date()) + " " + to_string(time, "HH:MM")
        add_line(line)
        line = to_string(htl_adr, "x(40)")
        for i in range(1,42 + 1) :
            line = line + " "
        line = line + "Bill-Date :" + " " + to_string(to_date)
        add_line(line)
        line = "Tel" + " " + to_string(htl_tel, "x(36)")
        for i in range(1,42 + 1) :
            line = line + " "
        line = line + "Page :" + " " + "##page"
        add_line(line)
        add_line(" ")
        line = "Finance Recapitulation Report"
        add_line(line)
        add_line(" ")
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "_"
        add_line(line)
        line = " " + "Current year Current year Current year Previous year Previous year"
        add_line(line)
        line = " " + "Effective-day Effective-month Effective-year Effective-month Effective-year"
        add_line(line)
        line = ""
        for i in range(1,p_width + 1) :
            line = line + "-"
        add_line(line)
        line = ""
        add_line(line)
        add_line("##end-header")

        for cl_list in query(cl_list_list):
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

                elif cl_list.bezeich.lower()  == ("*").lower() :
                    cl_list.bezeich = ""
                    fill_line()
                else:
                    fill_line()
        add_line("##end-of-file")


    def fill_line():

        nonlocal long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat


        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_list, cl_list_list, info_list_list

        if (price_decimal == 2 and cl_list.proz == 0) or cl_list.proz == 1:
            line = to_string(cl_list.bezeich, "x(24)") + " " + to_string(cl_list.dgros, " ->>>,>>>,>>9.99") + " " + to_string(cl_list.mgros, " ->>>,>>>,>>9.99") + " " + to_string(cl_list.ygros, " ->>>>,>>>,>>9.99") + " " + to_string(cl_list.lmgros, " ->>>,>>>,>>9.99") + " " + to_string(cl_list.lygros, " ->>>>,>>>,>>9.99")

        elif cl_list.proz == 2:
            line = to_string(cl_list.bezeich, "x(24)") + " " + to_string(cl_list.dgros, " ->>>,>>>,>>9 ") + " " + to_string(cl_list.mgros, " ->>>,>>>,>>9 ") + " " + to_string(cl_list.ygros, " ->>>>,>>>,>>9 ") + " " + to_string(cl_list.lmgros, " ->>>,>>>,>>9 ") + " " + to_string(cl_list.lygros, " ->>>>,>>>,>>9 ")
        else:
            line = to_string(cl_list.bezeich, "x(24)") + " " + to_string(cl_list.dgros, "->>>,>>>,>>>,>>9") + " " + to_string(cl_list.mgros, "->,>>>,>>>,>>>,>>9") + " " + to_string(cl_list.ygros, "->>,>>>,>>>,>>>,>>9") + " " + to_string(cl_list.lmgros, "->,>>>,>>>,>>>,>>9") + " " + to_string(cl_list.lygros, "->>,>>>,>>>,>>>,>>9")
        add_line(line)


    def add_line(s:str):

        nonlocal long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat


        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_list, cl_list_list, info_list_list

        if s == "":
            s = " "

        nitestor = db_session.query(Nitestor).filter(
                 (Nitestor.night_type == night_type) & (Nitestor.reihenfolge == reihenfolge) & (Nitestor.line_nr == line_nr)).first()

        if not nitestor:
            nitestor = Nitestor()
            db_session.add(nitestor)

            nitestor.night_type = night_type
            nitestor.reihenfolge = reihenfolge
            nitestor.line_nr = line_nr
        nitestor.line = s
        line_nr = line_nr + 1


    def create_fina():

        nonlocal long_digit, n, price_decimal, progname, night_type, reihenfolge, line_nr, line, p_width, p_length, htl_name, htl_adr, htl_tel, from_date, to_date, loop_i, htparam, paramtext, nightaudit, nitestor, zimmer, artikel, umsatz, hoteldpt, uebertrag, segment, segmentstat, nation, nationstat, zinrstat, zimkateg, zkstat


        nonlocal output_list, cl_list, info_list, cl_list1
        nonlocal output_list_list, cl_list_list, info_list_list

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
        dgros:decimal = to_decimal("0.0")
        mgros:decimal = to_decimal("0.0")
        ygros:decimal = to_decimal("0.0")
        lmgros:decimal = to_decimal("0.0")
        lygros:decimal = to_decimal("0.0")
        outstand:decimal = to_decimal("0.0")
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
        cl_list1_list = cl_list_list
        dd = get_day(to_date)
        yy = get_year(to_date) - 1
        jan1 = date_mdy(1, 1, get_year(to_date))
        ljan1 = date_mdy(1, 1, get_year(to_date) - timedelta(days=1))
        lfdate = date_mdy(get_month(from_date) , get_day(from_date) , get_year(from_date) - timedelta(days=1))

        if dd == 29 and (yy modulo 4 != 0):
            dd = 28
        ltdate = date_mdy(get_month(to_date) , dd, yy)
        anzroom = 0

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            anzroom = anzroom + 1
        for i in range(1,5 + 1) :
            info_list = Info_list()
            info_list_list.append(info_list)

            info_list.flag = i

        umsatz_obj_list = []
        for umsatz, artikel in db_session.query(Umsatz, Artikel).join(Artikel,(Artikel.artnr == Umsatz.artnr) & (Artikel.departement == Umsatz.departement) & ((Artikel.artart == 0) | (Artikel.artart == 8))).filter(
                 (((Umsatz.datum >= ljan1) & (Umsatz.datum <= lfdate)) | ((Umsatz.datum >= jan1) & (Umsatz.datum <= to_date)))).order_by(Artikel.departement, Artikel.artnr, Umsatz.datum).all():
            if umsatz._recid in umsatz_obj_list:
                continue
            else:
                umsatz_obj_list.append(umsatz._recid)

            if curr_dept != artikel.departement:

                if curr_dept != -1:
                    cl_list.dgros =  to_decimal(dgros)
                    cl_list.mgros =  to_decimal(mgros)
                    cl_list.ygros =  to_decimal(ygros)
                    cl_list.lmgros =  to_decimal(lmgros)
                    cl_list.lygros =  to_decimal(lygros)
                curr_dept = artikel.departement

                hoteldpt = db_session.query(Hoteldpt).filter(
                         (Hoteldpt.num == curr_dept)).first()
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

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

        for cl_list in query(cl_list_list):
            dgros =  to_decimal(dgros) + to_decimal(cl_list.dgros)
            mgros =  to_decimal(mgros) + to_decimal(cl_list.mgros)
            ygros =  to_decimal(ygros) + to_decimal(cl_list.ygros)
            lmgros =  to_decimal(lmgros) + to_decimal(cl_list.lmgros)
            lygros =  to_decimal(lygros) + to_decimal(cl_list.lygros)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 2
        cl_list.bezeich = "*"
        cl_list.dgros =  to_decimal(dgros)
        cl_list.mgros =  to_decimal(mgros)
        cl_list.ygros =  to_decimal(ygros)
        cl_list.lmgros =  to_decimal(lmgros)
        cl_list.lygros =  to_decimal(lygros)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 2

        uebertrag = db_session.query(Uebertrag).filter(
                 (Uebertrag.datum == to_date - timedelta(days=1))).first()

        if uebertrag:
            outstand =  to_decimal(uebertrag.betrag)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 3
        cl_list.bezeich = "YESTERDAY OUTSTANDING"
        cl_list.dgros =  to_decimal(outstand)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 3

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 2) | (Artikel.artart == 5) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.departement == 0)).order_by(Artikel.artart, Artikel.bezeich).all():
            dgros =  to_decimal("0")
            mgros =  to_decimal("0")
            ygros =  to_decimal("0")
            lmgros =  to_decimal("0")
            lygros =  to_decimal("0")
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

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
        cl_list_list.append(cl_list)

        cl_list.flag = 4
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 5
        cl_list.bezeich = "TODAY OUTSTANDING"

        for cl_list1 in query(cl_list1_list, filters=(lambda cl_list1: cl_list1.flag >= 2 and cl_list1.flag <= 4)):
            cl_list.dgros =  to_decimal(cl_list.dgros) + to_decimal(cl_list1.dgros)

        uebertrag = db_session.query(Uebertrag).filter(
                 (Uebertrag.datum == to_date)).first()

        if not uebertrag:
            uebertrag = Uebertrag()
            db_session.add(uebertrag)

            uebertrag.datum = to_date
        uebertrag.betrag =  to_decimal(cl_list.dgros)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 5
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 5

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 120)).first()
        art1 = htparam.finteger

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 6)) & (Artikel.departement == 0)).order_by(Artikel.artart, Artikel.bezeich).all():
            dgros =  to_decimal("0")
            mgros =  to_decimal("0")
            ygros =  to_decimal("0")
            lmgros =  to_decimal("0")
            lygros =  to_decimal("0")
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

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
        cl_list_list.append(cl_list)

        cl_list.flag = 6
        dgros =  to_decimal("0")
        mgros =  to_decimal("0")
        ygros =  to_decimal("0")
        lmgros =  to_decimal("0")
        lygros =  to_decimal("0")

        for cl_list in query(cl_list_list, filters=(lambda cl_list: cl_list.flag == 6)):
            dgros =  to_decimal(dgros) + to_decimal(cl_list.dgros)
            mgros =  to_decimal(mgros) + to_decimal(cl_list.mgros)
            ygros =  to_decimal(ygros) + to_decimal(cl_list.ygros)
            lmgros =  to_decimal(lmgros) + to_decimal(cl_list.lmgros)
            lygros =  to_decimal(lygros) + to_decimal(cl_list.lygros)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 7
        cl_list.bezeich = "BANK REMITTANCE"
        cl_list.dgros =  to_decimal(dgros)
        cl_list.mgros =  to_decimal(mgros)
        cl_list.ygros =  to_decimal(ygros)
        cl_list.lmgros =  to_decimal(lmgros)
        cl_list.lygros =  to_decimal(lygros)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 7
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 7

        for segment in db_session.query(Segment).order_by(Segment._recid).all():

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.segmentcode == segment.segmentcode) & (((Segmentstat.datum >= ljan1) & (Segmentstat.datum <= lfdate)) | ((Segmentstat.datum >= jan1) & (Segmentstat.datum <= to_date)))).order_by(Segmentstat._recid).all():

                if segmentstat.datum == to_date:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

                if segmentstat.datum >= from_date:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

                if segmentstat.datum >= jan1:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

                if datum >= lfdate and datum <= ltdate:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

                if datum >= ljan1 and datum <= ltdate:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
                    info_list.lodging =  to_decimal(info_list.lodging) + to_decimal(segmentstat.logis)

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation._recid).all():

            for nationstat in db_session.query(Nationstat).filter(
                     (Nationstat.nationnr == nation.nationnr) & (Nationstat.argtart == 2) & (((Nationstat.datum >= ljan1) & (Nationstat.datum <= lfdate)) | ((Nationstat.datum >= jan1) & (Nationstat.datum <= to_date)))).order_by(Nationstat._recid).all():

                if nationstat.datum == to_date:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

                if nationstat.datum >= from_date:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

                if nationstat.datum >= jan1:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

                if datum >= lfdate and datum <= ltdate:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

                if datum >= ljan1 and datum <= ltdate:

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
                    info_list.com = info_list.com + nationstat.loggratis

        for zinrstat in db_session.query(Zinrstat).filter(
                 (func.lower(Zinrstat.zinr) == ("vacant").lower()) & (((Zinrstat.datum >= ljan1) & (Zinrstat.datum <= lfdate)) | ((Zinrstat.datum >= jan1) & (Zinrstat.datum <= to_date)))).order_by(Zinrstat.datum).all():

            if zinrstat.datum == to_date:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

            if zinrstat.datum >= from_date:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

            if zinrstat.datum >= jan1:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

            if zinrstat.datum >= lfdate and zinrstat.datum <= ltdate:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

            if zinrstat.datum >= ljan1 and zinrstat.datum <= ltdate:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
                info_list.vacant = info_list.vacant + zinrstat.zimmeranz

        for zinrstat in db_session.query(Zinrstat).filter(
                 (func.lower(Zinrstat.zinr) == ("ooo").lower()) & (((Zinrstat.datum >= ljan1) & (Zinrstat.datum <= lfdate)) | ((Zinrstat.datum >= jan1) & (Zinrstat.datum <= to_date)))).order_by(Zinrstat.datum).all():

            if zinrstat.datum == to_date:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz

            if zinrstat.datum >= from_date:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz

            if zinrstat.datum >= jan1:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz

            if zinrstat.datum >= lfdate and zinrstat.datum <= ltdate:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz

            if zinrstat.datum >= ljan1 and zinrstat.datum <= ltdate:

                info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
                info_list.ooo = info_list.ooo + zinrstat.zimmeranz
        loop_i = 0

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():
            loop_i = loop_i + 1


            anzroom = 0

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.zikatnr == zimkateg.zikatnr)).order_by(Zimmer._recid).all():
                anzroom = anzroom + 1
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

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

                zinrstat = db_session.query(Zinrstat).filter(
                         (func.lower(Zinrstat.zinr) == ("tot-rm").lower()) & (Zinrstat.datum == zkstat.datum)).first()

                if zkstat.datum == to_date:
                    dgros =  to_decimal(dgros) + to_decimal(zkstat.zimmeranz)
                    d = d + zkstat.anz100
                    danz = danz + zkstat.anz100

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
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

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
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

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
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

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
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

                    info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
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
            cl_list_list.append(cl_list)

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
            cl_list_list.append(cl_list)

            cl_list.flag = 8
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 8
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "TOTAL ROOMS"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.room)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.room)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.room)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.room)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.room)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "SALEABLE ROOMS"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.avrm)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.avrm)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.avrm)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.avrm)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.avrm)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "OCCUPIED PAYING ROOMS"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.ocrm) - to_decimal(info_list.rcom)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "COMPLIMENTARY ROOMS"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.rcom)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.rcom)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.rcom)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.rcom)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.rcom)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "TOTAL OCCUPIED ROOMS"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.ocrm)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.ocrm)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.ocrm)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.ocrm)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.ocrm)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 1
        cl_list.bezeich = "TOTAL OCCUPANCY IN"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)

        if info_list.avrm != 0:
            cl_list.dgros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)

        if info_list.avrm != 0:
            cl_list.mgros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)

        if info_list.avrm != 0:
            cl_list.ygros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)

        if info_list.avrm != 0:
            cl_list.lmgros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)

        if info_list.avrm != 0:
            cl_list.lygros =  to_decimal(info_list.ocrm) / to_decimal(info_list.avrm) * to_decimal("100")
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "VACANT ROOMS"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.vacant)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.vacant)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.vacant)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.vacant)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.vacant)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "OUT OF ORDER ROOMS"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.ooo)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.ooo)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.ooo)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.ooo)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.ooo)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "PAYING GUESTS"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.pers)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.pers)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.pers)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.pers)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.pers)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "COMPLIMENTARY"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.com)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.com)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.com)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.com)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.com)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "ARRIVAL GUESTS"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.arrival)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.arrival)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.arrival)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.arrival)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.arrival)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.proz = 2
        cl_list.bezeich = "DAY USE"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.dayuse)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.dayuse)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.dayuse)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.dayuse)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.dayuse)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.bezeich = "LODGING TURNOVER"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)
        cl_list.dgros =  to_decimal(info_list.lodging)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)
        cl_list.mgros =  to_decimal(info_list.lodging)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)
        cl_list.ygros =  to_decimal(info_list.lodging)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)
        cl_list.lmgros =  to_decimal(info_list.lodging)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)
        cl_list.lygros =  to_decimal(info_list.lodging)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.bezeich = "AVERAGE RATE (PERSON)"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)

        if info_list.pers != 0:
            cl_list.dgros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)

        if info_list.pers != 0:
            cl_list.mgros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)

        if info_list.pers != 0:
            cl_list.ygros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)

        if info_list.pers != 0:
            cl_list.lmgros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)

        if info_list.pers != 0:
            cl_list.lygros =  to_decimal(info_list.lodging) / to_decimal(info_list.pers)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 9
        cl_list.bezeich = "AVERAGE RATE (ROOM)"

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 1), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.dgros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 2), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.mgros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 3), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.ygros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 4), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.lmgros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))

        info_list = query(info_list_list, filters=(lambda info_list: info_list.flag == 5), first=True)

        if (info_list.ocrm - info_list.rcom) != 0:
            cl_list.lygros =  to_decimal(info_list.lodging) / to_decimal((info_list.ocrm) - to_decimal(info_list.rcom))


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 200)).first()
    htl_name = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 201)).first()
    htl_adr = paramtext.ptexte

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 204)).first()
    htl_tel = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    nightaudit = db_session.query(Nightaudit).filter(
             (func.lower(Nightaudit.programm) == (progname).lower())).first()

    if nightaudit:

        if nightaudit.hogarest == 0:
            night_type = 0
        else:
            night_type = 2
        reihenfolge = nightaudit.reihenfolge

        for nitestor in db_session.query(Nitestor).filter(
                 (Nitestor.night_type == night_type) & (Nitestor.reihenfolge == reihenfolge)).order_by(Nitestor._recid).all():
            db_session.delete(nitestor)
        create_fina()
        umsatz_list()

    return generate_output()