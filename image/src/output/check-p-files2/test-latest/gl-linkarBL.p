DEFINE TEMP-TABLE g-list 
  FIELD  rechnr     AS INTEGER 
  FIELD  dept       AS INTEGER 
  FIELD  jnr        LIKE gl-journal.jnr 
  FIELD  fibukonto  LIKE gl-journal.fibukonto 
  FIELD  debit      LIKE gl-journal.debit 
  FIELD  credit     LIKE gl-journal.credit 
  FIELD  bemerk     AS CHAR FORMAT "x(50)" 
  FIELD  userinit   LIKE gl-journal.userinit 
  FIELD  sysdate    LIKE gl-journal.sysdate INITIAL today 
  FIELD  zeit       LIKE gl-journal.zeit 
  FIELD  chginit    LIKE gl-journal.chginit 
  FIELD  chgdate    LIKE gl-journal.chgdate INITIAL ? 
  FIELD  duplicate  AS LOGICAL INITIAL YES 
  FIELD  add-info   AS CHAR 
  FIELD  counter    AS INTEGER
  FIELD  acct-fibukonto LIKE gl-acct.fibukonto
  FIELD  bezeich    LIKE gl-acct.bezeich.

DEFINE TEMP-TABLE buf-g-list LIKE g-list.

DEFINE TEMP-TABLE s-list 
  FIELD fibukonto   LIKE gl-acct.fibukonto 
  FIELD bezeich     AS CHAR FORMAT "x(28)" 
  FIELD credit      AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99"   /*>>,>>>,>>9.99*/ /* Gerald 050320 */
  FIELD debit       AS DECIMAL FORMAT ">>>,>>>,>>>,>>9.99".  /*>>,>>>,>>9.99*/ /* Gerald 050320 */

DEF TEMP-TABLE pay-list 
    FIELD counter   AS INTEGER INITIAL 0 
    FIELD ar-recid  AS INTEGER 
    FIELD NAME      AS CHAR 
    FIELD artnr     AS INTEGER INITIAL 0 
    FIELD zahlkonto AS INTEGER INITIAL 0 
    FIELD amount    AS DECIMAL INITIAL 0 
    FIELD add-info  AS CHAR 
    INDEX idx1 ar-recid 
    INDEX idx2 artnr counter 
    INDEX idx3 counter zahlkonto. 

DEF INPUT PARAMETER merge-flag AS LOGICAL.
DEF INPUT PARAMETER from-date  AS DATE.
DEF INPUT PARAMETER to-date    AS DATE.
DEF INPUT PARAMETER user-init  AS CHAR.
DEF INPUT PARAMETER refno      AS CHAR NO-UNDO.

DEF INPUT-OUTPUT PARAMETER curr-anz AS INT.

DEF OUTPUT PARAMETER acct-error AS INTEGER INIT 0.
DEF OUTPUT PARAMETER debits     LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER credits    LIKE gl-acct.actual[1].
DEF OUTPUT PARAMETER remains    AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR buf-g-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER art-artnr  AS INT.
DEF OUTPUT PARAMETER art-bezeich AS CHAR.

DEFINE VARIABLE add-info        AS CHAR NO-UNDO.
DEFINE VARIABLE fibukonto       AS CHAR.
DEFINE VARIABLE credit-betrag   AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE VARIABLE debit-betrag    AS DECIMAL FORMAT "->>>,>>>,>>9.99".
DEFINE buffer gl-acct1 FOR gl-acct. 

FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = refno 
  AND gl-jouhdr.jtype = 2 NO-LOCK NO-ERROR. 
IF AVAILABLE gl-jouhdr THEN 
DO: 
  acct-error = 1.
  RETURN.
END.

IF NOT merge-flag THEN RUN step-two. 
ELSE RUN step-twoA. 

