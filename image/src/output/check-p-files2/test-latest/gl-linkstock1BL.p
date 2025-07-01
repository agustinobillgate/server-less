
DEFINE TEMP-TABLE g-list 
  FIELD docu-nr     AS CHAR 
  FIELD lscheinnr   AS CHAR 
  FIELD jnr         LIKE gl-journal.jnr 
  FIELD fibukonto   LIKE gl-journal.fibukonto 
  FIELD debit       LIKE gl-journal.debit 
  FIELD credit      LIKE gl-journal.credit 
  FIELD bemerk      AS CHAR FORMAT "x(50)" 
  FIELD userinit    LIKE gl-journal.userinit 
  FIELD sysdate     LIKE gl-journal.sysdate INITIAL today 
  FIELD zeit        LIKE gl-journal.zeit 
  FIELD chginit     LIKE gl-journal.chginit 
  FIELD chgdate     LIKE gl-journal.chgdate INITIAL ? 
  FIELD add-note    AS CHAR 
  FIELD duplicate   AS LOGICAL INITIAL YES
  FIELD acct-fibukonto LIKE gl-acct.fibukonto
  FIELD bezeich     LIKE gl-acct.bezeich.
DEFINE TEMP-TABLE t-g-list LIKE g-list.
DEFINE TEMP-TABLE s-list 
  FIELD nr      AS INTEGER 
  FIELD name    AS CHAR FORMAT "x(30)" 
  FIELD debit   AS DECIMAL FORMAT ">>>,>>>,>>9.99" 
  FIELD credit  AS DECIMAL FORMAT ">>>,>>>,>>9.99". 

DEF INPUT PARAMETER pvILanguage    AS INTEGER      NO-UNDO.
DEF INPUT PARAMETER link-out  AS LOGICAL.
DEF INPUT PARAMETER link-in   AS LOGICAL.
DEF INPUT PARAMETER from-grp  AS INTEGER.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date   AS DATE.
DEF INPUT PARAMETER user-init AS CHAR.

DEF OUTPUT PARAMETER curr-anz AS INTEGER INIT 0.
DEF OUTPUT PARAMETER credits  AS DECIMAL.
DEF OUTPUT PARAMETER debits   AS DECIMAL.
DEF OUTPUT PARAMETER remains  AS DECIMAL.
DEF OUTPUT PARAMETER msg-str  AS CHAR.
DEF OUTPUT PARAMETER msg-str2 AS CHAR.
DEF OUTPUT PARAMETER msg-str3 AS CHAR.
DEF OUTPUT PARAMETER msg-str4 AS CHAR.
DEF OUTPUT PARAMETER msg-str5 AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-g-list.
DEF OUTPUT PARAMETER TABLE FOR s-list.

DEFINE VARIABLE curr-zeit       AS INTEGER INITIAL 0 NO-UNDO.
DEFINE VARIABLE curr-lschein    AS CHAR.
DEFINE VARIABLE curr-note       AS CHAR.
DEFINE VARIABLE add-note        AS CHAR.
DEFINE VARIABLE fibukonto       AS CHAR. 
DEFINE VARIABLE debit-betrag    AS DECIMAL. 
DEFINE VARIABLE credit-betrag   AS DECIMAL. 

/* Malik */
DEFINE VAR tot-credit AS DECIMAL.
DEFINE VAR tot-debit AS DECIMAL.
DEFINE VAR counter AS DECIMAL. 

DEFINE buffer gl-acct1 FOR gl-acct.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "gl-linkstock".

IF link-out THEN 
DO: 
  IF from-grp = 0 THEN RUN step-two. 
  ELSE RUN step-two1. 
  IF from-grp LE 1 THEN RUN step-two2. 
END. 
ELSE IF link-in THEN 
DO: 
  RUN step-three. 
  credits = 0.
  debits = 0.
  /*FDL - Ticket 8DA193*/
  FOR EACH g-list NO-LOCK:
      g-list.debit = ROUND(g-list.debit,2).
      g-list.credit = ROUND(g-list.credit,2).
      /*FDL Jan 07, 2025: FF039B*/
      credits = credits + g-list.credit. 
      debits = debits + g-list.debit.
  END.
  remains = debits - credits.

  /* Fixed Asset License */ 
  FIND FIRST htparam WHERE paramnr = 329 NO-LOCK. 
  IF htparam.flogical = YES THEN RUN step-three-FA. 
END. 

FOR EACH g-list NO-LOCK,
    FIRST gl-acct1 WHERE gl-acct1.fibukonto = g-list.fibukonto NO-LOCK 
    BY g-list.zeit BY SUBSTR(g-list.bemerk,1,24) BY gl-acct1.fibukonto:
    CREATE t-g-list.
    BUFFER-COPY g-list TO t-g-list.
    ASSIGN
        t-g-list.acct-fibukonto = gl-acct1.fibukonto
        t-g-list.bezeich        = gl-acct1.bezeich.
END.

