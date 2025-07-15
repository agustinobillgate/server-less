#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Brief, Gl_acct, Gl_main, Gl_department, Briefzei, Htparam

def gl_parser_fill_listbl(briefnr:int):

    prepare_cache ([Brief, Gl_acct, Gl_main, Gl_department, Briefzei, Htparam])

    keycmd = ""
    keyvar = ""
    keycont = ""
    htv_list_data = []
    htp_list_data = []
    brief_list_data = []
    t_brief_data = []
    t_gl_acct_data = []
    t_gl_department_data = []
    t_gl_main_data = []
    t_briefzei_data = []
    i:int = 0
    brief = gl_acct = gl_main = gl_department = briefzei = htparam = None

    t_brief = t_gl_department = t_gl_acct = t_gl_main = brief_list = htp_list = htv_list = t_briefzei = None

    t_brief_data, T_brief = create_model("T_brief", {"briefnr":int})
    t_gl_department_data, T_gl_department = create_model("T_gl_department", {"nr":int, "bezeich":string})
    t_gl_acct_data, T_gl_acct = create_model("T_gl_acct", {"fibukonto":string, "deptnr":int, "bezeich":string, "main_nr":int, "acc_type":int, "actual":[Decimal,12], "budget":[Decimal,12], "last_yr":[Decimal,12], "ly_budget":[Decimal,12]})
    t_gl_main_data, T_gl_main = create_model("T_gl_main", {"nr":int, "code":int, "bezeich":string})
    brief_list_data, Brief_list = create_model("Brief_list", {"b_text":string})
    htp_list_data, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":string})
    htv_list_data, Htv_list = create_model("Htv_list", {"paramnr":int, "fchar":string})
    t_briefzei_data, T_briefzei = create_model("T_briefzei", {"briefnr":int, "briefzeilnr":int, "texte":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal keycmd, keyvar, keycont, htv_list_data, htp_list_data, brief_list_data, t_brief_data, t_gl_acct_data, t_gl_department_data, t_gl_main_data, t_briefzei_data, i, brief, gl_acct, gl_main, gl_department, briefzei, htparam
        nonlocal briefnr


        nonlocal t_brief, t_gl_department, t_gl_acct, t_gl_main, brief_list, htp_list, htv_list, t_briefzei
        nonlocal t_brief_data, t_gl_department_data, t_gl_acct_data, t_gl_main_data, brief_list_data, htp_list_data, htv_list_data, t_briefzei_data

        return {"keycmd": keycmd, "keyvar": keyvar, "keycont": keycont, "htv-list": htv_list_data, "htp-list": htp_list_data, "brief-list": brief_list_data, "t-brief": t_brief_data, "t-gl-acct": t_gl_acct_data, "t-gl-department": t_gl_department_data, "t-gl-main": t_gl_main_data, "t-briefzei": t_briefzei_data}

    def fill_list():

        nonlocal keycmd, keyvar, keycont, htv_list_data, htp_list_data, brief_list_data, t_brief_data, t_gl_acct_data, t_gl_department_data, t_gl_main_data, t_briefzei_data, brief, gl_acct, gl_main, gl_department, briefzei, htparam
        nonlocal briefnr


        nonlocal t_brief, t_gl_department, t_gl_acct, t_gl_main, brief_list, htp_list, htv_list, t_briefzei
        nonlocal t_brief_data, t_gl_department_data, t_gl_acct_data, t_gl_main_data, brief_list_data, htp_list_data, htv_list_data, t_briefzei_data

        i:int = 0
        j:int = 0
        n:int = 0
        c:string = ""
        l:int = 0
        continued:bool = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 600)]})
        keycmd = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 2030)]})
        keyvar = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1122)]})
        keycont = keycmd + htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == 39) & (Htparam.paramnr != 2030)).order_by(length(Htparam.fchar).desc()).all():

            if substring(htparam.fchar, 0 , 1) == (".").lower() :
                htv_list = Htv_list()
                htv_list_data.append(htv_list)

                htv_list.paramnr = htparam.paramnr
                htv_list.fchar = htparam.fchar
            else:
                htp_list = Htp_list()
                htp_list_data.append(htp_list)

                htp_list.paramnr = htparam.paramnr
                htp_list.fchar = keycmd + htparam.fchar

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
                        brief_list.b_text = substring(brief_list.b_text, 0, length(brief_list.b_text) - length(keycont))
                    else:
                        continued = False
            n = length(briefzei.texte) - j + 1
            c = substring(briefzei.texte, j - 1, n)

            if not continued:
                brief_list = Brief_list()
                brief_list_data.append(brief_list)

            brief_list.b_text = brief_list.b_text + c


    fill_list()

    for brief in db_session.query(Brief).order_by(Brief._recid).all():
        t_brief = T_brief()
        t_brief_data.append(t_brief)

        t_brief.briefnr = brief.briefnr

    for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
        t_gl_acct = T_gl_acct()
        t_gl_acct_data.append(t_gl_acct)

        t_gl_acct.fibukonto = gl_acct.fibukonto
        t_gl_acct.deptnr = gl_acct.deptnr
        t_gl_acct.bezeich = gl_acct.bezeich
        t_gl_acct.main_nr = gl_acct.main_nr
        t_gl_acct.acc_type = gl_acct.acc_type


        for i in range(1,12 + 1) :
            t_gl_acct.actual[i - 1] = gl_acct.actual[i - 1]
            t_gl_acct.budget[i - 1] = gl_acct.budget[i - 1]
            t_gl_acct.last_yr[i - 1] = gl_acct.last_yr[i - 1]
            t_gl_acct.ly_budget[i - 1] = gl_acct.ly_budget[i - 1]


            i = i + 1

    for gl_main in db_session.query(Gl_main).order_by(Gl_main._recid).all():
        t_gl_main = T_gl_main()
        t_gl_main_data.append(t_gl_main)

        t_gl_main.nr = gl_main.nr
        t_gl_main.code = gl_main.code
        t_gl_main.bezeich = gl_main.bezeich

    for gl_department in db_session.query(Gl_department).order_by(Gl_department._recid).all():
        t_gl_department = T_gl_department()
        t_gl_department_data.append(t_gl_department)

        t_gl_department.nr = gl_department.nr
        t_gl_department.bezeich = gl_department.bezeich

    for briefzei in db_session.query(Briefzei).filter(
             (Briefzei.briefnr == briefnr)).order_by(Briefzei._recid).all():
        t_briefzei = T_briefzei()
        t_briefzei_data.append(t_briefzei)

        t_briefzei.briefnr = briefzei.briefnr
        t_briefzei.briefzeilnr = briefzei.briefzeilnr
        t_briefzei.texte = briefzei.texte

    return generate_output()