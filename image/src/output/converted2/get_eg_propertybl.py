#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property, Queasy

def get_eg_propertybl(loc_nr:int, zinr:string, maintask:int, category:int):
    t_eg_property_list = []
    eg_property = queasy = None

    t_eg_property = qbuff = None

    t_eg_property_list, T_eg_property = create_model_like(Eg_property)

    Qbuff = create_buffer("Qbuff",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_property_list, eg_property, queasy
        nonlocal loc_nr, zinr, maintask, category
        nonlocal qbuff


        nonlocal t_eg_property, qbuff
        nonlocal t_eg_property_list

        return {"t-eg-property": t_eg_property_list}

    eg_property_obj_list = {}
    for eg_property, queasy, qbuff in db_session.query(Eg_property, Queasy, Qbuff).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).join(Qbuff,(Qbuff.key == 132) & (Qbuff.number1 == Queasy.number2) & (Qbuff.number1 == category)).filter(
             (Eg_property.location == loc_nr) & (Eg_property.zinr == (zinr).lower())).order_by(Eg_property._recid).all():
        if eg_property_obj_list.get(eg_property._recid):
            continue
        else:
            eg_property_obj_list[eg_property._recid] = True


        t_eg_property = T_eg_property()
        t_eg_property_list.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    return generate_output()