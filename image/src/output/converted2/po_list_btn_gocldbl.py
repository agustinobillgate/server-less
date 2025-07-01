#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_order, L_artikel, Htparam, L_lieferant, L_orderhdr, Parameters, Waehrung, Queasy

def po_list_btn_gocldbl(usrname:string, po_number:string, dml_only:bool):

    prepare_cache ([Htparam, L_lieferant, L_orderhdr, Parameters, Waehrung])

    p_267 = False
    q2_list_list = []
    p_71:bool = False
    loop:int = 0
    l_order = l_artikel = htparam = l_lieferant = l_orderhdr = parameters = waehrung = queasy = None

    w_list = cost_list = q2_list = l_order1 = l_order2 = l_art = None

    w_list_list, W_list = create_model("W_list", {"nr":int, "wabkurz":string})
    cost_list_list, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string})
    q2_list_list, Q2_list = create_model("Q2_list", {"bestelldatum":date, "bezeich":string, "firma":string, "docu_nr":string, "l_orderhdr_lieferdatum":date, "wabkurz":string, "bestellart":string, "gedruckt":date, "l_orderhdr_besteller":string, "l_order_gedruckt":date, "zeit":int, "lief_fax_2":string, "l_order_lieferdatum":date, "lief_fax_3":string, "lieferdatum_eff":date, "lief_fax_1":string, "lief_nr":int, "username":string, "del_reason":string, "tot_amount":Decimal})

    L_order1 = create_buffer("L_order1",L_order)
    L_order2 = create_buffer("L_order2",L_order)
    L_art = create_buffer("L_art",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_267, q2_list_list, p_71, loop, l_order, l_artikel, htparam, l_lieferant, l_orderhdr, parameters, waehrung, queasy
        nonlocal usrname, po_number, dml_only
        nonlocal l_order1, l_order2, l_art


        nonlocal w_list, cost_list, q2_list, l_order1, l_order2, l_art
        nonlocal w_list_list, cost_list_list, q2_list_list

        return {"p_267": p_267, "q2-list": q2_list_list}

    def disp_po():

        nonlocal p_267, q2_list_list, p_71, loop, l_order, l_artikel, htparam, l_lieferant, l_orderhdr, parameters, waehrung, queasy
        nonlocal usrname, po_number, dml_only
        nonlocal l_order1, l_order2, l_art


        nonlocal w_list, cost_list, q2_list, l_order1, l_order2, l_art
        nonlocal w_list_list, cost_list_list, q2_list_list

        if usrname == "":

            l_orderhdr_obj_list = {}
            for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                     (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr == (po_number).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                w_list = query(w_list_list, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                if not w_list:
                    continue

                cost_list = query(cost_list_list, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_orderhdr_obj_list.get(l_orderhdr._recid):
                    continue
                else:
                    l_orderhdr_obj_list[l_orderhdr._recid] = True

                if dml_only:

                    if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                        cr_temp_table()
                else:
                    cr_temp_table()


        elif usrname != "":

            l_orderhdr_obj_list = {}
            for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                     (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr == (po_number).lower()) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                w_list = query(w_list_list, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                if not w_list:
                    continue

                cost_list = query(cost_list_list, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_orderhdr_obj_list.get(l_orderhdr._recid):
                    continue
                else:
                    l_orderhdr_obj_list[l_orderhdr._recid] = True

                if dml_only:

                    if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                        cr_temp_table()
                else:
                    cr_temp_table()

    def create_costlist():

        nonlocal p_267, q2_list_list, p_71, loop, l_order, l_artikel, htparam, l_lieferant, l_orderhdr, parameters, waehrung, queasy
        nonlocal usrname, po_number, dml_only
        nonlocal l_order1, l_order2, l_art


        nonlocal w_list, cost_list, q2_list, l_order1, l_order2, l_art
        nonlocal w_list_list, cost_list_list, q2_list_list

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring


    def currency_list():

        nonlocal p_267, q2_list_list, p_71, loop, l_order, l_artikel, htparam, l_lieferant, l_orderhdr, parameters, waehrung, queasy
        nonlocal usrname, po_number, dml_only
        nonlocal l_order1, l_order2, l_art


        nonlocal w_list, cost_list, q2_list, l_order1, l_order2, l_art
        nonlocal w_list_list, cost_list_list, q2_list_list

        local_nr:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            local_nr = waehrung.waehrungsnr
        w_list = W_list()
        w_list_list.append(w_list)


        if local_nr != 0:
            w_list.wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).order_by(Waehrung.wabkurz).all():
            w_list = W_list()
            w_list_list.append(w_list)

            w_list.nr = waehrung.waehrungsnr
            w_list.wabkurz = waehrung.wabkurz


    def cr_temp_table():

        nonlocal p_267, q2_list_list, p_71, loop, l_order, l_artikel, htparam, l_lieferant, l_orderhdr, parameters, waehrung, queasy
        nonlocal usrname, po_number, dml_only
        nonlocal l_order1, l_order2, l_art


        nonlocal w_list, cost_list, q2_list, l_order1, l_order2, l_art
        nonlocal w_list_list, cost_list_list, q2_list_list

        t_amount:Decimal = to_decimal("0.0")
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

        if p_71:

            queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})
            while None != queasy:

                if q2_list.username != "":

                    if num_entries(q2_list.username, ";") < 4:
                        q2_list.username = q2_list.username + entry(0, queasy.char3, "|") + ";"
                    else:
                        q2_list.username = q2_list.username + entry(0, queasy.char3, "|")
                else:
                    q2_list.username = entry(0, queasy.char3, "|") + ";"

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 245) & (Queasy.char1 == l_orderhdr.docu_nr) & (Queasy._recid > curr_recid)).first()
            for loop in range(1,4 + 1) :

                if num_entries(q2_list.username, ";") != 4:
                    q2_list.username = q2_list.username + ";"
        else:

            queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

            if queasy:
                q2_list.username = queasy.char3
            else:
                q2_list.username = ""

        l_order2 = db_session.query(L_order2).filter(
                 (L_order2.docu_nr == l_orderhdr.docu_nr) & (L_order2.pos > 0) & (L_order2.loeschflag == 0)).first()
        while None != l_order2:

            l_art = db_session.query(L_art).filter(
                     (L_art.artnr == l_order2.artnr)).first()

            if l_art:
                t_amount =  to_decimal(t_amount) + to_decimal(l_order2.warenwert)

            curr_recid = l_order2._recid
            l_order2 = db_session.query(L_order2).filter(
                     (L_order2.docu_nr == l_orderhdr.docu_nr) & (L_order2.pos > 0) & (L_order2.loeschflag == 0) & (L_order2._recid > curr_recid)).first()
        q2_list.tot_amount =  to_decimal(t_amount)

    create_costlist()
    currency_list()
    disp_po()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 267)]})
    p_267 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 71)]})

    if htparam.paramgruppe == 21:
        p_71 = htparam.flogical

    return generate_output()