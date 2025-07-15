#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Hoteldpt, Artikel, Umsatz

def disc_listbl(to_date:date):

    prepare_cache ([Htparam, Hoteldpt, Artikel, Umsatz])

    disc_list_data = []
    ekumnr:int = 0
    mm:int = 0
    from_date:date = None
    i:int = 0
    dnet:Decimal = to_decimal("0.0")
    mnet:Decimal = to_decimal("0.0")
    ynet:Decimal = to_decimal("0.0")
    htparam = hoteldpt = artikel = umsatz = None

    disc_list = art_list = disc_list1 = None

    disc_list_data, Disc_list = create_model("Disc_list", {"flag":string, "dept_no":string, "dept_name":string, "artnr":string, "day_disc":string, "day_percent":string, "mtd_disc":string, "mtd_percent":string, "ytd_disc":string, "ytd_percent":string})
    art_list_data, Art_list = create_model("Art_list", {"artnr":int, "dept":int, "name":string})
    disc_list1_data, Disc_list1 = create_model("Disc_list1", {"flag":string, "dept_no":int, "dept_name":string, "artnr":int, "day_disc":Decimal, "day_percent":Decimal, "mtd_disc":Decimal, "mtd_percent":Decimal, "ytd_disc":Decimal, "ytd_percent":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal disc_list_data, ekumnr, mm, from_date, i, dnet, mnet, ynet, htparam, hoteldpt, artikel, umsatz
        nonlocal to_date


        nonlocal disc_list, art_list, disc_list1
        nonlocal disc_list_data, art_list_data, disc_list1_data

        return {"disc-list": disc_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 555)]})
    ekumnr = htparam.finteger

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == hoteldpt.num) & (Artikel.artart == 0) & (Artikel.endkum == ekumnr)).order_by(Artikel._recid).all():
            art_list = Art_list()
            art_list_data.append(art_list)

            art_list.artnr = artikel.artnr
            art_list.dept = artikel.departement
            art_list.name = hoteldpt.depart


    dnet =  to_decimal("0")
    mnet =  to_decimal("0")
    ynet =  to_decimal("0")
    mm = get_month(to_date)
    from_date = date_mdy(1, 1, get_year(to_date))
    disc_list_data.clear()
    disc_list1_data.clear()

    for art_list in query(art_list_data):
        disc_list1 = Disc_list1()
        disc_list1_data.append(disc_list1)

        disc_list1.artnr = art_list.artnr
        disc_list1.dept_no = art_list.dept
        disc_list1.dept_name = art_list.name

        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.artnr == art_list.artnr) & (Umsatz.departement == art_list.dept) & (Umsatz.datum >= from_date) & (Umsatz.datum <= to_date)).order_by(Umsatz._recid).all():

            if umsatz.datum == to_date:
                disc_list1.day_disc =  - to_decimal(umsatz.betrag)
                dnet =  to_decimal(dnet) - to_decimal(umsatz.betrag)

            if get_month(umsatz.datum) == mm:
                disc_list1.mtd_disc =  to_decimal(disc_list1.mtd_disc) - to_decimal(umsatz.betrag)
                mnet =  to_decimal(mnet) - to_decimal(umsatz.betrag)
            disc_list1.ytd_disc =  to_decimal(disc_list1.ytd_disc) - to_decimal(umsatz.betrag)
            ynet =  to_decimal(ynet) - to_decimal(umsatz.betrag)

    for disc_list1 in query(disc_list1_data):

        if dnet != 0:
            disc_list1.day_percent =  to_decimal(disc_list1.day_disc) / to_decimal(dnet) * to_decimal("100")

        if mnet != 0:
            disc_list1.mtd_percent =  to_decimal(disc_list1.mtd_disc) / to_decimal(mnet) * to_decimal("100")

        if ynet != 0:
            disc_list1.ytd_percent =  to_decimal(disc_list1.ytd_disc) / to_decimal(ynet) * to_decimal("100")
    disc_list1 = Disc_list1()
    disc_list1_data.append(disc_list1)

    disc_list1.flag = "*"
    disc_list1 = Disc_list1()
    disc_list1_data.append(disc_list1)

    disc_list1.flag = "**"
    disc_list1.dept_name = "T O T A L"
    disc_list1.day_disc =  to_decimal(dnet)

    if dnet != 0:
        disc_list1.day_percent =  to_decimal("100")
    disc_list1.mtd_disc =  to_decimal(mnet)

    if mnet != 0:
        disc_list1.mtd_percent =  to_decimal("100")
    disc_list1.ytd_disc =  to_decimal(ynet)

    if ynet != 0:
        disc_list1.ytd_percent =  to_decimal("100")

    for disc_list1 in query(disc_list1_data):
        disc_list = Disc_list()
        disc_list_data.append(disc_list)

        disc_list.flag = disc_list1.flag

        if disc_list1.flag.lower()  == ("*").lower() :
            disc_list.dept_no = fill("-", 2)
            disc_list.dept_name = fill("-", 24)
            disc_list.artnr = fill("-", 4)
            disc_list.day_disc = fill("-", 14)
            disc_list.day_percent = fill("-", 7)
            disc_list.mtd_disc = fill("-", 15)
            disc_list.mtd_percent = fill("-", 7)
            disc_list.ytd_disc = fill("-", 15)
            disc_list.ytd_percent = fill("-", 7)


        else:

            if disc_list1.flag.lower()  == ("**").lower() :
                disc_list.dept_no = to_string(disc_list1.dept_no, ">>")
            else:
                disc_list.dept_no = to_string(disc_list1.dept_no, ">9")
            disc_list.dept_name = to_string(disc_list1.dept_name, "x(24)")
            disc_list.artnr = to_string(disc_list1.artnr, ">>>>")
            disc_list.day_disc = to_string(disc_list1.day_disc, "->>,>>>>>,>>9")
            disc_list.day_percent = to_string(disc_list1.day_percent, "->>9.9")
            disc_list.mtd_disc = to_string(disc_list1.mtd_disc, "->>,>>>,>>>,>>9")
            disc_list.mtd_percent = to_string(disc_list1.mtd_percent, "->>9.9")
            disc_list.ytd_disc = to_string(disc_list1.ytd_disc, "->>,>>>,>>>,>>9")
            disc_list.ytd_percent = to_string(disc_list1.ytd_percent, "->>9.9")

    return generate_output()