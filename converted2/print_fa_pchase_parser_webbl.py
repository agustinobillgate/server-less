#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, Fa_ordheader, L_lieferant, Fa_order, Mathis

def print_fa_pchase_parser_webbl(docu_nr:string):

    prepare_cache ([Fa_ordheader, L_lieferant, Fa_order, Mathis])

    err = 0
    supplier_name = ""
    bill_recv = ""
    address1 = ""
    address2 = ""
    order_date = None
    deliv_date = None
    telefon = ""
    fax = ""
    pr_nr = ""
    op_list_data = []
    l_artikel = fa_ordheader = l_lieferant = fa_order = mathis = None

    op_list = None

    op_list_data, Op_list = create_model("Op_list", {"artnr":int, "anzahl":Decimal, "bezeich":string, "bez_aend":bool, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "epreis":Decimal, "epreis0":Decimal, "warenwert":Decimal, "konto":string, "warenwert0":Decimal, "remark":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, op_list_data, l_artikel, fa_ordheader, l_lieferant, fa_order, mathis
        nonlocal docu_nr


        nonlocal op_list
        nonlocal op_list_data

        return {"err": err, "supplier_name": supplier_name, "bill_recv": bill_recv, "address1": address1, "address2": address2, "order_date": order_date, "deliv_date": deliv_date, "telefon": telefon, "fax": fax, "pr_nr": pr_nr, "op-list": op_list_data}

    def create_list():

        nonlocal err, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, op_list_data, l_artikel, fa_ordheader, l_lieferant, fa_order, mathis
        nonlocal docu_nr


        nonlocal op_list
        nonlocal op_list_data

        create_it:bool = False
        curr_bez:string = ""
        bez_aend:bool = False
        disc:Decimal = to_decimal("0.0")
        disc2:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        tot_qty:Decimal = to_decimal("0.0")
        l_art = None
        L_art =  create_buffer("L_art",L_artikel)

        fa_ordheader = get_cache (Fa_ordheader, {"order_nr": [(eq, docu_nr)]})

        if not fa_ordheader:
            err = 2

            return

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, fa_ordheader.supplier_nr)]})

        if l_lieferant:
            supplier_name = l_lieferant.namekontakt + ", " + l_lieferant.vorname1 +\
                    " " + l_lieferant.anrede1
            bill_recv = l_lieferant.firma
            address1 = l_lieferant.adresse1
            address2 = l_lieferant.adresse2
            order_date = date_mdy(fa_ordheader.order_date)
            deliv_date = date_mdy(fa_ordheader.expected_delivery)
            telefon = l_lieferant.telefon
            fax = l_lieferant.fax
            pr_nr = fa_ordheader.pr_nr

        for fa_order in db_session.query(Fa_order).filter(
                 (Fa_order.order_nr == (docu_nr).lower()) & (Fa_order.activeflag == 0)).order_by(Fa_order.fa_pos).all():
            create_it = False
            bez_aend = False

            mathis = get_cache (Mathis, {"nr": [(eq, fa_order.fa_nr)]})
            curr_bez = mathis.name
            disc =  to_decimal("0")
            disc2 =  to_decimal("0")

            op_list = query(op_list_data, filters=(lambda op_list: op_list.artnr == fa_order.fa_nr and op_list.epreis == fa_order.order_price and op_list.bezeich == mathis.name and op_list.disc == fa_order.discount1 and op_list.disc2 == discount2), first=True)

            if not op_list or create_it:
                vat =  to_decimal("0")
                op_list = Op_list()
                op_list_data.append(op_list)

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

    create_list()

    return generate_output()