PROCEDURE step-two: 
DEFINE buffer art1 FOR artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 

  FOR EACH debitor WHERE debitor.rgdatum GE from-date 
    AND debitor.rgdatum LE to-date 
    AND debitor.opart GT 0 AND debitor.zahlkonto NE 0 NO-LOCK: 
   
    /* A/R article */ 
    add-info = ";&&1;" + STRING(debitor.artnr) + ";" 
      + STRING(debitor.rechnr) + ";" + STRING(debitor.betriebsnr). 
 
    FIND FIRST art1 WHERE art1.artnr = debitor.artnr /* AR article */
      AND art1.departement = 0 NO-LOCK. 
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = art1.fibukonto 
      NO-LOCK NO-ERROR. 

    IF AVAILABLE gl-acc1 THEN 
    DO: 
      fibukonto = gl-acc1.fibukonto. /* COA OF debt article */ 
      IF debitor.saldo LT 0 THEN 
      DO: 
        credit-betrag = - debitor.saldo. 
        debit-betrag = 0. 
 
        FIND FIRST g-list WHERE g-list.fibukonto = gl-acc1.fibukonto 
          AND g-list.rechnr = debitor.rechnr 
          AND g-list.dept = debitor.betriebsnr NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
        ELSE RUN add-list(NO).  
      END. 
      ELSE IF debitor.saldo GT 0 THEN 
      DO: 
        debit-betrag = debitor.saldo. 
        credit-betrag = 0. 
 
        FIND FIRST g-list WHERE g-list.fibukonto = gl-acc1.fibukonto 
          AND g-list.rechnr = debitor.rechnr NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
        ELSE RUN add-list(NO).  
      END. 
    END. 
    ELSE 
    DO: 
      ASSIGN
        art-artnr   = art1.artnr
        art-bezeich = art1.bezeich
        acct-error  = 2
      . 
      RETURN. 
    END. 
 
    /* A/R Payment article */ 
    add-info = ";&&2;" + STRING(debitor.artnr) + ";" 
      + STRING(debitor.counter) + ";" + STRING(debitor.zahlkonto). 
 
    FIND FIRST artikel WHERE artikel.artnr = debitor.zahlkonto 
      AND artikel.departement = 0 NO-LOCK. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.fibukonto NO-LOCK 
      NO-ERROR. 

    IF AVAILABLE gl-acct THEN 
    DO: 
      fibukonto = gl-acct.fibukonto.  /*COA OF A/R Payment article */ 
      IF debitor.saldo LE 0 THEN 
      DO: 
        debit-betrag = - debitor.saldo. 
        credit-betrag = 0. 
        RUN add-list(YES). 
      END. 
      ELSE IF debitor.saldo GT 0 THEN 
      DO: 
        credit-betrag = debitor.saldo. 
        debit-betrag = 0. 
        RUN add-list(YES). 
      END. 
    END. 
    ELSE 
    DO: 
      ASSIGN
        art-artnr   = artikel.artnr
        art-bezeich = artikel.bezeich
        acct-error  = 2
      . 
      RETURN. 
    END. 
  END. 

  RUN adjust-lists.

  /*FOR EACH g-list NO-LOCK,
    FIRST gl-acct1 WHERE gl-acct1.fibukonto = g-list.fibukonto NO-LOCK 
      BY g-list.sysdate descending BY g-list.zeit descending:FT serverless*/
  FOR EACH g-list NO-LOCK BY g-list.sysdate descending BY g-list.zeit descending:
    FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = g-list.fibukonto NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct1 THEN
    DO:
        CREATE buf-g-list.
        BUFFER-COPY g-list TO buf-g-list.
        ASSIGN
          buf-g-list.acct-fibukonto = gl-acct1.fibukonto
          buf-g-list.bezeich = gl-acct1.bezeich.
    END.
  END.
END. 
 
PROCEDURE adjust-lists:
  FOR EACH g-list.
      IF g-list.credit = g-list.debit THEN DELETE g-list.
      ELSE IF g-list.credit GT g-list.debit THEN
      ASSIGN
          g-list.credit = g-list.credit - g-list.debit
          g-list.debit  = 0.
      ELSE
      ASSIGN
          g-list.debit  = g-list.debit - g-list.credit
          g-list.credit = 0.
  END.
  FOR EACH s-list:
      DELETE s-list.
  END.
  FOR EACH g-list:
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = g-list.fibukonto
        NO-LOCK.
    FIND FIRST s-list WHERE s-list.fibukonto = gl-acct.fibukonto 
        NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE s-list THEN 
    DO: 
      CREATE s-list. 
      ASSIGN
        s-list.fibukonto = gl-acct.fibukonto
        s-list.bezeich   = gl-acct.bezeich. 
    END. 
    ASSIGN
      s-list.credit = s-list.credit + g-list.credit 
      s-list.debit  = s-list.debit + g-list.debit. 
  END.
