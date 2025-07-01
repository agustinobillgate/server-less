DEFINE INPUT PARAMETER task AS INT.
DEFINE INPUT PARAMETER beCode AS INT.
DEFINE INPUT PARAMETER flag AS LOGICAL.
DEFINE INPUT PARAMETER inp-str AS CHAR.

/*DEFINE VARIABLE task AS INT INIT 9.
DEFINE VARIABLE becode AS INT INIT 1.
DEFINE VARIABLE flag AS LOGICAL INIT YES.
DEFINE VARIABLE inp-str AS CHAR.
*/

DEFINE VARIABLE i       AS INT.
DEFINE VARIABLE str     AS CHAR.

FIND FIRST queasy WHERE KEY = 160 AND number1 = beCode EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    str = ENTRY(7,char1,";").
    IF NUM-ENTRIES(str,"=") GE 9 THEN
        ASSIGN
            ENTRY(task,str,"=") = STRING(flag)
            ENTRY(7,char1,";")  = str.
    FIND CURRENT queasy NO-LOCK.
END.

/* NC - 30/08/23 not used anymore since move to bookengine-config-btn-exitbl.p
FIND FIRST queasy WHERE queasy.KEY = 167 AND queasy.number1 = beCode NO-LOCK NO-ERROR. /*NC - 16/08/19*/
IF AVAILABLE queasy THEN
DO:
    FIND CURRENT queasy EXCLUSIVE-LOCK.
    queasy.logi1 = YES.
    RELEASE queasy.
END.
ELSE
DO :
    CREATE queasy.
    ASSIGN
        queasy.KEY = 167
        queasy.date1 = TODAY
		queasy.number1 = beCode /*NC - 16/08/19*/
        queasy.logi1 = YES.
END.
*/

