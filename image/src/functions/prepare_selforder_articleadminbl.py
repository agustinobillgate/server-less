from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Paramtext, Hoteldpt, H_artikel, Queasy

def prepare_selforder_articleadminbl(dept:str, case_type:int):
    licensenr = 0
    t_article_list = []
    t_dept_list = []
    nr:int = 0
    paramtext = hoteldpt = h_artikel = queasy = None

    t_article = t_dept = None

    t_article_list, T_article = create_model("T_article", {"nr":int, "artnr":int, "dept":int, "bezeich":str, "img":str, "remark":str, "activ_art":bool, "sold_out":bool, "selected_art":bool})
    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal licensenr, t_article_list, t_dept_list, nr, paramtext, hoteldpt, h_artikel, queasy


        nonlocal t_article, t_dept
        nonlocal t_article_list, t_dept_list
        return {"licensenr": licensenr, "t-article": t_article_list, "t-dept": t_dept_list}

    def decode_string1(in_str:str):

        nonlocal licensenr, t_article_list, t_dept_list, nr, paramtext, hoteldpt, h_artikel, queasy


        nonlocal t_article, t_dept
        nonlocal t_article_list, t_dept_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 71
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (len(out_str) - 4))


        return generate_inner_output()

    def decode_string(in_str:str):

        nonlocal licensenr, t_article_list, t_dept_list, nr, paramtext, hoteldpt, h_artikel, queasy


        nonlocal t_article, t_dept
        nonlocal t_article_list, t_dept_list

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


    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(ptexte)

    for hoteldpt in db_session.query(Hoteldpt).filter(
            (Hoteldpt.num > 0)).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    if dept == "":

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == 1)).first()
        dept = hoteldpt.depart

    hoteldpt = db_session.query(Hoteldpt).filter(
            (func.lower(Hoteldpt.depart) == (dept).lower())).first()

    for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == hoteldpt.num) &  (H_artikel.activeflag) &  (H_artikel.artart == 0) &  (H_artikel.epreis1 != 0)).all():

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.number1 == 2) &  (Queasy.number2 == h_artikel.artnr) &  (Queasy.number3 == h_artikel.departement)).first()

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

    for t_article in query(t_article_list):
        nr = nr + 1
        t_article.nr = nr
    nr = 0

    for t_article in query(t_article_list):
        nr = nr + 1
        t_article.nr = nr

    return generate_output()