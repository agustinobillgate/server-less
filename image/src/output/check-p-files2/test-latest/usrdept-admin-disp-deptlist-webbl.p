/*FD Nov 16, 2020 => BL for vhp web based move from UI progress*/

DEFINE TEMP-TABLE t-queasy      LIKE queasy
    FIELD comp-name AS CHAR.

DEFINE TEMP-TABLE dept-list 
    FIELD nr        AS INTEGER 
    FIELD dept      AS CHAR    
    FIELD SELECTED  AS LOGICAL 
.

DEFINE INPUT PARAMETER TABLE FOR t-queasy.
DEFINE OUTPUT PARAMETER TABLE FOR dept-list.

RUN create-dptlist.  

PROCEDURE create-dptlist:
DEF VAR i AS INTEGER NO-UNDO.

    FOR EACH t-queasy:        
        CREATE dept-list.
        ASSIGN
            dept-list.nr        = t-queasy.number1
            dept-list.dept      = t-queasy.char3
            dept-list.SELECTED  = NO.        
    END.

    FOR EACH t-queasy WHERE t-queasy.char2 NE "" NO-LOCK:
        DO i = 1 TO NUM-ENTRIES(t-queasy.char2, ";"):
            
            FIND FIRST dept-list WHERE dept-list.nr = 
                INTEGER(ENTRY(i, t-queasy.char2, ";")) NO-LOCK NO-ERROR.
            IF AVAILABLE dept-list THEN
                ASSIGN dept-list.SELECTED = YES.              
        END.
    END.

END.

