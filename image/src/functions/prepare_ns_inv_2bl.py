from functions.additional_functions import *
import decimal
from functions.htpdec import htpdec
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpchar import htpchar
from sqlalchemy import func
from models import Bill, Guest, Htparam, Artikel, Waehrung, Brief, Hoteldpt

def prepare_ns_inv_2bl(inp_rechnr:int, curr_department:int, combo_pf_file1:str, combo_pf_file2:str, combo_gastnr:int, combo_ledger:int):
    cashless_license = False
    cashless_minsaldo = 0
    ns_useraccess = False
    f_foinv_list = []
    t_bill_list = []
    t_guest_list = []
    golf_license:str = "NO"
    bill = guest = htparam = artikel = waehrung = brief = hoteldpt = None

    t_bill = t_guest = f_foinv = None

    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})
    t_guest_list, T_guest = create_model_like(Guest)
    f_foinv_list, F_foinv = create_model("F_foinv", {"price_decimal":int, "briefnr2314":int, "param60":int, "param145":int, "param487":int, "tel_rechnr":int, "pos1":int, "pos2":int, "ba_dept":int, "exchg_rate":decimal, "max_price":decimal, "param132":str, "ext_char":str, "curr_local":str, "curr_foreign":str, "b_title":str, "gname":str, "param219":bool, "double_currency":bool, "foreign_rate":bool, "banquet_flag":bool, "mc_flag":bool}, {"ba_dept": -1})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cashless_license, cashless_minsaldo, ns_useraccess, f_foinv_list, t_bill_list, t_guest_list, golf_license, bill, guest, htparam, artikel, waehrung, brief, hoteldpt


        nonlocal t_bill, t_guest, f_foinv
        nonlocal t_bill_list, t_guest_list, f_foinv_list
        return {"cashless_license": cashless_license, "cashless_minsaldo": cashless_minsaldo, "ns_useraccess": ns_useraccess, "f-foinv": f_foinv_list, "t-bill": t_bill_list, "t-guest": t_guest_list}

    pass


    if combo_gastnr == None:

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 155)).first()
        combo_gastnr = htparam.finteger

        if combo_gastnr > 0:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == combo_gastnr)).first()

            if not guest:
                combo_gastnr = 0
            else:
                combo_ledger = guest.zahlungsart

            if combo_ledger > 0:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == combo_ledger) &  (Artikel.departement == 0) &  (Artikel.artart == 2)).first()

                if not artikel:
                    combo_gastnr = 0
                    combo_ledger = 0


            else:
                combo_gastnr = 0
        else:
            combo_gastnr = 0

    if combo_gastnr > 0:

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 339)).first()
        combo_pf_file1 = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 340)).first()
        combo_pf_file2 = htparam.fchar
    f_foinv = F_foinv()
    f_foinv_list.append(f_foinv)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 148)).first()
    f_foinv.ext_char = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 453)).first()

    if htparam.feldtyp == 5 and htparam.fchar != "":
        f_foinv.ext_char = f_foinv.ext_char + ";" + htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    f_foinv.price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam:
        f_foinv.double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    f_foinv.foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            f_foinv.exchg_rate = waehrung.ankauf / waehrung.einheit
    f_foinv.max_price = get_output(htpdec(1086))
    mc_flag = get_output(htplogic(168))

    if mc_flag:
        pos1 = get_output(htpint(337))
        pos2 = get_output(htpint(338))

        if pos1 == 0:
            pos1 = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 985)).first()

    if htparam.flogical:
        f_foinv.ba_dept = get_output(htpint(900))
    f_foinv.curr_local = get_output(htpchar(152))
    f_foinv.curr_foreign = get_output(htpchar(144))
    f_foinv.param132 = get_output(htpchar(132))
    f_foinv.param219 = get_output(htplogic(219))
    f_foinv.param60 = get_output(htpint(60))
    f_foinv.param145 = get_output(htpint(145))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1022) &  (func.lower(Htparam.bezeich) != "not used") &  (Htparam.flogical)).first()

    if htparam:
        cashless_license = True
    cashless_minsaldo = get_output(htpdec(586))
    ns_useraccess = get_output(htplogic(589))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 2314)).first()

    if htparam.finteger > 0:

        brief = db_session.query(Brief).filter(
                (Briefnr == htparam.finteger)).first()

        if brief:
            f_foinv.briefnr2314 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 487)).first()

    if htparam.finteger > 0:

        brief = db_session.query(Brief).filter(
                (Briefnr == htparam.finteger)).first()

        if brief:
            f_foinv.param487 = htparam.finteger

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_department)).first()
    f_foinv.b_title = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 299)).first()

    if htparam.paramgruppe == 99 and htparam.flogical:
        golf_license = "YES"
    f_foinv.gname = golf_license + chr(2)

    if inp_rechnr != 0:

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == inp_rechnr)).first()
        t_bill = T_bill()
        t_bill_list.append(t_bill)

        buffer_copy(bill, t_bill)
        t_bill.bl_recid = to_int(bill._recid)

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == bill.gastnr)).first()

        if guest:
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            f_foinv.gname = f_foinv.gname + guest.name

    return generate_output()