#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 23/7/2025
# gitlab: 625
# add table name -> betrag
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Gl_acct, Gl_jouhdr, Gl_journal, Artikel, Umsatz, Bill_line, Hoteldpt, H_bill_line, Billjournal, H_artikel

def check_gledger_currdatebl(currdate:date):

    prepare_cache ([Htparam, Gl_jouhdr, Gl_journal, Artikel, Umsatz, Bill_line, Hoteldpt, H_bill_line, Billjournal, H_artikel])

    gl_bal = to_decimal("0.0")
    diff_u = to_decimal("0.0")
    u = to_decimal("0.0")
    diff_s = to_decimal("0.0")
    s = to_decimal("0.0")
    flag = False
    s_list_data = []
    p_list_data = []
    sysid:string = ""
    acct:string = ""
    htparam = gl_acct = gl_jouhdr = gl_journal = artikel = umsatz = bill_line = hoteldpt = h_bill_line = billjournal = h_artikel = None

    t_list = p_list = s_list = dept_list = None

    t_list_data, T_list = create_model("T_list", {"dept":int, "rechnr":int, "pay":Decimal, "compli":Decimal})
    p_list_data, P_list = create_model("P_list", {"bstr":string, "dept":int, "billno":int, "posbill":int, "billamt":Decimal, "posamt":Decimal})
    s_list_data, S_list = create_model("S_list", {"dept":int, "artnr":int, "artart":int, "bez":string, "betrag":Decimal, "ums":Decimal, "ums1":Decimal})
    dept_list_data, Dept_list = create_model("Dept_list", {"dptnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_bal, diff_u, u, diff_s, s, flag, s_list_data, p_list_data, sysid, acct, htparam, gl_acct, gl_jouhdr, gl_journal, artikel, umsatz, bill_line, hoteldpt, h_bill_line, billjournal, h_artikel
        nonlocal currdate


        nonlocal t_list, p_list, s_list, dept_list
        nonlocal t_list_data, p_list_data, s_list_data, dept_list_data

        return {"gl_bal": gl_bal, "diff_u": diff_u, "u": u, "diff_s": diff_s, "s": s, "flag": flag, "s-list": s_list_data, "p-list": p_list_data}

    def check_dept():

        nonlocal gl_bal, diff_u, u, diff_s, s, flag, s_list_data, p_list_data, sysid, acct, htparam, gl_acct, gl_jouhdr, gl_journal, artikel, umsatz, bill_line, hoteldpt, h_bill_line, billjournal, h_artikel
        nonlocal currdate


        nonlocal t_list, p_list, s_list, dept_list
        nonlocal t_list_data, p_list_data, s_list_data, dept_list_data

        nm:int = 0
        dept_list_data.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 793)]})

        if htparam.fchar == "":

            for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
                dept_list = Dept_list()
                dept_list_data.append(dept_list)

                dept_list.dptnr = hoteldpt.num


        else:
            for nm in range(1,num_entries(htparam.fchar, ",")  + 1) :

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, to_int(entry(nm - 1, htparam.fchar, ",")))]})

                if hoteldpt:
                    dept_list = Dept_list()
                    dept_list_data.append(dept_list)

                    dept_list.dptnr = hoteldpt.num


    def create_fo():

        nonlocal gl_bal, diff_u, u, diff_s, s, flag, s_list_data, p_list_data, sysid, acct, htparam, gl_acct, gl_jouhdr, gl_journal, artikel, umsatz, bill_line, hoteldpt, h_bill_line, billjournal, h_artikel
        nonlocal currdate


        nonlocal t_list, p_list, s_list, dept_list
        nonlocal t_list_data, p_list_data, s_list_data, dept_list_data

        pos_billno:int = 0
        s_list_data.clear()

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.bill_datum == currdate)).order_by(Bill_line._recid).all():

            artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

            if artikel and artikel.artart != 1:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == bill_line.artnr and s_list.dept == bill_line.departement), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = bill_line.artnr
                    s_list.dept = bill_line.departement
                    s_list.bez = artikel.bezeich
                    s_list.artart = artikel.artart


                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(bill_line.betrag)


            else:
                pos_billno = 0
                pos_billno = to_int(substring(bill_line.bezeich, get_index(bill_line.bezeich, " *") + 2 - 1))

                h_bill_line = db_session.query(H_bill_line).filter(
                         (H_bill_line.departement == bill_line.departement) & (H_bill_line.rechnr == pos_billno) & (matches(H_bill_line.bezeich,("*" + to_string(bill_line.rechnr) + "*"))) & (H_bill_line.zeit <= bill_line.zeit) & (H_bill_line.zeit >= (bill_line.zeit - 3))).first()

                if h_bill_line and (h_bill_line.betrag + bill_line.betrag) != 0:
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.dept = h_bill_line.departement
                    p_list.billno = bill_line.rechnr
                    p_list.posbill = h_bill_line.rechnr
                    p_list.billamt =  - to_decimal(bill_line.betrag)
                    p_list.posamt =  to_decimal(h_bill_line.betrag)

        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum == currdate)).order_by(Umsatz._recid).all():

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if (artikel and artikel.artart != 1 and artikel.artart != 9):

                s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == umsatz.artnr and s_list.dept == umsatz.departement), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = umsatz.artnr
                    s_list.dept = umsatz.departement
                    s_list.artart = artikel.artart

                    if artikel:
                        s_list.bez = artikel.bezeich
                s_list.ums =  to_decimal(umsatz.betrag)

            elif not artikel and umsatz.betrag != 0:
                pass

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.bill_datum == currdate) & (Billjournal.anzahl != 0) & (Billjournal.userinit == sysid)).order_by(Billjournal._recid).all():

            artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})

            if artikel and artikel.artart != 9:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    s_list.artnr = billjournal.artnr
                    s_list.dept = billjournal.departement
                    s_list.bez = artikel.bezeich
                    s_list.artart = artikel.artart


                s_list.ums1 =  to_decimal(s_list.ums1) + to_decimal(billjournal.betrag)


                s_list.ums =  to_decimal(s_list.ums) - to_decimal(billjournal.betrag)

            elif not billjournal:
                pass


    def create_fb():

        nonlocal gl_bal, diff_u, u, diff_s, s, flag, s_list_data, p_list_data, sysid, acct, htparam, gl_acct, gl_jouhdr, gl_journal, artikel, umsatz, bill_line, hoteldpt, h_bill_line, billjournal, h_artikel
        nonlocal currdate


        nonlocal t_list, p_list, s_list, dept_list
        nonlocal t_list_data, p_list_data, s_list_data, dept_list_data

        fo_billno:int = 0
        pos_billno:int = 0
        dept:int = 0
        balance:Decimal = to_decimal("0.0")
        t_list_data.clear()

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.bill_datum == currdate)).order_by(H_bill_line.departement, H_bill_line.rechnr).all():

            if pos_billno == 0:
                pos_billno = h_bill_line.rechnr
                dept = h_bill_line.departement

            if ((pos_billno != h_bill_line.rechnr) or (dept != h_bill_line.departement)):

                if balance != 0:
                    p_list = P_list()
                    p_list_data.append(p_list)

                    p_list.bstr = "*"
                    p_list.dept = dept
                    p_list.posbill = pos_billno
                    p_list.posamt =  to_decimal(balance)


                balance =  to_decimal("0")
                pos_billno = h_bill_line.rechnr
                dept = h_bill_line.departement
            balance =  to_decimal(balance) + to_decimal(h_bill_line.betrag)

            if h_bill_line.artnr == 0:

                t_list = query(t_list_data, filters=(lambda t_list: t_list.dept == h_bill_line.departement and t_list.rechnr == h_bill_line.rechnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.dept = h_bill_line.departement
                    t_list.rechnr = h_bill_line.rechnr


                t_list.pay =  to_decimal(t_list.pay) + to_decimal(h_bill_line.betrag)
            else:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

                if h_artikel.artart != 0:

                    t_list = query(t_list_data, filters=(lambda t_list: t_list.dept == h_bill_line.departement and t_list.rechnr == h_bill_line.rechnr), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_data.append(t_list)

                        t_list.dept = h_bill_line.departement
                        t_list.rechnr = h_bill_line.rechnr

                    if h_artikel.artart <= 7:
                        t_list.pay =  to_decimal(t_list.pay) + to_decimal(h_bill_line.betrag)
                    else:
                        t_list.compli =  to_decimal(t_list.compli) + to_decimal(h_bill_line.betrag)

        if balance != 0:
            p_list = P_list()
            p_list_data.append(p_list)

            p_list.bstr = "*"
            p_list.dept = dept
            p_list.posbill = pos_billno
            p_list.posamt =  to_decimal(balance)

        for t_list in query(t_list_data, filters=(lambda t_list: t_list.pay != 0)):

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.rechnr == t_list.rechnr) & (H_bill_line.departement == t_list.dept)).order_by(H_bill_line.departement, H_bill_line.rechnr).all():

                if h_bill_line.artnr != 0:

                    h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

                    if h_artikel.artart <= 7:

                        if h_artikel.artart == 0:

                            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
                        else:

                            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                        umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.artnr)],"datum": [(eq, currdate)]})

                        s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == artikel.artnr and s_list.dept == artikel.departement), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_data.append(s_list)

                            s_list.bez = artikel.bezeich

                            if umsatz:
                                s_list.artnr = umsatz.artnr
                                s_list.dept = umsatz.departement
                                s_list.ums =  to_decimal(umsatz.betrag)


                        s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(h_bill_line.betrag)
                else:
                    fo_billno = 0
                    fo_billno = to_int(substring(h_bill_line.bezeich, get_index(h_bill_line.bezeich, " *") + 2 - 1))

                    billjournal = db_session.query(Billjournal).filter(
                             (Billjournal.rechnr == fo_billno) & (Billjournal.bill_datum == h_bill_line.bill_datum) & (matches(Billjournal.bezeich,("*" + to_string(h_bill_line.rechnr) + "*"))) & (Billjournal.zeit >= h_bill_line.zeit) & (Billjournal.zeit <= (h_bill_line.zeit + 3))).first()

                    if billjournal and (h_bill_line.betrag + billjournal.betrag) != 0:
                        p_list = P_list()
                        p_list_data.append(p_list)

                        p_list.dept = h_bill_line.departement
                        p_list.billno = billjournal.rechnr
                        p_list.posbill = h_bill_line.rechnr
                        p_list.billamt =  to_decimal(billjournal.betrag)
                        p_list.posamt =  - to_decimal(h_bill_line.betrag)

                    elif not billjournal:
                        p_list = P_list()
                        p_list_data.append(p_list)

                        p_list.dept = h_bill_line.departement
                        p_list.posbill = h_bill_line.rechnr
                        p_list.posamt =  - to_decimal(h_bill_line.betrag)

        for s_list in query(s_list_data, filters=(lambda s_list: s_list.ums == 0 and s_list.betrag == 0 and s_list.ums1 == 0)):
            s_list_data.remove(s_list)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 104)]})

    if htparam:
        sysid = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 998)]})

    if htparam:
        acct = htparam.fchar

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, acct)]})
    check_dept()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.datum == currdate)).order_by(Gl_jouhdr._recid).all():

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr.jnr) & (Gl_journal.fibukonto == (acct).lower())).order_by(Gl_journal._recid).all():
            gl_bal =  to_decimal(gl_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

    umsatz_obj_list = {}
    for umsatz, artikel in db_session.query(Umsatz, Artikel).join(Artikel,(Artikel.artnr == Umsatz.artnr) & (Artikel.departement == Umsatz.departement)).filter(
             (Umsatz.datum == currdate)).order_by(Umsatz._recid).all():
        dept_list = query(dept_list_data, (lambda dept_list: dept_list.dptnr == umsatz.departement), first=True)
        if not dept_list:
            continue

        if umsatz_obj_list.get(umsatz._recid):
            continue
        else:
            umsatz_obj_list[umsatz._recid] = True

        if artikel.artart == 0 or artikel.artart == 2 or artikel.artart == 5 or artikel.artart == 6 or artikel.artart == 7 or artikel.artart == 8:
            u =  to_decimal(u) + to_decimal(umsatz.betrag)
    diff_u =  to_decimal(gl_bal) - to_decimal(u)

    bill_line_obj_list = {}
    for bill_line in db_session.query(Bill_line).filter(
             (Bill_line.bill_datum == currdate)).order_by(Bill_line._recid).all():
        dept_list = query(dept_list_data, (lambda dept_list: dept_list.dptnr == bill_line.departement), first=True)
        if not dept_list:
            continue

        if bill_line_obj_list.get(bill_line._recid):
            continue
        else:
            bill_line_obj_list[bill_line._recid] = True


        s =  to_decimal(s) + to_decimal(bill_line.betrag)
    diff_s =  to_decimal(gl_bal) - to_decimal(s)

    if (u - s) != 0:
        create_fo()
        create_fb()
        flag = True

    return generate_output()