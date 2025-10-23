#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix python indentation
            - add type ignore to avoid warning
            - activate model Wgrpdep
""" 

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Hoteldpt, Wgrpdep

def prepare_tbase_mapping_subgroup_fbarticlebl():

    prepare_cache ([Queasy, Hoteldpt, Wgrpdep])

    sgroup_list_data = []
    queasy = hoteldpt = None

    wgrpdep = Wgrpdep()

    sgroup_list = None

    sgroup_list_data, Sgroup_list = create_model(
        "Sgroup_list", {
            "vhp_deptnr":int, 
            "vhp_dept":string, 
            "vhp_nr":int, 
            "vhp_bezeich":string, 
            "tbase_nr":int, 
            "tbase_bezeich":string, 
            "queasy_recid":int
            }
        )

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sgroup_list_data, queasy, hoteldpt, wgrpdep
        nonlocal sgroup_list
        nonlocal sgroup_list_data

        return {
            "sgroup-list": sgroup_list_data
        }

    for queasy in db_session.query(Queasy).filter(
        (Queasy.key == 369) & (Queasy.char1 == ("subgroup-fb").lower())).order_by(Queasy._recid).all():
        sgroup_list = Sgroup_list()
        sgroup_list_data.append(sgroup_list)

        sgroup_list.vhp_nr = queasy.number2
        sgroup_list.vhp_bezeich = queasy.char2
        sgroup_list.tbase_nr = queasy.number3
        sgroup_list.tbase_bezeich = queasy.char3
        sgroup_list.queasy_recid = queasy._recid
        sgroup_list.vhp_deptnr = queasy.number1

        hoteldpt = get_cache (Hoteldpt, {
            "num": [(eq, sgroup_list.vhp_deptnr)]})

        if hoteldpt:
            sgroup_list.vhp_dept = hoteldpt.depart

    sgroup_list = query(sgroup_list_data, first=True)

    if not sgroup_list:
        for wgrpdep in db_session.query(Wgrpdep).order_by(Wgrpdep._recid).all():
            sgroup_list = Sgroup_list()
            sgroup_list_data.append(sgroup_list)

            sgroup_list.vhp_nr = wgrpdep.zknr
            sgroup_list.vhp_bezeich = wgrpdep.bezeich
            sgroup_list.vhp_deptnr = wgrpdep.departement

            hoteldpt = get_cache (Hoteldpt, {
                "num": [(eq, sgroup_list.vhp_deptnr)]})

            if hoteldpt:
                sgroup_list.vhp_dept = hoteldpt.depart

    elif sgroup_list:
        for wgrpdep in db_session.query(Wgrpdep).order_by(Wgrpdep._recid).all():
            sgroup_list = query(sgroup_list_data, filters=(lambda sgroup_list: sgroup_list.vhp_nr == wgrpdep.zknr and sgroup_list.vhp_deptnr == wgrpdep.departement), first=True)

            if not sgroup_list:
                sgroup_list = Sgroup_list()
                sgroup_list_data.append(sgroup_list)

                sgroup_list.vhp_nr = wgrpdep.zknr
                sgroup_list.vhp_bezeich = wgrpdep.bezeich
                sgroup_list.vhp_deptnr = wgrpdep.departement

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, sgroup_list.vhp_deptnr)]})

                if hoteldpt:
                    sgroup_list.vhp_dept = hoteldpt.depart

    return generate_output()