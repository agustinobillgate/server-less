#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# - Missing table fa_order in field discount2
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Printer, Htparam, Fa_ordheader, Waehrung, L_lieferant, Gl_department, Briefzei, L_artikel, Fa_order, Mathis, Printcod, Parameters

def fa_pchase_parser_webbl(briefnr:int, docu_nr:string, printnr:int):

    prepare_cache ([Printer, Htparam, Fa_ordheader, Waehrung, L_lieferant, Briefzei, Fa_order, Mathis])

    err = 0
    outfile = ""
    printer_pglen = 0
    supplier_name = ""
    bill_recv = ""
    address1 = ""
    address2 = ""
    order_date = None
    deliv_date = None
    telefon = ""
    fax = ""
    pr_nr = ""
    output_list_data = []
    op_list_data = []
    long_digit:bool = False
    price_decimal:int = 0
    foreign_currency:bool = False
    saldo:Decimal = to_decimal("0.0")
    bl_balance:Decimal = to_decimal("0.0")
    tot_qty:Decimal = to_decimal("0.0")
    currloop:int = 0
    pos_bez:int = 0
    keychar:string = ""
    remain_bez:string = ""
    pr:string = ""
    curr_line:int = 0
    curr_page:int = 0
    curr_pos:int = 0
    blloop:int = 0
    headloop:int = 0
    f_lmargin:bool = False
    lmargin:int = 1
    n:int = 0
    disc2_flag:bool = False
    remark_len:int = 24
    bez_len:int = 35
    pos_ord:int = 0
    ord_len:int = 35
    ntab:int = 1
    nskip:int = 1
    a:int = 0
    printer = htparam = fa_ordheader = waehrung = l_lieferant = gl_department = briefzei = l_artikel = fa_order = mathis = printcod = parameters = None

    output_list = op_list = header_list = loop1_list = loop_list = brief_list = htp_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string, "pos":int})
    op_list_data, Op_list = create_model("Op_list", {"artnr":int, "anzahl":Decimal, "bezeich":string, "bez_aend":bool, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "epreis":Decimal, "epreis0":Decimal, "warenwert":Decimal, "konto":string, "warenwert0":Decimal, "remark":string})
    header_list_data, Header_list = create_model("Header_list", {"texte":string})
    loop1_list_data, Loop1_list = create_model("Loop1_list", {"texte":string})
    loop_list_data, Loop_list = create_model("Loop_list", {"texte":string})
    brief_list_data, Brief_list = create_model("Brief_list", {"b_text":string})
    htp_list_data, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        return {"err": err, "outfile": outfile, "printer_pglen": printer_pglen, "supplier_name": supplier_name, "bill_recv": bill_recv, "address1": address1, "address2": address2, "order_date": order_date, "deliv_date": deliv_date, "telefon": telefon, "fax": fax, "pr_nr": pr_nr, "output-list": output_list_data, "op-list": op_list_data}

    def analyse_text():

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        htp_list = query(htp_list_data, filters=(lambda htp_list: htp_list.paramnr == 2300), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            headloop = 1

        htp_list = query(htp_list_data, filters=(lambda htp_list: htp_list.paramnr == 2301), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            headloop = headloop + 1

        htp_list = query(htp_list_data, filters=(lambda htp_list: htp_list.paramnr == 2302), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            blloop = 1

        htp_list = query(htp_list_data, filters=(lambda htp_list: htp_list.paramnr == 2303), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            blloop = blloop + 1


    def build_text_line(curr_texte:string):

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        i:int = 0
        j:int = 1
        n:int = 0
        found:bool = False
        for i in range(1,length(curr_texte)  + 1) :

            if substring(curr_texte, i - 1, 1) == (keychar).lower() :

                if i == length(curr_texte):
                    found = False

                elif substring(curr_texte, i + 1 - 1, 1) == " ":
                    found = False
                else:
                    put_string(substring(curr_texte, j - 1, i - j))
                    i, found = interprete_text(curr_texte, i)
                    j = i + 1
            else:
                found = False

        if not found:
            put_string(substring(curr_texte, j - 1, length(curr_texte) - j + 1))


    def fill_list():

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        i:int = 0
        j:int = 0
        l:int = 0
        n:int = 0
        c:string = ""
        keycont:string = ""
        continued:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 600)]})
        keychar = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1122)]})
        keycont = keychar + htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == 17) & (Htparam.bezeichnung != ("Not used").lower())).order_by(length(Htparam.fchar).desc()).all():
            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.paramnr = htparam.paramnr
            htp_list.fchar = keychar + htparam.fchar

        for briefzei in db_session.query(Briefzei).filter(
                     (Briefzei.briefnr == briefnr)).order_by(Briefzei.briefzeilnr).all():
            j = 1
            for i in range(1,length(briefzei.texte)  + 1) :

                if asc(substring(briefzei.texte, i - 1, 1)) == 10:
                    n = i - j
                    c = substring(briefzei.texte, j - 1, n)
                    l = length(c)

                    if not continued:
                        brief_list = Brief_list()
                        brief_list_data.append(brief_list)

                    brief_list.b_text = brief_list.b_text + c
                    j = i + 1

                    if l > length((keycont).lower() ) and substring(c, l - length((keycont).lower() ) + 1 - 1, length((keycont).lower() )) == (keycont).lower() :
                        continued = True
                        b_text = substring(b_text, 0, length(b_text) - length(keycont))
                    else:
                        continued = False
            n = length(briefzei.texte) - j + 1
            c = substring(briefzei.texte, j - 1, n)

            if not continued:
                brief_list = Brief_list()
                brief_list_data.append(brief_list)

            brief_list.b_text = brief_list.b_text + c


    def do_billhead():

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        n:int = 0
        headloop = 3
        header_list_data.clear()

        for loop1_list in query(loop1_list_data):
            header_list = Header_list()
            header_list_data.append(header_list)

            curr_pos = 1

            if f_lmargin:
                for n in range(1,lmargin + 1) :
                    put_string(" ")
            build_loop_line(loop1_list.texte)
        headloop = 0
        print_billhead()


    def build_loop_line(curr_texte:string):

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        i:int = 0
        j:int = 1
        n:int = 0
        found:bool = False
        for i in range(1,length(curr_texte)  + 1) :

            if substring(curr_texte, i - 1, 1) == (keychar).lower() :

                if i == length(curr_texte):
                    found = False

                elif substring(curr_texte, i + 1 - 1, 1) == " ":
                    found = False
                else:
                    put_string(substring(curr_texte, j - 1, i - j))
                    i, found = interprete_text(curr_texte, i)
                    j = i + 1
            else:
                found = False

        if not found:
            put_string(substring(curr_texte, j - 1, length(curr_texte) - j + 1))


    def do_billline():

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        l_art = None
        create_it:bool = False
        curr_bez:string = ""
        bez_aend:bool = False
        disc:Decimal = to_decimal("0.0")
        disc2:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        L_art =  create_buffer("L_art",L_artikel)
        saldo =  to_decimal("0")
        bl_balance =  to_decimal("0")
        op_list_data.clear()

        for fa_order in db_session.query(Fa_order).filter(
                 (Fa_order.order_nr == (docu_nr).lower()) & (Fa_order.activeflag == 0)).order_by(Fa_order.fa_pos).all():
            create_it = False
            bez_aend = False

            mathis = get_cache (Mathis, {"nr": [(eq, fa_order.fa_nr)]})
            curr_bez = mathis.name
            disc =  to_decimal("0")
            disc2 =  to_decimal("0")
            
            # Rulita, 27-11-2025 | Missing table fa_order in field discount2
            op_list = query(op_list_data, filters=(lambda op_list: op_list.artnr == fa_order.fa_nr and op_list.epreis == fa_order.order_price and op_list.bezeich == mathis.name and op_list.disc == fa_order.discount1 and op_list.disc2 == fa_order.discount2), first=True)

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
        currloop = 0

        for op_list in query(op_list_data):

            if op_list.anzahl == 0:
                op_list_data.remove(op_list)

        mathis_obj_list = {}
        for mathis in db_session.query(Mathis).filter(
                 ((Mathis.nr.in_(list(set([op_list.artnr for op_list in op_list_data])))))).order_by(Mathis._recid).all():
            if mathis_obj_list.get(mathis._recid):
                continue
            else:
                mathis_obj_list[mathis._recid] = True

            if curr_line > printer.pglen:
                curr_page = curr_page + 1
                curr_line = 1
                do_billhead()
            currloop = currloop + 1
            bl_balance =  to_decimal(bl_balance) + to_decimal(op_list.warenwert)
            saldo =  to_decimal(saldo) + to_decimal(op_list.warenwert)

            for loop_list in query(loop_list_data):
                curr_pos = 1
                remain_bez = ""

                if f_lmargin:
                    for n in range(1,lmargin + 1) :
                        put_string(" ")
                build_loop_line(loop_list.texte)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.str = output_list.str + to_string("")
                curr_line = curr_line + 1
                while remain_bez != "":
                    print_bezeich1()
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.str = output_list.str + to_string("")
                    curr_line = curr_line + 1
        loop_list_data.clear()
        blloop = 0


    def print_billhead():

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        i:int = 0

        for header_list in query(header_list_data):
            curr_pos = 1
            for i in range(1,length(header_list.texte)  + 1) :
                output_list.str = output_list.str + to_string(substring(header_list.texte, i - 1, 1) , "x(1)")
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_line = curr_line + 1


    def interprete_text(curr_texte:string, i:int):

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        found = False
        j:int = 0
        rowno:int = 0

        def generate_inner_output():
            return (i, found)

        j = i

        htp_list = query(htp_list_data, first=True)
        while None != htp_list and not found:

            if htp_list.fchar == substring(curr_texte, j - 1, length(htp_list.fchar)):
                found = True
                i = j + length(htp_list.fchar) - 1

                if htp_list.paramnr == 777:
                    disc2_flag = False

                    if substring(curr_texte, i + 1 - 1, 1) == ("2").lower() :
                        disc2_flag = True
                        i = i + 1

                elif htp_list.paramnr == 1005:

                    if substring(curr_texte, i + 1 - 1, 1) >= ("0").lower()  and substring(curr_texte, i + 1 - 1, 1) <= ("9").lower()  and substring(curr_texte, i + 2 - 1, 1) >= ("0").lower()  and substring(curr_texte, i + 2 - 1, 1) <= ("9").lower() :
                        remark_len = to_int(substring(curr_texte, i + 1 - 1, 2))
                        i = i + 2

                elif htp_list.paramnr == 1063:

                    if substring(curr_texte, i + 1 - 1, 1) >= ("0").lower()  and substring(curr_texte, i + 1 - 1, 1) <= ("9").lower()  and substring(curr_texte, i + 2 - 1, 1) >= ("0").lower()  and substring(curr_texte, i + 2 - 1, 1) <= ("9").lower() :
                        rowno = to_int(substring(curr_texte, i + 1 - 1, 2))

                        if rowno > printer.pglen:
                            rowno = printer.pglen
                        i = i + 2

                        if curr_line < rowno:
                            for j in range(1,(rowno - curr_line)  + 1) :
                                output_list.str = output_list.str + to_string(" ")
                                output_list = Output_list()
                                output_list_data.append(output_list)

                            curr_line = rowno
                            curr_pos = 1

                    if curr_line >= printer.pglen:
                        curr_page = curr_page + 1
                        curr_line = 1
                        do_billhead()

                elif htp_list.paramnr == 2306:

                    if substring(curr_texte, i + 1 - 1, 1) >= ("0").lower()  and substring(curr_texte, i + 1 - 1, 1) <= ("9").lower()  and substring(curr_texte, i + 2 - 1, 1) >= ("0").lower()  and substring(curr_texte, i + 2 - 1, 1) <= ("9").lower() :
                        bez_len = to_int(substring(curr_texte, i + 1 - 1, 2))
                        i = i + 2

                elif htp_list.paramnr == 692:
                    pos_ord = curr_pos

                    if substring(curr_texte, i + 1 - 1, 1) >= ("0").lower()  and substring(curr_texte, i + 1 - 1, 1) <= ("9").lower()  and substring(curr_texte, i + 2 - 1, 1) >= ("0").lower()  and substring(curr_texte, i + 2 - 1, 1) <= ("9").lower() :
                        ord_len = to_int(substring(curr_texte, i + 1 - 1, 2))

                        if bez_len > ord_len:
                            ord_len = bez_len
                        i = i + 2
                i = decode_key(curr_texte, htp_list.paramnr, i)

            htp_list = query(htp_list_data, next=True)

        if not found:
            put_string(substring(curr_texte, j - 1, 1))

        return generate_inner_output()


    def decode_key(curr_texte:string, paramnr:int, i:int):

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        out_str:string = ""
        status_code:int = 0
        n:int = 0
        m:int = 0

        def generate_inner_output():
            return (i)

        out_str, status_code = decode_key1(htparam.paramnr)

        if status_code >= 1 and status_code <= 5:
            i = find_parameter(htparam.paramnr, curr_texte, status_code, i)

        if status_code == 1:
            m = curr_pos + 1

            if curr_pos > ntab:
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_line = curr_line + 1
                curr_pos = 1
                for n in range(2,ntab + 1) :
                    put_string(" ")
            else:
                for n in range(m,ntab + 1) :
                    put_string(" ")
            curr_pos = ntab

        elif status_code == 2 and headloop == 0 and blloop == 0:
            for n in range(1,nskip + 1) :
                output_list.str = output_list.str + to_string("")
                output_list = Output_list()
                output_list_data.append(output_list)

                curr_pos = 1
                curr_line = curr_line + 1

        elif status_code == 3:
            for n in range(1,lmargin + 1) :
                put_string(" ")

        return generate_inner_output()


    def find_parameter(paramnr:int, curr_texte:string, status_code:int, i:int):

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        j:int = 0
        n:int = 0
        stopped:bool = False

        def generate_inner_output():
            return (i)


        htp_list = query(htp_list_data, filters=(lambda htp_list: htp_list.paramnr == paramnr), first=True)
        j = i + 1
        while not stopped:

            if substring(curr_texte, j - 1, 1) < ("0").lower()  or substring(curr_texte, j - 1, 1) > ("9").lower() :
                stopped = True
            else:
                j = j + 1

        if j > (i + 1):
            j = j - 1
            n = to_int(substring(curr_texte, i + 1 - 1, j - i))

            if status_code == 1:
                ntab = n

            elif status_code == 2:
                nskip = n

            elif status_code == 3:
                lmargin = n
            i = j

        return generate_inner_output()


    def decode_key1(paramnr:int):

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        out_str = ""
        status_code = 0
        i:int = 0
        n:int = 0
        curr_bez:string = ""
        l_od0 = None
        docu_str:string = ""
        c:string = ""
        len_:int = 0

        def generate_inner_output():
            return (out_str, status_code)


        htparam = get_cache (Htparam, {"paramnr": [(eq, paramnr)]})

        if htparam.paramnr == 601:
            pass

        elif htparam.paramnr == 602:
            put_string(to_string(curr_page))

        elif htparam.paramnr == 603:
            status_code = 1

        elif htparam.paramnr == 604:
            put_string(to_string(get_current_date()))

        elif htparam.paramnr == 605:
            status_code = 2

        elif htparam.paramnr == 637 and l_lieferant:
            put_string(l_lieferant.namekontakt + ", " + l_lieferant.vorname1 + " " + l_lieferant.anrede1)

        elif htparam.paramnr == 664 and l_lieferant:
            put_string(l_lieferant.firma)

        elif htparam.paramnr == 643 and l_lieferant:
            put_string(trim(l_lieferant.adresse1))

        elif htparam.paramnr == 644 and l_lieferant:
            put_string(trim(l_lieferant.adresse2))

        elif htparam.paramnr == 645 and l_lieferant:
            put_string(trim(l_lieferant.adresse3))

        elif htparam.paramnr == 646 and l_lieferant:
            put_string(trim(l_lieferant.land))

        elif htparam.paramnr == 647 and l_lieferant:
            put_string(to_string(l_lieferant.plz))

        elif htparam.paramnr == 648 and l_lieferant:
            put_string(trim(l_lieferant.wohnort))

        elif htparam.paramnr == 691 and l_lieferant:
            put_string(trim(l_lieferant.fax))

        elif htparam.paramnr == 382 and l_lieferant:
            put_string(trim(l_lieferant.telefon))

        elif htparam.paramnr == 616:
            f_lmargin = True
            status_code = 3

        elif htparam.paramnr == 617:
            f_lmargin = False

        elif (htparam.paramnr >= 618) and (htparam.paramnr <= 629):

            htparam = get_cache (Htparam, {"paramnr": [(eq, paramnr)]})

            printcod = get_cache (Printcod, {"emu": [(eq, printer.emu)],"code": [(eq, htparam.fchar)]})

            if printcod:
                put_string(trim(printcod.contcod))

        elif htparam.paramnr == 652:
            L_od0 =  create_buffer("L_od0",Fa_ordheader)

            l_od0 = get_cache (Fa_ordheader, {"order_nr": [(eq, docu_nr)],"supplier_nr": [(eq, fa_ordheader.supplier_nr)]})
            put_string(to_string(l_od0.pr_nr))

        elif htparam.paramnr == 661:
            put_string(to_string(fa_ordheader.credit_term))

        elif htparam.paramnr == 672:
            put_string(to_string(fa_ordheader.order_date))

        elif htparam.paramnr == 655:
            put_string(to_string(fa_ordheader.expected_delivery))

        elif htparam.paramnr == 673:
            docu_str = docu_nr

            if fa_ordheader.created_time > 0:
                docu_str = docu_str + "*"
            put_string(to_string(docu_str))

        elif htparam.paramnr == 727:
            put_string(to_string(fa_ordheader.paymentdate))

        elif htparam.paramnr == 1088:

            parameters = db_session.query(Parameters).filter(
                     (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == fa_ordheader.dept_nr)).first()

            if parameters:
                put_string(trim(parameters.vstring))

        elif htparam.paramnr == 1107:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, fa_ordheader.currency)]})

            if waehrung:
                put_string(to_string(waehrung.wabkurz))

        elif htparam.paramnr == 2302:
            status_code = 6

        elif htparam.paramnr == 2303:
            status_code = 7

        elif htparam.paramnr == 633:
            output_list.str = output_list.str + to_string(currloop, ">>9")
            curr_pos = curr_pos + 3

        elif htparam.paramnr == 2320:
            pass

        elif htparam.paramnr == 675:
            output_list.str = output_list.str + to_string(tot_qty, "->,>>9.9")
            curr_pos = curr_pos + 8

        elif htparam.paramnr == 692:
            print_instruction()

        elif htparam.paramnr == 1004 and fa_ordheader:
            put_string(trim(fa_ordheader.order_name))

        elif htparam.paramnr == 1005:
            for i in range(1,remark_len + 1) :

                if op_list:

                    if length(op_list.remark) >= i:
                        output_list.str = output_list.str + to_string(substring(op_list.remark, i - 1, 1) , "x(1)")
                    else:
                        output_list.str = output_list.str + to_string(" ", "x(1)")
                    curr_pos = curr_pos + 1

        elif htparam.paramnr == 2304:
            output_list.str = output_list.str + to_string(mathis.nr, "9999999")
            curr_pos = curr_pos + 7

        elif htparam.paramnr == 2305:

            if op_list:

                if op_list.anzahl >= 10000 or (- op_list.anzahl >= 10000):
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>9")

                elif op_list.anzahl >= 1000 or (- op_list.anzahl >= 1000):

                    if op_list.anzahl >= 0:
                        output_list.str = output_list.str + to_string(op_list.anzahl, ">,>>9.99")
                    else:
                        output_list.str = output_list.str + to_string(op_list.anzahl, "->,>>9.9")
                else:

                    if length(to_string(op_list.anzahl - round(op_list.anzahl - 0.5, 0))) > 3:
                        output_list.str = output_list.str + to_string(op_list.anzahl, "->>9.999")
                    else:
                        output_list.str = output_list.str + to_string(op_list.anzahl, "->>9.99 ")
                curr_pos = curr_pos + 8

        elif htparam.paramnr == 2306:
            pos_bez = curr_pos

            if op_list:
                curr_bez = op_list.bezeich

                if not op_list.bez_aend:
                    for i in range(1,bez_len + 1) :

                        if length(curr_bez) >= i:
                            output_list.str = output_list.str + to_string(substring(curr_bez, i - 1, 1) , "x(1)")
                        else:
                            output_list.str = output_list.str + to_string(" ", "x(1)")
                    curr_pos = curr_pos + bez_len
                else:
                    print_bezeich(curr_bez)

        elif htparam.paramnr == 710:

            if op_list:
                c = convert_fibu(op_list.konto)
            len_ = length(c)
            for i in range(1,len + 1) :
                output_list.str = output_list.str + to_string(substring(c, i - 1, 1) , "x(1)")
            curr_pos = curr_pos + len

        elif htparam.paramnr == 777:

            if op_list:

                if disc2_flag == False:
                    output_list.str = output_list.str + to_string(op_list.disc, ">9.99")
                else:
                    output_list.str = output_list.str + to_string(op_list.disc2, ">9.99")
                curr_pos = curr_pos + 5

        elif htparam.paramnr == 779:

            if op_list:

                if not long_digit:

                    if op_list.epreis >= 10000000:
                        output_list.str = output_list.str + to_string(op_list.epreis0, "->>,>>>,>>>,>>>,>>9")
                    else:
                        output_list.str = output_list.str + to_string(op_list.epreis0, "->>>,>>>,>>>,>>9.99")
                    curr_pos = curr_pos + 12
                else:
                    output_list.str = output_list.str + to_string(op_list.epreis0, "->>,>>>,>>>,>>>,>>9")
                    curr_pos = curr_pos + 13

        elif htparam.paramnr == 780:

            if op_list:
                output_list.str = output_list.str + to_string(op_list.vat, ">9.99")
            curr_pos = curr_pos + 5

        elif htparam.paramnr == 2307:

            if op_list:

                if not long_digit:

                    if op_list.epreis >= 10000000:
                        output_list.str = output_list.str + to_string(op_list.epreis, "->>,>>>,>>>,>>>,>>9")
                    else:
                        output_list.str = output_list.str + to_string(op_list.epreis, "->>>,>>>,>>>,>>9.99")
                    curr_pos = curr_pos + 12
                else:
                    output_list.str = output_list.str + to_string(op_list.epreis, "->>,>>>,>>>,>>>,>>9")
                    curr_pos = curr_pos + 13

        elif htparam.paramnr == 2308:

            if op_list:

                if not long_digit:

                    if price_decimal == 0 and not foreign_currency:
                        output_list.str = output_list.str + to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9")

                    elif price_decimal == 2 or foreign_currency:
                        output_list.str = output_list.str + to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9.99")
                    curr_pos = curr_pos + 11
                else:
                    output_list.str = output_list.str + to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9")
                    curr_pos = curr_pos + 14

        elif htparam.paramnr == 2316:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(bl_balance, "->,>>>,>>>,>>>,>>9")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(bl_balance, "->,>>>,>>>,>>>,>>9.99")
                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(bl_balance, "->,>>>,>>>,>>>,>>9")
                curr_pos = curr_pos + 14

        elif htparam.paramnr == 674:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(saldo, "->>,>>>,>>9")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(saldo, "->>>,>>9.99")
                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(saldo, "->,>>>,>>>,>>9")
                curr_pos = curr_pos + 14

        return generate_inner_output()


    def put_string(str:string):

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        len_:int = 0
        i:int = 0
        len_ = length(str)
        for i in range(1,len + 1) :

            if headloop == 0:
                output_list.str = output_list.str + to_string(substring(str, i - 1, 1) , "x(1)")

            elif headloop == 3:

                if header_list:
                    header_list.texte = header_list.texte + substring(str, i - 1, 1)
        curr_pos = curr_pos + len


    def print_bezeich(curr_bez:string):

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        i:int = 0
        j:int = 0
        curr_pos = curr_pos + bez_len
        for i in range(1,bez_len + 1) :

            if substring(curr_bez, i - 1, 2) == ("\\" + chr_unicode(10).lower()):
                i = i + 1
                remain_bez = substring(curr_bez, (i + 1) - 1, length(curr_bez) - i)
                for j in range(1,(bez_len - i + 2)  + 1) :
                    output_list.str = output_list.str + to_string(" ", "x(1)")

                return

            elif i == length(curr_bez):
                output_list.str = output_list.str + to_string(substring(curr_bez, i - 1, 1) , "x(1)")
                for j in range(1,(bez_len - i)  + 1) :
                    output_list.str = output_list.str + to_string(" ", "x(1)")

                return
            else:
                output_list.str = output_list.str + to_string(substring(curr_bez, i - 1, 1) , "x(1)")
        remain_bez = substring(curr_bez, i - 1, length(curr_bez))


    def print_bezeich1():

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        i:int = 0
        j:int = 0
        for i in range(1,pos_bez - 1 + 1) :
            output_list.str = output_list.str + to_string(" ", "x(1)")
        for i in range(1,bez_len + 1) :

            if substring(remain_bez, i - 1, 2) == ("\\" + chr_unicode(10).lower()):
                i = i + 1
                remain_bez = substring(remain_bez, (i + 1) - 1, length(remain_bez) - i)
                for j in range((bez_len - i),bez_len + 1) :
                    output_list.str = output_list.str + to_string(" ", "x(1)")

                return

            elif i == length(remain_bez):
                output_list.str = output_list.str + to_string(substring(remain_bez, i - 1, 1) , "x(1)")
                for j in range((bez_len - i),bez_len + 1) :
                    output_list.str = output_list.str + to_string(" ", "x(1)")
                remain_bez = ""

                return
            else:
                output_list.str = output_list.str + to_string(substring(remain_bez, i - 1, 1) , "x(1)")
        remain_bez = substring(remain_bez, i - 1, length(remain_bez))


    def print_instruction():

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        i:int = 0
        j:int = 0
        ind:int = 0

        if ord_len > 0:
            print_instruct1()

            return

        if pos_bez == 0:
            output_list.str = output_list.str + to_string("")
            output_list.pos = 20
            ind = 0
            for i in range(1,length(fa_ordheader.order_desc)  + 1) :
                ind = ind + 1

                if ind == 57:
                    output_list.str = output_list.str + to_string("")
                    output_list.pos = 20
                    ind = 1
                    curr_line = curr_line + 1

                if substring(fa_ordheader.order_desc, i - 1, 2) == ("\\" + chr_unicode(10).lower()):
                    output_list.str = output_list.str + to_string("")
                    output_list.pos = 20
                    curr_line = curr_line + 1
                    ind = 1
                    i = i + 1

                elif substring(fa_ordheader.order_desc, i - 1, 1) == chr_unicode(10):
                    output_list.str = output_list.str + to_string(" ", "x(1)")
                else:
                    output_list.str = output_list.str + to_string(substring(fa_ordheader.order_desc, i - 1, 1) , "x(1)")
        else:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_line = curr_line + 1
            for j in range(1,(pos_bez - 1)  + 1) :
                output_list.str = output_list.str + to_string(" ", "x(1)")
            ind = 0
            for i in range(1,length(fa_ordheader.order_desc)  + 1) :
                ind = ind + 1

                if ind == (bez_len + 1):
                    output_list.str = output_list.str + to_string("")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_bez - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")
                    ind = 1

                if substring(fa_ordheader.order_desc, i - 1, 2) == ("\\" + chr_unicode(10).lower()):
                    output_list.str = output_list.str + to_string("")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_bez - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")
                    ind = 1
                    i = i + 1

                elif substring(fa_ordheader.order_desc, i - 1, 1) == chr_unicode(10):
                    output_list.str = output_list.str + to_string(" ", "x(1)")
                else:
                    output_list.str = output_list.str + to_string(substring(fa_ordheader.order_desc, i - 1, 1) , "x(1)")
        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_line = curr_line + 1
        curr_pos = 1


    def print_instruct1():

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        i:int = 0
        j:int = 0
        ind:int = 0
        s:string = ""

        if pos_ord == 0:

            if ord_len >= 75:
                output_list.str = output_list.str + to_string("")
                output_list.pos = 5

            elif ord_len >= 60:
                output_list.str = output_list.str + to_string("")
                output_list.pos = 10

            elif ord_len >= 55:
                output_list.str = output_list.str + to_string("")
                output_list.pos = 15
            else:
                output_list.str = output_list.str + to_string("")
                output_list.pos = 20
            ind = 0
            for i in range(1,length(fa_ordheader.order_desc)  + 1) :
                ind = ind + 1

                if ind > ord_len and substring(fa_ordheader.order_desc, i - 1, 1) == " ":

                    if ord_len >= 80:
                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 5

                    elif ord_len >= 60:
                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 10

                    elif ord_len >= 55:
                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 15
                    else:
                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 20
                    ind = 1

                elif substring(fa_ordheader.order_desc, i - 1, 2) == ("\\" + chr_unicode(10).lower()):

                    if ord_len >= 80:
                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 5

                    elif ord_len >= 60:
                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 10

                    elif ord_len >= 55:
                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 15
                    else:
                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 20
                    ind = 1
                    i = i + 1

                elif substring(fa_ordheader.order_desc, i - 1, 1) == chr_unicode(10):
                    output_list.str = output_list.str + to_string(" ", "x(1)")
                else:
                    output_list.str = output_list.str + to_string(substring(fa_ordheader.order_desc, i - 1, 1) , "x(1)")
        else:
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_line = curr_line + 1
            for j in range(1,(pos_ord - 1)  + 1) :
                output_list.str = output_list.str + to_string(" ", "x(1)")
            ind = 0
            for i in range(1,length(fa_ordheader.order_desc)  + 1) :
                ind = ind + 1

                if ind > ord_len and substring(fa_ordheader.order_desc, i - 1, 1) == " ":
                    output_list.str = output_list.str + to_string("")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_ord - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")
                    ind = 1

                elif substring(fa_ordheader.order_desc, i - 1, 2) == ("\\" + chr_unicode(10).lower()):
                    output_list.str = output_list.str + to_string("")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_ord - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")
                    ind = 1
                    i = i + 1

                elif substring(fa_ordheader.order_desc, i - 1, 1) == chr_unicode(10):
                    output_list.str = output_list.str + to_string(" ", "x(1)")
                else:
                    output_list.str = output_list.str + to_string(substring(fa_ordheader.order_desc, i - 1, 1) , "x(1)")
        output_list.str = output_list.str + to_string("")
        output_list = Output_list()
        output_list_data.append(output_list)

        curr_line = curr_line + 1
        curr_pos = 1


    def convert_fibu(konto:string):

        nonlocal err, outfile, printer_pglen, supplier_name, bill_recv, address1, address2, order_date, deliv_date, telefon, fax, pr_nr, output_list_data, op_list_data, long_digit, price_decimal, foreign_currency, saldo, bl_balance, tot_qty, currloop, pos_bez, keychar, remain_bez, pr, curr_line, curr_page, curr_pos, blloop, headloop, f_lmargin, lmargin, n, disc2_flag, remark_len, bez_len, pos_ord, ord_len, ntab, nskip, a, printer, htparam, fa_ordheader, waehrung, l_lieferant, gl_department, briefzei, l_artikel, fa_order, mathis, printcod, parameters
        nonlocal briefnr, docu_nr, printnr


        nonlocal output_list, op_list, header_list, loop1_list, loop_list, brief_list, htp_list
        nonlocal output_list_data, op_list_data, header_list_data, loop1_list_data, loop_list_data, brief_list_data, htp_list_data

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
        ch = htparam.fchar
        j = 0
        for i in range(1,length(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()


    if printnr == 0:
        outfile = "\\vhp-letter.rtf"
    else:

        printer = get_cache (Printer, {"nr": [(eq, printnr)]})

        if not printer:
            err = 1

            return generate_output()
        else:
            outfile = printer.path
    printer_pglen = printer.pglen

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    fa_ordheader = get_cache (Fa_ordheader, {"order_nr": [(eq, docu_nr)]})

    if not fa_ordheader:
        err = 2

        return generate_output()
    pr = fa_ordheader.pr_nr

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, fa_ordheader.currency)]})

    if waehrung:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

        if htparam.fchar != "" and (htparam.fchar != waehrung.wabkurz):
            foreign_currency = True

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, fa_ordheader.supplier_nr)]})

    gl_department = get_cache (Gl_department, {"nr": [(eq, fa_ordheader.dept_nr)]})

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


    output_list = Output_list()
    output_list_data.append(output_list)

    fill_list()
    curr_line = 1
    curr_page = 1

    for brief_list in query(brief_list_data):
        a = a + 1

    for brief_list in query(brief_list_data):

        if curr_line > printer.pglen:
            curr_page = curr_page + 1
            curr_line = 1
            do_billhead()
        curr_pos = 1
        analyse_text()

        if blloop == 0 and headloop == 0:

            if f_lmargin:
                for n in range(1,lmargin + 1) :
                    put_string(" ")
            build_text_line(brief_list.b_text)
            output_list.str = output_list.str + to_string("")
            output_list = Output_list()
            output_list_data.append(output_list)

            curr_line = curr_line + 1
            curr_pos = 1

        elif blloop == 2:
            loop_list = Loop_list()
            loop_list_data.append(loop_list)

            loop_list.texte = brief_list.b_text
            curr_pos = 1

        elif headloop == 2:
            loop1_list = Loop1_list()
            loop1_list_data.append(loop1_list)

            loop1_list.texte = brief_list.b_text
            curr_pos = 1

        elif blloop == 3:
            do_billline()

        elif headloop == 3:
            do_billhead()

        if blloop == 1:
            blloop = 2

        if headloop == 1:
            headloop = 2

    # fa_ordheader = get_cache (Fa_ordheader, {"supplier_nr": [(eq, fa_ordheader.supplier_nr)],"order_nr": [(eq, docu_nr)]})
    fa_ordheader = db_session().query(Fa_ordheader).filter(
             (Fa_ordheader.supplier_nr == fa_ordheader.supplier_nr) & (Fa_ordheader.order_nr == docu_nr)).first()

    fa_ordheader.printed = get_current_date()
    fa_ordheader.printedtime = get_current_time_in_seconds()
    pass

    return generate_output()
