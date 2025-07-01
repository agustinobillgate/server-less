
DEF TEMP-TABLE t-queasy 
    FIELD char3   LIKE queasy.char3
    FIELD char1   LIKE queasy.char1
    FIELD number3 LIKE queasy.number3
    FIELD deci3   LIKE queasy.deci3.

DEF TEMP-TABLE dept-list  
    FIELD deptNo AS INTEGER  
    . 

DEF INPUT  PARAMETER mc-str     AS CHAR.
DEF INPUT  PARAMETER curr-dept  AS INTEGER.
DEF OUTPUT PARAMETER do-it      AS LOGICAL.
DEF OUTPUT PARAMETER msg-str    AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE VARIABLE excl-str AS CHAR NO-UNDO.
DEFINE VARIABLE count-i AS INTEGER NO-UNDO.
DEFINE VARIABLE dept AS INTEGER NO-UNDO.

FOR EACH dept-list:  
    DELETE dept-list.  
END.

FIND FIRST vhp.queasy WHERE vhp.queasy.key = 105
    AND vhp.queasy.number2 = 0 AND vhp.queasy.deci2 = 0
    AND vhp.queasy.char2 = mc-str AND vhp.queasy.logi2 = NO
    NO-LOCK NO-ERROR.
do-it = AVAILABLE vhp.queasy.
IF AVAILABLE queasy THEN
DO:
    CREATE t-queasy.
    ASSIGN
        t-queasy.char3   = queasy.char3
        t-queasy.char1   = queasy.char1
        t-queasy.number3 = queasy.number3
        t-queasy.deci3   = queasy.deci3.
END.

/*FDL Jan 31, 2024 => Ticket 6D3207*/
FIND FIRST t-queasy NO-LOCK NO-ERROR.  
IF AVAILABLE t-queasy THEN
DO:
    ASSIGN  
        excl-str = ""  
        excl-str = ENTRY(2, t-queasy.char3, "&"). 

    IF excl-str NE "" THEN
    DO:
        DO count-i = 1 TO NUM-ENTRIES(excl-str, ","):  
            ASSIGN  
                dept = -1  
                dept = INTEGER(ENTRY(count-i, excl-str, ",")) NO-ERROR  
            .  
            IF dept GT 0 THEN  
            DO:  
                CREATE dept-list.  
                ASSIGN dept-list.deptNo = dept.  
            END.  
        END.
        FIND FIRST dept-list WHERE dept-list.deptNo = curr-dept NO-LOCK NO-ERROR.  
        IF AVAILABLE dept-list THEN  
        DO:  
            msg-str = "Card not applicable for this outlet.".   
            RETURN.   
        END.
        /*FOR EACH dept-list WHERE dept-list.deptNo EQ curr-dept NO-LOCK:
        END.*/
    END.
END.
ELSE
DO:
    msg-str = "No such Card Number found.".
    RETURN.
END.
