#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, L_orderhdr, Waehrung, Bediener, Htparam, Parameters, L_artikel, L_lieferant, Gl_acct, L_pprice, L_bestand

def prepare_chg_pr_1bl(docu_nr:string):

    prepare_cache ([Htparam, Parameters, L_artikel, L_lieferant, Gl_acct, L_pprice, L_bestand])

    billdate = None
    comments = ""
    deptnr = 0
    lieferdatum = None
    deptname = ""
    hierarchie = False
    tot = to_decimal("0.0")
    s_list_list = []
    t_l_orderhdr_list = []
    t_l_artikel_list = []
    t_parameters_list = []
    t_waehrung_list = []
    local_curr:int = 0
    amt:Decimal = to_decimal("0.0")
    def_curr:string = ""
    tot_anz:Decimal = to_decimal("0.0")
    anz_anf_best:Decimal = to_decimal("0.0")
    anz_eingang:Decimal = to_decimal("0.0")
    anz_ausgang:Decimal = to_decimal("0.0")
    l_order = l_orderhdr = waehrung = bediener = htparam = parameters = l_artikel = l_lieferant = gl_acct = l_pprice = l_bestand = None

    s_list = t_parameters = t_l_orderhdr = t_waehrung = t_l_artikel = usr = b_list = None

    s_list_list, S_list = create_model_like(L_order, {"curr":string, "exrate":Decimal, "s_recid":int, "amount":Decimal, "supp1":int, "supp2":int, "supp3":int, "suppn1":string, "suppn2":string, "suppn3":string, "supps":string, "du_price1":Decimal, "du_price2":Decimal, "du_price3":Decimal, "curr1":string, "curr2":string, "curr3":string, "fdate1":date, "fdate2":date, "fdate3":date, "tdate1":date, "tdate2":date, "tdate3":date, "desc_coa":string, "last_pprice":Decimal, "avg_pprice":Decimal, "lprice":Decimal, "lief_fax2":string, "ek_letzter":Decimal, "lief_einheit":int, "supplier":string, "lief_fax_2":string, "vk_preis":Decimal, "soh":Decimal, "last_pdate":date, "a_firma":string, "last_pbook":Decimal})
    t_parameters_list, T_parameters = create_model("T_parameters", {"varname":string, "vstring":string})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_waehrung_list, T_waehrung = create_model_like(Waehrung)
    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "traubensort":string, "lief_einheit":Decimal, "bezeich":string, "jahrgang":int, "soh":Decimal})

    Usr = create_buffer("Usr",Bediener)
    B_list = S_list
    b_list_list = s_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, comments, deptnr, lieferdatum, deptname, hierarchie, tot, s_list_list, t_l_orderhdr_list, t_l_artikel_list, t_parameters_list, t_waehrung_list, local_curr, amt, def_curr, tot_anz, anz_anf_best, anz_eingang, anz_ausgang, l_order, l_orderhdr, waehrung, bediener, htparam, parameters, l_artikel, l_lieferant, gl_acct, l_pprice, l_bestand
        nonlocal docu_nr
        nonlocal usr, b_list


        nonlocal s_list, t_parameters, t_l_orderhdr, t_waehrung, t_l_artikel, usr, b_list
        nonlocal s_list_list, t_parameters_list, t_l_orderhdr_list, t_waehrung_list, t_l_artikel_list

        return {"billdate": billdate, "comments": comments, "deptnr": deptnr, "lieferdatum": lieferdatum, "deptname": deptname, "hierarchie": hierarchie, "tot": tot, "s-list": s_list_list, "t-l-orderhdr": t_l_orderhdr_list, "t-l-artikel": t_l_artikel_list, "t-parameters": t_parameters_list, "t-waehrung": t_waehrung_list}

    def reload_s_list():

        nonlocal billdate, comments, deptnr, lieferdatum, deptname, hierarchie, tot, s_list_list, t_l_orderhdr_list, t_l_artikel_list, t_parameters_list, t_waehrung_list, local_curr, amt, def_curr, tot_anz, anz_anf_best, anz_eingang, anz_ausgang, l_order, l_orderhdr, waehrung, bediener, htparam, parameters, l_artikel, l_lieferant, gl_acct, l_pprice, l_bestand
        nonlocal docu_nr
        nonlocal usr, b_list


        nonlocal s_list, t_parameters, t_l_orderhdr, t_waehrung, t_l_artikel, usr, b_list
        nonlocal s_list_list, t_parameters_list, t_l_orderhdr_list, t_waehrung_list, t_l_artikel_list

        l_order_obj_list = {}
        for l_order, l_artikel in db_session.query(L_order, L_artikel).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag <= 1)).order_by(L_artikel.bezeich).all():
            if l_order_obj_list.get(l_order._recid):
                continue
            else:
                l_order_obj_list[l_order._recid] = True

            usr = db_session.query(Usr).filter(
                     (Usr.username == l_order.lief_fax[0])).first()
            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(l_order, s_list)
            amt =  to_decimal(s_list.anzahl) * to_decimal(s_list.einzelpreis)
            s_list.amount =  to_decimal(l_order.warenwert)
            s_list.s_recid = l_order._recid
            s_list.angebot_lief[1] = l_order.angebot_lief[1]
            s_list.einzelpreis =  to_decimal(l_order.einzelpreis)
            s_list.lief_fax_2 = l_order.lief_fax[1]
            s_list.ek_letzter =  to_decimal(l_artikel.ek_letzter)
            s_list.lief_einheit = l_artikel.lief_einheit
            s_list.vk_preis =  to_decimal(l_artikel.vk_preis)
            s_list.lprice =  to_decimal(l_artikel.ek_letzter)

            if l_order.bestellart != "":
                s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                s_list.du_price1 =  to_decimal(to_decimal(entry(1 , entry(0 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                s_list.curr1 = entry(2, entry(0, l_order.bestellart , "-") , ";")
                s_list.fdate1 = date_mdy(entry(3, entry(0, l_order.bestellart , "-") , ";"))
                s_list.tdate1 = date_mdy(entry(4, entry(0, l_order.bestellart , "-") , ";"))
                s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                s_list.du_price2 =  to_decimal(to_decimal(entry(1 , entry(1 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                s_list.curr2 = entry(2, entry(1, l_order.bestellart , "-") , ";")
                s_list.fdate2 = date_mdy(entry(3, entry(1, l_order.bestellart , "-") , ";"))
                s_list.tdate2 = date_mdy(entry(4, entry(1, l_order.bestellart , "-") , ";"))
                s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))
                s_list.du_price3 =  to_decimal(to_decimal(entry(1 , entry(2 , l_order.bestellart , "-") , ";"))) / to_decimal("100")
                s_list.curr1 = entry(2, entry(2, l_order.bestellart , "-") , ";")
                s_list.fdate1 = date_mdy(entry(3, entry(2, l_order.bestellart , "-") , ";"))
                s_list.tdate1 = date_mdy(entry(4, entry(2, l_order.bestellart , "-") , ";"))

            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp1)]})

            if l_lieferant:
                s_list.suppn1 = l_lieferant.firma

            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp2)]})

            if l_lieferant:
                s_list.suppn2 = l_lieferant.firma

            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.supp3)]})

            if l_lieferant:
                s_list.suppn3 = l_lieferant.firma

            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, s_list.angebot_lief[1])]})

            if l_lieferant:
                s_list.supps = l_lieferant.firma

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

            if gl_acct:
                s_list.desc_coa = gl_acct.bezeich

            l_pprice_obj_list = {}
            l_pprice = L_pprice()
            l_lieferant = L_lieferant()
            for l_pprice.bestelldatum, l_pprice.einzelpreis, l_pprice._recid, l_lieferant.firma, l_lieferant._recid in db_session.query(L_pprice.bestelldatum, L_pprice.einzelpreis, L_pprice._recid, L_lieferant.firma, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                     (L_pprice.artnr == l_artikel.artnr)).order_by(L_pprice.bestelldatum.desc()).yield_per(100):
                if l_pprice_obj_list.get(l_pprice._recid):
                    continue
                else:
                    l_pprice_obj_list[l_pprice._recid] = True


                s_list.last_pdate = l_pprice.bestelldatum
                s_list.last_pbook =  to_decimal(l_pprice.einzelpreis)
                s_list.a_firma = l_lieferant.firma


                break

            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_order.lief_nr)]})

            if l_lieferant:
                s_list.supplier = l_lieferant.firma

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

            if l_bestand:
                s_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) -\
                        l_bestand.anz_ausgang

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, l_order.angebot_lief[2])]})

            if waehrung:
                s_list.curr = waehrung.wabkurz
                s_list.exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

            if waehrung:
                local_curr = to_int(s_list.angebot_lief[2])

                if local_curr != 1:
                    s_list.exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


            tot =  to_decimal("0")

            s_list = query(s_list_list, first=True)
            while None != s_list:

                if s_list.curr == "" or s_list.curr == " ":
                    s_list.curr = def_curr
                tot =  to_decimal(tot) + to_decimal(s_list.amount)

                s_list = query(s_list_list, next=True)
                pass


    htparam = get_cache (Htparam, {"paramnr": [(eq, 386)]})
    hierarchie = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    def_curr = htparam.fchar

    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})
    comments = l_orderhdr.lief_fax[2]
    deptnr = l_orderhdr.angebot_lief[0]
    lieferdatum = l_orderhdr.lieferdatum
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_list.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == deptnr)).first()

    if parameters:
        deptname = parameters.vstring
    reload_s_list()

    for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.rec_id = l_artikel._recid
        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.traubensort = l_artikel.traubensorte
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.jahrgang = l_artikel.jahrgang

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower())).order_by(Parameters._recid).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring

    for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():
        t_waehrung = T_waehrung()
        t_waehrung_list.append(t_waehrung)

        buffer_copy(waehrung, t_waehrung)

    return generate_output()