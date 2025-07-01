#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_property, Eg_propmeter

input_list_list, Input_list = create_model("Input_list", {"last_propnr":int, "location":int, "task":int, "zinr":string})

def eg_propertymeter_btn_go_webbl(input_list_list:[Input_list]):

    prepare_cache ([Eg_propmeter])

    rec_meter_list = []
    t_eg_property_list = []
    output_list_list = []
    counter:int = 0
    eg_property = eg_propmeter = None

    t_eg_property = rec_meter = input_list = output_list = None

    t_eg_property_list, T_eg_property = create_model_like(Eg_property)
    rec_meter_list, Rec_meter = create_model("Rec_meter", {"prop_nr":int, "rec_date":date, "rec_time":int, "rec_by":string, "rec_hour":int, "rec_meter":int})
    output_list_list, Output_list = create_model("Output_list", {"last_propnr":int, "all_data":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_meter_list, t_eg_property_list, output_list_list, counter, eg_property, eg_propmeter


        nonlocal t_eg_property, rec_meter, input_list, output_list
        nonlocal t_eg_property_list, rec_meter_list, output_list_list

        return {"rec-meter": rec_meter_list, "t-eg-property": t_eg_property_list, "output-list": output_list_list}

    def create_rec_meter(propnr:int):

        nonlocal rec_meter_list, t_eg_property_list, output_list_list, counter, eg_property, eg_propmeter


        nonlocal t_eg_property, rec_meter, input_list, output_list
        nonlocal t_eg_property_list, rec_meter_list, output_list_list

        for eg_propmeter in db_session.query(Eg_propmeter).filter(
                 (eg_propmeter.propertynr == propnr)).order_by(Eg_propmeter._recid).all():
            rec_meter = Rec_meter()
            rec_meter_list.append(rec_meter)

            rec_meter.prop_nr = eg_propmeter.propertynr
            rec_meter.rec_date = eg_propmeter.rec_date
            rec_meter.rec_time = eg_propmeter.rec_time
            rec_meter.rec_by = eg_propmeter.rec_by
            rec_meter.rec_hour = eg_propmeter.val_hour
            rec_meter.rec_meter = eg_propmeter.val_meter


    counter = 0

    input_list = query(input_list_list, first=True)

    if not input_list:

        return generate_output()
    else:
        output_list = Output_list()
        output_list_list.append(output_list)


    if input_list.location != 0 and trim(input_list.zinr) == "" and input_list.task != 0:

        for eg_property in db_session.query(Eg_property).filter(
                 (Eg_property.nr > input_list.last_propnr) & (Eg_property.location == input_list.location) & (Eg_property.maintask == input_list.task)).order_by(Eg_property.nr).yield_per(100):
            counter = counter + 1
            t_eg_property = T_eg_property()
            t_eg_property_list.append(t_eg_property)

            buffer_copy(eg_property, t_eg_property)
            create_rec_meter(eg_property.nr)

            if counter == 300:
                output_list.last_propnr = eg_property.nr
                break

    elif input_list.location != 0 and trim(input_list.zinr) == "" and input_list.task == 0:

        for eg_property in db_session.query(Eg_property).filter(
                 (Eg_property.nr > input_list.last_propnr) & (Eg_property.location == input_list.location)).order_by(Eg_property.nr).yield_per(100):
            counter = counter + 1
            t_eg_property = T_eg_property()
            t_eg_property_list.append(t_eg_property)

            buffer_copy(eg_property, t_eg_property)
            create_rec_meter(eg_property.nr)

            if counter == 300:
                output_list.last_propnr = eg_property.nr
                break

    elif input_list.location == 0 and trim(input_list.zinr) != "" and input_list.task != 0:

        for eg_property in db_session.query(Eg_property).filter(
                 (Eg_property.nr > input_list.last_propnr) & (Eg_property.zinr == input_list.zinr) & (Eg_property.maintask == input_list.task)).order_by(Eg_property.nr).yield_per(100):
            counter = counter + 1
            t_eg_property = T_eg_property()
            t_eg_property_list.append(t_eg_property)

            buffer_copy(eg_property, t_eg_property)
            create_rec_meter(eg_property.nr)

            if counter == 300:
                output_list.last_propnr = eg_property.nr
                break

    elif input_list.location == 0 and trim(input_list.zinr) != "" and input_list.task == 0:

        for eg_property in db_session.query(Eg_property).filter(
                 (Eg_property.nr > input_list.last_propnr) & (Eg_property.zinr == input_list.zinr)).order_by(Eg_property.nr).yield_per(100):
            counter = counter + 1
            t_eg_property = T_eg_property()
            t_eg_property_list.append(t_eg_property)

            buffer_copy(eg_property, t_eg_property)
            create_rec_meter(eg_property.nr)

            if counter == 300:
                output_list.last_propnr = eg_property.nr
                break

    elif input_list.location == 0 and trim(input_list.zinr) == "" and input_list.task != 0:

        for eg_property in db_session.query(Eg_property).filter(
                 (Eg_property.nr > input_list.last_propnr) & (Eg_property.location != 999) & (Eg_property.maintask == input_list.task)).order_by(Eg_property.nr).all():
            counter = counter + 1
            t_eg_property = T_eg_property()
            t_eg_property_list.append(t_eg_property)

            buffer_copy(eg_property, t_eg_property)
            create_rec_meter(eg_property.nr)

            if counter == 300:
                output_list.last_propnr = eg_property.nr
                break
    else:

        for eg_property in db_session.query(Eg_property).filter(
                 (Eg_property.nr > input_list.last_propnr) & (Eg_property.location != 999)).order_by(Eg_property.nr).all():
            counter = counter + 1
            t_eg_property = T_eg_property()
            t_eg_property_list.append(t_eg_property)

            buffer_copy(eg_property, t_eg_property)
            create_rec_meter(eg_property.nr)

            if counter == 300:
                output_list.last_propnr = eg_property.nr
                break

    if counter < 300:
        output_list.all_data = True

    return generate_output()