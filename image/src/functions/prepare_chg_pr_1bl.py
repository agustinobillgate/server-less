from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order, L_orderhdr, Waehrung, Bediener, Htparam, Parameters, L_artikel, L_lieferant, Gl_acct, L_pprice, L_bestand

def prepare_chg_pr_1bl(docu_nr:str):
    billdate = None
    comments = ""
    deptnr = 0
    lieferdatum = None
    deptname = ""
    hierarchie = False
    tot = 0
    s_list_list = []
    t_l_orderhdr_list = []
    t_l_artikel_list = []
    t_parameters_list = []
    t_waehrung_list = []
    local_curr:int = 0
    amt:decimal = 0
    def_curr:str = ""
    tot_anz:decimal = 0
    anz_anf_best:decimal = 0
    anz_eingang:decimal = 0
    anz_ausgang:decimal = 0
    l_order = l_orderhdr = waehrung = bediener = htparam = parameters = l_artikel = l_lieferant = gl_acct = l_pprice = l_bestand = None

    s_list = t_parameters = t_l_orderhdr = t_waehrung = t_l_artikel = usr = b_list = None

    s_list_list, S_list = create_model_like(L_order, {"curr":str, "exrate":decimal, "s_recid":int, "amount":decimal, "supp1":int, "supp2":int, "supp3":int, "suppn1":str, "suppn2":str, "suppn3":str, "supps":str, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "curr1":str, "curr2":str, "curr3":str, "fdate1":date, "fdate2":date, "fdate3":date, "tdate1":date, "tdate2":date, "tdate3":date, "desc_coa":str, "last_pprice":decimal, "avg_pprice":decimal, "lprice":decimal, "lief_fax2":str, "ek_letzter":decimal, "lief_einheit":int, "supplier":str, "lief_fax_2":str, "vk_preis":decimal, "soh":decimal, "last_pdate":date, "a_firma":str, "last_pbook":decimal})
    t_parameters_list, T_parameters = create_model("T_parameters", {"varname":str, "vstring":str})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_waehrung_list, T_waehrung = create_model_like(Waehrung)
    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "traubensort":str, "lief_einheit":decimal, "bezeich":str, "jahrgang":int, "soh":decimal})

    Usr = Bediener
    B_list = S_list
    b_list_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, comments, deptnr, lieferdatum, deptname, hierarchie, tot, s_list_list, t_l_orderhdr_list, t_l_artikel_list, t_parameters_list, t_waehrung_list, local_curr, amt, def_curr, tot_anz, anz_anf_best, anz_eingang, anz_ausgang, l_order, l_orderhdr, waehrung, bediener, htparam, parameters, l_artikel, l_lieferant, gl_acct, l_pprice, l_bestand
        nonlocal usr, b_list


        nonlocal s_list, t_parameters, t_l_orderhdr, t_waehrung, t_l_artikel, usr, b_list
        nonlocal s_list_list, t_parameters_list, t_l_orderhdr_list, t_waehrung_list, t_l_artikel_list
        return {"billdate": billdate, "comments": comments, "deptnr": deptnr, "lieferdatum": lieferdatum, "deptname": deptname, "hierarchie": hierarchie, "tot": tot, "s-list": s_list_list, "t-l-orderhdr": t_l_orderhdr_list, "t-l-artikel": t_l_artikel_list, "t-parameters": t_parameters_list, "t-waehrung": t_waehrung_list}

    def reload_s_list():

        nonlocal billdate, comments, deptnr, lieferdatum, deptname, hierarchie, tot, s_list_list, t_l_orderhdr_list, t_l_artikel_list, t_parameters_list, t_waehrung_list, local_curr, amt, def_curr, tot_anz, anz_anf_best, anz_eingang, anz_ausgang, l_order, l_orderhdr, waehrung, bediener, htparam, parameters, l_artikel, l_lieferant, gl_acct, l_pprice, l_bestand
        nonlocal usr, b_list


        nonlocal s_list, t_parameters, t_l_orderhdr, t_waehrung, t_l_artikel, usr, b_list
        nonlocal s_list_list, t_parameters_list, t_l_orderhdr_list, t_waehrung_list, t_l_artikel_list

        l_order_obj_list = []
        for l_order, l_artikel in db_session.query(L_order, L_artikel).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.lief_nr == 0) &  (L_order.loeschflag <= 1)).all():
            if l_order._recid in l_order_obj_list:
                continue
            else:
                l_order_obj_list.append(l_order._recid)

            usr = db_session.query(Usr).filter(
                    (Usr.username == l_order.lief_fax[0])).first()
            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(l_order, s_list)
            amt = s_list.anzahl * s_list.einzelpreis
            s_list.amount = l_order.warenwert
            s_list.s_recid = l_order._recid
            s_list.angebot_lief[1] = l_order.angebot_lief[1]
            s_list.einzelpreis = l_order.einzelpreis
            s_list.lief_fax_2 = l_order.lief_fax[1]
            s_list.ek_letzter = l_artikel.ek_letzter
            s_list.lief_einheit = l_artikel.lief_einheit
            s_list.vk_preis = l_artikel.vk_preis
            s_list.lprice = l_artikel.ek_letzter

            if l_order.bestellart != "":
                s_list.supp1 = to_int(entry(0, entry(0, l_order.bestellart , "-") , ";"))
                s_list.du_price1 = decimal.Decimal(entry(1, entry(0, l_order.bestellart , "-") , ";")) / 100
                s_list.curr1 = entry(2, entry(0, l_order.bestellart , "-") , ";")
                s_list.fdate1 = date_mdy(entry(3, entry(0, l_order.bestellart , "-") , ";"))
                s_list.tdate1 = date_mdy(entry(4, entry(0, l_order.bestellart , "-") , ";"))
                s_list.supp2 = to_int(entry(0, entry(1, l_order.bestellart , "-") , ";"))
                s_list.du_price2 = decimal.Decimal(entry(1, entry(1, l_order.bestellart , "-") , ";")) / 100
                s_list.curr2 = entry(2, entry(1, l_order.bestellart , "-") , ";")
                s_list.fdate2 = date_mdy(entry(3, entry(1, l_order.bestellart , "-") , ";"))
                s_list.tdate2 = date_mdy(entry(4, entry(1, l_order.bestellart , "-") , ";"))
                s_list.supp3 = to_int(entry(0, entry(2, l_order.bestellart , "-") , ";"))
                s_list.du_price3 = decimal.Decimal(entry(1, entry(2, l_order.bestellart , "-") , ";")) / 100
                s_list.curr1 = entry(2, entry(2, l_order.bestellart , "-") , ";")
                s_list.fdate1 = date_mdy(entry(3, entry(2, l_order.bestellart , "-") , ";"))
                s_list.tdate1 = date_mdy(entry(4, entry(2, l_order.bestellart , "-") , ";"))

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == s_list.supp1)).first()

            if l_lieferant:
                s_list.suppn1 = l_lieferant.firma

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == s_list.supp2)).first()

            if l_lieferant:
                s_list.suppn2 = l_lieferant.firma

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == s_list.supp3)).first()

            if l_lieferant:
                s_list.suppn3 = l_lieferant.firma

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == s_list.angebot_lief[1])).first()

            if l_lieferant:
                s_list.supps = l_lieferant.firma

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_order.stornogrund)).first()

            if gl_acct:
                s_list.desc_coa = gl_acct.bezeich

            l_pprice_obj_list = []
            for l_pprice, l_lieferant in db_session.query(L_pprice, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_pprice.lief_nr)).filter(
                    (L_pprice.artnr == l_artikel.artnr)).all():
                if l_pprice._recid in l_pprice_obj_list:
                    continue
                else:
                    l_pprice_obj_list.append(l_pprice._recid)


                s_list.last_pdate = l_pprice.bestelldatum
                s_list.last_pbook = l_pprice.einzelpreis
                s_list.a_firma = l_lieferant.firma


                break

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == l_order.lief_nr)).first()

            if l_lieferant:
                s_list.supplier = l_lieferant.firma

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr == l_artikel.artnr) &  (L_bestand.lager_nr == 0)).first()

            if l_bestand:
                s_list.soh = l_bestand.anz_anf_best + l_bestand.anz_eingang -\
                        l_bestand.anz_ausgang

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == l_order.angebot_lief[2])).first()

            if waehrung:
                s_list.curr = waehrung.wabkurz
                s_list.exrate = waehrung.ankauf / waehrung.einheit

            if waehrung:
                local_curr = to_int(s_list.angebot_lief[2])

                if local_curr != 1:
                    s_list.exrate = waehrung.ankauf / waehrung.einheit


            tot = 0

            s_list = query(s_list_list, first=True)
            while None != s_list:

                if s_list.curr == "" or s_list.curr == " ":
                    s_list.curr = def_curr
                tot = tot + s_list.amount

                s_list = query(s_list_list, next=True)

                s_list = query(s_list_list, current=True)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 386)).first()
    hierarchie = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    def_curr = htparam.fchar

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()
    comments = l_orderhdr.lief_fax[2]
    deptnr = l_orderhdr.angebot_lief[0]
    lieferdatum = l_orderhdr.lieferdatum
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_list.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    parameters = db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == deptnr)).first()

    if parameters:
        deptname = parameters.vstring
    reload_s_list()

    for l_artikel in db_session.query(L_artikel).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.rec_id = l_artikel._recid
        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.traubensort = l_artikel.traubensorte
        t_l_artikel.lief_einheit = l_artikel.lief_einheit
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.jahrgang = l_artikel.jahrgang

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name")).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring

    for waehrung in db_session.query(Waehrung).all():
        t_waehrung = T_waehrung()
        t_waehrung_list.append(t_waehrung)

        buffer_copy(waehrung, t_waehrung)

    return generate_output()