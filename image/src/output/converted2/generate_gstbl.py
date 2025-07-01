#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.generate_gst_fobillbl import generate_gst_fobillbl
from models import L_artikel, L_lieferant, L_op, Gl_acct, Gl_jouhdr, Gl_fstype, Gl_journal

def generate_gstbl(fdate:date, tdate:date, sorttype:int):

    prepare_cache ([L_artikel, L_lieferant, L_op, Gl_acct, Gl_jouhdr, Gl_fstype, Gl_journal])

    done = True
    t_supplier_list = []
    t_customer_list = []
    t_gl_list = []
    t_rcv_trx_list = []
    t_gl_trx_list = []
    a:int = 0
    b:string = ""
    l_artikel = l_lieferant = l_op = gl_acct = gl_jouhdr = gl_fstype = gl_journal = None

    t_rcv_trx = t_supplier = t_customer = t_gl_trx = t_gl = None

    t_rcv_trx_list, T_rcv_trx = create_model("T_rcv_trx", {"rcvtrx_suppname":string, "rcvtrx_suppbrn":int, "rcvtrx_invoicedate":date, "rcvtrx_invoicenumber":string, "rcvtrx_importdecno":int, "rcvtrx_linenumber":int, "rcvtrx_productdesc":string, "rcvtrx_pchasevalmyr":Decimal, "rcvtrx_gstvalmyr":Decimal, "rcvtrx_taxcode":string, "rcvtrx_fcycode":string, "rcvtrx_pchasefcy":int, "rcvtrx_gstfcy":int, "rcvtrx_artnr":int})
    t_supplier_list, T_supplier = create_model("T_supplier", {"suppid":int, "suppname":string, "suppbrn":int, "suppdategst":date, "suppgstno":int, "suppaddr1":string, "suppaddr2":string, "supptlp":string, "suppfax":string, "suppemail":string, "suppwebsite":string})
    t_customer_list, T_customer = create_model("T_customer", {"custid":int, "custname":string, "custbrn":int, "custinvdate":date, "custinvno":int, "custlineno":int, "custdesc":string, "custsuppvalmyr":Decimal, "custgstvalmyr":Decimal, "custtaxcode":string, "custcountry":string, "custfcycode":string, "custsuppfcy":Decimal, "custgstfcy":Decimal})
    t_gl_trx_list, T_gl_trx = create_model("T_gl_trx", {"gltrx_trxdate":date, "gltrx_accountid":string, "gltrx_accountname":string, "gltrx_trxdesc":string, "gltrx_name":string, "gltrx_trxid":int, "gltrx_srcdocumentid":string, "gltrx_srctype":string, "gltrx_debit":Decimal, "gltrx_credit":Decimal, "gltrx_balance":Decimal})
    t_gl_list, T_gl = create_model("T_gl", {"glid":string, "glaccname":string, "glacctype":int, "gldebit":Decimal, "glcredit":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal done, t_supplier_list, t_customer_list, t_gl_list, t_rcv_trx_list, t_gl_trx_list, a, b, l_artikel, l_lieferant, l_op, gl_acct, gl_jouhdr, gl_fstype, gl_journal
        nonlocal fdate, tdate, sorttype


        nonlocal t_rcv_trx, t_supplier, t_customer, t_gl_trx, t_gl
        nonlocal t_rcv_trx_list, t_supplier_list, t_customer_list, t_gl_trx_list, t_gl_list

        return {"done": done, "t-supplier": t_supplier_list, "t-customer": t_customer_list, "t-gl": t_gl_list, "t-rcv-trx": t_rcv_trx_list, "t-gl-trx": t_gl_trx_list}

    l_op_obj_list = {}
    l_op = L_op()
    l_artikel = L_artikel()
    l_lieferant = L_lieferant()
    for l_op.datum, l_op.docu_nr, l_op.pos, l_op.warenwert, l_op._recid, l_artikel.bezeich, l_artikel.lief_artnr, l_artikel.artnr, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant.adresse1, l_lieferant.adresse2, l_lieferant.notizen, l_lieferant._recid in db_session.query(L_op.datum, L_op.docu_nr, L_op.pos, L_op.warenwert, L_op._recid, L_artikel.bezeich, L_artikel.lief_artnr, L_artikel.artnr, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant.adresse1, L_lieferant.adresse2, L_lieferant.notizen, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
             (L_op.datum >= fdate) & (L_op.datum <= tdate) & (L_op.lief_nr > 0) & (L_op.loeschflag <= 1) & (L_op.op_art == 1)).order_by(L_lieferant.firma, L_op.datum, L_artikel.bezeich).all():
        if l_op_obj_list.get(l_op._recid):
            continue
        else:
            l_op_obj_list[l_op._recid] = True

        if l_artikel.lief_artnr[2] == "":
            done = False

            return generate_output()
        t_supplier = T_supplier()
        t_supplier_list.append(t_supplier)

        t_supplier.suppid = l_lieferant.lief_nr
        t_supplier.suppname = l_lieferant.firma
        t_supplier.suppdategst = 01/01/99
        t_supplier.suppgstno = 9999999
        t_supplier.suppaddr1 = l_lieferant.adresse1
        t_supplier.suppaddr2 = l_lieferant.adresse2
        t_supplier.supptlp = telefon
        t_supplier.suppfax = fax
        t_supplier.suppemail = "aaa@aa.com"
        t_supplier.suppwebsite = "www.aaa.com"

        if matches(l_lieferant.notizen[0],r"*" + r"#BRN*" + r"*"):
            a = length(trim(entry(1, l_lieferant.notizen[0], "#BRN")))
            b = trim(entry(1, l_lieferant.notizen[0], "#BRN"))
            t_supplier.suppbrn = to_int(substring(b, 3, a - 3))
        else:
            t_supplier.suppbrn = 9999
        t_rcv_trx = T_rcv_trx()
        t_rcv_trx_list.append(t_rcv_trx)

        t_rcv_trx.rcvtrx_suppname = l_lieferant.firma
        t_rcv_trx.rcvtrx_suppbrn = t_supplier.suppBRN
        t_rcv_trx.rcvtrx_invoicedate = l_op.datum
        t_rcv_trx.rcvtrx_invoicenumber = l_op.docu_nr
        t_rcv_trx.rcvtrx_importdecno = 999
        t_rcv_trx.rcvtrx_linenumber = l_op.pos
        t_rcv_trx.rcvtrx_productdesc = l_artikel.bezeich
        t_rcv_trx.rcvtrx_pchasevalmyr =  to_decimal("999")
        t_rcv_trx.rcvtrx_gstvalmyr =  to_decimal("999")
        t_rcv_trx.rcvtrx_taxcode = l_artikel.lief_artnr[2]
        t_rcv_trx.rcvtrx_fcycode = ""
        t_rcv_trx.rcvtrx_pchasefcy = 0
        t_rcv_trx.rcvtrx_gstfcy = 0
        t_rcv_trx.rcvtrx_pchasevalmyr =  to_decimal(l_op.warenwert)
        t_rcv_trx.rcvtrx_artnr = l_artikel.artnr


    t_customer_list = get_output(generate_gst_fobillbl(fdate, tdate))

    t_customer = query(t_customer_list, first=True)

    for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
        t_gl = T_gl()
        t_gl_list.append(t_gl)

        t_gl.glid = gl_acct.fibukonto
        t_gl.glaccname = gl_acct.bezeich
        t_gl.glacctype = gl_acct.acc_type
        t_gl.gldebit =  to_decimal(gl_acct.debit[0])
        t_gl.glcredit =  to_decimal(gl_acct.credit[0])

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.datum >= fdate) & (Gl_jouhdr.datum <= tdate)).order_by(Gl_jouhdr.datum).all():

        gl_journal_obj_list = {}
        gl_journal = Gl_journal()
        gl_acct = Gl_acct()
        gl_fstype = Gl_fstype()
        for gl_journal.fibukonto, gl_journal.jnr, gl_journal.debit, gl_journal.credit, gl_journal._recid, gl_acct.fibukonto, gl_acct.bezeich, gl_acct.acc_type, gl_acct.debit, gl_acct.credit, gl_acct._recid, gl_fstype.bezeich, gl_fstype._recid in db_session.query(Gl_journal.fibukonto, Gl_journal.jnr, Gl_journal.debit, Gl_journal.credit, Gl_journal._recid, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct.acc_type, Gl_acct.debit, Gl_acct.credit, Gl_acct._recid, Gl_fstype.bezeich, Gl_fstype._recid).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).filter(
                 (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal.fibukonto).all():
            if gl_journal_obj_list.get(gl_journal._recid):
                continue
            else:
                gl_journal_obj_list[gl_journal._recid] = True


            t_gl_trx = T_gl_trx()
            t_gl_trx_list.append(t_gl_trx)

            t_gl_trx.gltrx_trxdate = gl_jouhdr.datum
            t_gl_trx.gltrx_accountid = gl_journal.fibukonto
            t_gl_trx.gltrx_accountname = gl_acct.bezeich
            t_gl_trx.gltrx_trxdesc = gl_jouhdr.bezeich
            t_gl_trx.gltrx_name = gl_jouhdr.bezeich
            t_gl_trx.gltrx_trxid = gl_journal.jnr
            t_gl_trx.gltrx_srcdocumentid = gl_jouhdr.refno
            t_gl_trx.gltrx_srctype = gl_fstype.bezeich
            t_gl_trx.gltrx_debit =  to_decimal(gl_journal.debit)
            t_gl_trx.gltrx_credit =  to_decimal(gl_journal.credit)
            t_gl_trx.gltrx_balance =  to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

    return generate_output()