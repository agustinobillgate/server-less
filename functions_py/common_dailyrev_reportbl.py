#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 15-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from models import Queasy, Htparam, Hoteldpt, Gl_main, Gl_acct, Gl_jouhdr, Gl_journal, L_op, L_artikel, L_lieferant, L_ophis, Umsatz, Artikel, Res_line, Reservation, Guest, Zimkateg, Genstat, Zinrstat, Zkstat, Segment

def common_dailyrev_reportbl():

    prepare_cache ([Queasy, Htparam, Hoteldpt, Gl_main, Gl_acct, Gl_jouhdr, Gl_journal, L_op, L_ophis, Umsatz, Artikel, Res_line, Reservation, Genstat, Zinrstat, Zkstat, Segment])

    plist_data = []
    mm:int = 0
    yy:int = 0
    datum1:date = None
    loopi:int = 0
    bill_date:date = None
    sdatum:date = None
    sdatum1:date = None
    datum2:date = None
    counter:int = 19
    f_endkum:int = 0
    m_endkum:int = 0
    spadept:int = 0
    str1:string = ""
    fdate:date = None
    tdate:date = None
    fact:Decimal = to_decimal("0.0")
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    nett_amt:Decimal = to_decimal("0.0")
    nett_serv:Decimal = to_decimal("0.0")
    nett_tax:Decimal = to_decimal("0.0")
    artikel_service_code:int = 0
    artikel_mwst_code:int = 0
    total_ooo:Decimal = to_decimal("0.0")
    queasy = htparam = hoteldpt = gl_main = gl_acct = gl_jouhdr = gl_journal = l_op = l_artikel = l_lieferant = l_ophis = umsatz = artikel = res_line = reservation = guest = zimkateg = genstat = zinrstat = zkstat = segment = None

    plist = outlet_list = room_expenses = expenses_list = cost_list = artikel_list = blist = mlist = bqueasy = mlist = blist = olist = blist = None

    plist_data, Plist = create_model("Plist", {"datum":date, "bezeich":string, "amount":Decimal, "flag":int})
    outlet_list_data, Outlet_list = create_model("Outlet_list", {"deptnr":int, "departement":string})
    room_expenses_data, Room_expenses = create_model("Room_expenses", {"account_name":string, "main_nr":int})
    expenses_list_data, Expenses_list = create_model("Expenses_list", {"account_name":string, "main_nr":int})
    cost_list_data, Cost_list = create_model("Cost_list", {"account_name":string, "fibukonto":string})
    artikel_list_data, Artikel_list = create_model("Artikel_list", {"artnr":int, "depart":int})

    Blist = Plist
    blist_data = plist_data

    Mlist = Plist
    mlist_data = plist_data

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data

        return {"plist": plist_data}

    def fill_energycost():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Total Energy Cost"
        plist.flag = 41


        cost_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "energycost")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    cost_list = Cost_list()
                    cost_list_data.append(cost_list)

                    cost_list.fibukonto = entry(1, str1, "|")

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto) & (Gl_acct.deptnr != spadept)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.fibukonto == gl_journal.fibukonto), first=True)
                if not cost_list:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True

                plist = query(plist_data, filters=(lambda plist: plist.bezeich == cost_list.account_name), first=True)

                if plist:
                    plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_payrollexpenses():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Payroll & Related Expenses"
        plist.flag = 40


        room_expenses_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "payrollexpenses")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    room_expenses = Room_expenses()
                    room_expenses_data.append(room_expenses)

                    room_expenses.main_nr = to_int(entry(0, str1, "|"))

                    gl_main = get_cache (Gl_main, {"nr": [(eq, room_expenses.main_nr)]})

                    if gl_main:
                        room_expenses.account_name = gl_main.bezeich

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                room_expenses = query(room_expenses_data, (lambda room_expenses: room_expenses.main_nr == gl_acct.main_nr), first=True)
                if not room_expenses:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_pomecexpenses():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "POMEC Other Expenses"
        plist.flag = 39


        room_expenses_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "pomecexpenses")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    room_expenses = Room_expenses()
                    room_expenses_data.append(room_expenses)

                    room_expenses.main_nr = to_int(entry(0, str1, "|"))

                    gl_main = get_cache (Gl_main, {"nr": [(eq, room_expenses.main_nr)]})

                    if gl_main:
                        room_expenses.account_name = gl_main.bezeich

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                room_expenses = query(room_expenses_data, (lambda room_expenses: room_expenses.main_nr == gl_acct.main_nr), first=True)
                if not room_expenses:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_smexpenses():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "S&M Other Expenses"
        plist.flag = 38


        room_expenses_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "smexpenses")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    room_expenses = Room_expenses()
                    room_expenses_data.append(room_expenses)

                    room_expenses.main_nr = to_int(entry(0, str1, "|"))

                    gl_main = get_cache (Gl_main, {"nr": [(eq, room_expenses.main_nr)]})

                    if gl_main:
                        room_expenses.account_name = gl_main.bezeich

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                room_expenses = query(room_expenses_data, (lambda room_expenses: room_expenses.main_nr == gl_acct.main_nr), first=True)
                if not room_expenses:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_hrdexpenses():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "HRD Other Expenses"
        plist.flag = 37


        room_expenses_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "hrdexpenses")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    room_expenses = Room_expenses()
                    room_expenses_data.append(room_expenses)

                    room_expenses.main_nr = to_int(entry(0, str1, "|"))

                    gl_main = get_cache (Gl_main, {"nr": [(eq, room_expenses.main_nr)]})

                    if gl_main:
                        room_expenses.account_name = gl_main.bezeich

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                room_expenses = query(room_expenses_data, (lambda room_expenses: room_expenses.main_nr == gl_acct.main_nr), first=True)
                if not room_expenses:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_agexpenses():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "A&G Other Expenses"
        plist.flag = 36


        room_expenses_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "agexpenses")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    room_expenses = Room_expenses()
                    room_expenses_data.append(room_expenses)

                    room_expenses.main_nr = to_int(entry(0, str1, "|"))

                    gl_main = get_cache (Gl_main, {"nr": [(eq, room_expenses.main_nr)]})

                    if gl_main:
                        room_expenses.account_name = gl_main.bezeich

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                room_expenses = query(room_expenses_data, (lambda room_expenses: room_expenses.main_nr == gl_acct.main_nr), first=True)
                if not room_expenses:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_minorexpenses():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Minor Dept Other Expenses"
        plist.flag = 35


        room_expenses_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "minorexpenses")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    room_expenses = Room_expenses()
                    room_expenses_data.append(room_expenses)

                    room_expenses.main_nr = to_int(entry(0, str1, "|"))

                    gl_main = get_cache (Gl_main, {"nr": [(eq, room_expenses.main_nr)]})

                    if gl_main:
                        room_expenses.account_name = gl_main.bezeich

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                room_expenses = query(room_expenses_data, (lambda room_expenses: room_expenses.main_nr == gl_acct.main_nr), first=True)
                if not room_expenses:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_spaexpenses():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "SPA Other Expenses"
        plist.flag = 34


        room_expenses_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "spaexpenses")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    room_expenses = Room_expenses()
                    room_expenses_data.append(room_expenses)

                    room_expenses.main_nr = to_int(entry(0, str1, "|"))

                    gl_main = get_cache (Gl_main, {"nr": [(eq, room_expenses.main_nr)]})

                    if gl_main:
                        room_expenses.account_name = gl_main.bezeich

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                room_expenses = query(room_expenses_data, (lambda room_expenses: room_expenses.main_nr == gl_acct.main_nr), first=True)
                if not room_expenses:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_fbexcpenses():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "FB Other Expenses"
        plist.flag = 33


        room_expenses_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "fbexpenses")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    room_expenses = Room_expenses()
                    room_expenses_data.append(room_expenses)

                    room_expenses.main_nr = to_int(entry(0, str1, "|"))

                    gl_main = get_cache (Gl_main, {"nr": [(eq, room_expenses.main_nr)]})

                    if gl_main:
                        room_expenses.account_name = gl_main.bezeich

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                room_expenses = query(room_expenses_data, (lambda room_expenses: room_expenses.main_nr == gl_acct.main_nr), first=True)
                if not room_expenses:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_roomexpenses():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Room Div. Other Expenses"
        plist.flag = 32


        room_expenses_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "roomexpenses")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    room_expenses = Room_expenses()
                    room_expenses_data.append(room_expenses)

                    room_expenses.main_nr = to_int(entry(0, str1, "|"))

                    gl_main = get_cache (Gl_main, {"nr": [(eq, room_expenses.main_nr)]})

                    if gl_main:
                        room_expenses.account_name = gl_main.bezeich

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                room_expenses = query(room_expenses_data, (lambda room_expenses: room_expenses.main_nr == gl_acct.main_nr), first=True)
                if not room_expenses:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_transportcost():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Transportation & Guest Activities Cost"
        plist.flag = 31


        cost_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "transportcost")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    cost_list = Cost_list()
                    cost_list_data.append(cost_list)

                    cost_list.fibukonto = entry(1, str1, "|")

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto) & (Gl_acct.deptnr != spadept)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.fibukonto == gl_journal.fibukonto), first=True)
                if not cost_list:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True

                plist = query(plist_data, filters=(lambda plist: plist.bezeich == cost_list.account_name), first=True)

                if plist:
                    plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_laundrycost():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Laundry Cost"
        plist.flag = 30


        cost_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "laundrycost")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    cost_list = Cost_list()
                    cost_list_data.append(cost_list)

                    cost_list.fibukonto = entry(1, str1, "|")

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto) & (Gl_acct.deptnr != spadept)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.fibukonto == gl_journal.fibukonto), first=True)
                if not cost_list:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True

                plist = query(plist_data, filters=(lambda plist: plist.bezeich == cost_list.account_name), first=True)

                if plist:
                    plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_spacost():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Spa Cost"
        plist.flag = 29


        cost_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "spacost")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    cost_list = Cost_list()
                    cost_list_data.append(cost_list)

                    cost_list.fibukonto = entry(1, str1, "|")

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto) & (Gl_acct.deptnr != spadept)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.fibukonto == gl_journal.fibukonto), first=True)
                if not cost_list:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True

                plist = query(plist_data, filters=(lambda plist: plist.bezeich == cost_list.account_name), first=True)

                if plist:
                    plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_bqtcost():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Banquet / Other FB Cost"
        plist.flag = 28


        cost_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "bqtcost")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    cost_list = Cost_list()
                    cost_list_data.append(cost_list)

                    cost_list.fibukonto = entry(1, str1, "|")

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr._recid).all():

            gl_journal_obj_list = {}
            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto) & (Gl_acct.deptnr != spadept)).filter(
                     (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.fibukonto == gl_journal.fibukonto), first=True)
                if not cost_list:
                    continue

                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True

                plist = query(plist_data, filters=(lambda plist: plist.bezeich == cost_list.account_name), first=True)

                if plist:
                    plist.amount =  to_decimal(plist.amount) + to_decimal((gl_journal.debit) - to_decimal(gl_journal.credit) )


    def fill_bevcost():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Beverage Cost"
        plist.flag = 27

        l_op = get_cache (L_op, {"datum": [(ge, fdate),(le, tdate)]})

        if l_op:

            l_op_obj_list = {}
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == 2)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                         (L_op.datum >= fdate) & (L_op.datum <= tdate) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1)).order_by(L_lieferant.firma, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal(l_op.warenwert)


        else:

            l_ophis_obj_list = {}
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == 2)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                         (L_ophis.datum >= fdate) & (L_ophis.datum <= tdate) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_lieferant.firma, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal(l_ophis.warenwert)


    def fill_foodcost():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Food Cost"
        plist.flag = 26

        l_op = get_cache (L_op, {"datum": [(ge, fdate),(le, tdate)]})

        if l_op:

            l_op_obj_list = {}
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == 1)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                         (L_op.datum >= fdate) & (L_op.datum <= tdate) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1)).order_by(L_lieferant.firma, L_op.datum, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal(l_op.warenwert)


        else:

            l_ophis_obj_list = {}
            for l_ophis, l_artikel, l_lieferant in db_session.query(L_ophis, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_ophis.artnr) & (L_artikel.endkum == 1)).join(L_lieferant,(L_lieferant.lief_nr == L_ophis.lief_nr)).filter(
                         (L_ophis.datum >= fdate) & (L_ophis.datum <= tdate) & (L_ophis.lief_nr > 0) & (L_ophis.op_art == 1) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_lieferant.firma, L_ophis.datum, L_artikel.bezeich).all():
                if l_ophis_obj_list.get(l_ophis._recid):
                    continue
                else:
                    l_ophis_obj_list[l_ophis._recid] = True


                plist.amount =  to_decimal(plist.amount) + to_decimal(l_ophis.warenwert)


    def fill_otherrevenue():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Other Income Revenue"
        plist.flag = 25


        artikel_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "otherrevenue")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    artikel_list = Artikel_list()
                    artikel_list_data.append(artikel_list)

                    artikel_list.artnr = to_int(entry(0, str1, "|"))
                    artikel_list.depart = to_int(entry(1, str1, "|"))

        umsatz_obj_list = {}
        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= fdate) & (Umsatz.datum <= tdate)).order_by(Umsatz._recid).all():
            artikel_list = query(artikel_list_data, (lambda artikel_list: artikel_list.artnr == umsatz.artnr and artikel_list.depart == umsatz.departement), first=True)
            if not artikel_list:
                continue

            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:
                artikel_service_code = artikel.service_code
                artikel_mwst_code = artikel.mwst_code


            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel_service_code, artikel_mwst_code))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

            if vat == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal("0")
                nett_tax =  to_decimal(umsatz.betrag)

            elif serv == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal(umsatz.betrag)
                nett_tax =  to_decimal("0")


            else:
                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


            plist.datum = umsatz.datum

            if nett_amt != 0:
                plist.amount =  to_decimal(plist.amount) + to_decimal(nett_amt)


            else:
                plist.amount =  to_decimal(plist.amount) + to_decimal(umsatz.betrag)


    def fill_telprevenue():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Telephone Revenue"
        plist.flag = 24


        artikel_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "tlprevenue")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    artikel_list = Artikel_list()
                    artikel_list_data.append(artikel_list)

                    artikel_list.artnr = to_int(entry(0, str1, "|"))
                    artikel_list.depart = to_int(entry(1, str1, "|"))

        umsatz_obj_list = {}
        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= fdate) & (Umsatz.datum <= tdate)).order_by(Umsatz._recid).all():
            artikel_list = query(artikel_list_data, (lambda artikel_list: artikel_list.artnr == umsatz.artnr and artikel_list.depart == umsatz.departement), first=True)
            if not artikel_list:
                continue

            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:
                artikel_service_code = artikel.service_code
                artikel_mwst_code = artikel.mwst_code


            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel_service_code, artikel_mwst_code))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

            if vat == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal("0")
                nett_tax =  to_decimal(umsatz.betrag)

            elif serv == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal(umsatz.betrag)
                nett_tax =  to_decimal("0")


            else:
                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


            plist.datum = umsatz.datum

            if nett_amt != 0:
                plist.amount =  to_decimal(plist.amount) + to_decimal(nett_amt)


            else:
                plist.amount =  to_decimal(plist.amount) + to_decimal(umsatz.betrag)


    def fill_bcenterrevenue():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Bussiness Center Revenue"
        plist.flag = 23


        artikel_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "bcenterrevenue")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    artikel_list = Artikel_list()
                    artikel_list_data.append(artikel_list)

                    artikel_list.artnr = to_int(entry(0, str1, "|"))
                    artikel_list.depart = to_int(entry(1, str1, "|"))

        umsatz_obj_list = {}
        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= fdate) & (Umsatz.datum <= tdate)).order_by(Umsatz._recid).all():
            artikel_list = query(artikel_list_data, (lambda artikel_list: artikel_list.artnr == umsatz.artnr and artikel_list.depart == umsatz.departement), first=True)
            if not artikel_list:
                continue

            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:
                artikel_service_code = artikel.service_code
                artikel_mwst_code = artikel.mwst_code


            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel_service_code, artikel_mwst_code))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

            if vat == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal("0")
                nett_tax =  to_decimal(umsatz.betrag)

            elif serv == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal(umsatz.betrag)
                nett_tax =  to_decimal("0")


            else:
                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


            plist.datum = umsatz.datum

            if nett_amt != 0:
                plist.amount =  to_decimal(plist.amount) + to_decimal(nett_amt)


            else:
                plist.amount =  to_decimal(plist.amount) + to_decimal(umsatz.betrag)


    def fill_laundryrevenue():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Laundry Revenue"
        plist.flag = 22


        artikel_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "laundryrevenue")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    artikel_list = Artikel_list()
                    artikel_list_data.append(artikel_list)

                    artikel_list.artnr = to_int(entry(0, str1, "|"))
                    artikel_list.depart = to_int(entry(1, str1, "|"))

        umsatz_obj_list = {}
        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= fdate) & (Umsatz.datum <= tdate)).order_by(Umsatz._recid).all():
            artikel_list = query(artikel_list_data, (lambda artikel_list: artikel_list.artnr == umsatz.artnr and artikel_list.depart == umsatz.departement), first=True)
            if not artikel_list:
                continue

            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:
                artikel_service_code = artikel.service_code
                artikel_mwst_code = artikel.mwst_code


            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel_service_code, artikel_mwst_code))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

            if vat == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal("0")
                nett_tax =  to_decimal(umsatz.betrag)

            elif serv == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal(umsatz.betrag)
                nett_tax =  to_decimal("0")


            else:
                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


            plist.datum = umsatz.datum

            if nett_amt != 0:
                plist.amount =  to_decimal(plist.amount) + to_decimal(nett_amt)


            else:
                plist.amount =  to_decimal(plist.amount) + to_decimal(umsatz.betrag)


    def fill_sparevenue():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Spa Revenue"
        plist.flag = 21


        artikel_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "sparevenue")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    artikel_list = Artikel_list()
                    artikel_list_data.append(artikel_list)

                    artikel_list.artnr = to_int(entry(0, str1, "|"))
                    artikel_list.depart = to_int(entry(1, str1, "|"))

        umsatz_obj_list = {}
        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= fdate) & (Umsatz.datum <= tdate)).order_by(Umsatz._recid).all():
            artikel_list = query(artikel_list_data, (lambda artikel_list: artikel_list.artnr == umsatz.artnr and artikel_list.depart == umsatz.departement), first=True)
            if not artikel_list:
                continue

            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:
                artikel_service_code = artikel.service_code
                artikel_mwst_code = artikel.mwst_code


            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel_service_code, artikel_mwst_code))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

            if vat == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal("0")
                nett_tax =  to_decimal(umsatz.betrag)

            elif serv == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal(umsatz.betrag)
                nett_tax =  to_decimal("0")


            else:
                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


            plist.datum = umsatz.datum

            if nett_amt != 0:
                plist.amount =  to_decimal(plist.amount) + to_decimal(nett_amt)


            else:
                plist.amount =  to_decimal(plist.amount) + to_decimal(umsatz.betrag)


    def fill_bqtrevenue():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Banquet / Other FB Revenue"
        plist.flag = 20


        artikel_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "bqtrevenue")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    artikel_list = Artikel_list()
                    artikel_list_data.append(artikel_list)

                    artikel_list.artnr = to_int(entry(0, str1, "|"))
                    artikel_list.depart = to_int(entry(1, str1, "|"))

        umsatz_obj_list = {}
        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= fdate) & (Umsatz.datum <= tdate)).order_by(Umsatz._recid).all():
            artikel_list = query(artikel_list_data, (lambda artikel_list: artikel_list.artnr == umsatz.artnr and artikel_list.depart == umsatz.departement), first=True)
            if not artikel_list:
                continue

            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:
                artikel_service_code = artikel.service_code
                artikel_mwst_code = artikel.mwst_code


            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel_service_code, artikel_mwst_code))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

            if vat == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal("0")
                nett_tax =  to_decimal(umsatz.betrag)

            elif serv == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal(umsatz.betrag)
                nett_tax =  to_decimal("0")


            else:
                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


            plist.datum = umsatz.datum

            if nett_amt != 0:
                plist.amount =  to_decimal(plist.amount) + to_decimal(nett_amt)


            else:
                plist.amount =  to_decimal(plist.amount) + to_decimal(umsatz.betrag)


    def fill_bevrevenue():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Beverage Revenue"
        plist.flag = 19


        artikel_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "beveragerevenue")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    artikel_list = Artikel_list()
                    artikel_list_data.append(artikel_list)

                    artikel_list.artnr = to_int(entry(0, str1, "|"))
                    artikel_list.depart = to_int(entry(1, str1, "|"))

        umsatz_obj_list = {}
        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= fdate) & (Umsatz.datum <= tdate)).order_by(Umsatz._recid).all():
            artikel_list = query(artikel_list_data, (lambda artikel_list: artikel_list.artnr == umsatz.artnr and artikel_list.depart == umsatz.departement), first=True)
            if not artikel_list:
                continue

            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:
                artikel_service_code = artikel.service_code
                artikel_mwst_code = artikel.mwst_code


            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel_service_code, artikel_mwst_code))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

            if vat == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal("0")
                nett_tax =  to_decimal(umsatz.betrag)

            elif serv == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal(umsatz.betrag)
                nett_tax =  to_decimal("0")


            else:
                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


            plist.datum = umsatz.datum

            if nett_amt != 0:
                plist.amount =  to_decimal(plist.amount) + to_decimal(nett_amt)


            else:
                plist.amount =  to_decimal(plist.amount) + to_decimal(umsatz.betrag)


    def fill_foodrevenue():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Food Revenue"
        plist.flag = 18


        artikel_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "foodrevenue")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    artikel_list = Artikel_list()
                    artikel_list_data.append(artikel_list)

                    artikel_list.artnr = to_int(entry(0, str1, "|"))
                    artikel_list.depart = to_int(entry(1, str1, "|"))

        umsatz_obj_list = {}
        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= fdate) & (Umsatz.datum <= tdate)).order_by(Umsatz._recid).all():
            artikel_list = query(artikel_list_data, (lambda artikel_list: artikel_list.artnr == umsatz.artnr and artikel_list.depart == umsatz.departement), first=True)
            if not artikel_list:
                continue

            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:
                artikel_service_code = artikel.service_code
                artikel_mwst_code = artikel.mwst_code


            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel_service_code, artikel_mwst_code))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

            if vat == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal("0")
                nett_tax =  to_decimal(umsatz.betrag)

            elif serv == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal(umsatz.betrag)
                nett_tax =  to_decimal("0")


            else:
                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


            plist.datum = umsatz.datum

            if nett_amt != 0:
                plist.amount =  to_decimal(plist.amount) + to_decimal(nett_amt)


            else:
                plist.amount =  to_decimal(plist.amount) + to_decimal(umsatz.betrag)


    def fill_rmrevenue():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Room Revenue"
        plist.flag = 17


        artikel_list_data.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "roomrevenue")]})

        if queasy:
            for loopi in range(1,num_entries(queasy.char2, ";")  + 1) :
                str1 = entry(loopi - 1, queasy.char2, ";")

                if str1 != "":
                    artikel_list = Artikel_list()
                    artikel_list_data.append(artikel_list)

                    artikel_list.artnr = to_int(entry(0, str1, "|"))
                    artikel_list.depart = to_int(entry(1, str1, "|"))

        umsatz_obj_list = {}
        for umsatz in db_session.query(Umsatz).filter(
                 (Umsatz.datum >= fdate) & (Umsatz.datum <= tdate)).order_by(Umsatz._recid).all():
            artikel_list = query(artikel_list_data, (lambda artikel_list: artikel_list.artnr == umsatz.artnr and artikel_list.depart == umsatz.departement), first=True)
            if not artikel_list:
                continue

            if umsatz_obj_list.get(umsatz._recid):
                continue
            else:
                umsatz_obj_list[umsatz._recid] = True

            artikel = get_cache (Artikel, {"artnr": [(eq, umsatz.artnr)],"departement": [(eq, umsatz.departement)]})

            if artikel:
                artikel_service_code = artikel.service_code
                artikel_mwst_code = artikel.mwst_code


            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel_service_code, artikel_mwst_code))
            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)

            if vat == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal("0")
                nett_tax =  to_decimal(umsatz.betrag)

            elif serv == 1:
                nett_amt =  to_decimal("0")
                nett_serv =  to_decimal(umsatz.betrag)
                nett_tax =  to_decimal("0")


            else:
                nett_amt =  to_decimal(umsatz.betrag) / to_decimal(fact)
                nett_serv =  to_decimal(nett_amt) * to_decimal(serv)
                nett_tax =  to_decimal(nett_amt) * to_decimal(vat)
                nett_amt =  to_decimal(umsatz.betrag) - to_decimal(nett_serv) - to_decimal(nett_tax)


            plist.datum = umsatz.datum

            if nett_amt != 0:
                plist.amount =  to_decimal(plist.amount) + to_decimal(nett_amt)


            else:
                plist.amount =  to_decimal(plist.amount) + to_decimal(umsatz.betrag)


    def fill_arrival():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "# Of Arrivals (Room)"
        plist.flag = 16

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.resstatus != 3) & (Res_line.resstatus != 9) & (Res_line.resstatus != 11) & (Res_line.resstatus != 12) & (Res_line.resstatus != 13) & (Res_line.resstatus != 99) & (Res_line.active_flag <= 1)).order_by(Res_line._recid).all():
            plist.datum = res_line.ankunft
            plist.amount =  to_decimal(plist.amount) + to_decimal(res_line.zimmeranz)


    def fill_cancel():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Cancellation For Today"
        plist.flag = 15

        res_line_obj_list = {}
        for res_line, reservation, guest, zimkateg in db_session.query(Res_line, Reservation, Guest, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.resstatus == 9) & (Res_line.cancelled >= fdate) & (Res_line.cancelled <= tdate) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            plist.datum = res_line.ankunft
            plist.amount =  to_decimal(plist.amount) + to_decimal(res_line.zimmeranz)


    def fill_creatersv():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Reservation Made Today"
        plist.flag = 14

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.resdat >= fdate) & (Reservation.resdat <= tdate)).order_by(Reservation._recid).all():

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == reservation.resnr)).order_by(Res_line._recid).all():
                plist.amount =  to_decimal(plist.amount) + to_decimal("1")


            plist.datum = reservation.resdat


    def fill_noshow():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "No Shows"
        plist.flag = 13

        res_line_obj_list = {}
        for res_line, reservation, guest, zimkateg in db_session.query(Res_line, Reservation, Guest, Zimkateg).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                 (Res_line.resstatus == 10) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(ankunft).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            plist.datum = res_line.ankunft
            plist.amount =  to_decimal(plist.amount) + to_decimal(res_line.zimmeranz)

    def fill_arr():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data

        curr_rmpay:Decimal = to_decimal("0.0")
        curr_revenue:Decimal = to_decimal("0.0")
        Mlist = Plist
        mlist_data = plist_data
        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Average Room Rate"
        plist.flag = 12

        mlist = query(mlist_data, filters=(lambda mlist: mlist.flag == 6), first=True)

        if mlist:
            curr_rmpay =  to_decimal(mlist.amount)

        mlist = query(mlist_data, filters=(lambda mlist: mlist.flag == 17), first=True)

        if mlist:
            curr_revenue =  to_decimal(mlist.amount)


        plist.amount =  to_decimal(curr_revenue) / to_decimal(curr_rmpay)


    def fill_personinhouse():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Person In House"
        plist.flag = 11

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= fdate) & (Genstat.datum <= bill_date - timedelta(days=1)) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():
            plist.datum = genstat.datum
            plist.amount =  to_decimal(plist.amount) + to_decimal((genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis) )


        for res_line in db_session.query(Res_line).filter(
                 (((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > tdate)) & (not_ (Res_line.abreise < bill_date)))) | (((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == bill_date) & (Res_line.abreise == bill_date)) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.abreise == bill_date))) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():
            sdatum = bill_date

            if res_line.ankunft > bill_date:
                sdatum = res_line.ankunft


            sdatum1 = tdate

            if res_line.abreise < sdatum1:
                sdatum1 = res_line.abreise
            for datum2 in date_range(sdatum,sdatum1) :

                if datum2 >= fdate and datum2 <= tdate:
                    plist.datum = datum2
                    plist.amount =  to_decimal(plist.amount) + to_decimal((res_line.erwachs) + to_decimal(res_line.kind1) + to_decimal(res_line.kind2) + to_decimal(res_line.gratis) )

    def fill_occ_perc():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data

        curr_amount:Decimal = to_decimal("0.0")
        curr_amount1:Decimal = to_decimal("0.0")
        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "% Occupancy"
        plist.flag = 9


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "% Occupancy Paying"
        plist.flag = 10

        blist = query(blist_data, filters=(lambda blist: blist.flag == 1), first=True)

        if blist:

            mlist = query(mlist_data, filters=(lambda mlist: mlist.flag == 3 and mlist.datum == blist.datum), first=True)

            if mlist:

                plist = query(plist_data, filters=(lambda plist: plist.flag == 9), first=True)

                if plist:
                    curr_amount = ( to_decimal(((mlist.amount)) / to_decimal(blist.amount)) * to_decimal("100") )

                    if curr_amount == None:
                        curr_amount =  to_decimal("0")


                    plist.datum = mlist.datum
                    plist.amount =  to_decimal(plist.amount) + to_decimal(curr_amount)

            mlist = query(mlist_data, filters=(lambda mlist: mlist.flag == 6 and mlist.datum == blist.datum), first=True)

            if mlist:

                plist = query(plist_data, filters=(lambda plist: plist.flag == 10), first=True)

                if plist:
                    curr_amount1 = ( to_decimal(((mlist.amount)) / to_decimal(blist.amount)) * to_decimal("100") )

                    if curr_amount1 == None:
                        curr_amount1 =  to_decimal("0")


                    plist.datum = mlist.datum
                    plist.amount =  to_decimal(plist.amount) + to_decimal(curr_amount1)


    def fill_rmstat(key_word:string):

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        Blist = Plist
        blist_data = plist_data
        Olist = Plist
        olist_data = plist_data

        if key_word.lower()  == ("ooo").lower() :
            plist = Plist()
            plist_data.append(plist)

            plist.bezeich = "Out Of Order Rooms"
            plist.flag = 7

        elif key_word.lower()  == ("vacant").lower() :
            plist = Plist()
            plist_data.append(plist)

            plist.bezeich = "Vacant Rooms"
            plist.flag = 8

        if key_word.lower()  == ("ooo").lower() :

            for zinrstat in db_session.query(Zinrstat).filter(
                     (Zinrstat.datum >= fdate) & (Zinrstat.datum <= tdate) & (Zinrstat.zinr == (key_word).lower())).order_by(Zinrstat._recid).all():

                plist = query(plist_data, filters=(lambda plist: plist.flag == 7), first=True)

                if plist:
                    plist.datum = zinrstat.datum
                    plist.amount =  to_decimal(plist.amount) + to_decimal(zinrstat.zimmeranz)
                    total_ooo =  to_decimal(plist.amount)

        if key_word.lower()  == ("vacant").lower() :

            for zkstat in db_session.query(Zkstat).filter(
                     (Zkstat.datum >= fdate) & (Zkstat.datum <= tdate)).order_by(Zkstat._recid).all():

                plist = query(plist_data, filters=(lambda plist: plist.flag == 8), first=True)

                if plist:
                    plist.datum = zkstat.datum
                    plist.amount =  to_decimal(plist.amount) + to_decimal(zkstat.anz100)

            blist = query(blist_data, filters=(lambda blist: blist.flag == 3), first=True)

            if blist:

                plist = query(plist_data, filters=(lambda plist: plist.flag == 8), first=True)

                if plist:
                    plist.amount =  to_decimal(plist.amount) - to_decimal(blist.amount) - to_decimal(total_ooo)


    def fill_rm_pay():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Room Paying"
        plist.flag = 6

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.zipreis != 0) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():
            plist.datum = genstat.datum
            plist.amount =  to_decimal(plist.amount) + to_decimal("1")


    def fill_comp_hu():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "House Uses"
        plist.flag = 4


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Complimentary Rooms"
        plist.flag = 5

        for segment in db_session.query(Segment).filter(
                 (Segment.betriebsnr == 1) | (Segment.betriebsnr == 2)).order_by(Segment._recid).all():

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat._recid).all():

                if segment.betriebsnr == 1:

                    plist = query(plist_data, filters=(lambda plist: plist.flag == 5), first=True)

                    if plist:
                        plist.datum = genstat.datum
                        plist.amount =  to_decimal(plist.amount) + to_decimal("1")

                elif segment.betriebsnr == 2:

                    plist = query(plist_data, filters=(lambda plist: plist.flag == 4), first=True)

                    if plist:
                        plist.datum = genstat.datum
                        plist.amount =  to_decimal(plist.amount) + to_decimal("1")


    def fill_rm_occupied():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Room Occupied"
        plist.flag = 3

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():
            plist.datum = genstat.datum
            plist.amount =  to_decimal(plist.amount) + to_decimal("1")


    def fill_tot_avail():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        Blist = Plist
        blist_data = plist_data
        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Room Available"
        plist.flag = 2

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum >= fdate) & (Zkstat.datum <= tdate)).order_by(Zkstat._recid).all():
            plist.datum = zkstat.datum
            plist.amount =  to_decimal(plist.amount) + to_decimal(zkstat.anz100)

        blist = query(blist_data, filters=(lambda blist: blist.flag == 3), first=True)

        if blist:
            plist.amount =  to_decimal(plist.amount) - to_decimal(blist.amount)

        blist = query(blist_data, filters=(lambda blist: blist.flag == 7), first=True)

        if blist:
            plist.amount =  to_decimal(plist.amount) - to_decimal(blist.amount)


    def fill_tot_room():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data


        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Total Room"
        plist.flag = 1


        for datum1 in date_range(fdate,tdate) :

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, datum1)],"zinr": [(eq, "tot-rm")]})

            if zinrstat:
                plist.datum = datum1
                plist.amount =  to_decimal(plist.amount) + to_decimal(zinrstat.zimmeranz)


    def fill_room_sold():

        nonlocal plist_data, mm, yy, datum1, loopi, bill_date, sdatum, sdatum1, datum2, counter, f_endkum, m_endkum, spadept, str1, fdate, tdate, fact, serv, vat, nett_amt, nett_serv, nett_tax, artikel_service_code, artikel_mwst_code, total_ooo, queasy, htparam, hoteldpt, gl_main, gl_acct, gl_jouhdr, gl_journal, l_op, l_artikel, l_lieferant, l_ophis, umsatz, artikel, res_line, reservation, guest, zimkateg, genstat, zinrstat, zkstat, segment
        nonlocal blist, mlist, bqueasy


        nonlocal plist, outlet_list, room_expenses, expenses_list, cost_list, artikel_list, blist, mlist, bqueasy, mlist, blist, olist, blist
        nonlocal plist_data, outlet_list_data, room_expenses_data, expenses_list_data, cost_list_data, artikel_list_data

        room_occupied_amount:Decimal = to_decimal("0.0")
        house_uses_amount:Decimal = to_decimal("0.0")
        complimentary_amount:Decimal = to_decimal("0.0")
        plist = Plist()
        plist_data.append(plist)

        plist.bezeich = "Room Sold"
        plist.flag = 28

        blist = query(blist_data, filters=(lambda blist: blist.flag == 3), first=True)

        if blist:
            room_occupied_amount =  to_decimal(blist.amount)

        mlist = query(mlist_data, filters=(lambda mlist: mlist.flag == 4), first=True)

        if mlist:
            house_uses_amount =  to_decimal(mlist.amount)

        mlist = query(mlist_data, filters=(lambda mlist: mlist.flag == 5), first=True)

        if mlist:
            complimentary_amount =  to_decimal(mlist.amount)


        plist.amount =  to_decimal(room_occupied_amount) - to_decimal((house_uses_amount) + to_decimal(complimentary_amount) )

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate


    fdate = bill_date - timedelta(days=1)
    tdate = bill_date - timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 862)]})
    f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 273)]})
    m_endkum = htparam.finteger

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num != 0)).order_by(Hoteldpt._recid).all():
        outlet_list = Outlet_list()
        outlet_list_data.append(outlet_list)

        outlet_list.deptnr = hoteldpt.num
        outlet_list.departement = hoteldpt.depart

    bqueasy = get_cache (Queasy, {"key": [(eq, 322)],"char1": [(eq, "deptspa")]})

    if bqueasy:
        spadept = to_int(bqueasy.char2)

    gl_acct_obj_list = {}
    gl_acct = Gl_acct()
    gl_main = Gl_main()
    for gl_acct.main_nr, gl_acct.fibukonto, gl_acct.bezeich, gl_acct._recid, gl_main.bezeich, gl_main.nr, gl_main._recid in db_session.query(Gl_acct.main_nr, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct._recid, Gl_main.bezeich, Gl_main.nr, Gl_main._recid).join(Gl_main,(Gl_main.nr == Gl_acct.main_nr)).filter(
             (Gl_acct.acc_type == 5)).order_by(Gl_acct._recid).all():
        if gl_acct_obj_list.get(gl_acct._recid):
            continue
        else:
            gl_acct_obj_list[gl_acct._recid] = True

        room_expenses = query(room_expenses_data, filters=(lambda room_expenses: room_expenses.main_nr == gl_main.nr), first=True)

        if not room_expenses:

            expenses_list = query(expenses_list_data, filters=(lambda expenses_list: expenses_list.main_nr == gl_main.nr), first=True)

            if not expenses_list:
                expenses_list = Expenses_list()
                expenses_list_data.append(expenses_list)

                expenses_list.main_nr = gl_main.nr
                expenses_list.account_name = gl_main.bezeich

    for gl_acct in db_session.query(Gl_acct).filter(
             (Gl_acct.acc_type == 2)).order_by(Gl_acct._recid).all():
        cost_list = Cost_list()
        cost_list_data.append(cost_list)

        cost_list.fibukonto = gl_acct.fibukonto
        cost_list.account_name = gl_acct.bezeich


    fill_tot_room()
    fill_rm_occupied()
    fill_rmstat("ooo")
    fill_rmstat("vacant")
    fill_tot_avail()
    fill_comp_hu()
    fill_rm_pay()
    fill_room_sold()
    fill_occ_perc()
    fill_personinhouse()
    fill_rmrevenue()
    fill_arr()
    fill_noshow()
    fill_creatersv()
    fill_cancel()
    fill_arrival()
    fill_foodrevenue()
    fill_bevrevenue()
    fill_bqtrevenue()
    fill_sparevenue()
    fill_laundryrevenue()
    fill_bcenterrevenue()
    fill_telprevenue()
    fill_otherrevenue()
    fill_foodcost()
    fill_bevcost()

    return generate_output()