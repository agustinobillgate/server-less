from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, L_untergrup, L_op, Gl_acct, H_bill, H_bill_line, H_artikel, H_rezept, H_rezlin

def autodeduct_listbl(sorttype:int, curr_lager:int, from_grp:int, transdate:date, fdate:date, tdate:date):
    tot_amount = to_decimal("0.0")
    tot_avrg_amount = to_decimal("0.0")
    c_list_list = []
    deduct_compli:bool = False
    l_artikel = l_untergrup = l_op = gl_acct = h_bill = h_bill_line = h_artikel = h_rezept = h_rezlin = None

    c_list = t_list = None

    c_list_list, C_list = create_model("C_list", {"artnr":int, "bezeich":str, "munit":str, "inhalt":decimal, "zwkum":int, "endkum":int, "qty":decimal, "qty1":decimal, "amount":decimal, "avrg_amount":decimal, "fibukonto":str, "cost_center":str, "store":int, "dept":int, "price":decimal, "item_artno":int})
    t_list_list, T_list = create_model("T_list", {"dept":int, "rechnr":int, "pay":decimal, "rmtrans":decimal, "compli":decimal, "coupon":decimal, "fibukonto":str, "pax":int}, {"fibukonto": "0000000000"})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_amount, tot_avrg_amount, c_list_list, deduct_compli, l_artikel, l_untergrup, l_op, gl_acct, h_bill, h_bill_line, h_artikel, h_rezept, h_rezlin
        nonlocal sorttype, curr_lager, from_grp, transdate, fdate, tdate


        nonlocal c_list, t_list
        nonlocal c_list_list, t_list_list
        return {"tot_amount": tot_amount, "tot_avrg_amount": tot_avrg_amount, "c-list": c_list_list}

    def journal_list1():

        nonlocal tot_amount, tot_avrg_amount, c_list_list, deduct_compli, l_artikel, l_untergrup, l_op, gl_acct, h_bill, h_bill_line, h_artikel, h_rezept, h_rezlin
        nonlocal sorttype, curr_lager, from_grp, transdate, fdate, tdate


        nonlocal c_list, t_list
        nonlocal c_list_list, t_list_list


        c_list_list.clear()

        if from_grp == 0:

            if sorttype == 1:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0)).order_by(L_artikel.artnr).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.artnr = l_artikel.artnr
                    c_list.bezeich = l_artikel.bezeich
                    c_list.munit = l_artikel.masseinheit
                    c_list.inhalt =  to_decimal(l_artikel.inhalt)
                    c_list.zwkum = l_artikel.zwkum
                    c_list.endkum = l_artikel.endkum
                    c_list.qty =  to_decimal(l_op.anzahl)
                    c_list.fibukonto = l_op.stornogrund
                    c_list.amount =  to_decimal(l_op.warenwert)
                    c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                    tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                    gl_acct = db_session.query(Gl_acct).filter(
                             (Gl_acct.fibukonto == c_list.fibukonto)).first()

                    if gl_acct:
                        c_list.cost_center = gl_acct.bezeich

            elif sorttype == 2:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0)).order_by(L_artikel.bezeich).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.artnr = l_artikel.artnr
                    c_list.bezeich = l_artikel.bezeich
                    c_list.munit = l_artikel.masseinheit
                    c_list.inhalt =  to_decimal(l_artikel.inhalt)
                    c_list.zwkum = l_artikel.zwkum
                    c_list.endkum = l_artikel.endkum
                    c_list.qty =  to_decimal(l_op.anzahl)
                    c_list.fibukonto = l_op.stornogrund
                    c_list.amount =  to_decimal(l_op.warenwert)
                    c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                    tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                    gl_acct = db_session.query(Gl_acct).filter(
                             (Gl_acct.fibukonto == c_list.fibukonto)).first()

                    if gl_acct:
                        c_list.cost_center = gl_acct.bezeich

            elif sorttype == 3:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0)).order_by(L_artikel.zwkum, L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)

                    c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                    if not c_list:
                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = 0
                        c_list.fibukonto = ""
                        c_list.endkum = l_artikel.endkum
                        c_list.zwkum = l_artikel.zwkum
                        c_list.bezeich = l_untergrup.bezeich


                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.artnr = l_artikel.artnr
                    c_list.bezeich = l_artikel.bezeich
                    c_list.munit = l_artikel.masseinheit
                    c_list.inhalt =  to_decimal(l_artikel.inhalt)
                    c_list.zwkum = l_artikel.zwkum
                    c_list.endkum = l_artikel.endkum
                    c_list.qty =  to_decimal(l_op.anzahl)
                    c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                    c_list.fibukonto = l_op.stornogrund
                    c_list.amount =  to_decimal(l_op.warenwert)
                    c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                    tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                    gl_acct = db_session.query(Gl_acct).filter(
                             (Gl_acct.fibukonto == c_list.fibukonto)).first()

                    if gl_acct:
                        c_list.cost_center = gl_acct.bezeich

            elif sorttype == 4:
                create_list()
                get_l_artikels()
        else:

            if sorttype == 1:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0)).order_by(L_artikel.artnr).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.artnr = l_artikel.artnr
                    c_list.bezeich = l_artikel.bezeich
                    c_list.munit = l_artikel.masseinheit
                    c_list.inhalt =  to_decimal(l_artikel.inhalt)
                    c_list.zwkum = l_artikel.zwkum
                    c_list.endkum = l_artikel.endkum
                    c_list.qty =  to_decimal(l_op.anzahl)
                    c_list.fibukonto = l_op.stornogrund
                    c_list.amount =  to_decimal(l_op.warenwert)
                    c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                    tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                    gl_acct = db_session.query(Gl_acct).filter(
                             (Gl_acct.fibukonto == c_list.fibukonto)).first()

                    if gl_acct:
                        c_list.cost_center = gl_acct.bezeich

            elif sorttype == 2:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0)).order_by(L_artikel.bezeich).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.artnr = l_artikel.artnr
                    c_list.bezeich = l_artikel.bezeich
                    c_list.munit = l_artikel.masseinheit
                    c_list.inhalt =  to_decimal(l_artikel.inhalt)
                    c_list.zwkum = l_artikel.zwkum
                    c_list.endkum = l_artikel.endkum
                    c_list.qty =  to_decimal(l_op.anzahl)
                    c_list.fibukonto = l_op.stornogrund
                    c_list.amount =  to_decimal(l_op.warenwert)
                    c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                    tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                    gl_acct = db_session.query(Gl_acct).filter(
                             (Gl_acct.fibukonto == c_list.fibukonto)).first()

                    if gl_acct:
                        c_list.cost_center = gl_acct.bezeich

            elif sorttype == 3:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                         (L_op.lager_nr == curr_lager) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0)).order_by(L_artikel.zwkum, L_artikel.bezeich, L_op.datum, L_op.lscheinnr).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)

                    c_list = query(c_list_list, filters=(lambda c_list: c_list.artnr == 0 and c_list.endkum == l_artikel.endkum and c_list.zwkum == l_artikel.zwkum), first=True)

                    if not c_list:
                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.artnr = 0
                        c_list.fibukonto = ""
                        c_list.endkum = l_artikel.endkum
                        c_list.zwkum = l_artikel.zwkum
                        c_list.bezeich = l_untergrup.bezeich


                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.artnr = l_artikel.artnr
                    c_list.bezeich = l_artikel.bezeich
                    c_list.munit = l_artikel.masseinheit
                    c_list.inhalt =  to_decimal(l_artikel.inhalt)
                    c_list.zwkum = l_artikel.zwkum
                    c_list.endkum = l_artikel.endkum
                    c_list.qty =  to_decimal(l_op.anzahl)
                    c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(l_op.anzahl)
                    c_list.fibukonto = l_op.stornogrund
                    c_list.amount =  to_decimal(l_op.warenwert)
                    c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                    tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                    gl_acct = db_session.query(Gl_acct).filter(
                             (Gl_acct.fibukonto == c_list.fibukonto)).first()

                    if gl_acct:
                        c_list.cost_center = gl_acct.bezeich

            elif sorttype == 4:
                create_list()
                get_l_artikels()


    def create_list():

        nonlocal tot_amount, tot_avrg_amount, c_list_list, deduct_compli, l_artikel, l_untergrup, l_op, gl_acct, h_bill, h_bill_line, h_artikel, h_rezept, h_rezlin
        nonlocal sorttype, curr_lager, from_grp, transdate, fdate, tdate


        nonlocal c_list, t_list
        nonlocal c_list_list, t_list_list

        h_bill_line_obj_list = []
        for h_bill_line, h_bill in db_session.query(H_bill_line, H_bill).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr)).filter(
                 (H_bill_line.bill_datum >= htparam.fdate) & (H_bill_line.bill_datum <= tdate)).order_by(H_bill_line._recid).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.artnr == h_bill_line.artnr)).first()

            if h_artikel and h_artikel.artart == 0:

                t_list = query(t_list_list, filters=(lambda t_list: t_list.dept == h_bill_line.departement and t_list.rechnr == h_bill_line.rechnr), first=True)

                if not t_list:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.dept = h_bill_line.departement
                    t_list.rechnr = h_bill_line.rechnr
                    t_list.pax = h_bill.belegung


    def get_l_artikels():

        nonlocal tot_amount, tot_avrg_amount, c_list_list, deduct_compli, l_artikel, l_untergrup, l_op, gl_acct, h_bill, h_bill_line, h_artikel, h_rezept, h_rezlin
        nonlocal sorttype, curr_lager, from_grp, transdate, fdate, tdate


        nonlocal c_list, t_list
        nonlocal c_list_list, t_list_list

        do_it:bool = False
        pax:int = 0

        for t_list in query(t_list_list):

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departement == t_list.dept) & (H_bill_line.rechnr == t_list.rechnr)).order_by(H_bill_line.rechnr).all():

                if h_bill_line.artnr == 0:
                    pass
                else:

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.artnr == h_bill_line.artnr) & (H_artikel.departement == h_bill_line.departement)).first()

                    if not h_artikel:
                        pass

                    elif h_artikel.artart == 0:

                        if h_artikel.artnrlager != 0:

                            l_artikel = db_session.query(L_artikel).filter(
                                     (L_artikel.artnr == h_artikel.artnrlager) & (L_artikel.bezeich == h_artikel.bezeich)).first()

                            if l_artikel and l_artikel.endkum <= 2:

                                c_list = query(c_list_list, filters=(lambda c_list: c_list.dept == t_list.dept and c_list.artnr == l_artikel.artnr and c_list.fibukonto == c_list.fibukonto and c_list.item_artno == h_bill_line.artnr), first=True)

                                if not c_list:
                                    c_list = C_list()
                                    c_list_list.append(c_list)

                                    c_list.dept = t_list.dept
                                    c_list.fibukonto = t_list.fibukonto
                                    c_list.bezeich = l_artikel.bezeich
                                    c_list.artnr = l_artikel.artnr
                                    c_list.price =  to_decimal(l_artikel.vk_preis)
                                    c_list.store = h_artikel.lagernr
                                    c_list.item_artno = h_bill_line.artnr
                                    c_list.inhalt =  to_decimal(l_artikel.inhalt)

                                l_op_obj_list = []
                                for l_op, l_untergrup in db_session.query(L_op, L_untergrup).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                                         (L_op.lager_nr == h_artikel.lagernr) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.anzahl != 0) & (L_op.artnr == l_artikel.artnr)).order_by(L_op.datum, L_op.lscheinnr).all():
                                    if l_op._recid in l_op_obj_list:
                                        continue
                                    else:
                                        l_op_obj_list.append(l_op._recid)


                                    c_list.qty =  to_decimal(l_op.anzahl)
                                    c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal(h_bill_line.anzahl)
                                    c_list.fibukonto = l_op.stornogrund
                                    c_list.amount =  to_decimal(l_op.warenwert)
                                    c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                                    tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                                    gl_acct = db_session.query(Gl_acct).filter(
                                             (Gl_acct.fibukonto == c_list.fibukonto)).first()

                                    if gl_acct:
                                        c_list.cost_center = gl_acct.bezeich

                        elif h_artikel.artnrrezept != 0:

                            c_list = query(c_list_list, filters=(lambda c_list: c_list.dept == t_list.dept and c_list.artnr == h_artikel.artnr and c_list.fibukonto == c_list.fibukonto and c_list.item_artno == h_bill_line.artnr), first=True)

                            if not c_list:
                                pax = pax + t_list.pax


                                c_list = C_list()
                                c_list_list.append(c_list)

                                c_list.dept = t_list.dept
                                c_list.fibukonto = t_list.fibukonto
                                c_list.bezeich = h_artikel.bezeich + " - " + to_string(pax, ">>>9") + " pax"
                                c_list.artnr = h_artikel.artnr
                                c_list.store = h_artikel.lagernr
                                c_list.item_artno = h_bill_line.artnr


                            else:
                                c_list.qty1 =  to_decimal(c_list.qty) + to_decimal(h_bill_line.anzahl)

                            h_rezept = db_session.query(H_rezept).filter(
                                     (H_rezept.artnrrezept == h_artikel.artnrrezept)).first()

                            if h_rezept:
                                get_recipe(h_rezept.artnrrezept, 1)


    def get_recipe(p_artnr:int, menge:decimal):

        nonlocal tot_amount, tot_avrg_amount, c_list_list, deduct_compli, l_artikel, l_untergrup, l_op, gl_acct, h_bill, h_bill_line, h_artikel, h_rezept, h_rezlin
        nonlocal sorttype, curr_lager, from_grp, transdate, fdate, tdate


        nonlocal c_list, t_list
        nonlocal c_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                get_recipe2(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel and l_artikel.endkum <= 2:

                    c_list = query(c_list_list, filters=(lambda c_list: c_list.dept == t_list.dept and c_list.artnr == l_artikel.artnr and c_list.item_artno == h_bill_line.artnr), first=True)

                    if not c_list:
                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.bezeich = l_artikel.bezeich
                        c_list.dept = t_list.dept
                        c_list.fibukonto = t_list.fibukonto
                        c_list.munit = l_artikel.masseinheit
                        c_list.artnr = l_artikel.artnr
                        c_list.price =  to_decimal(l_artikel.vk_preis)
                        c_list.item_artno = h_bill_line.artnr
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)

                        l_op_obj_list = []
                        for l_op, l_untergrup in db_session.query(L_op, L_untergrup).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                                 (L_op.lager_nr == h_artikel.lagernr) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.artnr == l_artikel.artnr) & (L_op.anzahl != 0)).order_by(L_op.datum, L_op.lscheinnr).all():
                            if l_op._recid in l_op_obj_list:
                                continue
                            else:
                                l_op_obj_list.append(l_op._recid)


                            c_list.qty =  to_decimal(l_op.anzahl)
                            c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal((h_bill_line.anzahl) * to_decimal(inh) )
                            c_list.fibukonto = l_op.stornogrund
                            c_list.amount =  to_decimal(l_op.warenwert)
                            c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                            tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                            tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                            gl_acct = db_session.query(Gl_acct).filter(
                                     (Gl_acct.fibukonto == c_list.fibukonto)).first()

                            if gl_acct:
                                c_list.cost_center = gl_acct.bezeich


    def get_recipe2(p_artnr:int, menge:decimal):

        nonlocal tot_amount, tot_avrg_amount, c_list_list, deduct_compli, l_artikel, l_untergrup, l_op, gl_acct, h_bill, h_bill_line, h_artikel, h_rezept, h_rezlin
        nonlocal sorttype, curr_lager, from_grp, transdate, fdate, tdate


        nonlocal c_list, t_list
        nonlocal c_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                get_recipe3(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel and l_artikel.endkum <= 2:

                    c_list = query(c_list_list, filters=(lambda c_list: c_list.dept == t_list.dept and c_list.artnr == l_artikel.artnr and c_list.item_artno == h_bill_line.artnr), first=True)

                    if not c_list:
                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.bezeich = l_artikel.bezeich
                        c_list.dept = t_list.dept
                        c_list.fibukonto = t_list.fibukonto
                        c_list.munit = l_artikel.masseinheit
                        c_list.artnr = l_artikel.artnr
                        c_list.price =  to_decimal(l_artikel.vk_preis)
                        c_list.qty1 =  to_decimal(c_list.qty) + to_decimal(h_bill_line.anzahl)
                        c_list.item_artno = h_bill_line.artnr
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)

                        l_op_obj_list = []
                        for l_op, l_untergrup in db_session.query(L_op, L_untergrup).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                                 (L_op.lager_nr == h_artikel.lagernr) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.artnr == l_artikel.artnr) & (L_op.anzahl != 0)).order_by(L_op.datum, L_op.lscheinnr).all():
                            if l_op._recid in l_op_obj_list:
                                continue
                            else:
                                l_op_obj_list.append(l_op._recid)


                            c_list.qty =  to_decimal(l_op.anzahl)
                            c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal((h_bill_line.anzahl) * to_decimal(inh) )
                            c_list.fibukonto = l_op.stornogrund
                            c_list.amount =  to_decimal(l_op.warenwert)
                            c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                            tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                            tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                            gl_acct = db_session.query(Gl_acct).filter(
                                     (Gl_acct.fibukonto == c_list.fibukonto)).first()

                            if gl_acct:
                                c_list.cost_center = gl_acct.bezeich


    def get_recipe3(p_artnr:int, menge:decimal):

        nonlocal tot_amount, tot_avrg_amount, c_list_list, deduct_compli, l_artikel, l_untergrup, l_op, gl_acct, h_bill, h_bill_line, h_artikel, h_rezept, h_rezlin
        nonlocal sorttype, curr_lager, from_grp, transdate, fdate, tdate


        nonlocal c_list, t_list
        nonlocal c_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                get_recipe4(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel and l_artikel.endkum <= 2:

                    c_list = query(c_list_list, filters=(lambda c_list: c_list.dept == t_list.dept and c_list.artnr == l_artikel.artnr and c_list.item_artno == h_bill_line.artnr), first=True)

                    if not c_list:
                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.bezeich = l_artikel.bezeich
                        c_list.dept = t_list.dept
                        c_list.fibukonto = t_list.fibukonto
                        c_list.artnr = l_artikel.artnr
                        c_list.munit = l_artikel.masseinheit
                        c_list.price =  to_decimal(l_artikel.vk_preis)
                        c_list.item_artno = h_bill_line.artnr
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)

                        l_op_obj_list = []
                        for l_op, l_untergrup in db_session.query(L_op, L_untergrup).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                                 (L_op.lager_nr == h_artikel.lagernr) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.artnr == l_artikel.artnr) & (L_op.anzahl != 0)).order_by(L_op.datum, L_op.lscheinnr).all():
                            if l_op._recid in l_op_obj_list:
                                continue
                            else:
                                l_op_obj_list.append(l_op._recid)


                            c_list.qty =  to_decimal(l_op.anzahl)
                            c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal((h_bill_line.anzahl) * to_decimal(inh) )
                            c_list.fibukonto = l_op.stornogrund
                            c_list.amount =  to_decimal(l_op.warenwert)
                            c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                            tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                            tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                            gl_acct = db_session.query(Gl_acct).filter(
                                     (Gl_acct.fibukonto == c_list.fibukonto)).first()

                            if gl_acct:
                                c_list.cost_center = gl_acct.bezeich


    def get_recipe4(p_artnr:int, menge:decimal):

        nonlocal tot_amount, tot_avrg_amount, c_list_list, deduct_compli, l_artikel, l_untergrup, l_op, gl_acct, h_bill, h_bill_line, h_artikel, h_rezept, h_rezlin
        nonlocal sorttype, curr_lager, from_grp, transdate, fdate, tdate


        nonlocal c_list, t_list
        nonlocal c_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            if h_rezlin.recipe_flag :
                get_recipe5(h_rezlin.artnrlager, inh)
            else:

                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

                if l_artikel and l_artikel.endkum <= 2:

                    c_list = query(c_list_list, filters=(lambda c_list: c_list.dept == t_list.dept and c_list.artnr == l_artikel.artnr and c_list.fibukonto == t_list.fibukonto and c_list.item_artno == h_bill_line.artnr), first=True)

                    if not c_list:
                        c_list = C_list()
                        c_list_list.append(c_list)

                        c_list.bezeich = l_artikel.bezeich
                        c_list.dept = t_list.dept
                        c_list.fibukonto = t_list.fibukonto
                        c_list.artnr = l_artikel.artnr
                        c_list.price =  to_decimal(l_artikel.vk_preis)
                        c_list.munit = l_artikel.masseinheit
                        c_list.qty1 =  to_decimal(c_list.qty) + to_decimal(h_bill_line.anzahl)
                        c_list.item_artno = h_bill_line.artnr
                        c_list.inhalt =  to_decimal(l_artikel.inhalt)

                        l_op_obj_list = []
                        for l_op, l_untergrup in db_session.query(L_op, L_untergrup).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                                 (L_op.lager_nr == h_artikel.lagernr) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.artnr == l_artikel.artnr) & (L_op.anzahl != 0)).order_by(L_op.datum, L_op.lscheinnr).all():
                            if l_op._recid in l_op_obj_list:
                                continue
                            else:
                                l_op_obj_list.append(l_op._recid)


                            c_list.qty =  to_decimal(l_op.anzahl)
                            c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal((h_bill_line.anzahl) * to_decimal(inh) )
                            c_list.fibukonto = l_op.stornogrund
                            c_list.amount =  to_decimal(l_op.warenwert)
                            c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                            tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                            tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                            gl_acct = db_session.query(Gl_acct).filter(
                                     (Gl_acct.fibukonto == c_list.fibukonto)).first()

                            if gl_acct:
                                c_list.cost_center = gl_acct.bezeich


    def get_recipe5(p_artnr:int, menge:decimal):

        nonlocal tot_amount, tot_avrg_amount, c_list_list, deduct_compli, l_artikel, l_untergrup, l_op, gl_acct, h_bill, h_bill_line, h_artikel, h_rezept, h_rezlin
        nonlocal sorttype, curr_lager, from_grp, transdate, fdate, tdate


        nonlocal c_list, t_list
        nonlocal c_list_list, t_list_list

        inh:decimal = to_decimal("0.0")
        store_found:bool = False
        h_recipe = None
        H_recipe =  create_buffer("H_recipe",H_rezept)

        h_recipe = db_session.query(H_recipe).filter(
                 (H_recipe.artnrrezept == p_artnr)).first()

        for h_rezlin in db_session.query(H_rezlin).filter(
                 (H_rezlin.artnrrezept == p_artnr)).order_by(H_rezlin._recid).all():
            inh =  to_decimal(menge) * to_decimal(h_rezlin.menge) / to_decimal(h_recipe.portion)

            l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == h_rezlin.artnrlager)).first()

            if l_artikel and l_artikel.endkum <= 2:

                c_list = query(c_list_list, filters=(lambda c_list: c_list.dept == t_list.dept and c_list.artnr == l_artikel.artnr and c_list.fibukonto == t_list.fibukonto and c_list.item_artno == h_bill_line.artnr), first=True)

                if not c_list:
                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.bezeich = l_artikel.bezeich
                    c_list.dept = t_list.dept
                    c_list.fibukonto = t_list.fibukonto
                    c_list.artnr = l_artikel.artnr
                    c_list.price =  to_decimal(l_artikel.vk_preis)
                    c_list.munit = l_artikel.masseinheit
                    c_list.qty1 =  to_decimal(c_list.qty) + to_decimal(h_bill_line.anzahl)
                    c_list.item_artno = h_bill_line.artnr
                    c_list.inhalt =  to_decimal(l_artikel.inhalt)

                    l_op_obj_list = []
                    for l_op, l_untergrup in db_session.query(L_op, L_untergrup).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                                 (L_op.lager_nr == h_artikel.lagernr) & (L_op.op_art == 3) & (L_op.datum >= htparam.fdate) & (L_op.datum <= tdate) & ((substring(L_op.lscheinnr, 0, 3) == ("SAD").lower())) & (L_op.loeschflag <= 1) & (L_op.artnr == l_artikel.artnr) & (L_op.anzahl != 0)).order_by(L_op.datum, L_op.lscheinnr).all():
                        if l_op._recid in l_op_obj_list:
                            continue
                        else:
                            l_op_obj_list.append(l_op._recid)


                        c_list.qty =  to_decimal(l_op.anzahl)
                        c_list.qty1 =  to_decimal(l_op.deci1[0]) - to_decimal((h_bill_line.anzahl) * to_decimal(inh) )
                        c_list.fibukonto = l_op.stornogrund
                        c_list.amount =  to_decimal(l_op.warenwert)
                        c_list.avrg_amount =  to_decimal(l_op.warenwert) / to_decimal(l_op.anzahl)


                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)
                        tot_avrg_amount =  to_decimal(tot_avrg_amount) + to_decimal((l_op.warenwert) / to_decimal(l_op.anzahl))

                        gl_acct = db_session.query(Gl_acct).filter(
                                     (Gl_acct.fibukonto == c_list.fibukonto)).first()

                        if gl_acct:
                            c_list.cost_center = gl_acct.bezeich


    journal_list1()

    return generate_output()