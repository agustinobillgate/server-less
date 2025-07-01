
DEFINE TEMP-TABLE output-list
  FIELD coa         AS CHAR     FORMAT "x(10)"
  FIELD post-date   AS DATE     FORMAT "99.99.9999"
  FIELD liq-item    AS CHAR     FORMAT "x(6)"
  FIELD trans-curr  AS CHAR     FORMAT "x(3)"
  FIELD amt-trans   AS DECIMAL  FORMAT "->>>>>>>>>>>>9"
  FIELD trd-partner AS CHAR     FORMAT "x(4)"
  FIELD debit       AS DECIMAL  FORMAT "->>>>>>>>>>>>9"
  FIELD credit      AS DECIMAL  FORMAT "->>>>>>>>>>>>9"
  FIELD bezeich     AS CHAR     FORMAT "x(50)"
  FIELD cf-bezeich  AS CHAR     FORMAT "x(70)"
  FIELD cashflow-code AS CHAR   FORMAT "x(20)"
  .

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER to-date          AS DATE    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE from-date AS DATE.
DEFINE VARIABLE currency  AS CHAR.

DEFINE BUFFER b-jouhdr FOR gl-jouhdr.

/*************** MAIN LOGIC ***************/     
FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
IF AVAILABLE htparam THEN
DO: 
    IF htparam.fchar = "RP" THEN
    DO:
       ASSIGN currency = "IDR".
    END.                      
    ELSE IF htparam.fchar = "US$" THEN
    DO:
        ASSIGN currency = "USD".
    END.
    ELSE ASSIGN currency = htparam.fchar.
END.

ASSIGN from-date = DATE(MONTH(to-date), 1, YEAR(to-date)).

RUN create-list.

PROCEDURE create-list:
  DEFINE VARIABLE c             AS CHARACTER.
  DEFINE VARIABLE cashflow-code AS CHARACTER.
  DEFINE VARIABLE amount        AS DECIMAL.
  DEFINE VARIABLE post-date     AS DATE.
  DEFINE VARIABLE coa           AS CHAR.
  DEFINE VARIABLE liq-item      AS CHAR.
  DEFINE VARIABLE trd-partner   AS CHAR.


  FOR EACH gl-journal NO-LOCK,
    FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto NO-LOCK,
    FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr
     AND gl-jouhdr.datum GE from-date
     AND gl-jouhdr.datum LE to-date NO-LOCK BY gl-jouhdr.datum BY gl-journal.fibukonto:
        /*RUN convert-fibu(gl-acct.fibukonto, OUTPUT c).*/

    IF NUM-ENTRIES(gl-journal.bemerk,CHR(2)) GE 2 THEN 
    DO:
      IF ENTRY(2,gl-journal.bemerk,CHR(2)) NE "" THEN
      DO:
        FIND FIRST output-list WHERE output-list.coa = gl-journal.fibukonto
            AND output-list.post-date = gl-jouhdr.datum
            AND output-list.cashflow-code = ENTRY(2,gl-journal.bemerk,CHR(2)) NO-LOCK NO-ERROR.
        IF NOT AVAILABLE output-list THEN
        DO:
          CREATE output-list.
          ASSIGN
              cashflow-code             = ENTRY(2,gl-journal.bemerk,CHR(2))
              output-list.cashflow-code = ENTRY(2,gl-journal.bemerk,CHR(2))
              output-list.coa           = gl-acct.fibukonto
              output-list.post-date     = gl-jouhdr.datum
              output-list.trans-curr    = currency
              output-list.liq-item      = SUBSTR(cashflow-code, 1, 6)
              /*output-list.trd-partner   = SUBSTR(cashflow-code, 7, 4)*/
              output-list.bezeich       = STRING(ENTRY(1, gl-journal.bemerk, CHR(2)), "x(50)")
              output-list.amt-trans     = ROUND(gl-journal.debit - gl-journal.credit, 0).
           .

          IF SUBSTR(cashflow-code, 7, 4) = "0000" THEN trd-partner = " ".
          ELSE trd-partner = SUBSTR(cashflow-code, 7, 4).
          output-list.trd-partner = trd-partner.
          
          FIND FIRST queasy WHERE queasy.KEY = 177
              AND queasy.deci1 = DEC(cashflow-code) NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN
          DO:
              output-list.cf-bezeich = queasy.char1.
          END.
        END.
        ELSE 
        DO:
          output-list.amt-trans = output-list.amt-trans + ROUND(gl-journal.debit - gl-journal.credit, 0).
        END.
      END.
    END.
  END.
END.

PROCEDURE convert-fibu: 
DEFINE INPUT  PARAMETER konto   AS CHAR. 
DEFINE OUTPUT PARAMETER s       AS CHAR INITIAL "". 
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
  ch = htparam.fchar. 
  j = 0. 
  DO i = 1 TO length(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 
                                                                                                                                                                                                               
