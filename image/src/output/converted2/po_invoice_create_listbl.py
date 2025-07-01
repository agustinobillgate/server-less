#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_op

def po_invoice_create_listbl(lscheinnr:string):

    prepare_cache ([L_artikel, L_op])

    tot_amt = to_decimal("0.0")
    tot_disc = to_decimal("0.0")
    tot_disc2 = to_decimal("0.0")
    tot_vat = to_decimal("0.0")
    tot_val = to_decimal("0.0")
    confirm_flag = True
    s_list_list = []
    l_artikel = l_op = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":string, "einzelpreis":Decimal, "price0":Decimal, "anzahl":Decimal, "anz0":Decimal, "brutto":Decimal, "val0":Decimal, "disc":Decimal, "disc0":Decimal, "disc2":Decimal, "disc20":Decimal, "disc_amt":Decimal, "disc2_amt":Decimal, "vat":Decimal, "warenwert":Decimal, "vat0":Decimal, "vat_amt":Decimal, "betriebsnr":int}, {"price0": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, s_list_list, l_artikel, l_op
        nonlocal lscheinnr


        nonlocal s_list
        nonlocal s_list_list

        return {"tot_amt": tot_amt, "tot_disc": tot_disc, "tot_disc2": tot_disc2, "tot_vat": tot_vat, "tot_val": tot_val, "confirm_flag": confirm_flag, "s-list": s_list_list}

    def create_list():

        nonlocal tot_amt, tot_disc, tot_disc2, tot_vat, tot_val, confirm_flag, s_list_list, l_artikel, l_op
        nonlocal lscheinnr


        nonlocal s_list
        nonlocal s_list_list


        tot_amt =  to_decimal("0")
        tot_vat =  to_decimal("0")
        tot_disc =  to_decimal("0")
        tot_disc2 =  to_decimal("0")


        s_list_list.clear()

        l_op_obj_list = {}
        l_op = L_op()
        l_artikel = L_artikel()
        for l_op.betriebsnr, l_op.artnr, l_op.datum, l_op.anzahl, l_op.deci1, l_op.rueckgabegrund, l_op.warenwert, l_op._recid, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.betriebsnr, L_op.artnr, L_op.datum, L_op.anzahl, L_op.deci1, L_op.rueckgabegrund, L_op.warenwert, L_op._recid, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                 (L_op.lief_nr == lief_nr) & (L_op.lscheinnr == (lscheinnr).lower()) & (L_op.op_art == 1) & (L_op.loeschflag <= 1)).order_by(L_artikel.bezeich, L_op.betriebsnr).all():
            if l_op_obj_list.get(l_op._recid):
                continue
            else:
                l_op_obj_list[l_op._recid] = True

            if l_op.betriebsnr == 0 or l_op.betriebsnr == 10:
                confirm_flag = False
            s_list = S_list()
            s_list_list.append(s_list)


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

    create_list()

    return generate_output()