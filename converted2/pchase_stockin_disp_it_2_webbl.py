#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_order, Htparam, L_lieferant, L_orderhdr, Waehrung, Queasy

def pchase_stockin_disp_it_2_webbl(sorttype:int, ponum:string, supplier:string, to_supp:string, order_date:date, f_date:date, t_date:date, app_sort:string):

    prepare_cache ([L_order, Htparam, L_lieferant, L_orderhdr, Waehrung])

    q2_list_data = []
    p_71:bool = False
    approval:int = 0
    app_lvl:int = 0
    l_order = htparam = l_lieferant = l_orderhdr = waehrung = queasy = None

    w_list = l_order1 = q2_list = None

    w_list_data, W_list = create_model("W_list", {"nr":int, "wabkurz":string})
    q2_list_data, Q2_list = create_model("Q2_list", {"lief_nr":int, "lief_fax_1":string, "docu_nr":string, "firma":string, "bestelldatum":date, "lieferdatum":date, "wabkurz":string, "bestellart":string, "lief_fax_3":string, "besteller":string, "lief_fax_2":string, "betriebsnr":int, "gedruckt":date})

    L_order1 = create_buffer("L_order1",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_list_data, p_71, approval, app_lvl, l_order, htparam, l_lieferant, l_orderhdr, waehrung, queasy
        nonlocal sorttype, ponum, supplier, to_supp, order_date, f_date, t_date, app_sort
        nonlocal l_order1


        nonlocal w_list, l_order1, q2_list
        nonlocal w_list_data, q2_list_data

        return {"q2-list": q2_list_data}

    def currency_list():

        nonlocal q2_list_data, p_71, approval, app_lvl, l_order, htparam, l_lieferant, l_orderhdr, waehrung, queasy
        nonlocal sorttype, ponum, supplier, to_supp, order_date, f_date, t_date, app_sort
        nonlocal l_order1


        nonlocal w_list, l_order1, q2_list
        nonlocal w_list_data, q2_list_data

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


    def assign_it():

        nonlocal q2_list_data, p_71, approval, app_lvl, l_order, htparam, l_lieferant, l_orderhdr, waehrung, queasy
        nonlocal sorttype, ponum, supplier, to_supp, order_date, f_date, t_date, app_sort
        nonlocal l_order1


        nonlocal w_list, l_order1, q2_list
        nonlocal w_list_data, q2_list_data

        if p_71 and app_sort.lower()  != ("ALL").lower() :
            app_lvl = 0

            queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, l_orderhdr.docu_nr)]})
            while None != queasy:
                app_lvl = queasy.number1

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 245) & (Queasy.char1 == l_orderhdr.docu_nr) & (Queasy._recid > curr_recid)).first()

            if app_sort.lower()  == ("Approve 1").lower()  and app_lvl == 0:
                q2_list = Q2_list()
                q2_list_data.append(q2_list)

                q2_list.lief_nr = l_orderhdr.lief_nr
                q2_list.lief_fax_1 = l_order1.lief_fax[0]
                q2_list.docu_nr = l_orderhdr.docu_nr
                q2_list.firma = l_lieferant.firma
                q2_list.bestelldatum = l_orderhdr.bestelldatum
                q2_list.lieferdatum = l_orderhdr.lieferdatum
                q2_list.wabkurz = w_list.wabkurz
                q2_list.bestellart = l_orderhdr.bestellart
                q2_list.lief_fax_3 = l_orderhdr.lief_fax[2]
                q2_list.besteller = l_orderhdr.besteller
                q2_list.lief_fax_2 = l_order1.lief_fax[1]
                q2_list.betriebsnr = l_orderhdr.betriebsnr
                q2_list.gedruckt = l_orderhdr.gedruckt


            else:

                if app_lvl == approval:
                    q2_list = Q2_list()
                    q2_list_data.append(q2_list)

                    q2_list.lief_nr = l_orderhdr.lief_nr
                    q2_list.lief_fax_1 = l_order1.lief_fax[0]
                    q2_list.docu_nr = l_orderhdr.docu_nr
                    q2_list.firma = l_lieferant.firma
                    q2_list.bestelldatum = l_orderhdr.bestelldatum
                    q2_list.lieferdatum = l_orderhdr.lieferdatum
                    q2_list.wabkurz = w_list.wabkurz
                    q2_list.bestellart = l_orderhdr.bestellart
                    q2_list.lief_fax_3 = l_orderhdr.lief_fax[2]
                    q2_list.besteller = l_orderhdr.besteller
                    q2_list.lief_fax_2 = l_order1.lief_fax[1]
                    q2_list.betriebsnr = l_orderhdr.betriebsnr
                    q2_list.gedruckt = l_orderhdr.gedruckt


        else:
            q2_list = Q2_list()
            q2_list_data.append(q2_list)

            q2_list.lief_nr = l_orderhdr.lief_nr
            q2_list.lief_fax_1 = l_order1.lief_fax[0]
            q2_list.docu_nr = l_orderhdr.docu_nr
            q2_list.firma = l_lieferant.firma
            q2_list.bestelldatum = l_orderhdr.bestelldatum
            q2_list.lieferdatum = l_orderhdr.lieferdatum
            q2_list.wabkurz = w_list.wabkurz
            q2_list.bestellart = l_orderhdr.bestellart
            q2_list.lief_fax_3 = l_orderhdr.lief_fax[2]
            q2_list.besteller = l_orderhdr.besteller
            q2_list.lief_fax_2 = l_order1.lief_fax[1]
            q2_list.betriebsnr = l_orderhdr.betriebsnr
            q2_list.gedruckt = l_orderhdr.gedruckt

    htparam = get_cache (Htparam, {"paramnr": [(eq, 71)]})

    if htparam.paramgruppe == 21:
        p_71 = htparam.flogical

    if app_sort.lower()  == ("Approve 2").lower() :
        approval = 1

    if app_sort.lower()  == ("Approve 3").lower() :
        approval = 2

    if app_sort.lower()  == ("Approve 4").lower() :
        approval = 3

    if app_sort.lower()  == ("Approved").lower() :
        approval = 4


    currency_list()

    if supplier == None:
        supplier = ""

    if to_supp == None:
        to_supp = ""

    if trim(ponum) == "":
        ponum = ""
    supplier = "*" + supplier + "*"
    to_supp = "*" + to_supp + "*"
    ponum = "*" + ponum + "*"

    if sorttype == 1:

        l_orderhdr_obj_list = {}
        for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) & (matches(L_lieferant.firma,supplier))).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                 (L_orderhdr.betriebsnr <= 1) & (matches(L_orderhdr.docu_nr,ponum))).order_by(L_lieferant.firma, L_orderhdr.docu_nr).all():
            w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
            if not w_list:
                continue

            if l_orderhdr_obj_list.get(l_orderhdr._recid):
                continue
            else:
                l_orderhdr_obj_list[l_orderhdr._recid] = True


            assign_it()

    if sorttype == 2:

        l_orderhdr_obj_list = {}
        for l_orderhdr, l_lieferant, l_order1 in db_session.query(L_orderhdr, L_lieferant, L_order1).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
                 (L_orderhdr.bestelldatum == order_date) & (L_orderhdr.betriebsnr <= 1) & (matches(L_orderhdr.docu_nr,ponum))).order_by(L_orderhdr.docu_nr).all():
            w_list = query(w_list_data, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
            if not w_list:
                continue

            if l_orderhdr_obj_list.get(l_orderhdr._recid):
                continue
            else:
                l_orderhdr_obj_list[l_orderhdr._recid] = True


            assign_it()

    return generate_output()