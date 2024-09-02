from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Parameters, L_lager, Bediener, Htparam, L_artikel, L_untergrup, L_hauptgrp

def prepare_s_storerequest_1bl(user_init:str):
    show_price = False
    req_flag = False
    transdate = None
    t_parameters_list = []
    t_l_lager_list = []
    temp_l_artikel_list = []
    art_list_list = []
    parameters = l_lager = bediener = htparam = l_artikel = l_untergrup = l_hauptgrp = None

    temp_l_artikel = t_parameters = t_l_lager = art_list = None

    temp_l_artikel_list, Temp_l_artikel = create_model("Temp_l_artikel", {"artnr":int, "betriebsnr":int, "endkum":int, "bezeich":str, "masseinheit":str, "vk_preis":decimal, "lief_einheit":decimal, "traubensort":str})
    t_parameters_list, T_parameters = create_model_like(Parameters)
    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    art_list_list, Art_list = create_model("Art_list", {"artnr":int, "zwkum":int, "endkum":int, "zwkum_bezeich":str, "endkum_bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, req_flag, transdate, t_parameters_list, t_l_lager_list, temp_l_artikel_list, art_list_list, parameters, l_lager, bediener, htparam, l_artikel, l_untergrup, l_hauptgrp


        nonlocal temp_l_artikel, t_parameters, t_l_lager, art_list
        nonlocal temp_l_artikel_list, t_parameters_list, t_l_lager_list, art_list_list
        return {"show_price": show_price, "req_flag": req_flag, "transdate": transdate, "t-parameters": t_parameters_list, "t-l-lager": t_l_lager_list, "temp-l-artikel": temp_l_artikel_list, "art-list": art_list_list}


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 475)).first()
    req_flag = not htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    transdate = htparam.fdate

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name")).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        buffer_copy(parameters, t_parameters)

    for l_lager in db_session.query(L_lager).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for l_artikel in db_session.query(L_artikel).all():
        temp_l_artikel = Temp_l_artikel()
        temp_l_artikel_list.append(temp_l_artikel)

        temp_l_artikel.artnr = l_artikel.artnr
        temp_l_artikel.betriebsnr = l_artikel.betriebsnr
        temp_l_artikel.endkum = l_artikel.endkum
        temp_l_artikel.bezeich = l_artikel.bezeich
        temp_l_artikel.masseinheit = l_artikel.masseinheit
        temp_l_artikel.vk_preis = l_artikel.vk_preis
        temp_l_artikel.lief_einheit = l_artikel.lief_einheit
        temp_l_artikel.traubensort = l_artikel.traubensorte

    for l_artikel in db_session.query(L_artikel).all():

        l_untergrup = db_session.query(L_untergrup).filter(
                (L_untergrup.zwkum == l_artikel.zwkum)).first()

        if l_untergrup:

            l_hauptgrp = db_session.query(L_hauptgrp).filter(
                    (L_hauptgrp.endkum == l_artikel.endkum)).first()

            if l_hauptgrp:
                art_list = Art_list()
                art_list_list.append(art_list)

                art_list.artnr = l_artikel.artnr
                art_list.zwkum = l_untergrup.zwkum
                art_list.endkum = l_hauptgrp.endkum
                art_list.zwkum_bezeich = l_untergrup.bezeich
                art_list.endkum_bezeich = l_hauptgrp.bezeich

    return generate_output()