DEF TEMP-TABLE s-list 
    FIELD fibukonto LIKE gl-acct.fibukonto INITIAL "000000000000" 
    FIELD debit     LIKE gl-journal.debit 
    FIELD credit    LIKE gl-journal.credit
    FIELD flag      AS LOGICAL INIT NO
    /*FD 27-11-19 -> Request by Dwi Setiyawan 9BAD9C*/
    FIELD bezeich   LIKE gl-acct.bezeich 
    /*End FD*/
    FIELD remark    AS CHARACTER FORMAT "x(115)". /*FD Sept 29, 2022 => Ticket No 506FA2 - Input remark per COA*/

DEF TEMP-TABLE xls-list 
    FIELD fibukonto AS CHAR INITIAL "000000000000" 
    FIELD debit     LIKE gl-journal.debit 
    FIELD credit    LIKE gl-journal.credit
    FIELD flag      AS LOGICAL INIT NO
    FIELD bezeich   LIKE gl-acct.bezeich 
    FIELD remark    AS CHARACTER FORMAT "x(115)".

DEFINE INPUT PARAMETER TABLE FOR xls-list.
DEFINE OUTPUT PARAMETER gl-notavail AS LOGICAL.
DEFINE OUTPUT PARAMETER gl-fibu AS CHARACTER.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR s-list.

FOR EACH xls-list:
    IF xls-list.fibukonto NE "000000000000" THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto EQ xls-list.fibukonto NO-LOCK NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN
        DO:
            gl-notavail = YES.
            gl-fibu = xls-list.fibukonto.
            RETURN.
        END.
            
        xls-list.bezeich = gl-acct.bezeich.
    END.    
END.

FOR EACH s-list:
    DELETE s-list.
END.

FOR EACH xls-list:
    CREATE s-list.
    BUFFER-COPY xls-list TO s-list.
END.

