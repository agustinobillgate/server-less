#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Mc_disc, Hoteldpt, Mc_types

def prepare_mc_discadmin_webbl(curr_nr:int):

    prepare_cache ([Hoteldpt, Mc_types])

    types_bezeich = ""
    disc_list_list = []
    tdept_list = []
    counter:int = 0
    mc_disc = hoteldpt = mc_types = None

    disc_list = tdept = hbuff = None

    disc_list_list, Disc_list = create_model_like(Mc_disc, {"depart":string, "rec_id":int, "counter":int})
    tdept_list, Tdept = create_model_like(Hoteldpt)

    Hbuff = create_buffer("Hbuff",Hoteldpt)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal types_bezeich, disc_list_list, tdept_list, counter, mc_disc, hoteldpt, mc_types
        nonlocal curr_nr
        nonlocal hbuff


        nonlocal disc_list, tdept, hbuff
        nonlocal disc_list_list, tdept_list

        return {"types_bezeich": types_bezeich, "disc-list": disc_list_list, "tdept": tdept_list}


    mc_types = get_cache (Mc_types, {"nr": [(eq, curr_nr)]})

    if mc_types:
        types_bezeich = mc_types.bezeich

    mc_disc_obj_list = {}
    for mc_disc, hbuff in db_session.query(Mc_disc, Hbuff).join(Hbuff,(Hbuff.num == Mc_disc.departement)).filter(
             (Mc_disc.nr == curr_nr)).order_by(Mc_disc.artnrfront).all():
        if mc_disc_obj_list.get(mc_disc._recid):
            continue
        else:
            mc_disc_obj_list[mc_disc._recid] = True


        counter = counter + 1
        disc_list = Disc_list()
        disc_list_list.append(disc_list)

        buffer_copy(mc_disc, disc_list)
        disc_list.depart = hbuff.depart
        disc_list.rec_id = mc_disc._recid
        disc_list.counter = counter

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        tdept = Tdept()
        tdept_list.append(tdept)

        buffer_copy(hoteldpt, tdept)

    return generate_output()