END.

PROCEDURE step-twoA: 
DEFINE buffer art1 FOR artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 
DEF VAR curr-art   AS INTEGER INITIAL 0 NO-UNDO. 
DEF VAR curr-zahl  AS INTEGER INITIAL 0 NO-UNDO. 
DEF VAR curr-count AS INTEGER INITIAL 0 NO-UNDO. 
DEF VAR curr-saldo AS DECIMAL INITIAL 0 NO-UNDO. 
DEF VAR curr-pay AS DECIMAL INITIAL 0 NO-UNDO. 
DEF VAR do-it AS LOGICAL NO-UNDO. 
DEF VAR pay-it AS LOGICAL NO-UNDO. 
 
  FOR EACH pay-list: 
      DELETE pay-list. 
  END. 
  FOR EACH g-list: 
      DELETE g-list. 
  END. 
  FOR EACH s-list: 
      DELETE s-list. 
  END. 
  
                  
  FOR EACH debitor WHERE debitor.rgdatum GE from-date 
    AND debitor.rgdatum LE to-date 
    AND debitor.opart GT 0 AND debitor.zahlkonto NE 0 NO-LOCK 
    BY debitor.betriebsnr BY debitor.artnr BY debitor.zahlkonto 
    BY debitor.rgdatum BY debitor.counter: 
      
    IF debitor.betriebsnr = 0 THEN 
    DO: 
        CREATE pay-list. 
        pay-list.ar-recid = RECID(debitor). 
    END. 
    ELSE 
    DO: 
        FIND FIRST pay-list WHERE pay-list.counter = debitor.betriebsnr 
            AND pay-list.artnr = debitor.artnr NO-ERROR. 
        FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK. 
        IF NOT AVAILABLE pay-list THEN 
        DO: 
            /* A/R article */ 
            add-info = ";&&3;" + STRING(debitor.artnr) + ";" 
              + STRING(debitor.betriebsnr). 
 
            CREATE pay-list. 
            ASSIGN 
              pay-list.counter = debitor.betriebsnr 
              pay-list.NAME = guest.NAME 
              pay-list.artnr = debitor.artnr 
              pay-list.add-info = add-info. 

            IF debitor.vesrcod NE "" THEN 
              pay-list.NAME = debitor.vesrcod + ";" + pay-list.NAME. 
        
        END. 
        pay-list.amount = pay-list.amount - debitor.saldo. 
        FIND FIRST pay-list WHERE pay-list.counter = debitor.betriebsnr 
            AND pay-list.zahlkonto = debitor.zahlkonto NO-ERROR. 
        IF NOT AVAILABLE pay-list THEN 
        DO: 
            /* A/R Payment article */ 
            add-info = ";&&4;" + STRING(debitor.artnr) + ";" 
              + STRING(debitor.betriebsnr) + ";" + STRING(debitor.zahlkonto). 
 
            CREATE pay-list. 
            ASSIGN 
              pay-list.counter = debitor.betriebsnr 
              pay-list.NAME = guest.NAME 
              pay-list.zahlkonto = debitor.zahlkonto 
              pay-list.add-info = add-info. 

            IF debitor.vesrcod NE "" THEN 
              pay-list.NAME = debitor.vesrcod + ";" + pay-list.NAME. 
        
        END. 
        pay-list.amount = pay-list.amount + debitor.saldo. 
    END. 
  END. 
 
  FOR EACH pay-list: 
      IF pay-list.counter = 0 THEN RUN step-three1. 
      ELSE IF pay-list.zahlkonto NE 0 THEN RUN step-three2(pay-list.zahlkonto). 
      ELSE IF pay-list.artnr NE 0 THEN RUN step-three2(pay-list.artnr). 
  END. 
  
  RUN adjust-lists.

  FOR EACH g-list NO-LOCK BY g-list.sysdate DESCENDING BY g-list.zeit DESCENDING:
    FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = g-list.fibukonto NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct1 THEN
    DO:
      CREATE buf-g-list.
      BUFFER-COPY g-list TO buf-g-list.
      ASSIGN
          buf-g-list.acct-fibukonto = gl-acct1.fibukonto
          buf-g-list.bezeich = gl-acct1.bezeich.
    END.                                        
  END.
