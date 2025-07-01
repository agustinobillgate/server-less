#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_artikel, L_untergrup, L_ophis, Gl_jouhdr, Gl_journal

def inv_checking_out_glbl(invtype:int, d1:date, d2:date):

    prepare_cache ([L_op, L_artikel, L_untergrup, L_ophis, Gl_jouhdr, Gl_journal])

    frnr = 0
    tonr = 0
    saldo = to_decimal("0.0")
    coa_list3_list = []
    art_list4_list = []
    d:date = None
    mon:int = 0
    art1:int = 0
    art2:int = 0
    fibu:string = ""
    l_op = l_artikel = l_untergrup = l_ophis = gl_jouhdr = gl_journal = None

    coa_list = coa_list3 = art_list4 = None

    coa_list_list, Coa_list = create_model("Coa_list", {"fibukonto":string, "datum":date, "wert":Decimal, "debit":Decimal, "credit":Decimal})
    coa_list3_list, Coa_list3 = create_model("Coa_list3", {"datum2":date, "wert2":Decimal, "fibu2":string, "creditdebit":Decimal, "diff":Decimal})
    art_list4_list, Art_list4 = create_model("Art_list4", {"datum":date, "artnr":int, "artname":string, "saldo1":Decimal, "saldo2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal frnr, tonr, saldo, coa_list3_list, art_list4_list, d, mon, art1, art2, fibu, l_op, l_artikel, l_untergrup, l_ophis, gl_jouhdr, gl_journal
        nonlocal invtype, d1, d2


        nonlocal coa_list, coa_list3, art_list4
        nonlocal coa_list_list, coa_list3_list, art_list4_list

        return {"frnr": frnr, "tonr": tonr, "saldo": saldo, "coa-list3": coa_list3_list, "art-list4": art_list4_list}

    def out_gl():

        nonlocal frnr, tonr, saldo, coa_list3_list, art_list4_list, d, mon, art1, art2, fibu, l_op, l_artikel, l_untergrup, l_ophis, gl_jouhdr, gl_journal
        nonlocal invtype, d1, d2


        nonlocal coa_list, coa_list3, art_list4
        nonlocal coa_list_list, coa_list3_list, art_list4_list


        coa_list_list.clear()
        coa_list3_list.clear()

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


        for d in date_range(d1,d2) :

            for l_op in db_session.query(L_op).filter(
                     (L_op.artnr >= frnr) & (L_op.artnr <= tonr) & (L_op.datum == d) & (L_op.op_art == 3) & (substring(L_op.stornogrund, 0, 8) != ("00000000").lower()) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

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


                art_list4 = Art_list4()
                art_list4_list.append(art_list4)

                art_list4.datum = d
                art_list4.artnr = l_op.artnr
                art_list4.artname = l_artikel.bezeich
                art_list4.saldo1 =  to_decimal(l_op.warenwert)

            l_ophis = get_cache (L_ophis, {"artnr": [(ge, frnr),(le, tonr)],"datum": [(eq, d)],"op_art": [(eq, 3)]})

            if l_ophis:

                for l_ophis in db_session.query(L_ophis).filter(
                         (L_ophis.artnr >= frnr) & (L_ophis.artnr <= tonr) & (L_ophis.datum == d) & (substring(L_ophis.fibukonto, 0, 8) != ("00000000").lower()) & (L_ophis.op_art == 3)).order_by(L_ophis._recid).all():

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


                    art_list4 = Art_list4()
                    art_list4_list.append(art_list4)

                    art_list4.datum = d
                    art_list4.artnr = l_ophis.artnr
                    art_list4.artname = l_artikel.bezeich
                    art_list4.saldo1 =  to_decimal(l_ophis.warenwert)


        for coa_list in query(coa_list_list):

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.datum == coa_list.datum) & (Gl_jouhdr.jtyp == 3) & (substring(Gl_jouhdr.refNo, 0, length(refNo)) == refNo)).order_by(Gl_jouhdr._recid).all():

                for gl_journal in db_session.query(Gl_journal).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr) & (Gl_journal.fibukonto == coa_list.fibukonto) & (substring(Gl_journal.bemer, 0, 1) != ("*").lower())).order_by(Gl_journal._recid).all():
                    coa_list.debit =  to_decimal(coa_list.debit) + to_decimal(gl_journal.debit)
                    coa_list.credit =  to_decimal(coa_list.credit) + to_decimal(gl_journal.credit)

                art_list4 = query(art_list4_list, filters=(lambda art_list4: art_list4.datum == coa_list.datum), first=True)

                if art_list4:
                    art_list4.saldo2 =  to_decimal(coa_list.debit) - to_decimal(coa_list.credit)

        for coa_list in query(coa_list_list, sort_by=[("datum",False)]):
            coa_list3 = Coa_list3()
            coa_list3_list.append(coa_list3)

            coa_list3.datum2 = coa_list.datum
            coa_list3.wert2 =  to_decimal(coa_list.wert)
            coa_list3.fibu = coa_list.fibukonto
            coa_list3.creditdebit =  to_decimal(coa_list.credit) - to_decimal(coa_list.debit)
            coa_list3.diff =  to_decimal(coa_list.wert) - to_decimal(coa_list.credit) + to_decimal(coa_list.debit)

    out_gl()

    for coa_list3 in query(coa_list3_list, sort_by=[("datum",False)]):

        if coa_list3.diff == 0:
            coa_list3_list.remove(coa_list3)

    return generate_output()