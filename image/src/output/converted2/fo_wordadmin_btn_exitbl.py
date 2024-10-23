from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Brief, Bediener, Res_history

t_brief_list, T_brief = create_model_like(Brief)

def fo_wordadmin_btn_exitbl(t_brief_list:[T_brief], case_type:int, last_column:str, kateg:int, user_init:str):
    success_flag = False
    v_log:bool = False
    chcol:List[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "i", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]
    brief = bediener = res_history = None

    t_brief = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, v_log, chcol, brief, bediener, res_history
        nonlocal case_type, last_column, kateg, user_init


        nonlocal t_brief
        nonlocal t_brief_list
        return {"success_flag": success_flag}

    def fill_brief():

        nonlocal success_flag, v_log, chcol, brief, bediener, res_history
        nonlocal case_type, last_column, kateg, user_init


        nonlocal t_brief
        nonlocal t_brief_list

        ind:int = 0
        ind = get_columnno(last_column)

        if case_type == 2:

            if trim(brief.briefbezeich) != trim(t_brief.briefbezeich) or brief.fname != t_brief.fname or brief.ftyp != ind or brief.etk_anzahl != t_brief.etk_anzahl:
                v_log = True

            if v_log:

                bediener = db_session.query(Bediener).filter(
                         (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "F/O Excel Program Setup"
                res_history.aenderung = "Modify FileNo " + to_string(brief.briefnr) + " => "

                if trim(brief.briefbezeich) != trim(t_brief.briefbezeich):
                    res_history.aenderung = res_history.aenderung + brief.briefbezeich + " to " + t_brief.briefbezeich + ";"

                if brief.fname != t_brief.fname:
                    res_history.aenderung = res_history.aenderung + "NameFile " + to_string(brief.fname) + " to " + to_string(t_brief.fname) + ";"

                if brief.ftyp != ind:
                    res_history.aenderung = res_history.aenderung + "Lastcolomn " + to_string(brief.ftyp) + " to " + to_string(ind) + ";"

                if brief.etk_anzahl != t_brief.etk_anzahl:
                    res_history.aenderung = res_history.aenderung + "Lastrow " + to_string(brief.etk_anzahl) + " to " + to_string(t_brief.etk_anzahl) + ";"
        brief.briefnr = t_brief.briefnr
        brief.briefbezeich = t_brief.briefbezeich
        brief.fname = t_brief.fname
        brief.briefkateg = kateg
        brief.ftyp = ind
        brief.etk_anzahl = t_brief.etk_anzahl


    def get_columnno(last_column:str):

        nonlocal success_flag, v_log, chcol, brief, bediener, res_history
        nonlocal case_type, kateg, user_init


        nonlocal t_brief
        nonlocal t_brief_list

        ind = 1
        i:int = 0
        ind1:int = 0
        ind2:int = 0

        def generate_inner_output():
            return (ind)


        if len(last_column) == 2:
            for i in range(1,26 + 1) :

                if chcol[i - 1] == substring(last_column, 0, 1):
                    ind1 = i * 26
            for i in range(1,26 + 1) :

                if chcol[i - 1] == substring(last_column, 1, 1):
                    ind2 = i
            ind = ind1 + ind2
        else:
            for i in range(1,26 + 1) :

                if chcol[i - 1] == (last_column).lower() :
                    ind = i

                    return generate_inner_output()

        return generate_inner_output()


    t_brief = query(t_brief_list, first=True)

    if case_type == 1:
        brief = Brief()
        db_session.add(brief)

        fill_brief()
        success_flag = True

    elif case_type == 2:

        brief = db_session.query(Brief).filter(
                 (Brief.briefnr == t_brief.briefnr)).first()

        if brief:
            fill_brief()
            success_flag = True

    return generate_output()