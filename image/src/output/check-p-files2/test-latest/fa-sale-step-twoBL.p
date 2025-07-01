DEFINE buffer gl-acc1    FOR gl-acct.
DEFINE buffer gl-acct1   FOR gl-acct.
DEFINE buffer gl-jouhdr1 FOR gl-jouhdr.

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
    
  FIELD  acct-fibukonto LIKE gl-acct1.fibukonto
  FIELD  acct-bezeich   LIKE gl-acct1.bezeich.

DEFINE TEMP-TABLE s-list 
  FIELD fibukonto LIKE gl-acct.fibukonto 
  FIELD bezeich     AS CHAR FORMAT "x(28)" 
  FIELD credit      AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" 
  FIELD debet       AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99". 

DEFINE TEMP-TABLE buff-g-list LIKE g-list.

DEF INPUT PARAMETER nr          AS INT.
DEF INPUT PARAMETER qty         AS INT.
DEF INPUT PARAMETER amt         AS DECIMAL.
DEF INPUT PARAMETER user-init   AS CHAR.
DEF OUTPUT PARAMETER fa-wert    AS DECIMAL. 
DEF OUTPUT PARAMETER depn-wert  AS DECIMAL. 
DEF OUTPUT PARAMETER book-wert  AS DECIMAL. 
DEF OUTPUT PARAMETER curr-anz   AS INTEGER. 
DEF OUTPUT PARAMETER debits     AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Debets". 
DEF OUTPUT PARAMETER credits    AS DECIMAL FORMAT ">>>,>>>,>>9.99" LABEL "Credits". 
DEF OUTPUT PARAMETER remains    AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR buff-g-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.

DEFINE VARIABLE profit          AS DECIMAL.
DEFINE VARIABLE credit-betrag   AS DECIMAL.
DEFINE VARIABLE debit-betrag    AS DECIMAL.

FIND FIRST fa-artikel WHERE fa-artikel.nr = nr NO-LOCK. 
FIND FIRST mathis WHERE mathis.nr = nr NO-LOCK. 

IF qty = fa-artikel.anzahl THEN 
DO: 
    fa-wert = fa-artikel.warenwert. 
    book-wert = fa-artikel.book-wert. 
    depn-wert = fa-artikel.depn-wert. 
END. 
ELSE 
DO: 
    fa-wert = fa-artikel.warenwert * qty / fa-artikel.anzahl. 
    book-wert = fa-artikel.book-wert * qty / fa-artikel.anzahl. 
    depn-wert = fa-artikel.depn-wert * qty / fa-artikel.anzahl. 
END. 
profit = amt - book-wert. 
 
FIND FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp
  AND fa-grup.flag = 1 NO-LOCK.
FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fa-grup.fibukonto NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-acc1 THEN
FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fa-artikel.fibukonto NO-LOCK NO-ERROR. 

IF AVAILABLE gl-acc1 THEN 
DO: 
    credit-betrag = fa-wert. 
    debit-betrag = 0. 
    RUN add-list(YES). 
END. 
ELSE 
DO: 
    /*MT
    hide MESSAGE NO-PAUSE. 
    MESSAGE translateExtended ("Fixed Asset Account not defined.", lvCAREA, "":U) 
        VIEW-AS ALERT-BOX INFORMATION.
    */
END. 
 
IF depn-wert NE 0 THEN 
DO: 
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fa-artikel.credit-fibu 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acc1 THEN 
    DO: 
      debit-betrag = depn-wert. 
      credit-betrag = 0. 
      RUN add-list(YES). 
    END. 
    ELSE 
    DO: 
      /*MT
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("Accum-Depn Account not defined.", lvCAREA, "":U) 
          VIEW-AS ALERT-BOX INFORMATION. 
      */
    END. 
END. 
 
IF amt NE 0 THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 882 NO-LOCK. 
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = htparam.fchar 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acc1 THEN 
    DO: 
      debit-betrag = amt. 
      credit-betrag = 0. 
      RUN add-list(YES). 
    END. 
    ELSE 
    DO: 
      /*MT
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("AcctNo for cash clearance not defined (Param 882)", 
          lvCAREA, "":U) VIEW-AS ALERT-BOX INFORMATION. 
      */
    END. 
END. 
 
IF profit GT 0 THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 885 NO-LOCK. 
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = htparam.fchar 
    NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acc1 THEN 
    DO: 
      credit-betrag = profit. 
      debit-betrag = 0. 
      RUN add-list(YES). 
    END. 
    ELSE IF profit LT 0 THEN 
    DO: 
      /*MT
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("AcctNo for Income not defined (Param 885).", lvCAREA, "":U) 
          VIEW-AS ALERT-BOX INFORMATION. 
      */
    END. 
END. 
ELSE IF profit LT 0 THEN 
DO: 
    FIND FIRST htparam WHERE paramnr = 886 NO-LOCK. 
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = htparam.fchar 
    NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acc1 THEN 
    DO: 
      debit-betrag = - profit. 
      credit-betrag = 0. 
      RUN add-list(YES). 
    END. 
    ELSE 
    DO: 
      /*MT
      hide MESSAGE NO-PAUSE. 
      MESSAGE translateExtended ("AcctNo for Expense not defined (Param 886).", 
         lvCAREA, "":U) VIEW-AS ALERT-BOX INFORMATION. 
      */
    END. 
END. 

FOR EACH g-list NO-LOCK, 
    FIRST gl-acct1 WHERE gl-acct1.fibukonto = g-list.fibukonto NO-LOCK :
    CREATE buff-g-list.
    BUFFER-COPY g-list TO buff-g-list.
    ASSIGN buff-g-list.acct-fibukonto = gl-acct1.fibukonto
           buff-g-list.acct-bezeich   = gl-acct1.bezeich.
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
