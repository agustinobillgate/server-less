from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_maintain, Eg_property

def eg_maincalendar_btn_delbl(t_maintainnr:int, user_init:str):
    maintain_list = []
    eg_maintain = eg_property = None

    maintain = qbuff = None

    maintain_list, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":str, "propertynr":int, "pic":int})

    Qbuff = Eg_maintain

    db_session = local_storage.db_session

    def generate_output():
        nonlocal maintain_list, eg_maintain, eg_property
        nonlocal qbuff


        nonlocal maintain, qbuff
        nonlocal maintain_list
        return {"maintain": maintain_list}

    def create_maintain():

        nonlocal maintain_list, eg_maintain, eg_property
        nonlocal qbuff


        nonlocal maintain, qbuff
        nonlocal maintain_list


        Qbuff = Eg_maintain
        maintain_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.delete_flag == False)).all():

            if qbuff.propertynr != 0:

                eg_property = db_session.query(Eg_property).filter(
                        (Eg_property.nr == qbuff.propertynr)).first()

                if eg_property:
                    maintain = Maintain()
                    maintain_list.append(maintain)

                    maintain.maintainnr = qbuff.maintainnr
                    maintain.workdate = qbuff.workdate
                    maintain.estworkdate = qbuff.estworkdate
                    maintain.donedate = qbuff.donedate
                    maintain.TYPE = qbuff.TYPE
                    maintain.maintask = eg_property.maintask
                    maintain.location = qbuff.location
                    maintain.zinr = qbuff.zinr
                    maintain.propertynr = qbuff.propertynr
                    maintain.pic = qbuff.pic


                else:
                    pass
            else:
                maintain = Maintain()
                maintain_list.append(maintain)

                maintain.maintainnr = qbuff.maintainnr
                maintain.workdate = qbuff.workdate
                maintain.estworkdate = qbuff.estworkdate
                maintain.donedate = qbuff.donedate
                maintain.TYPE = qbuff.TYPE
                maintain.maintask = eg_property.maintask
                maintain.location = qbuff.location
                maintain.zinr = qbuff.zinr
                maintain.propertynr = qbuff.propertynr
                maintain.pic = qbuff.pic

    eg_maintain = db_session.query(Eg_maintain).filter(
            (Eg_maintain.maintainnr == t_maintainnr)).first()

    if eg_maintain:
        eg_maintain.delete_flag = True
        eg_maintain.cancel_date = get_current_date()
        eg_maintain.cancel_time = get_current_time_in_seconds()
        eg_maintain.cancel_by = user_init


    create_maintain()

    return generate_output()