PROCEDURE step-two: 
DEFINE buffer art1 FOR artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 
DEFINE buffer gl-acc2 FOR gl-acct. 
DEFINE BUFFER bqueasy FOR queasy.
DEFINE VARIABLE cost-account AS CHAR. 
DEFINE VARIABLE cost-value AS DECIMAL. 
DEFINE VARIABLE do-it AS LOGICAL. 
 
  curr-zeit = TIME. 
  FOR EACH l-op WHERE l-op.pos GT 0 AND l-op.op-art = 3 AND l-op.loeschflag LT 2 
    AND l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.lager-nr GT 0 NO-LOCK, 
    FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
    AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-op.datum BY l-op.lscheinnr: 
 
    IF l-op.stornogrund NE "" THEN 
      FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
        NO-LOCK NO-ERROR. 
    ELSE FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-ophdr.fibukonto 
      NO-LOCK NO-ERROR. 
    do-it = AVAILABLE gl-acct1. 
 
    cost-value = 0. 
    IF do-it THEN 
    DO: 
      curr-zeit = curr-zeit + 1. 
      curr-lschein = l-ophdr.lscheinnr. 
      curr-note = STRING(l-ophdr.lager-nr,"99") + "-" + curr-lschein 
        + " " + l-artikel.bezeich. 
      add-note = ";&&5;" + STRING(l-ophdr.lager-nr,"99") + ";" 
        + curr-lschein + ";". 
      cost-account = gl-acct1.fibukonto. 
 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE gl-acct THEN 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-artikel.fibukonto 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct THEN 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-value = cost-value + round(l-op.warenwert, 2). 
        IF l-op.warenwert GT 0 THEN 
        DO: 
          credit-betrag = round(l-op.warenwert,2). 
          debit-betrag = 0. 
          FIND FIRST g-list WHERE g-list.fibukonto = gl-acct.fibukonto 
            AND g-list.lscheinnr EQ l-op.lscheinnr 
            AND g-list.credit NE 0 NO-ERROR. 
          IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
          ELSE RUN add-list(YES). 
        END. 
        ELSE IF l-op.warenwert LT 0 THEN 
        DO: 
          debit-betrag = - round(l-op.warenwert, 2). 
          credit-betrag = 0. 
          FIND FIRST g-list WHERE g-list.fibukonto = gl-acct.fibukonto 
            AND g-list.lscheinnr EQ l-op.lscheinnr 
            AND g-list.debit NE 0 NO-ERROR. 
          IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
          ELSE RUN add-list(YES). 
        END. 
      END. 
      ELSE 
      DO:
        msg-str = msg-str + CHR(2)
                + translateExtended ("Chart of Account not defined at stock article",lvCAREA,"")
                + CHR(10)
                + translateExtended ("ArticleNo",lvCAREA,"") + " " + STRING(l-artikel.artnr) + " - " + l-artikel.bezeich.
      END.
    END. 

    IF cost-value NE 0 THEN 
    DO: 
      curr-zeit = curr-zeit + 1. 
      fibukonto = cost-account. 
      curr-lschein = l-ophdr.lscheinnr. 
      curr-note = STRING(l-ophdr.lager-nr,"99") + " - " + curr-lschein. 
      add-note = ";&&5;" + STRING(l-ophdr.lager-nr,"99") + ";" 
        + curr-lschein + ";". 
      IF cost-value GT 0 THEN 
      DO: 
        debit-betrag = cost-value. 
        credit-betrag = 0. 
        FIND FIRST g-list WHERE g-list.fibukonto = cost-account 
          AND g-list.lscheinnr EQ l-op.lscheinnr 
          AND g-list.debit NE 0 NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
        ELSE RUN add-list(NO). 
      END. 
      ELSE IF cost-value LT 0 THEN 
      DO: 
        credit-betrag = - cost-value. 
        debit-betrag = 0. 
        FIND FIRST g-list WHERE g-list.fibukonto = cost-account 
          AND g-list.lscheinnr EQ l-op.lscheinnr 
          AND g-list.credit NE 0 NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
        ELSE RUN add-list(NO). 
      END. 
    END. 
  END. 
END. 


