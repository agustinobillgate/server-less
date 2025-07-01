
DEFINE TEMP-TABLE g-list 
  FIELD  nr         AS INTEGER 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  debit      LIKE gl-journal.debit 
  FIELD  credit     LIKE gl-journal.credit 
  FIELD  bemerk     AS CHAR FORMAT "x(32)" 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL TODAY 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  duplicate  AS LOGICAL INITIAL YES. 

DEFINE TEMP-TABLE s-list 
  FIELD fibukonto LIKE gl-acct.fibukonto 
  FIELD bezeich   AS CHAR FORMAT "x(28)" 
  FIELD credit    AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99" 
  FIELD debet     AS DECIMAL FORMAT ">>,>>>,>>>,>>9.99". 

DEFINE INPUT PARAMETER p-nr            AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER amt             AS DECIMAL NO-UNDO.
DEFINE INPUT PARAMETER user-init       AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER debits         AS DECIMAL NO-UNDO.
DEFINE OUTPUT PARAMETER credits        AS DECIMAL NO-UNDO.
DEFINE OUTPUT PARAMETER avail-gl-acct  AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER avail-gl-acct1 AS LOGICAL NO-UNDO.
DEFINE OUTPUT PARAMETER name-mathis    AS CHAR    NO-UNDO.
DEFINE OUTPUT PARAMETER curr-anz       AS INTEGER NO-UNDO. 
DEFINE OUTPUT PARAMETER remains        AS DECIMAL NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR g-list.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.


DEFINE VARIABLE debit-betrag   AS DECIMAL NO-UNDO.
DEFINE VARIABLE credit-betrag  AS DECIMAL NO-UNDO.


FIND FIRST fa-artikel WHERE fa-artikel.nr = p-nr NO-LOCK NO-ERROR. 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN 
DO: 
    ASSIGN avail-gl-acct1 = YES
           debit-betrag   = amt 
           credit-betrag  = 0.
    RUN add-list(YES). 
END. 

FIND FIRST mathis WHERE mathis.nr = p-nr NO-LOCK NO-ERROR. 
FIND FIRST fa-artikel WHERE fa-artikel.nr = p-nr NO-LOCK NO-ERROR. 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN 
DO: 
    ASSIGN avail-gl-acct = YES
           credit-betrag = amt 
           debit-betrag  = 0.
    RUN add-list(YES). 
END. 
ELSE 
DO: 
    ASSIGN name-mathis   = mathis.NAME.
END. 


PROCEDURE add-list: 
DEFINE INPUT PARAMETER create-it AS LOGICAL. 
  curr-anz = curr-anz + 1. 
  IF create-it THEN 
      CREATE g-list. 
      ASSIGN g-list.nr          = fa-artikel.nr 
             g-list.fibukonto   = gl-acct.fibukonto 
             g-list.debit       = g-list.debit + debit-betrag 
             g-list.credit      = g-list.credit + credit-betrag 
             g-list.bemerk      = mathis.asset + " - " + mathis.NAME
             g-list.userinit    = user-init 
             g-list.zeit        = TIME
             g-list.duplicate   = NO. 
 
  FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE s-list THEN 
  DO: 
    CREATE s-list. 
    ASSIGN s-list.fibukonto = gl-acct.fibukonto
           s-list.bezeich   = gl-acct.bezeich. 
  END. 
  ASSIGN s-list.credit = s-list.credit + credit-betrag
         s-list.debet = s-list.debet + debit-betrag
         credits = credits + credit-betrag 
         debits = debits + debit-betrag 
         remains = debits - credits 
         debit-betrag = 0
         credit-betrag = 0. 
END. 
