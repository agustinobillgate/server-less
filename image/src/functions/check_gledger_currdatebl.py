from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Gl_acct, Gl_jouhdr, Gl_journal, Artikel, Umsatz, Bill_line, Hoteldpt, H_bill_line, Billjournal, H_artikel

def check_gledger_currdatebl(currdate:date):
    gl_bal = 0
    diff_u = 0
    u = 0
    diff_s = 0
    s = 0
    flag = False
    s_list_list = []
    p_list_list = []
    sysid:str = ""
    acct:str = ""
    htparam = gl_acct = gl_jouhdr = gl_journal = artikel = umsatz = bill_line = hoteldpt = h_bill_line = billjournal = h_artikel = None

    t_list = p_list = s_list = dept_list = None

    t_list_list, T_list = create_model("T_list", {"dept":int, "rechnr":int, "pay":decimal, "compli":decimal})
    p_list_list, P_list = create_model("P_list", {"bstr":str, "dept":int, "billno":int, "posbill":int, "billamt":decimal, "posamt":decimal})
    s_list_list, S_list = create_model("S_list", {"dept":int, "artnr":int, "artikel.artart":int, "bez":str, "betrag":decimal, "ums":decimal, "ums1":decimal})
    dept_list_list, Dept_list = create_model("Dept_list", {"dptnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_bal, diff_u, u, diff_s, s, flag, s_list_list, p_list_list, sysid, acct, htparam, gl_acct, gl_jouhdr, gl_journal, artikel, umsatz, bill_line, hoteldpt, h_bill_line, billjournal, h_artikel


        nonlocal t_list, p_list, s_list, dept_list
        nonlocal t_list_list, p_list_list, s_list_list, dept_list_list
        return {"gl_bal": gl_bal, "diff_u": diff_u, "u": u, "diff_s": diff_s, "s": s, "flag": flag, "s-list": s_list_list, "p-list": p_list_list}

    def check_dept():

        nonlocal gl_bal, diff_u, u, diff_s, s, flag, s_list_list, p_list_list, sysid, acct, htparam, gl_acct, gl_jouhdr, gl_journal, artikel, umsatz, bill_line, hoteldpt, h_bill_line, billjournal, h_artikel


        nonlocal t_list, p_list, s_list, dept_list
        nonlocal t_list_list, p_list_list, s_list_list, dept_list_list

        nm:int = 0
        dept_list_list.clear()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 793)).first()

        if htparam.fchar == "":

            for hoteldpt in db_session.query(Hoteldpt).all():
                dept_list = Dept_list()
                dept_list_list.append(dept_list)

                dept_list.dptnr = hoteldpt.num


        else:
            for nm in range(1,num_entries(htparam.fchar, ",")  + 1) :

                hoteldpt = db_session.query(Hoteldpt).filter(
                        (Hoteldpt.num == to_int(entry(nm - 1, htparam.fchar, ",")))).first()

                if hoteldpt:
                    dept_list = Dept_list()
                    dept_list_list.append(dept_list)

                    dept_list.dptnr = hoteldpt.num

    def create_fo():

        nonlocal gl_bal, diff_u, u, diff_s, s, flag, s_list_list, p_list_list, sysid, acct, htparam, gl_acct, gl_jouhdr, gl_journal, artikel, umsatz, bill_line, hoteldpt, h_bill_line, billjournal, h_artikel


        nonlocal t_list, p_list, s_list, dept_list
        nonlocal t_list_list, p_list_list, s_list_list, dept_list_list

        pos_billno:int = 0
        s_list_list.clear()

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.bill_datum == currdate)).all():

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

            if artikel.artart != 1:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == bill_line.artnr and s_list.dept == bill_line.departement), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = bill_line.artnr
                    s_list.dept = bill_line.departement
                    s_list.bez = artikel.bezeich
                    s_list.artikel.artart = artikel.artart


                s_list.betrag = s_list.betrag + bill_line.betrag


            else:
                pos_billno = 0
                pos_billno = to_int(substring(bill_line.bezeich,0 + get_index(bill_line.bezeich, " *") + 2))

                h_bill_line = db_session.query(H_bill_line).filter(
                        (H_bill_line.departement == bill_line.departement) &  (H_bill_line.rechnr == pos_billno) &  (H_bill_line.bezeich.op("~")(".*" + to_string(bill_line.rechnr) + "*")) &  (H_bill_line.zeit <= bill_line.zeit) &  (H_bill_line.zeit >= (bill_line.zeit - 3))).first()

                if h_bill_line and (h_bill_line.betrag + bill_line.betrag) != 0:
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.dept = h_bill_line.departement
                    p_list.billno = bill_line.rechnr
                    p_list.posbill = h_bill_line.rechnr
                    p_list.billamt = - bill_line.betrag
                    p_list.posamt = h_bill_line.betrag

        for umsatz in db_session.query(Umsatz).filter(
                (Umsatz.datum == currdate)).all():

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == umsatz.artnr) &  (Artikel.departement == umsatz.departement)).first()

            if (artikel and artikel.artart != 1 and artikel.artart != 9):

                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == umsatz.artnr and s_list.dept == umsatz.departement), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = umsatz.artnr
                    s_list.dept = umsatz.departement
                    s_list.artikel.artart = artikel.artart

                    if artikel:
                        s_list.bez = artikel.bezeich
                s_list.ums = umsatz.betrag

            elif not artikel and umsatz.betrag != 0:

        for billjournal in db_session.query(Billjournal).filter(
                (Billjournal.bill_datum == currdate) &  (Billjournal.anzahl != 0) &  (Billjournal.userinit == sysid)).all():

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == billjournal.artnr) &  (Artikel.departement == billjournal.departement)).first()

            if artikel and artikel.artart != 9:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == billjournal.artnr and s_list.dept == billjournal.departement), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = billjournal.artnr
                    s_list.dept = billjournal.departement
                    s_list.bez = artikel.bezeich
                    s_list.artikel.artart = artikel.artart


                s_list.ums1 = s_list.ums1 + billjournal.betrag


                s_list.ums = s_list.ums - billjournal.betrag

            elif not billjournal:

    def create_fb():

        nonlocal gl_bal, diff_u, u, diff_s, s, flag, s_list_list, p_list_list, sysid, acct, htparam, gl_acct, gl_jouhdr, gl_journal, artikel, umsatz, bill_line, hoteldpt, h_bill_line, billjournal, h_artikel


        nonlocal t_list, p_list, s_list, dept_list
        nonlocal t_list_list, p_list_list, s_list_list, dept_list_list

        fo_billno:int = 0
        pos_billno:int = 0
        dept:int = 0
        balance:decimal = 0
        t_list_list.clear()

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.bill_datum == currdate)).all():

            if pos_billno == 0:
                pos_billno = h_bill_line.rechnr
                dept = h_bill_line.departement

            if ((pos_billno != h_bill_line.rechnr) or (dept != h_bill_line.departement)):

                if balance != 0:
                    p_list = P_list()
                    p_list_list.append(p_list)

                    p_list.bstr = "*"
                    p_list.dept = dept
                    p_list.posbill = pos_billno
                    p_list.posamt = balance


                balance = 0
                pos_billno = h_bill_line.rechnr
                dept = h_bill_line.departement
            balance = balance + betrag

            if h_bill_line.artnr == 0:

                t_list = query(t_list_list, filters=(lambda t_list :t_list.dept == h_bill_line.departement and t_list.rechnr == h_bill_line.rechnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.dept = h_bill_line.departement
                    t_list.rechnr = h_bill_line.rechnr


                t_list.pay = t_list.pay + h_bill_line.betrag
            else:

                h_artikel = db_session.query(H_artikel).filter(
                        (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()

                if h_artikel.artart != 0:

                    t_list = query(t_list_list, filters=(lambda t_list :t_list.dept == h_bill_line.departement and t_list.rechnr == h_bill_line.rechnr), first=True)

                    if not t_list:
                        t_list = T_list()
                        t_list_list.append(t_list)

                        t_list.dept = h_bill_line.departement
                        t_list.rechnr = h_bill_line.rechnr

                    if h_artikel.artart <= 7:
                        t_list.pay = t_list.pay + h_bill_line.betrag
                    else:
                        t_list.compli = t_list.compli + h_bill_line.betrag

        if balance != 0:
            p_list = P_list()
            p_list_list.append(p_list)

            p_list.bstr = "*"
            p_list.dept = dept
            p_list.posbill = pos_billno
            p_list.posamt = balance

        for t_list in query(t_list_list, filters=(lambda t_list :t_list.pay != 0)):

            for h_bill_line in db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == t_list.rechnr) &  (H_bill_line.departement == t_list.dept)).all():

                if h_bill_line.artnr != 0:

                    h_artikel = db_session.query(H_artikel).filter(
                            (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()

                    if h_artikel.artart <= 7:

                        if h_artikel.artart == 0:

                            artikel = db_session.query(Artikel).filter(
                                    (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()
                        else:

                            artikel = db_session.query(Artikel).filter(
                                    (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == 0)).first()

                        umsatz = db_session.query(Umsatz).filter(
                                (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.artnr) &  (Umsatz.datum == currdate)).first()

                        s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == artikel.artnr and s_list.dept == artikel.departement), first=True)

                        if not s_list:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.bez = artikel.bezeich

                            if umsatz:
                                s_list.artnr = umsatz.artnr
                                s_list.dept = umsatz.departement
                                s_list.ums = umsatz.betrag


                        s_list.betrag = s_list.betrag + h_bill_line.betrag
                else:
                    fo_billno = 0
                    fo_billno = to_int(substring(h_bill_line.bezeich,0 + get_index(h_bill_line.bezeich, " *") + 2))

                    billjournal = db_session.query(Billjournal).filter(
                            (Billjournal.rechnr == fo_billno) &  (Billjournal.bill_datum == h_bill_line.bill_datum) &  (Billjournal.bezeich.op("~")(".*" + to_string(h_bill_line.rechnr) + "*")) &  (Billjournal.zeit >= h_bill_line.zeit) &  (Billjournal.zeit <= (h_bill_line.zeit + 3))).first()

                    if billjournal and (h_bill_line.betrag + billjournal.betrag) != 0:
                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.dept = h_bill_line.departement
                        p_list.billno = billjournal.rechnr
                        p_list.posbill = h_bill_line.rechnr
                        p_list.billamt = billjournal.betrag
                        p_list.posamt = - h_bill_line.betrag

                    elif not billjournal:
                        p_list = P_list()
                        p_list_list.append(p_list)

                        p_list.dept = h_bill_line.departement
                        p_list.posbill = h_bill_line.rechnr
                        p_list.posamt = - h_bill_line.betrag

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.ums == 0 and s_list.betrag == 0 and s_list.ums1 == 0)):
            s_list_list.remove(s_list)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 104)).first()

    if htparam:
        sysid = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 998)).first()

    if htparam:
        acct = htparam.fchar

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (acct).lower())).first()
    check_dept()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.datum == currdate)).all():

        for gl_journal in db_session.query(Gl_journal).filter(
                (Gl_journal.jnr == gl_jouhdr.jnr) &  (func.lower(Gl_journal.fibukonto) == (acct).lower())).all():
            gl_bal = gl_bal + gl_journal.debit - gl_journal.credit

    umsatz_obj_list = []
    for umsatz, artikel, dept_list in db_session.query(Umsatz, Artikel, Dept_list).join(Artikel,(Artikel.artnr == Umsatz.artnr) &  (Artikel.departement == Umsatz.departement)).join(Dept_list,(Dept_list.dptnr == Umsatz.departement)).filter(
            (Umsatz.datum == currdate)).all():
        if umsatz._recid in umsatz_obj_list:
            continue
        else:
            umsatz_obj_list.append(umsatz._recid)

        if artikel.artart == 0 or artikel.artart == 2 or artikel.artart == 5 or artikel.artart == 6 or artikel.artart == 7 or artikel.artart == 8:
            u = u + umsatz.betrag
    diff_u = gl_bal - u

    bill_line_obj_list = []
    for bill_line, dept_list in db_session.query(Bill_line, Dept_list).join(Dept_list,(Dept_list.dptnr == Bill_line.departement)).filter(
            (Bill_line.bill_datum == currdate)).all():
        if bill_line._recid in bill_line_obj_list:
            continue
        else:
            bill_line_obj_list.append(bill_line._recid)


        s = s + bill_line.betrag
    diff_s = gl_bal - s

    if (u - s) != 0:
        create_fo()
        create_fb()
        flag = True

    return generate_output()