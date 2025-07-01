#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit, L_lieferant, L_op, Res_history

def ap_list_mi_chgsuppbl(ap_recid:int, lief_nr:int, bediener_nr:int):

    prepare_cache ([L_kredit, L_lieferant, L_op, Res_history])

    chr1 = ""
    l_kredit = l_lieferant = l_op = res_history = None

    l_ap = supplier = subuff = opbuff = None

    L_ap = create_buffer("L_ap",L_kredit)
    Supplier = create_buffer("Supplier",L_lieferant)
    Subuff = create_buffer("Subuff",L_lieferant)
    Opbuff = create_buffer("Opbuff",L_op)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal chr1, l_kredit, l_lieferant, l_op, res_history
        nonlocal ap_recid, lief_nr, bediener_nr
        nonlocal l_ap, supplier, subuff, opbuff


        nonlocal l_ap, supplier, subuff, opbuff

        return {"chr1": chr1}


    l_kredit = get_cache (L_kredit, {"_recid": [(eq, ap_recid)]})

    subuff = get_cache (L_lieferant, {"lief_nr": [(eq, l_kredit.lief_nr)]})

    supplier = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    for l_op in db_session.query(L_op).filter(
                 (L_op.lief_nr == l_kredit.lief_nr) & (L_op.datum == l_kredit.rgdatum) & (L_op.op_art == 1) & (L_op.docu_nr == l_kredit.name) & (L_op.lscheinnr == l_kredit.lscheinnr)).order_by(L_op._recid).all():

        opbuff = get_cache (L_op, {"_recid": [(eq, l_op._recid)]})
        opbuff.lief_nr = lief_nr


        pass

    for l_op in db_session.query(L_op).filter(
                 (L_op.lief_nr == l_kredit.lief_nr) & (L_op.datum == l_kredit.rgdatum) & (L_op.op_art == 3) & (L_op.docu_nr == l_kredit.name) & (L_op.lscheinnr == l_kredit.lscheinnr)).order_by(L_op._recid).all():

        opbuff = get_cache (L_op, {"_recid": [(eq, l_op._recid)]})
        opbuff.lief_nr = lief_nr


        pass
    pass
    l_kredit.lief_nr = lief_nr


    pass

    if l_kredit.counter != 0:

        for l_ap in db_session.query(L_ap).filter(
                     (L_ap.counter == l_kredit.counter) & (L_ap.opart >= 1) & (L_ap._recid != l_kredit._recid)).order_by(L_ap._recid).all():
            l_ap.lief_nr = lief_nr
        pass

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
    chr1 = to_string(l_lieferant.firma, "x(26)")
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener_nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "P/O " + l_kredit.name +\
            "; DeliveryNote " + l_kredit.lscheinnr +\
            "; Change Supplier " + suBuff.firma +\
            " -> " + supplier.firma


    res_history.action = "A/P"
    pass
    pass

    return generate_output()