#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_maintain, Eg_property

def eg_maincalendar_btn_delbl(t_maintainnr:int, user_init:string):

    prepare_cache ([Eg_maintain, Eg_property])

    maintain_data = []
    eg_maintain = eg_property = None

    maintain = None

    maintain_data, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":string, "propertynr":int, "pic":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal maintain_data, eg_maintain, eg_property
        nonlocal t_maintainnr, user_init


        nonlocal maintain
        nonlocal maintain_data

        return {"maintain": maintain_data}

    def create_maintain():

        nonlocal maintain_data, eg_maintain, eg_property
        nonlocal t_maintainnr, user_init


        nonlocal maintain
        nonlocal maintain_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_maintain)
        maintain_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.delete_flag == False)).order_by(Qbuff._recid).all():

            if qbuff.propertynr != 0:

                eg_property = get_cache (Eg_property, {"nr": [(eq, qbuff.propertynr)]})

                if eg_property:
                    maintain = Maintain()
                    maintain_data.append(maintain)

                    maintain.maintainnr = qbuff.maintainnr
                    maintain.workdate = qbuff.workdate
                    maintain.estworkdate = qbuff.estworkdate
                    maintain.donedate = qbuff.donedate
                    maintain.type = qbuff.type
                    maintain.maintask = eg_property.maintask
                    maintain.location = qbuff.location
                    maintain.zinr = qbuff.zinr
                    maintain.propertynr = qbuff.propertynr
                    maintain.pic = qbuff.pic


                else:
                    pass
            else:
                maintain = Maintain()
                maintain_data.append(maintain)

                maintain.maintainnr = qbuff.maintainnr
                maintain.workdate = qbuff.workdate
                maintain.estworkdate = qbuff.estworkdate
                maintain.donedate = qbuff.donedate
                maintain.type = qbuff.type
                maintain.maintask = eg_property.maintask
                maintain.location = qbuff.location
                maintain.zinr = qbuff.zinr
                maintain.propertynr = qbuff.propertynr
                maintain.pic = qbuff.pic


    eg_maintain = get_cache (Eg_maintain, {"maintainnr": [(eq, t_maintainnr)]})

    if eg_maintain:
        eg_maintain.delete_flag = True
        eg_maintain.cancel_date = get_current_date()
        eg_maintain.cancel_time = get_current_time_in_seconds()
        eg_maintain.cancel_by = user_init


    create_maintain()

    return generate_output()