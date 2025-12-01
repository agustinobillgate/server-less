#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Htparam, Brief, Waehrung, Hoteldpt, Artikel, Res_line

def prepare_fo_invoicebl(bil_flag:int):

    prepare_cache ([Bill, Htparam, Waehrung, Hoteldpt, Res_line])

    t_artikel_data = []
    t_foinv_data = []
    vat_artlist:List[int] = [0, 0, 0, 0]
    lvint1:int = 0
    curr_parent:int = 0
    bill = htparam = brief = waehrung = hoteldpt = artikel = res_line = None

    t_artikel = t_foinv = bbuff = None

    t_artikel_data, T_artikel = create_model("T_artikel", {"artnr":int, "bezeich":string, "epreis":Decimal, "departement":int, "artart":int, "activeflag":bool, "artgrp":int, "bezaendern":bool, "autosaldo":bool, "pricetab":bool, "betriebsnr":int, "resart":bool, "zwkum":int})
    t_foinv_data, T_foinv = create_model("T_foinv", {"vipnr1":int, "vipnr2":int, "vipnr3":int, "vipnr4":int, "vipnr5":int, "vipnr6":int, "vipnr7":int, "vipnr8":int, "vipnr9":int, "ext_char":string, "price_decimal":int, "double_currency":bool, "change_date":bool, "foreign_rate":bool, "exchg_rate":Decimal, "curr_local":string, "curr_foreign":string, "lvanzvat":int, "b_title":string, "artikel_str":string, "p_219":bool, "p_199":bool, "p_145":int, "p_242":int, "p_60":int, "p_251":bool, "p_2313":int, "p_1116":int, "p_685":int, "avail_brief685":bool, "p_173":string, "p_2314":int, "p_83":bool, "p_497":int, "p_120":int, "avail_brief497":bool, "p_1086":Decimal}, {"exchg_rate": 1})

    Bbuff = create_buffer("Bbuff",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_data, t_foinv_data, vat_artlist, lvint1, curr_parent, bill, htparam, brief, waehrung, hoteldpt, artikel, res_line
        nonlocal bil_flag
        nonlocal bbuff


        nonlocal t_artikel, t_foinv, bbuff
        nonlocal t_artikel_data, t_foinv_data

        return {"t-artikel": t_artikel_data, "t-foinv": t_foinv_data}

    t_foinv = T_foinv()
    t_foinv_data.append(t_foinv)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1086)]})
    p_1086 = htparam.fdecimal

    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})
    p_120 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 2314)]})
    p_2314 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 83)]})
    p_83 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 60)]})
    t_foinv.p_60 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 251)]})
    t_foinv.p_251 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 2313)]})
    t_foinv.p_2313 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1116)]})
    t_foinv.p_1116 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 685)]})
    t_foinv.p_685 = htparam.finteger

    brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

    if brief:
        avail_brief685 = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 497)]})
    t_foinv.p_497 = htparam.finteger

    brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

    if brief:
        avail_brief497 = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 173)]})
    t_foinv.p_173 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 219)]})
    t_foinv.p_219 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 199)]})
    t_foinv.p_199 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})
    t_foinv.p_145 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 242)]})
    t_foinv.p_242 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        t_foinv.vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        t_foinv.vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        t_foinv.vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        t_foinv.vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        t_foinv.vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        t_foinv.vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        t_foinv.vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        t_foinv.vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        t_foinv.vipnr9 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 148)]})
    t_foinv.ext_char = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 453)]})

    if htparam.feldtyp == 5 and htparam.fchar != "":
        t_foinv.ext_char = t_foinv.ext_char + ";" + htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    t_foinv.price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam:
        t_foinv.double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 219)]})
    t_foinv.change_date = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    t_foinv.foreign_rate = htparam.flogical

    if t_foinv.foreign_rate or t_foinv.double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            t_foinv.exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    t_foinv.curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
    t_foinv.curr_foreign = htparam.fchar
    t_foinv.lvanzvat = 0

    htparam = get_cache (Htparam, {"paramnr": [(eq, 132)]})

    if htparam.fchar != "":
        for lvint1 in range(1,num_entries(htparam.fchar, ";")  + 1) :

            if to_int(entry(lvint1 - 1, htparam.fchar, ";")) != 0:
                t_foinv.lvanzvat = t_foinv.lvanzvat + 1
                vat_artlist[t_foinv.lvanzvat - 1] = to_int(entry(lvint1 - 1, htparam.fchar, ";"))

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})

    if bil_flag == 0:
        t_foinv.b_title = hoteldpt.depart + " BILLS"

    elif bil_flag == 1:
        t_foinv.b_title = hoteldpt.depart + " CLOSED BILLS"
    t_foinv.artikel_str = "F/O Articles"

    for artikel in db_session.query(Artikel).filter(
             (Artikel.activeflag)).order_by(Artikel._recid).all():
        t_artikel = T_artikel()
        t_artikel_data.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    if bil_flag != 0:

        return generate_output()

    for bill in db_session.query(Bill).filter(
        (Bill.resnr > 0) & (Bill.reslinnr > 0) & (Bill.flag == 0)
    ).order_by(Bill.resnr).all():

        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

        if res_line and res_line.zinr != bill.zinr and res_line.active_flag == 1:

            bbuff = db_session.query(Bill).filter(Bill._recid == bill._recid).with_for_update().first()
            
            if bbuff:
                bbuff.zinr = res_line.zinr

    return generate_output()