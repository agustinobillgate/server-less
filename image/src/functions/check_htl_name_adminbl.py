from functions.additional_functions import *
import decimal
from models import Htparam, Paramtext

def check_htl_name_adminbl():
    flag = False
    t_list_list = []
    htparam = paramtext = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"htl_name":str, "htl_adr1":str, "htl_adr2":str, "htl_adr3":str, "htl_tel":str, "htl_fax":str, "htl_email":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, t_list_list, htparam, paramtext


        nonlocal t_list
        nonlocal t_list_list
        return {"flag": flag, "t-list": t_list_list}

    def fill_list():

        nonlocal flag, t_list_list, htparam, paramtext


        nonlocal t_list
        nonlocal t_list_list

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 200)).first()
        t_list.htl_name = paramtext.ptexte

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 201)).first()
        t_list.htl_adr1 = paramtext.ptexte

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 202)).first()
        t_list.htl_adr2 = paramtext.ptexte

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 203)).first()
        t_list.htl_adr3 = paramtext.ptexte

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 204)).first()
        t_list.htl_tel = paramtext.ptexte

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 205)).first()
        t_list.htl_fax = paramtext.ptexte

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 206)).first()
        t_list.htl_email = paramtext.ptexte

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 996)).first()

    if not htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1015)).first()

        if not htparam.flogical:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 990)).first()

            if htparam.flogical:
                flag = True
    t_list = T_list()
    t_list_list.append(t_list)

    fill_list()

    return generate_output()