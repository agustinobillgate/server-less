from functions.additional_functions import *
import decimal
from functions.check_userkeybl import check_userkeybl
from models import Queasy

def common_precheckin_loadsetupbl(input_username:str, input_userkey:str, icase:int):
    output_ok_flag = False
    pci_setup_list = []
    queasy = None

    pci_setup = None

    pci_setup_list, Pci_setup = create_model("Pci_setup", {"number1":int, "number2":int, "descr":str, "setupflag":bool, "price":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_ok_flag, pci_setup_list, queasy
        nonlocal input_username, input_userkey, icase


        nonlocal pci_setup
        nonlocal pci_setup_list
        return {"output_ok_flag": output_ok_flag, "pci-setup": pci_setup_list}

    output_ok_flag = get_output(check_userkeybl(input_username, input_userkey))

    if not output_ok_flag:

        return generate_output()


    if icase == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 216)).order_by(Queasy._recid).all():
            pci_setup = Pci_setup()
            pci_setup_list.append(pci_setup)

            pci_setup.number1 = queasy.number1
            pci_setup.number2 = queasy.number2
            pci_setup.descr = queasy.char3
            pci_setup.setupflag = queasy.logi1
            pci_setup.price =  to_decimal(queasy.deci1)

    elif icase == 2:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 216) & (Queasy.logi1)).order_by(Queasy._recid).all():
            pci_setup = Pci_setup()
            pci_setup_list.append(pci_setup)

            pci_setup.number1 = queasy.number1
            pci_setup.number2 = queasy.number2
            pci_setup.descr = queasy.char3
            pci_setup.setupflag = queasy.logi1
            pci_setup.price =  to_decimal(queasy.deci1)

    return generate_output()