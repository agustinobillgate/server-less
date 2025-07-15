from functions.additional_functions import *
import decimal

def create_load_d_filebl_dotp():
    df_directory:str = "c:\\vhp10\\vhp.df"
    str1:str = ""

    t_list = tbuff = None

    t_list_list, T_list = create_model("T_list", {"table_name":str, "dfile_name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal df_directory, str1


        nonlocal t_list, tbuff
        nonlocal t_list_list

        return {}

    def create_a2z_procedure():

        nonlocal df_directory, str1


        nonlocal t_list, tbuff
        nonlocal t_list_list

        curr_i:int = 0
        curr_char:str = ""
        curr_counter:int = 0
        str1 = "DEFINE INPUT PARAMETER inp-table AS CHAR NO-UNDO."
        put_stream(str1)
        str1 = "DEFINE INPUT PARAMETER inp-dfile AS CHAR NO-UNDO."
        put_stream(str1)
        str1 = "DEFINE OUTPUT PARAMETER error-flag AS INTEGER INIT -1 NO-UNDO."
        put_stream(str1)
        str1 = " "
        put_stream(str1)
        str1 = "RUN a2z-procedure."
        put_stream(str1)
        str1 = " ASSIGN error-flag = 0."
        put_stream(str1)
        str1 = " "
        put_stream(str1)
        str1 = "PROCEDURE a2z-procedure:"
        put_stream(str1)
        for curr_counter in range(97,122 + 1) :
            curr_char = chr(curr_counter)
            curr_i = curr_i + 1

            if curr_i == 1:
                str1 = " IF SUBSTR(inp-table,1,1) = " + '"' + curr_char + '"' + " THEN RUN load-" + curr_char + "-table."
            else:
                str1 = " ELSE IF SUBSTR(inp-table,1,1) = " + '"' + curr_char + '"' + " THEN RUN load-" + curr_char + "-table."
            put_stream(str1)
        str1 = "END."
        put_stream(str1)
        str1 = " "
        put_stream(str1)


    def create_load_a2z_procedure():

        nonlocal df_directory, str1


        nonlocal t_list, tbuff
        nonlocal t_list_list

        curr_char:str = ""
        curr_i:int = 0
        Tbuff = T_list
        tbuff_list = t_list_list

        for t_list in query(t_list_list, sort_by=[("table_name",False)]):

            if curr_char != substring(t_list.table_name, 0, 1):
                curr_char = substring(t_list.table_name, 0, 1)
                str1 = "PROCEDURE load-" + curr_char + "-table:"
                put_stream(str1)
                curr_i = 1

                for tbuff in query(tbuff_list, filters=(lambda tbuff: tbuff.substring(tbuff.table_name, 0, 1) == (curr_char).lower()), sort_by=[("table_name",False)]):

                    if curr_i == 1:
                        str1 = " IF inp-table = " + '"' + tbuff.table_name + '"' + " THEN RUN load-" + tbuff.table_name + "."
                    else:
                        str1 = " ELSE IF inp-table = " + '"' + tbuff.table_name + '"' + " THEN RUN load-" + tbuff.table_name + "."
                    put_stream(str1)
                    curr_i = curr_i + 1
                str1 = "END."
                put_stream(str1)
                str1 = " "
                put_stream(str1)


    def create_load_procedure():

        nonlocal df_directory, str1


        nonlocal t_list, tbuff
        nonlocal t_list_list

        for t_list in query(t_list_list, sort_by=[("table_name",False)]):
            str1 = "PROCEDURE load-" + t_list.table_name + ":"
            put_stream(str1)
            str1 = "DEFINE VARIABLE str1 AS CHAR NO-UNDO."
            put_stream(str1)
            str1 = "DEFINE VARIABLE curr-dfile AS CHAR NO-UNDO."
            put_stream(str1)
            str1 = " INPUT FROM VALUE(inp-dfile)."
            put_stream(str1)
            str1 = " REPEAT:"
            put_stream(str1)
            str1 = " DO TRANSACTION:"
            put_stream(str1)
            str1 = " CREATE " + t_list.table_name + "."
            put_stream(str1)
            str1 = " IMPORT " + t_list.table_name + "."
            put_stream(str1)
            str1 = " END."
            put_stream(str1)
            str1 = " END."
            put_stream(str1)
            str1 = " INPUT CLOSE."
            put_stream(str1)
            str1 = "END."
            put_stream(str1)
            str1 = " "
            put_stream(str1)


    def put_stream(ostr:str):

        nonlocal df_directory, str1


        nonlocal t_list, tbuff
        nonlocal t_list_list

    INPUT STREAM s1 FROM VALUE (df_directory)
    while True:
        IMPORT STREAM s1 UNFORMATTED str1
        str1 = trim(str1)

        if substring(str1, 0, 9) == ("ADD TABLE").lower() :
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.table_name = entry(1, str1, '"')

        elif substring(str1, 0, 9) == ("DUMP-NAME").lower() :
            t_list.dfile_name = entry(1, str1, '"') + ".d"
    INPUT STREAM s1 CLOSE
    OUTPUT STREAM s1 TO "c:\\vhp\\commonbl\\load-d-fileBL.p"
    create_a2z_procedure()
    create_load_a2z_procedure()
    create_load_procedure()
    OUTPUT STREAM s1 CLOSE

    return generate_output()