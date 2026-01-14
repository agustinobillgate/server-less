# using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Parameters, L_lager, Bediener, Htparam, L_artikel, L_untergrup, L_hauptgrp, L_bestand




def prepare_s_storerequest_1bl(user_init: string):

    prepare_cache([Bediener, Htparam, L_artikel, L_untergrup, L_hauptgrp])

    show_price = False
    req_flag = False
    transdate = None
    t_parameters_data = []
    t_l_lager_data = []
    temp_l_artikel_data = []
    art_list_data = []
    parameters = l_lager = bediener = htparam = l_artikel = l_untergrup = l_hauptgrp = None

    temp_l_artikel = t_parameters = t_l_lager = art_list = None

    temp_l_artikel_data, Temp_l_artikel = create_model(
        "Temp_l_artikel",
        {
            "artnr": int,
            "betriebsnr": int,
            "endkum": int,
            "bezeich": string,
            "masseinheit": string,
            "vk_preis": Decimal,
            "lief_einheit": Decimal,
            "traubensort": string
        })
    t_parameters_data, T_parameters = create_model_like(Parameters)
    t_l_lager_data, T_l_lager = create_model_like(L_lager)
    art_list_data, Art_list = create_model(
        "Art_list",
        {
            "artnr": int,
            "zwkum": int,
            "endkum": int,
            "zwkum_bezeich": string,
            "endkum_bezeich": string
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, req_flag, transdate, t_parameters_data, t_l_lager_data, temp_l_artikel_data, art_list_data, parameters, l_lager, bediener, htparam, l_artikel, l_untergrup, l_hauptgrp
        nonlocal user_init
        nonlocal temp_l_artikel, t_parameters, t_l_lager, art_list
        nonlocal temp_l_artikel_data, t_parameters_data, t_l_lager_data, art_list_data

        return {
            "show_price": show_price,
            "req_flag": req_flag,
            "transdate": transdate,
            "t-parameters": t_parameters_data,
            "t-l-lager": t_l_lager_data,
            "temp-l-artikel": temp_l_artikel_data,
            "art-list": art_list_data
        }

    bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache(Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    htparam = get_cache(Htparam, {"paramnr": [(eq, 475)]})
    req_flag = not htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 110)]})
    transdate = htparam.fdate

    parameters_query = (
        db_session.query(Parameters)
        .filter(
            ((Parameters.progname) == "costcenter") &
            ((Parameters.section) == "name")
        )
        .order_by(Parameters._recid)
    )

    for parameters in parameters_query.yield_per(100):
        t_parameters = T_parameters()
        t_parameters_data.append(t_parameters)

        buffer_copy(parameters, t_parameters)
        

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid):
        t_l_lager = T_l_lager()
        t_l_lager_data.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    # try filter excecution query
    artikel_query = (
        db_session.query(L_artikel)
        # .join(L_bestand,
        #       L_artikel.artnr == L_bestand.artnr)
        # .filter(
        #     (L_bestand.anz_anf_best + L_bestand.anz_eingang - L_bestand.anz_ausgang) >= 0, 
        # )
        .order_by(L_artikel._recid))
    
    for l_artikel in artikel_query.yield_per(1000):
        
        # print(f"l_artikel: {l_artikel.artnr} {l_artikel.bezeich}")
        
        temp_l_artikel = Temp_l_artikel()
        temp_l_artikel_data.append(temp_l_artikel)

        temp_l_artikel.artnr = l_artikel.artnr
        temp_l_artikel.betriebsnr = l_artikel.betriebsnr
        temp_l_artikel.endkum = l_artikel.endkum
        temp_l_artikel.bezeich = l_artikel.bezeich
        temp_l_artikel.masseinheit = l_artikel.masseinheit
        temp_l_artikel.vk_preis = to_decimal(l_artikel.vk_preis)
        temp_l_artikel.lief_einheit = to_decimal(l_artikel.lief_einheit)
        temp_l_artikel.traubensort = l_artikel.traubensorte

    # for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).yield_per(100):

        l_untergrup = get_cache(
            L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

        if l_untergrup:

            l_hauptgrp = get_cache(
                L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

            if l_hauptgrp:
                art_list = Art_list()
                art_list_data.append(art_list)

                art_list.artnr = l_artikel.artnr
                art_list.zwkum = l_untergrup.zwkum
                art_list.endkum = l_hauptgrp.endkum
                art_list.zwkum_bezeich = l_untergrup.bezeich
                art_list.endkum_bezeich = l_hauptgrp.bezeich

    return generate_output()
