#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, L_lieferant, L_artikel, Queasy, Htparam, L_orderhdr, Parameters, Waehrung

def po_list_btn_go2cldbl(t_liefno:int, last_docu_nr:string, sorttype:int, deptnr:int, all_supp:bool, stattype:int, usrname:string, from_date:date, to_date:date, billdate:date, dml_only:bool, app_sort:string):

    prepare_cache ([L_lieferant, Htparam, L_orderhdr, Parameters, Waehrung])

    first_docu_nr = ""
    curr_docu_nr = ""
    p_267 = False
    last_docu_nr1 = ""
    q2_list_data = []
    counter:int = 0
    curr_counter:int = 0
    last_to_sort:int = 0
    temp_docu_nr:string = ""
    temp_counter_nr:int = 0
    approval:int = 0
    p_71:bool = False
    loop:int = 0
    app_lvl:int = 0
    l_order = l_lieferant = l_artikel = queasy = htparam = l_orderhdr = parameters = waehrung = None

    w_list = cost_list = l_order1 = l_supp = l_order2 = l_art = q2_list = q_list = q245 = None

    w_list_data, W_list = create_model("W_list", {"nr":int, "wabkurz":string})
    cost_list_data, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string})
    q2_list_data, Q2_list = create_model("Q2_list", {"bestelldatum":date, "bezeich":string, "firma":string, "docu_nr":string, "l_orderhdr_lieferdatum":date, "wabkurz":string, "bestellart":string, "gedruckt":date, "l_orderhdr_besteller":string, "l_order_gedruckt":date, "zeit":int, "lief_fax_2":string, "l_order_lieferdatum":date, "lief_fax_3":string, "lieferdatum_eff":date, "lief_fax_1":string, "lief_nr":int, "username":string, "del_reason":string, "tot_amount":Decimal})
    q_list_data, Q_list = create_model_like(Q2_list, {"to_sort":int})

    L_order1 = create_buffer("L_order1",L_order)
    L_supp = create_buffer("L_supp",L_lieferant)
    L_order2 = create_buffer("L_order2",L_order)
    L_art = create_buffer("L_art",L_artikel)
    Q245 = create_buffer("Q245",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        return {"first_docu_nr": first_docu_nr, "curr_docu_nr": curr_docu_nr, "p_267": p_267, "last_docu_nr1": last_docu_nr1, "q2-list": q2_list_data}

    def disp_list1():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":
            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:
                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list1a():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if num_entries(last_docu_nr, ";") > 1:
            temp_docu_nr = entry(0, last_docu_nr, ";")
            temp_counter_nr = to_int(entry(1, last_docu_nr, ";"))

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list1b():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list11():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list11a():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if num_entries(last_docu_nr, ";") > 1:
            temp_docu_nr = entry(0, last_docu_nr, ";")
            temp_counter_nr = to_int(entry(1, last_docu_nr, ";"))

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list11b():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list2():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list2a():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if num_entries(last_docu_nr, ";") > 1:
            temp_docu_nr = entry(0, last_docu_nr, ";")
            temp_counter_nr = to_int(entry(1, last_docu_nr, ";"))

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list2b():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

        else:

            l_orderhdr_obj_list = {}
            for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                     (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                if not w_list:
                    continue

                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list22():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr, L_lieferant.firma).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list22a():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if num_entries(last_docu_nr, ";") > 1:
            temp_docu_nr = entry(0, last_docu_nr, ";")
            temp_counter_nr = to_int(entry(1, last_docu_nr, ";"))

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                    if not cost_list:
                        continue

                    if l_orderhdr_obj_list.get(l_orderhdr._recid):
                        continue
                    else:
                        l_orderhdr_obj_list[l_orderhdr._recid] = True

                    if dml_only:

                        if matches(l_order1.lief_fax[0],r"D*") and l_order1.lief_fax[2] == ("DML").lower() :
                            create_temp_table_list()
                    else:
                        create_temp_table_list()

                for q_list in query(q_list_data, filters=(lambda q_list: q_list.to_sort > temp_counter_nr)):
                    curr_counter = curr_counter + 1
                    temp_counter_nr = q_list.to_sort

                    if curr_counter >= 25:
                        break
                    else:
                        q2_list = Q2_list()
                        q2_list_data.append(q2_list)

                        buffer_copy(q_list, q2_list,except_fields=["q_list.to_sort"])
                        last_to_sort = q_list.to_sort

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(last_to_sort)
            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_lieferant.firma, L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

    def disp_list22b():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        if stattype == 0 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname == "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 0 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum >= billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 1 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 1) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 2 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.lieferdatum < billdate) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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


        elif stattype == 3 and usrname != "":

            if last_docu_nr != "":

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                         (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname) & (L_orderhdr.docu_nr > (last_docu_nr).lower())).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

            else:

                l_orderhdr_obj_list = {}
                for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 2) & (L_order1.pos == 0)).filter(
                        (L_orderhdr.bestelldatum >= from_date) & (L_orderhdr.bestelldatum <= to_date) & (L_orderhdr.lief_nr == l_supp.lief_nr) & (L_orderhdr.angebot_lief[inc_value(0)] == deptnr) & (L_orderhdr.betriebsnr <= 1) & (L_orderhdr.besteller == usrname)).order_by(L_orderhdr.docu_nr, L_lieferant.firma, L_orderhdr.bestelldatum).all():
                    w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
                    if not w_list:
                        continue

                    cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
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

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_data.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring


    def currency_list():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        local_nr:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            local_nr = waehrung.waehrungsnr
        w_list = W_list()
        w_list_data.append(w_list)


        if local_nr != 0:
            w_list.wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).order_by(Waehrung.wabkurz).all():
            w_list = W_list()
            w_list_data.append(w_list)

            w_list.nr = waehrung.waehrungsnr
            w_list.wabkurz = waehrung.wabkurz


    def cr_temp_table():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        t_amount:Decimal = to_decimal("0.0")
        app_lvl = 0

        queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})
        while None != queasy:
            app_lvl = queasy.number1

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 245) & (Queasy.char1 == l_orderhdr.docu_nr) & (Queasy._recid > curr_recid)).first()

        if app_sort.lower()  == ("ALL").lower() :

            if counter == 1:
                first_docu_nr = l_orderhdr.docu_nr

            if (counter >= 25) and (curr_docu_nr != l_orderhdr.docu_nr):
                return

            if (counter >= 25) and (last_docu_nr1 != l_orderhdr.docu_nr):
                return
            q2_list = Q2_list()
            q2_list_data.append(q2_list)

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


            last_docu_nr1 = l_orderhdr.docu_nr

            if p_71:

                queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})

                if queasy:

                    q245 = db_session.query(Q245).filter(
                             (Q245.key == 245) & (Q245.char1 == l_orderhdr.docu_nr)).first()
                    while None != q245:

                        if q2_list.username != "":

                            if num_entries(q2_list.username, ";") < 4:
                                q2_list.username = q2_list.username + entry(0, q245.char3, "|") + ";"
                            else:
                                q2_list.username = q2_list.username + entry(0, q245.char3, "|")
                        else:
                            q2_list.username = entry(0, q245.char3, "|") + ";"

                        curr_recid = q245._recid
                        q245 = db_session.query(Q245).filter(
                                 (Q245.key == 245) & (Q245.char1 == l_orderhdr.docu_nr) & (Q245._recid > curr_recid)).first()
                    for loop in range(1,4 + 1) :

                        if num_entries(q2_list.username, ";") != 4:
                            q2_list.username = q2_list.username + ";"
                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

                    if queasy:
                        q2_list.username = queasy.char3
                    else:
                        q2_list.username = ""
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

            if sorttype == 2:
                last_docu_nr1 = last_docu_nr1 + ";" + to_string(counter)

        elif app_sort.lower()  == ("Approve 1").lower() :

            queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

            if not queasy:

                queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})

                if not queasy:

                    if counter == 1:
                        first_docu_nr = l_orderhdr.docu_nr

                    if (counter >= 25) and (curr_docu_nr != l_orderhdr.docu_nr):
                        return

                    if (counter >= 25) and (last_docu_nr1 != l_orderhdr.docu_nr):
                        return
                    q2_list = Q2_list()
                    q2_list_data.append(q2_list)

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


                    last_docu_nr1 = l_orderhdr.docu_nr

                    if p_71:

                        queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

                        if queasy:
                            q2_list.username = queasy.char3
                        else:
                            q2_list.username = ""
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

                    if sorttype == 2:
                        last_docu_nr1 = last_docu_nr1 + ";" + to_string(counter)
        else:

            if app_lvl == approval:

                if counter == 1:
                    first_docu_nr = l_orderhdr.docu_nr

                if (counter >= 25) and (curr_docu_nr != l_orderhdr.docu_nr):
                    return

                if (counter >= 25) and (last_docu_nr1 != l_orderhdr.docu_nr):
                    return
                q2_list = Q2_list()
                q2_list_data.append(q2_list)

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


                last_docu_nr1 = l_orderhdr.docu_nr

                if p_71:

                    queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})

                    if queasy:

                        q245 = db_session.query(Q245).filter(
                                 (Q245.key == 245) & (Q245.char1 == l_orderhdr.docu_nr)).first()
                        while None != q245:

                            if q2_list.username != "":

                                if num_entries(q2_list.username, ";") < 4:
                                    q2_list.username = q2_list.username + entry(0, q245.char3, "|") + ";"
                                else:
                                    q2_list.username = q2_list.username + entry(0, q245.char3, "|")
                            else:
                                q2_list.username = entry(0, q245.char3, "|") + ";"

                            curr_recid = q245._recid
                            q245 = db_session.query(Q245).filter(
                                     (Q245.key == 245) & (Q245.char1 == l_orderhdr.docu_nr) & (Q245._recid > curr_recid)).first()
                        for loop in range(1,4 + 1) :

                            if num_entries(q2_list.username, ";") != 4:
                                q2_list.username = q2_list.username + ";"
                    else:

                        queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

                        if queasy:
                            q2_list.username = queasy.char3
                        else:
                            q2_list.username = ""
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

                if sorttype == 2:
                    last_docu_nr1 = last_docu_nr1 + ";" + to_string(counter)


    def create_temp_table_list():

        nonlocal first_docu_nr, curr_docu_nr, p_267, last_docu_nr1, q2_list_data, counter, curr_counter, last_to_sort, temp_docu_nr, temp_counter_nr, approval, p_71, loop, app_lvl, l_order, l_lieferant, l_artikel, queasy, htparam, l_orderhdr, parameters, waehrung
        nonlocal t_liefno, last_docu_nr, sorttype, deptnr, all_supp, stattype, usrname, from_date, to_date, billdate, dml_only, app_sort
        nonlocal l_order1, l_supp, l_order2, l_art, q245


        nonlocal w_list, cost_list, l_order1, l_supp, l_order2, l_art, q2_list, q_list, q245
        nonlocal w_list_data, cost_list_data, q2_list_data, q_list_data

        t_amount:Decimal = to_decimal("0.0")
        app_lvl = 0

        queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})
        while None != queasy:
            app_lvl = queasy.number1

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 245) & (Queasy.char1 == l_orderhdr.docu_nr) & (Queasy._recid > curr_recid)).first()

        if app_sort.lower()  == ("ALL").lower() :
            counter = counter + 1
            q_list = Q_list()
            q_list_data.append(q_list)

            q_list.bestelldatum = l_orderhdr.bestelldatum
            q_list.bezeich = cost_list.bezeich
            q_list.firma = l_lieferant.firma
            q_list.docu_nr = l_orderhdr.docu_nr
            q_list.l_orderhdr_lieferdatum = l_orderhdr.lieferdatum
            q_list.wabkurz = w_list.wabkurz
            q_list.bestellart = l_orderhdr.bestellart
            q_list.gedruckt = l_orderhdr.gedruckt
            q_list.l_orderhdr_besteller = l_orderhdr.besteller
            q_list.l_order_gedruckt = l_order1.gedruckt
            q_list.zeit = l_order1.zeit
            q_list.lief_fax_2 = l_order1.lief_fax[1]
            q_list.l_order_lieferdatum = l_order1.lieferdatum
            q_list.lief_fax_3 = l_order1.lief_fax[2]
            q_list.lieferdatum_eff = l_order1.lieferdatum_eff
            q_list.lief_fax_1 = l_order1.lief_fax[0]
            q_list.lief_nr = l_order1.lief_nr
            q_list.to_sort = counter

            if sorttype == 2:
                last_docu_nr1 = l_orderhdr.docu_nr

            if p_71:

                queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})

                if queasy:

                    q245 = db_session.query(Q245).filter(
                             (Q245.key == 245) & (Q245.char1 == l_orderhdr.docu_nr)).first()
                    while None != q245:

                        if q_list.username != "":

                            if num_entries(q_list.username, ";") < 4:
                                q_list.username = q_list.username + entry(0, q245.char3, "|") + ";"
                            else:
                                q_list.username = q_list.username + entry(0, q245.char3, "|")
                        else:
                            q_list.username = entry(0, q245.char3, "|") + ";"

                        curr_recid = q245._recid
                        q245 = db_session.query(Q245).filter(
                                 (Q245.key == 245) & (Q245.char1 == l_orderhdr.docu_nr) & (Q245._recid > curr_recid)).first()
                    for loop in range(1,4 + 1) :

                        if num_entries(q_list.username, ";") != 4:
                            q_list.username = q_list.username + ";"
                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

                    if queasy:
                        q_list.username = queasy.char3
                    else:
                        q_list.username = ""
            else:

                queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

                if queasy:
                    q_list.username = queasy.char3
                else:
                    q_list.username = ""

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
            q_list.tot_amount =  to_decimal(t_amount)

        elif app_sort.lower()  == ("Approve 1").lower() :

            queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

            if not queasy:

                queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})

                if not queasy:
                    counter = counter + 1
                    q_list = Q_list()
                    q_list_data.append(q_list)

                    q_list.bestelldatum = l_orderhdr.bestelldatum
                    q_list.bezeich = cost_list.bezeich
                    q_list.firma = l_lieferant.firma
                    q_list.docu_nr = l_orderhdr.docu_nr
                    q_list.l_orderhdr_lieferdatum = l_orderhdr.lieferdatum
                    q_list.wabkurz = w_list.wabkurz
                    q_list.bestellart = l_orderhdr.bestellart
                    q_list.gedruckt = l_orderhdr.gedruckt
                    q_list.l_orderhdr_besteller = l_orderhdr.besteller
                    q_list.l_order_gedruckt = l_order1.gedruckt
                    q_list.zeit = l_order1.zeit
                    q_list.lief_fax_2 = l_order1.lief_fax[1]
                    q_list.l_order_lieferdatum = l_order1.lieferdatum
                    q_list.lief_fax_3 = l_order1.lief_fax[2]
                    q_list.lieferdatum_eff = l_order1.lieferdatum_eff
                    q_list.lief_fax_1 = l_order1.lief_fax[0]
                    q_list.lief_nr = l_order1.lief_nr
                    q_list.to_sort = counter

                    if sorttype == 2:
                        last_docu_nr1 = l_orderhdr.docu_nr

                    if p_71:

                        queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

                        if queasy:
                            q_list.username = queasy.char3
                        else:
                            q_list.username = ""
                    else:

                        queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

                        if queasy:
                            q_list.username = queasy.char3
                        else:
                            q_list.username = ""

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
                    q_list.tot_amount =  to_decimal(t_amount)


        else:

            if app_lvl == approval:
                counter = counter + 1
                q_list = Q_list()
                q_list_data.append(q_list)

                q_list.bestelldatum = l_orderhdr.bestelldatum
                q_list.bezeich = cost_list.bezeich
                q_list.firma = l_lieferant.firma
                q_list.docu_nr = l_orderhdr.docu_nr
                q_list.l_orderhdr_lieferdatum = l_orderhdr.lieferdatum
                q_list.wabkurz = w_list.wabkurz
                q_list.bestellart = l_orderhdr.bestellart
                q_list.gedruckt = l_orderhdr.gedruckt
                q_list.l_orderhdr_besteller = l_orderhdr.besteller
                q_list.l_order_gedruckt = l_order1.gedruckt
                q_list.zeit = l_order1.zeit
                q_list.lief_fax_2 = l_order1.lief_fax[1]
                q_list.l_order_lieferdatum = l_order1.lieferdatum
                q_list.lief_fax_3 = l_order1.lief_fax[2]
                q_list.lieferdatum_eff = l_order1.lieferdatum_eff
                q_list.lief_fax_1 = l_order1.lief_fax[0]
                q_list.lief_nr = l_order1.lief_nr
                q_list.to_sort = counter

                if sorttype == 2:
                    last_docu_nr1 = l_orderhdr.docu_nr

                if p_71:

                    queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})

                    if queasy:

                        q245 = db_session.query(Q245).filter(
                                 (Q245.key == 245) & (Q245.char1 == l_orderhdr.docu_nr)).first()
                        while None != q245:

                            if q_list.username != "":

                                if num_entries(q_list.username, ";") < 4:
                                    q_list.username = q_list.username + entry(0, q245.char3, "|") + ";"
                                else:
                                    q_list.username = q_list.username + entry(0, q245.char3, "|")
                            else:
                                q_list.username = entry(0, q245.char3, "|") + ";"

                            curr_recid = q245._recid
                            q245 = db_session.query(Q245).filter(
                                     (Q245.key == 245) & (Q245.char1 == l_orderhdr.docu_nr) & (Q245._recid > curr_recid)).first()
                        for loop in range(1,4 + 1) :

                            if num_entries(q_list.username, ";") != 4:
                                q_list.username = q_list.username + ";"
                    else:

                        queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

                        if queasy:
                            q_list.username = queasy.char3
                        else:
                            q_list.username = ""
                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 214)],"char1": [(eq, to_string(l_orderhdr._recid))]})

                    if queasy:
                        q_list.username = queasy.char3
                    else:
                        q_list.username = ""

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
                q_list.tot_amount =  to_decimal(t_amount)

    if app_sort.lower()  == ("Approve 2").lower() :
        approval = 1

    if app_sort.lower()  == ("Approve 3").lower() :
        approval = 2

    if app_sort.lower()  == ("Approve 4").lower() :
        approval = 3

    htparam = get_cache (Htparam, {"paramnr": [(eq, 71)]})

    if htparam.paramgruppe == 21:
        p_71 = htparam.flogical

    if t_liefno != 0:

        l_supp = get_cache (L_lieferant, {"lief_nr": [(eq, t_liefno)]})
    create_costlist()
    currency_list()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 267)]})
    p_267 = htparam.flogical

    if sorttype == 1:

        if all_supp:

            if deptnr < 0:
                disp_list1()

            elif deptnr > 0:
                disp_list11()

        if not all_supp:

            if deptnr < 0:
                disp_list2()

            elif deptnr > 0:
                disp_list22()

    elif sorttype == 2:

        if all_supp:

            if deptnr < 0:
                disp_list1a()

            elif deptnr > 0:
                disp_list11a()

        if not all_supp:

            if deptnr < 0:
                disp_list2a()

            elif deptnr > 0:
                disp_list22a()

    elif sorttype == 3:

        if all_supp:

            if deptnr < 0:
                disp_list1b()

            elif deptnr > 0:
                disp_list11b()

        if not all_supp:

            if deptnr < 0:
                disp_list2b()

            elif deptnr > 0:
                disp_list22b()

    return generate_output()