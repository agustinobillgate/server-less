
DEF TEMP-TABLE s-list 
    FIELD fibukonto LIKE gl-acct.fibukonto INITIAL "000000000000" 
    FIELD debit     LIKE gl-journal.debit 
    FIELD credit    LIKE gl-journal.credit
    FIELD flag      AS LOGICAL INIT NO
    FIELD bezeich   LIKE gl-acct.bezeich
    FIELD remark    AS CHARACTER. /*FD Sept 29, 2022 => Ticket No 506FA2 - Input remark per COA*/

DEF INPUT-OUTPUT  PARAMETER TABLE FOR s-list.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER invoice        AS CHAR.
DEF INPUT  PARAMETER journ-flag     AS LOGICAL.
DEF INPUT  PARAMETER balance        AS DECIMAL.
DEF INPUT  PARAMETER avail-sbuff    AS LOGICAL.
DEF INPUT  PARAMETER docu-nr        AS CHAR.
DEF INPUT  PARAMETER rgdatum        AS DATE.
DEF INPUT  PARAMETER lief-nr        AS INT.
DEF INPUT  PARAMETER disc           AS DECIMAL.
DEF INPUT  PARAMETER saldo          AS DECIMAL.
DEF INPUT  PARAMETER d-amount       AS DECIMAL.
DEF INPUT  PARAMETER ziel           AS INT.
DEF INPUT  PARAMETER nr             AS INT.
DEF INPUT  PARAMETER comments       AS CHAR.
DEF INPUT  PARAMETER netto          AS DECIMAL.
DEF INPUT  PARAMETER userinit       AS CHAR.
DEF INPUT  PARAMETER ap-other       AS CHAR.
DEF INPUT  PARAMETER user-init      AS CHAR.
DEF INPUT  PARAMETER firma          AS CHAR.

DEF INPUT  PARAMETER s-list-fibukonto AS CHAR.
DEF INPUT  PARAMETER s-list-debit     AS DECIMAL.
DEF INPUT  PARAMETER tax-code         AS CHAR NO-UNDO.
DEF INPUT  PARAMETER tax-amt          AS CHAR NO-UNDO.

DEF OUTPUT PARAMETER msg-str  AS CHAR.
DEF OUTPUT PARAMETER fl-code  AS INT INIT 0.
DEF OUTPUT PARAMETER avail-gl AS LOGICAL INIT YES.

DEF VARIABLE return-flag AS LOGICAL INIT NO NO-UNDO.

DEF BUFFER sbuff FOR s-list.

