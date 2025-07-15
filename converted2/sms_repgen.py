from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from sqlalchemy import func
from models import Htparam, Queasy, Brief, Briefzei, Sms_broadcast, Segmentstat, Segment, Zkstat, Artikel, Umsatz, Hoteldpt, Budget

def sms_repgen(bill_date:date, s_recid:int, nzeit:int):
    lvcarea:str = "sms-repgen"
    i:int = 0
    loopi:int = 0
    j:int = 0
    sms_kateg:int = 0
    repnr:List[int] = create_empty_list(10, 0)
    mobil_no:str = ""
    mail_to:str = ""
    str:str = ""
    n:int = 0
    spos:int = 0
    ss:str = ""
    by_sms:bool = False
    by_mail:bool = True
    val_sign:int = 1
    curr_group:int = 0
    flag_group:bool = False
    mtd_flag:bool = False
    str_group:str = ""
    str_result:str = ""
    dept_group:int = ""
    occ:decimal = to_decimal("0.0")
    occ_room:int = 0
    deptno:int = 0
    artno:int = 0
    dept_name:str = ""
    dept_rev:decimal = to_decimal("0.0")
    dept_rev_exfb:decimal = to_decimal("0.0")
    mtd_rev:decimal = to_decimal("0.0")
    tbudget:decimal = to_decimal("0.0")
    mtdbudget:decimal = to_decimal("0.0")
    mtdbudgetnonbfast:decimal = to_decimal("0.0")
    tot_rev:decimal = to_decimal("0.0")
    tot_mtd:decimal = to_decimal("0.0")
    avrate:decimal = to_decimal("0.0")
    mtdavrate:decimal = to_decimal("0.0")
    tot_group:decimal = to_decimal("0.0")
    rpt_msg:str = ""
    rpt_email:str = ""
    curr_msg:str = ""
    long_digit:bool = False
    price_decimal:int = 0
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    fact1:int = 0
    vat_str:str = ""
    vat_artnr:int = 0
    serv_artnr:int = 0
    nett_amt:decimal = to_decimal("0.0")
    nett_serv:decimal = to_decimal("0.0")
    nett_tax:decimal = to_decimal("0.0")
    htparam = queasy = brief = briefzei = sms_broadcast = segmentstat = segment = zkstat = artikel = umsatz = hoteldpt = budget = None

    temp_list = None

    temp_list_list, Temp_list = create_model("Temp_list", {"str":str, "nr":int, "rev":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, deptno, artno, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        return {"nzeit": nzeit}

    def occ_room():

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, deptno, artno, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        occ_room = 0
        occ = to_decimal("0.0")
        tot_room:int = 0

        def generate_inner_output():
            return (occ_room, occ)


        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.datum == bill_date)).order_by(Segmentstat._recid).all():

            segment = db_session.query(Segment).filter(
                     (Segment.segmentcode == segmentstat.segmentcode) & (segmentstat.datum == bill_date)).first()

            if segment:
                occ_room = occ_room + segmentstat.zimmeranz

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == bill_date)).order_by(Zkstat._recid).all():
            tot_room = tot_room + zkstat.anz100
        occ = ( to_decimal(occ_room) / to_decimal(tot_room)) * to_decimal("100")

        if occ == None:
            occ =  to_decimal("0")

        return generate_inner_output()


    def total_rev():

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, deptno, artno, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == 0) | (Artikel.artart == 8))).order_by(Artikel._recid).all():

            for umsatz in db_session.query(Umsatz).filter(
                     (Umsatz.departement == artikel.departement) & (Umsatz.artnr == artikel.artnr) & (Umsatz.datum >= date_mdy(get_month(bill_date) , 1, get_year(bill_date))) & (Umsatz.datum <= bill_date)).order_by(Umsatz._recid).all():
                serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

                if artikel.artnr == vat_artnr and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_serv =  to_decimal("0")
                    nett_tax =  to_decimal(umsatz.betrag)

                elif re.match(r".*;" + to_string(artikel.artnr) + r";.*",vat_str, re.IGNORECASE) and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_serv =  to_decimal("0")
                    nett_tax =  to_decimal(umsatz.betrag)

                elif artikel.artnr == serv_artnr and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_tax =  to_decimal("0")
                    nett_serv =  to_decimal(umsatz.betrag)


                else:
                    nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                    nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                    nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                    nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)

                if umsatz.datum == bill_date:
                    tot_rev =  to_decimal(tot_rev) + to_decimal((nett_amt) / to_decimal(fact1))
                tot_mtd =  to_decimal(tot_mtd) + to_decimal((nett_amt) / to_decimal(fact1))


    def dept_name(deptno:int):

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, artno, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        dept_name = ""

        def generate_inner_output():
            return (dept_name)


        hoteldpt = db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num == deptno)).first()

        if hoteldpt:
            dept_name = hoteldpt.depart

        return generate_inner_output()


    def dept_rev(deptno:int, artno:int):

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        dept_rev = to_decimal("0.0")

        def generate_inner_output():
            return (dept_rev)


        if artno == 0:

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == deptno) & ((Artikel.artart == 0) | (Artikel.artart == 8))).order_by(Artikel._recid).all():

                umsatz = db_session.query(Umsatz).filter(
                         (Umsatz.departement == artikel.departement) & (Umsatz.artnr == artikel.artnr) & (Umsatz.datum == bill_date)).first()

                if umsatz:
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

                    if artikel.artnr == vat_artnr and artikel.departement == 0:
                        nett_amt =  to_decimal("0")
                        nett_serv =  to_decimal("0")
                        nett_tax =  to_decimal(umsatz.betrag)

                    elif re.match(r".*;" + to_string(artikel.artnr) + r";.*",vat_str, re.IGNORECASE) and artikel.departement == 0:
                        nett_amt =  to_decimal("0")
                        nett_serv =  to_decimal("0")
                        nett_tax =  to_decimal(umsatz.betrag)

                    elif artikel.artnr == serv_artnr and artikel.departement == 0:
                        nett_amt =  to_decimal("0")
                        nett_tax =  to_decimal("0")
                        nett_serv =  to_decimal(umsatz.betrag)


                    else:
                        nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                        nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                        nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                        nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


                    dept_rev =  to_decimal(dept_rev) + to_decimal((nett_amt) / to_decimal(fact1))

        else:

            for umsatz in db_session.query(Umsatz).filter(
                     (Umsatz.departement == deptno) & (Umsatz.artnr == artno) & (Umsatz.datum == bill_date)).order_by(Umsatz._recid).all():

                artikel = db_session.query(Artikel).filter(
                         (Artikel.departement == deptno) & (Artikel.artnr == artno)).first()
                serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

                if artikel.artnr == vat_artnr and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_serv =  to_decimal("0")
                    nett_tax =  to_decimal(umsatz.betrag)

                elif re.match(r".*;" + to_string(artikel.artnr) + r";.*",vat_str, re.IGNORECASE) and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_serv =  to_decimal("0")
                    nett_tax =  to_decimal(umsatz.betrag)

                elif artikel.artnr == serv_artnr and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_tax =  to_decimal("0")
                    nett_serv =  to_decimal(umsatz.betrag)


                else:
                    nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                    nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                    nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                    nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


                dept_rev =  to_decimal(dept_rev) + to_decimal((nett_amt) / to_decimal(fact1))


        return generate_inner_output()


    def dept_mtd(deptno:int, artno:int):

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        mtd_rev = to_decimal("0.0")

        def generate_inner_output():
            return (mtd_rev)


        if artno == 0:

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == deptno) & ((Artikel.artart == 0) | (Artikel.artart == 8))).order_by(Artikel._recid).all():

                for umsatz in db_session.query(Umsatz).filter(
                         (Umsatz.departement == artikel.departement) & (Umsatz.artnr == artikel.artnr) & (Umsatz.datum >= date_mdy(get_month(bill_date) , 1, get_year(bill_date))) & (Umsatz.datum <= bill_date)).order_by(Umsatz._recid).all():
                    serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                    fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

                    if artikel.artnr == vat_artnr and artikel.departement == 0:
                        nett_amt =  to_decimal("0")
                        nett_serv =  to_decimal("0")
                        nett_tax =  to_decimal(umsatz.betrag)

                    elif re.match(r".*;" + to_string(artikel.artnr) + r";.*",vat_str, re.IGNORECASE) and artikel.departement == 0:
                        nett_amt =  to_decimal("0")
                        nett_serv =  to_decimal("0")
                        nett_tax =  to_decimal(umsatz.betrag)

                    elif artikel.artnr == serv_artnr and artikel.departement == 0:
                        nett_amt =  to_decimal("0")
                        nett_tax =  to_decimal("0")
                        nett_serv =  to_decimal(umsatz.betrag)


                    else:
                        nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                        nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                        nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                        nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


                    mtd_rev =  to_decimal(mtd_rev) + to_decimal((nett_amt) / to_decimal(fact1))

        else:

            for umsatz in db_session.query(Umsatz).filter(
                     (Umsatz.departement == deptno) & (Umsatz.artnr == artno) & (Umsatz.datum >= date_mdy(get_month(bill_date) , 1, get_year(bill_date))) & (Umsatz.datum <= bill_date)).order_by(Umsatz._recid).all():

                artikel = db_session.query(Artikel).filter(
                         (Artikel.departement == deptno) & (Artikel.artnr == artno)).first()
                serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

                if artikel.artnr == vat_artnr and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_serv =  to_decimal("0")
                    nett_tax =  to_decimal(umsatz.betrag)

                elif re.match(r".*;" + to_string(artikel.artnr) + r";.*",vat_str, re.IGNORECASE) and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_serv =  to_decimal("0")
                    nett_tax =  to_decimal(umsatz.betrag)

                elif artikel.artnr == serv_artnr and artikel.departement == 0:
                    nett_amt =  to_decimal("0")
                    nett_tax =  to_decimal("0")
                    nett_serv =  to_decimal(umsatz.betrag)


                else:
                    nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                    nett_serv = to_decimal(round(nett_amt * serv , price_decimal))
                    nett_tax = to_decimal(round(nett_amt * vat , price_decimal))
                    nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


                mtd_rev =  to_decimal(mtd_rev) + to_decimal((nett_amt) / to_decimal(fact1))


        return generate_inner_output()


    def t_budget(deptno:int, artno:int):

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        tbudget = to_decimal("0.0")

        def generate_inner_output():
            return (tbudget)


        if artno == 0:

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == deptno) & ((Artikel.artart == 0) | (Artikel.artart == 8))).order_by(Artikel._recid).all():

                budget = db_session.query(Budget).filter(
                         (Budget.departement == artikel.departement) & (Budget.artnr == artikel.artnr) & (Budget.datum == bill_date)).first()

                if budget:
                    tbudget =  to_decimal(tbudget) + to_decimal(budget.betrag)


        else:

            for budget in db_session.query(Budget).filter(
                     (Budget.departement == deptno) & (Budget.artnr == artno) & (Budget.datum == bill_date)).order_by(Budget._recid).all():
                tbudget =  to_decimal(tbudget) + to_decimal(budget.betrag)

        return generate_inner_output()


    def mtd_budget(deptno:int, artno:int):

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        mtdbudget = to_decimal("0.0")

        def generate_inner_output():
            return (mtdbudget)


        if artno == 0:

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == deptno) & ((Artikel.artart == 0) | (Artikel.artart == 8))).order_by(Artikel._recid).all():

                for budget in db_session.query(Budget).filter(
                         (Budget.departement == artikel.departement) & (Budget.artnr == artikel.artnr) & (Budget.datum >= date_mdy(get_month(bill_date) , 1, get_year(bill_date))) & (Budget.datum <= bill_date)).order_by(Budget._recid).all():
                    mtdbudget =  to_decimal(mtdbudget) + to_decimal(budget.betrag)


        else:

            for budget in db_session.query(Budget).filter(
                     (Budget.departement == deptno) & (Budget.artnr == artno) & (Budget.datum >= date_mdy(get_month(bill_date) , 1, get_year(bill_date))) & (Budget.datum <= bill_date)).order_by(Budget._recid).all():
                mtdbudget =  to_decimal(mtdbudget) + to_decimal(budget.betrag)

        return generate_inner_output()


    def mtd_budget_non_bfast(deptno:int, artno:int):

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        mtdbudgetnonbfast = to_decimal("0.0")

        def generate_inner_output():
            return (mtdbudgetnonbfast)


        if artno == 0:

            for artikel, budget in db_session.query(Artikel, Budget).join(Budget,(Budget.departement == Artikel.departement) & (Budget.artnr == Artikel.artnr) & (Budget.datum >= date_mdy(get_month(bill_date) , 1, get_year(bill_date))) & (Budget.datum <= bill_date)).filter(
                     (Artikel.departement == deptno) & ((Artikel.artart == 0) | (Artikel.artart == 8)) & (func.lower(not Artikel.bezeich).op("~")(("*fast*".lower().replace("*",".*"))))).order_by(Artikel._recid).all():
                mtdbudgetnonbfast =  to_decimal(mtdbudgetnonbfast) + to_decimal(budget.betrag)


        else:

            for budget in db_session.query(Budget).filter(
                     (Budget.departement == deptno) & (Budget.artnr == artno) & (Budget.datum >= date_mdy(get_month(bill_date) , 1, get_year(bill_date))) & (Budget.datum <= bill_date)).order_by(Budget._recid).all():
                mtdbudgetnonbfast =  to_decimal(mtdbudgetnonbfast) + to_decimal(budget.betrag)

        return generate_inner_output()


    def avrate(bill_date:date):

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, deptno, artno, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        avrate = to_decimal("0.0")
        temp_avrate:decimal = to_decimal("0.0")
        counter:int = 0

        def generate_inner_output():
            return (avrate)


        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.datum == bill_date)).order_by(Segmentstat._recid).all():
            temp_avrate =  to_decimal(temp_avrate) + to_decimal(segmentstat.logis)
            counter = counter + segmentstat.zimmeranz - segmentstat.betriebsnr


        avrate =  to_decimal(temp_avrate) / to_decimal(counter)

        if avrate == None:
            avrate =  to_decimal(0.00)

        return generate_inner_output()


    def mtd_avrate(bill_date:date):

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, deptno, artno, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        mtdavrate = to_decimal("0.0")
        temp_avrate:decimal = to_decimal("0.0")
        counter:int = 0

        def generate_inner_output():
            return (mtdavrate)


        for segmentstat in db_session.query(Segmentstat).filter(
                 (Segmentstat.datum >= date_mdy(get_month(bill_date) , 1, get_year(bill_date))) & (Segmentstat.datum <= bill_date)).order_by(Segmentstat._recid).all():
            temp_avrate =  to_decimal(temp_avrate) + to_decimal(segmentstat.logis)
            counter = counter + segmentstat.zimmeranz - segmentstat.betriebsnr


        mtdavrate =  to_decimal(temp_avrate) / to_decimal(counter)

        if mtdavrate == None:
            mtdavrate =  to_decimal(0.00)

        return generate_inner_output()


    def read_param():

        nonlocal lvcarea, i, loopi, j, sms_kateg, repnr, mobil_no, mail_to, str, n, spos, ss, by_sms, by_mail, val_sign, curr_group, flag_group, mtd_flag, str_group, str_result, dept_group, occ, occ_room, deptno, artno, dept_name, dept_rev, dept_rev_exfb, mtd_rev, tbudget, mtdbudget, mtdbudgetnonbfast, tot_rev, tot_mtd, avrate, mtdavrate, tot_group, rpt_msg, rpt_email, curr_msg, long_digit, price_decimal, serv, vat, fact, fact1, vat_str, vat_artnr, serv_artnr, nett_amt, nett_serv, nett_tax, htparam, queasy, brief, briefzei, sms_broadcast, segmentstat, segment, zkstat, artikel, umsatz, hoteldpt, budget
        nonlocal bill_date, s_recid, nzeit


        nonlocal temp_list
        nonlocal temp_list_list

        param1:str = ""
        str_param:str = ""
        str_param = SESSION:PARAMETER
        for i in range(1,num_entries(str_param, ";")  + 1) :
            param1 = entry(i - 1, str_param, ";")

            if re.match(r".*bysms.*",param1, re.IGNORECASE):
                by_sms = logical(entry(1, param1, "="))

            if re.match(r".*bymail.*",param1, re.IGNORECASE):
                by_mail = logical(entry(1, param1, "="))


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 132)).first()
    vat_artnr = htparam.finteger
    vat_str = htparam.fchar

    if vat_str != "":

        if substring(vat_str, 0, 1) != (";").lower() :
            vat_str = ";" + vat_str

        if substring(vat_str, len(vat_str) - 1, 1) != (";").lower() :
            vat_str = vat_str + ";"

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 133)).first()
    serv_artnr = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    if not long_digit:
        fact1 = 1
    else:
        fact1 = 1000

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 839)).first()

    if htparam.finteger == 0:

        return generate_output()
    by_mail = True
    sms_kateg = htparam.finteger


    temp_list_list.clear()
    total_rev()

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 34) & (Queasy._recid == s_recid)).first()
    rpt_email = ""
    for loopi in range(1,(num_entries(queasy.char3, ";") - 1)  + 1) :
        repnr[loopi - 1] = to_int(entry(loopi - 1, queasy.char3, ";"))
        mobil_no = entry(0, queasy.char2, ";")
        mobil_no = replace_str(mobil_no, "-", "")
        mobil_no = "+" + mobil_no
        mail_to = entry(1, queasy.char2, ";")

        brief = db_session.query(Brief).filter(
                 (Brief.briefkateg == sms_kateg) & (Brief.briefnr == repnr[loopi - 1])).first()

        if brief:
            rpt_msg = ""

            briefzei = db_session.query(Briefzei).filter(
                     (Briefzei.briefnr == brief.briefnr)).first()

            if briefzei:
                for j in range(1,num_entries(briefzei.texte, chr(10))  + 1) :
                    curr_msg = entry(j - 1, briefzei.texte, chr(10))

                    if re.match(r".*\$RESULT.*",curr_msg, re.IGNORECASE) and not (re.match(r".*\$GROUP.*",curr_msg, re.IGNORECASE)):
                        str_result = substring(curr_msg, 0 + get_index(curr_msg, "$result") , len(curr_msg))

                        temp_list = query(temp_list_list, filters=(lambda temp_list: temp_list.nr == to_int(entry(1, str_result, " "))), first=True)

                        if temp_list:
                            curr_msg = replace_str(curr_msg, str_result, trim(to_string(temp_list.rev, "->>>,>>>,>>>,>99.99")))

                    if re.match(r".*\$TODAY.*",curr_msg, re.IGNORECASE):
                        curr_msg = replace_str(curr_msg, "$TODAY", to_string(bill_date, "99-99-9999"))

                    if re.match(r".*\$RMOCC.*",curr_msg, re.IGNORECASE):
                        occ_room, occ = occ_room()
                        curr_msg = replace_str(curr_msg, "$RMOCC", to_string(occ_room))

                    if re.match(r".*\$occ%.*",curr_msg, re.IGNORECASE):
                        occ_room, occ = occ_room()
                        curr_msg = replace_str(curr_msg, "$occ%", to_string(occ, ">>99.99"))

                    if re.match(r".*\$DEPTNAME.*",curr_msg, re.IGNORECASE):
                        deptno = to_int(trim(substring(entry(1, curr_msg, "$") , len("DEPTNAME") + 1 - 1, 3)))
                        dept_name = dept_name(deptno)
                        curr_msg = replace_str(curr_msg, "$DEPTNAME " + to_string(deptno) , dept_name)

                    if re.match(r".*\$deptno.*",curr_msg, re.IGNORECASE):
                        deptno = to_int(trim(substring(entry(1, curr_msg, "$") , len("deptno") + 1 - 1, 3)))
                        curr_msg = replace_str(curr_msg, "$deptno " , "D")

                    if re.match(r".*\$REVMTD.*",curr_msg, re.IGNORECASE):

                        if flag_group:

                            if substring(curr_msg, 0, 1) == ("-").lower() :
                                val_sign = - 1
                                curr_msg = substring(curr_msg, 1, len(curr_msg))


                            else:
                                val_sign = 1
                        for i in range(1,num_entries(curr_msg, "$")  + 1) :
                            str = entry(i - 1, curr_msg, "$")

                            if re.match(r".*REVMTD.*",str, re.IGNORECASE):

                                if re.match(r".*;.*",str, re.IGNORECASE):
                                    deptno = to_int(entry(0, entry(1, str, " ") , ";"))
                                    artno = to_int(trim(entry(1, curr_msg, ";")))


                                    mtd_rev = dept_mtd(deptno, artno)

                                    if flag_group:
                                        mtd_rev =  to_decimal(val_sign) * to_decimal(mtd_rev)
                                        str_group = str_group + to_string(mtd_rev) + ";"
                                        dept_group = deptno
                                        curr_msg = replace_str(curr_msg, "$REVMTD " + to_string(deptno) + ";" + to_string(artno) , "delete")


                                    else:
                                        curr_msg = replace_str(curr_msg, "$REVMTD " + to_string(deptno) + ";" + to_string(artno) , trim(to_string(mtd_rev, "->>>,>>>,>>>,>>>,>99.99")))
                                else:
                                    deptno = to_int(entry(1, str, " "))
                                    mtd_rev = dept_mtd(deptno, 0)

                                    if flag_group:
                                        mtd_rev =  to_decimal(val_sign) * to_decimal(mtd_rev)
                                        str_group = str_group + to_string(mtd_rev) + ";"
                                        dept_group = deptno
                                        curr_msg = replace_str(curr_msg, "$REVMTD " + to_string(deptno) , "delete")


                                    else:
                                        curr_msg = replace_str(curr_msg, "$REVMTD " + to_string(deptno) , trim(to_string(mtd_rev, "->>>,>>>,>>>,>>>,>99.99")))

                    if re.match(r".*\$REV.*",curr_msg, re.IGNORECASE) and not (re.match(r".*REVMTD.*",curr_msg, re.IGNORECASE)) and not (re.match(r".*REV-EXFB.*",curr_msg, re.IGNORECASE)):

                        if flag_group:

                            if substring(curr_msg, 0, 1) == ("-").lower() :
                                val_sign = - 1
                                curr_msg = substring(curr_msg, 1, len(curr_msg))


                            else:
                                val_sign = 1
                        str_result = substring(curr_msg, 0 + get_index(curr_msg, "$rev") , len(curr_msg))

                        if re.match(r".*;.*",str_result, re.IGNORECASE):
                            deptno = to_int(entry(0, entry(1, str_result, " ") , ";"))
                            artno = to_int(trim(entry(1, str_result, ";")))


                            dept_rev = dept_rev(deptno, artno)

                            if flag_group:
                                dept_rev =  to_decimal(val_sign) * to_decimal(dept_rev)
                                str_group = str_group + to_string(dept_rev) + ";"
                                dept_group = deptno
                                curr_msg = replace_str(curr_msg, "$REV " + to_string(deptno) + ";" + to_string(artno) , "delete")


                            else:
                                curr_msg = replace_str(curr_msg, "$REV " + to_string(deptno) + ";" + to_string(artno) , trim(to_string(dept_rev, "->>>,>>>,>>>,>>>,>99.99")))
                        else:
                            deptno = to_int(entry(1, str_result, " "))
                            dept_rev = dept_rev(deptno, 0)

                            if flag_group:
                                dept_rev =  to_decimal(val_sign) * to_decimal(dept_rev)
                                str_group = str_group + to_string(dept_rev) + ";"
                                dept_group = deptno
                                curr_msg = replace_str(curr_msg, "$REV " + to_string(deptno) , "delete")


                            else:
                                curr_msg = replace_str(curr_msg, "$REV " + to_string(deptno) , trim(to_string(dept_rev, "->>>,>>>,>>>,>>>,>99.99")))

                    if re.match(r".*\$GROUP.*",curr_msg, re.IGNORECASE):
                        temp_list = Temp_list()
                        temp_list_list.append(temp_list)

                        temp_list.str = entry(1, curr_msg, " ")
                        temp_list.nr = to_int(entry(2, curr_msg, " "))
                        curr_group = to_int(entry(2, curr_msg, " "))


                        flag_group = True
                        curr_msg = "delete"

                    if re.match(r".*\$END-GROUP.*",curr_msg, re.IGNORECASE):

                        temp_list = query(temp_list_list, filters=(lambda temp_list: temp_list.nr == curr_group), first=True)

                        if temp_list:
                            for i in range(1,num_entries(str_group, ";")  + 1) :
                                tot_group =  to_decimal(tot_group) + to_decimal(to_decimal(entry(i) - to_decimal(1 , str_group , ";")))
                            temp_list.rev =  to_decimal(tot_group)
                        flag_group = False
                        curr_msg = "delete"
                        str_group = ""
                        tot_group =  to_decimal("0")
                        curr_group = 0

                    if re.match(r".*\$BUDGETMTD.*",curr_msg, re.IGNORECASE):

                        if flag_group:

                            if substring(curr_msg, 0, 1) == ("-").lower() :
                                val_sign = - 1
                                curr_msg = substring(curr_msg, 1, len(curr_msg))


                            else:
                                val_sign = 1
                        for i in range(1,num_entries(curr_msg, "$")  + 1) :
                            str = entry(i - 1, curr_msg, "$")

                            if re.match(r".*BUDGETMTD.*",str, re.IGNORECASE):

                                if re.match(r".*;.*",str, re.IGNORECASE):
                                    deptno = to_int(entry(0, entry(1, str, " ") , ";"))
                                    artno = to_int(trim(entry(1, curr_msg, ";")))


                                    mtdbudget = mtd_budget(deptno, artno)
                                    mtdbudgetnonbfast = mtd_budget_non_bfast(deptno, artno)

                                    if flag_group:
                                        mtdbudget =  to_decimal(val_sign) * to_decimal(mtdbudget)
                                        str_group = str_group + to_string(mtdbudgetnonbfast) + ";"
                                        dept_group = deptno
                                        curr_msg = replace_str(curr_msg, "$BUDGETMTD " + to_string(deptno) + ";" + to_string(artno) , "delete")


                                    else:
                                        curr_msg = replace_str(curr_msg, "$BUDGETMTD " + to_string(deptno) + ";" + to_string(artno) , trim(to_string(mtdbudgetnonbfast, "->>>,>>>,>>>,>>>,>99.99")))
                                else:
                                    deptno = to_int(entry(1, str, " "))
                                    mtdbudget = mtd_budget(deptno, 0)
                                    mtdbudgetnonbfast = mtd_budget_non_bfast(deptno, 0)

                                    if flag_group:
                                        mtdbudgetnonbfast =  to_decimal(val_sign) * to_decimal(mtdbudgetnonbfast)
                                        str_group = str_group + to_string(mtdbudgetnonbfast) + ";"
                                        dept_group = deptno
                                        curr_msg = replace_str(curr_msg, "$BUDGETMTD " + to_string(deptno) , "delete")


                                    else:
                                        curr_msg = replace_str(curr_msg, "$BUDGETMTD " + to_string(deptno) , trim(to_string(mtdbudgetnonbfast, "->>>,>>>,>>>,>>>,>99.99")))

                    if re.match(r".*\$BUDGET.*",curr_msg, re.IGNORECASE) and not (re.match(r".*\$BUDGETMTD.*",curr_msg, re.IGNORECASE)):

                        if flag_group:

                            if substring(curr_msg, 0, 1) == ("-").lower() :
                                val_sign = - 1
                                curr_msg = substring(curr_msg, 1, len(curr_msg))


                            else:
                                val_sign = 1
                        str_result = substring(curr_msg, 0 + get_index(curr_msg, "$BUDGET") , len(curr_msg))

                        if re.match(r".*;.*",str_result, re.IGNORECASE):
                            deptno = to_int(entry(0, entry(1, str_result, " ") , ";"))
                            artno = to_int(trim(entry(1, str_result, ";")))


                            tbudget = t_budget(deptno, artno)

                            if flag_group:
                                tbudget =  to_decimal(val_sign) * to_decimal(tbudget)
                                str_group = str_group + to_string(tbudget) + ";"
                                dept_group = deptno
                                curr_msg = replace_str(curr_msg, "$BUDGET " + to_string(deptno) + ";" + to_string(artno) , "delete")


                            else:
                                curr_msg = replace_str(curr_msg, "$BUDGET " + to_string(deptno) + ";" + to_string(artno) , trim(to_string(tbudget, "->>>,>>>,>>>,>>>,>99.99")))
                        else:
                            deptno = to_int(entry(1, str_result, " "))
                            tbudget = t_budget(deptno, 0)

                            if flag_group:
                                tbudget =  to_decimal(val_sign) * to_decimal(tbudget)
                                str_group = str_group + to_string(tbudget) + ";"
                                dept_group = deptno
                                curr_msg = replace_str(curr_msg, "$BUDGET " + to_string(deptno) , "delete")


                            else:
                                curr_msg = replace_str(curr_msg, "$BUDGET " + to_string(deptno) , trim(to_string(tbudget, "->>>,>>>,>>>,>>>,>99.99")))

                    if re.match(r".*\$TTLREVMTD.*",curr_msg, re.IGNORECASE):
                        curr_msg = replace_str(curr_msg, "$TTLREVMTD" , trim(to_string(tot_mtd, "->>>,>>>,>>>,>>>,>99.99")))

                    if re.match(r".*\$TTLREV.*",curr_msg, re.IGNORECASE):
                        curr_msg = replace_str(curr_msg, "$TTLREV" , trim(to_string(tot_rev, "->>>,>>>,>>>,>>>,>99.99")))

                    if re.match(r".*\$AVRATEMTD.*",curr_msg, re.IGNORECASE):
                        mtdavrate = mtd_avrate(bill_date)
                        curr_msg = replace_str(curr_msg, "$AVRATEMTD" , trim(to_string(mtdavrate, "->>>,>>>,>>>,>>>,>99.99")))

                    if re.match(r".*\$avrate.*",curr_msg, re.IGNORECASE):
                        avrate = avrate(bill_date)
                        curr_msg = replace_str(curr_msg, "$avrate" , trim(to_string(avrate, "->>>,>>>,>>>,>>>,>99.99")))

                    if re.match(r".*delete.*",curr_msg, re.IGNORECASE):
                        pass
                    else:
                        rpt_msg = rpt_msg + curr_msg + chr(10) + chr(13)
            OUTPUT STREAM inpstream1 TO VALUE ("C:\\e1-vhp\\output-sms.txt") APPEND UNBUFFERED
            OUTPUT STREAM inpstream1 CLOSE
            rpt_email = rpt_email + rpt_msg + chr(10) + chr(13)
            n = 0
    OUTPUT STREAM inpstream1 TO VALUE ("c:\\e1-vhp\\output-email.txt") APPEND UNBUFFERED
    OUTPUT STREAM inpstream1 CLOSE

    if by_mail:
        n = n + 1
        sms_broadcast = Sms_broadcast()
        db_session.add(sms_broadcast)

        sms_broadcast.key = 2
        sms_broadcast.datum = bill_date
        sms_broadcast.zeit = nzeit
        sms_broadcast.usrid = "**"
        sms_broadcast.char1 = mail_to
        sms_broadcast.broadcast_msg = rpt_email
        sms_broadcast.mstatus = 0
        sms_broadcast.bemerk = "email"


        nzeit = nzeit + 1
        pass

    return generate_output()