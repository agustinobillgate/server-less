from functions.additional_functions import *
import decimal
from datetime import date
from models import L_op, L_artikel, L_bestand, L_kredit, L_liefumsatz

def po_invoice_create_retinvbl(pvilanguage:int, tot_amt:decimal, tot_disc:decimal, tot_disc2:decimal, tot_vat:decimal, tot_val:decimal, qty:decimal, brutto:decimal, s_list_s_recid:int, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, bediener_nr:int):
    msg_str = ""
    s_list_list = []
    lvcarea:str = "po_invoice"
    l_op = l_artikel = l_bestand = l_kredit = l_liefumsatz = None

    s_list = l_op1 = l_art = None

    s_list_list, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":str, "einzelpreis":decimal, "price0":decimal, "anzahl":decimal, "anz0":decimal, "brutto":decimal, "val0":decimal, "disc":decimal, "disc0":decimal, "disc2":decimal, "disc20":decimal, "disc_amt":decimal, "disc2_amt":decimal, "vat":decimal, "warenwert":decimal, "vat0":decimal, "vat_amt":decimal, "betriebsnr":int}, {"price0": None})

    L_op1 = L_op
    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, s_list_list, lvcarea, l_op, l_artikel, l_bestand, l_kredit, l_liefumsatz
        nonlocal l_op1, l_art


        nonlocal s_list, l_op1, l_art
        nonlocal s_list_list
        return {"msg_str": msg_str, "s-list": s_list_list}

    def create_retinv():

        nonlocal msg_str, s_list_list, lvcarea, l_op, l_artikel, l_bestand, l_kredit, l_liefumsatz
        nonlocal l_op1, l_art


        nonlocal s_list, l_op1, l_art
        nonlocal s_list_list

        netto:decimal = 0
        L_op1 = L_op

        l_op1 = db_session.query(L_op1).filter(
                (L_op1._recid == s_list_s_recid)).first()

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_op1.artnr)).first()
        netto = brutto / (1 + l_op1.deci1[1] * 0.01)
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = l_op1.datum
        l_op.lager_nr = l_op1.lager_nr
        l_op.artnr = l_op1.artnr
        l_op.lief_nr = l_op1.lief_nr
        l_op.zeit = l_op1.zeit
        l_op.anzahl = qty
        l_op.einzelpreis = l_op1.einzelpreis
        l_op.warenwert = netto
        l_op.deci1[0] = l_op1.deci1[0]
        l_op.deci1[1] = l_op1.deci1[1]
        l_op.deci1[2] = l_op1.deci1[2]
        l_op.deci1[3] = l_op.warenwert * l_op.deci1[2] * 0.01
        l_op.op_art = 1
        l_op.herkunftflag = l_op1.herkunftflag
        l_op.docu_nr = l_op1.docu_nr
        l_op.lscheinnr = l_op1.lscheinnr
        l_op.pos = l_op1.pos
        l_op.flag = l_op1.flag
        l_op.fuellflag = bediener_nr
        l_op.betriebsnr = l_op1.betriebsnr + 10

        l_op = db_session.query(L_op).first()
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.artnr = l_op.artnr
        s_list.datum = l_op.datum
        s_list.bezeich = l_artikel.bezeich
        s_list.anzahl = l_op.anzahl
        s_list.anz0 = l_op.anzahl
        s_list.einzelpreis = l_op.deci1[0]
        s_list.price0 = l_op.deci1[0]
        s_list.brutto = brutto
        s_list.warenwert = l_op.warenwert
        s_list.val0 = l_op.warenwert
        s_list.disc = l_op.deci1[1]
        s_list.disc0 = l_op.deci1[1]
        s_list.disc2 = l_op.rueckgabegrund / 100
        s_list.disc20 = l_op.rueckgabegrund / 100
        s_list.disc_amt = brutto * l_op.deci1[1] * 0.01
        s_list.vat = l_op.deci1[2]
        s_list.vat0 = l_op.deci1[2]
        s_list.vat_amt = s_list.warenwert * s_list.vat * 0.01
        s_list.betriebsnr = l_op.betriebsnr
        s_list.s_recid = l_op._recid

        if l_op.flag:

            l_op1 = db_session.query(L_op1).filter(
                    (L_op1.artnr == l_op.artnr) &  (L_op1.datum == l_op.datum) &  (L_op1.lscheinnr == l_op.lscheinnr) &  (L_op1.op_art == 3) &  (L_op1.flag) &  (L_op1.lief_nr == l_op.lief_nr)).first()

            if l_op1:
                l_op1.warenwert = l_op1.warenwert + l_op.warenwert

                l_op1 = db_session.query(L_op1).first()
        else:
            reorg_oh1()
        tot_amt = tot_amt + brutto
        tot_disc = tot_disc + s_list.disc_amt
        tot_disc2 = tot_disc2 + s_list.disc2_amt
        tot_vat = tot_vat + s_list.vat_amt
        tot_val = tot_amt - tot_disc - tot_disc2 + tot_vat

    def reorg_oh1():

        nonlocal msg_str, s_list_list, lvcarea, l_op, l_artikel, l_bestand, l_kredit, l_liefumsatz
        nonlocal l_op1, l_art


        nonlocal s_list, l_op1, l_art
        nonlocal s_list_list

        oh_anz:decimal = 0
        oh_wert:decimal = 0
        L_art = L_artikel

        l_art = db_session.query(L_art).filter(
                (L_art.artnr == l_op.artnr)).first()

        if (l_art.endkum == f_endkum or l_art.endkum == b_endkum) and l_op.datum > fb_closedate:

            return

        elif l_art.endkum >= m_endkum and l_op.datum > m_closedate:

            return

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == 0) &  (L_bestand.artnr == l_op.artnr)).first()

        if l_bestand:
            l_bestand.wert_eingang = l_bestand.wert_eingang + l_op.warenwert
            oh_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
            oh_wert = l_bestand.val_anf_best + l_bestand.wert_eingang - l_bestand.wert_ausgang

            l_art = db_session.query(L_art).first()
            l_art.vk_preis = oh_wert / oh_anz

            l_art = db_session.query(L_art).first()

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.lager_nr == l_op.lager_nr) &  (L_bestand.artnr == l_op.artnr)).first()

        if l_bestand:
            l_bestand.wert_eingang = l_bestand.wert_eingang + l_op.warenwert
            oh_anz = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

            if oh_anz < 0:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("Onhand becomes negative", lvcarea, "") + " " + to_string(l_art.artnr) + ": " + to_string(oh_anz)

        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit.lief_nr == l_op.lief_nr) &  (L_kredit.name == l_op.docu_nr) &  (L_kredit.lscheinnr == l_op.lscheinnr) &  (L_kredit.opart == 0) &  (L_kredit.zahlkonto == 0)).first()

        if l_kredit:
            l_kredit.saldo = l_kredit.saldo + l_op.warenwert
            l_kredit.netto = l_kredit.netto + l_op.warenwert

            l_kredit = db_session.query(L_kredit).first()

        l_liefumsatz = db_session.query(L_liefumsatz).filter(
                (L_liefumsatz.lief_nr == l_op.lief_nr) &  (L_liefumsatz.datum == l_op.datum)).first()

        if l_liefumsatz:
            l_liefumsatz.gesamtumsatz = l_liefumsatz.gesamtumsatz + l_op.warenwert

            l_liefumsatz = db_session.query(L_liefumsatz).first()


    create_retinv()

    return generate_output()