{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "mk-ap".

FOR EACH s-list:
    IF s-list.debit NE 0 THEN 
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = s-list.fibukonto NO-LOCK NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN avail-gl = NO.
    END.
    IF DECIMAL(s-list.fibukonto) NE 0 THEN
    DO:
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = s-list.fibukonto NO-LOCK NO-ERROR.
        IF NOT AVAILABLE gl-acct THEN avail-gl = NO.
    END.
    IF NOT avail-gl THEN 
    DO:
      ASSIGN
        s-list.flag = YES
        return-flag = YES
       .
      LEAVE.
    END.
END.

IF return-flag THEN RETURN.

FIND FIRST l-op WHERE l-op.op-art = 1 AND l-op.loeschflag LE 1 
      AND l-op.lscheinnr = invoice NO-LOCK NO-ERROR. 
IF AVAILABLE l-op THEN 
DO: 
  msg-str = msg-str + CHR(2)
          + translateExtended ("Same Delivery No exists in Receiving Record, date =",lvCAREA,"")
          + " " + STRING(l-op.datum) + " - " + l-op.docu-nr.
  fl-code = 1.
  /*MTAPPLY "entry" TO invoice. */
  RETURN NO-APPLY. 
END. 
 
IF journ-flag THEN 
DO: 
    DEF VAR gl-close-month AS DATE NO-UNDO.
    IF balance NE 0 THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Journal Transaction NOT balanced.",lvCAREA,"").
      fl-code = 2.
      /*MTAPPLY "entry" TO b1. */
      RETURN NO-APPLY.      
    END. 

    IF NOT avail-sbuff THEN
    DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Journal record NOT found.",lvCAREA,"").
        fl-code = 3.
        /*MTAPPLY "entry" TO b1.*/
        RETURN NO-APPLY.      
    END.

    FIND FIRST gl-jouhdr WHERE gl-jouhdr.refno = docu-nr NO-LOCK NO-ERROR. 
    IF AVAILABLE gl-jouhdr THEN 
    DO: 
      msg-str = msg-str + CHR(2)
              + translateExtended ("Same G/L RefNo exists, date =",lvCAREA,"")
              + " " + STRING(gl-jouhdr.datum).
      fl-code = 4.
      /*MTAPPLY "entry" TO docu-nr. */
      RETURN NO-APPLY. 
    END. 
    FIND FIRST htparam WHERE htparam.paramnr = 558 NO-LOCK. /*last GL closeDate*/
    IF rgdatum LE htparam.fdate THEN
    DO:
      msg-str = msg-str + CHR(2)
              + translateExtended ("A/P transaction date too old.",lvCAREA,"").
      fl-code = 5.
      /*MTAPPLY "entry" TO rgdatum. */
      RETURN NO-APPLY. 
    END.
END. 
ELSE 
DO: 
  DEF VAR ch AS CHAR INITIAL "". 
    FIND FIRST l-kredit WHERE l-kredit.lief-nr NE lief-nr 
        AND l-kredit.NAME = docu-nr AND l-kredit.zahlkonto = 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-kredit THEN 
    DO: 
      FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = lief-nr NO-LOCK 
        NO-ERROR. 
      IF AVAILABLE l-lieferant THEN ch = l-lieferant.firma. 
      msg-str = msg-str + CHR(2)
              + translateExtended ("A/P with same RefNo exists:",lvCAREA,"")
              + " " + STRING(l-kredit.rgdatum)  + " " + ch.
      fl-code = 6.
      /*MTAPPLY "entry" TO docu-nr. */
      RETURN NO-APPLY. 
    END. 
END. 
 
IF netto NE 0 THEN 
DO TRANSACTION: 
    IF tax-code NE " " THEN DO:
        IF tax-amt NE " " THEN
            comments = comments + ";" + tax-code + ";" + tax-amt.
        ELSE comments = comments + ";" + tax-code.
    END.

    CREATE l-kredit. 
    ASSIGN 
      l-kredit.name = docu-nr 
      l-kredit.lief-nr = lief-nr 
      l-kredit.lscheinnr = invoice 
      l-kredit.rgdatum = rgdatum 
      l-kredit.datum = ? 
      l-kredit.saldo = saldo 
      l-kredit.rabatt = disc 
      l-kredit.rabattbetrag = d-amount 
      l-kredit.ziel = ziel 
      l-kredit.netto = netto 
      l-kredit.bediener-nr = nr 
      l-kredit.bemerk = comments
      l-kredit.steuercode = 1 
      l-kredit.betriebsnr = INTEGER(journ-flag) 
    . 
 
    CREATE ap-journal. 
    ASSIGN 
      ap-journal.lief-nr = lief-nr 
      ap-journal.docu-nr = docu-nr 
      ap-journal.lscheinnr = invoice 
      ap-journal.rgdatum = rgdatum 
      ap-journal.saldo = saldo 
      ap-journal.netto = netto 
      ap-journal.userinit = userinit
      ap-journal.zeit = TIME 
      ap-journal.betriebsnr = INTEGER(journ-flag) 
    . 
 
    IF journ-flag THEN 
    DO:
      FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE counters THEN 
      DO: 
        create counters. 
        counters.counter-no = 25. 
        counters.counter-bez = translateExtended ("G/L Transaction Journal",lvCAREA,""). 
      END. 
      counters.counter = counters.counter + 1. 
      FIND CURRENT counter NO-LOCK. 
      CREATE gl-jouhdr. 
      ASSIGN 
        gl-jouhdr.jnr = counters.counter 
        gl-jouhdr.refno = docu-nr 
        gl-jouhdr.datum = rgdatum 
        gl-jouhdr.bezeich = firma 
        gl-jouhdr.batch = YES 
        gl-jouhdr.jtype = 4 
      . 
      
      CREATE gl-journal. 
      ASSIGN 
        gl-journal.jnr = gl-jouhdr.jnr 
        gl-journal.fibukonto = ap-other 
        gl-journal.userinit = user-init 
        gl-journal.zeit = TIME 
        gl-journal.bemerk = invoice 
      . 
      
      IF netto GT 0 THEN gl-journal.credit = netto. 
      ELSE gl-journal.debit = - netto. 
      IF l-kredit.bemerk NE "" THEN DO:
          IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN
              gl-journal.bemerk = gl-journal.bemerk + " - " + ENTRY(1, l-kredit.bemerk, ";").
          ELSE gl-journal.bemerk = gl-journal.bemerk + " - " + l-kredit.bemerk. 
      END.
 
      gl-jouhdr.credit = gl-jouhdr.credit + gl-journal.credit. 
      gl-jouhdr.debit = gl-jouhdr.debit + gl-journal.debit. 
 
      FOR EACH sbuff WHERE DECIMAL(sbuff.fibukonto) NE 0: 
        CREATE gl-journal. 
        ASSIGN 
          gl-journal.jnr = gl-jouhdr.jnr 
          gl-journal.fibukonto = sbuff.fibukonto 
          gl-journal.userinit = user-init 
          gl-journal.zeit = TIME 
          /*gl-journal.bemerk = invoice */
          gl-journal.bemerk = sbuff.remark
          gl-journal.debit = sbuff.debit 
          gl-journal.credit = sbuff.credit 
        . 
        /* FD Comment Sept 29, 2022
        IF l-kredit.bemerk NE "" THEN DO:
              IF NUM-ENTRIES(l-kredit.bemerk, ";") GT 1 THEN
                  gl-journal.bemerk = gl-journal.bemerk + " - " + ENTRY(1, l-kredit.bemerk, ";").
              ELSE gl-journal.bemerk = gl-journal.bemerk + " - " + l-kredit.bemerk. 
        END.
        */
        gl-jouhdr.credit = gl-jouhdr.credit + gl-journal.credit. 
        gl-jouhdr.debit = gl-jouhdr.debit + gl-journal.debit. 
 
        FIND CURRENT gl-journal NO-LOCK. 
 
      END. 
      FIND CURRENT gl-jouhdr NO-LOCK. 
      
    END. 
END. 
