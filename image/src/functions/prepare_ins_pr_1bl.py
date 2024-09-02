from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, Htparam, L_orderhdr, Parameters, L_order, L_bestand

def prepare_ins_pr_1bl(docu_nr:str):
    billdate = None
    comments = ""
    deptname = ""
    pos = 0
    t_l_orderhdr_list = []
    ins_list_list = []
    l_artikel = htparam = l_orderhdr = parameters = l_order = l_bestand = None

    s_list = t_l_orderhdr = ins_list = l_art = None

    s_list_list, S_list = create_model("S_list", {"pos":int, "artnr":int, "new_created":bool, "bemerk":str})
    t_l_orderhdr_list, T_l_orderhdr = create_model("T_l_orderhdr", {"docu_nr":str, "besteller":str, "angebot_lief":[int], "bestelldatum":date, "lieferdatum":date})
    ins_list_list, Ins_list = create_model("Ins_list", {"t_recid":int, "artnr":int, "bezeich":str, "anzahl":decimal, "traubensort":str, "txtnr":int, "lieferdatum":date, "stornogrund":str, "bemerk":str, "quality":str, "jahrgang":int, "new_created":bool, "lief_nr":int, "op_art":int, "docu_nr":str, "bestelldatum":date, "soh":decimal})

    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, comments, deptname, pos, t_l_orderhdr_list, ins_list_list, l_artikel, htparam, l_orderhdr, parameters, l_order, l_bestand
        nonlocal l_art


        nonlocal s_list, t_l_orderhdr, ins_list, l_art
        nonlocal s_list_list, t_l_orderhdr_list, ins_list_list
        return {"billdate": billdate, "comments": comments, "deptname": deptname, "pos": pos, "t-l-orderhdr": t_l_orderhdr_list, "ins-list": ins_list_list}

    def create_list():

        nonlocal billdate, comments, deptname, pos, t_l_orderhdr_list, ins_list_list, l_artikel, htparam, l_orderhdr, parameters, l_order, l_bestand
        nonlocal l_art


        nonlocal s_list, t_l_orderhdr, ins_list, l_art
        nonlocal s_list_list, t_l_orderhdr_list, ins_list_list

        for l_order in db_session.query(L_order).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.lief_nr == 0) &  (L_order.loeschflag <= 1)).all():
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.artnr = l_order.artnr
            s_list.pos = l_order.pos
            s_list.bemerk = l_order.besteller
            pos = l_order.pos

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()

    parameters = db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

    if parameters:
        deptname = parameters.vstring

    if l_orderhdr:
        comments = l_orderhdr.lief_fax[2]
        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_list.append(t_l_orderhdr)

        buffer_copy(l_orderhdr, t_l_orderhdr)
    create_list()

    l_order_obj_list = []
    for l_order, l_art, s_list in db_session.query(L_order, L_art, S_list).join(L_art,(L_art.artnr == L_order.artnr)).join(S_list,(S_list.artnr == L_order.artnr)).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.lief_nr == 0) &  (L_order.loeschflag <= 1)).all():
        if l_order._recid in l_order_obj_list:
            continue
        else:
            l_order_obj_list.append(l_order._recid)


        ins_list = Ins_list()
        ins_list_list.append(ins_list)

        ins_list.t_recid = l_order._recid
        ins_list.artnr = l_order.artnr
        ins_list.bezeich = l_art.bezeich
        ins_list.anzahl = l_order.anzahl
        ins_list.traubensort = l_art.traubensort
        ins_list.txtnr = l_order.txtnr
        ins_list.lieferdatum = l_order.lieferdatum
        ins_list.stornogrund = l_order.stornogrund
        ins_list.bemerk = s_list.bemerk
        ins_list.quality = l_order.quality
        ins_list.jahrgang = l_art.jahrgang
        ins_list.new_created = s_list.new_created
        ins_list.lief_nr = l_order.lief_nr
        ins_list.op_art = l_order.op_art
        ins_list.docu_nr = l_order.docu_nr
        ins_list.bestelldatum = l_order.bestelldatum

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == l_art.artnr) &  (L_bestand.lager_nr == 0)).first()

        if l_bestand:
            ins_list.soh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

    return generate_output()