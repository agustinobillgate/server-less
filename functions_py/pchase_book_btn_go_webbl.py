#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_pprice, L_lieferant, L_order, L_op

def pchase_book_btn_go_webbl(sorttype:int, from_date:date, to_date:date, mtd_date:date, mi_ch:string, mi_all:bool, s_artnr:int):

    prepare_cache ([L_artikel, L_pprice, L_lieferant, L_order, L_op])

    pchase_list_data = []
    tmpart:int = 0
    f_date:date = None
    t_date:date = None
    datum:date = None
    lief_nr:int = 0
    artnr:int = 0
    t_qty:Decimal = Decimal("0.0000000")
    tot_qty:Decimal = Decimal("0.0000000")
    t_price:Decimal = Decimal("0.0000000")
    tot_price:Decimal = Decimal("0.0000000")
    l_artikel = l_pprice = l_lieferant = l_order = l_op = None

    pchase_list = l_art = l_ppr = l_lief = None

    pchase_list_data, Pchase_list = create_model("Pchase_list", {"bestelldatum":date, "firma":string, "docu_nr":string, "traubensort":string, "lief_einheit":Decimal, "betriebsnr":int, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "remark":string, "artnr":int, "bezeich":string, "deliv_note":string})

    L_art = create_buffer("L_art",L_artikel)
    L_ppr = create_buffer("L_ppr",L_pprice)
    L_lief = create_buffer("L_lief",L_lieferant)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pchase_list_data, tmpart, f_date, t_date, datum, lief_nr, artnr, t_qty, tot_qty, t_price, tot_price, l_artikel, l_pprice, l_lieferant, l_order, l_op
        nonlocal sorttype, from_date, to_date, mtd_date, mi_ch, mi_all, s_artnr
        nonlocal l_art, l_ppr, l_lief


        nonlocal pchase_list, l_art, l_ppr, l_lief
        nonlocal pchase_list_data

        return {"pchase-list": pchase_list_data}

    def custom_rounding(dec:Decimal, format_data:str, is_up:bool = True):
        if is_up:
            return dec.quantize(Decimal(format_data), rounding=ROUND_HALF_UP)
        else:
            return dec.quantize(Decimal(format_data), rounding=ROUND_HALF_DOWN)

    if mi_ch.lower()  == ("FTD").lower() :
        f_date = from_date
        t_date = to_date
    else:
        f_date = date_mdy(1, 1, get_year(mtd_date))
        t_date = mtd_date

    set_cache(L_pprice, (L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.anzahl != 0) & (L_pprice.warenwert != 0),[], True,[],["docu_nr"])

    set_cache(L_order, (L_order.docu_nr.in_(get_cache_value_list(L_pprice, "docu_nr"))),[["docu_nr", "lief_nr", "artnr"]], True,[],[])

    set_cache(L_op, (L_op.datum >= f_date) & (L_op.datum <= t_date),[["lscheinnr", "lief_nr", "artnr", "datum"], ["docu_nr", "lief_nr", "artnr", "datum"]], True,[],[])


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

            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter((L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_pprice.bestelldatum.desc(), L_lieferant.firma, L_art.bezeich, L_pprice.einzelpreis).all():

                # if l_pprice_obj_list.get(l_pprice._recid):
                #     continue
                # else:
                #     l_pprice_obj_list[l_pprice._recid] = True

                if datum != l_pprice.bestelldatum:
                    pchase_list = Pchase_list()
                    pchase_list_data.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  custom_rounding(t_qty, "0.01")
                    pchase_list.warenwert =  custom_rounding(t_price, "0.01")

                    t_qty = Decimal("0.0000000")
                    t_price =  Decimal("0.0000000")

                datum = l_pprice.bestelldatum
                pchase_list = Pchase_list()
                pchase_list_data.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  custom_rounding(l_art.lief_einheit, "0.01")
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  custom_rounding(l_pprice.anzahl, "0.01")
                pchase_list.einzelpreis =  custom_rounding(l_pprice.einzelpreis, "0.01")
                pchase_list.warenwert =  custom_rounding(l_pprice.warenwert, "0.01")
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich

                t_qty = t_qty + custom_rounding(l_pprice.anzahl, "0.01")
                t_price =  t_price + custom_rounding(l_pprice.warenwert, "0.01")
                tot_qty = tot_qty + custom_rounding(l_pprice.anzahl, "0.01")
                tot_price =  tot_price + custom_rounding(l_pprice.warenwert, "0.01")

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = get_cache (L_op, {"lscheinnr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if not l_op:
                    l_op = get_cache (L_op, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

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

            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter((L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_lieferant.firma, L_pprice.bestelldatum.desc(), L_art.bezeich, L_pprice.einzelpreis).all():

                # if l_pprice_obj_list.get(l_pprice._recid):
                #     continue
                # else:
                #     l_pprice_obj_list[l_pprice._recid] = True

                if lief_nr != l_pprice.lief_nr:
                    pchase_list = Pchase_list()
                    pchase_list_data.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  custom_rounding(t_qty, "0.01")
                    pchase_list.warenwert =  custom_rounding(t_price, "0.01")

                    t_qty = Decimal("0.0000000")
                    t_price =  Decimal("0.0000000")

                lief_nr = l_pprice.lief_nr
                pchase_list = Pchase_list()
                pchase_list_data.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  custom_rounding(l_art.lief_einheit, "0.01")
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  custom_rounding(l_pprice.anzahl, "0.01")
                pchase_list.einzelpreis =  custom_rounding(l_pprice.einzelpreis, "0.01")
                pchase_list.warenwert =  custom_rounding(l_pprice.warenwert, "0.01")
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich

                t_qty = t_qty + custom_rounding(l_pprice.anzahl, "0.01")
                t_price =  t_price + custom_rounding(l_pprice.warenwert, "0.01")
                tot_qty = tot_qty + custom_rounding(l_pprice.anzahl, "0.01")
                tot_price =  tot_price + custom_rounding(l_pprice.warenwert, "0.01")

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = get_cache (L_op, {"lscheinnr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if not l_op:
                    l_op = get_cache (L_op, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

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

            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter((L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_pprice.einzelpreis, L_lieferant.firma, L_pprice.bestelldatum.desc(), L_art.bezeich).all():

                # if l_pprice_obj_list.get(l_pprice._recid):
                #     continue
                # else:
                #     l_pprice_obj_list[l_pprice._recid] = True

                if lief_nr != l_pprice.lief_nr:
                    pchase_list = Pchase_list()
                    pchase_list_data.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  custom_rounding(t_qty, "0.01")
                    pchase_list.warenwert =  custom_rounding(t_price, "0.01")

                    t_qty = Decimal("0.0000000")
                    t_price =  Decimal("0.0000000")

                lief_nr = l_pprice.lief_nr
                pchase_list = Pchase_list()
                pchase_list_data.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  custom_rounding(l_art.lief_einheit, "0.01")
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  custom_rounding(l_pprice.anzahl, "0.01")
                pchase_list.einzelpreis =  custom_rounding(l_pprice.einzelpreis, "0.01")
                pchase_list.warenwert =  custom_rounding(l_pprice.warenwert, "0.01")
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + custom_rounding(l_pprice.anzahl, "0.01")
                t_price =  t_price + custom_rounding(l_pprice.warenwert, "0.01")
                tot_qty = tot_qty + custom_rounding(l_pprice.anzahl, "0.01")
                tot_price =  tot_price + custom_rounding(l_pprice.warenwert, "0.01")

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = get_cache (L_op, {"lscheinnr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if not l_op:
                    l_op = get_cache (L_op, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

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

            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter((L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date) & (L_pprice.artnr == s_artnr)).order_by(L_art.bezeich, L_lieferant.firma, L_pprice.bestelldatum.desc(), L_pprice.einzelpreis).all():

                # if l_pprice_obj_list.get(l_pprice._recid):
                #     continue
                # else:
                #     l_pprice_obj_list[l_pprice._recid] = True

                if artnr != l_pprice.artnr:
                    pchase_list = Pchase_list()
                    pchase_list_data.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  custom_rounding(t_qty, "0.01")
                    pchase_list.warenwert =  custom_rounding(t_price, "0.01")

                    t_qty = Decimal("0.0000000")
                    t_price =  Decimal("0.0000000")

                artnr = l_pprice.artnr
                pchase_list = Pchase_list()
                pchase_list_data.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  custom_rounding(l_art.lief_einheit, "0.01")
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  custom_rounding(l_pprice.anzahl, "0.01")
                pchase_list.einzelpreis =  custom_rounding(l_pprice.einzelpreis, "0.01")
                pchase_list.warenwert =  custom_rounding(l_pprice.warenwert, "0.01")
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich


                t_qty = t_qty + custom_rounding(l_pprice.anzahl, "0.01")
                t_price =  t_price + custom_rounding(l_pprice.warenwert, "0.01")
                tot_qty = tot_qty + custom_rounding(l_pprice.anzahl, "0.01")
                tot_price =  tot_price + custom_rounding(l_pprice.warenwert, "0.01")

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = get_cache (L_op, {"lscheinnr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if not l_op:
                    l_op = get_cache (L_op, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if l_op:

                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr
                else:
                    pchase_list.docu_nr = l_pprice.docu_nr

        pchase_list = Pchase_list()
        pchase_list_data.append(pchase_list)

        pchase_list.docu_nr = "T O T A L"
        pchase_list.anzahl =  t_qty
        pchase_list.warenwert =  t_price


        pchase_list = Pchase_list()
        pchase_list_data.append(pchase_list)

        pchase_list.docu_nr = "GRAND TOTAL"
        pchase_list.anzahl =  tot_qty
        pchase_list.warenwert =  tot_price

    else:

        if sorttype == 1:

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_art = L_artikel()
            l_lieferant = L_lieferant()

            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter((L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date)).order_by(L_pprice.bestelldatum.desc(), L_lieferant.firma, L_art.bezeich, L_pprice.einzelpreis).all():

                # if l_pprice_obj_list.get(l_pprice._recid):
                #     continue
                # else:
                #     l_pprice_obj_list[l_pprice._recid] = True

                if datum != l_pprice.bestelldatum:
                    pchase_list = Pchase_list()
                    pchase_list_data.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  custom_rounding(t_qty, "0.01")
                    pchase_list.warenwert =  custom_rounding(t_price, "0.01")

                    t_qty = Decimal("0.0000000")
                    t_price =  Decimal("0.0000000")

                datum = l_pprice.bestelldatum
                pchase_list = Pchase_list()
                pchase_list_data.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  custom_rounding(l_art.lief_einheit, "0.01")
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  custom_rounding(l_pprice.anzahl, "0.01")
                pchase_list.einzelpreis =  custom_rounding(l_pprice.einzelpreis, "0.01")
                pchase_list.warenwert =  custom_rounding(l_pprice.warenwert, "0.01")
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich

                t_qty = t_qty + custom_rounding(l_pprice.anzahl, "0.01")
                t_price =  t_price + custom_rounding(l_pprice.warenwert, "0.01")
                tot_qty = tot_qty + custom_rounding(l_pprice.anzahl, "0.01")
                tot_price =  tot_price + custom_rounding(l_pprice.warenwert, "0.01")

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = get_cache (L_op, {"lscheinnr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if not l_op:
                    l_op = get_cache (L_op, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

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

            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter((L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date)).order_by(L_lieferant.firma, L_pprice.bestelldatum.desc(), L_art.bezeich, L_pprice.einzelpreis).all():

                # if l_pprice_obj_list.get(l_pprice._recid):
                #     continue
                # else:
                #     l_pprice_obj_list[l_pprice._recid] = True

                if lief_nr != l_pprice.lief_nr:
                    pchase_list = Pchase_list()
                    pchase_list_data.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  custom_rounding(t_qty, "0.01")
                    pchase_list.warenwert =  custom_rounding(t_price, "0.01")

                    t_qty = Decimal("0.0000000")
                    t_price =  Decimal("0.0000000")

                lief_nr = l_pprice.lief_nr
                pchase_list = Pchase_list()
                pchase_list_data.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  custom_rounding(l_art.lief_einheit, "0.01")
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  custom_rounding(l_pprice.anzahl, "0.01")
                pchase_list.einzelpreis =  custom_rounding(l_pprice.einzelpreis, "0.01")
                pchase_list.warenwert =  custom_rounding(l_pprice.warenwert, "0.01")
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich

                t_qty = t_qty + custom_rounding(l_pprice.anzahl, "0.01")
                t_price =  t_price + custom_rounding(l_pprice.warenwert, "0.01")
                tot_qty = tot_qty + custom_rounding(l_pprice.anzahl, "0.01")
                tot_price =  tot_price + custom_rounding(l_pprice.warenwert, "0.01")

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = get_cache (L_op, {"lscheinnr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if not l_op:
                    l_op = get_cache (L_op, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

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

            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter((L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date)).order_by(L_pprice.einzelpreis, L_lieferant.firma, L_pprice.bestelldatum.desc(), L_art.bezeich).all():

                # if l_pprice_obj_list.get(l_pprice._recid):
                #     continue
                # else:
                #     l_pprice_obj_list[l_pprice._recid] = True

                if lief_nr != l_pprice.lief_nr:
                    pchase_list = Pchase_list()
                    pchase_list_data.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  custom_rounding(t_qty, "0.01")
                    pchase_list.warenwert =  custom_rounding(t_price, "0.01")

                    t_qty = Decimal("0.0000000")
                    t_price =  Decimal("0.0000000")

                lief_nr = l_pprice.lief_nr
                pchase_list = Pchase_list()
                pchase_list_data.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  custom_rounding(l_art.lief_einheit, "0.01")
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  custom_rounding(l_pprice.anzahl, "0.01")
                pchase_list.einzelpreis =  custom_rounding(l_pprice.einzelpreis, "0.01")
                pchase_list.warenwert =  custom_rounding(l_pprice.warenwert, "0.01")
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich

                t_qty = t_qty + custom_rounding(l_pprice.anzahl, "0.01")
                t_price =  t_price + custom_rounding(l_pprice.warenwert, "0.01")
                tot_qty = tot_qty + custom_rounding(l_pprice.anzahl, "0.01")
                tot_price =  tot_price + custom_rounding(l_pprice.warenwert, "0.01")

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = get_cache (L_op, {"lscheinnr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if not l_op:

                    l_op = get_cache (L_op, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

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

            for l_pprice.bestelldatum, l_pprice.docu_nr, l_pprice.betriebsnr, l_pprice.anzahl, l_pprice.einzelpreis, l_pprice.warenwert, l_pprice.lief_nr, l_pprice.artnr, l_pprice._recid, l_art.traubensorte, l_art.lief_einheit, l_art.artnr, l_art.bezeich, l_art._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.docu_nr, L_pprice.betriebsnr, L_pprice.anzahl, L_pprice.einzelpreis, L_pprice.warenwert, L_pprice.lief_nr, L_pprice.artnr, L_pprice._recid, L_art.traubensorte, L_art.lief_einheit, L_art.artnr, L_art.bezeich, L_art._recid, L_lieferant.firma, L_lieferant._recid).join(L_art,(L_art.artnr == L_pprice.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter((L_pprice.bestelldatum >= f_date) & (L_pprice.bestelldatum <= t_date)).order_by(L_art.bezeich, L_lieferant.firma, L_pprice.bestelldatum.desc(), L_pprice.einzelpreis).all():

                # if l_pprice_obj_list.get(l_pprice._recid):
                #     continue
                # else:
                #     l_pprice_obj_list[l_pprice._recid] = True

                if artnr != l_pprice.artnr:
                    pchase_list = Pchase_list()
                    pchase_list_data.append(pchase_list)

                    pchase_list.docu_nr = "T O T A L"
                    pchase_list.anzahl =  custom_rounding(t_qty, "0.01")
                    pchase_list.warenwert =  custom_rounding(t_price, "0.01")

                    t_qty = Decimal("0.0000000")
                    t_price =  Decimal("0.0000000")

                artnr = l_pprice.artnr
                pchase_list = Pchase_list()
                pchase_list_data.append(pchase_list)

                pchase_list.bestelldatum = l_pprice.bestelldatum
                pchase_list.firma = l_lieferant.firma
                pchase_list.deliv_note = l_pprice.docu_nr
                pchase_list.traubensort = l_art.traubensorte
                pchase_list.lief_einheit =  custom_rounding(l_art.lief_einheit, "0.01")
                pchase_list.betriebsnr = l_pprice.betriebsnr
                pchase_list.anzahl =  custom_rounding(l_pprice.anzahl, "0.01")
                pchase_list.einzelpreis =  custom_rounding(l_pprice.einzelpreis, "0.01")
                pchase_list.warenwert =  custom_rounding(l_pprice.warenwert, "0.01")
                pchase_list.artnr = l_art.artnr
                pchase_list.bezeich = l_art.bezeich

                t_qty = t_qty + custom_rounding(l_pprice.anzahl, "0.01")
                t_price =  t_price + custom_rounding(l_pprice.warenwert, "0.01")
                tot_qty = tot_qty + custom_rounding(l_pprice.anzahl, "0.01")
                tot_price =  tot_price + custom_rounding(l_pprice.warenwert, "0.01")

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, s_artnr)]})

                if l_order:
                    pchase_list.remark = l_order.besteller

                l_op = get_cache (L_op, {"lscheinnr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if not l_op:
                    l_op = get_cache (L_op, {"docu_nr": [(eq, l_pprice.docu_nr)],"lief_nr": [(eq, l_pprice.lief_nr)],"artnr": [(eq, l_pprice.artnr)],"datum": [(eq, l_pprice.bestelldatum)]})

                if l_op:
                    if l_op.docu_nr == l_op.lscheinnr:
                        pchase_list.docu_nr = "Direct Purchase "
                    else:
                        pchase_list.docu_nr = l_op.docu_nr
                        pchase_list.deliv_note = l_op.lscheinnr
                else:
                    pchase_list.docu_nr = l_pprice.docu_nr
        
        pchase_list = Pchase_list()
        pchase_list_data.append(pchase_list)

        pchase_list.docu_nr = "T O T A L"
        pchase_list.anzahl =  t_qty
        pchase_list.warenwert = t_price


        pchase_list = Pchase_list()
        pchase_list_data.append(pchase_list)

        pchase_list.docu_nr = "GRAND TOTAL"
        pchase_list.anzahl =  tot_qty
        pchase_list.warenwert =  tot_price

    for pchase_list in query(pchase_list_data):

        if pchase_list.anzahl == 0 and pchase_list.warenwert == 0:
            pchase_list_data.remove(pchase_list)

    return generate_output()