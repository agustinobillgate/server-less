DEFINE TEMP-TABLE t-param
    FIELD grup      AS INTEGER   FORMAT ">>9"
    FIELD number    AS INTEGER   FORMAT ">>9"   LABEL "No"
    FIELD bezeich   AS CHARACTER FORMAT "x(50)" LABEL "Description"
    FIELD typ       AS INTEGER 
    FIELD logv      AS LOGICAL 
    FIELD val       AS CHARACTER FORMAT "x(30)" LABEL "Value".

DEF INPUT PARAMETER deptno  AS INT.
DEF INPUT PARAMETER grup    AS INT.
DEF INPUT PARAMETER paramnr AS INT.
DEF INPUT PARAMETER intval  AS INT.
DEF INPUT PARAMETER decval  AS DECIMAL.
DEF INPUT PARAMETER dateval AS DATE.
DEF INPUT PARAMETER logval  AS LOGICAL.
DEF INPUT PARAMETER charval AS CHAR.

DEF OUTPUT PARAMETER htp-val AS CHAR.
DEF OUTPUT PARAMETER htp-logv AS LOGICAL.
/*DEF OUTPUT PARAMETER TABLE FOR t-param.*/

RUN update-queasy.
/*RUN update-tparam.*/

PROCEDURE update-queasy:
    FIND FIRST queasy WHERE queasy.KEY EQ 222 AND queasy.betriebsnr EQ deptno 
        AND queasy.number1 EQ grup 
        AND queasy.number2 EQ paramnr EXCLUSIVE-LOCK.
    IF queasy.number3 EQ 1 THEN 
    DO:
        queasy.char2 = STRING(intval).
        htp-val      = STRING(queasy.char2).
    END.
    ELSE IF queasy.number3 EQ 2 THEN
    DO: 
        queasy.deci1 = decval.
        htp-val      = STRING(queasy.deci1).
    END.
    ELSE IF queasy.number3 EQ 3 THEN 
    DO: 
        queasy.date1 = dateval.
        htp-val      = STRING(queasy.date1).
    END.
    ELSE IF queasy.number3 EQ 4 THEN 
    DO:    
        queasy.logi1 = logval.
        htp-logv     = queasy.logi1.
    END.
    ELSE IF queasy.number3 EQ 5 THEN
    DO: 
        queasy.char2 = STRING(charval).
        htp-val      = STRING(queasy.char2).
    END.
END.
/*
PROCEDURE update-tparam:
    FOR EACH t-param:
        DELETE t-param.
    END.

    FOR EACH queasy WHERE queasy.KEY EQ 222 AND queasy.number1 EQ 1 NO-LOCK:
        CREATE t-param.
        ASSIGN
            t-param.grup    = queasy.number1
            t-param.number  = queasy.number2
            t-param.bezeich = queasy.char1
            t-param.typ     = queasy.number3.
        IF queasy.number3 EQ 1 THEN t-param.val = STRING(queasy.char2).
        ELSE IF queasy.number3 EQ 2 THEN t-param.val = STRING(queasy.deci1).
        ELSE IF queasy.number3 EQ 3 THEN t-param.val = STRING(queasy.date1).
        ELSE IF queasy.number3 EQ 4 THEN
        DO:
            t-param.val  = STRING(queasy.logi1).
            t-param.logv = queasy.logi1.
        END.
        ELSE IF queasy.number3 EQ 5 THEN t-param.val = STRING(queasy.char2).
    END.
END.*/
