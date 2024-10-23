DEF TEMP-TABLE t-buff
    FIELD key        AS INTEGER  
    FIELD number1    AS INTEGER  
    FIELD number2    AS INTEGER  
    FIELD number3    AS INTEGER  
    FIELD date1      AS DATE     
    FIELD date2      AS DATE     
    FIELD date3      AS DATE     
    FIELD char1      AS CHAR     
    FIELD char2      AS CHAR     
    FIELD char3      AS CHAR     
    FIELD deci1      AS DECIMAL  
    FIELD deci2      AS DECIMAL  
    FIELD deci3      AS DECIMAL  
    FIELD logi1      AS LOGICAL  
    FIELD logi2      AS LOGICAL  
    FIELD logi3      AS LOGICAL  
    FIELD betriebsnr AS INTEGER  
    FIELD gname      AS CHAR.

DEF TEMP-TABLE t-res-line LIKE res-line.

DEFINE INPUT-OUTPUT PARAMETER TABLE FOR t-buff.

FOR EACH t-buff BY t-buff.char1 BY t-buff.date1:
    RUN read-res-linebl.p(20, ?,?, 6, 1, t-buff.char1, ?,?,?,?,"",
                          OUTPUT TABLE t-res-line).
    FIND FIRST t-res-line NO-ERROR. 
    IF NOT AVAILABLE t-res-line THEN 
    DO:
        RUN read-res-linebl.p(20, ?,?, 13, 1, t-buff.char1, ?,?,?,?,"",
                             OUTPUT TABLE t-res-line).
    END.
    FIND FIRST t-res-line WHERE t-res-line.zinr = t-buff.char1 NO-LOCK NO-ERROR.
    IF AVAILABLE t-res-line THEN
        ASSIGN t-buff.gname = t-res-line.NAME.
END.
