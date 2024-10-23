DEFINE buffer gl-acc1    FOR gl-acct. 
DEFINE buffer gl-acct1   FOR gl-acct. 
DEFINE buffer gl-jouhdr1 FOR gl-jouhdr. 

DEFINE TEMP-TABLE s-list 
  FIELD fibukonto   LIKE gl-acct.fibukonto 
  FIELD bezeich     AS CHAR FORMAT "x(28)" 
  FIELD credit      AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" 
  FIELD debet       AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99". 

DEFINE TEMP-TABLE g-list 
  FIELD  nr         AS INTEGER 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  debit      LIKE gl-journal.debit 
  FIELD  credit     LIKE gl-journal.credit 
  FIELD  bemerk     AS CHAR FORMAT "x(32)" 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  duplicate  AS LOGICAL INITIAL YES
    
  FIELD gl-acct1-fibukonto LIKE gl-acct1.fibukonto
  FIELD gl-acct1-bezeich LIKE gl-acct1.bezeich.

DEF TEMP-TABLE buff-g-list LIKE g-list.

DEF INPUT PARAMETER datum AS DATE.
DEF INPUT PARAMETER user-init AS CHAR.
DEF INPUT-OUTPUT PARAMETER curr-anz AS INT.
DEF INPUT-OUTPUT PARAMETER debits AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER credits AS DECIMAL.
DEF INPUT-OUTPUT PARAMETER remains AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR buff-g-list.

DEFINE VARIABLE debit-betrag    AS DECIMAL. 
DEFINE VARIABLE credit-betrag   AS DECIMAL. 
DEFINE VARIABLE depn-value      AS DECIMAL.

DEFINE VARIABLE dept-methode    AS LOGICAL.
/**/

FIND FIRST htparam WHERE htparam.paramnr = 1366 AND htparam.bezeich NE "not used" NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
  dept-methode = htparam.flogical.
END.


FOR EACH fa-artikel WHERE fa-artikel.next-depn EQ datum
    AND fa-artikel.loeschflag = 0 NO-LOCK, 
    FIRST mathis WHERE mathis.nr = fa-artikel.nr NO-LOCK BY mathis.name: 

    FIND FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp
      AND fa-grup.flag = 1 NO-LOCK.
    RUN get-depn-value. 
    IF depn-value GT 0 THEN 
    DO: 
      FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fa-grup.credit-fibu 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE gl-acc1 THEN
      FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fa-artikel.credit-fibu 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acc1 THEN 
      DO: 
        credit-betrag = depn-value. 
        debit-betrag = 0. 
        RUN add-list(YES). 
      END. 
      ELSE 
      DO: 
        /*MT
        hide MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("Accum.-Depn Account not defined:", lvCAREA, "":U) 
            SKIP 
            translateExtended ("Fix-Asset Name : ", lvCAREA, "":U) + mathis.name 
            VIEW-AS ALERT-BOX INFORMATION.
        */
      END. 
 
      FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fa-grup.debit-fibu 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE gl-acc1 THEN
      FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fa-artikel.debit-fibu 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acc1 THEN 
      DO: 
        debit-betrag = depn-value. 
        credit-betrag = 0. 
        RUN add-list(YES). 
      END. 
      ELSE 
      DO: 
        /*MT
        hide MESSAGE NO-PAUSE. 
        MESSAGE translateExtended ("Depn-Expense Account not defined", lvCAREA, "":U) 
            SKIP 
            translateExtended ("Fixed-Asset Name : ", lvCAREA, "":U) + mathis.name 
            VIEW-AS ALERT-BOX INFORMATION. 
        */
      END. 
    END. 
END.

FOR EACH g-list NO-LOCK, 
    FIRST gl-acct1 WHERE gl-acct1.fibukonto = g-list.fibukonto NO-LOCK 
    BY g-list.sysdate descending BY g-list.zeit descending:
    CREATE buff-g-list.
    BUFFER-COPY g-list TO buff-g-list.
    ASSIGN buff-g-list.gl-acct1-fibukonto = gl-acct1.fibukonto
           buff-g-list.gl-acct1-bezeich   = gl-acct1.bezeich.
END.

PROCEDURE add-list: 
DEFINE INPUT PARAMETER create-it AS LOGICAL. 
  curr-anz = curr-anz + 1. 
  IF create-it THEN create g-list. 
  g-list.nr = fa-artikel.nr. 
  g-list.fibukonto = gl-acc1.fibukonto. 
  g-list.debit = g-list.debit + debit-betrag. 
  g-list.credit = g-list.credit + credit-betrag. 
  g-list.bemerk = mathis.asset + " - " + mathis.name. 
  g-list.userinit = user-init. 
  g-list.zeit = time. 
  g-list.duplicate = NO. 
 
  FIND FIRST s-list WHERE s-list.fibukonto = gl-acc1.fibukonto 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE s-list THEN 
  DO: 
    create s-list. 
    s-list.fibukonto = gl-acc1.fibukonto. 
    s-list.bezeich = gl-acc1.bezeich. 
  END. 
  s-list.credit = s-list.credit + credit-betrag. 
  s-list.debet = s-list.debet + debit-betrag. 
 
  credits = credits + credit-betrag. 
  debits = debits + debit-betrag. 
  remains = debits - credits. 
  debit-betrag = 0. 
  credit-betrag = 0. 
END. 

PROCEDURE get-depn-value: 
DEFINE VARIABLE tot-anz AS INTEGER. 
  FIND FIRST fa-kateg WHERE fa-kateg.katnr = fa-artikel.katnr NO-LOCK. 
  IF fa-kateg.methode = 0 THEN 
  DO: 
    IF dept-methode THEN
    DO:
        tot-anz = fa-kateg.nutzjahr - fa-artikel.anz-depn. 
    END.
    ELSE
    DO:
      tot-anz = fa-kateg.nutzjahr * 12 - fa-artikel.anz-depn. 
    END.
    
    IF tot-anz GT 0 THEN depn-value = fa-artikel.book-wert / tot-anz. 
    ELSE depn-value = 0. 
  END. 
END. 
