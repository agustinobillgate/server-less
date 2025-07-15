from functions.additional_functions import *
import decimal
from datetime import date
from models import Interface, Queasy

tlist_list, Tlist = create_model("Tlist", {"datum":date, "id_no":int, "rmno":str, "amount":decimal, "amount_pjk":decimal, "date_time":str, "depart":int})

def online_tax_pasuruan_updbl(tlist_list:[Tlist]):
    interface = queasy = None

    tlist = binter = None

    Binter = create_buffer("Binter",Interface)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal interface, queasy
        nonlocal binter


        nonlocal tlist, binter

        return {}

    for tlist in query(tlist_list):

        interface = db_session.query(Interface).filter(
                 (Interface.intfield == tlist.id_no) & (Interface.decfield == to_decimal(tlist.depart)) & (Interface.betriebsnr == 0)).first()

        if interface:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 234) & (Queasy.number1 == interface.intfield) & (Queasy.deci1 == interface.decfield)).first()

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 234
                queasy.number1 = interface.intfield
                queasy.deci1 =  to_decimal(interface.decfield)
                queasy.number2 = interface.resnr
                queasy.deci2 =  to_decimal(to_decimal(interface.reslinnr) )
                queasy.date1 = interface.intdate
                queasy.number3 = interface.int_time


            interface.betriebsnr = 1


            pass

    return generate_output()