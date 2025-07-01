DEFINE TEMP-TABLE s-list 
  FIELD fibukonto   LIKE gl-acct.fibukonto 
  FIELD bezeich     AS CHAR FORMAT "x(28)" 
  FIELD credit      AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>9.99"  /*>>,>>>,>>>,>>9.99*/ /* Gerald 050320 [667796]*/
  FIELD debet       AS DECIMAL FORMAT "->>,>>>,>>>,>>>,>>9.99". /*>>,>>>,>>>,>>9.99*/ /* Gerald 050320 [667796]*/

DEFINE TEMP-TABLE g-list 
  FIELD  nr         AS INTEGER 
  FIELD  remark     AS CHAR 
  FIELD  docu-nr    AS CHAR 
  FIELD  lscheinnr  AS CHAR 
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
  FIELD  acct-fibukonto  LIKE gl-acct.fibukonto
  FIELD  bezeich    LIKE gl-acct.bezeich.
DEF TEMP-TABLE t-g-list LIKE g-list.

DEF INPUT PARAMETER pvILanguage     AS INTEGER NO-UNDO.
DEF INPUT PARAMETER from-date       AS DATE.
DEF INPUT PARAMETER to-date         AS DATE.
DEF INPUT PARAMETER fibukonto       AS CHAR.
DEF INPUT PARAMETER user-init       AS CHAR.
DEF INPUT PARAMETER refno           AS CHAR.

DEF OUTPUT PARAMETER acct-error     AS INTEGER INIT 0.
DEF OUTPUT PARAMETER credits        AS DECIMAL.
DEF OUTPUT PARAMETER debits         AS DECIMAL.
DEF OUTPUT PARAMETER remains        AS DECIMAL.
DEF OUTPUT PARAMETER curr-anz       AS INTEGER.
DEF OUTPUT PARAMETER msg-str        AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-g-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.

DEFINE VARIABLE curr-docu       AS CHAR. 
DEFINE VARIABLE curr-lschein    AS CHAR. 
DEFINE VARIABLE note            AS CHAR. 
DEFINE VARIABLE note1           AS CHAR. 
DEFINE VARIABLE add-note        AS CHAR. 
DEFINE VARIABLE curr-nr         AS INTEGER. 
DEFINE VARIABLE debit-betrag    AS DECIMAL FORMAT ">>>,>>>,>>9.99". 
DEFINE VARIABLE credit-betrag   AS DECIMAL FORMAT ">>>,>>>,>>9.99". 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkap".

FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = refno 
  AND gl-jouhdr.jtype = 4 NO-LOCK NO-ERROR. 
IF AVAILABLE gl-jouhdr THEN 
DO: 
  msg-str = translateExtended ("Reference number already exists.",lvCAREA,""). 
  acct-error = 1.
  RETURN.
END.

RUN step-two.
IF acct-error GT 0 THEN
DO:
  FOR EACH g-list:
      DELETE g-list.
  END.
  FOR EACH s-list:
      DELETE s-list.
  END.
  RETURN.
END.

RUN step-three.