PROCEDURE step-two1: 
DEFINE buffer art1 FOR artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 
DEFINE VARIABLE cost-account AS CHAR. 
DEFINE VARIABLE cost-value AS DECIMAL. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE s AS DECIMAL. 
  create s-list. 
    s-list.nr = 1. 
    s-list.name = "INVENTORY". 
  create s-list. 
    s-list.nr = 2. 
    s-list.name = "EXPENSES". 
 
  curr-zeit = TIME. 
  FOR EACH l-op WHERE l-op.pos GT 0 AND l-op.op-art = 3 AND l-op.loeschflag LT 2 
    AND l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.lager-nr GT 0 NO-LOCK, 
    FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
    AND l-ophdr.op-typ = "STT" AND l-ophdr.fibukonto NE "" NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr 
    AND l-artikel.endkum = from-grp NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-op.datum BY l-op.lscheinnr: 
 
    IF l-op.stornogrund NE "" THEN 
      FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
      NO-LOCK NO-ERROR. 
    ELSE FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-ophdr.fibukonto 
      NO-LOCK NO-ERROR. 
    do-it = AVAILABLE gl-acct1. 
 
    cost-value = 0. 
    IF do-it THEN 
    DO: 
      curr-zeit = curr-zeit + 1. 
      curr-lschein = l-ophdr.lscheinnr. 
      curr-note = STRING(l-ophdr.lager-nr,"99") + "-" + curr-lschein 
        + " " + l-artikel.bezeich. 
      add-note = ";&&5;" + STRING(l-ophdr.lager-nr,"99") + ";" 
        + curr-lschein + ";". 
      cost-account = gl-acct1.fibukonto. 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE gl-acct THEN 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-artikel.fibukonto 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct THEN 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        cost-value = cost-value + round(l-op.warenwert, 2). 
        s = s + l-op.warenwert. 
        IF l-op.warenwert GT 0 THEN 
        DO: 
          credit-betrag = round(l-op.warenwert, 2). 
          debit-betrag = 0. 
          FIND FIRST g-list WHERE g-list.fibukonto = gl-acct.fibukonto 
            AND g-list.lscheinnr EQ l-op.lscheinnr 
            AND g-list.credit NE 0 NO-ERROR. 
          IF NOT AVAILABLE g-list THEN RUN add-list1(YES, 1). 
          ELSE RUN add-list1(YES, 1). 
        END. 
        ELSE IF l-op.warenwert LT 0 THEN 
        DO: 
          debit-betrag = - round(l-op.warenwert, 2). 
          credit-betrag = 0. 
          FIND FIRST g-list WHERE g-list.fibukonto = gl-acct.fibukonto 
            AND g-list.lscheinnr EQ l-op.lscheinnr 
            AND g-list.debit NE 0 NO-ERROR. 
          IF NOT AVAILABLE g-list THEN RUN add-list1(YES, 1). 
          ELSE RUN add-list1(YES, 1). 
        END. 
      END. 
      ELSE 
      DO: 
        msg-str2 = msg-str2 + CHR(2)
                 + translateExtended ("Chart of Account not defined at stock article",lvCAREA,"")
                 + CHR(10)
                 + translateExtended ("ArticleNo",lvCAREA,"") + " " + STRING(l-artikel.artnr) + " - " + l-artikel.bezeich.
      END. 
    END. 

    IF cost-value NE 0 THEN 
    DO: 
      curr-zeit = curr-zeit + 1. 
      fibukonto = cost-account. 
      curr-lschein = l-ophdr.lscheinnr. 
      curr-note = STRING(l-ophdr.lager-nr,"99") + " - " + curr-lschein. 
      add-note = ";&&5;" + STRING(l-ophdr.lager-nr,"99") + ";" 
        + curr-lschein + ";". 
      IF cost-value GT 0 THEN 
      DO: 
        debit-betrag = cost-value. 
        credit-betrag = 0. 
        FIND FIRST g-list WHERE g-list.fibukonto = cost-account 
          AND g-list.lscheinnr EQ l-op.lscheinnr 
          AND g-list.debit NE 0 NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list1(YES, 2). 
        ELSE RUN add-list1(NO, 2). 
      END. 
      ELSE IF cost-value LT 0 THEN 
      DO: 
        credit-betrag = - cost-value. 
        debit-betrag = 0. 
        FIND FIRST g-list WHERE g-list.fibukonto = cost-account 
          AND g-list.lscheinnr EQ l-op.lscheinnr 
          AND g-list.credit NE 0 NO-ERROR. 
        IF NOT AVAILABLE g-list THEN RUN add-list1(YES, 2). 
        ELSE RUN add-list1(NO, 2). 
      END. 
    END. 
  END. 
END. 


PROCEDURE step-two2: 
DEFINE buffer art1 FOR artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 
DEFINE VARIABLE cost-value AS DECIMAL. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE s AS DECIMAL. 
DEFINE VARIABLE wip-acct AS CHAR INITIAL "". 
 
  FIND FIRST l-op WHERE l-op.op-art = 2 AND l-op.loeschflag LT 2 
    AND l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.lager-nr GT 0 AND l-op.herkunftflag = 3 NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE l-op THEN RETURN. 
 
  create s-list. 
    s-list.nr = 3. 
    s-list.name = "TRANSFORM OUT". 
  create s-list. 
    s-list.nr = 4. 
    s-list.name = "TRANSFORM IN". 
 
  cost-value = 0. 
  curr-zeit = TIME. 
  FOR EACH l-op WHERE l-op.op-art GE 2 
    AND l-op.op-art LE 4 AND l-op.herkunftflag = 3 AND l-op.loeschflag LT 2 
    AND l-op.datum GE from-date AND l-op.datum LE to-date 
    AND l-op.lager-nr GT 0 NO-LOCK, 
    FIRST l-ophdr WHERE l-ophdr.lscheinnr = l-op.lscheinnr 
    AND l-ophdr.op-typ = "STT" NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-op.datum BY l-op.lscheinnr BY l-op.op-art descending: 
 
    IF wip-acct = "" THEN 
    DO: 
      FIND FIRST gl-acct1 WHERE gl-acct1.fibukonto = l-op.stornogrund 
        NO-LOCK NO-ERROR. 
      do-it = AVAILABLE gl-acct1. 
      IF NOT do-it THEN 
      DO:
        msg-str3 = msg-str3 + CHR(2)
                 + translateExtended ("No G/L WIP Account number found :",lvCAREA,"") + " " + l-op.lscheinnr.
        RETURN. 
      END. 
    END. 
    wip-acct = gl-acct1.fibukonto. 
 
    IF do-it THEN 
    DO: 
      curr-lschein = l-ophdr.lscheinnr. 
      curr-note = STRING(l-ophdr.lager-nr,"99") + " - " + curr-lschein. 
      add-note = ";&&6;" + STRING(l-ophdr.lager-nr,"99") + ";" 
        + curr-lschein + ";". 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto 
        NO-LOCK NO-ERROR. 
      IF NOT AVAILABLE gl-acct THEN 
        FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-artikel.fibukonto 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acct THEN 
      DO: 
        fibukonto = gl-acct.fibukonto. 
        s = s + l-op.warenwert. 
        IF l-op.op-art = 4 THEN 
        DO: 
          credit-betrag = round(l-op.warenwert, 2). 
          debit-betrag = 0. 
          FIND FIRST g-list WHERE g-list.fibukonto = gl-acct.fibukonto 
            AND g-list.lscheinnr EQ l-op.lscheinnr 
            AND g-list.credit NE 0 NO-ERROR. 
          IF NOT AVAILABLE g-list THEN 
          DO: 
            curr-zeit = curr-zeit + 1. 
            RUN add-list1(YES, 3). 
          END. 
          ELSE RUN add-list1(NO, 3). 
        END. 
        ELSE IF l-op.op-art = 2 THEN 
        DO: 
          curr-note = STRING(l-ophdr.lager-nr,"99") + " - " + l-artikel.bezeich. 
          add-note = ";&&6;" + STRING(l-ophdr.lager-nr,"99") + ";" 
            + curr-lschein + ";". 
          cost-value = cost-value + round(l-op.warenwert, 2). 
          debit-betrag = round(l-op.warenwert, 2). 
          credit-betrag = 0. 
          RUN add-list1(YES, 4). 
        END. 
      END. 
      ELSE 
      DO: 
        msg-str4 = msg-str4 + CHR(2)
                 + translateExtended ("Chart of Account not defined at stock article",lvCAREA,"") 
                 + CHR(10)
                 + translateExtended ("ArticleNo",lvCAREA,"") + " " + STRING(l-artikel.artnr) + " - " + l-artikel.bezeich.
      END.       
    END. 
  END. 
  IF cost-value GT 0 THEN 
  DO: 
    curr-zeit = curr-zeit + 1. 
    fibukonto = wip-acct. 
    curr-lschein = "". 
    curr-note = "WIP Transform IN". 
    debit-betrag = cost-value. 
    credit-betrag = 0. 
    RUN add-list1(YES, 0). 
    curr-note = "WIP Transform OUT". 
    credit-betrag = cost-value. 
    debit-betrag = 0. 
    RUN add-list1(YES, 0). 
  END. 
