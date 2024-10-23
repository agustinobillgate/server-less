from functions.additional_functions import *
import decimal
from functions.check_userkeybl import check_userkeybl
from models import Queasy

pci_setup_list, Pci_setup = create_model("Pci_setup", {"number1":int, "number2":int, "number3":int, "descr":str, "setupflag":bool, "price":decimal})

def common_precheckin_savesetupbl(input_username:str, input_userkey:str, pci_setup_list:[Pci_setup]):
    output_ok_flag = False
    queasy = None

    pci_setup = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_ok_flag, queasy
        nonlocal input_username, input_userkey


        nonlocal pci_setup
        nonlocal pci_setup_list
        return {"output_ok_flag": output_ok_flag}

    output_ok_flag = get_output(check_userkeybl(input_username, input_userkey))

    if not output_ok_flag:

        return generate_output()


    for pci_setup in query(pci_setup_list, sort_by=[("number1",False)]):

        queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 216) & (Queasy.number1 == pci_setup.number1) & (Queasy.number2 == pci_setup.number2)).first()

        if pci_setup.number1 == 1:

            if pci_setup.number2 == 99:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.descr


            else:
                queasy.logi1 = pci_setup.setupflag


        elif pci_setup.number1 == 2:
            queasy.logi1 = pci_setup.setupflag
            queasy.deci1 =  to_decimal(pci_setup.price)


        elif pci_setup.number1 == 3:
            queasy.logi1 = pci_setup.setupflag


        elif pci_setup.number1 == 4:

            if pci_setup.number2 == 99:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.descr


            else:
                queasy.logi1 = pci_setup.setupflag


        elif pci_setup.number1 == 5:

            if pci_setup.number2 == 99:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.descr


            else:
                queasy.logi1 = pci_setup.setupflag


        elif pci_setup.number1 == 6:
            queasy.logi1 = pci_setup.setupflag
            queasy.char3 = pci_setup.descr


        elif pci_setup.number1 == 7:
            queasy.logi1 = pci_setup.setupflag
            queasy.char3 = pci_setup.descr


    return generate_output()