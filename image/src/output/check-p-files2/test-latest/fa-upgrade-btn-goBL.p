
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

DEFINE INPUT PARAMETER TABLE FOR g-list.
DEFINE INPUT PARAMETER p-nr    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER nr      AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER amt     AS DECIMAL NO-UNDO.
DEFINE INPUT PARAMETER user-init AS CHAR  NO-UNDO.
DEFINE INPUT PARAMETER qty     AS INTEGER NO-UNDO. 
DEFINE INPUT PARAMETER refno   AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER datum   AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER bezeich AS CHAR    NO-UNDO.
DEFINE INPUT PARAMETER debits  AS DECIMAL NO-UNDO.
DEFINE INPUT PARAMETER credits AS DECIMAL NO-UNDO.
DEFINE INPUT PARAMETER remains AS DECIMAL NO-UNDO.

DEFINE VARIABLE new-hdr AS LOGICAL INITIAL YES. 

RUN create-header. 
RUN create-journals. 
RUN update-fix-asset. 

PROCEDURE create-header: 
  CREATE gl-jouhdr. 
  FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
  IF NOT AVAILABLE counters THEN 
  DO: 
    CREATE counters. 
    ASSIGN counters.counter-no = 25
           counters.counter-bez = "G/L Transaction Journal". 
  END. 
  counters.counter = counters.counter + 1. 
  FIND CURRENT counters NO-LOCK.
  ASSIGN 
      gl-jouhdr.jnr     = counters.counter
      gl-jouhdr.refno   = refno 
      gl-jouhdr.datum   = datum 
      gl-jouhdr.bezeich = bezeich 
      gl-jouhdr.batch   = YES 
      gl-jouhdr.jtype   = 7 
      new-hdr           = YES. 
END. 
 
PROCEDURE create-journals: 
  FOR EACH g-list  NO-LOCK: 
    CREATE gl-journal. 
    ASSIGN gl-journal.jnr       = /*MT 23/10/13 gl-jouhdr.jnr. */ counters.counter
           gl-journal.fibukonto = g-list.fibukonto 
           gl-journal.debit     = g-list.debit 
           gl-journal.credit    = g-list.credit 
           gl-journal.bemerk    = g-list.bemerk 
           gl-journal.userinit  = g-list.userinit 
           gl-journal.zeit      = g-list.zeit. 
  END. 
  DO TRANSACTION: 
    IF remains = 0.01 OR remains = - 0.01 THEN remains = 0. 
    FIND CURRENT gl-jouhdr EXCLUSIVE-LOCK. 
    ASSIGN gl-jouhdr.credit = credits
           gl-jouhdr.debit  = debits 
           gl-jouhdr.remain = remains. 
    FIND CURRENT gl-jouhdr NO-LOCK. 
  END. 
  RELEASE gl-jouhdr. 
END. 
 
PROCEDURE update-fix-asset: 
DEFINE VARIABLE orig-bookval AS DECIMAL. 
DEFINE VARIABLE qty AS DECIMAL. 
DEFINE BUFFER fa-art FOR fa-artikel. /* upgrade artikel */
DEFINE BUFFER mhis FOR mathis. 

  ASSIGN qty = fa-artikel.anzahl
         orig-bookval = fa-artikel.book-wert. 
  FIND CURRENT fa-artikel EXCLUSIVE-LOCK. 
  ASSIGN fa-artikel.posted    = YES 
         fa-artikel.warenwert = fa-artikel.warenwert + amt /* amt = upgrade value */
         fa-artikel.book-wert = fa-artikel.book-wert + amt. 
  FIND CURRENT fa-artikel NO-LOCK. 
 
/* upgrade article */
  FIND FIRST mhis WHERE mhis.nr = p-nr NO-LOCK NO-ERROR. 
  FIND FIRST fa-art WHERE fa-art.nr = p-nr EXCLUSIVE-LOCK. 
  ASSIGN fa-art.loeschflag = 1 
         fa-art.p-nr       = nr 
         fa-art.deleted    = datum 
         fa-art.did        = user-init. 
  FIND CURRENT fa-art NO-LOCK. 
 
  CREATE mhis-line. 
  ASSIGN mhis-line.nr      = nr
         mhis-line.datum   = datum 
         mhis-line.remark  = "Upgrading Part: " + mhis.name 
                + "; Value = " + TRIM(STRING(amt,">,>>>,>>>,>>9.99")). 
  FIND CURRENT mhis-line NO-LOCK. 
 
  CREATE fa-op. 
  ASSIGN fa-op.nr           = nr
         fa-op.opart        = 4 
         fa-op.datum        = datum 
         fa-op.zeit         = TIME 
         fa-op.anzahl       = qty 
         fa-op.einzelpreis  = orig-bookval 
         fa-op.warenwert    = amt 
         fa-op.id           = user-init 
         fa-op.lscheinnr    = refno 
         fa-op.docu-nr      = mhis.asset + " - " + mhis.NAME 
         fa-op.lief-nr      = fa-op.lief-nr. 
  RELEASE fa-op. 
END. 
