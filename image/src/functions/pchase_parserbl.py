from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Htparam, L_orderhdr, L_order, Waehrung, L_lieferant, Gl_department, Printer, Briefzei, L_artikel, Printcod, Queasy, Parameters

def pchase_parserbl(briefnr:int, printnr:int, docu_nr:str):
    outfile = ""
    printer_pglen = 0
    err_code = 0
    output_list_list = []
    f_page:bool = True
    foot_text1:str = ""
    foot_char2:str = ""
    foreign_currency:bool = False
    currloop:int = 0
    betrag:decimal = 0
    saldo:decimal = 0
    bl_balance:decimal = 0
    tot_qty:decimal = 0
    pos_bez:int = 0
    bez_len:int = 35
    remark_len:int = 24
    pos_ord:int = 0
    ord_len:int = 35
    remain_bez:str = ""
    disc2_flag:bool = False
    pr:str = ""
    f_lmargin:bool = False
    headloop:int = 0
    blloop:int = 0
    lmargin:int = 1
    nskip:int = 1
    ntab:int = 1
    n:int = 0
    curr_pos:int = 0
    curr_line:int = 0
    curr_page:int = 0
    buttom_line:int = 0
    keychar:str = ""
    price_decimal:int = 0
    globaldisc:decimal = 0
    long_digit:bool = False
    htparam = l_orderhdr = l_order = waehrung = l_lieferant = gl_department = printer = briefzei = l_artikel = printcod = queasy = parameters = None

    output_list = op_list = brief_list = htp_list = loop_list = loop1_list = header_list = l_art = l_od0 = None

    output_list_list, Output_list = create_model("Output_list", {"str":str, "pos":int})
    op_list_list, Op_list = create_model("Op_list", {"artnr":int, "anzahl":decimal, "bezeich":str, "bez_aend":bool, "disc":decimal, "disc2":decimal, "vat":decimal, "epreis":decimal, "epreis0":decimal, "warenwert":decimal, "konto":str, "warenwert0":decimal, "remark":str})
    brief_list_list, Brief_list = create_model("Brief_list", {"b_text":str})
    htp_list_list, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":str})
    loop_list_list, Loop_list = create_model("Loop_list", {"texte":str})
    loop1_list_list, Loop1_list = create_model("Loop1_list", {"texte":str})
    header_list_list, Header_list = create_model("Header_list", {"texte":str})

    L_art = L_artikel
    L_od0 = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list
        return {"outfile": outfile, "printer_pglen": printer_pglen, "err_code": err_code, "output-list": output_list_list}

    def fill_list():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        i:int = 0
        j:int = 0
        l:int = 0
        n:int = 0
        c:str = ""
        keycont:str = ""
        continued:bool = False

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 600)).first()
        keychar = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1122)).first()
        keycont = keychar + htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramgruppe == 17) &  (func.lower(Htparam.bezeich) != "Not used")).all():
            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.paramnr = htparam.paramnr
            htp_list.fchar = keychar + htparam.fchar
        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9990
        htp_list.fchar = keychar + "Globdisc"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9989
        htp_list.fchar = keychar + "AfterDisc"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9991
        htp_list.fchar = keychar + "createdby"

        for briefzei in db_session.query(Briefzei).filter(
                    (Briefzei.briefnr == briefnr)).all():
            j = 1
            for i in range(1,len(briefzei.texte)  + 1) :

                if ord(substring(briefzei.texte, i - 1, 1)) == 10:
                    n = i - j
                    c = substring(briefzei.texte, j - 1, n)
                    l = len(c)

                    if not continued:
                        brief_list = Brief_list()
                    brief_list_list.append(brief_list)

                    brief_list.b_text = brief_list.b_text + c
                    j = i + 1

                    if l > len((keycont).lower() ) and substring(c, l - len((keycont).lower() ) + 1 - 1, len((keycont).lower() )) == (keycont).lower() :
                        continued = True
                        b_text = substring(b_text, 0, len(b_text) - len(keycont))
                    else:
                        continued = False
            n = len(briefzei.texte) - j + 1
            c = substring(briefzei.texte, j - 1, n)

            if not continued:
                brief_list = Brief_list()
            brief_list_list.append(brief_list)

            brief_list.b_text = brief_list.b_text + c

    def analyse_text():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        htp_list = query(htp_list_list, filters=(lambda htp_list :htp_list.paramnr == 2300), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            headloop = 1

        htp_list = query(htp_list_list, filters=(lambda htp_list :htp_list.paramnr == 2301), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            headloop = headloop + 1

        htp_list = query(htp_list_list, filters=(lambda htp_list :htp_list.paramnr == 2302), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            blloop = 1

        htp_list = query(htp_list_list, filters=(lambda htp_list :htp_list.paramnr == 2303), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            blloop = blloop + 1

    def build_text_line(curr_texte:str):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        i:int = 0
        j:int = 1
        n:int = 0
        found:bool = False
        for i in range(1,len(curr_texte)  + 1) :

            if substring(curr_texte, i - 1, 1) == (keychar).lower() :

                if i == len(curr_texte):
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
            put_string(substring(curr_texte, j - 1, len(curr_texte) - j + 1))

    def build_loop_line(curr_texte:str):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        i:int = 0
        j:int = 1
        n:int = 0
        found:bool = False
        for i in range(1,len(curr_texte)  + 1) :

            if substring(curr_texte, i - 1, 1) == (keychar).lower() :

                if i == len(curr_texte):
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
            put_string(substring(curr_texte, j - 1, len(curr_texte) - j + 1))

    def do_billline():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        create_it:bool = False
        curr_bez:str = ""
        bez_aend:bool = False
        disc:decimal = 0
        disc2:decimal = 0
        vat:decimal = 0
        L_art = L_artikel
        saldo = 0
        bl_balance = 0
        op_list_list.clear()

        l_order_obj_list = []
        for l_order, l_art in db_session.query(L_order, L_art).join(L_art,(L_art.artnr == L_order.artnr)).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.loeschflag <= 1) &  (L_order.pos > 0)).all():
            if l_order._recid in l_order_obj_list:
                continue
            else:
                l_order_obj_list.append(l_order._recid)


            create_it = False
            bez_aend = False
            curr_bez = l_art.bezeich
            disc = 0
            disc2 = 0

            if l_order.quality != "":
                disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) * 0.01

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

                if l_order.quality != "":
                    vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) * 0.01
                    op_list.disc = disc
                    op_list.disc2 = disc2
                    op_list.vat = vat
                    disc = disc / 100
                    disc2 = disc2 / 100
                    vat = vat / 100
            op_list.epreis0 = l_order.einzelpreis / (1 - disc) / (1 - disc2) / (1 + vat)
            op_list.anzahl = op_list.anzahl + l_order.anzahl
            op_list.warenwert = op_list.warenwert + l_order.warenwert
            op_list.warenwert0 = op_list.warenwert0 + l_order.warenwert / (1 - disc) / (1 - disc2) / (1 + vat)
            tot_qty = tot_qty + l_order.anzahl
        currloop = 0

        for op_list in query(op_list_list):

            if op_list.anzahl == 0:
                op_list_list.remove(op_list)

        for op_list in query(op_list_list):
            l_artikel = db_session.query(L_artikel).filter((L_artikel.artnr == op_list.artnr)).first()
            if not l_artikel:
                continue


            if curr_line > printer.pglen:
                curr_page = curr_page + 1
                curr_line = 1
                do_billhead()
            currloop = currloop + 1
            bl_balance = bl_balance + op_list.warenwert
            saldo = saldo + op_list.warenwert

            for loop_list in query(loop_list_list):
                curr_pos = 1
                remain_bez = ""

                if f_lmargin:
                    for n in range(1,lmargin + 1) :
                        put_string(" ")
                build_loop_line(loop_list.texte)
                output_list.str = output_list.str + to_string("")


                output_list = Output_list()
                output_list_list.append(output_list)

                curr_line = curr_line + 1
                while remain_bez != "":
                    print_bezeich1()
                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_line = curr_line + 1
        loop_list_list.clear()
        blloop = 0

    def do_billhead():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        n:int = 0
        headloop = 3
        header_list_list.clear()

        for loop1_list in query(loop1_list_list):
            header_list = Header_list()
            header_list_list.append(header_list)

            curr_pos = 1

            if f_lmargin:
                for n in range(1,lmargin + 1) :
                    put_string(" ")
            build_loop_line(loop1_list.texte)
        headloop = 0
        print_billhead()

    def print_billhead():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        i:int = 0

        for header_list in query(header_list_list):
            curr_pos = 1
            for i in range(1,len(header_list.texte)  + 1) :
                output_list.str = output_list.str + to_string(substring(header_list.texte, i - 1, 1) , "x(1)")


            output_list.str = output_list.str + to_string("")


            output_list = Output_list()
            output_list_list.append(output_list)

            curr_line = curr_line + 1

    def interprete_text(curr_texte:str, i:int):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        found = False
        j:int = 0
        rowno:int = 0

        def generate_inner_output():
            return found
        j = i

        htp_list = query(htp_list_list, first=True)
        while None != htp_list and not found:

            if htp_list.fchar == substring(curr_texte, j - 1, len(htp_list.fchar)):
                found = True
                i = j + len(htp_list.fchar) - 1

                if htp_list.paramnr == 777:
                    disc2_flag = False

                    if substring(curr_texte, i + 1 - 1, 1) == "2":
                        disc2_flag = True
                        i = i + 1

                elif htp_list.paramnr == 1005:

                    if substring(curr_texte, i + 1 - 1, 1) >= "0" and substring(curr_texte, i + 1 - 1, 1) <= "9" and substring(curr_texte, i + 2 - 1, 1) >= "0" and substring(curr_texte, i + 2 - 1, 1) <= "9":
                        remark_len = to_int(substring(curr_texte, i + 1 - 1, 2))
                        i = i + 2

                elif htp_list.paramnr == 1063:

                    if substring(curr_texte, i + 1 - 1, 1) >= "0" and substring(curr_texte, i + 1 - 1, 1) <= "9" and substring(curr_texte, i + 2 - 1, 1) >= "0" and substring(curr_texte, i + 2 - 1, 1) <= "9":
                        rowno = to_int(substring(curr_texte, i + 1 - 1, 2))

                        if rowno > printer.pglen:
                            rowno = printer.pglen
                        i = i + 2

                        if curr_line < rowno:
                            for j in range(1,(rowno - curr_line)  + 1) :
                                output_list.str = output_list.str + to_string("")


                                output_list = Output_list()
                                output_list_list.append(output_list)

                            curr_line = rowno
                            curr_pos = 1

                    if curr_line >= printer.pglen:
                        curr_page = curr_page + 1
                        curr_line = 1
                        do_billhead()

                elif htp_list.paramnr == 2306:

                    if substring(curr_texte, i + 1 - 1, 1) >= "0" and substring(curr_texte, i + 1 - 1, 1) <= "9" and substring(curr_texte, i + 2 - 1, 1) >= "0" and substring(curr_texte, i + 2 - 1, 1) <= "9":
                        bez_len = to_int(substring(curr_texte, i + 1 - 1, 2))
                        i = i + 2

                elif htp_list.paramnr == 692:
                    pos_ord = curr_pos

                    if substring(curr_texte, i + 1 - 1, 1) >= "0" and substring(curr_texte, i + 1 - 1, 1) <= "9" and substring(curr_texte, i + 2 - 1, 1) >= "0" and substring(curr_texte, i + 2 - 1, 1) <= "9":
                        ord_len = to_int(substring(curr_texte, i + 1 - 1, 2))

                        if bez_len > ord_len:
                            ord_len = bez_len
                        i = i + 2
                i = decode_key(curr_texte, htp_list.paramnr, i)

            htp_list = query(htp_list_list, next=True)

        if not found:
            put_string(substring(curr_texte, j - 1, 1))


        return generate_inner_output()

    def decode_key(curr_texte:str, paramnr:int, i:int):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        out_str:str = ""
        status_code:int = 0
        n:int = 0
        m:int = 0
        out_str, status_code = decode_key1(paramnr)

        if status_code >= 1 and status_code <= 5:
            i = find_parameter(paramnr, curr_texte, status_code, i)

        if status_code == 1:
            m = curr_pos + 1

            if curr_pos > ntab:
                output_list.str = output_list.str + to_string("")


                output_list = Output_list()
                output_list_list.append(output_list)

                curr_line = curr_line + 1
                curr_pos = 1
                for n in range(2,ntab + 1) :
                    output_list.str = output_list.str + to_string(" ")


                    output_list = Output_list()
                    output_list_list.append(output_list)

            else:
                for n in range(m,ntab + 1) :
                    put_string(" ")
            curr_pos = ntab

        elif status_code == 2 and headloop == 0 and blloop == 0:
            for n in range(1,nskip + 1) :
                output_list.str = output_list.str + to_string("")


                output_list = Output_list()
                output_list_list.append(output_list)

                curr_pos = 1
                curr_line = curr_line + 1

        elif status_code == 3:
            for n in range(1,lmargin + 1) :
                put_string(" ")

    def find_parameter(paramnr:int, curr_texte:str, status_code:int, i:int):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        j:int = 0
        n:int = 0
        stopped:bool = False

        htp_list = query(htp_list_list, filters=(lambda htp_list :htp_list.paramnr == paramnr), first=True)
        j = i + 1
        while not stopped:

            if substring(curr_texte, j - 1, 1) < "0" or substring(curr_texte, j - 1, 1) > "9":
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

    def decode_key1(paramnr:int):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        out_str = ""
        status_code = 0
        i:int = 0
        n:int = 0
        curr_bez:str = ""
        docu_str:str = ""
        c:str = ""
        len_:int = 0

        def generate_inner_output():
            return out_str, status_code

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == paramnr)).first()

        if paramnr == 602:
            put_string(to_string(curr_page))

        elif paramnr == 603:
            status_code = 1

        elif paramnr == 604:
            put_string(to_string(get_current_date()))

        elif paramnr == 605:
            status_code = 2

        elif paramnr == 637 and l_lieferant:
            put_string(l_lieferant.namekontakt + ", " + l_lieferant.vorname1 + " " + l_lieferant.anrede1)

        elif paramnr == 664 and l_lieferant:
            put_string(l_lieferant.firma)

        elif paramnr == 643 and l_lieferant:
            put_string(trim(l_lieferant.adresse1))

        elif paramnr == 644 and l_lieferant:
            put_string(trim(l_lieferant.adresse2))

        elif paramnr == 645 and l_lieferant:
            put_string(trim(l_lieferant.adresse3))

        elif paramnr == 646 and l_lieferant:
            put_string(trim(l_lieferant.land))

        elif paramnr == 647 and l_lieferant:
            put_string(to_string(l_lieferant.plz))

        elif paramnr == 648 and l_lieferant:
            put_string(trim(l_lieferant.wohnort))

        elif paramnr == 691 and l_lieferant:
            put_string(trim(l_lieferant.fax))

        elif paramnr == 382 and l_lieferant:
            put_string(trim(l_lieferant.telefon))

        elif paramnr == 616:
            f_lmargin = True
            status_code = 3

        elif paramnr == 617:
            f_lmargin = False

        elif (paramnr >= 618) and (paramnr <= 629):

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == paramnr)).first()

            printcod = db_session.query(Printcod).filter(
                    (Printcod.emu == printer.emu) &  (Printcod.code == htparam.fchar)).first()

            if printcod:
                put_string(trim(printcod.contcod))

        elif paramnr == 652:
            L_od0 = L_order

            l_od0 = db_session.query(L_od0).filter(
                    (L_od0.docu_nr == l_orderhdr.docu_nr) &  (L_od0.lief_nr == l_orderhdr.lief_nr) &  (L_od0.pos == 0)).first()
            put_string(to_string(l_od0.lief_fax[0]))

        elif paramnr == 661:
            put_string(to_string(l_orderhdr.angebot_lief[1]))

        elif paramnr == 672:
            put_string(to_string(l_orderhdr.bestelldatum))

        elif paramnr == 655:
            put_string(to_string(l_orderhdr.lieferdatum))

        elif paramnr == 673:
            docu_str = docu_nr

            if l_order:

                if l_order.zeit == 0:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 240) &  (Queasy.char1 == l_order.docu_nr)).first()

                    if not queasy:
                        docu_str = docu_str
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 240
                        queasy.char1 = docu_nr
                        queasy.number1 = 1


                else:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 240) &  (Queasy.char1 == l_order.docu_nr)).first()

                    if not queasy:
                        docu_str = docu_str
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 240
                        queasy.char1 = docu_nr
                        queasy.number1 = 1


                    else:
                        queasy.number1 = queasy.number1 + 1
                        docu_str = docu_str + "-REPRINT" + to_string(queasy.number1)
            put_string(to_string(docu_str))

        elif paramnr == 727:
            put_string(to_string(l_orderhdr.gefaxt))

        elif paramnr == 1088:

            parameters = db_session.query(Parameters).filter(
                    (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

            if parameters:
                put_string(trim(parameters.vstring))

        elif paramnr == 1107:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == l_orderhdr.angebot_lief[2])).first()

            if waehrung:
                put_string(to_string(waehrung.wabkurz))

        elif paramnr == 2302:
            status_code = 6

        elif paramnr == 2303:
            status_code = 7

        elif paramnr == 633:
            output_list.str = output_list.str + to_string(currloop, ">>9")


            curr_pos = curr_pos + 3

        elif paramnr == 2320:
            output_list.str = output_list.str + to_string(l_artikel.traubensort, "x(5)")


            curr_pos = curr_pos + 5

        elif paramnr == 675:
            output_list.str = output_list.str + to_string(tot_qty, "->,>>9.9")


            curr_pos = curr_pos + 8

        elif paramnr == 692:
            print_instruction()

        elif paramnr == 1004 and l_orderhdr:
            put_string(trim(l_orderhdr.lief_fax[1]))

        elif paramnr == 1005:
            for i in range(1,remark_len + 1) :

                if len(op_list.remark) >= i:
                    output_list.str = output_list.str + to_string(substring(op_list.remark, i - 1, 1) , "x(1)")


                else:
                    output_list.str = output_list.str + to_string(" ", "x(1)")
                    curr_pos = curr_pos + 1

        elif paramnr == 2304:
            output_list.str = output_list.str + to_string(l_artikel.artnr, "9999999")
            curr_pos = curr_pos + 7

        elif paramnr == 2305:

            if op_list.anzahl >= 10000 or (- op_list.anzahl >= 10000):
                output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>>,>>9")

            elif op_list.anzahl >= 1000 or (- op_list.anzahl >= 1000):

                if op_list.anzahl >= 0:
                    output_list.str = output_list.str + to_string(op_list.anzahl, ">>>,>>9.99")


                else:
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>9.9")


            else:

                if len(to_string(op_list.anzahl - round(op_list.anzahl - 0.5, 0))) > 3:
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>9.999")


                else:
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>>9.99 ")


            curr_pos = curr_pos + 8

        elif paramnr == 2306:
            pos_bez = curr_pos
            curr_bez = op_list.bezeich

            if not op_list.bez_aend:
                for i in range(1,bez_len + 1) :

                    if len(curr_bez) >= i:
                        output_list.str = output_list.str + to_string(substring(curr_bez, i - 1, 1) , "x(1)")


                    else:
                        output_list.str = output_list.str + to_string(" ", "x(1)")


                curr_pos = curr_pos + bez_len
            else:
                print_bezeich(curr_bez)

        elif paramnr == 9990:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(globaldisc, "->>>,>>>,>>9")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(globaldisc, "->>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(globaldisc, "->,>>>,>>>,>>9")


                curr_pos = curr_pos + 14

        elif paramnr == 9991:
            put_string(to_string(l_orderhdr.besteller))

        elif paramnr == 710:
            c = convert_fibu(op_list.konto)
            len_ = len(c)
            for i in range(1,len + 1) :
                output_list.str = output_list.str + to_string(substring(c, i - 1, 1) , "x(1)")


            curr_pos = curr_pos + len

        elif paramnr == 777:

            if disc2_flag == False:
                output_list.str = output_list.str + to_string(op_list.disc, ">9.99")


            else:
                output_list.str = output_list.str + to_string(op_list.disc2, ">9.99")


            curr_pos = curr_pos + 5

        elif paramnr == 779:

            if not long_digit:

                if op_list.epreis >= 10000000:
                    output_list.str = output_list.str + to_string(op_list.epreis0, " >>,>>>,>>>,>>9")


                else:
                    output_list.str = output_list.str + to_string(op_list.epreis0, ">>,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 12
            else:
                output_list.str = output_list.str + to_string(op_list.epreis0, ">,>>>,>>9.99")


                curr_pos = curr_pos + 13

        elif paramnr == 780:
            output_list.str = output_list.str + to_string(op_list.vat, ">9.99")


            curr_pos = curr_pos + 5

        elif paramnr == 2307:

            if not long_digit:

                if op_list.epreis >= 10000000000:
                    output_list.str = output_list.str + to_string(op_list.epreis, " >>>,>>>,>>>,>>9")


                else:
                    output_list.str = output_list.str + to_string(op_list.epreis, ">,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 12
            else:
                output_list.str = output_list.str + to_string(op_list.epreis, ">,>>>,>>>,>>9")


                curr_pos = curr_pos + 13

        elif paramnr == 2308:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(op_list.warenwert, "->,>>>,>>>,>>9")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9")


                curr_pos = curr_pos + 14

        elif paramnr == 2316:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(bl_balance, "->>,>>>,>>>,>>9")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(bl_balance, "->>,>>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(bl_balance, "->,>>>,>>>,>>9")


                curr_pos = curr_pos + 14

        elif paramnr == 674:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(saldo, "->,>>>,>>>,>>9")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(saldo, "->>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(saldo, "->,>>>,>>>,>>9")


                curr_pos = curr_pos + 14

        elif paramnr == 9989:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(saldo - globaldisc, "->>>,>>>,>>9")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(saldo - globaldisc, "->>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(saldo - globaldisc, "->,>>>,>>>,>>9")


                curr_pos = curr_pos + 14


        return generate_inner_output()

    def put_string(str:str):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        len_:int = 0
        i:int = 0
        len_ = len(str)
        for i in range(1,len + 1) :

            if headloop == 0:
                output_list.str = output_list.str + to_string(substring(str, i - 1, 1) , "x(1)")

            elif headloop == 3:
                header_list.texte = header_list.texte + substring(str, i - 1, 1)
        curr_pos = curr_pos + len

    def print_bezeich(curr_bez:str):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        i:int = 0
        j:int = 0
        curr_pos = curr_pos + bez_len
        for i in range(1,bez_len + 1) :

            if substring(curr_bez, i - 1, 2) == "\\" + chr (10):
                i = i + 1
                remain_bez = substring(curr_bez, (i + 1) - 1, len(curr_bez) - i)
                for j in range(1,(bez_len - i + 2)  + 1) :
                    output_list.str = output_list.str + to_string(" ", "x(1)")

                return

            elif i == len(curr_bez):
                output_list.str = output_list.str + to_string(substring(curr_bez, i - 1, 1) , "x(1)")


                for j in range(1,(bez_len - i)  + 1) :
                    output_list.str = output_list.str + to_string(" ", "x(1)")

                return
            else:
                output_list.str = output_list.str + to_string(substring(curr_bez, i - 1, 1) , "x(1)")


        remain_bez = substring(curr_bez, i - 1, len(curr_bez))

    def print_bezeich1():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        i:int = 0
        j:int = 0
        for i in range(1,pos_bez - 1 + 1) :
            output_list.str = output_list.str + to_string(" ", "x(1)")


        for i in range(1,bez_len + 1) :

            if substring(remain_bez, i - 1, 2) == "\\" + chr (10):
                i = i + 1
                remain_bez = substring(remain_bez, (i + 1) - 1, len(remain_bez) - i)
                for j in range((bez_len - i),bez_len + 1) :
                    output_list.str = output_list.str + to_string(" ", "x(1)")

                return

            elif i == len(remain_bez):
                output_list.str = output_list.str + to_string(substring(remain_bez, i - 1, 1) , "x(1)")


                for j in range((bez_len - i),bez_len + 1) :
                    output_list.str = output_list.str + to_string(" ", "x(1)")


                remain_bez = ""

                return
            else:
                output_list.str = output_list.str + to_string(substring(remain_bez, i - 1, 1) , "x(1)")


        remain_bez = substring(remain_bez, i - 1, len(remain_bez))

    def print_instruction():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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
            for i in range(1,len(l_orderhdr.lief_fax[2])  + 1) :
                ind = ind + 1

                if ind == 57:
                    output_list.str = output_list.str + to_string("")
                    output_list.pos = 20


                    ind = 1
                    curr_line = curr_line + 1

                if substring(l_orderhdr.lief_fax[2], i - 1, 2) == "\\" + chr (10):
                    output_list.str = output_list.str + to_string("")
                    output_list.pos = 20


                    curr_line = curr_line + 1
                    ind = 1
                    i = i + 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 1) == chr (10):
                    output_list.str = output_list.str + to_string(" ", "x(1)")


                else:
                    output_list.str = output_list.str + to_string(substring(l_orderhdr.lief_fax[2], i - 1, 1) , "x(1)")


        else:
            output_list.str = output_list.str + to_string("")


            output_list = Output_list()
            output_list_list.append(output_list)

            curr_line = curr_line + 1
            for j in range(1,(pos_bez - 1)  + 1) :
                output_list.str = output_list.str + to_string(" ", "x(1)")


            ind = 0
            for i in range(1,len(l_orderhdr.lief_fax[2])  + 1) :
                ind = ind + 1

                if ind == (bez_len + 1):
                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_bez - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")


                    ind = 1

                if substring(l_orderhdr.lief_fax[2], i - 1, 2) == "\\" + chr (10):
                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_bez - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")


                    ind = 1
                    i = i + 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 1) == chr (10):
                    output_list.str = output_list.str + to_string(" ", "x(1)")


                else:
                    output_list.str = output_list.str + to_string(substring(l_orderhdr.lief_fax[2], i - 1, 1) , "x(1)")


        output_list.str = output_list.str + to_string("")


        output_list = Output_list()
        output_list_list.append(output_list)

        curr_line = curr_line + 1
        curr_pos = 1

    def print_instruct1():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        i:int = 0
        j:int = 0
        ind:int = 0
        s:str = ""

        if pos_ord == 0:

            if ord_len >= 75:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = output_list.str + to_string("")
                output_list.pos = 5

            elif ord_len >= 60:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = output_list.str + to_string("")
                output_list.pos = 10

            elif ord_len >= 55:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = output_list.str + to_string("")
                output_list.pos = 15


            else:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.str = output_list.str + to_string("")
                output_list.pos = 20


            ind = 0
            for i in range(1,len(l_orderhdr.lief_fax[2])  + 1) :
                ind = ind + 1

                if ind > ord_len and substring(l_orderhdr.lief_fax[2], i - 1, 1) == " ":

                    if ord_len >= 80:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 5

                    elif ord_len >= 60:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 10

                    elif ord_len >= 55:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 15


                    else:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 20


                    ind = 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 2) == "\\" + chr (10):

                    if ord_len >= 80:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 5

                    elif ord_len >= 60:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 10

                    elif ord_len >= 55:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 15


                    else:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.str = output_list.str + to_string("")
                        output_list.pos = 20


                    ind = 1
                    i = i + 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 1) == chr (10):
                    output_list.str = output_list.str + to_string(" ", "x(1)")


                else:
                    output_list.str = output_list.str + to_string(substring(l_orderhdr.lief_fax[2], i - 1, 1) , "x(1)")


        else:
            output_list.str = output_list.str + to_string("")


            output_list = Output_list()
            output_list_list.append(output_list)

            curr_line = curr_line + 1
            for j in range(1,(pos_ord - 1)  + 1) :
                output_list.str = output_list.str + to_string(" ", "x(1)")


            ind = 0
            for i in range(1,len(l_orderhdr.lief_fax[2])  + 1) :
                ind = ind + 1

                if ind > ord_len and substring(l_orderhdr.lief_fax[2], i - 1, 1) == " ":
                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_ord - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")


                    ind = 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 2) == "\\" + chr (10):
                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_ord - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")


                    ind = 1
                    i = i + 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 1) == chr (10):
                    output_list.str = output_list.str + to_string(" ", "x(1)")


                else:
                    output_list.str = output_list.str + to_string(substring(l_orderhdr.lief_fax[2], i - 1, 1) , "x(1)")


        output_list.str = output_list.str + to_string("")


        output_list = Output_list()
        output_list_list.append(output_list)

        curr_line = curr_line + 1
        curr_pos = 1

    def convert_fibu(konto:str):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal l_art, l_od0


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list, l_art, l_od0
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        s = ""
        ch:str = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return s

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 977)).first()
        ch = htparam.fchar
        j = 0
        for i in range(1,len(ch)  + 1) :

            if substring(ch, i - 1, 1) >= "0" and substring(ch, i - 1, 1) <= "9":
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)


        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower()) &  (L_orderhdr.lief_nr > 0)).first()

    if not l_orderhdr:

        l_orderhdr = db_session.query(L_orderhdr).filter(
                (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower()) &  (L_orderhdr.lief_nr == 0)).first()

    l_order = db_session.query(L_order).filter(
            (L_order.lief_nr == l_orderhdr.lief_nr) &  (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos == 0)).first()

    if not l_order:
        err_code = 1

        return generate_output()
    pr = l_order.lief_fax[0]
    globaldisc = l_order.warenwert

    waehrung = db_session.query(Waehrung).filter(
            (Waehrungsnr == l_orderhdr.angebot_lief[2])).first()

    if waehrung:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 152)).first()

        if htparam.fchar != "" and (htparam.fchar != waehrung.wabkurz):
            foreign_currency = True

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == l_orderhdr.lief_nr)).first()

    gl_department = db_session.query(Gl_department).filter(
            (Gl_department.nr == l_orderhdr.angebot_lief[0])).first()

    if printnr == 0:
        outfile = "\\vhp_letter.rtf"
    else:

        printer = db_session.query(Printer).filter(
                (Printer.nr == printnr)).first()

        if not printer:
            err_code = 2

            return generate_output()
        else:
            outfile = printer.path
    printer_pglen = printer.pglen
    fill_list()
    curr_line = 1
    curr_page = 1
    output_list = Output_list()
    output_list_list.append(output_list)


    for brief_list in query(brief_list_list):

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
            output_list_list.append(output_list)

            curr_line = curr_line + 1
            curr_pos = 1

        elif blloop == 2:
            loop_list = Loop_list()
            loop_list_list.append(loop_list)

            loop_list.texte = brief_list.b_text
            curr_pos = 1

        elif headloop == 2:
            loop1_list = Loop1_list()
            loop1_list_list.append(loop1_list)

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

    l_order = db_session.query(L_order).filter(
            (L_order.lief_nr == l_orderhdr.lief_nr) &  (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos == 0)).first()
    l_order.gedruckt = get_current_date()
    l_order.zeit = get_current_time_in_seconds()

    l_order = db_session.query(L_order).first()

    return generate_output()