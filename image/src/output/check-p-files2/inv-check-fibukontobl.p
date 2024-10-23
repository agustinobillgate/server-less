
DEFINE TEMP-TABLE c-list 
  /*FIELD artnr       AS CHAR FORMAT "x(11)" COLUMN-LABEL "Artno"*/
  FIELD artnr LIKE l-artikel.artnr
  FIELD bezeich     AS CHAR FORMAT "x(36)" COLUMN-LABEL "Description" 
  FIELD munit       AS CHAR FORMAT "x(5)" COLUMN-LABEL "Unit" 
  FIELD inhalt      AS CHAR FORMAT "x(8)" COLUMN-LABEL "Content" 
  FIELD zwkum       AS CHAR FORMAT "x(8)"
  FIELD endkum      AS INTEGER
  FIELD qty         AS DECIMAL FORMAT "->>>,>>9.999" LABEL "   Curr-Qty" 
  FIELD qty1        AS DECIMAL FORMAT "->>>,>>9.999" LABEL " Actual-Qty" 
  FIELD fibukonto   LIKE gl-acct.fibukonto INITIAL "0000000000" 
/* DO NOT change the INITIAL value 0000000000, used BY hcost-anal.p */ 
  FIELD avrg-price  AS DECIMAL FORMAT "->>>,>>>,>>9.99" LABEL "  Average Price" /*FD Jan 27, 20222*/
  FIELD cost-center AS CHAR FORMAT "x(50)" LABEL "Cost Allocation".

DEFINE INPUT PARAMETER TABLE FOR c-list.
DEFINE OUTPUT PARAMETER found-it AS LOGICAL NO-UNDO.

DEFINE VARIABLE p-272 AS CHAR NO-UNDO.
DEFINE VARIABLE p-275 AS CHAR NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 272 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN p-272 = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 275 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN p-275 = htparam.fchar.


FOR EACH c-list WHERE c-list.fibukonto NE "0000000000"  NO-LOCK:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = c-list.fibukonto
        AND gl-acct.acc-type = 2 NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acct THEN DO:
        IF gl-acct.fibukonto NE p-272 AND gl-acct.fibukonto NE p-275 THEN DO:
            ASSIGN found-it = YES.
            LEAVE.
        END.
    END.
END.
