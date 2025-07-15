#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_pprice, L_lieferant, L_order, L_op

def pchase_book_btn_go_webbl_fitria_1600ms(sorttype:int, from_date:date, to_date:date, mtd_date:date, mi_ch:string, mi_all:bool, s_artnr:int):

    prepare_cache ([L_artikel, L_pprice, L_lieferant, L_order, L_op])

    pchase_list_list = []
    tmpart:int = 0
    f_date:date = None
    t_date:date = None
    datum:date = None
    lief_nr:int = 0
    artnr:int = 0
    t_qty:int = 0
    tot_qty:int = 0
    t_price:Decimal = to_decimal("0.0")
    tot_price:Decimal = to_decimal("0.0")
    l_artikel = l_pprice = l_lieferant = l_order = l_op = None

    pchase_list = l_art = l_ppr = l_lief = None

    pchase_list_list, Pchase_list = create_model("Pchase_list", {"bestelldatum":date, "firma":string, "docu_nr":string, "traubensort":string, "lief_einheit":Decimal, "betriebsnr":int, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "remark":string, "artnr":int, "bezeich":string, "deliv_note":string})

    L_art = create_buffer("L_art",L_artikel)
    L_ppr = create_buffer("L_ppr",L_pprice)
    L_lief = create_buffer("L_lief",L_lieferant)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pchase_list_list, tmpart, f_date, t_date, datum, lief_nr, artnr, t_qty, tot_qty, t_price, tot_price, l_artikel, l_pprice, l_lieferant, l_order, l_op
        nonlocal sorttype, from_date, to_date, mtd_date, mi_ch, mi_all, s_artnr
        nonlocal l_art, l_ppr, l_lief


        nonlocal pchase_list, l_art, l_ppr, l_lief
        nonlocal pchase_list_list

        return {"pchase-list": pchase_list_list}

    if mi_ch.lower()  == ("FTD").lower() :
        f_date = from_date
        t_date = to_date


    else:
        f_date = date_mdy(1, 1, get_year(mtd_date))
        t_date = mtd_date

    if not mi_all:
        t_qty = 0
        t_price =  to_decimal("0")
        tot_qty = 0
        tot_price =  to_decimal("0")

        if sorttype == 1:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_pprice.bestelldatum.desc(), L_lieferant.firma, L_art.bezeich, L_pprice.einzelpreis).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True

                if datum != l_pprice.bestelldatum:
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  to_decimal(t_qty)
                    pchase_list.warenwert =  to_decimal(t_price)


                    t_qty = 0
                    t_price =  to_decimal("0")
                datum = l_pprice.bestelldatum
                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + l_pprice.anzahl
                t_price =  to_decimal(t_price) + to_decimal(l_pprice.warenwert)
                tot_qty = tot_qty + l_pprice.anzahl
                tot_price =  to_decimal(tot_price) + to_decimal(l_pprice.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = db_session.query(L_op).filter(
                         ((L_op.lscheinnr == l_pprice.docu_nr) | (L_op.docu_nr == l_pprice.docu_nr)) & (L_op.lief_nr == l_pprice.lief_nr) & (L_op.artnr == s_artnr) & (L_op.datum == l_pprice.bestelldatum)).first()

                if l_op:

                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr


                else:
                    pchase_list.docu_nr = l_pprice.docu_nr

        elif sorttype == 2:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_lieferant.firma, L_pprice.bestelldatum.desc(), L_art.bezeich, L_pprice.einzelpreis).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True

                if lief_nr != l_pprice.lief_nr:
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  to_decimal(t_qty)
                    pchase_list.warenwert =  to_decimal(t_price)


                    t_qty = 0
                    t_price =  to_decimal("0")
                lief_nr = l_pprice.lief_nr
                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + l_pprice.anzahl
                t_price =  to_decimal(t_price) + to_decimal(l_pprice.warenwert)
                tot_qty = tot_qty + l_pprice.anzahl
                tot_price =  to_decimal(tot_price) + to_decimal(l_pprice.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = db_session.query(L_op).filter(
                         ((L_op.lscheinnr == l_pprice.docu_nr) | (L_op.docu_nr == l_pprice.docu_nr)) & (L_op.lief_nr == l_pprice.lief_nr) & (L_op.artnr == s_artnr) & (L_op.datum == l_pprice.bestelldatum)).first()

                if l_op:

                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr


                else:
                    pchase_list.docu_nr = l_pprice.docu_nr

        elif sorttype == 3:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_pprice.einzelpreis, L_lieferant.firma, L_pprice.bestelldatum.desc(), L_art.bezeich).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True

                if lief_nr != l_pprice.lief_nr:
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  to_decimal(t_qty)
                    pchase_list.warenwert =  to_decimal(t_price)


                    t_qty = 0
                    t_price =  to_decimal("0")
                lief_nr = l_pprice.lief_nr
                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + l_pprice.anzahl
                t_price =  to_decimal(t_price) + to_decimal(l_pprice.warenwert)
                tot_qty = tot_qty + l_pprice.anzahl
                tot_price =  to_decimal(tot_price) + to_decimal(l_pprice.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = db_session.query(L_op).filter(
                         ((L_op.lscheinnr == l_pprice.docu_nr) | (L_op.docu_nr == l_pprice.docu_nr)) & (L_op.lief_nr == l_pprice.lief_nr) & (L_op.artnr == s_artnr) & (L_op.datum == l_pprice.bestelldatum)).first()

                if l_op:

                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr


                else:
                    pchase_list.docu_nr = l_pprice.docu_nr
        else:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_art.bezeich, L_lieferant.firma, L_pprice.bestelldatum.desc(), L_pprice.einzelpreis).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True

                if artnr != l_pprice.artnr:
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  to_decimal(t_qty)
                    pchase_list.warenwert =  to_decimal(t_price)


                    t_qty = 0
                    t_price =  to_decimal("0")
                artnr = l_pprice.artnr
                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + l_pprice.anzahl
                t_price =  to_decimal(t_price) + to_decimal(l_pprice.warenwert)
                tot_qty = tot_qty + l_pprice.anzahl
                tot_price =  to_decimal(tot_price) + to_decimal(l_pprice.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = db_session.query(L_op).filter(
                         ((L_op.lscheinnr == l_pprice.docu_nr) | (L_op.docu_nr == l_pprice.docu_nr)) & (L_op.lief_nr == l_pprice.lief_nr) & (L_op.artnr == s_artnr) & (L_op.datum == l_pprice.bestelldatum)).first()

                if l_op:

                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr


                else:
                    pchase_list.docu_nr = l_pprice.docu_nr
        pchase_list = Pchase_list()
        pchase_list_list.append(pchase_list)

        pchase_list.docu_nr = "T O T A L"
        pchase_list.anzahl =  to_decimal(t_qty)
        pchase_list.warenwert =  to_decimal(t_price)


        pchase_list = Pchase_list()
        pchase_list_list.append(pchase_list)

        pchase_list.docu_nr = "GRAND TOTAL"
        pchase_list.anzahl =  to_decimal(tot_qty)
        pchase_list.warenwert =  to_decimal(tot_price)


    else:

        if sorttype == 1:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.anzahl != 0) & (L_pprice.warenwert != 0)).order_by(L_pprice.bestelldatum.desc(), L_lieferant.firma, L_art.bezeich, L_pprice.einzelpreis).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True

                if datum != l_pprice.bestelldatum:
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  to_decimal(t_qty)
                    pchase_list.warenwert =  to_decimal(t_price)


                    t_qty = 0
                    t_price =  to_decimal("0")
                datum = l_pprice.bestelldatum
                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + l_pprice.anzahl
                t_price =  to_decimal(t_price) + to_decimal(l_pprice.warenwert)
                tot_qty = tot_qty + l_pprice.anzahl
                tot_price =  to_decimal(tot_price) + to_decimal(l_pprice.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = db_session.query(L_op).filter(
                         ((L_op.lscheinnr == l_pprice.docu_nr) | (L_op.docu_nr == l_pprice.docu_nr)) & (L_op.lief_nr == l_pprice.lief_nr) & (L_op.artnr == l_pprice.artnr) & (L_op.datum == l_pprice.bestelldatum)).first()

                if l_op:

                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr


                else:
                    pchase_list.docu_nr = l_pprice.docu_nr

        elif sorttype == 2:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.anzahl != 0) & (L_pprice.warenwert != 0)).order_by(L_lieferant.firma, L_pprice.bestelldatum.desc(), L_art.bezeich, L_pprice.einzelpreis).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True

                if lief_nr != l_pprice.lief_nr:
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  to_decimal(t_qty)
                    pchase_list.warenwert =  to_decimal(t_price)


                    t_qty = 0
                    t_price =  to_decimal("0")
                lief_nr = l_pprice.lief_nr
                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + l_pprice.anzahl
                t_price =  to_decimal(t_price) + to_decimal(l_pprice.warenwert)
                tot_qty = tot_qty + l_pprice.anzahl
                tot_price =  to_decimal(tot_price) + to_decimal(l_pprice.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = db_session.query(L_op).filter(
                         ((L_op.lscheinnr == l_pprice.docu_nr) | (L_op.docu_nr == l_pprice.docu_nr)) & (L_op.lief_nr == l_pprice.lief_nr) & (L_op.artnr == l_pprice.artnr) & (L_op.datum == l_pprice.bestelldatum)).first()

                if l_op:

                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr


                else:
                    pchase_list.docu_nr = l_pprice.docu_nr

        elif sorttype == 3:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.anzahl != 0) & (L_pprice.warenwert != 0)).order_by(L_pprice.einzelpreis, L_lieferant.firma, L_pprice.bestelldatum.desc(), L_art.bezeich).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True

                if lief_nr != l_pprice.lief_nr:
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  to_decimal(t_qty)
                    pchase_list.warenwert =  to_decimal(t_price)


                    t_qty = 0
                    t_price =  to_decimal("0")
                lief_nr = l_pprice.lief_nr
                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + l_pprice.anzahl
                t_price =  to_decimal(t_price) + to_decimal(l_pprice.warenwert)
                tot_qty = tot_qty + l_pprice.anzahl
                tot_price =  to_decimal(tot_price) + to_decimal(l_pprice.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = db_session.query(L_op).filter(
                         ((L_op.lscheinnr == l_pprice.docu_nr) | (L_op.docu_nr == l_pprice.docu_nr)) & (L_op.lief_nr == l_pprice.lief_nr) & (L_op.artnr == l_pprice.artnr) & (L_op.datum == l_pprice.bestelldatum)).first()

                if l_op:

                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr


                else:
                    pchase_list.docu_nr = l_pprice.docu_nr
        else:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.anzahl != 0) & (L_pprice.warenwert != 0)).order_by(L_art.bezeich, L_lieferant.firma, L_pprice.bestelldatum.desc(), L_pprice.einzelpreis).all():
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True

                if artnr != l_pprice.artnr:
                    pchase_list = Pchase_list()
                    pchase_list_list.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  to_decimal(t_qty)
                    pchase_list.warenwert =  to_decimal(t_price)


                    t_qty = 0
                    t_price =  to_decimal("0")
                artnr = l_pprice.artnr
                pchase_list = Pchase_list()
                pchase_list_list.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  to_decimal(l_art.lief_einheit)
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  to_decimal(l_pprice.anzahl)
                pchase_list.einzelpreis =  to_decimal(l_pprice.einzelpreis)
                pchase_list.warenwert =  to_decimal(l_pprice.warenwert)
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + l_pprice.anzahl
                t_price =  to_decimal(t_price) + to_decimal(l_pprice.warenwert)
                tot_qty = tot_qty + l_pprice.anzahl
                tot_price =  to_decimal(tot_price) + to_decimal(l_pprice.warenwert)

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = db_session.query(L_op).filter(
                         ((L_op.lscheinnr == l_pprice.docu_nr) | (L_op.docu_nr == l_pprice.docu_nr)) & (L_op.lief_nr == l_pprice.lief_nr) & (L_op.artnr == l_pprice.artnr) & (L_op.datum == l_pprice.bestelldatum)).first()

                if l_op:

                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr


                else:
                    pchase_list.docu_nr = l_pprice.docu_nr
        pchase_list = Pchase_list()
        pchase_list_list.append(pchase_list)

        pchase_list.docu_nr = "T O T A L"
        pchase_list.anzahl =  to_decimal(t_qty)
        pchase_list.warenwert =  to_decimal(t_price)


        pchase_list = Pchase_list()
        pchase_list_list.append(pchase_list)

        pchase_list.docu_nr = "GRAND TOTAL"
        pchase_list.anzahl =  to_decimal(tot_qty)
        pchase_list.warenwert =  to_decimal(tot_price)

    for pchase_list in query(pchase_list_list):

        if pchase_list.anzahl == 0 and pchase_list.warenwert == 0:
            pchase_list_list.remove(pchase_list)

    return generate_output()