from functions.additional_functions import *
import decimal
from models import Queasy, Eg_subtask

def prepare_sel_egmainbl(categ_nr:int, dept_nr:int):
    main_task_list = []
    queasy = eg_subtask = None

    main_task = queasy1 = subtask = None

    main_task_list, Main_task = create_model("Main_task", {"nr":int, "bezeich":str})

    Queasy1 = Queasy
    Subtask = Eg_subtask

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_task_list, queasy, eg_subtask
        nonlocal queasy1, subtask


        nonlocal main_task, queasy1, subtask
        nonlocal main_task_list
        return {"main-task": main_task_list}

    def create_main():

        nonlocal main_task_list, queasy, eg_subtask
        nonlocal queasy1, subtask


        nonlocal main_task, queasy1, subtask
        nonlocal main_task_list


        Queasy1 = Queasy
        Subtask = Eg_subtask

        for queasy1 in db_session.query(Queasy1).filter(
                (Queasy1.key == 133) &  (Queasy1.number2 == categ_nr)).all():
            main_task = Main_task()
            main_task_list.append(main_task)

            main_task.nr = queasy1.number1
            main_task.bezeich = queasy1.CHAR1


    create_main()

    return generate_output()