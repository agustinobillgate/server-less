#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr, L_order, Htparam, L_artikel, L_bestand, Parameters, Dml_art
from sqlalchemy.orm.attributes import flag_modified

def prepare_mk_pr_1bl(docu_nr:string, tp_bediener_user_group:int, tp_bediener_username:string, dml_flag:bool, dml_grp:int, dml_datum:date, cost_acct:string):

    prepare_cache ([Htparam, L_artikel, L_bestand, Parameters, Dml_art])

    billdate = None
    eng_dept = 0
    pos = 0
    dml_created = False
    p_370 = False
    t_l_orderhdr_data = []
    s_list_data = []
    t_l_artikel_data = []
    t_parameters_data = []
    l_orderhdr = l_order = htparam = l_artikel = l_bestand = parameters = dml_art = None

    t_parameters = t_l_orderhdr = t_l_artikel = s_list = None

    t_parameters_data, T_parameters = create_model("T_parameters", {"varname":string, "vstring":string})
    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_artikel_data, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "bezeich":string, "betriebsnr":int, "traubensort":string, "lief_einheit":Decimal, "jahrgang":int, "inhalt":Decimal, "masseinheit":string, "zwkum":int, "soh":Decimal})
    s_list_data, S_list = create_model_like(L_order, {"s_recid":int})


    set_cache(L_bestand, (L_bestand.lager_nr == 0),[["artnr", "lager_nr"]], True,[],[])

    db_session = local_storage.db_session
    docu_nr = docu_nr.strip()
    tp_bediener_username = tp_bediener_username.strip()
    cost_acct = cost_acct.strip()

    def generate_output():
        nonlocal billdate, eng_dept, pos, dml_created, p_370, t_l_orderhdr_data, s_list_data, t_l_artikel_data, t_parameters_data, l_orderhdr, l_order, htparam, l_artikel, l_bestand, parameters, dml_art
        nonlocal docu_nr, tp_bediener_user_group, tp_bediener_username, dml_flag, dml_grp, dml_datum, cost_acct


        nonlocal t_parameters, t_l_orderhdr, t_l_artikel, s_list
        nonlocal t_parameters_data, t_l_orderhdr_data, t_l_artikel_data, s_list_data

        return {"docu_nr": docu_nr, "billdate": billdate, "eng_dept": eng_dept, "pos": pos, "dml_created": dml_created, "p_370": p_370, "t-l-orderhdr": t_l_orderhdr_data, "s-list": s_list_data, "t-l-artikel": t_l_artikel_data, "t-parameters": t_parameters_data}

    def new_pr_number():

        nonlocal billdate, eng_dept, pos, dml_created, p_370, t_l_orderhdr_data, s_list_data, t_l_artikel_data, t_parameters_data, l_orderhdr, l_order, htparam, l_artikel, l_bestand, parameters, dml_art
        nonlocal docu_nr, tp_bediener_user_group, tp_bediener_username, dml_flag, dml_grp, dml_datum, cost_acct


        nonlocal t_parameters, t_l_orderhdr, t_l_artikel, s_list
        nonlocal t_parameters_data, t_l_orderhdr_data, t_l_artikel_data, s_list_data

        l_orderhdr1 = None
        s:string = ""
        i:int = 1
        L_orderhdr1 =  create_buffer("L_orderhdr1",L_orderhdr)
        s = "R" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                 (L_orderhdr1.bestelldatum == billdate)).order_by(L_orderhdr1.docu_nr.desc()).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            docu_nr = s + to_string(i, "999")

            return
        docu_nr = s + to_string(i, "999")


    def create_dml_pr():

        nonlocal billdate, eng_dept, pos, dml_created, p_370, t_l_orderhdr_data, s_list_data, t_l_artikel_data, t_parameters_data, l_orderhdr, l_order, htparam, l_artikel, l_bestand, parameters, dml_art
        nonlocal docu_nr, tp_bediener_user_group, tp_bediener_username, dml_flag, dml_grp, dml_datum, cost_acct


        nonlocal t_parameters, t_l_orderhdr, t_l_artikel, s_list
        nonlocal t_parameters_data, t_l_orderhdr_data, t_l_artikel_data, s_list_data

        if pos == 0:
            s_list = S_list()
            s_list_data.append(s_list)

            s_list.docu_nr = docu_nr
            s_list.pos = 0
            s_list.bestelldatum = l_orderhdr.bestelldatum
            s_list.op_art = 1

        if dml_grp == 0:

            dml_art_obj_list = {}
            dml_art = Dml_art()
            l_artikel = L_artikel()
            for dml_art.anzahl, dml_art.datum, dml_art._recid, l_artikel.artnr, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel._recid, l_artikel.bezeich, l_artikel.betriebsnr, l_artikel.jahrgang, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.zwkum in db_session.query(Dml_art.anzahl, Dml_art.datum, Dml_art._recid, L_artikel.artnr, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel._recid, L_artikel.bezeich, L_artikel.betriebsnr, L_artikel.jahrgang, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.zwkum).join(L_artikel,(L_artikel.artnr == Dml_art.artnr)).filter(
                     (Dml_art.datum == dml_datum) & (Dml_art.anzahl != 0)).order_by(L_artikel.bezeich).with_for_update().all():
                if dml_art_obj_list.get(dml_art._recid):
                    continue
                else:
                    dml_art_obj_list[dml_art._recid] = True


                pos = pos + 1
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.docu_nr = docu_nr
                s_list.artnr = l_artikel.artnr
                s_list.anzahl =  to_decimal(dml_art.anzahl)
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

            dml_art_obj_list = {}
            dml_art = Dml_art()
            l_artikel = L_artikel()
            for dml_art.anzahl, dml_art.datum, dml_art._recid, l_artikel.artnr, l_artikel.traubensorte, l_artikel.lief_einheit, l_artikel._recid, l_artikel.bezeich, l_artikel.betriebsnr, l_artikel.jahrgang, l_artikel.inhalt, l_artikel.masseinheit, l_artikel.zwkum in db_session.query(Dml_art.anzahl, Dml_art.datum, Dml_art._recid, L_artikel.artnr, L_artikel.traubensorte, L_artikel.lief_einheit, L_artikel._recid, L_artikel.bezeich, L_artikel.betriebsnr, L_artikel.jahrgang, L_artikel.inhalt, L_artikel.masseinheit, L_artikel.zwkum).join(L_artikel,(L_artikel.artnr == Dml_art.artnr) & (L_artikel.zwkum == dml_grp)).filter(
                     (Dml_art.datum == dml_datum)).order_by(L_artikel.bezeich).with_for_update().all():
                if dml_art_obj_list.get(dml_art._recid):
                    continue
                else:
                    dml_art_obj_list[dml_art._recid] = True


                pos = pos + 1
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.docu_nr = docu_nr
                s_list.artnr = l_artikel.artnr
                s_list.anzahl =  to_decimal(dml_art.anzahl)
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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1060)]})

    if htparam.finteger != 0 and tp_bediener_user_group == htparam.finteger:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1062)]})
        eng_dept = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 370)]})

    if htparam:
        p_370 = htparam.flogical


    new_pr_number()
    l_orderhdr = L_orderhdr()
    db_session.add(l_orderhdr)

    l_orderhdr.betriebsnr = 9
    l_orderhdr.bestelldatum = billdate
    l_orderhdr.lieferdatum = billdate + timedelta(days=1)
    l_orderhdr.besteller = tp_bediener_username
    l_orderhdr.gedruckt = None
    l_orderhdr.angebot_lief[0] = eng_dept
    l_orderhdr.lief_fax[1] = " ; ; ; "


    l_orderhdr.docu_nr = docu_nr
    pass
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_data.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    if dml_flag:
        create_dml_pr()

    for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():
        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        t_l_artikel.rec_id = l_artikel._recid
        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.betriebsnr = l_artikel.betriebsnr
        t_l_artikel.traubensort = l_artikel.traubensorte
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.jahrgang = l_artikel.jahrgang
        t_l_artikel.inhalt =  to_decimal(l_artikel.inhalt)
        t_l_artikel.masseinheit = l_artikel.masseinheit
        t_l_artikel.zwkum = l_artikel.zwkum

        l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

        if l_bestand:
            t_l_artikel.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower())).order_by(Parameters._recid).all():
        t_parameters = T_parameters()
        t_parameters_data.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring

    return generate_output()