END. 


PROCEDURE step-three:   /* Receiving <--> A/P*/ 
DEFINE buffer art1 FOR artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 
DEFINE VARIABLE ap-account AS CHAR. 
DEFINE VARIABLE ratio AS DECIMAL. 
DEFINE VARIABLE note AS CHAR. 
DEFINE VARIABLE curr-docu AS CHAR. 
DEFINE VARIABLE curr-lschein AS CHAR. 
DEFINE VARIABLE op-exist AS LOGICAL. 
DEFINE VARIABLE tot-wert AS DECIMAL INITIAL 0. 
DEFINE VARIABLE do-it AS LOGICAL. 
DEFINE VARIABLE tot-vat AS DECIMAL INITIAL 0.
/* Naufal Afthar - A7E79D */
DEFINE VARIABLE curr-bezeich AS CHARACTER.
DEFINE VARIABLE curr-firma AS CHARACTER.
DEFINE VARIABLE counter AS INTEGER INITIAL 0. /* keep track num of credits*/

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER gl-acc2 FOR gl-acct. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 986 no-lock.    /*AP Account-# */ 
  ap-account = htparam.fchar. 
 
  op-exist = NO. 
  curr-lschein = "". 
  curr-zeit = TIME. 
  FOR EACH l-op WHERE l-op.pos GT 0 AND l-op.anzahl NE 0 
    AND l-op.op-art = 1 AND l-op.loeschflag LT 2 
    AND l-op.datum GE from-date AND l-op.datum LE to-date NO-LOCK, 
    FIRST l-artikel WHERE l-artikel.artnr = l-op.artnr NO-LOCK, 
    FIRST l-untergrup WHERE l-untergrup.zwkum = l-artikel.zwkum NO-LOCK 
    BY l-op.lscheinnr BY l-op.lief-nr: 
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-untergrup.fibukonto 
      NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE gl-acct THEN 
      FIND FIRST gl-acct WHERE gl-acct.fibukonto = l-artikel.fibukonto 
      NO-LOCK NO-ERROR.
    IF AVAILABLE gl-acct THEN
    DO:
        curr-zeit = curr-zeit + 1. 

        IF curr-lschein = "" THEN 
        DO: 
          curr-lschein = l-op.lscheinnr. 
          FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
            NO-ERROR. 
          IF NOT AVAILABLE l-lieferant THEN FIND FIRST l-kredit WHERE 
            l-kredit.lscheinnr = l-op.lscheinnr NO-LOCK NO-ERROR. 
        END. 

        IF curr-lschein NE l-op.lscheinnr THEN 
        DO: 
          /* Naufal Afthar - A7E79D */
          IF AVAILABLE l-lieferant THEN
          DO:  
              IF counter LE 1 THEN /* case credit = 1 */
                  curr-note = curr-lschein + " - " + curr-bezeich + "; " + l-lieferant.firma.
              ELSE 
                  curr-note = curr-lschein + " - " + l-lieferant.firma.
              counter = 0.
          END.
          ELSE
          DO: 
              /* Naufal Afthar - A7E79D */
              IF counter LE 1 THEN /* case credit = 1 */
                  curr-note = curr-lschein + " - " + curr-bezeich + "; " + curr-firma.
              ELSE 
                  curr-note = curr-lschein + " - " + curr-firma.
              counter = 0.
          END.
          /* Naufal Afthar - A7E79D */

          do-it = YES. 
          IF AVAILABLE l-lieferant AND l-lieferant.z-code NE "" THEN 
          DO: 
            FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-lieferant.z-code 
              NO-LOCK NO-ERROR. 
            IF AVAILABLE gl-acc1 THEN do-it = (gl-acc1.fibukonto EQ ap-account). 
          END. 

          IF NOT do-it THEN 
          DO: 
            fibukonto = gl-acc1.fibukonto. 
            IF tot-wert GT 0 THEN 
            DO: 
              credit-betrag = tot-wert. 
              debit-betrag = 0. 
              RUN add-list(YES). 
            END. 
            ELSE IF tot-wert LT 0 THEN 
            DO: 
              debit-betrag = - tot-wert. 
              credit-betrag = 0. 
              RUN add-list(YES). 
            END. 
          END. 
          ELSE 
          DO: 
            fibukonto = ap-account. 
            FOR EACH l-kredit WHERE 
              l-kredit.rgdatum GE from-date AND l-kredit.rgdatum LE to-date 
              AND l-kredit.lscheinnr = curr-lschein 
              AND l-kredit.opart GE 0 AND l-kredit.zahlkonto EQ 0 
              AND l-kredit.saldo NE 0 NO-LOCK: 
              ratio = l-kredit.netto / l-kredit.saldo. 
              IF l-kredit.netto GE 0 THEN 
              DO: 
                credit-betrag = l-kredit.netto. 
                debit-betrag = 0. 
                RUN add-list(YES). 
              END. 
              ELSE IF l-kredit.netto LT 0 THEN 
              DO: 
                debit-betrag = - l-kredit.netto. 
                credit-betrag = 0. 
                RUN add-list(YES). 
              END. 
            END. 
          END. 
          FIND FIRST l-lieferant WHERE l-lieferant.lief-nr = l-op.lief-nr NO-LOCK 
            NO-ERROR. 
          IF NOT AVAILABLE l-lieferant THEN FIND FIRST l-kredit WHERE 
            l-kredit.lscheinnr = l-op.lscheinnr NO-LOCK NO-ERROR. 
          curr-lschein = l-op.lscheinnr. 
          op-exist = NO. 
          tot-wert = 0.
          tot-vat = 0. 
        END. 

        IF AVAILABLE l-lieferant THEN 
        DO: 
          /* Naufal Afthar - A7E79D */
          curr-note = l-op.lscheinnr + " - " + l-artikel.bezeich + 
            "; " + l-lieferant.firma.
          curr-bezeich = l-artikel.bezeich.
          curr-firma = l-lieferant.firma.
          counter = counter + 1.
        END.
        ELSE curr-note = l-op.lscheinnr + " - " + l-artikel.bezeich. 

        add-note = ";&&3;" + STRING(l-op.lager-nr,"99") + ";" + STRING(l-op.lief-nr) 
          + ";" + l-op.docu-nr + ";" + l-op.lscheinnr + ";". 

        tot-wert = tot-wert + l-op.warenwert. 
        fibukonto = gl-acct.fibukonto. 
        curr-docu = l-op.docu-nr. 

        IF l-op.warenwert GE 0 THEN 
        DO: 
          debit-betrag = /*round(l-op.warenwert, 2)*/ l-op.warenwert. /*FDL - Ticket 8DA193-Comment round*/ 
          credit-betrag = 0. 
          FIND FIRST g-list WHERE g-list.fibukonto = gl-acct.fibukonto 
    /*      AND g-list.docu-nr EQ l-op.docu-nr */ 
            AND g-list.lscheinnr EQ l-op.lscheinnr 
            AND g-list.debit NE 0 NO-ERROR. 
          IF NOT AVAILABLE g-list AND debit-betrag NE 0 THEN /* Naufal Afthar - A7E79D */
              RUN add-list(YES).
          ELSE RUN add-list(NO). 
          op-exist = YES. 
        END. 
        ELSE IF l-op.warenwert LT 0 THEN 
        DO: 
          credit-betrag = /*- round(l-op.warenwert, 2)*/ - l-op.warenwert. /*FDL - Ticket 8DA193-Comment round*/ 
          debit-betrag = 0. 
          FIND FIRST g-list WHERE g-list.fibukonto = gl-acct.fibukonto 
    /*      AND g-list.docu-nr EQ l-op.docu-nr  */ 
            AND g-list.lscheinnr EQ l-op.lscheinnr 
            AND g-list.credit NE 0 NO-ERROR. 
          IF NOT AVAILABLE g-list AND credit-betrag NE 0 THEN /* Naufal Afthar - A7E79D */
              RUN add-list(YES).
          ELSE RUN add-list(NO). 
          op-exist = YES. 
        END. 
            
        /*ITA : VAT Inventory Request Vietname*/
          FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
              AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
          IF AVAILABLE queasy THEN DO:
              FIND FIRST bqueasy WHERE bqueasy.KEY = 303
                  AND bqueasy.number1 = queasy.number2 NO-LOCK NO-ERROR.
    
               FIND FIRST gl-acc2 WHERE gl-acc2.fibukonto = bqueasy.char2 NO-LOCK NO-ERROR. 

                IF AVAILABLE l-lieferant THEN 
                  curr-note = "VAT " + l-op.lscheinnr + " " + l-artikel.bezeich + 
                    "; " + l-lieferant.firma. 
                ELSE curr-note = "VAT " + l-op.lscheinnr + " " + l-artikel.bezeich. 
        
                add-note = ";&&3;" + STRING(l-op.lager-nr,"99") + ";" + STRING(l-op.lief-nr) 
                  + ";" + l-op.docu-nr + ";" + l-op.lscheinnr + ";". 
        
                tot-wert = tot-wert + (l-op.warenwert * (queasy.deci1 / 100)). 
                tot-vat  = tot-vat + (l-op.warenwert * (queasy.deci1 / 100)).
                IF AVAILABLE gl-acc2 THEN /* Naufal Afthar - add validation */
                    fibukonto = gl-acc2.fibukonto.
                curr-docu = l-op.docu-nr. 

                IF (l-op.warenwert * (queasy.deci1 / 100)) GE 0 THEN 
                DO: 
                  debit-betrag = (l-op.warenwert * (queasy.deci1 / 100)).
                  credit-betrag = 0. 
                  FIND FIRST g-list WHERE g-list.fibukonto = gl-acc2.fibukonto 
                    AND g-list.lscheinnr EQ l-op.lscheinnr 
                    AND g-list.debit NE 0 NO-ERROR. 
                  IF NOT AVAILABLE g-list AND debit-betrag NE 0 THEN /* Naufal Afthar - A7E79D */
                      RUN add-list(YES).
                  ELSE RUN add-list(NO).
                  op-exist = YES. 
                END. 
                ELSE IF (l-op.warenwert * (queasy.deci1 / 100)) LT 0 THEN 
                DO: 
                  credit-betrag =  - (l-op.warenwert * (queasy.deci1 / 100)). /*FDL - Ticket 8DA193-Comment round*/ 
                  debit-betrag = 0. 
                  FIND FIRST g-list WHERE g-list.fibukonto = gl-acc2.fibukonto 
                    AND g-list.lscheinnr EQ l-op.lscheinnr 
                    AND g-list.credit NE 0 NO-ERROR. 
                  IF NOT AVAILABLE g-list AND debit-betrag NE 0 THEN /* Naufal Afthar - A7E79D */
                      RUN add-list(YES).
                  ELSE RUN add-list(NO).
                  op-exist = YES. 
                END. 
           END.
    END.
    ELSE
    DO: 
      msg-str5 = msg-str5 + CHR(2)
               + translateExtended ("Chart-of-acct of following inventory item not defined :",lvCAREA,"")
               + CHR(10)
               + STRING(l-artikel.artnr) + " - " + l-artikel.bezeich.
    END.
  END. 


  IF op-exist THEN 
  DO: 
    curr-zeit = curr-zeit + 1. 
    IF AVAILABLE l-lieferant THEN 
    DO:
        /* Naufal Afthar - A7E79D */
        IF counter LE 1 THEN /* case credit = 1 */
            curr-note = curr-lschein + " - " + curr-bezeich + "; " + l-lieferant.firma.
        ELSE 
            curr-note = curr-lschein + " - " + l-lieferant.firma.
        counter = 0.
    END.
    ELSE 
    DO:  
        /* Naufal Afthar - A7E79D */
        IF counter LE 1 THEN /* case credit = 1 */
            curr-note = curr-lschein + " - " + curr-bezeich + "; " + curr-firma.
        ELSE 
            curr-note = curr-lschein + " - " + curr-firma.
        counter = 0.
    END.
    /* Naufal Afthar - A7E79D */
    do-it = YES. 
    IF AVAILABLE l-lieferant AND l-lieferant.z-code NE "" THEN 
    DO: 
      FIND FIRST gl-acc1 WHERE gl-acc1.fibukonto = l-lieferant.z-code 
        NO-LOCK NO-ERROR. 
      IF AVAILABLE gl-acc1 THEN do-it = (gl-acc1.fibukonto EQ ap-account). 
    END. 
    
    IF NOT do-it THEN 
    DO: 
      fibukonto = gl-acc1.fibukonto. 
      IF tot-wert GT 0 THEN 
      DO: 
        credit-betrag = tot-wert. 
        debit-betrag = 0. 
        RUN add-list(YES). 
      END. 
      ELSE IF tot-wert LT 0 THEN 
      DO: 
        debit-betrag = - tot-wert. 
        credit-betrag = 0. 
        RUN add-list(YES). 
      END. 
    END. 
    ELSE 
    DO: 
      fibukonto = ap-account. 
      FOR EACH l-kredit WHERE 
        l-kredit.rgdatum GE from-date AND l-kredit.rgdatum LE to-date 
        AND l-kredit.lscheinnr = curr-lschein 
        AND l-kredit.opart GE 0 AND l-kredit.zahlkonto EQ 0 
        AND l-kredit.saldo NE 0 NO-LOCK: 
        ratio = l-kredit.netto / l-kredit.saldo. 
        
        IF l-kredit.netto GE 0 THEN 
        DO: 
          credit-betrag = l-kredit.netto. 
          debit-betrag = 0. 
          RUN add-list(YES). 
        END. 
        ELSE IF l-kredit.netto LT 0 THEN 
        DO: 
          debit-betrag = - l-kredit.netto. 
          credit-betrag = 0. 
          RUN add-list(YES). 
        END. 
      END. 
    END. 
  END. 
