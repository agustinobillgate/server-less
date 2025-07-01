#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, Htparam, L_orderhdr, Parameters, L_order

def prepare_ins_prbl(docu_nr:string):

    prepare_cache ([L_artikel, Htparam, Parameters, L_order])

    billdate = None
    comments = ""
    deptname = ""
    pos = 0
    t_l_orderhdr_list = []
    ins_list_list = []
    l_artikel = htparam = l_orderhdr = parameters = l_order = None

    s_list = t_l_orderhdr = ins_list = l_art = None

    s_list_list, S_list = create_model("S_list", {"pos":int, "artnr":int, "new_created":bool, "bemerk":string})
    t_l_orderhdr_list, T_l_orderhdr = create_model("T_l_orderhdr", {"docu_nr":string, "besteller":string, "angebot_lief":[int,3], "bestelldatum":date, "lieferdatum":date})
    ins_list_list, Ins_list = create_model("Ins_list", {"t_recid":int, "artnr":int, "bezeich":string, "anzahl":Decimal, "traubensort":string, "txtnr":int, "lieferdatum":date, "stornogrund":string, "bemerk":string, "quality":string, "jahrgang":int, "new_created":bool, "lief_nr":int, "op_art":int, "docu_nr":string, "bestelldatum":date})

    L_art = create_buffer("L_art",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, comments, deptname, pos, t_l_orderhdr_list, ins_list_list, l_artikel, htparam, l_orderhdr, parameters, l_order
        nonlocal docu_nr
        nonlocal l_art


        nonlocal s_list, t_l_orderhdr, ins_list, l_art
        nonlocal s_list_list, t_l_orderhdr_list, ins_list_list

        return {"billdate": billdate, "comments": comments, "deptname": deptname, "pos": pos, "t-l-orderhdr": t_l_orderhdr_list, "ins-list": ins_list_list}

    def create_list():

        nonlocal billdate, comments, deptname, pos, t_l_orderhdr_list, ins_list_list, l_artikel, htparam, l_orderhdr, parameters, l_order
        nonlocal docu_nr
        nonlocal l_art


        nonlocal s_list, t_l_orderhdr, ins_list, l_art
        nonlocal s_list_list, t_l_orderhdr_list, ins_list_list

        for l_order in db_session.query(L_order).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag <= 1)).order_by(L_order.pos).all():
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.artnr = l_order.artnr
            s_list.pos = l_order.pos
            s_list.bemerk = l_order.besteller
            pos = l_order.pos


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})

    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

    if parameters:
        deptname = parameters.vstring

    if l_orderhdr:
        comments = l_orderhdr.lief_fax[2]
        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_list.append(t_l_orderhdr)

        buffer_copy(l_orderhdr, t_l_orderhdr)
    create_list()

    l_order_obj_list = {}
    for l_order, l_art in db_session.query(L_order, L_art).join(L_art,(L_art.artnr == L_order.artnr)).filter(
             (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag <= 1)).order_by(s_list.pos.desc()).all():
        s_list = query(s_list_list, (lambda s_list: s_list.artnr == l_order.artnr), first=True)
        if not s_list:
            continue

        if l_order_obj_list.get(l_order._recid):
            continue
        else:
            l_order_obj_list[l_order._recid] = True


        ins_list = Ins_list()
        ins_list_list.append(ins_list)

        ins_list.t_recid = l_order._recid
        ins_list.artnr = l_order.artnr
        ins_list.bezeich = l_art.bezeich
        ins_list.anzahl =  to_decimal(l_order.anzahl)
        ins_list.traubensort = l_art.traubensorte
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

    return generate_output()