
DEFINE TEMP-TABLE t-kellner1 LIKE vhp.kellner. 

DEFINE TEMP-TABLE table-list 
    FIELD rechnr     AS INTEGER 
    FIELD tischnr    AS INTEGER 
    FIELD saldo      AS DECIMAL 
    FIELD belong     AS CHAR INITIAL "L". 

DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER TABLE FOR table-list.
DEF INPUT PARAMETER transdate AS DATE.
DEF INPUT PARAMETER curr-waiter AS INT.
DEF INPUT PARAMETER curr-dept AS INT.
DEF INPUT PARAMETER usr-nr AS INT.
DEF OUTPUT PARAMETER bill-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-kellner1.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "TS-restinv".

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 110 no-lock. /* billdate */ 
bill-date = vhp.htparam.fdate. 
IF transdate NE ? THEN bill-date = transdate. 
ELSE 
DO: 
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 253 NO-LOCK. /* NA running */ 
    IF vhp.htparam.flogical AND bill-date LT TODAY THEN bill-date = bill-date + 1. 
END. 

RUN transfer-now(curr-waiter, usr-nr, bill-date).

PROCEDURE transfer-now: 
  DEFINE INPUT PARAMETER k1 AS integer.  /* CURRENT waiter */ 
  DEFINE INPUT PARAMETER k2 AS integer.  /* NEW waiter */ 
  DEFINE INPUT PARAMETER bill-date AS DATE. 
 
  DEFINE buffer hbill FOR vhp.h-bill. 
  DEFINE buffer hbill1 FOR vhp.h-bill. 
  DEFINE buffer kellner1 FOR vhp.kellner. 
  DEFINE buffer kellner2 FOR vhp.kellner. 
  DEFINE buffer umsatz2 FOR vhp.umsatz. 
 
  DO TRANSACTION: 
    FIND FIRST kellner1 WHERE kellner1.kellner-nr = k1 
     AND kellner1.departement = curr-dept NO-LOCK. 
    FIND FIRST kellner2 WHERE kellner2.kellner-nr = k2 
      AND kellner2.departement = curr-dept NO-LOCK. 
 
    FOR EACH table-list WHERE table-list.belong = "R": 
      FIND FIRST hbill WHERE hbill.rechnr = table-list.rechnr 
        AND hbill.departement = curr-dept NO-LOCK. 
      IF AVAILABLE hbill THEN /*FT serverless*/
      DO:
          FIND FIRST hbill1 WHERE RECID(hbill1) = RECID(hbill) EXCLUSIVE-LOCK. 
          ASSIGN hbill1.kellner-nr = k2. 
          FIND CURRENT hbill1 NO-LOCK. 
     
          FIND FIRST vhp.h-bill-line WHERE vhp.h-bill-line.rechnr = hbill.rechnr 
            AND vhp.h-bill-line.departement = curr-dept NO-LOCK NO-ERROR. 
          IF AVAILABLE vhp.h-bill-line THEN 
          DO: 
            CREATE vhp.h-journal. 
            ASSIGN 
              vhp.h-journal.rechnr = hbill.rechnr 
              vhp.h-journal.departement = hbill.departement 
              vhp.h-journal.bill-datum = h-bill-line.bill-datum 
              vhp.h-journal.tischnr = hbill.tischnr 
              vhp.h-journal.zeit = TIME 
              vhp.h-journal.kellner-nr = k1 
            . 
            vhp.h-journal.bezeich = translateExtended ("Waiter Transfer To",lvCAREA,"") 
              + " " + STRING(k2). 
          END. 
          DELETE table-list. 
      END.
 
      
    END. 
  END. /* TRANSACTION */ 

  IF AVAILABLE kellner1 THEN
  DO:
      CREATE t-kellner1.
      BUFFER-COPY kellner1 TO t-kellner1.
  END.
END. 