END. 
 
PROCEDURE step-three-FA:   /* Receiving Fixed Asset <--> A/P*/ 
DEFINE buffer art1 FOR artikel. 
DEFINE buffer gl-acc1 FOR gl-acct. 
DEFINE VARIABLE ap-account AS CHAR. 
DEFINE VARIABLE note AS CHAR. 
DEFINE VARIABLE curr-docu AS CHAR. 
DEFINE VARIABLE curr-lschein AS CHAR. 
DEFINE VARIABLE op-exist AS LOGICAL. 
DEFINE VARIABLE tot-vat AS DECIMAL NO-UNDO INITIAL 0.
DEFINE BUFFER bqueasy FOR queasy.
DEFINE buffer gl-acc2 FOR gl-acct. 
 
  FIND FIRST htparam WHERE htparam.paramnr = 887 NO-LOCK NO-ERROR.    /*FA AP Account-# */ 
  IF htparam.fchar NE "" THEN ap-account = htparam.fchar. 
  ELSE DO:
      FIND FIRST htparam WHERE htparam.paramnr = 986 NO-LOCK NO-ERROR.    /*AP Account-# */ 
      ap-account = htparam.fchar. 
  END.
 
  op-exist = NO. 
  curr-lschein = "". 
  curr-zeit = TIME. 
  FOR EACH fa-op WHERE fa-op.anzahl NE 0 AND fa-op.loeschflag LT 2
    AND fa-op.opart = 1
    AND fa-op.datum GE from-date AND fa-op.datum LE to-date NO-LOCK, 
    FIRST l-lieferant WHERE l-lieferant.lief-nr = fa-op.lief-nr NO-LOCK, 
    FIRST fa-artikel WHERE fa-artikel.nr = fa-op.nr NO-LOCK
    BY fa-op.lscheinnr: 
 
    FIND FIRST fa-grup WHERE fa-grup.gnr = fa-artikel.subgrp
        AND fa-grup.flag = 1 NO-LOCK.
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-grup.fibukonto NO-LOCK 
      NO-ERROR.
    IF NOT AVAILABLE gl-acct THEN
    FIND FIRST gl-acct WHERE gl-acct.fibukonto = fa-artikel.fibukonto NO-LOCK.

    curr-zeit = curr-zeit + 1. 
 
    add-note = ";&&9;" + TRIM(STRING(fa-op.nr,">>>99")) + ";" 
      + fa-op.docu-nr + ";" + fa-op.lscheinnr + ";". 
 
    IF curr-lschein = "" THEN 
    DO: 
      curr-lschein = fa-op.lscheinnr. 
      curr-note = curr-lschein + " - " + l-lieferant.firma. 
    END. 
    IF curr-lschein NE fa-op.lscheinnr THEN 
    DO: 
      fibukonto = ap-account. 
      FOR EACH l-kredit WHERE 
        l-kredit.rgdatum GE from-date AND l-kredit.rgdatum LE to-date 
        AND l-kredit.lscheinnr = curr-lschein 
        AND l-kredit.opart GE 0 AND l-kredit.zahlkonto EQ 0 
        AND l-kredit.saldo NE 0 NO-LOCK: 
        IF l-kredit.netto GE 0 THEN 
        DO: 
          credit-betrag = l-kredit.netto. 
          debit-betrag = 0. 
          RUN add-list(YES). 
        END. 
        ELSE IF l-kredit.netto LT 0 THEN 
        DO: 
          debit-betrag = - l-kredit.netto. 
          credit-betrag = 0. 
          RUN add-list(YES). 
        END. 
      END. 
      curr-lschein = fa-op.lscheinnr. 
      curr-note = curr-lschein + " - " + l-lieferant.firma. 
      op-exist = NO. 
      tot-vat = 0.
    END. 
 
    fibukonto = gl-acct.fibukonto. 
    curr-docu = fa-op.docu-nr. 
    IF fa-op.warenwert GE 0 THEN 
    DO: 
      debit-betrag = round(fa-op.warenwert, 2). 
      credit-betrag = 0. 
      FIND FIRST g-list WHERE g-list.fibukonto = gl-acct.fibukonto 
