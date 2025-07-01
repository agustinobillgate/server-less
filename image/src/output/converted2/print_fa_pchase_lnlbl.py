#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Fa_ordheader, L_lieferant, Fa_order, Parameters, L_artikel, Mathis

def print_fa_pchase_lnlbl(pvilanguage:int, docunr:string, lnldelimeter:string):

    prepare_cache ([Htparam, Fa_ordheader, L_lieferant, Fa_order, Parameters, Mathis])

    str1 = ""
    str2 = ""
    tmp_tbl_data_list = []
    lvcarea:string = "print-fa-pchase-lnl"
    long_digit:bool = False
    foreign_currency:bool = False
    price_decimal:int = 0
    bill_recv:string = ""
    address1:string = ""
    address2:string = ""
    cp_name:string = ""
    telp:string = ""
    fax_no:string = ""
    bill_no:string = ""
    bill_date:string = ""
    refer:string = ""
    fa_source:string = ""
    dep_date:string = ""
    arr_date:string = ""
    delivery_date:string = ""
    bl_descript:string = ""
    bl_qty:string = ""
    d_unit:string = ""
    bl_price:string = ""
    bl_amount:string = ""
    c_exrate:string = ""
    bl_balance:string = ""
    balance:Decimal = to_decimal("0.0")
    remark:string = ""
    htparam = fa_ordheader = l_lieferant = fa_order = parameters = l_artikel = mathis = None

    tmp_tbl_data = op_list = None

    tmp_tbl_data_list, Tmp_tbl_data = create_model("Tmp_tbl_data", {"str3":string})
    op_list_list, Op_list = create_model("Op_list", {"artnr":int, "anzahl":Decimal, "bezeich":string, "bez_aend":bool, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "epreis":Decimal, "epreis0":Decimal, "warenwert":Decimal, "konto":string, "warenwert0":Decimal, "remark":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str1, str2, tmp_tbl_data_list, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, fa_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, bl_amount, c_exrate, bl_balance, balance, remark, htparam, fa_ordheader, l_lieferant, fa_order, parameters, l_artikel, mathis
        nonlocal pvilanguage, docunr, lnldelimeter


        nonlocal tmp_tbl_data, op_list
        nonlocal tmp_tbl_data_list, op_list_list

        return {"str1": str1, "str2": str2, "tmp-tbl-data": tmp_tbl_data_list}

    def str_header():

        nonlocal str1, str2, tmp_tbl_data_list, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, fa_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, bl_amount, c_exrate, bl_balance, balance, remark, htparam, fa_ordheader, l_lieferant, fa_order, parameters, l_artikel, mathis
        nonlocal pvilanguage, docunr, lnldelimeter


        nonlocal tmp_tbl_data, op_list
        nonlocal tmp_tbl_data_list, op_list_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
        long_digit = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger

        fa_ordheader = db_session.query(Fa_ordheader).filter(
                 (Fa_ordheader.order_nr == (docunr).lower()) & (Fa_ordheader.supplier_nr > 0)).first()

        if not fa_ordheader:

            fa_ordheader = get_cache (Fa_ordheader, {"order_nr": [(eq, docunr)],"supplier_nr": [(eq, 0)]})

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, fa_ordheader.supplier_nr)]})

        if l_lieferant:
            bill_recv = l_lieferant.firma
            address1 = l_lieferant.adresse1
            address2 = l_lieferant.adresse2
            cp_name = l_lieferant.namekontakt + ", " + l_lieferant.vorname1 +\
                    " " + l_lieferant.anrede1
            telp = l_lieferant.telefon
            fax_no = l_lieferant.fax

        if fa_ordheader:
            bill_no = docunr

            fa_order = get_cache (Fa_order, {"order_nr": [(eq, fa_ordheader.order_nr)]})

            if fa_order:

                if fa_order.create_time > 0:
                    bill_no = bill_no + "*"
            bill_date = to_string(fa_ordheader.order_date)
            dep_date = to_string(fa_ordheader.Credit_Term)
            remark = fa_ordheader.Order_Desc
            arr_date = to_string(fa_ordheader.Expected_Delivery)
            delivery_date = to_string(fa_ordheader.Expected_Delivery)
            refer = to_string(fa_ordheader.pr_nr)

            parameters = db_session.query(Parameters).filter(
                     (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == fa_ordheader.dept_nr)).first()

            if parameters:
                fa_source = parameters.vstring
        str1 = "$bill-recv" + bill_recv + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$name" + cp_name + lnldelimeter + "$telp" + telp + lnldelimeter + "$fax-no" + fax_no + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$bill-date" + bill_date + lnldelimeter + "$refer" + refer + lnldelimeter + "$source" + fa_source + lnldelimeter + "$dep-date" + dep_date + lnldelimeter + "$arr-date" + arr_date + lnldelimeter + "$delivery-date" + delivery_date + lnldelimeter + "$remark" + remark
        str2 = translateExtended ("DESCRIPTION", lvcarea, "") + lnldelimeter + translateExtended ("DELIVDATE", lvcarea, "") + lnldelimeter + translateExtended ("QTY", lvcarea, "") + lnldelimeter + translateExtended ("PRICE UNIT", lvcarea, "") + lnldelimeter + translateExtended ("AMOUNT", lvcarea, "")


    def str_data():

        nonlocal str1, str2, tmp_tbl_data_list, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, fa_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, bl_amount, c_exrate, bl_balance, balance, remark, htparam, fa_ordheader, l_lieferant, fa_order, parameters, l_artikel, mathis
        nonlocal pvilanguage, docunr, lnldelimeter


        nonlocal tmp_tbl_data, op_list
        nonlocal tmp_tbl_data_list, op_list_list

        l_art = None
        create_it:bool = False
        curr_bez:string = ""
        bez_aend:bool = False
        disc:Decimal = to_decimal("0.0")
        disc2:Decimal = to_decimal("0.0")
        tot_qty:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        L_art =  create_buffer("L_art",L_artikel)

        for fa_order in db_session.query(Fa_order).filter(
                 (Fa_order.order_nr == (docunr).lower()) & (Fa_order.activeflag == 0)).order_by(Fa_order.fa_pos).all():
            create_it = False
            bez_aend = False

            mathis = get_cache (Mathis, {"nr": [(eq, fa_order.fa_nr)]})
            curr_bez = mathis.name
            disc =  to_decimal("0")
            disc2 =  to_decimal("0")

            op_list = query(op_list_list, filters=(lambda op_list: op_list.artnr == fa_order.fa_nr and op_list.epreis == fa_order.order_price and op_list.bezeich == mathis.name and op_list.disc == fa_order.discount1 and op_list.disc2 == discount2), first=True)

            if not op_list or create_it:
                vat =  to_decimal("0")
                op_list = Op_list()
                op_list_list.append(op_list)

                op_list.artnr = fa_order.fa_nr
                op_list.bezeich = curr_bez
                op_list.bez_aend = bez_aend
                op_list.epreis =  to_decimal(fa_order.order_price)
                op_list.epreis0 =  to_decimal(fa_order.order_price)
                op_list.remark = fa_order.fa_remarks


                op_list.disc =  to_decimal(fa_order.discount1)
                op_list.disc2 =  to_decimal(fa_order.discount2)
                op_list.vat =  to_decimal(fa_order.vat)
                disc =  to_decimal(fa_order.discount1) / to_decimal("100")
                disc2 =  to_decimal(fa_order.discount2) / to_decimal("100")
                vat =  to_decimal(fa_order.vat) / to_decimal("100")
            op_list.epreis0 =  to_decimal(fa_order.order_price) / to_decimal((1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
            op_list.anzahl =  to_decimal(op_list.anzahl) + to_decimal(fa_order.order_qty)
            op_list.warenwert =  to_decimal(op_list.warenwert) + to_decimal(fa_order.order_amount)
            op_list.warenwert0 =  to_decimal(op_list.warenwert0) + to_decimal(fa_order.order_amount) / to_decimal((1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
            tot_qty =  to_decimal(tot_qty) + to_decimal(fa_order.order_qty)

        for op_list in query(op_list_list):
            bl_descript = op_list.bezeich

            if op_list.anzahl >= 10000 or (- op_list.anzahl >= 10000):
                bl_qty = to_string(op_list.anzahl, "->>>,>>9")

            elif op_list.anzahl >= 1000 or (- op_list.anzahl >= 1000):

                if op_list.anzahl >= 0:
                    bl_qty = to_string(op_list.anzahl, ">,>>9.99")
                else:
                    bl_qty = to_string(op_list.anzahl, "->,>>9.9")
            else:

                if length(to_string(op_list.anzahl - round(op_list.anzahl - 0.5, 0))) > 3:
                    bl_qty = to_string(op_list.anzahl, "->>9.999")
                else:
                    bl_qty = to_string(op_list.anzahl, "->>9.99")
            balance =  to_decimal(balance) + to_decimal(op_list.warenwert)

            if not long_digit:

                if op_list.epreis >= 10000000:
                    bl_price = to_string(op_list.epreis, "->>,>>>,>>>,>>>,>>9")
                else:
                    bl_price = to_string(op_list.epreis, ">,>>>,>>9.99")

                if price_decimal == 0 and not foreign_currency:
                    bl_amount = to_string(op_list.warenwert, "->>>,>>>,>>>,>>9.99")
                    bl_balance = to_string(balance, "->>>,>>>,>>>,>>9.99")

                elif price_decimal == 2 or foreign_currency:
                    bl_amount = to_string(op_list.warenwert, "->>>,>>>,>>>,>>9.99")
                    bl_balance = to_string(balance, "->>>,>>>,>>>,>>9.99")


            else:
                bl_price = to_string(op_list.epreis, "->>>,>>>,>>>,>>9.99")
                bl_amount = to_string(op_list.warenwert, "->>>,>>>,>>>,>>9.99")
                bl_balance = to_string(balance, "->>>,>>>,>>>,>>9.99")


            tmp_tbl_data = Tmp_tbl_data()
            tmp_tbl_data_list.append(tmp_tbl_data)

            tmp_tbl_data.str3 = bl_descript + lnldelimeter +\
                    arr_date + lnldelimeter +\
                    bl_qty + lnldelimeter +\
                    bl_price + lnldelimeter +\
                    bl_amount + lnldelimeter +\
                    c_exrate + lnldelimeter +\
                    bl_balance + lnldelimeter +\
                    op_list.remark


    str_header()
    str_data()

    return generate_output()