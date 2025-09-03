#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd 3/9/2025, 
# asumsi data blm sama, tidak lolos filter po_no, devnote_no
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Mathis, Fa_op

def fa_incomingbl(fromdate:date, todate:date, searchby:int, devnote_no:string, po_no:string, supp_no:int):

    prepare_cache ([L_lieferant, Mathis, Fa_op])

    q2_list_data = []
    l_lieferant = mathis = fa_op = None

    q2_list = None

    q2_list_data, Q2_list = create_model("Q2_list", {"lscheinnr":string, "name":string, "location":string, "einzelpreis":Decimal, "anzahl":int, "warenwert":Decimal, "firma":string, "datum":date, "docu_nr":string, "lief_nr":int, "rec_id":int})

    db_session = local_storage.db_session
    # Rd, 3/9/20225
    po_no = po_no.strip()
    devnote_no = devnote_no.strip()
    
    def generate_output():
        nonlocal q2_list_data, l_lieferant, mathis, fa_op
        nonlocal fromdate, todate, searchby, devnote_no, po_no, supp_no


        nonlocal q2_list
        nonlocal q2_list_data

        return {"q2-list": q2_list_data}

    def create_q2_list():

        nonlocal q2_list_data, l_lieferant, mathis, fa_op
        nonlocal fromdate, todate, searchby, devnote_no, po_no, supp_no


        nonlocal q2_list
        nonlocal q2_list_data


        q2_list = Q2_list()
        q2_list_data.append(q2_list)

        q2_list.lscheinnr = fa_op.lscheinnr
        q2_list.name = mathis.name
        q2_list.location = mathis.location
        q2_list.einzelpreis =  to_decimal(fa_op.einzelpreis)
        q2_list.anzahl = fa_op.anzahl
        q2_list.warenwert =  to_decimal(fa_op.warenwert)
        q2_list.firma = l_lieferant.firma
        q2_list.datum = fa_op.datum
        q2_list.docu_nr = fa_op.docu_nr
        q2_list.lief_nr = fa_op.lief_nr
        q2_list.rec_id = fa_op._recid


    if (devnote_no == "" and po_no == "" and supp_no == 0) or searchby == None or (searchby == 1 and devnote_no == "") or (searchby == 2 and po_no == "") or (searchby == 3 and supp_no == 0):

        fa_op_obj_list = {}
        fa_op = Fa_op()
        l_lieferant = L_lieferant()
        mathis = Mathis()
        for fa_op.lscheinnr, fa_op.einzelpreis, fa_op.anzahl, fa_op.warenwert, fa_op.datum, fa_op.docu_nr, fa_op.lief_nr, fa_op._recid, l_lieferant.firma, l_lieferant._recid, mathis.name, mathis.location, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.einzelpreis, Fa_op.anzahl, Fa_op.warenwert, Fa_op.datum, Fa_op.docu_nr, Fa_op.lief_nr, Fa_op._recid, L_lieferant.firma, L_lieferant._recid, Mathis.name, Mathis.location, Mathis._recid).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_op.opart == 1) & (Fa_op.datum >= fromdate) & (Fa_op.datum <= todate) & (Fa_op.loeschflag <= 1)).order_by(Fa_op.datum, Fa_op.docu_nr).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True


            create_q2_list()


    elif searchby == 1 and devnote_no != "":

        fa_op_obj_list = {}
        fa_op = Fa_op()
        l_lieferant = L_lieferant()
        mathis = Mathis()
        for fa_op.lscheinnr, fa_op.einzelpreis, fa_op.anzahl, fa_op.warenwert, fa_op.datum, fa_op.docu_nr, fa_op.lief_nr, fa_op._recid, l_lieferant.firma, l_lieferant._recid, mathis.name, mathis.location, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.einzelpreis, Fa_op.anzahl, Fa_op.warenwert, Fa_op.datum, Fa_op.docu_nr, Fa_op.lief_nr, Fa_op._recid, L_lieferant.firma, L_lieferant._recid, Mathis.name, Mathis.location, Mathis._recid).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_op.opart == 1) & (Fa_op.datum >= fromdate) & (Fa_op.datum <= todate) & (Fa_op.loeschflag <= 1) & (Fa_op.lscheinnr == (devnote_no).lower())).order_by(Fa_op.datum, Fa_op.docu_nr).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True


            create_q2_list()


    elif searchby == 2 and po_no != "":

        fa_op_obj_list = {}
        fa_op = Fa_op()
        l_lieferant = L_lieferant()
        mathis = Mathis()
        for fa_op.lscheinnr, fa_op.einzelpreis, fa_op.anzahl, fa_op.warenwert, fa_op.datum, fa_op.docu_nr, fa_op.lief_nr, fa_op._recid, l_lieferant.firma, l_lieferant._recid, mathis.name, mathis.location, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.einzelpreis, Fa_op.anzahl, Fa_op.warenwert, Fa_op.datum, Fa_op.docu_nr, Fa_op.lief_nr, Fa_op._recid, L_lieferant.firma, L_lieferant._recid, Mathis.name, Mathis.location, Mathis._recid).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_op.opart == 1) & (Fa_op.datum >= fromdate) & (Fa_op.datum <= todate) & (Fa_op.loeschflag <= 1) & (Fa_op.docu_nr == (po_no).lower())).order_by(Fa_op.datum, Fa_op.docu_nr).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True


            create_q2_list()


    elif searchby == 3 and supp_no != 0:

        fa_op_obj_list = {}
        fa_op = Fa_op()
        l_lieferant = L_lieferant()
        mathis = Mathis()
        for fa_op.lscheinnr, fa_op.einzelpreis, fa_op.anzahl, fa_op.warenwert, fa_op.datum, fa_op.docu_nr, fa_op.lief_nr, fa_op._recid, l_lieferant.firma, l_lieferant._recid, mathis.name, mathis.location, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.einzelpreis, Fa_op.anzahl, Fa_op.warenwert, Fa_op.datum, Fa_op.docu_nr, Fa_op.lief_nr, Fa_op._recid, L_lieferant.firma, L_lieferant._recid, Mathis.name, Mathis.location, Mathis._recid).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_op.opart == 1) & (Fa_op.datum >= fromdate) & (Fa_op.datum <= todate) & (Fa_op.loeschflag <= 1) & (Fa_op.lief_nr == supp_no)).order_by(Fa_op.datum, Fa_op.docu_nr).all():
            if fa_op_obj_list.get(fa_op._recid):
                continue
            else:
                fa_op_obj_list[fa_op._recid] = True


            create_q2_list()


    return generate_output()