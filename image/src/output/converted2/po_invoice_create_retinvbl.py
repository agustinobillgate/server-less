#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_artikel, L_bestand, L_kredit, L_liefumsatz

def po_invoice_create_retinvbl(pvilanguage:int, tot_amt:Decimal, tot_disc:Decimal, tot_disc2:Decimal, tot_vat:Decimal, tot_val:Decimal, qty:Decimal, brutto:Decimal, s_list_s_recid:int, f_endkum:int, b_endkum:int, m_endkum:int, fb_closedate:date, m_closedate:date, bediener_nr:int):

    prepare_cache ([L_op, L_artikel, L_bestand, L_kredit, L_liefumsatz])

    msg_str = ""
    s_list_list = []
    lvcarea:string = "po-invoice"
    l_op = l_artikel = l_bestand = l_kredit = l_liefumsatz = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":string, "einzelpreis":Decimal, "price0":Decimal, "anzahl":Decimal, "anz0":Decimal, "brutto":Decimal, "val0":Decimal, "disc":Decimal, "disc0":Decimal, "disc2":Decimal, "disc20":Decimal, "disc_amt":Decimal, "disc2_amt":Decimal, "vat":Decimal, "warenwert":Decimal, "vat0":Decimal, "vat_amt":Decimal, "betriebsnr":int}, {"price0": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, s_list_list, lvcarea, l_op, l_artikel, l_bestand, l_kredit, l_liefumsatz
        nonlocal pvilanguage, tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, qty, brutto, s_list_s_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, bediener_nr


        nonlocal s_list
        nonlocal s_list_list

        return {"tot_amt": tot_amt, "tot_disc": tot_disc, "tot_disc2": tot_disc2, "tot_vat": tot_vat, "tot_val": tot_val, "msg_str": msg_str, "s-list": s_list_list}

    def create_retinv():

        nonlocal msg_str, s_list_list, lvcarea, l_op, l_artikel, l_bestand, l_kredit, l_liefumsatz
        nonlocal pvilanguage, tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, qty, brutto, s_list_s_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, bediener_nr


        nonlocal s_list
        nonlocal s_list_list

        netto:Decimal = to_decimal("0.0")
        l_op1 = None
        L_op1 =  create_buffer("L_op1",L_op)

        l_op1 = get_cache (L_op, {"_recid": [(eq, s_list_s_recid)]})

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op1.artnr)]})
        netto =  to_decimal(brutto) / to_decimal((1) + to_decimal(l_op1.deci1[1]) * to_decimal(0.01))
        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = l_op1.datum
        l_op.lager_nr = l_op1.lager_nr
        l_op.artnr = l_op1.artnr
        l_op.lief_nr = l_op1.lief_nr
        l_op.zeit = l_op1.zeit
        l_op.anzahl =  to_decimal(qty)
        l_op.einzelpreis =  to_decimal(l_op1.einzelpreis)
        l_op.warenwert =  to_decimal(netto)
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


        pass
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.artnr = l_op.artnr
        s_list.datum = l_op.datum
        s_list.bezeich = l_artikel.bezeich
        s_list.anzahl =  to_decimal(l_op.anzahl)
        s_list.anz0 =  to_decimal(l_op.anzahl)
        s_list.einzelpreis =  to_decimal(l_op.deci1[0])
        s_list.price0 =  to_decimal(l_op.deci1[0])
        s_list.brutto =  to_decimal(brutto)
        s_list.warenwert =  to_decimal(l_op.warenwert)
        s_list.val0 =  to_decimal(l_op.warenwert)
        s_list.disc =  to_decimal(l_op.deci1[1])
        s_list.disc0 =  to_decimal(l_op.deci1[1])
        s_list.disc2 =  to_decimal(l_op.rueckgabegrund) / to_decimal("100")
        s_list.disc20 =  to_decimal(l_op.rueckgabegrund) / to_decimal("100")
        s_list.disc_amt =  to_decimal(brutto) * to_decimal(l_op.deci1[1]) * to_decimal(0.01)
        s_list.vat =  to_decimal(l_op.deci1[2])
        s_list.vat0 =  to_decimal(l_op.deci1[2])
        s_list.vat_amt =  to_decimal(s_list.warenwert) * to_decimal(s_list.vat) * to_decimal(0.01)
        s_list.betriebsnr = l_op.betriebsnr
        s_list.s_recid = l_op._recid

        if l_op.flag:

            l_op1 = db_session.query(L_op1).filter(
                     (L_op1.artnr == l_op.artnr) & (L_op1.datum == l_op.datum) & (L_op1.lscheinnr == l_op.lscheinnr) & (L_op1.op_art == 3) & (L_op1.flag) & (L_op1.lief_nr == l_op.lief_nr)).first()

            if l_op1:
                l_op1.warenwert =  to_decimal(l_op1.warenwert) + to_decimal(l_op.warenwert)
                pass
        else:
            reorg_oh1()
        tot_amt =  to_decimal(tot_amt) + to_decimal(brutto)
        tot_disc =  to_decimal(tot_disc) + to_decimal(s_list.disc_amt)
        tot_disc2 =  to_decimal(tot_disc2) + to_decimal(s_list.disc2_amt)
        tot_vat =  to_decimal(tot_vat) + to_decimal(s_list.vat_amt)
        tot_val =  to_decimal(tot_amt) - to_decimal(tot_disc) - to_decimal(tot_disc2) + to_decimal(tot_vat)


    def reorg_oh1():

        nonlocal msg_str, s_list_list, lvcarea, l_op, l_artikel, l_bestand, l_kredit, l_liefumsatz
        nonlocal pvilanguage, tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, qty, brutto, s_list_s_recid, f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, bediener_nr


        nonlocal s_list
        nonlocal s_list_list

        oh_anz:Decimal = to_decimal("0.0")
        oh_wert:Decimal = to_decimal("0.0")
        l_art = None
        L_art =  create_buffer("L_art",L_artikel)

        l_art = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

        if (l_art.endkum == f_endkum or l_art.endkum == b_endkum) and l_op.datum > fb_closedate:

            return

        elif l_art.endkum >= m_endkum and l_op.datum > m_closedate:

            return

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, l_op.artnr)]})

        if l_bestand:
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(l_op.warenwert)
            oh_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
            oh_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
            pass
            l_art.vk_preis =  to_decimal(oh_wert) / to_decimal(oh_anz)
            pass

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_op.lager_nr)],"artnr": [(eq, l_op.artnr)]})

        if l_bestand:
            l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) + to_decimal(l_op.warenwert)
            oh_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if oh_anz < 0:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Onhand becomes negative", lvcarea, "") + " " + to_string(l_art.artnr) + ": " + to_string(oh_anz)

        l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, l_op.lief_nr)],"name": [(eq, l_op.docu_nr)],"lscheinnr": [(eq, l_op.lscheinnr)],"opart": [(eq, 0)],"zahlkonto": [(eq, 0)]})

        if l_kredit:
            l_kredit.saldo =  to_decimal(l_kredit.saldo) + to_decimal(l_op.warenwert)
            l_kredit.netto =  to_decimal(l_kredit.netto) + to_decimal(l_op.warenwert)
            pass

        l_liefumsatz = get_cache (L_liefumsatz, {"lief_nr": [(eq, l_op.lief_nr)],"datum": [(eq, l_op.datum)]})

        if l_liefumsatz:
            l_liefumsatz.gesamtumsatz =  to_decimal(l_liefumsatz.gesamtumsatz) + to_decimal(l_op.warenwert)
            pass

    create_retinv()

    return generate_output()