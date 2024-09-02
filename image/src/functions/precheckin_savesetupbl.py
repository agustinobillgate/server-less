from functions.additional_functions import *
import decimal
from models import Queasy

def precheckin_savesetupbl(pci_setup:[Pci_setup]):
    mess_str = ""
    queasy = None

    pci_setup = bqueasy = None

    pci_setup_list, Pci_setup = create_model("Pci_setup", {"number1":int, "number2":int, "descr":str, "setupvalue":str, "setupflag":bool, "price":decimal, "remarks":str})

    Bqueasy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, queasy
        nonlocal bqueasy


        nonlocal pci_setup, bqueasy
        nonlocal pci_setup_list
        return {"mess_str": mess_str}

    for pci_setup in query(pci_setup_list):

        queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 216) &  (Queasy.number1 == pci_setup.number1) &  (Queasy.number2 == pci_setup.number2)).first()

        if pci_setup.number1 == 1:
            queasy.logi1 = pci_setup.setupflag
            queasy.char3 = pci_setup.setupvalue


        elif pci_setup.number1 == 2:
            queasy.logi1 = pci_setup.setupflag
            queasy.deci1 = pci_setup.price


        elif pci_setup.number1 == 3:
            queasy.logi1 = pci_setup.setupflag


        elif pci_setup.number1 == 4:

            if pci_setup.number2 == 99:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.setupvalue

                bqueasy = db_session.query(Bqueasy).filter(
                            (Bqueasy.key == 216) &  (Bqueasy.number1 == 4) &  (Bqueasy.number2 == 1)).first()
                bqueasy.logi1 = False


            else:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.setupvalue

                bqueasy = db_session.query(Bqueasy).filter(
                            (Bqueasy.key == 216) &  (Bqueasy.number1 == 4) &  (Bqueasy.number2 == 99)).first()
                bqueasy.logi1 = False


        elif pci_setup.number1 == 5:

            if pci_setup.number2 == 99:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.setupvalue

                bqueasy = db_session.query(Bqueasy).filter(
                            (Bqueasy.key == 216) &  (Bqueasy.number1 == 5) &  (Bqueasy.number2 == 1)).first()
                bqueasy.logi1 = False


            else:
                queasy.logi1 = pci_setup.setupflag
                queasy.char3 = pci_setup.setupvalue

                bqueasy = db_session.query(Bqueasy).filter(
                            (Bqueasy.key == 216) &  (Bqueasy.number1 == 5) &  (Bqueasy.number2 == 99)).first()
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