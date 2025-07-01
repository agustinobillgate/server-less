#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Hoteldpt, H_artikel

def prepare_tada_mappingbl(dept:int):

    prepare_cache ([Hoteldpt, H_artikel])

    t_dept_list = []
    t_queasy270_list = []
    vhp_art_list = []
    t_article_list = []
    queasy = hoteldpt = h_artikel = None

    t_dept = t_queasy270 = vhp_art = t_article = None

    t_dept_list, T_dept = create_model("T_dept", {"nr":int, "dept":string})
    t_queasy270_list, T_queasy270 = create_model_like(Queasy)
    vhp_art_list, Vhp_art = create_model("Vhp_art", {"art_dept":int, "art_nr":int, "art_name":string})
    t_article_list, T_article = create_model("T_article", {"vhpdept":int, "vhpartnr":int, "vhpbezeich":string, "vhpflag":bool, "tadadept":int, "tadaartnr":int, "tadabezeich":string, "tadaflag":bool, "tadasku":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_dept_list, t_queasy270_list, vhp_art_list, t_article_list, queasy, hoteldpt, h_artikel
        nonlocal dept


        nonlocal t_dept, t_queasy270, vhp_art, t_article
        nonlocal t_dept_list, t_queasy270_list, vhp_art_list, t_article_list

        return {"t-dept": t_dept_list, "t-queasy270": t_queasy270_list, "vhp-art": vhp_art_list, "t-article": t_article_list}


    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():
        t_dept = T_dept()
        t_dept_list.append(t_dept)

        t_dept.nr = hoteldpt.num
        t_dept.dept = hoteldpt.depart.upper()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 1)).order_by(Queasy.betriebsnr, Queasy.number2).all():
        t_queasy270 = T_queasy270()
        t_queasy270_list.append(t_queasy270)

        buffer_copy(queasy, t_queasy270)

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == dept) & (H_artikel.artart == 0) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():
        vhp_art = Vhp_art()
        vhp_art_list.append(vhp_art)

        vhp_art.art_dept = h_artikel.departement
        vhp_art.art_nr = h_artikel.artnr
        vhp_art.art_name = h_artikel.bezeich

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 270) & (Queasy.number1 == 2) & (Queasy.betriebsnr == dept)).order_by(Queasy._recid).all():
        t_article = T_article()
        t_article_list.append(t_article)

        t_article.vhpdept = queasy.betriebsnr
        t_article.tadadept = queasy.deci1
        t_article.tadaartnr = queasy.number2
        t_article.vhpartnr = queasy.number3
        t_article.tadasku = queasy.char1
        t_article.tadabezeich = queasy.char2
        t_article.vhpbezeich = queasy.char3
        t_article.tadaflag = queasy.logi2
        t_article.vhpflag = queasy.logi3

    return generate_output()