PROCEDURE step-two: 
DEFINE VARIABLE ap-account  AS CHAR. 
DEFINE VARIABLE ap-other    AS CHAR. 
DEFINE VARIABLE ap-fa       AS CHAR.
DEFINE BUFFER art1    FOR artikel. 
DEFINE BUFFER gl-acc1 FOR gl-acct. 
DEFINE BUFFER g-list1 FOR g-list. 
DEFINE BUFFER ap-buff FOR l-kredit.

  FIND FIRST htparam WHERE htparam.paramnr = 986 no-lock.    /*AP Account-# */ 
  ap-account = htparam.fchar. 
 
  FIND FIRST htparam WHERE paramnr = 395 no-lock. /* AP Others AcctNo */ 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-acct THEN ap-other = gl-acct.fibukonto. 
  ELSE ap-other = ap-account. 

  FIND FIRST htparam WHERE paramnr = 887 no-lock. /*FA AP Account-# */
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar NO-LOCK NO-ERROR. 
  IF AVAILABLE gl-acct THEN ap-fa = gl-acct.fibukonto. 
  ELSE ap-fa = ap-account. 
  
  FOR EACH l-kredit WHERE l-kredit.rgdatum GE from-date 
    AND l-kredit.rgdatum LE to-date AND l-kredit.lief-nr GT 0 
    AND l-kredit.opart GT 0 AND l-kredit.zahlkonto GT 0 USE-INDEX liefnr_ix 
    NO-LOCK BY l-kredit.bemerk BY l-kredit.counter: 
    
    FIND FIRST ap-buff WHERE ap-buff.counter = l-kredit.counter
      AND ap-buff.zahlkonto = 0 NO-LOCK.
    IF ap-buff.betriebsnr = 0 THEN fibukonto = ap-account.
    ELSE IF ap-buff.betriebsnr = 1 THEN fibukonto = ap-other.
    ELSE IF ap-buff.betriebsnr = 2 THEN fibukonto = ap-fa.

    curr-docu = l-kredit.name. 
    curr-lschein = l-kredit.lscheinnr. 
    curr-nr = 1. 
    note = l-kredit.lscheinnr + " - " + l-kredit.bemerk. 
    note1 = l-kredit.bemerk + " - " + l-kredit.lscheinnr. 
    add-note = ";&&1;" + STRING(l-kredit.counter) + ";" + STRING(l-kredit.lief-nr). 
 
    IF l-kredit.saldo LT 0 THEN 
    DO: 
      debit-betrag = - l-kredit.saldo. 
      credit-betrag = 0. 
      FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
        AND g-list.docu-nr EQ l-kredit.name 
        AND g-list.lscheinnr EQ l-kredit.lscheinnr 
        AND g-list.debit NE 0 NO-ERROR. 
      IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
      ELSE RUN add-list(NO). 
    END. 
    ELSE IF l-kredit.saldo GT 0 THEN 
    DO: 
      credit-betrag = l-kredit.saldo. 
      debit-betrag = 0. 
      FIND FIRST g-list WHERE g-list.fibukonto = fibukonto 
        AND g-list.docu-nr EQ l-kredit.name 
        AND g-list.lscheinnr EQ l-kredit.lscheinnr 
        AND g-list.credit NE 0 NO-ERROR. 
      IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
      ELSE RUN add-list(NO). 
    END. 
 
    FIND FIRST artikel WHERE artikel.artnr = l-kredit.zahlkonto 
      AND artikel.departement = 0 NO-LOCK. 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = artikel.fibukonto NO-LOCK 
      NO-ERROR. 
    IF AVAILABLE gl-acct THEN 
    DO: 
      fibukonto = gl-acct.fibukonto. 
      curr-nr = 2. 
      note = l-kredit.bemerk. 
      note1 = l-kredit.bemerk + " - zz". 
      add-note = ";&&2;" + STRING(l-kredit.counter) + ";" + STRING(l-kredit.lief-nr) + ";" 
          + STRING(l-kredit.zahlkonto) + ";" + STRING(l-kredit.saldo * 100). 
      IF l-kredit.saldo LE 0 THEN 
      DO: 
        credit-betrag = - l-kredit.saldo. 
        debit-betrag = 0. 
        FIND FIRST g-list WHERE g-list.fibukonto = artikel.fibukonto 
        AND ENTRY(1, g-list.bemerk, ";&&") EQ note
        AND g-list.credit NE 0 NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
        ELSE RUN add-list(NO). 
      END. 
      ELSE IF l-kredit.saldo GT 0 THEN 
      DO: 
        debit-betrag = l-kredit.saldo. 
        credit-betrag = 0. 
        FIND FIRST g-list WHERE g-list.fibukonto = artikel.fibukonto 
        AND ENTRY(1, g-list.bemerk, ";&&") EQ note 
        AND g-list.debit NE 0 NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
        ELSE RUN add-list(NO). 
      END. 
    END. 
    ELSE 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Chart of Account not defined",lvCAREA,"")
              + CHR(10)
              + translateExtended ("ArticleNo",lvCAREA,"") + " " + STRING(artikel.artnr) + " - " + artikel.bezeich.
      acct-error = 2.
      RETURN.
    END. 
  END. 
 
  FOR EACH g-list WHERE g-list.nr = 1 AND g-list.credit GT 0: 
    FIND FIRST g-list1 WHERE g-list1.fibukonto = g-list.fibukonto 
      AND g-list.nr = 1 AND g-list1.lscheinnr = g-list.lscheinnr 
      AND (g-list1.debit GT g-list.credit) NO-ERROR. 
    IF AVAILABLE g-list1 THEN 
    DO: 
      g-list1.debit = g-list1.debit - g-list.credit. 
      credits = credits - g-list.credit. 
      debits = debits - g-list.credit. 
      delete g-list. 
    END. 
  END.
END. 

PROCEDURE add-list: 
DEFINE INPUT PARAMETER create-it AS LOGICAL. 
DEFINE BUFFER gl-acct1 FOR gl-acct. 
  FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = fibukonto NO-LOCK. 
  curr-anz = curr-anz + 1. 
  IF create-it THEN 
  DO: 
    create g-list. 
    g-list.fibukonto = fibukonto. 
    g-list.nr = curr-nr. 
    g-list.remark = note1. 
    g-list.bemerk = note + add-note. 
    g-list.docu-nr = curr-docu. 
    g-list.lscheinnr = curr-lschein. 
  END. 
  g-list.debit = g-list.debit + debit-betrag. 
  g-list.credit = g-list.credit + credit-betrag. 
  g-list.userinit = user-init. 
  g-list.zeit = time. 
  g-list.duplicate = NO. 
 
  FIND FIRST s-list WHERE s-list.fibukonto = gl-acct1.fibukonto 
    NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE s-list THEN 
  DO: 
    create s-list. 
    s-list.fibukonto = gl-acct1.fibukonto. 
    s-list.bezeich = gl-acct1.bezeich. 
  END. 
  s-list.credit = s-list.credit + credit-betrag. 
  s-list.debet = s-list.debet + debit-betrag. 
 
  credits = credits + credit-betrag. 
  debits = debits + debit-betrag. 
  remains = debits - credits. 
  debit-betrag = 0. 
  credit-betrag = 0. 
END. 

PROCEDURE step-three:
DEFINE BUFFER gl-acct1 FOR gl-acct.
  FOR EACH g-list NO-LOCK, 
      FIRST gl-acct1 WHERE gl-acct1.fibukonto = g-list.fibukonto NO-LOCK 
      BY g-list.remark BY g-list.nr:
      CREATE t-g-list.
      BUFFER-COPY g-list TO t-g-list.
      ASSIGN
        t-g-list.acct-fibukonto  = gl-acct1.fibukonto
        t-g-list.bezeich    = gl-acct1.bezeich.
  END.
END. 
