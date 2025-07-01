#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, L_kredit, Artikel

def prepare_gl_detailapbl(pvilanguage:int, fibu:string, bemerk:string):

    prepare_cache ([Artikel])

    receive_date = None
    t_gl_acct_list = []
    s_list_list = []
    lvcarea:string = "gl-detailAP"
    gl_acct = l_kredit = artikel = None

    s_list = t_gl_acct = None

    s_list_list, S_list = create_model("S_list", {"rgdatum":date, "artnr":int, "bezeich":string, "saldo":Decimal, "name":string, "lscheinnr":string, "fibu":string, "lief_nr":int, "lflag":bool})
    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal receive_date, t_gl_acct_list, s_list_list, lvcarea, gl_acct, l_kredit, artikel
        nonlocal pvilanguage, fibu, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        return {"receive_date": receive_date, "t-gl-acct": t_gl_acct_list, "s-list": s_list_list}

    def disp_it():

        nonlocal receive_date, t_gl_acct_list, s_list_list, lvcarea, gl_acct, l_kredit, artikel
        nonlocal pvilanguage, fibu, bemerk


        nonlocal s_list, t_gl_acct
        nonlocal s_list_list, t_gl_acct_list

        counter:int = 0
        zahlkonto:int = 0
        lief_nr:int = 0
        saldo:Decimal = to_decimal("0.0")
        docu_nr:string = ""
        lscheinnr:string = ""
        bezeich:string = ""
        ltype:int = 0
        ltype = to_int(substring(entry(1, bemerk, ";") , 2, 1))

        if ltype == 2:
            counter = to_int(entry(2, bemerk, ";"))
            lief_nr = to_int(entry(3, bemerk, ";"))
            zahlkonto = to_int(entry(4, bemerk, ";"))
            saldo =  to_decimal(to_decimal(entry(5 , bemerk , ";"))) / to_decimal("100")
        else:
            counter = to_int(entry(2, bemerk, ";"))
            lief_nr = to_int(entry(3, bemerk, ";"))

        for l_kredit in db_session.query(L_kredit).filter(
                 (L_kredit.counter == counter)).order_by(L_kredit.zahlkonto).all():

            if l_kredit.zahlkonto == 0:
                receive_date = l_kredit.rgdatum
            s_list = S_list()
            s_list_list.append(s_list)

            buffer_copy(l_kredit, s_list)

            if l_kredit.zahlkonto > 0:

                artikel = get_cache (Artikel, {"artnr": [(eq, l_kredit.zahlkonto)],"departement": [(eq, 0)]})
                s_list.artnr = artikel.artnr
                s_list.bezeich = artikel.bezeich


            else:
                s_list.bezeich = translateExtended ("A/P Trade", lvcarea, "")

            if ltype == 2:
                s_list.lflag = (s_list.saldo == saldo)
            else:
                s_list.lflag = (l_kredit.zahlkonto == 0)

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})
    t_gl_acct = T_gl_acct()
    t_gl_acct_list.append(t_gl_acct)

    buffer_copy(gl_acct, t_gl_acct)
    disp_it()

    return generate_output()