/*      AND g-list.docu-nr EQ fa-op.docu-nr */ 
        AND g-list.lscheinnr EQ fa-op.lscheinnr 
        AND g-list.debit NE 0 NO-ERROR. 
      IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
      ELSE RUN add-list(NO). 
      op-exist = YES. 
    END. 
    ELSE IF fa-op.warenwert LT 0 THEN 
    DO: 
      credit-betrag = - round(fa-op.warenwert, 2). 
      debit-betrag = 0. 
      FIND FIRST g-list WHERE g-list.fibukonto = gl-acct.fibukonto 
/*      AND g-list.docu-nr EQ fa-op.docu-nr  */ 
        AND g-list.lscheinnr EQ fa-op.lscheinnr 
        AND g-list.credit NE 0 NO-ERROR. 
      IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
      ELSE RUN add-list(NO). 
      op-exist = YES. 
    END. 


    /*ITA : VAT Inventory Request Vietname*/
      FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-op.lscheinnr 
          AND queasy.number1 = l-op.artnr NO-LOCK NO-ERROR.
      IF AVAILABLE queasy THEN DO:
          FIND FIRST bqueasy WHERE bqueasy.KEY = 303
              AND bqueasy.number1 = queasy.number2 NO-LOCK NO-ERROR.

          FIND FIRST gl-acc2 WHERE gl-acc2.fibukonto = bqueasy.char2 NO-LOCK NO-ERROR. 

            fibukonto = gl-acc2.fibukonto. 
            curr-docu = fa-op.docu-nr.
            tot-vat  = (fa-op.warenwert * (queasy.deci1 / 100)).

            IF (fa-op.warenwert * (queasy.deci1 / 100)) GE 0 THEN 
            DO: 
              debit-betrag = round((fa-op.warenwert * (queasy.deci1 / 100)), 2). 
              credit-betrag = 0. 
              FIND FIRST g-list WHERE g-list.fibukonto = gl-acc2.fibukonto 
                AND g-list.lscheinnr EQ fa-op.lscheinnr 
                AND g-list.debit NE 0 NO-ERROR. 
              IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
              ELSE RUN add-list(NO). 
              op-exist = YES. 
            END. 
            ELSE IF (fa-op.warenwert * (queasy.deci1 / 100)) LT 0 THEN 
            DO: 
              credit-betrag = - round((fa-op.warenwert * (queasy.deci1 / 100)), 2). 
              debit-betrag = 0. 
              FIND FIRST g-list WHERE g-list.fibukonto = gl-acc2.fibukonto 
                AND g-list.lscheinnr EQ fa-op.lscheinnr 
                AND g-list.credit NE 0 NO-ERROR. 
              IF NOT AVAILABLE g-list THEN RUN add-list(YES). 
              ELSE RUN add-list(NO). 
              op-exist = YES. 
            END. 
       END.
  END.

  IF op-exist THEN 
  DO: 
    curr-zeit = curr-zeit + 1. 
    fibukonto = ap-account. 
    FOR EACH l-kredit WHERE 
      l-kredit.rgdatum GE from-date AND l-kredit.rgdatum LE to-date 
      AND l-kredit.lscheinnr = curr-lschein 
      AND l-kredit.opart GE 0 AND l-kredit.zahlkonto EQ 0 
      AND l-kredit.saldo NE 0 NO-LOCK: 
      IF l-kredit.netto GE 0 THEN 
      DO: 
        credit-betrag = l-kredit.netto. 
        debit-betrag = 0. 
        RUN add-list(YES). 
      END. 
      ELSE IF l-kredit.netto LT 0 THEN 
      DO: 
        debit-betrag = - l-kredit.netto. 
        credit-betrag = 0. 
        RUN add-list(YES). 
      END. 
    END. 
  END. 
