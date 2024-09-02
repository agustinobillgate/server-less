from functions.additional_functions import *
import decimal
from models import Bill, Htparam, Brief, Waehrung, Hoteldpt, Artikel, Res_line

def prepare_fo_invoicebl(bil_flag:int):
    t_artikel_list = []
    t_foinv_list = []
    vat_artlist:[int] = [0, 0, 0, 0, 0]
    lvint1:int = 0
    curr_parent:int = 0
    bill = htparam = brief = waehrung = hoteldpt = artikel = res_line = None

    t_artikel = t_foinv = bbuff = None

    t_artikel_list, T_artikel = create_model("T_artikel", {"artnr":int, "bezeich":str, "epreis":decimal, "departement":int, "artart":int, "activeflag":bool, "artgrp":int, "bezaendern":bool, "autosaldo":bool, "pricetab":bool, "betriebsnr":int, "resart":bool, "zwkum":int})
    t_foinv_list, T_foinv = create_model("T_foinv", {"vipnr1":int, "vipnr2":int, "vipnr3":int, "vipnr4":int, "vipnr5":int, "vipnr6":int, "vipnr7":int, "vipnr8":int, "vipnr9":int, "ext_char":str, "price_decimal":int, "double_currency":bool, "change_date":bool, "foreign_rate":bool, "exchg_rate":decimal, "curr_local":str, "curr_foreign":str, "lvanzvat":int, "b_title":str, "artikel_str":str, "p_219":bool, "p_199":bool, "p_145":int, "p_242":int, "p_60":int, "p_251":bool, "p_2313":int, "p_1116":int, "p_685":int, "avail_brief685":bool, "p_173":str, "p_2314":int, "p_83":bool, "p_497":int, "p_120":int, "avail_brief497":bool, "p_1086":decimal}, {"exchg_rate": 1})

    Bbuff = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, t_foinv_list, vat_artlist, lvint1, curr_parent, bill, htparam, brief, waehrung, hoteldpt, artikel, res_line
        nonlocal bbuff


        nonlocal t_artikel, t_foinv, bbuff
        nonlocal t_artikel_list, t_foinv_list
        return {"t-artikel": t_artikel_list, "t-foinv": t_foinv_list}

    t_foinv = T_foinv()
    t_foinv_list.append(t_foinv)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1086)).first()
    p_1086 = htparam.fdecimal

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 120)).first()
    p_120 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2314)).first()
    p_2314 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 83)).first()
    p_83 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 60)).first()
    t_foinv.p_60 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 251)).first()
    t_foinv.p_251 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2313)).first()
    t_foinv.p_2313 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1116)).first()
    t_foinv.p_1116 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 685)).first()
    t_foinv.p_685 = htparam.finteger

    brief = db_session.query(Brief).filter(
            (Briefnr == htparam.finteger)).first()

    if brief:
        avail_brief685 = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 497)).first()
    t_foinv.p_497 = htparam.finteger

    brief = db_session.query(Brief).filter(
            (Briefnr == htparam.finteger)).first()

    if brief:
        avail_brief497 = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 173)).first()
    t_foinv.p_173 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 219)).first()
    t_foinv.p_219 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 199)).first()
    t_foinv.p_199 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 145)).first()
    t_foinv.p_145 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 242)).first()
    t_foinv.p_242 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 700)).first()

    if htparam.finteger != 0:
        t_foinv.vipnr1 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 701)).first()

    if htparam.finteger != 0:
        t_foinv.vipnr2 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 702)).first()

    if htparam.finteger != 0:
        t_foinv.vipnr3 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 703)).first()

    if htparam.finteger != 0:
        t_foinv.vipnr4 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 704)).first()

    if htparam.finteger != 0:
        t_foinv.vipnr5 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 705)).first()

    if htparam.finteger != 0:
        t_foinv.vipnr6 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 706)).first()

    if htparam.finteger != 0:
        t_foinv.vipnr7 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 707)).first()

    if htparam.finteger != 0:
        t_foinv.vipnr8 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 708)).first()

    if htparam.finteger != 0:
        t_foinv.vipnr9 = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 148)).first()
    t_foinv.ext_char = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 453)).first()

    if htparam.feldtyp == 5 and htparam.fchar != "":
        t_foinv.ext_char = t_foinv.ext_char + ";" + htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    t_foinv.price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam:
        t_foinv.double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 219)).first()
    t_foinv.change_date = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    t_foinv.foreign_rate = htparam.flogical

    if t_foinv.foreign_rate or t_foinv.double_currency:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            t_foinv.exchg_rate = waehrung.ankauf / waehrung.einheit

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    t_foinv.curr_local = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    t_foinv.curr_foreign = fchar
    t_foinv.lvAnzVat = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 132)).first()

    if htparam.fchar != "":
        for lvint1 in range(1,num_entries(htparam.fchar, ";")  + 1) :

            if to_int(entry(lvint1 - 1, htparam.fchar, ";")) != 0:
                t_foinv.lvAnzVat = t_foinv.lvAnzVat + 1
                vat_artlist[lvAnzVat - 1] = to_int(entry(lvint1 - 1, htparam.fchar, ";"))

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == 0)).first()

    if bil_flag == 0:
        t_foinv.b_title = hoteldpt.depart + " BILLS"

    elif bil_flag == 1:
        t_foinv.b_title = hoteldpt.depart + " CLOSED BILLS"
    t_foinv.artikel_str = "F/O Articles"

    for artikel in db_session.query(Artikel).filter(
            (Artikel.activeflag)).all():
        t_artikel = T_artikel()
        t_artikel_list.append(t_artikel)

        buffer_copy(artikel, t_artikel)

    if bil_flag != 0:

        return generate_output()

    for bill in db_session.query(Bill).filter(
            (Bill.resnr > 0) &  (Bill.reslinnr > 0) &  (Bill.flag == 0)).all():

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

        if res_line and res_line.zinr != bill.zinr and res_line.active_flag == 1:

            bbuff = db_session.query(Bbuff).filter(
                    (Bbuff._recid == bill._recid)).first()
            bbuff.zinr = res_line.zinr

            bbuff = db_session.query(Bbuff).first()


    return generate_output()