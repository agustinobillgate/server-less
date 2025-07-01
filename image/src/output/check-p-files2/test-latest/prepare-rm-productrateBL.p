

DEF TEMP-TABLE t-bediener LIKE bediener.

DEF INPUT PARAMETER LnL-prog AS CHAR.
DEF INPUT PARAMETER LnL-prog1 AS CHAR.
DEF OUTPUT PARAMETER LnL-filepath AS CHAR.
DEF OUTPUT PARAMETER LnL-filepath1 AS CHAR.
DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER p-547 AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.

FIND FIRST htparam WHERE htparam.paramnr = 417 NO-LOCK. 
IF htparam.fchar NE "" THEN 
DO: 
    LnL-filepath = htparam.fchar. 
    IF SUBSTR(LnL-filepath, LENGTH(LnL-filepath), 1) NE "\" THEN 
        LnL-filepath = LnL-filepath + "\". 
    LnL-filepath = LnL-filepath + LnL-prog. 
    LnL-filepath1 = htparam.fchar. 
    IF SUBSTR(LnL-filepath1, LENGTH(LnL-filepath1), 1) NE "\" THEN 
        LnL-filepath1 = LnL-filepath1 + "\". 
    LnL-filepath1 = LnL-filepath1 + LnL-prog1. 
END.

FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 

RUN fill-salesID.


PROCEDURE fill-salesID:
    FIND FIRST htparam WHERE htparam.paramnr = 547 NO-LOCK.
    IF htparam.paramnr = 0 THEN RETURN.
    p-547 = htparam.paramnr.
    /*MTsales-ID:ADD-LAST("") IN FRAME frame1.*/
    FOR EACH bediener WHERE bediener.flag EQ 0 AND user-group = htparam.finteger /* bernatd 5FA946 2024 */
        NO-LOCK BY bediener.username:
       
             CREATE t-bediener.
             BUFFER-COPY bediener TO t-bediener.
        /*MTsales-ID:ADD-LAST(bediener.userinit + " - " + bediener.username) 
            IN FRAME frame1. */

    END.
END.