END. 

PROCEDURE add-list: 
DEFINE INPUT PARAMETER create-it AS LOGICAL. 
  curr-anz = curr-anz + 1. 
  IF create-it THEN 
  DO: 
    create g-list. 
    g-list.fibukonto = fibukonto. 
    g-list.lscheinnr = curr-lschein. 
    g-list.bemerk = curr-note. 
    g-list.add-note = add-note. 
  END. 
  g-list.debit = g-list.debit + debit-betrag. 
  g-list.credit = g-list.credit + credit-betrag. 
  g-list.userinit = user-init. 
  g-list.zeit = curr-zeit. 
  g-list.duplicate = NO. 

  credits = credits + credit-betrag. 
  debits = debits + debit-betrag. 
  remains = debits - credits. 
  debit-betrag = 0.
  credit-betrag = 0. 
END. 


PROCEDURE add-list1: 
DEFINE INPUT PARAMETER create-it AS LOGICAL. 
DEFINE INPUT PARAMETER nr AS INTEGER. 
 
  IF nr GT 0 THEN 
  DO: 
    FIND FIRST s-list WHERE s-list.nr = nr. 
    s-list.debit = s-list.debit + debit-betrag. 
    s-list.credit = s-list.credit + credit-betrag. 
  END. 

  /* Malik */
  tot-credit = tot-credit + credit-betrag.  
  tot-debit  = tot-debit +  debit-betrag.
  
  IF create-it THEN
  DO:
    counter = counter + 1.
    IF tot-debit - tot-credit = 0.01 THEN
    DO:
      g-list.credit = g-list.credit + 0.01.
      credits = credits + 0.01.
    END.
    ELSE IF tot-debit - tot-credit = -0.01 THEN
    DO:
      g-list.credit = g-list.credit - 0.01.
      credits = credits - 0.01.
    END.

    IF counter GT 1 THEN
    DO:
      tot-credit = 0.
      tot-debit = 0.
      counter = 0.
    END.
  END.
  
 
  curr-anz = curr-anz + 1.
  IF create-it THEN 
  DO: 
    create g-list. 
    g-list.fibukonto = fibukonto. 
    g-list.lscheinnr = curr-lschein. 
    g-list.bemerk = curr-note. 
    g-list.add-note = add-note. 
  END. 
  g-list.debit = g-list.debit + debit-betrag. 
  g-list.credit = g-list.credit + credit-betrag. 
  g-list.userinit = user-init. 
  g-list.zeit = curr-zeit. 
  g-list.duplicate = NO. 
  credits = credits + credit-betrag. 
  debits = debits + debit-betrag. 
  remains = debits - credits. 
  debit-betrag = 0. 
  credit-betrag = 0.
  
END. 
