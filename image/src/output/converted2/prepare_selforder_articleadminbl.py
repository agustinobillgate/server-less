#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Hoteldpt, H_artikel, Queasy

def prepare_selforder_articleadminbl(dept:string, case_type:int):

    prepare_cache ([Paramtext, Hoteldpt, H_artikel, Queasy])

    licensenr = 0
    t_article_list = []
    t_dept_list = []
    nr:int = 0
    paramtext = hoteldpt = h_artikel = queasy = None

    t_article = t_dept = None

    t_article_list, T_article = create_model("T_article", {"nr":int, "artnr":int, "dept":int, "bezeich":string, "img":string, "remark":string, "activ_art":bool, "sold_out":bool, "selected_art":bool})
    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal licensenr, t_article_list, t_dept_list, nr, paramtext, hoteldpt, h_artikel, queasy
        nonlocal dept, case_type


        nonlocal t_article, t_dept
        nonlocal t_article_list, t_dept_list

        return {"licensenr": licensenr, "t-article": t_article_list, "t-dept": t_dept_list}

    def decode_string1(in_str:string):

        nonlocal licensenr, t_article_list, t_dept_list, nr, paramtext, hoteldpt, h_artikel, queasy
        nonlocal dept, case_type


        nonlocal t_article, t_dept
        nonlocal t_article_list, t_dept_list

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (length(out_str) - 4))

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal licensenr, t_article_list, t_dept_list, nr, paramtext, hoteldpt, h_artikel, queasy
        nonlocal dept, case_type


        nonlocal t_article, t_dept
        nonlocal t_article_list, t_dept_list

        out_str = ""
        s:string = ""
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

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    if dept == "":

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 1)]})
        dept = hoteldpt.depart

    hoteldpt = get_cache (Hoteldpt, {"depart": [(eq, dept)]})

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == hoteldpt.num) & (H_artikel.activeflag) & (H_artikel.artart == 0) & (H_artikel.epreis1 != 0)).order_by(H_artikel._recid).all():

        queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_artikel.artnr)],"number3": [(eq, h_artikel.departement)]})

        if queasy:
            t_article = T_article()
            t_article_list.append(t_article)

            t_article.artnr = queasy.number2
            t_article.dept = queasy.number3
            t_article.bezeich = h_artikel.bezeich
            t_article.img = queasy.char2
            t_article.remark = queasy.char3
            t_article.activ_art = queasy.logi1
            t_article.sold_out = queasy.logi2


        else:
            t_article = T_article()
            t_article_list.append(t_article)

            t_article.artnr = h_artikel.artnr
            t_article.dept = h_artikel.departement
            t_article.bezeich = h_artikel.bezeich


    nr = 0

    for t_article in query(t_article_list, sort_by=[("activ_art",True),("bezeich",False)]):
        nr = nr + 1
        t_article.nr = nr
    nr = 0

    for t_article in query(t_article_list, sort_by=[("activ_art",True),("bezeich",False)]):
        nr = nr + 1
        t_article.nr = nr

    return generate_output()