#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.check_userkeybl import check_userkeybl
from models import Queasy

def common_precheckin_loadsetupbl(input_username:string, input_userkey:string, icase:int):

    prepare_cache ([Queasy])

    output_ok_flag = False
    pci_setup_data = []
    queasy = None

    pci_setup = None

    pci_setup_data, Pci_setup = create_model("Pci_setup", {"number1":int, "number2":int, "descr":string, "setupflag":bool, "price":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_ok_flag, pci_setup_data, queasy
        nonlocal input_username, input_userkey, icase


        nonlocal pci_setup
        nonlocal pci_setup_data

        return {"output_ok_flag": output_ok_flag, "pci-setup": pci_setup_data}

    output_ok_flag = get_output(check_userkeybl(input_username, input_userkey))

    if not output_ok_flag:

        return generate_output()


    if icase == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 216)).order_by(Queasy._recid).all():
            pci_setup = Pci_setup()
            pci_setup_data.append(pci_setup)

            pci_setup.number1 = queasy.number1
            pci_setup.number2 = queasy.number2
            pci_setup.descr = queasy.char3
            pci_setup.setupflag = queasy.logi1
            pci_setup.price =  to_decimal(queasy.deci1)

    elif icase == 2:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 216) & (Queasy.logi1)).order_by(Queasy._recid).all():
            pci_setup = Pci_setup()
            pci_setup_data.append(pci_setup)

            pci_setup.number1 = queasy.number1
            pci_setup.number2 = queasy.number2
            pci_setup.descr = queasy.char3
            pci_setup.setupflag = queasy.logi1
            pci_setup.price =  to_decimal(queasy.deci1)

    return generate_output()