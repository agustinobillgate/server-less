from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, L_order, Htparam, L_artikel, L_bestand, Parameters, Dml_art

def prepare_mk_pr_1bl(docu_nr:str, tp_bediener_user_group:int, tp_bediener_username:str, dml_flag:bool, dml_grp:int, dml_datum:date, cost_acct:str):
    billdate = None
    eng_dept = 0
    pos = 0
    dml_created = False
    p_370 = False
    t_l_orderhdr_list = []
    s_list_list = []
    t_l_artikel_list = []
    t_parameters_list = []
    l_orderhdr = l_order = htparam = l_artikel = l_bestand = parameters = dml_art = None

    t_parameters = t_l_orderhdr = t_l_artikel = s_list = l_orderhdr1 = None

    t_parameters_list, T_parameters = create_model("T_parameters", {"varname":str, "vstring":str})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "bezeich":str, "betriebsnr":int, "traubensort":str, "lief_einheit":decimal, "jahrgang":int, "inhalt":decimal, "masseinheit":str, "zwkum":int, "soh":decimal})
    s_list_list, S_list = create_model_like(L_order, {"s_recid":int})

    L_orderhdr1 = L_orderhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, eng_dept, pos, dml_created, p_370, t_l_orderhdr_list, s_list_list, t_l_artikel_list, t_parameters_list, l_orderhdr, l_order, htparam, l_artikel, l_bestand, parameters, dml_art
        nonlocal l_orderhdr1


        nonlocal t_parameters, t_l_orderhdr, t_l_artikel, s_list, l_orderhdr1
        nonlocal t_parameters_list, t_l_orderhdr_list, t_l_artikel_list, s_list_list
        return {"billdate": billdate, "eng_dept": eng_dept, "pos": pos, "dml_created": dml_created, "p_370": p_370, "t-l-orderhdr": t_l_orderhdr_list, "s-list": s_list_list, "t-l-artikel": t_l_artikel_list, "t-parameters": t_parameters_list}

    def new_pr_number():

        nonlocal billdate, eng_dept, pos, dml_created, p_370, t_l_orderhdr_list, s_list_list, t_l_artikel_list, t_parameters_list, l_orderhdr, l_order, htparam, l_artikel, l_bestand, parameters, dml_art
        nonlocal l_orderhdr1


        nonlocal t_parameters, t_l_orderhdr, t_l_artikel, s_list, l_orderhdr1
        nonlocal t_parameters_list, t_l_orderhdr_list, t_l_artikel_list, s_list_list

        s:str = ""
        i:int = 1
        L_orderhdr1 = L_orderhdr
        s = "R" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                (L_orderhdr1.bestelldatum == billdate)).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            docu_nr = s + to_string(i, "999")

            return
        docu_nr = s + to_string(i, "999")

    def create_dml_pr():

        nonlocal billdate, eng_dept, pos, dml_created, p_370, t_l_orderhdr_list, s_list_list, t_l_artikel_list, t_parameters_list, l_orderhdr, l_order, htparam, l_artikel, l_bestand, parameters, dml_art
        nonlocal l_orderhdr1


        nonlocal t_parameters, t_l_orderhdr, t_l_artikel, s_list, l_orderhdr1
        nonlocal t_parameters_list, t_l_orderhdr_list, t_l_artikel_list, s_list_list

        if pos == 0:
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.docu_nr = docu_nr
            s_list.pos = 0
            s_list.bestelldatum = l_orderhdr.bestelldatum
            s_list.op_art = 1

        if dml_grp == 0:

            dml_art_obj_list = []
            for dml_art, l_artikel in db_session.query(Dml_art, L_artikel).join(L_artikel,(L_artikel.artnr == Dml_art.artnr)).filter(
                    (Dml_art.datum == dml_datum) &  (Dml_art.anzahl != 0)).all():
                if dml_art._recid in dml_art_obj_list:
                    continue
                else:
                    dml_art_obj_list.append(dml_art._recid)


                pos = pos + 1
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.docu_nr = docu_nr
                s_list.artnr = l_artikel.artnr
                s_list.anzahl = dml_art.anzahl
                s_list.lieferdatum = dml_art.datum
                s_list.pos = pos
                s_list.bestelldatum = l_orderhdr.bestelldatum
                s_list.op_art = 1
                s_list.lief_fax[0] = tp_bediener_username
                s_list.lief_fax[2] = l_artikel.traubensorte
                s_list.flag = True

                if l_artikel.lief_einheit != 0:
                    s_list.txtnr = l_artikel.lief_einheit

                if to_int(cost_acct) != 0:
                    s_list.stornogrund = cost_acct
        else:

            dml_art_obj_list = []
            for dml_art, l_artikel in db_session.query(Dml_art, L_artikel).join(L_artikel,(L_artikel.artnr == Dml_art.artnr) &  (L_artikel.zwkum == dml_grp)).filter(
                    (Dml_art.datum == dml_datum)).all():
                if dml_art._recid in dml_art_obj_list:
                    continue
                else:
                    dml_art_obj_list.append(dml_art._recid)


                pos = pos + 1
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.docu_nr = docu_nr
                s_list.artnr = l_artikel.artnr
                s_list.anzahl = dml_art.anzahl
                s_list.lieferdatum = dml_art.datum
                s_list.stornogrund = cost_acct
                s_list.pos = pos
                s_list.bestelldatum = l_orderhdr.bestelldatum
                s_list.op_art = 1
                s_list.lief_fax[0] = tp_bediener_username
                s_list.lief_fax[2] = l_artikel.traubensorte
                s_list.flag = True

                if l_artikel.lief_einheit != 0:
                    s_list.txtnr = l_artikel.lief_einheit

                if to_int(cost_acct) != 0:
                    s_list.stornogrund = cost_acct
        dml_created = True
        l_orderhdr.lieferdatum = dml_datum


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1060)).first()

    if htparam.finteger != 0 and tp_bediener_user_group == htparam.finteger:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1062)).first()
        eng_dept = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 370)).first()

    if htparam:
        p_370 = htparam.flogical


    new_pr_number()
    l_orderhdr = L_orderhdr()
    db_session.add(l_orderhdr)

    l_orderhdr.betriebsnr = 9
    l_orderhdr.bestelldatum = billdate
    l_orderhdr.lieferdatum = billdate + 1
    l_orderhdr.besteller = tp_bediener_username
    l_orderhdr.gedruckt = None
    l_orderhdr.angebot_lief[0] = eng_dept
    l_orderhdr.lief_fax[1] = " ; ; ; "


    l_orderhdr.docu_nr = docu_nr

    l_orderhdr = db_session.query(L_orderhdr).first()
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_list.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid


    if dml_flag:
        create_dml_pr()

    for l_artikel in db_session.query(L_artikel).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.rec_id = l_artikel._recid
        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.betriebsnr = l_artikel.betriebsnr
        t_l_artikel.traubensort = l_artikel.traubensorte
        t_l_artikel.lief_einheit = l_artikel.lief_einheit
        t_l_artikel.jahrgang = l_artikel.jahrgang
        t_l_artikel.inhalt = l_artikel.inhalt
        t_l_artikel.masseinheit = l_artikel.masseinheit
        t_l_artikel.zwkum = l_artikel.zwkum

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == l_artikel.artnr) &  (L_bestand.lager_nr == 0)).first()

        if l_bestand:
            t_l_artikel.soh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name")).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring

    return generate_output()