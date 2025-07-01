#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_artikel, L_untergrup, L_ophis, Gl_jouhdr, Gl_journal

coa_list_list, Coa_list = create_model("Coa_list", {"fibukonto":string, "datum":date, "wert":Decimal, "debit":Decimal, "credit":Decimal})

def inv_checking_create_list2_cldbl(coa_list_list:[Coa_list], invtype:int, d1:date, d2:date):

    prepare_cache ([L_op, L_artikel, L_untergrup, L_ophis, Gl_jouhdr, Gl_journal])

    frnr = 0
    tonr = 0
    saldo = to_decimal("0.0")
    coa_list2_list = []
    art_list3_list = []
    d:date = None
    mon:int = 0
    art1:int = 0
    art2:int = 0
    fibu:string = ""
    l_op = l_artikel = l_untergrup = l_ophis = gl_jouhdr = gl_journal = None

    coa_list2 = coa_list = art_list3 = None

    coa_list2_list, Coa_list2 = create_model("Coa_list2", {"datum1":date, "wert1":Decimal, "fibu1":string, "debitcredit":Decimal, "diff":Decimal})
    art_list3_list, Art_list3 = create_model("Art_list3", {"datum":date, "artnr":int, "artname":string, "saldo1":Decimal, "saldo2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal frnr, tonr, saldo, coa_list2_list, art_list3_list, d, mon, art1, art2, fibu, l_op, l_artikel, l_untergrup, l_ophis, gl_jouhdr, gl_journal
        nonlocal invtype, d1, d2


        nonlocal coa_list2, coa_list, art_list3
        nonlocal coa_list2_list, art_list3_list

        return {"frnr": frnr, "tonr": tonr, "saldo": saldo, "coa-list2": coa_list2_list, "art-list3": art_list3_list}

    def create_list2():

        nonlocal frnr, tonr, saldo, coa_list2_list, art_list3_list, d, mon, art1, art2, fibu, l_op, l_artikel, l_untergrup, l_ophis, gl_jouhdr, gl_journal
        nonlocal invtype, d1, d2


        nonlocal coa_list2, coa_list, art_list3
        nonlocal coa_list2_list, art_list3_list


        coa_list2_list.clear()

        if invtype == 0:

            return
        mon = get_month(d1) - 1

        if invtype == 1:
            art1 = 3
            art2 = 5
            frnr = 1000000
            tonr = 1999999

        elif invtype == 2:
            art1 = 6
            art2 = 6
            frnr = 2000000
            tonr = 2999999

        if invtype == 3:
            frnr = 3000000
            tonr = 9999999

        l_op = get_cache (L_op, {"datum": [(ge, d1),(le, d2)]})

        if l_op:
            for d in date_range(d1,d2) :

                for l_op in db_session.query(L_op).filter(
                         (L_op.artnr >= frnr) & (L_op.artnr <= tonr) & (L_op.datum == d) & (L_op.op_art == 1) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                    if l_untergrup.fibukonto != "":
                        fibu = l_untergrup.fibukonto
                    else:
                        fibu = l_artikel.fibukonto

                    coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.fibukonto.lower()  == (fibu).lower()  and coa_list.datum == d), first=True)

                    if not coa_list:
                        coa_list = Coa_list()
                        coa_list_list.append(coa_list)

                        coa_list.fibukonto = fibu
                        coa_list.datum = d


                    coa_list.wert =  to_decimal(coa_list.wert) + to_decimal(l_op.warenwert)


                    art_list3 = Art_list3()
                    art_list3_list.append(art_list3)

                    art_list3.datum = d
                    art_list3.artnr = l_op.artnr
                    art_list3.artname = l_artikel.bezeich
                    art_list3.saldo1 =  to_decimal(l_op.warenwert)


        else:
            for d in date_range(d1,d2) :

                for l_ophis in db_session.query(L_ophis).filter(
                         (L_ophis.artnr >= frnr) & (L_ophis.artnr <= tonr) & (L_ophis.datum == d) & (L_ophis.op_art == 1)).order_by(L_ophis._recid).all():

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_ophis.artnr)]})

                    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                    if l_untergrup.fibukonto != "":
                        fibu = l_untergrup.fibukonto
                    else:
                        fibu = l_artikel.fibukonto

                    coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.fibukonto.lower()  == (fibu).lower()  and coa_list.datum == d), first=True)

                    if not coa_list:
                        coa_list = Coa_list()
                        coa_list_list.append(coa_list)

                        coa_list.fibukonto = fibu
                        coa_list.datum = d


                    coa_list.wert =  to_decimal(coa_list.wert) + to_decimal(l_ophis.warenwert)


                    art_list3 = Art_list3()
                    art_list3_list.append(art_list3)

                    art_list3.datum = d
                    art_list3.artnr = l_ophis.artnr
                    art_list3.artname = l_artikel.bezeich
                    art_list3.saldo1 =  to_decimal(l_ophis.warenwert)

        for coa_list in query(coa_list_list):

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.datum == coa_list.datum) & (Gl_jouhdr.jtyp == 6)).order_by(Gl_jouhdr._recid).all():

                for gl_journal in db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr) & (Gl_journal.fibukonto == coa_list.fibukonto)).order_by(Gl_journal._recid).all():
                    coa_list.debit =  to_decimal(coa_list.debit) + to_decimal(gl_journal.debit)
                    coa_list.credit =  to_decimal(coa_list.credit) + to_decimal(gl_journal.credit)

                art_list3 = query(art_list3_list, filters=(lambda art_list3: art_list3.datum == coa_list.datum), first=True)

                if art_list3:
                    art_list3.saldo2 =  to_decimal(coa_list.debit) - to_decimal(coa_list.credit)

        for coa_list in query(coa_list_list, sort_by=[("datum",False)]):
            coa_list2 = Coa_list2()
            coa_list2_list.append(coa_list2)

            coa_list2.datum1 = coa_list.datum
            coa_list2.wert1 =  to_decimal(coa_list.wert)
            coa_list2.fibu1 = coa_list.fibukonto
            coa_list2.debitcredit =  to_decimal(coa_list.debit) - to_decimal(coa_list.credit)
            coa_list2.diff =  to_decimal(coa_list.wert) - to_decimal(coa_list.debit) + to_decimal(coa_list.credit)

    create_list2()

    for coa_list2 in query(coa_list2_list, sort_by=[("datum",False)]):

        if coa_list2.diff == 0:
            coa_list2_list.remove(coa_list2)

    return generate_output()