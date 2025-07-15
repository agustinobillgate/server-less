#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

pci_setup_data, Pci_setup = create_model("Pci_setup", {"number1":int, "number2":int, "descr":string, "setupvalue":string, "setupflag":bool, "price":Decimal, "remarks":string})

def precheckin_savesetupbl(pci_setup_data:[Pci_setup]):

    prepare_cache ([Queasy])

    mess_str = ""
    queasy = None

    pci_setup = bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, queasy
        nonlocal bqueasy


        nonlocal pci_setup, bqueasy

        return {"mess_str": mess_str}

    for pci_setup in query(pci_setup_data, sort_by=[("number1",False)]):

        queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, pci_setup.number1)],"number2": [(eq, pci_setup.number2)]})

        if pci_setup.number1 == 1:
            queasy.logi1 = pci_setup.setupflag
            queasy.char3 = pci_setup.setupvalue


        elif pci_setup.number1 == 2:
            queasy.logi1 = pci_setup.setupflag
            queasy.deci1 =  to_decimal(pci_setup.price)


        elif pci_setup.number1 == 3:
            queasy.logi1 = pci_setup.setupflag


        elif pci_setup.number1 == 4:

            if pci_setup.number2 == 99:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.setupvalue

                bqueasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 4)],"number2": [(eq, 1)]})
                bqueasy.logi1 = False


            else:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.setupvalue

                bqueasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 4)],"number2": [(eq, 99)]})
                bqueasy.logi1 = False


        elif pci_setup.number1 == 5:

            if pci_setup.number2 == 99:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.setupvalue

                bqueasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 5)],"number2": [(eq, 1)]})
                bqueasy.logi1 = False


            else:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.setupvalue

                bqueasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 5)],"number2": [(eq, 99)]})
                bqueasy.logi1 = False


        elif pci_setup.number1 == 6:
            queasy.logi1 = pci_setup.setupflag
            queasy.char3 = pci_setup.setupvalue


        elif pci_setup.number1 == 7:
            queasy.logi1 = pci_setup.setupflag
            queasy.char3 = pci_setup.setupvalue


        elif pci_setup.number1 == 8:
            queasy.logi1 = pci_setup.setupflag


    mess_str = "Setup Updated Successfully"

    return generate_output()