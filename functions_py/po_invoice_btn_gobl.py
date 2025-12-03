#using conversion tools version: 1.0.0.117
"""_yusufwijasena_20/10/2025

    TicketID: 01EBC4
        _issue_:    - update from DZIKRI: 8F94DC
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_artikel, L_pprice, Htparam, L_kredit, L_liefumsatz, L_bestand
from sqlalchemy.orm.attributes import flag_modified

s_list_data, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":string, "einzelpreis":Decimal, "price0":Decimal, "anzahl":Decimal, "anz0":Decimal, "brutto":Decimal, "val0":Decimal, "disc":Decimal, "disc0":Decimal, "disc2":Decimal, "disc20":Decimal, "disc_amt":Decimal, "disc2_amt":Decimal, "vat":Decimal, "warenwert":Decimal, "vat0":Decimal, "vat_amt":Decimal, "betriebsnr":int}, {"price0": None})

def po_invoice_btn_gobl(pvilanguage:int, s_list_data:[S_list], f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, lscheinnr:string):

    prepare_cache ([L_op, L_artikel, L_pprice, L_kredit, L_liefumsatz, L_bestand])

    tot_amt = to_decimal("0.0")
    tot_disc = to_decimal("0.0")
    tot_disc2 = to_decimal("0.0")
    tot_vat = to_decimal("0.0")
    tot_val = to_decimal("0.0")
    confirm_flag = True
    msg_str = ""
    msg_str2 = ""
    lvcarea:string = "po-invoice"
    l_op = l_artikel = l_pprice = htparam = l_kredit = l_liefumsatz = l_bestand = None

    s_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, msg_str, msg_str2, lvcarea, l_op, l_artikel, l_pprice, htparam, l_kredit, l_liefumsatz, l_bestand
        nonlocal pvilanguage, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lscheinnr
        nonlocal s_list

        return {
            "s-list": s_list_data, 
            "tot_amt": tot_amt, 
            "tot_disc": tot_disc, 
            "tot_disc2": tot_disc2, 
            "tot_vat": tot_vat, 
            "tot_val": tot_val, 
            "confirm_flag": confirm_flag, 
            "msg_str": msg_str, 
            "msg_str2": msg_str2
        }

    def do_adjustment():
        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, msg_str, msg_str2, lvcarea, l_op, l_artikel, l_pprice, htparam, l_kredit, l_liefumsatz, l_bestand
        nonlocal pvilanguage, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lscheinnr
        nonlocal s_list

        l_op1 = None
        L_op1 =  create_buffer("L_op1",L_op)
        tot_amt =  to_decimal("0")
        tot_vat =  to_decimal("0")
        tot_disc =  to_decimal("0")
        tot_disc2 =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("bezeich",False),("betriebsnr",False)]):
            if (s_list.anzahl != s_list.anz0) or (s_list.einzelpreis != s_list.price0) or (s_list.disc != s_list.disc0) or (s_list.disc2 != s_list.disc20) or (s_list.vat != s_list.vat0):

                l_op = db_session.query(L_op).filter(L_op._recid == s_list.s_recid).with_for_update().first()

                l_op.anzahl =  to_decimal(s_list.anzahl)
                l_op.deci1[0] = s_list.einzelpreis
                l_op.deci1[1] = s_list.disc
                l_op.deci1[2] = s_list.vat
                l_op.rueckgabegrund = s_list.disc2 * 100
                l_op.einzelpreis =  to_decimal(s_list.einzelpreis) * to_decimal((1) - to_decimal(s_list.disc) * to_decimal(0.01)) * (1 - to_decimal(s_list.disc2) * to_decimal(0.01) )
                l_op.warenwert =  to_decimal(s_list.warenwert)
                l_op.deci1[3] = l_op.warenwert * l_op.deci1[2] * 0.01
                flag_modified(l_op, "deci1")

                if l_op.flag:
                    l_op1 = db_session.query(L_op1).filter(
                             (L_op1.artnr == l_op.artnr) & (L_op1.datum == l_op.datum) & (L_op1.lscheinnr == l_op.lscheinnr) & (L_op1.op_art == 3) & (L_op1.flag) & (L_op1.lief_nr == l_op.lief_nr)).with_for_update().first()

                    if l_op1:
                        l_op1.anzahl =  to_decimal(l_op.anzahl)
                        l_op1.einzelpreis =  to_decimal(l_op.einzelpreis) # DZIKRI: 8F94DC

                        if l_op.betriebsnr <= 1:
                            l_op1.warenwert =  to_decimal(l_op.warenwert)
                        else:
                            l_op1.warenwert =  to_decimal(l_op1.warenwert) + to_decimal(l_op.warenwert)

                l_artikel = db_session.query(L_artikel).filter(L_artikel.artnr == l_op.artnr).first()

                if l_artikel:

                    if (l_artikel.ek_aktuell != l_op.einzelpreis) and l_op.einzelpreis != 0:
                        db_session.refresh(l_artikel, with_for_update=True)

                        l_artikel.ek_letzter =  to_decimal(l_artikel.ek_aktuell)
                        l_artikel.ek_aktuell =  to_decimal(l_op.einzelpreis)

                        db_session.flush()
                        
                reorg_oh(l_op.flag)

        for s_list in query(s_list_data):
            s_list.anz0 =  to_decimal(s_list.anzahl)
            s_list.price0 =  to_decimal(s_list.einzelpreis)
            s_list.disc0 =  to_decimal(s_list.disc)
            s_list.disc20 =  to_decimal(s_list.disc2)
            s_list.vat0 =  to_decimal(s_list.vat)
            s_list.val0 =  to_decimal(s_list.warenwert)

    def create_list():
        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, msg_str, msg_str2, lvcarea, l_op, l_artikel, l_pprice, htparam, l_kredit, l_liefumsatz, l_bestand
        nonlocal pvilanguage, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lscheinnr


        nonlocal s_list


        tot_amt =  to_decimal("0")
        tot_vat =  to_decimal("0")
        tot_disc =  to_decimal("0")
        tot_disc2 =  to_decimal("0")


        s_list_data.clear()

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.warenwert, l_op.deci1, l_op.artnr, l_op.datum, l_op.lscheinnr, l_op.lief_nr, l_op.anzahl, l_op.einzelpreis, l_op.docu_nr, l_op.betriebsnr, l_op.rueckgabegrund, l_op._recid, l_op.lager_nr, l_artikel.ek_aktuell, l_artikel.bezeich, l_artikel.ek_letzter, l_artikel._recid, l_artikel.endkum, l_artikel.artnr, l_artikel.vk_preis in db_session.query(L_op.warenwert, L_op.deci1, L_op.artnr, L_op.datum, L_op.lscheinnr, L_op.lief_nr, L_op.anzahl, L_op.einzelpreis, L_op.docu_nr, L_op.betriebsnr, L_op.rueckgabegrund, L_op._recid, L_op.lager_nr, L_artikel.ek_aktuell, L_artikel.bezeich, L_artikel.ek_letzter, L_artikel._recid, L_artikel.endkum, L_artikel.artnr, L_artikel.vk_preis).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_op.lief_nr == lief_nr) & (L_op.lscheinnr == (lscheinnr).lower()) & (L_op.op_art == 1) & (L_op.loeschflag <= 1)).order_by(L_artikel.bezeich, L_op.betriebsnr).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            l_pprice = db_session.query(L_pprice).filter(
                     (L_pprice.artnr == l_op.artnr) & (L_pprice.bestelldatum == l_op.datum) & (L_pprice.lief_nr == l_op.lief_nr) & (L_pprice.docu_nr == l_op.docu_nr)).first()

            if l_pprice:
                db_session.refresh(l_pprice, with_for_update=True)

                l_pprice.anzahl =  to_decimal(l_op.anzahl)
                l_pprice.einzelpreis =  to_decimal(l_op.einzelpreis)
                l_pprice.warenwert =  to_decimal(l_op.warenwert)

                db_session.flush()

            if l_op.betriebsnr == 0 or l_op.betriebsnr == 10:
                confirm_flag = False
                
            s_list = S_list()
            s_list_data.append(s_list)


            if l_op.betriebsnr <= 1:
                s_list.artnr = l_op.artnr
                s_list.datum = l_op.datum
                s_list.bezeich = l_artikel.bezeich
                s_list.anzahl =  to_decimal(l_op.anzahl)
                s_list.anz0 =  to_decimal(l_op.anzahl)
                s_list.einzelpreis =  to_decimal(l_op.deci1[0])
                s_list.price0 =  to_decimal(l_op.deci1[0])
                s_list.disc =  to_decimal(l_op.deci1[1])
                s_list.disc0 =  to_decimal(l_op.deci1[1])
                s_list.disc2 =  to_decimal(l_op.rueckgabegrund) / to_decimal("100")
                s_list.disc20 =  to_decimal(l_op.rueckgabegrund) / to_decimal("100")
                s_list.brutto =  to_decimal(l_op.warenwert) / to_decimal((1) - to_decimal(s_list.disc) * to_decimal(0.01)) /\
                        (1 - to_decimal(s_list.disc2) * to_decimal(0.01) )
                s_list.warenwert =  to_decimal(l_op.warenwert)
                s_list.val0 =  to_decimal(l_op.warenwert)
                s_list.disc_amt =  to_decimal(l_op.deci1[0]) * to_decimal(l_op.anzahl) * to_decimal(l_op.deci1[1]) * to_decimal(0.01)
                s_list.disc2_amt =  to_decimal(l_op.deci1[0]) * to_decimal(l_op.anzahl) *\
                        (1 - to_decimal(s_list.disc) * to_decimal(0.01)) * to_decimal(s_list.disc2) * to_decimal(0.01)
                s_list.vat =  to_decimal(l_op.deci1[2])
                s_list.vat0 =  to_decimal(l_op.deci1[2])
                s_list.vat_amt =  to_decimal(s_list.warenwert) * to_decimal(s_list.vat) * to_decimal(0.01)
                s_list.betriebsnr = l_op.betriebsnr
                s_list.s_recid = l_op._recid

                tot_amt =  to_decimal(tot_amt) + to_decimal(s_list.brutto)
                tot_disc =  to_decimal(tot_disc) + to_decimal(s_list.disc_amt)
                tot_disc2 =  to_decimal(tot_disc2) + to_decimal(s_list.disc2_amt)
                tot_vat =  to_decimal(tot_vat) + to_decimal(s_list.vat_amt)
            else:
                s_list.artnr = l_op.artnr
                s_list.datum = l_op.datum
                s_list.bezeich = l_artikel.bezeich
                s_list.anzahl =  to_decimal(l_op.anzahl)
                s_list.einzelpreis =  to_decimal(l_op.deci1[0])
                s_list.price0 =  to_decimal(l_op.deci1[0])
                s_list.disc =  to_decimal(l_op.deci1[1])
                s_list.disc0 =  to_decimal(l_op.deci1[1])
                s_list.disc2 =  to_decimal(l_op.rueckgabegrund) / to_decimal("100")
                s_list.disc20 =  to_decimal(l_op.rueckgabegrund) / to_decimal("100")
                s_list.brutto =  to_decimal(l_op.warenwert) / to_decimal((1) - to_decimal(s_list.disc) * to_decimal(0.01)) /\
                        (1 - to_decimal(s_list.disc2) * to_decimal(0.01) )
                s_list.warenwert =  to_decimal(l_op.warenwert)
                s_list.val0 =  to_decimal(l_op.warenwert)
                s_list.disc_amt =  to_decimal(s_list.brutto) * to_decimal(l_op.deci1[1]) * to_decimal(0.01)
                s_list.disc2_amt =  to_decimal(s_list.brutto) * to_decimal((1) - to_decimal(s_list.disc) * to_decimal(0.01)) *\
                        s_list.disc2 * to_decimal(0.01)
                s_list.vat =  to_decimal(l_op.deci1[2])
                s_list.vat0 =  to_decimal(l_op.deci1[2])
                s_list.vat_amt =  to_decimal(l_op.warenwert) * to_decimal(l_op.deci[2]) * to_decimal(0.01)
                s_list.betriebsnr = l_op.betriebsnr
                s_list.s_recid = l_op._recid

                tot_amt =  to_decimal(tot_amt) + to_decimal(s_list.brutto)
                tot_disc =  to_decimal(tot_disc) + to_decimal(s_list.disc_amt)
                tot_disc2 =  to_decimal(tot_disc2) + to_decimal(s_list.disc2_amt)
                tot_vat =  to_decimal(tot_vat) + to_decimal(s_list.vat_amt)
        tot_val =  to_decimal(tot_amt) - to_decimal(tot_disc) - to_decimal(tot_disc2) + to_decimal(tot_vat)


    def reorg_oh(direct_issue:bool):
        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, msg_str, msg_str2, lvcarea, l_op, l_artikel, l_pprice, htparam, l_kredit, l_liefumsatz, l_bestand
        nonlocal pvilanguage, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, lscheinnr
        nonlocal s_list

        oh_anz:Decimal = to_decimal("0.0")
        oh_wert:Decimal = to_decimal("0.0")
        l_art = None
        L_art =  create_buffer("L_art",L_artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})

        if htparam.flogical:

            l_kredit = db_session.query(L_kredit).filter(
                     (L_kredit.lief_nr == l_op.lief_nr) & (L_kredit.name == l_op.docu_nr) & (L_kredit.lscheinnr == l_op.lscheinnr) & (L_kredit.opart <= 2) & (L_kredit.zahlkonto == 0)).first()

            if not l_kredit:

                l_kredit = db_session.query(L_kredit).filter(
                         (L_kredit.lief_nr == l_op.lief_nr) & (L_kredit.lscheinnr == l_op.lscheinnr) & (L_kredit.rgdatum == l_op.datum) & (L_kredit.opart <= 2) & (L_kredit.zahlkonto == 0)).first()

            if l_kredit:
                db_session.refresh(l_kredit, with_for_update=True)

                l_kredit.saldo =  to_decimal(l_kredit.saldo) - to_decimal(s_list.val0) + to_decimal(s_list.warenwert)
                l_kredit.netto =  to_decimal(l_kredit.netto) - to_decimal(s_list.val0) + to_decimal(s_list.warenwert)

                db_session.flush()
            else:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("A/P record not found!", lvcarea, "")

        l_liefumsatz = db_session.query(L_liefumsatz).filter(
                 (L_liefumsatz.lief_nr == l_op.lief_nr) & (L_liefumsatz.datum == s_list.datum)).with_for_update().first()

        if l_liefumsatz:
            l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) - to_decimal(s_list.val0) + to_decimal(s_list.warenwert)
            pass

        if direct_issue:
            return

        if (s_list.anzahl == s_list.anz0) and (s_list.einzelpreis == s_list.price0) and (s_list.disc == s_list.disc0) and (s_list.disc2 == s_list.disc20) and (s_list.val0 == s_list.warenwert):
            return
        
        l_art = db_session.query(L_art).filter(L_art.artnr == s_list.artnr).first()

        if (l_art.endkum == f_endkum or l_art.endkum == b_endkum) and s_list.datum > fb_closedate:
            return

        elif l_art.endkum >= m_endkum and s_list.datum > m_closedate:
            return

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == 0) & (L_bestand.artnr == l_op.artnr)).with_for_update().first()

        if l_bestand:
            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(s_list.anz0) + to_decimal(s_list.anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(s_list.val0) + to_decimal(s_list.warenwert)
            oh_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if oh_anz != 0:
                db_session.refresh(l_art, with_for_update=True)

                oh_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                l_art.vk_preis =  to_decimal(oh_wert) / to_decimal(oh_anz)

                db_session.flush()

        l_bestand = db_session.query(L_bestand).filter(
                 (L_bestand.lager_nr == l_op.lager_nr) & (L_bestand.artnr == l_op.artnr)).with_for_update().first()

        if l_bestand:
            l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(s_list.anz0) + to_decimal(s_list.anzahl)
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(s_list.val0) + to_decimal(s_list.warenwert)
            
            oh_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if oh_anz < 0:
                msg_str2 = msg_str2 + chr_unicode(2) + "&W" + translateExtended ("Onhand becomes negative", lvcarea, "") + " " + to_string(l_art.artnr) + ": " + to_string(oh_anz)

    do_adjustment()
    create_list()

    return generate_output()