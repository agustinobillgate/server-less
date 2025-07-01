
DEF INPUT PARAMETER category-number1 AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER er-code AS INT INIT 0.

DEF BUFFER egReq FOR eg-Request.
DEF BUFFER queasyBuff FOR queasy.

FIND FIRST queasybuff WHERE queasybuff.KEY = 133 AND queasybuff.number2 = category-number1 NO-LOCK NO-ERROR.
IF AVAILABLE queasybuff THEN
DO:
    er-code = 1.
    /*MTHIDE MESSAGE NO-PAUSE.  
    MESSAGE translateExtended ("Object exists for this Category.",lvCAREA,"")   
        SKIP
        translateExtended ("Deleting not posibble",lvCAREA,"")   
    VIEW-AS ALERT-BOX INFORMATION.*/
    RETURN NO-APPLY.
END.
FIND FIRST queasy WHERE RECID(queasy) = rec-id.
FIND CURRENT queasy EXCLUSIVE-LOCK.
DELETE queasy.

/*MTOPEN QUERY q1 FOR EACH queasy WHERE queasy.KEY = 132 NO-LOCK 
    BY queasy.number1.

answer = NO.  

curr-select = "".
RUN init-category.
APPLY "entry" TO b1.
RUN mk-readonly(YES).
DISABLE btn-exit with frame frame1.  
ENABLE btn-addart btn-renart btn-delart with frame frame1.
*/
