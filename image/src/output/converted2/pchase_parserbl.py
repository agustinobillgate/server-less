#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, L_orderhdr, L_order, Waehrung, L_lieferant, Gl_department, Printer, Briefzei, L_artikel, Printcod, Queasy, Parameters

def pchase_parserbl(briefnr:int, printnr:int, docu_nr:string):

    prepare_cache ([Htparam, L_orderhdr, L_order, Waehrung, Printer, Briefzei, L_artikel, Queasy])

    outfile = ""
    printer_pglen = 0
    err_code = 0
    output_list_list = []
    f_page:bool = True
    foot_text1:string = ""
    foot_char2:string = ""
    foreign_currency:bool = False
    currloop:int = 0
    betrag:Decimal = to_decimal("0.0")
    saldo:Decimal = to_decimal("0.0")
    bl_balance:Decimal = to_decimal("0.0")
    tot_qty:Decimal = to_decimal("0.0")
    pos_bez:int = 0
    bez_len:int = 35
    remark_len:int = 24
    pos_ord:int = 0
    ord_len:int = 35
    remain_bez:string = ""
    disc2_flag:bool = False
    pr:string = ""
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
    keychar:string = ""
    price_decimal:int = 0
    globaldisc:Decimal = to_decimal("0.0")
    long_digit:bool = False
    htparam = l_orderhdr = l_order = waehrung = l_lieferant = gl_department = printer = briefzei = l_artikel = printcod = queasy = parameters = None

    output_list = op_list = brief_list = htp_list = loop_list = loop1_list = header_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":string, "pos":int})
    op_list_list, Op_list = create_model("Op_list", {"artnr":int, "anzahl":Decimal, "bezeich":string, "bez_aend":bool, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "epreis":Decimal, "epreis0":Decimal, "warenwert":Decimal, "konto":string, "warenwert0":Decimal, "remark":string})
    brief_list_list, Brief_list = create_model("Brief_list", {"b_text":string})
    htp_list_list, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":string})
    loop_list_list, Loop_list = create_model("Loop_list", {"texte":string})
    loop1_list_list, Loop1_list = create_model("Loop1_list", {"texte":string})
    header_list_list, Header_list = create_model("Header_list", {"texte":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        return {"outfile": outfile, "printer_pglen": printer_pglen, "err_code": err_code, "output-list": output_list_list}

    def fill_list():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.paramnr = 9992
        htp_list.fchar = keychar + "orderType"

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
                        brief_list_list.append(brief_list)

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
                brief_list_list.append(brief_list)

            brief_list.b_text = brief_list.b_text + c


    def analyse_text():

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == 2300), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            headloop = 1

        htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == 2301), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            headloop = headloop + 1

        htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == 2302), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            blloop = 1

        htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == 2303), first=True)

        if trim(brief_list.b_text) == htp_list.fchar:
            blloop = blloop + 1


    def build_text_line(curr_texte:string):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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


    def build_loop_line(curr_texte:string):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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
        op_list_list.clear()

        l_order_obj_list = {}
        l_order = L_order()
        l_art = L_artikel()
        for l_order.quality, l_order.stornogrund, l_order.artnr, l_order.einzelpreis, l_order.besteller, l_order.anzahl, l_order.warenwert, l_order.docu_nr, l_order.lief_fax, l_order.zeit, l_order.gedruckt, l_order._recid, l_art.traubensorte, l_art.artnr, l_art._recid in db_session.query(L_order.quality, L_order.stornogrund, L_order.artnr, L_order.einzelpreis, L_order.besteller, L_order.anzahl, L_order.warenwert, L_order.docu_nr, L_order.lief_fax, L_order.zeit, L_order.gedruckt, L_order._recid, L_art.traubensorte, L_art.artnr, L_art._recid).join(L_art,(L_art.artnr == L_order.artnr)).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.loeschflag <= 1) & (L_order.pos > 0)).order_by(L_art.bezeich).all():
            if l_order_obj_list.get(l_order._recid):
                continue
            else:
                l_order_obj_list[l_order._recid] = True


            create_it = False
            bez_aend = False
            curr_bez = l_art.bezeich
            disc =  to_decimal("0")
            disc2 =  to_decimal("0")

            if l_order.quality != "":
                disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) * 0.01

            if l_art.jahrgang == 0 or length(l_order.stornogrund) <= 12:

                op_list = query(op_list_list, filters=(lambda op_list: op_list.artnr == l_order.artnr and op_list.epreis == l_order.einzelpreis and op_list.bezeich == l_art.bezeich and op_list.disc == disc and op_list.disc2 == disc2 and op_list.konto == l_order.stornogrund), first=True)
            else:
                curr_bez = substring(l_order.stornogrund, 12, length(l_order.stornogrund))
                create_it = True
                bez_aend = True

            if length(l_order.stornogrund) > 12:
                curr_bez = substring(l_order.stornogrund, 12)

            if not op_list or create_it:
                vat =  to_decimal("0")
                op_list = Op_list()
                op_list_list.append(op_list)

                op_list.artnr = l_order.artnr
                op_list.bezeich = curr_bez
                op_list.bez_aend = bez_aend
                op_list.epreis =  to_decimal(l_order.einzelpreis)
                op_list.epreis0 =  to_decimal(l_order.einzelpreis)
                op_list.konto = l_order.stornogrund
                op_list.remark = l_order.besteller

                if l_order.quality != "":
                    vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) * 0.01
                    op_list.disc =  to_decimal(disc)
                    op_list.disc2 =  to_decimal(disc2)
                    op_list.vat =  to_decimal(vat)
                    disc =  to_decimal(disc) / to_decimal("100")
                    disc2 =  to_decimal(disc2) / to_decimal("100")
                    vat =  to_decimal(vat) / to_decimal("100")
            op_list.epreis0 =  to_decimal(l_order.einzelpreis) / to_decimal((1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
            op_list.anzahl =  to_decimal(op_list.anzahl) + to_decimal(l_order.anzahl)
            op_list.warenwert =  to_decimal(op_list.warenwert) + to_decimal(l_order.warenwert)
            op_list.warenwert0 =  to_decimal(op_list.warenwert0) + to_decimal(l_order.warenwert) / to_decimal((1) - to_decimal(disc)) / to_decimal((1) - to_decimal(disc2)) / to_decimal((1) + to_decimal(vat))
            tot_qty =  to_decimal(tot_qty) + to_decimal(l_order.anzahl)
        currloop = 0

        for op_list in query(op_list_list):

            if op_list.anzahl == 0:
                op_list_list.remove(op_list)

        l_artikel_obj_list = {}
        for l_artikel in db_session.query(L_artikel).filter(
                 ((L_artikel.artnr.in_(list(set([op_list.artnr for op_list in op_list_list])))))).order_by(L_artikel._recid).all():
            if l_artikel_obj_list.get(l_artikel._recid):
                continue
            else:
                l_artikel_obj_list[l_artikel._recid] = True

            if curr_line > printer.pglen:
                curr_page = curr_page + 1
                curr_line = 1
                do_billhead()
            currloop = currloop + 1
            bl_balance =  to_decimal(bl_balance) + to_decimal(op_list.warenwert)
            saldo =  to_decimal(saldo) + to_decimal(op_list.warenwert)

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

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
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
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        i:int = 0

        for header_list in query(header_list_list):
            curr_pos = 1
            for i in range(1,length(header_list.texte)  + 1) :
                output_list.str = output_list.str + to_string(substring(header_list.texte, i - 1, 1) , "x(1)")


            output_list.str = output_list.str + to_string("")


            output_list = Output_list()
            output_list_list.append(output_list)

            curr_line = curr_line + 1


    def interprete_text(curr_texte:string, i:int):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        found = False
        j:int = 0
        rowno:int = 0

        def generate_inner_output():
            return (i, found)

        j = i

        htp_list = query(htp_list_list, first=True)
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

            htp_list = query(htp_list_list, next=True)

        if not found:
            put_string(substring(curr_texte, j - 1, 1))

        return generate_inner_output()


    def decode_key(curr_texte:string, paramnr:int, i:int):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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

        return generate_inner_output()


    def find_parameter(paramnr:int, curr_texte:string, status_code:int, i:int):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        j:int = 0
        n:int = 0
        stopped:bool = False

        def generate_inner_output():
            return (i)


        htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == paramnr), first=True)
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

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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

        if htparam.paramnr == 602:
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
            L_od0 =  create_buffer("L_od0",L_order)

            l_od0 = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"lief_nr": [(eq, l_orderhdr.lief_nr)],"pos": [(eq, 0)]})
            put_string(to_string(l_od0.lief_fax[0]))

        elif htparam.paramnr == 661:
            put_string(to_string(l_orderhdr.angebot_lief[1]))

        elif htparam.paramnr == 9992:
            put_string(to_string(l_orderhdr.bestellart))

        elif htparam.paramnr == 672:
            put_string(to_string(l_orderhdr.bestelldatum))

        elif htparam.paramnr == 655:
            put_string(to_string(l_orderhdr.lieferdatum))

        elif htparam.paramnr == 673:
            docu_str = docu_nr

            if l_order:

                if l_order.zeit == 0:

                    queasy = get_cache (Queasy, {"key": [(eq, 240)],"char1": [(eq, l_order.docu_nr)]})

                    if not queasy:
                        docu_str = docu_str
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 240
                        queasy.char1 = docu_nr
                        queasy.number1 = 1


                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 240)],"char1": [(eq, l_order.docu_nr)]})

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

        elif htparam.paramnr == 727:
            put_string(to_string(l_orderhdr.gefaxt))

        elif htparam.paramnr == 1088:

            parameters = db_session.query(Parameters).filter(
                     (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

            if parameters:
                put_string(trim(parameters.vstring))

        elif htparam.paramnr == 1107:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, l_orderhdr.angebot_lief[2])]})

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
            output_list.str = output_list.str + to_string(l_artikel.traubensorte, "x(5)")


            curr_pos = curr_pos + 5

        elif htparam.paramnr == 675:
            output_list.str = output_list.str + to_string(tot_qty, "->,>>9.99")


            curr_pos = curr_pos + 8

        elif htparam.paramnr == 692:
            print_instruction()

        elif htparam.paramnr == 1004 and l_orderhdr:
            put_string(trim(l_orderhdr.lief_fax[1]))

        elif htparam.paramnr == 1005:
            for i in range(1,remark_len + 1) :

                if length(op_list.remark) >= i:
                    output_list.str = output_list.str + to_string(substring(op_list.remark, i - 1, 1) , "x(1)")


                else:
                    output_list.str = output_list.str + to_string(" ", "x(1)")
                    curr_pos = curr_pos + 1

        elif htparam.paramnr == 2304:
            output_list.str = output_list.str + to_string(l_artikel.artnr, "9999999")
            curr_pos = curr_pos + 7

        elif htparam.paramnr == 2305:

            if op_list.anzahl >= 10000 or (- op_list.anzahl >= 10000):
                output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>>,>>9.99") + " "

            elif op_list.anzahl >= 1000 or (- op_list.anzahl >= 1000):

                if op_list.anzahl >= 0:
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>>,>>9.99") + " "


                else:
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>>,>>9.99") + " "

            elif op_list.anzahl >= 100 or (- op_list.anzahl >= 100):

                if op_list.anzahl >= 0:
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>>,>>9.99") + " "


                else:
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>>,>>9.99") + " "


            else:

                if length(to_string(op_list.anzahl - round(op_list.anzahl - 0.5, 0))) > 3:
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>>,>>9.99") + " "


                else:
                    output_list.str = output_list.str + to_string(op_list.anzahl, "->>>,>>>,>>9.99") + " "


            curr_pos = curr_pos + 8

        elif htparam.paramnr == 2306:
            pos_bez = curr_pos
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

        elif htparam.paramnr == 9990:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(globaldisc, "->>>,>>>,>>9.99")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(globaldisc, "->>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(globaldisc, "->,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 14

        elif htparam.paramnr == 9991:
            put_string(to_string(l_orderhdr.besteller))

        elif htparam.paramnr == 710:
            c = convert_fibu(op_list.konto)
            len_ = length(c)
            for i in range(1,len + 1) :
                output_list.str = output_list.str + to_string(substring(c, i - 1, 1) , "x(1)")


            curr_pos = curr_pos + len

        elif htparam.paramnr == 777:

            if disc2_flag == False:
                output_list.str = output_list.str + to_string(op_list.disc, ">9.99")


            else:
                output_list.str = output_list.str + to_string(op_list.disc2, ">9.99")


            curr_pos = curr_pos + 5

        elif htparam.paramnr == 779:

            if not long_digit:

                if op_list.epreis >= 10000000:
                    output_list.str = output_list.str + to_string(op_list.epreis0, " >>,>>>,>>>,>>9.99")


                else:
                    output_list.str = output_list.str + to_string(op_list.epreis0, ">>,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 12
            else:
                output_list.str = output_list.str + to_string(op_list.epreis0, ">,>>>,>>9.99")


                curr_pos = curr_pos + 13

        elif htparam.paramnr == 780:
            output_list.str = output_list.str + to_string(op_list.vat, ">9.99")


            curr_pos = curr_pos + 5

        elif htparam.paramnr == 2307:

            if not long_digit:

                if op_list.epreis >= 10000000000:
                    output_list.str = output_list.str + to_string(op_list.epreis, " >>>,>>>,>>>,>>9.99")


                else:
                    output_list.str = output_list.str + to_string(op_list.epreis, ">,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 12
            else:
                output_list.str = output_list.str + to_string(op_list.epreis, ">,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 13

        elif htparam.paramnr == 2308:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(op_list.warenwert, "->,>>>,>>>,>>9.99")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(op_list.warenwert, "->,>>>,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 14

        elif htparam.paramnr == 2316:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(bl_balance, "->>,>>>,>>>,>>9.99")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(bl_balance, "->>,>>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(bl_balance, "->,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 14

        elif htparam.paramnr == 674:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(saldo, "->,>>>,>>>,>>9.99")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(saldo, "->>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(saldo, "->,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 14

        elif htparam.paramnr == 9989:

            if not long_digit:

                if price_decimal == 0 and not foreign_currency:
                    output_list.str = output_list.str + to_string(saldo - globaldisc, "->>>,>>>,>>9.99")

                elif price_decimal == 2 or foreign_currency:
                    output_list.str = output_list.str + to_string(saldo - globaldisc, "->>>,>>9.99")


                curr_pos = curr_pos + 11
            else:
                output_list.str = output_list.str + to_string(saldo - globaldisc, "->,>>>,>>>,>>9.99")


                curr_pos = curr_pos + 14

        return generate_inner_output()


    def put_string(str:string):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        len_:int = 0
        i:int = 0
        len_ = length(str)
        for i in range(1,len + 1) :

            if headloop == 0:
                output_list.str = output_list.str + to_string(substring(str, i - 1, 1) , "x(1)")

            elif headloop == 3:
                header_list.texte = header_list.texte + substring(str, i - 1, 1)
        curr_pos = curr_pos + len


    def print_bezeich(curr_bez:string):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
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
            for i in range(1,length(l_orderhdr.lief_fax[2])  + 1) :
                ind = ind + 1

                if ind == 57:
                    output_list.str = output_list.str + to_string("")
                    output_list.pos = 20


                    ind = 1
                    curr_line = curr_line + 1

                if substring(l_orderhdr.lief_fax[2], i - 1, 2) == ("\\" + chr_unicode(10).lower()):
                    output_list.str = output_list.str + to_string("")
                    output_list.pos = 20


                    curr_line = curr_line + 1
                    ind = 1
                    i = i + 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 1) == chr_unicode(10):
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
            for i in range(1,length(l_orderhdr.lief_fax[2])  + 1) :
                ind = ind + 1

                if ind == (bez_len + 1):
                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_bez - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")


                    ind = 1

                if substring(l_orderhdr.lief_fax[2], i - 1, 2) == ("\\" + chr_unicode(10).lower()):
                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_bez - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")


                    ind = 1
                    i = i + 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 1) == chr_unicode(10):
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
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

        i:int = 0
        j:int = 0
        ind:int = 0
        s:string = ""

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
            for i in range(1,length(l_orderhdr.lief_fax[2])  + 1) :
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

                elif substring(l_orderhdr.lief_fax[2], i - 1, 2) == ("\\" + chr_unicode(10).lower()):

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

                elif substring(l_orderhdr.lief_fax[2], i - 1, 1) == chr_unicode(10):
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
            for i in range(1,length(l_orderhdr.lief_fax[2])  + 1) :
                ind = ind + 1

                if ind > ord_len and substring(l_orderhdr.lief_fax[2], i - 1, 1) == " ":
                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_ord - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")


                    ind = 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 2) == ("\\" + chr_unicode(10).lower()):
                    output_list.str = output_list.str + to_string("")


                    output_list = Output_list()
                    output_list_list.append(output_list)

                    curr_line = curr_line + 1
                    for j in range(1,(pos_ord - 1)  + 1) :
                        output_list.str = output_list.str + to_string(" ", "x(1)")


                    ind = 1
                    i = i + 1

                elif substring(l_orderhdr.lief_fax[2], i - 1, 1) == chr_unicode(10):
                    output_list.str = output_list.str + to_string(" ", "x(1)")


                else:
                    output_list.str = output_list.str + to_string(substring(l_orderhdr.lief_fax[2], i - 1, 1) , "x(1)")


        output_list.str = output_list.str + to_string("")


        output_list = Output_list()
        output_list_list.append(output_list)

        curr_line = curr_line + 1
        curr_pos = 1


    def convert_fibu(konto:string):

        nonlocal outfile, printer_pglen, err_code, output_list_list, f_page, foot_text1, foot_char2, foreign_currency, currloop, betrag, saldo, bl_balance, tot_qty, pos_bez, bez_len, remark_len, pos_ord, ord_len, remain_bez, disc2_flag, pr, f_lmargin, headloop, blloop, lmargin, nskip, ntab, n, curr_pos, curr_line, curr_page, buttom_line, keychar, price_decimal, globaldisc, long_digit, htparam, l_orderhdr, l_order, waehrung, l_lieferant, gl_department, printer, briefzei, l_artikel, printcod, queasy, parameters
        nonlocal briefnr, printnr, docu_nr


        nonlocal output_list, op_list, brief_list, htp_list, loop_list, loop1_list, header_list
        nonlocal output_list_list, op_list_list, brief_list_list, htp_list_list, loop_list_list, loop1_list_list, header_list_list

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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr.docu_nr == (docu_nr).lower()) & (L_orderhdr.lief_nr > 0)).first()

    if not l_orderhdr:

        l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)],"lief_nr": [(eq, 0)]})

    l_order = get_cache (L_order, {"lief_nr": [(eq, l_orderhdr.lief_nr)],"docu_nr": [(eq, docu_nr)],"pos": [(eq, 0)]})

    if not l_order:
        err_code = 1

        return generate_output()
    pr = l_order.lief_fax[0]
    globaldisc =  to_decimal(l_order.warenwert)

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, l_orderhdr.angebot_lief[2])]})

    if waehrung:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

        if htparam.fchar != "" and (htparam.fchar != waehrung.wabkurz):
            foreign_currency = True

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_orderhdr.lief_nr)]})

    gl_department = get_cache (Gl_department, {"nr": [(eq, l_orderhdr.angebot_lief[0])]})

    if printnr == 0:
        outfile = "\\vhp-letter.rtf"
    else:

        printer = get_cache (Printer, {"nr": [(eq, printnr)]})

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
            output_list.str = output_list.str + to_string(" ")


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

    l_order = get_cache (L_order, {"lief_nr": [(eq, l_orderhdr.lief_nr)],"docu_nr": [(eq, docu_nr)],"pos": [(eq, 0)]})
    l_order.gedruckt = get_current_date()
    l_order.zeit = get_current_time_in_seconds()
    pass

    return generate_output()