END. 


PROCEDURE add-list: 
DEFINE INPUT PARAMETER create-it AS LOGICAL. 
DEFINE buffer gl-acc1 FOR gl-acct. 
FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fibukonto NO-LOCK. 
  curr-anz = curr-anz + 1. 
 
  IF create-it THEN 
  DO: 
    create g-list. 
    g-list.add-info = add-info. 
  END. 
 
  g-list.fibukonto = fibukonto. 
  g-list.rechnr = debitor.rechnr. 
  g-list.dept = debitor.betriebsnr. 
  IF debitor.vesrcod = "" THEN 
  g-list.bemerk = STRING(debitor.rechnr) + " - " + debitor.name. 
  ELSE g-list.bemerk = STRING(debitor.rechnr) + " - " + debit.vesrcod. 
  g-list.userinit = user-init. 
  g-list.zeit = time. 
  g-list.duplicate = NO. 
 
/*
  IF g-list.credit NE 0 AND debit-betrag NE 0 THEN 
  DO: 
      IF g-list.credit GE debit-betrag THEN 
          g-list.credit = g-list.credit - debit-betrag. 
      ELSE 
      DO: 
          g-list.debit = debit-betrag - g-list.credit. 
          g-list.credit = 0. 
      END. 
  END. 
  ELSE IF g-list.debit NE 0 AND credit-betrag NE 0 THEN 
  DO: 
      IF g-list.debit GE credit-betrag THEN 
          g-list.debit = g-list.debit - credit-betrag. 
      ELSE 
      DO: 
          g-list.credit = credit-betrag - g-list.debit. 
          g-list.debit = 0. 
      END. 
  END. 
  ELSE 
*/  
  DO: 
    g-list.debit = g-list.debit + debit-betrag. 
    g-list.credit = g-list.credit + credit-betrag. 
  END. 
 
  FIND FIRST s-list WHERE s-list.fibukonto = gl-acc1.fibukonto 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE s-list THEN 
  DO: 
    create s-list. 
    s-list.fibukonto = gl-acc1.fibukonto. 
    s-list.bezeich = gl-acc1.bezeich. 
  END. 
  s-list.credit = s-list.credit + credit-betrag. 
  s-list.debit = s-list.debit + debit-betrag. 
 
  credits = credits + credit-betrag. 
  debits = debits + debit-betrag. 
  remains = debits - credits. 
  debit-betrag = 0. 
  credit-betrag = 0. 
END. 


PROCEDURE step-three1: 
DEFINE buffer art1 FOR artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 
 
  FIND FIRST debitor WHERE RECID(debitor) = pay-list.ar-recid NO-LOCK. 
  DO: 
    /* A/R article */ 
    add-info = ";&&1;" + STRING(debitor.artnr) + ";" 
      + STRING(debitor.rechnr) + ";" + STRING(debitor.betriebsnr). 
 
    FIND FIRST art1 WHERE art1.artnr = debitor.artnr 
      AND art1.departement = 0 NO-LOCK. 
    FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = art1.fibukonto 
      NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-acc1 THEN 
    DO: 
      fibukonto = gl-acc1.fibukonto. /* COA OF debt article */ 
      IF debitor.saldo LT 0 THEN 
      DO: 
        credit-betrag = - debitor.saldo. 
        debit-betrag = 0. 
 
        FIND FIRST g-list WHERE g-list.fibukonto = gl-acc1.fibukonto 
          AND g-list.rechnr = debitor.rechnr 
          AND g-list.dept = debitor.betriebsnr NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
        ELSE RUN add-list(NO). 
      END. 
      ELSE IF debitor.saldo GT 0 THEN 
      DO: 
        debit-betrag = debitor.saldo. 
        credit-betrag = 0. 
 
        FIND FIRST g-list WHERE g-list.fibukonto = gl-acc1.fibukonto 
          AND g-list.rechnr = debitor.rechnr NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
        ELSE RUN add-list(NO). 
      END. 
    END. 
    ELSE 
    DO: 
      ASSIGN
        art-artnr   = art1.artnr
        art-bezeich = art1.bezeich
        acct-error  = 2
      . 
      RETURN. 
    END. 
 
    /* A/R Payment article */ 
    add-info = ";&&2;" + STRING(debitor.artnr) + ";" 
      + STRING(debitor.counter) + ";" + STRING(debitor.zahlkonto). 
 
    FIND FIRST artikel WHERE artikel.artnr = debitor.zahlkonto 
      AND artikel.departement = 0 NO-LOCK. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.fibukonto NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE gl-acct THEN 
    DO: 
      fibukonto = gl-acct.fibukonto.  /*COA OF A/R Payment article */ 
      IF debitor.saldo LE 0 THEN 
      DO: 
        debit-betrag = - debitor.saldo. 
        credit-betrag = 0. 
        RUN add-list(YES). 
      END. 
      ELSE IF debitor.saldo GT 0 THEN 
      DO: 
        credit-betrag = debitor.saldo. 
        debit-betrag = 0. 
        RUN add-list(YES). 
      END. 
    END. 
    ELSE 
    DO: 
      ASSIGN
        art-artnr   = artikel.artnr.
        art-bezeich = artikel.bezeich.
        acct-error  = 2
      . 
      RETURN. 
    END. 
  END. 
