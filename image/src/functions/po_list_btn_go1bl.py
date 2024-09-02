from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_order, Htparam, L_lieferant, L_orderhdr, Parameters, Waehrung

def po_list_btn_go1bl(usrname:str, po_number:str):
    p_267 = False
    q2_list_list = []
    l_order = htparam = l_lieferant = l_orderhdr = parameters = waehrung = None

    q2_list = w_list = cost_list = l_order1 = None

    q2_list_list, Q2_list = create_model("Q2_list", {"bestelldatum":date, "bezeich":str, "firma":str, "docu_nr":str, "l_orderhdr_lieferdatum":date, "wabkurz":str, "bestellart":str, "gedruckt":date, "l_orderhdr_besteller":str, "l_order_gedruckt":date, "zeit":int, "lief_fax_2":str, "l_order_lieferdatum":date, "lief_fax_3":str, "lieferdatum_eff":date, "lief_fax_1":str, "lief_nr":int})
    w_list_list, W_list = create_model("W_list", {"nr":int, "wabkurz":str})
    cost_list_list, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":str})

    L_order1 = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_267, q2_list_list, l_order, htparam, l_lieferant, l_orderhdr, parameters, waehrung
        nonlocal l_order1


        nonlocal q2_list, w_list, cost_list, l_order1
        nonlocal q2_list_list, w_list_list, cost_list_list
        return {"p_267": p_267, "q2-list": q2_list_list}

    def disp_po():

        nonlocal p_267, q2_list_list, l_order, htparam, l_lieferant, l_orderhdr, parameters, waehrung
        nonlocal l_order1


        nonlocal q2_list, w_list, cost_list, l_order1
        nonlocal q2_list_list, w_list_list, cost_list_list

        if usrname == "":

            l_orderhdr_obj_list = []
            for l_orderhdr, w_list, cost_list, l_lieferant, l_order1 in db_session.query(L_orderhdr, W_list, Cost_list, L_lieferant, L_order1).join(W_list,(W_list.nr == L_orderhdr.angebot_lief[2])).join(Cost_list,(Cost_list.nr == L_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                    (L_orderhdr.betriebsnr <= 1) &  (func.lower(L_orderhdr.docu_nr) == (po_number).lower())).all():
                if l_orderhdr._recid in l_orderhdr_obj_list:
                    continue
                else:
                    l_orderhdr_obj_list.append(l_orderhdr._recid)


                cr_temp_table()


        elif usrname != "":

            l_orderhdr_obj_list = []
            for l_orderhdr, w_list, cost_list, l_lieferant, l_order1 in db_session.query(L_orderhdr, W_list, Cost_list, L_lieferant, L_order1).join(W_list,(W_list.nr == L_orderhdr.angebot_lief[2])).join(Cost_list,(Cost_list.nr == L_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                    (L_orderhdr.betriebsnr <= 1) &  (func.lower(L_orderhdr.docu_nr) == (po_number).lower()) &  (L_orderhdr.besteller == usrname)).all():
                if l_orderhdr._recid in l_orderhdr_obj_list:
                    continue
                else:
                    l_orderhdr_obj_list.append(l_orderhdr._recid)


                cr_temp_table()


    def create_costlist():

        nonlocal p_267, q2_list_list, l_order, htparam, l_lieferant, l_orderhdr, parameters, waehrung
        nonlocal l_order1


        nonlocal q2_list, w_list, cost_list, l_order1
        nonlocal q2_list_list, w_list_list, cost_list_list

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (Parameters.varname > "")).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring

    def currency_list():

        nonlocal p_267, q2_list_list, l_order, htparam, l_lieferant, l_orderhdr, parameters, waehrung
        nonlocal l_order1


        nonlocal q2_list, w_list, cost_list, l_order1
        nonlocal q2_list_list, w_list_list, cost_list_list

        local_nr:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 152)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            local_nr = waehrungsnr
        w_list = W_list()
        w_list_list.append(w_list)


        if local_nr != 0:
            w_list.wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).all():
            w_list = W_list()
            w_list_list.append(w_list)

            w_list.nr = waehrungsnr
            w_list.wabkurz = waehrung.wabkurz

    def cr_temp_table():

        nonlocal p_267, q2_list_list, l_order, htparam, l_lieferant, l_orderhdr, parameters, waehrung
        nonlocal l_order1


        nonlocal q2_list, w_list, cost_list, l_order1
        nonlocal q2_list_list, w_list_list, cost_list_list


        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        q2_list.bestelldatum = l_orderhdr.bestelldatum
        q2_list.bezeich = cost_list.bezeich
        q2_list.firma = l_lieferant.firma
        q2_list.docu_nr = l_orderhdr.docu_nr
        q2_list.l_orderhdr_lieferdatum = l_orderhdr.lieferdatum
        q2_list.wabkurz = w_list.wabkurz
        q2_list.bestellart = l_orderhdr.bestellart
        q2_list.gedruckt = l_orderhdr.gedruckt
        q2_list.l_orderhdr_besteller = l_orderhdr.besteller
        q2_list.l_order_gedruckt = l_order1.gedruckt
        q2_list.zeit = l_order1.zeit
        q2_list.lief_fax_2 = l_order1.lief_fax[1]
        q2_list.l_order_lieferdatum = l_order1.lieferdatum
        q2_list.lief_fax_3 = l_order1.lief_fax[2]
        q2_list.lieferdatum_eff = l_order1.lieferdatum_eff
        q2_list.lief_fax_1 = l_order1.lief_fax[0]
        q2_list.lief_nr = l_order1.lief_nr


    create_costlist()
    currency_list()
    disp_po()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 267)).first()
    p_267 = htparam.flogical

    return generate_output()