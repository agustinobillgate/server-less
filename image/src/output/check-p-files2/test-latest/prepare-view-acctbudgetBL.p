
DEFINE TEMP-TABLE b-list 
  FIELD k AS INTEGER 
  FIELD monat AS CHAR FORMAT "x(3)" LABEL "Month" 
  FIELD wert LIKE gl-acct.budget[1] COLUMN-LABEL "Budget Value".

DEF TEMP-TABLE gl-acct1
    FIELD fibukonto LIKE gl-acct.fibukonto
    FIELD bezeich   LIKE gl-acct.bezeich
    FIELD budget    LIKE gl-acct.budget.

DEF INPUT  PARAMETER fibukonto      AS CHAR.
DEF OUTPUT PARAMETER curr-yr        AS INTEGER.
DEF OUTPUT PARAMETER price-decimal  AS INTEGER.
DEF OUTPUT PARAMETER tot-budget     AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR b-list.
DEF OUTPUT PARAMETER TABLE FOR gl-acct1.


FIND FIRST htparam WHERE paramnr = 597 NO-LOCK. 
curr-yr = year(fdate). 
FIND FIRST htparam WHERE htparam.paramnr = 491. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 

RUN create-b-list.
RUN create-gl-acct1.

PROCEDURE create-b-list: 
   DEFINE VARIABLE i AS INTEGER. 
   DEFINE VARIABLE mon AS CHAR FORMAT "x(3)" EXTENT 12 INITIAL 
       ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", 
        "AUG", "SEP", "OCT", "NOV", "DEC"]. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fibukonto NO-LOCK. 
   tot-budget = 0. 
   DO i = 1 TO 12: 
      tot-budget = tot-budget + gl-acct.budget[i]. 
      create b-list. 
      b-list.k = i. 
      b-list.monat = mon[i]. 
      b-list.wert = gl-acct.budget[i]. 
   END. 
END. 

PROCEDURE create-gl-acct1:
    DEF VAR i AS INT.
    FOR EACH gl-acct WHERE gl-acct.activeflag = YES 
        AND (acc-type = 1 OR acc-type = 2 OR acc-type = 5) 
        NO-LOCK BY gl-acct.fibukonto:
        CREATE gl-acct1.
        ASSIGN gl-acct1.fibukonto = gl-acct.fibukonto
               gl-acct1.bezeich   = gl-acct.bezeich.

        DO i = 1 TO 12: 
          ASSIGN
            gl-acct1.budget[i]    = gl-acct.budget[i].
        END. 
    END.
END.