END. 
 
PROCEDURE step-three2: 
  DEF INPUT PARAMETER artnr AS INTEGER. 
    FIND FIRST artikel WHERE artikel.artnr = artnr 
    AND artikel.departement = 0 NO-LOCK. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.fibukonto NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE gl-acct THEN 
    DO: 
      fibukonto = gl-acct.fibukonto. 
      IF pay-list.amount LE 0 THEN 
      DO: 
        debit-betrag = - pay-list.amount. 
        credit-betrag = 0. 
        RUN add-listA. 
      END. 
      ELSE IF pay-list.amount GT 0 THEN 
      DO: 
        credit-betrag = pay-list.amount. 
        debit-betrag = 0. 
        RUN add-listA. 
      END. 
    END. 
    ELSE 
    DO: 
      ASSIGN
        art-artnr   = artikel.artnr
        art-bezeich = artikel.bezeich
        acct-error  = 2
      . 
      RETURN. 
    END. 
END. 


PROCEDURE add-listA: 
DEFINE buffer gl-acc1 FOR gl-acct. 
  FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = fibukonto NO-LOCK. 
  curr-anz = curr-anz + 1. 
 
  FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
      AND g-list.counter = pay-list.counter NO-ERROR. 
  IF NOT AVAILABLE g-list THEN 
  DO: 
    CREATE g-list. 
    g-list.fibukonto = fibukonto. 
    g-list.counter = pay-list.counter. 
    g-list.bemerk = pay-list.name. 
    g-list.userinit = user-init. 
    g-list.zeit = time. 
    g-list.duplicate = NO. 
    g-list.add-info = pay-list.add-info. 
  END. 
 
  IF g-list.credit NE 0 AND debit-betrag NE 0 THEN 
  DO: 
      IF g-list.credit GE debit-betrag THEN 
          g-list.credit = g-list.credit - debit-betrag. 
      ELSE 
      DO: 
          g-list.debit = debit-betrag - g-list.credit. 
          g-list.credit = 0. 
      END. 
  END. 
  ELSE IF g-list.debit NE 0 AND credit-betrag NE 0 THEN 
  DO: 
      IF g-list.debit GE credit-betrag THEN 
          g-list.debit = g-list.debit - credit-betrag. 
      ELSE 
      DO: 
          g-list.credit = credit-betrag - g-list.debit. 
          g-list.debit = 0. 
      END. 
  END. 
  ELSE 
  DO: 
    g-list.debit = g-list.debit + debit-betrag. 
    g-list.credit = g-list.credit + credit-betrag. 
  END. 
 
  FIND FIRST s-list WHERE s-list.fibukonto = gl-acc1.fibukonto 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE s-list THEN 
  DO: 
    create s-list. 
    s-list.fibukonto = gl-acc1.fibukonto. 
    s-list.bezeich = gl-acc1.bezeich. 
  END. 
  s-list.credit = s-list.credit + credit-betrag. 
  s-list.debit = s-list.debit + debit-betrag. 
 
  credits = credits + credit-betrag. 
  debits = debits + debit-betrag. 
  remains = debits - credits. 
  debit-betrag = 0. 
  credit-betrag = 0. 
END. 

