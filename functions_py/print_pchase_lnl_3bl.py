#using conversion tools version: 1.0.0.117
"""_yusufwijasena_20/10/2025

    TicketID: 3EAECD
        _remark_:   - Fix variable declaration
                    - Fix python indentation
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Paramtext, Htparam, L_orderhdr, L_lieferant, L_order, Parameters, Waehrung, Guestbook, L_artikel

def print_pchase_lnl_3bl(pvilanguage:int, lnldelimeter:str, docunr:str, stattype:int, curr_status:str):

    prepare_cache ([Queasy, Paramtext, Htparam, L_orderhdr, L_lieferant, L_order, Parameters, Waehrung, Guestbook, L_artikel])

    str1 = ""
    str2 = ""
    str3_list_data = []
    esign_print_data = []
    lvcarea:str = "print-pchase-lnl"
    long_digit:bool = False
    foreign_currency:bool = False
    price_decimal:int = 0
    bill_recv = ""
    address1 = ""
    address2 = ""
    cp_name = ""
    telp = ""
    fax_no = ""
    bill_no = ""
    bill_date = ""
    refer = ""
    po_source = ""
    dep_date = ""
    arr_date = ""
    delivery_date = ""
    bl_descript = ""
    bl_qty = ""
    d_unit = ""
    bl_price = ""
    b2_price = ""
    bl_amount = ""
    b2_amount = ""
    c_exrate = ""
    bl_balance = ""
    b2_balance = ""
    balance = to_decimal("0.0")
    remark = ""
    bank_name = ""
    account = ""
    rekening = ""
    i:int = 0
    globaldisc = to_decimal("0.0")
    companytitle = ""
    bl_vat = ""
    po_number = ""
    htl_name = ""
    htl_adr = ""
    htl_tel = ""
    created_by = ""
    vat_code = ""
    vat1 = to_decimal("0.0")
    vat2 = to_decimal("0.0")
    p_app:bool = False
    img_id_name:List[str] = create_empty_list(4,"")
    img_id_date:List[str] = create_empty_list(4,"")
    img_id_pos:List[str] = create_empty_list(4,"")
    bestellart = ""
    queasy = paramtext = htparam = l_orderhdr = l_lieferant = l_order = parameters = waehrung = guestbook = l_artikel = None

    str3_list = esign_print = op_list = b_queasy = None

    str3_list_data, Str3_list = create_model(
        "Str3_list", {
            "str":str
            }
        )
    esign_print_data, Esign_print = create_model(
        "Esign_print", {
            "sign_nr":int, 
            "sign_name":str, 
            "sign_img":bytes, 
            "sign_date":str, 
            "sign_position":str
            }
        )
    op_list_data, Op_list = create_model(
        "Op_list", {
            "artnr":int, 
            "anzahl":Decimal, 
            "bezeich":str, 
            "bez_aend":bool, 
            "disc":Decimal, 
            "disc2":Decimal, 
            "vat":Decimal, 
            "epreis":Decimal, 
            "epreis0":Decimal, 
            "warenwert":Decimal, 
            "konto":str, 
            "warenwert0":Decimal, 
            "remark":str, 
            "disc_value":Decimal, 
            "disc2_value":Decimal, 
            "brutto":Decimal, 
            "vat_value":Decimal, 
            "po_nr":str, 
            "vat_code":str, 
            "vat1":Decimal, 
            "vat2":Decimal
            }
        )

    B_queasy = create_buffer("B_queasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str1, str2, str3_list_data, esign_print_data, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, po_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, b2_price, bl_amount, b2_amount, c_exrate, bl_balance, b2_balance, balance, remark, bank_name, account, rekening, i, globaldisc, companytitle, bl_vat, po_number, htl_name, htl_adr, htl_tel, created_by, vat_code, vat1, vat2, p_app, img_id_name, img_id_date, img_id_pos, bestellart, queasy, paramtext, htparam, l_orderhdr, l_lieferant, l_order, parameters, waehrung, guestbook, l_artikel
        nonlocal pvilanguage, lnldelimeter, docunr, stattype, curr_status
        nonlocal b_queasy
        nonlocal str3_list, esign_print, op_list, b_queasy
        nonlocal str3_list_data, esign_print_data, op_list_data

        return {
            "str1": str1, 
            "str2": str2, 
            "str3-list": str3_list_data, 
            "esign-print": esign_print_data
            }

    def decode_str(in_str:str):
        nonlocal str1, str2, str3_list_data, esign_print_data, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, po_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, b2_price, bl_amount, b2_amount, c_exrate, bl_balance, b2_balance, balance, remark, bank_name, account, rekening, i, globaldisc, companytitle, bl_vat, po_number, htl_name, htl_adr, htl_tel, created_by, vat_code, vat1, vat2, p_app, img_id_name, img_id_date, img_id_pos, bestellart, queasy, paramtext, htparam, l_orderhdr, l_lieferant, l_order, parameters, waehrung, guestbook, l_artikel
        nonlocal pvilanguage, lnldelimeter, docunr, stattype, curr_status
        nonlocal b_queasy
        nonlocal str3_list, esign_print, op_list, b_queasy
        nonlocal str3_list_data, esign_print_data, op_list_data

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    def do_billline():
        nonlocal str1, str2, str3_list_data, esign_print_data, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, po_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, b2_price, bl_amount, b2_amount, c_exrate, bl_balance, b2_balance, balance, remark, bank_name, account, rekening, i, globaldisc, companytitle, bl_vat, po_number, htl_name, htl_adr, htl_tel, created_by, vat_code, vat1, vat2, p_app, img_id_name, img_id_date, img_id_pos, bestellart, queasy, paramtext, htparam, l_orderhdr, l_lieferant, l_order, parameters, waehrung, guestbook, l_artikel
        nonlocal pvilanguage, lnldelimeter, docunr, stattype, curr_status
        nonlocal b_queasy
        nonlocal str3_list, esign_print, op_list, b_queasy
        nonlocal str3_list_data, esign_print_data, op_list_data

        l_art = None
        create_it:bool = False
        curr_bez = ""
        bez_aend:bool = False
        disc = to_decimal("0.0")
        disc2 = to_decimal("0.0")
        disc_value = to_decimal("0.0")
        disc2_value = to_decimal("0.0")
        tot_qty = to_decimal("0.0")
        vat = to_decimal("0.0")
        vat_val = to_decimal("0.0")
        L_art =  create_buffer("L_art",L_artikel)
        op_list_data.clear()

        if stattype == 0 or stattype == 2:
            for l_order in db_session.query(L_order).filter(
                (L_order.docu_nr == (docunr).lower()) & (L_order.loeschflag <= 1) & (L_order.pos > 0)).order_by(L_order.pos).all():
                create_it = False
                bez_aend = False

                l_art = get_cache (L_artikel, {
                    "artnr": [(eq, l_order.artnr)]})

                if l_art:
                    curr_bez = l_art.bezeich
                    disc =  to_decimal("0")
                    disc2 =  to_decimal("0")

                    if l_order.quality != "":
                        disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) * 0.01
                        disc_value = to_int(substring(l_order.quality, 18, 18))

                        if length(l_order.quality) > 12:
                            disc2 = to_int(substring(l_order.quality, 12, 2)) + int(substring(l_order.quality, 15, 2)) * 0.01
                            disc2_value = to_int(substring(l_order.quality, 36, 18))
                            vat_val = to_int(substring(l_order.quality, 54))

                    if l_art.jahrgang == 0 or length(l_order.stornogrund) <= 12:
                        op_list = query(op_list_data, filters=(lambda op_list: op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich == l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund), first=True)
                    else:
                        create_it = True
                        bez_aend = True

                    if not op_list or create_it:
                        vat =  to_decimal("0")
                        op_list = Op_list()
                        op_list_data.append(op_list)

                        op_list.artnr = l_order.artnr
                        op_list.bezeich = curr_bez
                        op_list.bez_aend = bez_aend
                        op_list.epreis =  to_decimal(l_order.einzelpreis)
                        op_list.epreis0 =  to_decimal(l_order.einzelpreis)
                        op_list.konto = l_order.stornogrund
                        op_list.remark = l_order.besteller
                        op_list.po_nr = po_number
                        op_list.vat_code = vat_code
                        op_list.vat1 =  to_decimal(vat1)
                        op_list.vat2 =  to_decimal(vat2)

                        if l_order.quality != "":
                            vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) * 0.01
                            op_list.disc =  to_decimal(disc)
                            op_list.disc2 =  to_decimal(disc2)
                            op_list.disc_value =  to_decimal(disc_value)
                            op_list.disc2_value =  to_decimal(disc2_value)
                            op_list.vat =  to_decimal(vat)
                            op_list.vat_value =  to_decimal(vat_val)
                            disc =  to_decimal(disc) / to_decimal("100")
                            disc2 =  to_decimal(disc2) / to_decimal("100")
                            vat =  to_decimal(vat) / to_decimal("100")

                    op_list.anzahl =  to_decimal(op_list.anzahl + l_order.anzahl)
                    op_list.warenwert =  to_decimal(op_list.warenwert + l_order.warenwert)
                    op_list.brutto = (to_decimal(op_list.warenwert + op_list.disc_value + op_list.disc2_value) - vat_val)
                    op_list.epreis0 =  to_decimal(op_list.brutto / op_list.anzahl)
                    op_list.warenwert0 =  to_decimal(op_list.warenwert0 + l_order.warenwert) / to_decimal((1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
                    tot_qty =  to_decimal(tot_qty + l_order.anzahl)

        elif stattype == 1 or stattype == 3:
            for l_order in db_session.query(L_order).filter(
                (L_order.docu_nr == (docunr).lower()) & (L_order.loeschflag > 0) & (L_order.pos > 0)).order_by(L_order.pos).all():
                create_it = False
                bez_aend = False

                l_art = get_cache (L_artikel, {
                    "artnr": [(eq, l_order.artnr)]})
                curr_bez = l_art.bezeich
                disc =  to_decimal("0")
                disc2 =  to_decimal("0")

                if l_order.quality != "":
                    disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) * 0.01
                    disc_value = to_int(substring(l_order.quality, 18, 18))

                    if length(l_order.quality) > 12:
                        disc2 = to_int(substring(l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) * 0.01
                        disc2_value = to_int(substring(l_order.quality, 36, 18))
                        vat_val = to_int(substring(l_order.quality, 54))

                if l_art.jahrgang == 0 or length(l_order.stornogrund) <= 12:
                    op_list = query(op_list_data, filters=(lambda op_list: op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich == l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund), first=True)
                else:
                    create_it = True
                    bez_aend = True

                if not op_list or create_it:
                    vat =  to_decimal("0")
                    op_list = Op_list()
                    op_list_data.append(op_list)

                    op_list.artnr = l_order.artnr
                    op_list.bezeich = curr_bez
                    op_list.bez_aend = bez_aend
                    op_list.epreis =  to_decimal(l_order.einzelpreis)
                    op_list.epreis0 =  to_decimal(l_order.einzelpreis)
                    op_list.konto = l_order.stornogrund
                    op_list.remark = l_order.besteller
                    op_list.po_nr = po_number
                    op_list.vat_code = vat_code
                    op_list.vat1 =  to_decimal(vat1)
                    op_list.vat2 =  to_decimal(vat2)

                    if l_order.quality != "":
                        vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) * 0.01
                        op_list.disc =  to_decimal(disc)
                        op_list.disc2 =  to_decimal(disc2)
                        op_list.disc_value =  to_decimal(disc_value)
                        op_list.disc2_value =  to_decimal(disc2_value)
                        op_list.vat =  to_decimal(vat)
                        op_list.vat_value =  to_decimal(vat_val)
                        disc =  to_decimal(disc) / to_decimal("100")
                        disc2 =  to_decimal(disc2) / to_decimal("100")
                        vat =  to_decimal(vat) / to_decimal("100")

                op_list.anzahl =  to_decimal(op_list.anzahl + l_order.anzahl)
                op_list.warenwert =  to_decimal(op_list.warenwert + l_order.warenwert)
                op_list.brutto = (l_order.warenwert + op_list.disc_value + op_list.disc2_value) - to_int(substring(l_order.quality, 54))
                op_list.epreis0 =  to_decimal(op_list.brutto / l_order.anzahl)
                op_list.warenwert0 =  to_decimal(op_list.warenwert0 + l_order.warenwert) / to_decimal((1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
                tot_qty =  to_decimal(tot_qty + l_order.anzahl)

        elif stattype == None:

            for l_order in db_session.query(L_order).filter(
                (L_order.docu_nr == (docunr).lower()) & (L_order.pos > 0)).order_by(L_order.pos).all():
                create_it = False
                bez_aend = False

                l_art = get_cache (L_artikel, {
                    "artnr": [(eq, l_order.artnr)]})
                curr_bez = l_art.bezeich
                disc =  to_decimal("0")
                disc2 =  to_decimal("0")

                if l_order.quality != "":
                    disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) * 0.01
                    disc_value = to_int(substring(l_order.quality, 18, 18))

                    if length(l_order.quality) > 12:
                        disc2 = to_int(substring(l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) * 0.01
                        disc2_value = to_int(substring(l_order.quality, 36, 18))
                        vat_val = to_int(substring(l_order.quality, 54))

                if l_art.jahrgang == 0 or length(l_order.stornogrund) <= 12:
                    op_list = query(op_list_data, filters=(lambda op_list: op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich == l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund), first=True)
                else:
                    create_it = True
                    bez_aend = True

                if not op_list or create_it:
                    vat =  to_decimal("0")
                    op_list = Op_list()
                    op_list_data.append(op_list)

                    op_list.artnr = l_order.artnr
                    op_list.bezeich = curr_bez
                    op_list.bez_aend = bez_aend
                    op_list.epreis =  to_decimal(l_order.einzelpreis)
                    op_list.epreis0 =  to_decimal(l_order.einzelpreis)
                    op_list.konto = l_order.stornogrund
                    op_list.remark = l_order.besteller
                    op_list.po_nr = po_number
                    op_list.vat_code = vat_code
                    op_list.vat1 =  to_decimal(vat1)
                    op_list.vat2 =  to_decimal(vat2)

                    if l_order.quality != "":
                        vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) * 0.01
                        op_list.disc =  to_decimal(disc)
                        op_list.disc2 =  to_decimal(disc2)
                        op_list.disc_value =  to_decimal(disc_value)
                        op_list.disc2_value =  to_decimal(disc2_value)
                        op_list.vat =  to_decimal(vat)
                        op_list.vat_value =  to_decimal(vat_val)
                        disc =  to_decimal(disc) / to_decimal("100")
                        disc2 =  to_decimal(disc2) / to_decimal("100")
                        vat =  to_decimal(vat) / to_decimal("100")


                op_list.anzahl =  to_decimal(op_list.anzahl + l_order.anzahl)
                op_list.warenwert =  to_decimal(op_list.warenwert + l_order.warenwert)
                op_list.brutto = (l_order.warenwert + op_list.disc_value + op_list.disc2_value) - to_int(substring(l_order.quality, 54))
                op_list.epreis0 =  to_decimal(op_list.brutto / l_order.anzahl)
                op_list.warenwert0 =  to_decimal(op_list.warenwert0 + l_order.warenwert) / to_decimal((1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
                tot_qty =  to_decimal(tot_qty + l_order.anzahl)

        for op_list in query(op_list_data):

            if op_list.anzahl == 0:
                op_list_data.remove(op_list)

    htl_name = ""

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 240)]})

    if paramtext and paramtext.ptexte != "":
        htl_name = decode_str(paramtext.ptexte)
    htl_adr = ""

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})

    if paramtext:
        htl_adr = paramtext.ptexte
    htl_tel = ""

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})

    if paramtext:
        htl_tel = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 71)]})
    p_app = htparam.flogical

    l_orderhdr = db_session.query(L_orderhdr).filter(
        (L_orderhdr.docu_nr == (docunr).lower()) & (L_orderhdr.lief_nr > 0)).first()

    if not l_orderhdr:
        l_orderhdr = get_cache (L_orderhdr, {
            "docu_nr": [(eq, docunr)],
            "lief_nr": [(eq, 0)]})

    l_lieferant = get_cache (L_lieferant, {
        "lief_nr": [(eq, l_orderhdr.lief_nr)]})

    if l_lieferant:
        for i in range(1,length(l_lieferant.bank)  + 1) :

            if matches(substring(l_lieferant.bank, i - 1, 3),r"a/n"):
                break
        bill_recv = l_lieferant.firma
        address1 = l_lieferant.adresse1
        address2 = l_lieferant.adresse2
        cp_name = l_lieferant.namekontakt + ", " + l_lieferant.vorname1 + " " + l_lieferant.anrede1
        telp = l_lieferant.telefon
        fax_no = l_lieferant.fax
        bank_name = substring(l_lieferant.bank, 0, i - 2)
        account = substring(l_lieferant.bank, i + 4 - 1, length(l_lieferant.bank))
        rekening = l_lieferant.kontonr
        companytitle = l_lieferant.anredefirma

        queasy = get_cache (Queasy, {
            "key": [(eq, 219)],
            "number1": [(eq, l_lieferant.lief_nr)]})

        if queasy:
            vat_code = queasy.char1
            vat1 =  to_decimal(queasy.deci1)
            vat2 =  to_decimal(queasy.deci2)

    if l_orderhdr:
        bill_no = docunr

        l_order = get_cache (L_order, {
            "lief_nr": [(eq, l_orderhdr.lief_nr)],
            "docu_nr": [(eq, docunr)],"pos": [(eq, 0)]})

        if l_order:
            if l_order.zeit > 0:
                if curr_status.lower()  == ("design"):
                    bill_no = docunr + "-REPRINT"
                else:
                    queasy = get_cache (Queasy, {
                        "key": [(eq, 240)],
                        "char1": [(eq, l_order.docu_nr)]})

                    if not queasy:
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 240
                        queasy.char1 = l_order.docu_nr


                        bill_no = docunr
                    else:
                        queasy.number1 = queasy.number1 + 1
                        bill_no = docunr + "-REPRINT" + to_string(queasy.number1)
            refer = to_string(l_order.lief_fax[0])
            globaldisc =  to_decimal(l_order.warenwert)


        bill_date = to_string(l_orderhdr.bestelldatum)
        dep_date = to_string(l_orderhdr.angebot_lief[1])
        remark = l_orderhdr.lief_fax[2]
        arr_date = to_string(l_orderhdr.lieferdatum)
        delivery_date = to_string(l_orderhdr.lieferdatum)
        po_number = l_order.docu_nr
        created_by = to_string(l_orderhdr.besteller)


        bestellart = to_string(l_orderhdr.bestellart)

        parameters = db_session.query(Parameters).filter(
            (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

        if parameters:
            po_source = parameters.vstr

        waehrung = get_cache (Waehrung, {
            "waehrungsnr": [(eq, l_orderhdr.angebot_lief[2])]})

        if waehrung:
            htparam = get_cache (Htparam, {
                "paramnr": [(eq, 152)]})

            if htparam.fchar != "" and (htparam.fchar != waehrung.wabkurz):
                foreign_currency = True
            c_exrate = to_string(waehrung.wabkurz)

        if p_app:
            for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 245) & (Queasy.char1 == (docunr).lower())).order_by(Queasy._recid).all():

                guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == queasy.number2) & (Guestbook.reserve_logic[inc_value(1)])).first()

                if guestbook:
                    esign_print = Esign_print()
                    esign_print_data.append(esign_print)

                    esign_print.sign_nr = queasy.number1
                    esign_print.sign_name = entry(1, guestbook.infostr, "|")
                    esign_print.sign_img = guestbook.imagefile
                    esign_print.sign_date = entry(1, queasy.char3, "|")
                    esign_print.sign_position = entry(3, guestbook.infostr, "|")
                    img_id_name[queasy.number1 - 1] = entry(1, guestbook.infostr, "|")
                    img_id_date[queasy.number1 - 1] = entry(1, queasy.char3, "|")
                    img_id_pos[queasy.number1 - 1] = entry(3, guestbook.infostr, "|")


    str1 = "$bill-recv" + bill_recv + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$name" + cp_name + lnldelimeter + "$telp" + telp + lnldelimeter + "$fax-no" + fax_no + lnldelimeter + "$bill-no" + bill_no + lnldelimeter + "$bill-date" + bill_date + lnldelimeter + "$refer" + refer + lnldelimeter + "$source" + po_source + lnldelimeter + "$dep-date" + dep_date + lnldelimeter + "$arr-date" + arr_date + lnldelimeter + "$delivery-date" + delivery_date + lnldelimeter + "$remark" + remark + lnldelimeter + "$GlobDisc" + to_string(globaldisc, "->>>,>>>,>>9.99") + lnldelimeter + "$bankname" + bank_name + lnldelimeter + "$account" + account + lnldelimeter + "$rekening" + rekening + lnldelimeter + "$title" + companytitle + lnldelimeter + "$orderType" + bestellart
    
    str2 = translateExtended ("DESCRIPTION", lvcarea, "") + lnldelimeter + translateExtended ("DELIVDATE", lvcarea, "") + lnldelimeter + translateExtended ("QTY", lvcarea, "") + lnldelimeter + translateExtended ("UNIT", lvcarea, "") + lnldelimeter + translateExtended ("PRICE UNIT", lvcarea, "") + lnldelimeter + translateExtended ("AMOUNT", lvcarea, "") + lnldelimeter + translateExtended ("disc", lvcarea, "") + lnldelimeter + translateExtended ("disc2", lvcarea, "") + lnldelimeter + translateExtended ("vat", lvcarea, "") + lnldelimeter + translateExtended ("PO Number", lvcarea, "")
    do_billline()

    for op_list in query(op_list_data, sort_by=[("bezeich",False)]):
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

        l_artikel = get_cache (L_artikel, {
            "artnr": [(eq, op_list.artnr)]})

        if l_artikel:
            d_unit = l_artikel.traubensorte
        balance =  to_decimal(balance + op_list.warenwert)

        if not long_digit:
            if price_decimal == 0 and not foreign_currency:
                bl_amount = to_string(op_list.warenwert, "->>>,>>>,>>>,>>9")
                bl_balance = to_string(balance, "->>>,>>>,>>>,>>9")

                if op_list.epreis >= 10000000:
                    bl_price = to_string(op_list.epreis, " >>>,>>>,>>>,>>9")
                else:
                    bl_price = to_string(op_list.epreis, ">>>,>>>,>>>,>>9")

            elif price_decimal == 2 or foreign_currency:
                bl_amount = to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9.99")
                bl_balance = to_string(balance, "->,>>>,>>>,>>>,>>9.99")

                if op_list.epreis >= 10000000:
                    bl_price = to_string(op_list.epreis, " >>,>>>,>>>,>>>,>>9.99")
                else:
                    bl_price = to_string(op_list.epreis, ">>>,>>>,>>>,>>9.99")
            bl_vat = to_string(op_list.vat_value, "->,>>>,>>>,>>9")


        else:
            bl_price = to_string(op_list.epreis, ">,>>>,>>>,>>>,>>9")
            bl_amount = to_string(op_list.warenwert, "->>,>>>,>>>,>>>,>>9")
            bl_balance = to_string(balance, "->>,>>>,>>>,>>>,>>9")
            bl_vat = to_string(op_list.vat_value, "->,>>>,>>>,>>9")
            po_nr = op_list.po_nr


        b2_price = to_string(op_list.epreis, ">>>,>>>,>>>,>>9.999")
        b2_amount = to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9.999")
        b2_balance = to_string(balance, "->,>>>,>>>,>>>,>>9.999")


        str3_list = Str3_list()
        str3_list_data.append(str3_list)

        str3_list.str = bl_descript + lnldelimeter + arr_date + lnldelimeter + bl_qty + lnldelimeter + d_unit + lnldelimeter + bl_price + lnldelimeter + bl_amount + lnldelimeter + c_exrate + lnldelimeter + bl_balance + lnldelimeter + op_list.remark + lnldelimeter + op_list.konto + lnldelimeter + to_string(op_list.disc, "->>9.99") + lnldelimeter + to_string(op_list.disc2, "->>9.99") + lnldelimeter + to_string(op_list.vat, "->>9.99") + lnldelimeter + to_string(op_list.disc_value, "->>>,>>>,>>>,>>9") + lnldelimeter + to_string(op_list.disc2_value, "->>>,>>>,>>>,>>9") + lnldelimeter + to_string(op_list.epreis0, ">>,>>>,>>>,>>>,>>9") + lnldelimeter + bl_vat + lnldelimeter + to_string(op_list.artnr, ">>>>>>>9") + lnldelimeter + to_string(op_list.brutto, ">>>,>>>,>>>,>>9") + lnldelimeter + po_nr + lnldelimeter + po_source + lnldelimeter + to_string(vat1, "->,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(vat1, "->,>>>,>>>,>>>,>>9.99") + lnldelimeter + b2_price + lnldelimeter + b2_amount + lnldelimeter + b2_balance
    
    str1 = str1 + lnldelimeter + "$AfterDisc" + to_string(balance - globaldisc, "->>>,>>>,>>9.99") + lnldelimeter + "$HN" + htl_name + lnldelimeter + "$HA" + htl_adr + lnldelimeter + "$HT" + htl_tel + lnldelimeter + "$CreatedBy" + created_by + lnldelimeter + "$VC" + vat_code + lnldelimeter + "$n1" + img_id_name[0] + lnldelimeter + "$n2" + img_id_name[1] + lnldelimeter + "$n3" + img_id_name[2] + lnldelimeter + "$n4" + img_id_name[3] + lnldelimeter + "$d1" + img_id_date[0] + lnldelimeter + "$d2" + img_id_date[1] + lnldelimeter + "$d3" + img_id_date[2] + lnldelimeter + "$d4" + img_id_date[3] + lnldelimeter + "$p1" + img_id_pos[0] + lnldelimeter + "$p2" + img_id_pos[1] + lnldelimeter + "$p3" + img_id_pos[2] + lnldelimeter + "$p4" + img_id_pos[3]

    l_order = get_cache (L_order, {
        "lief_nr": [(eq, l_orderhdr.lief_nr)],
        "docu_nr": [(eq, docunr)],
        "pos": [(eq, 0)]})
    l_order.gedruckt = get_current_date()
    l_order.zeit = get_current_time_in_seconds()
    pass

    return generate_output()