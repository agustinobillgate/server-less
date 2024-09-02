from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_artikel, L_pprice, Htparam, L_kredit, L_liefumsatz, L_bestand

def po_invoice_btn_gobl(pvilanguage:int, s_list:[S_list], f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, lscheinnr:str):
    tot_amt = 0
    tot_disc = 0
    tot_disc2 = 0
    tot_vat = 0
    tot_val = 0
    confirm_flag = False
    msg_str = ""
    msg_str2 = ""
    lvcarea:str = "po_invoice"
    l_op = l_artikel = l_pprice = htparam = l_kredit = l_liefumsatz = l_bestand = None

    s_list = l_op1 = l_art = None

    s_list_list, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":str, "einzelpreis":decimal, "price0":decimal, "anzahl":decimal, "anz0":decimal, "brutto":decimal, "val0":decimal, "disc":decimal, "disc0":decimal, "disc2":decimal, "disc20":decimal, "disc_amt":decimal, "disc2_amt":decimal, "vat":decimal, "warenwert":decimal, "vat0":decimal, "vat_amt":decimal, "betriebsnr":int}, {"price0": None})

    L_op1 = L_op
    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, msg_str, msg_str2, lvcarea, l_op, l_artikel, l_pprice, htparam, l_kredit, l_liefumsatz, l_bestand
        nonlocal l_op1, l_art


        nonlocal s_list, l_op1, l_art
        nonlocal s_list_list
        return {"tot_amt": tot_amt, "tot_disc": tot_disc, "tot_disc2": tot_disc2, "tot_vat": tot_vat, "tot_val": tot_val, "confirm_flag": confirm_flag, "msg_str": msg_str, "msg_str2": msg_str2}

    def do_adjustment():

        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, msg_str, msg_str2, lvcarea, l_op, l_artikel, l_pprice, htparam, l_kredit, l_liefumsatz, l_bestand
        nonlocal l_op1, l_art


        nonlocal s_list, l_op1, l_art
        nonlocal s_list_list


        L_op1 = L_op
        tot_amt = 0
        tot_vat = 0
        tot_disc = 0
        tot_disc2 = 0

        for s_list in query(s_list_list):

            if (s_list.anzahl != s_list.anz0) or (s_list.einzelpreis != s_list.price0) or (s_list.disc != s_list.disc0) or (s_list.disc2 != s_list.disc20) or (s_list.vat != s_list.vat0):

                l_op = db_session.query(L_op).filter(
                        (L_op._recid == s_list.s_recid)).first()
                l_op.anzahl = s_list.anzahl
                l_op.deci1[0] = s_list.einzelpreis
                l_op.deci1[1] = s_list.disc
                l_op.deci1[2] = s_list.vat
                l_op.rueckgabegrund = s_list.disc2 * 100
                l_op.einzelpreis = s_list.einzelpreis * (1 - s_list.disc * 0.01) *\
                        (1 - s_list.disc2 * 0.01)
                l_op.warenwert = s_list.warenwert
                l_op.deci1[3] = l_op.warenwert * l_op.deci1[2] * 0.01

                l_op = db_session.query(L_op).first()

                if l_op.flag:

                    l_op1 = db_session.query(L_op1).filter(
                            (L_op1.artnr == l_op.artnr) &  (L_op1.datum == l_op.datum) &  (L_op1.lscheinnr == l_op.lscheinnr) &  (L_op1.op_art == 3) &  (L_op1.flag) &  (L_op1.lief_nr == l_op.lief_nr)).first()

                    if l_op1:

                        if l_op.betriebsnr <= 1:
                            l_op1.warenwert = l_op.warenwert
                        else:
                            l_op1.warenwert = l_op1.warenwert + l_op.warenwert

                        l_op1 = db_session.query(L_op1).first()
                reorg_oh(l_op.flag)

        for s_list in query(s_list_list):
            s_list.anz0 = s_list.anzahl
            s_list.price0 = s_list.einzelpreis
            s_list.disc0 = s_list.disc
            s_list.disc20 = s_list.disc2
            s_list.vat0 = s_list.vat
            s_list.val0 = s_list.warenwert

    def create_list():

        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, msg_str, msg_str2, lvcarea, l_op, l_artikel, l_pprice, htparam, l_kredit, l_liefumsatz, l_bestand
        nonlocal l_op1, l_art


        nonlocal s_list, l_op1, l_art
        nonlocal s_list_list


        tot_amt = 0
        tot_vat = 0
        tot_disc = 0
        tot_disc2 = 0


        s_list_list.clear()

        l_op_obj_list = []
        for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                (L_op.lief_nr == lief_nr) &  (func.lower(L_op.(lscheinnr).lower()) == (lscheinnr).lower()) &  (L_op.op_art == 1) &  (L_op.loeschflag <= 1)).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)

            l_pprice = db_session.query(L_pprice).filter(
                    (L_pprice.artnr == l_op.artnr) &  (L_pprice.bestelldatum == l_op.datum) &  (L_pprice.lief_nr == l_op.lief_nr) &  (L_pprice.docu_nr == l_op.docu_nr)).first()

            if l_pprice:

                l_pprice = db_session.query(L_pprice).first()
                l_pprice.anzahl = l_op.anzahl
                l_pprice.einzelpreis = l_op.einzelpreis
                l_pprice.warenwert = l_op.warenwert

                l_pprice = db_session.query(L_pprice).first()


            if l_op.betriebsnr == 0 or l_op.betriebsnr == 10:
                confirm_flag = False
            s_list = S_list()
            s_list_list.append(s_list)


            if l_op.betriebsnr <= 1:
                s_list.artnr = l_op.artnr
                s_list.datum = l_op.datum
                s_list.bezeich = l_artikel.bezeich
                s_list.anzahl = l_op.anzahl
                s_list.anz0 = l_op.anzahl
                s_list.einzelpreis = l_op.deci1[0]
                s_list.price0 = l_op.deci1[0]
                s_list.disc = l_op.deci1[1]
                s_list.disc0 = l_op.deci1[1]
                s_list.disc2 = l_op.rueckgabegrund / 100
                s_list.disc20 = l_op.rueckgabegrund / 100
                s_list.brutto = l_op.warenwert / (1 - s_list.disc * 0.01) /\
                        (1 - s_list.disc2 * 0.01)
                s_list.warenwert = l_op.warenwert
                s_list.val0 = l_op.warenwert
                s_list.disc_amt = l_op.deci1[0] * l_op.anzahl * l_op.deci1[1] * 0.01
                s_list.disc2_amt = l_op.deci1[0] * l_op.anzahl *\
                        (1 - s_list.disc * 0.01) * s_list.disc2 * 0.01
                s_list.vat = l_op.deci1[2]
                s_list.vat0 = l_op.deci1[2]
                s_list.vat_amt = s_list.warenwert * s_list.vat * 0.01
                s_list.betriebsnr = l_op.betriebsnr
                s_list.s_recid = l_op._recid


                tot_amt = tot_amt + s_list.brutto
                tot_disc = tot_disc + s_list.disc_amt
                tot_disc2 = tot_disc2 + s_list.disc2_amt
                tot_vat = tot_vat + s_list.vat_amt
            else:
                s_list.artnr = l_op.artnr
                s_list.datum = l_op.datum
                s_list.bezeich = l_artikel.bezeich
                s_list.anzahl = l_op.anzahl
                s_list.einzelpreis = l_op.deci1[0]
                s_list.price0 = l_op.deci1[0]
                s_list.disc = l_op.deci1[1]
                s_list.disc0 = l_op.deci1[1]
                s_list.disc2 = l_op.rueckgabegrund / 100
                s_list.disc20 = l_op.rueckgabegrund / 100
                s_list.brutto = l_op.warenwert / (1 - s_list.disc * 0.01) /\
                        (1 - s_list.disc2 * 0.01)
                s_list.warenwert = l_op.warenwert
                s_list.val0 = l_op.warenwert
                s_list.disc_amt = s_list.brutto * l_op.deci1[1] * 0.01
                s_list.disc2_amt = s_list.brutto * (1 - s_list.disc * 0.01) *\
                        s_list.disc2 * 0.01
                s_list.vat = l_op.deci1[2]
                s_list.vat0 = l_op.deci1[2]
                s_list.vat_amt = l_op.warenwert * l_op.deci[2] * 0.01
                s_list.betriebsnr = l_op.betriebsnr
                s_list.s_recid = l_op._recid


                tot_amt = tot_amt + s_list.brutto
                tot_disc = tot_disc + s_list.disc_amt
                tot_disc2 = tot_disc2 + s_list.disc2_amt
                tot_vat = tot_vat + s_list.vat_amt
        tot_val = tot_amt - tot_disc - tot_disc2 + tot_vat

    def reorg_oh(direct_issue:bool):

        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, msg_str, msg_str2, lvcarea, l_op, l_artikel, l_pprice, htparam, l_kredit, l_liefumsatz, l_bestand
        nonlocal l_op1, l_art


        nonlocal s_list, l_op1, l_art
        nonlocal s_list_list

        oh_anz:decimal = 0
        oh_wert:decimal = 0
        L_art = L_artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1016)).first()

        if htparam.flogical:

            l_kredit = db_session.query(L_kredit).filter(
                    (L_kredit.lief_nr == l_op.lief_nr) &  (L_kredit.name == l_op.docu_nr) &  (L_kredit.lscheinnr == l_op.lscheinnr) &  (L_kredit.opart == 0) &  (L_kredit.zahlkonto == 0)).first()

            if l_kredit:
                l_kredit.saldo = l_kredit.saldo - s_list.val0 + s_list.warenwert
                l_kredit.netto = l_kredit.netto - s_list.val0 + s_list.warenwert

                l_kredit = db_session.query(L_kredit).first()
            else:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("A/P record not found!", lvcarea, "")

        l_liefumsatz = db_session.query(L_liefumsatz).filter(
                (L_liefumsatz.lief_nr == l_op.lief_nr) &  (L_liefumsatz.datum == s_list.datum)).first()

        if l_liefumsatz:
            l_liefumsatz.gesamtumsatz = l_liefumsatz.gesamtumsatz - s_list.val0 + s_list.warenwert

            l_liefumsatz = db_session.query(L_liefumsatz).first()

        if direct_issue:

            return

        if (s_list.anzahl == s_list.anz0) and (s_list.einzelpreis == s_list.price0) and (s_list.disc == s_list.disc0) and (s_list.disc2 == s_list.disc20) and (s_list.val0 == s_list.warenwert):

            return

        l_art = db_session.query(L_art).filter(
                (L_art.artnr == s_list.artnr)).first()

        if (l_art.endkum == f_endkum or l_art.endkum == b_endkum) and s_list.datum > fb_closedate:

            return

        elif l_art.endkum >= m_endkum and s_list.datum > m_closedate:

            return

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  (L_bestand.artnr == l_op.artnr)).first()

        if l_bestand:
            l_bestand.anz_eingang = l_bestand.anz_eingang - s_list.anz0 + s_list.anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang - s_list.val0 + s_list.warenwert
            oh_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

            if oh_anz != 0:
                oh_wert = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

                l_art = db_session.query(L_art).first()
                l_art.vk_preis = oh_wert / oh_anz

                l_art = db_session.query(L_art).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == l_op.lager_nr) &  (L_bestand.artnr == l_op.artnr)).first()

        if l_bestand:
            l_bestand.anz_eingang = l_bestand.anz_eingang - s_list.anz0 + s_list.anzahl
            l_bestand.wert_eingang = l_bestand.wert_eingang - s_list.val0 + s_list.warenwert

            l_bestand = db_session.query(L_bestand).first()
            oh_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

            if oh_anz < 0:
                msg_str2 = msg_str2 + chr(2) + "&W" + translateExtended ("Onhand becomes negative", lvcarea, "") + " " + to_string(l_art.artnr) + ": " + to_string(oh_anz)


    do_adjustment()
    create_list()

    return generate_output()