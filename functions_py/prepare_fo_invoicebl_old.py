#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from functions.get_vip import get_vip
from functions.htpchar import htpchar
from functions.htplogic import htplogic
from functions.htpint import htpint
from models import Bill, Htparam, Guest, Artikel, Waehrung, Brief, Hoteldpt, Res_line, Bill_line

def prepare_fo_invoicebl_old(inp_rechnr:int, combo_pf_file1:string, combo_pf_file2:string, combo_gastnr:int, combo_ledger:int):

    prepare_cache ([Bill, Htparam, Guest, Waehrung, Hoteldpt, Res_line, Bill_line])

    f_foinv_data = []
    t_bill_data = []
    bill = htparam = guest = artikel = waehrung = brief = hoteldpt = res_line = bill_line = None

    t_bill = f_foinv = None

    t_bill_data, T_bill = create_model_like(Bill, {"bl_recid":int})
    f_foinv_data, F_foinv = create_model("F_foinv", {"vipnr1":int, "vipnr2":int, "vipnr3":int, "vipnr4":int, "vipnr5":int, "vipnr6":int, "vipnr7":int, "vipnr8":int, "vipnr9":int, "price_decimal":int, "briefnr497":int, "briefnr685":int, "briefnr1116":int, "briefnr2313":int, "briefnr2314":int, "param60":int, "param145":int, "exchg_rate":Decimal, "param132":string, "param173":string, "ext_char":string, "curr_local":string, "curr_foreign":string, "b_title":string, "room":string, "gname":string, "param219":bool, "double_currency":bool, "change_date":bool, "foreign_rate":bool}, {"vipnr1": 999999, "vipnr2": 999999, "vipnr3": 999999, "vipnr4": 999999, "vipnr5": 999999, "vipnr6": 999999, "vipnr7": 999999, "vipnr8": 999999, "vipnr9": 999999})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_foinv_data, t_bill_data, bill, htparam, guest, artikel, waehrung, brief, hoteldpt, res_line, bill_line
        nonlocal inp_rechnr, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger


        nonlocal t_bill, f_foinv
        nonlocal t_bill_data, f_foinv_data

        return {"f-foinv": f_foinv_data, "t-bill": t_bill_data, "combo_pf_file1": combo_pf_file1, "combo_pf_file2": combo_pf_file2, "combo_gastnr": combo_gastnr, "combo_ledger": combo_ledger}

    def assign_saldo():

        nonlocal f_foinv_data, t_bill_data, bill, htparam, guest, artikel, waehrung, brief, hoteldpt, res_line, bill_line
        nonlocal inp_rechnr, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger


        nonlocal t_bill, f_foinv
        nonlocal t_bill_data, f_foinv_data

        saldo:Decimal = to_decimal("0.0")
        buff_bill = None
        Buff_bill =  create_buffer("Buff_bill",Bill)

        bill = db_session.query(Bill).filter(
            (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.reslinnr > 0) & (Bill.billtyp == 0)
        ).first() 
        while bill is not None:
            saldo =  to_decimal("0")

            for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                saldo =  to_decimal(saldo) + to_decimal(bill_line.betrag)

            if bill.saldo != saldo:
                buff_bill = db_session.query(Bill).filter(Bill._recid == bill._recid).with_for_update().first()
                buff_bill.saldo =  to_decimal(saldo)

            curr_recid = bill._recid
            bill = db_session.query(Bill).filter(
                (Bill.flag == 0) & (Bill.resnr > 0) & (Bill.reslinnr > 0) & (Bill.billtyp == 0) & (Bill._recid > curr_recid)
            ).first() 

    assign_saldo()

    if combo_gastnr == None:
        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 155).first()
        combo_gastnr = htparam.finteger

        if combo_gastnr > 0:
            guest = db_session.query(Guest).filter(Guest.gastnr == combo_gastnr).first()

            if not guest:
                combo_gastnr = 0
            else:
                combo_ledger = guest.zahlungsart

            if combo_ledger > 0:
                artikel = db_session.query(Artikel).filter(Artikel.artnr == combo_ledger, Artikel.departement == 0, Artikel.artart == 2).first()  

                if not artikel:
                    combo_gastnr = 0
                    combo_ledger = 0
            else:
                combo_gastnr = 0
        else:
            combo_gastnr = 0

    if combo_gastnr > 0:
        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 339).first()
        combo_pf_file1 = htparam.fchar

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 340).first()
        combo_pf_file2 = htparam.fchar

    f_foinv = F_foinv()
    f_foinv_data.append(f_foinv)

    f_foinv.vipnr1, f_foinv.vipnr2, f_foinv.vipnr3, f_foinv.vipnr4, f_foinv.vipnr5, f_foinv.vipnr6, f_foinv.vipnr7, f_foinv.vipnr8, f_foinv.vipnr9 = get_output(get_vip())

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 148).first()
    f_foinv.ext_char = htparam.fchar

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 491).first()
    f_foinv.price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 240).first()
    if htparam:
        f_foinv.double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 219).first() 
    f_foinv.change_date = htparam.flogical

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 143).first()
    f_foinv.foreign_rate = htparam.flogical

    if f_foinv.foreign_rate or f_foinv.double_currency:

        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 144).first()

        waehrung = db_session.query(Waehrung).filter(Waehrung.wabkurz == htparam.fchar).first()

        if waehrung:
            f_foinv.exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    f_foinv.curr_local = get_output(htpchar(152))
    f_foinv.curr_foreign = get_output(htpchar(144))
    f_foinv.param132 = get_output(htpchar(132))
    f_foinv.param173 = get_output(htpchar(173))
    f_foinv.param219 = get_output(htplogic(219))
    f_foinv.param60 = get_output(htpint(60))
    f_foinv.param145 = get_output(htpint(645))
    f_foinv.briefnr1116 = get_output(htpint(1116))
    f_foinv.briefnr2313 = get_output(htpint(2313))
    f_foinv.briefnr2314 = get_output(htpint(2314))

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 497).first()

    if htparam.finteger > 0:
        brief = db_session.query(Brief).filter(Brief.briefnr == htparam.finteger).first()

        if brief:
            f_foinv.briefnr497 = htparam.finteger

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 685).first()

    if htparam.finteger > 0:
        brief = db_session.query(Brief).filter(Brief.briefnr == htparam.finteger).first()

        if brief:
            f_foinv.briefnr685 = htparam.finteger

    hoteldpt = db_session.query(Hoteldpt).filter(Hoteldpt.num == 0).first()
    f_foinv.b_title = hoteldpt.depart

    if inp_rechnr != 0:
        bill = db_session.query(Bill).filter(Bill.rechnr == inp_rechnr).first()
        t_bill = T_bill()
        t_bill_data.append(t_bill)

        buffer_copy(bill, t_bill)
        t_bill.bl_recid = to_int(bill._recid)

        res_line = db_session.query(Res_line).filter(Res_line.resnr == bill.resnr, Res_line.reslinnr == bill.reslinnr).first()
        f_foinv.room = bill.zinr

        if res_line:
            f_foinv.gname = res_line.name

    return generate_output()