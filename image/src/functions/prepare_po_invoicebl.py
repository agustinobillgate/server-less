from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from functions.htplogic import htplogic
from sqlalchemy import func
from models import L_lieferant, Htparam, L_artikel, L_op

def prepare_po_invoicebl(pvilanguage:int, lief_nr:int, lscheinnr:str):
    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    fb_closedate = None
    m_closedate = None
    b1_tittle = ""
    tot_amt = 0
    tot_disc = 0
    tot_disc2 = 0
    tot_vat = 0
    tot_val = 0
    confirm_flag = False
    price_decimal = 0
    long_digit = False
    p_269 = None
    l_lieferant_firma = ""
    s_list_list = []
    lvcarea:str = "po_invoice"
    l_lieferant = htparam = l_artikel = l_op = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":str, "einzelpreis":decimal, "price0":decimal, "anzahl":decimal, "anz0":decimal, "brutto":decimal, "val0":decimal, "disc":decimal, "disc0":decimal, "disc2":decimal, "disc20":decimal, "disc_amt":decimal, "disc2_amt":decimal, "vat":decimal, "warenwert":decimal, "vat0":decimal, "vat_amt":decimal, "betriebsnr":int}, {"price0": None})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, b1_tittle, tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, price_decimal, long_digit, p_269, l_lieferant_firma, s_list_list, lvcarea, l_lieferant, htparam, l_artikel, l_op


        nonlocal s_list
        nonlocal s_list_list
        return {"f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "b1_tittle": b1_tittle, "tot_amt": tot_amt, "tot_disc": tot_disc, "tot_disc2": tot_disc2, "tot_vat": tot_vat, "tot_val": tot_val, "confirm_flag": confirm_flag, "price_decimal": price_decimal, "long_digit": long_digit, "p_269": p_269, "l_lieferant_firma": l_lieferant_firma, "s-list": s_list_list}

    def create_list():

        nonlocal f_endkum, b_endkum, m_endkum, fb_closedate, m_closedate, b1_tittle, tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, price_decimal, long_digit, p_269, l_lieferant_firma, s_list_list, lvcarea, l_lieferant, htparam, l_artikel, l_op


        nonlocal s_list
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


    p_269 = get_output(htpdate(269))
    price_decimal = get_output(htpint(491))
    long_digit = get_output(htplogic(246))

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()
    l_lieferant_firma = l_lieferant.firma

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    f_endkum = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    b_endkum = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 268)).first()
    m_endkum = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    fb_closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    m_closedate = htparam.fdate
    b1_tittle = translateExtended ("Stocks Incoming List -", lvcarea, "") + " " + l_lieferant.firma + " / " + lscheinnr
    create_list()

    return generate_output()