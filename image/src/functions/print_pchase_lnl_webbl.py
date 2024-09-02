from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Queasy, Paramtext, Htparam, L_orderhdr, L_lieferant, L_order, Parameters, Waehrung, Guestbook, L_artikel

def print_pchase_lnl_webbl(pvilanguage:int, lnldelimeter:str, docunr:str, stattype:int, curr_status:str):
    str3_list_list = []
    esign_print_list = []
    str1_list = []
    str3_list = []
    str1:str = ""
    str2:str = ""
    lvcarea:str = "print_pchase_lnl"
    long_digit:bool = False
    foreign_currency:bool = False
    price_decimal:int = 0
    bill_recv:str = ""
    address1:str = ""
    address2:str = ""
    cp_name:str = ""
    telp:str = ""
    fax_no:str = ""
    bill_no:str = ""
    bill_date:str = ""
    refer:str = ""
    po_source:str = ""
    dep_date:str = ""
    arr_date:str = ""
    delivery_date:str = ""
    bl_descript:str = ""
    bl_qty:str = ""
    d_unit:str = ""
    bl_price:str = ""
    bl_amount:str = ""
    c_exrate:str = ""
    bl_balance:str = ""
    balance:decimal = 0
    remark:str = ""
    bank_name:str = ""
    account:str = ""
    rekening:str = ""
    i:int = 0
    globaldisc:decimal = 0
    companytitle:str = ""
    bl_vat:str = ""
    po_number:str = ""
    htl_name:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    created_by:str = ""
    vat_code:str = ""
    vat1:decimal = 0
    vat2:decimal = 0
    p_app:bool = False
    img_id_name:[str] = ["", "", "", "", ""]
    img_id_date:[str] = ["", "", "", "", ""]
    img_id_pos:[str] = ["", "", "", "", ""]
    queasy = paramtext = htparam = l_orderhdr = l_lieferant = l_order = parameters = waehrung = guestbook = l_artikel = None

    str3_list = esign_print = str1 = str3 = op_list = b_queasy = l_art = None

    str3_list_list, Str3_list = create_model("Str3_list", {"str":str})
    esign_print_list, Esign_print = create_model("Esign_print", {"sign_nr":int, "sign_name":str, "sign_img":bytes, "sign_date":str, "sign_position":str})
    str1_list, str1 = create_model("str1", {"bill_recv":str, "address1":str, "address2":str, "cp_name":str, "telp":str, "fax_no":str, "bill_no":str, "bill_date":date, "refer":str, "po_source":str, "po_number":str, "dep_date":int, "arr_date":date, "created_by":str, "delivery_date":date, "remark":str, "globaldisc":decimal, "bank_name":str, "account":str, "rekening":str, "companytitle":str, "vat_code":str, "afterdisc":decimal, "htl_name":str, "htl_adr":str, "htl_tel":str})
    str3_list, Str3 = create_model("Str3", {"bl_descript":str, "arr_date":str, "bl_qty":str, "d_unit":str, "bl_price":str, "bl_amount":str, "c_exrate":str, "bl_balance":str, "remark":str, "konto":str, "disc":decimal, "disc2":decimal, "vat":decimal, "disc_value":decimal, "disc2_value":decimal, "epreis0":decimal, "bl_vat":str, "artnr":int, "brutto":decimal, "po_nr":str, "po_source":str, "vat1":decimal, "vat2":decimal})
    op_list_list, Op_list = create_model("Op_list", {"artnr":int, "anzahl":decimal, "bezeich":str, "bez_aend":bool, "disc":decimal, "disc2":decimal, "vat":decimal, "epreis":decimal, "epreis0":decimal, "warenwert":decimal, "konto":str, "warenwert0":decimal, "remark":str, "disc_value":decimal, "disc2_value":decimal, "brutto":decimal, "vat_value":decimal, "po_nr":str, "vat_code":str, "vat1":decimal, "vat2":decimal})

    B_queasy = Queasy
    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str3_list_list, esign_print_list, str1_list, str3_list, str1, str2, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, po_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, bl_amount, c_exrate, bl_balance, balance, remark, bank_name, account, rekening, i, globaldisc, companytitle, bl_vat, po_number, htl_name, htl_adr, htl_tel, created_by, vat_code, vat1, vat2, p_app, img_id_name, img_id_date, img_id_pos, queasy, paramtext, htparam, l_orderhdr, l_lieferant, l_order, parameters, waehrung, guestbook, l_artikel
        nonlocal b_queasy, l_art


        nonlocal str3_list, esign_print, str1, str3, op_list, b_queasy, l_art
        nonlocal str3_list_list, esign_print_list, str1_list, str3_list, op_list_list
        return {"str3-list": str3_list_list, "esign-print": esign_print_list, "str1": str1_list, "str3": str3_list}

    def decode_string(in_str:str):

        nonlocal str3_list_list, esign_print_list, str1_list, str3_list, str1, str2, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, po_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, bl_amount, c_exrate, bl_balance, balance, remark, bank_name, account, rekening, i, globaldisc, companytitle, bl_vat, po_number, htl_name, htl_adr, htl_tel, created_by, vat_code, vat1, vat2, p_app, img_id_name, img_id_date, img_id_pos, queasy, paramtext, htparam, l_orderhdr, l_lieferant, l_order, parameters, waehrung, guestbook, l_artikel
        nonlocal b_queasy, l_art


        nonlocal str3_list, esign_print, str1, str3, op_list, b_queasy, l_art
        nonlocal str3_list_list, esign_print_list, str1_list, str3_list, op_list_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()

    def do_billline():

        nonlocal str3_list_list, esign_print_list, str1_list, str3_list, str1, str2, lvcarea, long_digit, foreign_currency, price_decimal, bill_recv, address1, address2, cp_name, telp, fax_no, bill_no, bill_date, refer, po_source, dep_date, arr_date, delivery_date, bl_descript, bl_qty, d_unit, bl_price, bl_amount, c_exrate, bl_balance, balance, remark, bank_name, account, rekening, i, globaldisc, companytitle, bl_vat, po_number, htl_name, htl_adr, htl_tel, created_by, vat_code, vat1, vat2, p_app, img_id_name, img_id_date, img_id_pos, queasy, paramtext, htparam, l_orderhdr, l_lieferant, l_order, parameters, waehrung, guestbook, l_artikel
        nonlocal b_queasy, l_art


        nonlocal str3_list, esign_print, str1, str3, op_list, b_queasy, l_art
        nonlocal str3_list_list, esign_print_list, str1_list, str3_list, op_list_list

        create_it:bool = False
        curr_bez:str = ""
        bez_aend:bool = False
        disc:decimal = 0
        disc2:decimal = 0
        disc_value:decimal = 0
        disc2_value:decimal = 0
        tot_qty:decimal = 0
        vat:decimal = 0
        vat_val:decimal = 0
        L_art = L_artikel
        op_list_list.clear()

        if stattype == 0 or stattype == 2:

            for l_order in db_session.query(L_order).filter(
                    (func.lower(L_order.docu_nr) == (docunr).lower()) &  (L_order.loeschflag <= 1) &  (L_order.pos > 0)).all():
                create_it = False
                bez_aend = False

                l_art = db_session.query(L_art).filter(
                        (L_art.artnr == l_order.artnr)).first()

                if l_art:
                    curr_bez = l_art.bezeich
                    disc = 0
                    disc2 = 0

                    if l_order.quality != "":
                        disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) * 0.01
                        disc_value = to_int(substring(l_order.quality, 18, 18))

                        if len(l_order.quality) > 12:
                            disc2 = to_int(substring(l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) * 0.01
                            disc2_value = to_int(substring(l_order.quality, 36, 18))
                            vat_val = to_int(substring(l_order.quality, 54))

                    if l_art.jahrgang == 0 or len(l_order.stornogrund) <= 12:

                        op_list = query(op_list_list, filters=(lambda op_list :op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich == l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund), first=True)
                    else:
                        curr_bez = substring(l_order.stornogrund, 12, len(l_order.stornogrund))
                        create_it = True
                        bez_aend = True

                    if len(l_order.stornogrund) > 12:
                        curr_bez = substring(l_order.stornogrund, 12)

                    if not op_list or create_it:
                        vat = 0
                        op_list = Op_list()
                        op_list_list.append(op_list)

                        op_list.artnr = l_order.artnr
                        op_list.bezeich = curr_bez
                        op_list.bez_aend = bez_aend
                        op_list.epreis = l_order.einzelpreis
                        op_list.epreis0 = l_order.einzelpreis
                        op_list.konto = l_order.stornogrund
                        op_list.remark = l_order.besteller
                        op_list.po_nr = po_number
                        op_list.vat_code = vat_code
                        op_list.vat1 = vat1
                        op_list.vat2 = vat2

                        if l_order.quality != "":
                            vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) * 0.01
                            op_list.disc = disc
                            op_list.disc2 = disc2
                            op_list.disc_value = disc_value
                            op_list.disc2_value = disc2_value
                            op_list.vat = vat
                            op_list.vat_value = vat_val
                            disc = disc / 100
                            disc2 = disc2 / 100
                            vat = vat / 100


                    op_list.anzahl = op_list.anzahl + l_order.anzahl
                    op_list.warenwert = op_list.warenwert + l_order.warenwert
                    op_list.brutto = (op_list.warenwert + op_list.disc_value + op_list.disc2_value) - vat_val
                    op_list.epreis0 = op_list.brutto / op_list.anzahl
                    op_list.warenwert0 = op_list.warenwert0 + l_order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat)
                    tot_qty = tot_qty + l_order.anzahl

        elif stattype == 1 or stattype == 3:

            for l_order in db_session.query(L_order).filter(
                    (func.lower(L_order.docu_nr) == (docunr).lower()) &  (L_order.loeschflag > 0) &  (L_order.pos > 0)).all():
                create_it = False
                bez_aend = False

                l_art = db_session.query(L_art).filter(
                        (L_art.artnr == l_order.artnr)).first()
                curr_bez = l_art.bezeich
                disc = 0
                disc2 = 0

                if l_order.quality != "":
                    disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) * 0.01
                    disc_value = to_int(substring(l_order.quality, 18, 18))

                    if len(l_order.quality) > 12:
                        disc2 = to_int(substring(l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) * 0.01
                        disc2_value = to_int(substring(l_order.quality, 36, 18))
                        vat_val = to_int(substring(l_order.quality, 54))

                if l_art.jahrgang == 0 or len(l_order.stornogrund) <= 12:

                    op_list = query(op_list_list, filters=(lambda op_list :op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich == l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund), first=True)
                else:
                    curr_bez = substring(l_order.stornogrund, 12, len(l_order.stornogrund))
                    create_it = True
                    bez_aend = True

                if len(l_order.stornogrund) > 12:
                    curr_bez = substring(l_order.stornogrund, 12)

                if not op_list or create_it:
                    vat = 0
                    op_list = Op_list()
                    op_list_list.append(op_list)

                    op_list.artnr = l_order.artnr
                    op_list.bezeich = curr_bez
                    op_list.bez_aend = bez_aend
                    op_list.epreis = l_order.einzelpreis
                    op_list.epreis0 = l_order.einzelpreis
                    op_list.konto = l_order.stornogrund
                    op_list.remark = l_order.besteller
                    op_list.po_nr = po_number
                    op_list.vat_code = vat_code
                    op_list.vat1 = vat1
                    op_list.vat2 = vat2

                    if l_order.quality != "":
                        vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) * 0.01
                        op_list.disc = disc
                        op_list.disc2 = disc2
                        op_list.disc_value = disc_value
                        op_list.disc2_value = disc2_value
                        op_list.vat = vat
                        op_list.vat_value = vat_val
                        disc = disc / 100
                        disc2 = disc2 / 100
                        vat = vat / 100


                op_list.anzahl = op_list.anzahl + l_order.anzahl
                op_list.warenwert = op_list.warenwert + l_order.warenwert
                op_list.brutto = (l_order.warenwert + op_list.disc_value + op_list.disc2_value) - to_int(substring(l_order.quality, 54))
                op_list.epreis0 = op_list.brutto / l_order.anzahl
                op_list.warenwert0 = op_list.warenwert0 + l_order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat)
                tot_qty = tot_qty + l_order.anzahl

        elif stattype == None:

            for l_order in db_session.query(L_order).filter(
                    (func.lower(L_order.docu_nr) == (docunr).lower()) &  (L_order.pos > 0)).all():
                create_it = False
                bez_aend = False

                l_art = db_session.query(L_art).filter(
                        (L_art.artnr == l_order.artnr)).first()
                curr_bez = l_art.bezeich
                disc = 0
                disc2 = 0

                if l_order.quality != "":
                    disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) * 0.01
                    disc_value = to_int(substring(l_order.quality, 18, 18))

                    if len(l_order.quality) > 12:
                        disc2 = to_int(substring(l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) * 0.01
                        disc2_value = to_int(substring(l_order.quality, 36, 18))
                        vat_val = to_int(substring(l_order.quality, 54))

                if l_art.jahrgang == 0 or len(l_order.stornogrund) <= 12:

                    op_list = query(op_list_list, filters=(lambda op_list :op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich == l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund), first=True)
                else:
                    curr_bez = substring(l_order.stornogrund, 12, len(l_order.stornogrund))
                    create_it = True
                    bez_aend = True

                if len(l_order.stornogrund) > 12:
                    curr_bez = substring(l_order.stornogrund, 12)

                if not op_list or create_it:
                    vat = 0
                    op_list = Op_list()
                    op_list_list.append(op_list)

                    op_list.artnr = l_order.artnr
                    op_list.bezeich = curr_bez
                    op_list.bez_aend = bez_aend
                    op_list.epreis = l_order.einzelpreis
                    op_list.epreis0 = l_order.einzelpreis
                    op_list.konto = l_order.stornogrund
                    op_list.remark = l_order.besteller
                    op_list.po_nr = po_number
                    op_list.vat_code = vat_code
                    op_list.vat1 = vat1
                    op_list.vat2 = vat2

                    if l_order.quality != "":
                        vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) * 0.01
                        op_list.disc = disc
                        op_list.disc2 = disc2
                        op_list.disc_value = disc_value
                        op_list.disc2_value = disc2_value
                        op_list.vat = vat
                        op_list.vat_value = vat_val
                        disc = disc / 100
                        disc2 = disc2 / 100
                        vat = vat / 100


                op_list.anzahl = op_list.anzahl + l_order.anzahl
                op_list.warenwert = op_list.warenwert + l_order.warenwert
                op_list.brutto = (l_order.warenwert + op_list.disc_value + op_list.disc2_value) - to_int(substring(l_order.quality, 54))
                op_list.epreis0 = op_list.brutto / l_order.anzahl
                op_list.warenwert0 = op_list.warenwert0 + l_order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat)
                tot_qty = tot_qty + l_order.anzahl

        for op_list in query(op_list_list):

            if op_list.anzahl == 0:
                op_list_list.remove(op_list)


    htl_name = ""

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 240)).first()

    if paramtext and paramtext.ptexte != "":
        htl_name = decode_string(paramtext.ptexte)
    htl_adr = ""

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 201)).first()

    if paramtext:
        htl_adr = paramtext.ptexte
    htl_tel = ""

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 204)).first()

    if paramtext:
        htl_tel = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 71)).first()
    p_app = htparam.flogical

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.docu_nr) == (docunr).lower()) &  (L_orderhdr.lief_nr > 0)).first()

    if not l_orderhdr:

        l_orderhdr = db_session.query(L_orderhdr).filter(
                (func.lower(L_orderhdr.docu_nr) == (docunr).lower()) &  (L_orderhdr.lief_nr == 0)).first()

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == l_orderhdr.lief_nr)).first()

    if l_lieferant:
        for i in range(1,len(l_lieferant.bank)  + 1) :

            if re.match("a/n",substring(l_lieferant.bank, i - 1, 3)):
                break
        bill_recv = l_lieferant.firma
        address1 = l_lieferant.adresse1
        address2 = l_lieferant.adresse2
        cp_name = l_lieferant.namekontakt + ", " + l_lieferant.vorname1 +\
                " " + l_lieferant.anrede1
        telp = l_lieferant.telefon
        fax_no = l_lieferant.fax
        bank_name = substring(l_lieferant.bank, 0, i - 2)
        account = substring(l_lieferant.bank, i + 4 - 1, len(l_lieferant.bank))
        rekening = l_lieferant.kontonr
        companytitle = l_lieferant.anredefirma


        str1 = str1()
        str1_list.append(str1)

        str1.bill_recv = l_lieferant.firma
        str1.address1 = l_lieferant.adresse1
        str1.address2 = l_lieferant.adresse2
        str1.cp_name = l_lieferant.namekontakt + ", " + l_lieferant.vorname1 + " " + l_lieferant.anrede1
        str1.telp = l_lieferant.telefon
        str1.fax_no = l_lieferant.fax
        str1.bank_name = substring(l_lieferant.bank, 0, i - 2)
        str1.account = substring(l_lieferant.bank, i + 4 - 1, len(l_lieferant.bank))
        str1.rekening = l_lieferant.kontonr
        str1.companytitle = l_lieferant.anredefirma

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 219) &  (Queasy.number1 == l_lieferant.lief_nr)).first()

        if queasy:
            vat_code = queasy.char1
            vat1 = queasy.deci1
            vat2 = queasy.deci2


            str1.vat_code = queasy.char1

    if l_orderhdr:
        bill_no = docunr

        l_order = db_session.query(L_order).filter(
                (L_order.lief_nr == l_orderhdr.lief_nr) &  (func.lower(L_order.docu_nr) == (docunr).lower()) &  (L_order.pos == 0)).first()

        if l_order:

            if l_order.zeit > 0:

                if curr_status.lower()  == "design":
                    bill_no = docunr + "-REPRINT"
                else:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 240) &  (Queasy.char1 == l_order.docu_nr)).first()

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
            globaldisc = l_order.warenwert


            str1.refer = refer
            str1.globaldisc = globaldisc
            str1.bill_no = bill_no


        bill_date = to_string(l_orderhdr.bestelldatum)
        dep_date = to_string(l_orderhdr.angebot_lief[1])
        remark = l_orderhdr.lief_fax[2]
        arr_date = to_string(l_orderhdr.lieferdatum)
        delivery_date = to_string(l_orderhdr.lieferdatum)
        po_number = l_order.docu_nr
        created_by = to_string(l_orderhdr.besteller)


        str1.bill_date = l_orderhdr.bestelldatum
        str1.dep_date = l_orderhdr.angebot_lief[1]
        str1.remark = remark
        str1.arr_date = l_orderhdr.lieferdatum
        str1.delivery_date = l_orderhdr.lieferdatum
        str1.po_number = po_number
        str1.created_by = l_orderhdr.besteller

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

        if parameters:
            po_source = parameters.vstring

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == l_orderhdr.angebot_lief[2])).first()

        if waehrung:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 152)).first()

            if htparam.fchar != "" and (htparam.fchar != waehrung.wabkurz):
                foreign_currency = True
            c_exrate = to_string(waehrung.wabkurz)

        if p_app:

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 245) &  (func.lower(Queasy.char1) == (docunr).lower())).all():

                guestbook = db_session.query(Guestbook).filter(
                        (Guestbook.gastnr == queasy.number2) &  (Guestbook.reserve_logic[1])).first()

                if guestbook:
                    esign_print = Esign_print()
                    esign_print_list.append(esign_print)

                    esign_print.sign_nr = queasy.number1
                    esign_print.sign_name = entry(1, guestbook.infostr, "|")
                    esign_print.sign_img = guestbook.imagefile
                    esign_print.sign_date = entry(1, queasy.char3, "|")
                    esign_print.sign_position = entry(3, guestbook.infostr, "|")
                    img_id_name[queasy.number1 - 1] = entry(1, guestbook.infostr, "|")
                    img_id_date[queasy.number1 - 1] = entry(1, queasy.char3, "|")
                    img_id_pos[queasy.number1 - 1] = entry(3, guestbook.infostr, "|")


    str1 = "$bill_recv" + bill_recv + lnldelimeter + "$address1" + address1 + lnldelimeter + "$address2" + address2 + lnldelimeter + "$name" + cp_name + lnldelimeter + "$telp" + telp + lnldelimeter + "$fax_no" + fax_no + lnldelimeter + "$bill_no" + bill_no + lnldelimeter + "$bill_date" + bill_date + lnldelimeter + "$refer" + refer + lnldelimeter + "$source" + po_source + lnldelimeter + "$dep_date" + dep_date + lnldelimeter + "$arr_date" + arr_date + lnldelimeter + "$delivery_date" + delivery_date + lnldelimeter + "$remark" + remark + lnldelimeter + "$GlobDisc" + to_string(globaldisc, "->>>,>>>,>>9.99") + lnldelimeter + "$bankname" + bank_name + lnldelimeter + "$account" + account + lnldelimeter + "$rekening" + rekening + lnldelimeter + "$title" + companytitle
    str2 = translateExtended ("DESCRIPTION", lvcarea, "") + lnldelimeter + translateExtended ("DELIVDATE", lvcarea, "") + lnldelimeter + translateExtended ("QTY", lvcarea, "") + lnldelimeter + translateExtended ("UNIT", lvcarea, "") + lnldelimeter + translateExtended ("PRICE UNIT", lvcarea, "") + lnldelimeter + translateExtended ("AMOUNT", lvcarea, "") + lnldelimeter + translateExtended ("disc", lvcarea, "") + lnldelimeter + translateExtended ("disc2", lvcarea, "") + lnldelimeter + translateExtended ("vat", lvcarea, "") + lnldelimeter + translateExtended ("PO Number", lvcarea, "")
    do_billline()

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

            if len(to_string(op_list.anzahl - round(op_list.anzahl - 0.5, 0))) > 3:
                bl_qty = to_string(op_list.anzahl, "->>9.999")
            else:
                bl_qty = to_string(op_list.anzahl, "->>9.99")

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == op_list.artnr)).first()

        if l_artikel:
            d_unit = l_artikel.traubensort
        balance = balance + op_list.warenwert

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


        str3_list = Str3_list()
        str3_list_list.append(str3_list)

        str3_list.str = bl_descript + lnldelimeter + arr_date + lnldelimeter + bl_qty + lnldelimeter + d_unit + lnldelimeter + bl_price + lnldelimeter + bl_amount + lnldelimeter + c_exrate + lnldelimeter + bl_balance + lnldelimeter + op_list.remark + lnldelimeter + op_list.konto + lnldelimeter + to_string(op_list.disc, "->>9.99") + lnldelimeter + to_string(op_list.disc2, "->>9.99") + lnldelimeter + to_string(op_list.vat, "->>9.99") + lnldelimeter + to_string(op_list.disc_value, "->>>,>>>,>>>,>>9") + lnldelimeter + to_string(op_list.disc2_value, "->>>,>>>,>>>,>>9") + lnldelimeter + to_string(op_list.epreis0, ">>,>>>,>>>,>>>,>>9") + lnldelimeter + bl_vat + lnldelimeter + to_string(op_list.artnr, ">>>>>>>9") + lnldelimeter + to_string(op_list.brutto, ">>>,>>>,>>>,>>9") + lnldelimeter + po_nr + lnldelimeter + po_source + lnldelimeter + to_string(vat1, "->,>>>,>>>,>>>,>>9.99") + lnldelimeter + to_string(vat2, "->,>>>,>>>,>>>,>>9.99")
        str3 = Str3()
        str3_list.append(str3)

        str3.bl_descript = bl_descript
        str3.arr_date = arr_date
        str3.bl_qty = bl_qty
        str3.d_unit = d_unit
        str3.bl_price = bl_price
        str3.bl_amount = bl_amount
        str3.c_exrate = c_exrate
        str3.bl_balance = bl_balance
        str3.remark = op_list.remark
        str3.konto = op_list.konto
        str3.disc = op_list.disc
        str3.disc2 = op_list.disc2
        str3.vat = op_list.vat
        str3.disc_value = op_list.disc_value
        str3.disc2_value = op_list.disc2_value
        str3.epreis0 = op_list.epreis0
        str3.bl_vat = bl_vat
        str3.artnr = op_list.artnr
        str3.brutto = op_list.brutto
        str3.po_nr = op_list.po_nr
        str3.po_source = po_source
        str3.vat1 = vat1
        str3.vat2 = vat2


    str1 = str1 + lnldelimeter + "$AfterDisc" + to_string(balance - globaldisc, "->>>,>>>,>>9.99") + lnldelimeter + "$HN" + htl_name + lnldelimeter + "$HA" + htl_adr + lnldelimeter + "$HT" + htl_tel + lnldelimeter + "$CreatedBy" + created_by + lnldelimeter + "$VC" + vat_code + lnldelimeter + "$n1" + img_id_name[0] + lnldelimeter + "$n2" + img_id_name[1] + lnldelimeter + "$n3" + img_id_name[2] + lnldelimeter + "$n4" + img_id_name[3] + lnldelimeter + "$d1" + img_id_date[0] + lnldelimeter + "$d2" + img_id_date[1] + lnldelimeter + "$d3" + img_id_date[2] + lnldelimeter + "$d4" + img_id_date[3] + lnldelimeter + "$p1" + img_id_pos[0] + lnldelimeter + "$p2" + img_id_pos[1] + lnldelimeter + "$p3" + img_id_pos[2] + lnldelimeter + "$p4" + img_id_pos[3]
    str1.afterdisc = balance - globaldisc
    str1.htl_name = htl_name
    str1.htl_adr = htl_adr
    str1.htl_tel = htl_tel

    l_order = db_session.query(L_order).filter(
            (L_order.lief_nr == l_orderhdr.lief_nr) &  (func.lower(L_order.docu_nr) == (docunr).lower()) &  (L_order.pos == 0)).first()
    l_order.gedruckt = get_current_date()
    l_order.zeit = get_current_time_in_seconds()

    l_order = db_session.query(L_order).first()

    return generate_output()