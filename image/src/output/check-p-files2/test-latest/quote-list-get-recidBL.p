DEFINE TEMP-TABLE t-quote 
    FIELD artnr         LIKE l-quote.artnr          
    FIELD lief-nr       LIKE l-quote.lief-nr
    FIELD docu-nr       LIKE l-quote.docu-nr
    FIELD from-date     LIKE l-quote.from-date      
    FIELD to-date       LIKE l-quote.to-date
    .

DEFINE INPUT PARAMETER TABLE FOR t-quote.
DEFINE OUTPUT PARAMETER quote-recid AS INT.
DEFINE OUTPUT PARAMETER msg-result  AS CHARACTER.

FIND FIRST t-quote NO-LOCK.
IF NOT AVAILABLE t-quote THEN
DO:
    msg-result = "No record available".
    RETURN.
END.

FIND FIRST l-quote WHERE l-quote.artnr EQ t-quote.artnr
    AND l-quote.lief-nr EQ t-quote.lief-nr
    AND l-quote.docu-nr EQ t-quote.docu-nr
    AND l-quote.from-date EQ t-quote.from-date 
    AND l-quote.to-date EQ t-quote.to-date NO-LOCK NO-ERROR.
IF NOT AVAILABLE l-quote THEN
DO:
    msg-result = "No record available".
    RETURN.
END.

quote-recid = RECID(l-quote).
