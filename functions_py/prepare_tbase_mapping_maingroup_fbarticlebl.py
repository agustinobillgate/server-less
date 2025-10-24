#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix definition variabel
            - fix python indentation
            - add type ignore to avoid warning
            - activate model Wgrpgen & Ekum
""" 

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Wgrpgen, Ekum

def prepare_tbase_mapping_maingroup_fbarticlebl():

    prepare_cache ([Queasy, Wgrpgen, Ekum])

    mgroup_list_data = []
    queasy = None
    
    wgrpgen = Wgrpgen()
    ekum = Ekum()

    mgroup_list = bmgroup_list = None

    mgroup_list_data, Mgroup_list = create_model(
        "Mgroup_list", {
            "vhp_nr":int, 
            "vhp_bezeich":string, 
            "tbase_nr":int, 
            "tbase_bezeich":string, 
            "queasy_recid":int, 
            "resto_artikel":bool, 
            "bill_artikel":bool
            }
        )
    
    bmgroup_list_data, Bmgroup_list = create_model_like(Mgroup_list)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mgroup_list_data, queasy, wgrpgen, ekum


        nonlocal mgroup_list, bmgroup_list
        nonlocal mgroup_list_data, bmgroup_list_data

        return {
            "mgroup-list": mgroup_list_data
        }


    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 369) & (Queasy.char1 == ("maingroup-fb").lower())).order_by(Queasy._recid).all():
        bmgroup_list = Bmgroup_list()
        bmgroup_list_data.append(bmgroup_list)

        bmgroup_list.vhp_nr = queasy.number2
        bmgroup_list.vhp_bezeich = queasy.char2
        bmgroup_list.tbase_nr = queasy.number3
        bmgroup_list.tbase_bezeich = queasy.char3
        bmgroup_list.queasy_recid = queasy._recid

        if queasy.logi1 :
            bmgroup_list.resto_artikel = True

        elif queasy.logi2 :
            bmgroup_list.bill_artikel = True

    bmgroup_list = query(bmgroup_list_data, first=True)

    if not bmgroup_list:
        for wgrpgen in db_session.query(Wgrpgen).order_by(Wgrpgen.eknr).all():
            bmgroup_list = Bmgroup_list()
            bmgroup_list_data.append(bmgroup_list)

            bmgroup_list.vhp_nr = wgrpgen.eknr
            bmgroup_list.vhp_bezeich = wgrpgen.bezeich
            bmgroup_list.resto_artikel = True

        for ekum in db_session.query(Ekum).order_by(Ekum.eknr).all():
            bmgroup_list = Bmgroup_list()
            bmgroup_list_data.append(bmgroup_list)

            bmgroup_list.vhp_nr = ekum.eknr
            bmgroup_list.vhp_bezeich = ekum.bezeich
            bmgroup_list.bill_artikel = True

    elif bmgroup_list:
        for wgrpgen in db_session.query(Wgrpgen).order_by(Wgrpgen._recid).all():
            bmgroup_list = query(bmgroup_list_data, filters=(lambda bmgroup_list: bmgroup_list.vhp_nr == wgrpgen.eknr and bmgroup_list.resto_artikel), first=True)

            if not bmgroup_list:
                bmgroup_list = Bmgroup_list()
                bmgroup_list_data.append(bmgroup_list)

                bmgroup_list.vhp_nr = wgrpgen.eknr
                bmgroup_list.vhp_bezeich = wgrpgen.bezeich
                bmgroup_list.resto_artikel = True

        for ekum in db_session.query(Ekum).order_by(Ekum.eknr).all():
            bmgroup_list = query(bmgroup_list_data, filters=(lambda bmgroup_list: bmgroup_list.vhp_nr == ekum.eknr and bmgroup_list.bill_artikel), first=True)

            if not bmgroup_list:
                bmgroup_list = Bmgroup_list()
                bmgroup_list_data.append(bmgroup_list)

                bmgroup_list.vhp_nr = ekum.eknr
                bmgroup_list.vhp_bezeich = ekum.bezeich
                bmgroup_list.bill_artikel = True

    for bmgroup_list in query(bmgroup_list_data, sort_by=[("resto_artikel",False),("vhp_nr",False)]):  # type: ignore bmgroup_list_data masih bernilai none
        mgroup_list = Mgroup_list()
        mgroup_list_data.append(mgroup_list)

        buffer_copy(bmgroup_list, mgroup_list)

    return generate_output()