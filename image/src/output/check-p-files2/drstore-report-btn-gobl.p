DEFINE TEMP-TABLE s-list 
    FIELD zinr     LIKE zimmer.zinr		/*MT 25/07/12 */
    FIELD gname    AS CHAR FORMAT "x(20)" 
    FIELD rechnr   AS INTEGER FORMAT ">>>>>>" 
    FIELD zknr     AS INTEGER EXTENT 6 
    FIELD anzahl   AS INTEGER FORMAT ">>9" EXTENT 6 
    FIELD amount   AS DECIMAL FORMAT " ->>>,>>9.99" EXTENT 6 
    FIELD tamount  AS DECIMAL FORMAT "->,>>>,>>9" LABEL "Tot-Amount" 
    FIELD tanz     AS INTEGER FORMAT ">>9" LABEL "Qty" 
    FIELD userinit AS CHAR FORMAT "x(2)" LABEL "ID ". 

DEFINE TEMP-TABLE pay-list 
    FIELD flag AS INTEGER /* 1 cash  2 room  3 CC  4 EL  5 CL  6 Comp  */ 
    FIELD bezeich AS CHAR FORMAT "x(24)" 
    FIELD artnr AS INTEGER FORMAT ">>>>9 " 
    FIELD rechnr AS INTEGER FORMAT ">>>>>>9 " 
    FIELD foreign AS DECIMAL FORMAT "->>>,>>9.99" 
    FIELD saldo AS DECIMAL FORMAT "->>,>>>,>>9.99". 
 
DEF TEMP-TABLE usr-list 
    FIELD kellner-nr AS INTEGER 
    FIELD kellnername AS CHAR.


DEFINE INPUT PARAMETER usr-created AS LOGICAL.
DEFINE INPUT PARAMETER dstore-dept AS INTEGER.
DEFINE INPUT PARAMETER all-flag    AS LOGICAL.
DEFINE INPUT PARAMETER ekumnr      AS INTEGER.
DEFINE INPUT PARAMETER zknr1       AS INTEGER.
DEFINE INPUT PARAMETER zknr2       AS INTEGER.
DEFINE INPUT PARAMETER zknr3       AS INTEGER.
DEFINE INPUT PARAMETER zknr4       AS INTEGER.
DEFINE INPUT PARAMETER zknr5       AS INTEGER.
DEFINE INPUT PARAMETER zknr6       AS INTEGER.
DEFINE INPUT PARAMETER from-date   AS DATE.
DEFINE INPUT PARAMETER to-date     AS DATE.
DEFINE INPUT PARAMETER usr-init    AS CHARACTER.
DEFINE OUTPUT PARAMETER exchg-rate  AS DECIMAL.
DEFINE OUTPUT PARAMETER t-betrag   AS DECIMAL.
DEFINE OUTPUT PARAMETER t-foreign  AS DECIMAL.
DEFINE OUTPUT PARAMETER TABLE FOR s-list.
DEFINE OUTPUT PARAMETER TABLE FOR pay-list.
   
DEF BUFFER sbuff FOR s-list. 

IF all-flag THEN RUN create-list-all. 
ELSE RUN create-list(usr-init,""). 

PROCEDURE create-list-all: 
    /*IF NOT usr-created THEN*/
    DO: 
        FOR EACH h-journal WHERE h-journal.departement = dstore-dept 
            AND bill-datum = from-date NO-LOCK: 
          FIND FIRST kellner WHERE kellner.kellner-nr = h-journal.kellner-nr 
              AND kellner.departement = dstore-dept NO-LOCK NO-ERROR. 
          IF AVAILABLE kellner THEN 
          DO: 
              FIND FIRST usr-list WHERE usr-list.kellner-nr = h-journal.kellner-nr 
                  NO-LOCK NO-ERROR. 
              IF NOT AVAILABLE usr-list THEN 
              DO: 
                  CREATE usr-list. 
                  ASSIGN 
                      usr-list.kellner-nr = h-journal.kellner-nr 
                      usr-list.kellnername = kellner.kellnername 
                  . 
              END. 
          END. 
        END. 
        usr-created = YES. 
    END. 
    FOR EACH usr-list BY usr-list.kellner-nr: 
        RUN create-list(STRING(usr-list.kellner-nr), usr-list.kellnername). 
    END. 
    IF all-flag THEN
    DO: 
        CREATE sbuff. 
        ASSIGN sbuff.gname = "Grand Total". 
        FOR EACH s-list WHERE NOT s-list.gname MATCHES ("*Total*"): 
            sbuff.anzahl[1] = sbuff.anzahl[1] + s-list.anzahl[1]. 
            sbuff.anzahl[2] = sbuff.anzahl[2] + s-list.anzahl[2]. 
            sbuff.anzahl[3] = sbuff.anzahl[3] + s-list.anzahl[3]. 
            sbuff.anzahl[4] = sbuff.anzahl[4] + s-list.anzahl[4]. 
            sbuff.anzahl[5] = sbuff.anzahl[5] + s-list.anzahl[5]. 
            sbuff.anzahl[6] = sbuff.anzahl[6] + s-list.anzahl[6]. 
            sbuff.amount[1] = sbuff.amount[1] + s-list.amount[1]. 
            sbuff.amount[2] = sbuff.amount[2] + s-list.amount[2]. 
            sbuff.amount[3] = sbuff.amount[3] + s-list.amount[3]. 
            sbuff.amount[4] = sbuff.amount[4] + s-list.amount[4]. 
            sbuff.amount[5] = sbuff.amount[5] + s-list.amount[5]. 
            sbuff.amount[6] = sbuff.amount[6] + s-list.amount[6]. 
            sbuff.tanz = sbuff.tanz + s-list.tanz. 
            sbuff.tamount = sbuff.tamount + s-list.tamount. 
        END. 
    END. 
END. 
 
PROCEDURE create-list: 
DEF INPUT PARAMETER usr-init AS CHAR. 
DEF INPUT PARAMETER kellner-name AS CHAR. 
 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE rmno LIKE zimmer.zinr.		/*MT 25/07/12 */
DEFINE VARIABLE billno AS INTEGER. 
DEFINE VARIABLE gname AS CHAR. 
DEFINE VARIABLE t-qty AS INTEGER EXTENT 6 INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL EXTENT 6 INITIAL 0. 
DEFINE VARIABLE tot-qty AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE disc-art AS LOGICAL. 
DEFINE VARIABLE qty-i AS INTEGER. 

  DO curr-date = from-date TO to-date: 
    FOR EACH h-journal WHERE h-journal.kellner-nr = INTEGER(usr-init) 
      AND h-journal.departement = dstore-dept 
      AND bill-datum = curr-date NO-LOCK, 
      FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr 
        AND h-bill.departement = h-journal.departement NO-LOCK 
      BY h-journal.rechnr: 
 
      IF h-journal.artnr = 0 AND SUBSTR(h-journal.bezeich, 7, 4) = "RmNo" THEN 
      DO: 
 
        FIND FIRST pay-list WHERE pay-list.flag = 2 NO-ERROR. 
        IF NOT AVAILABLE pay-list THEN 
        DO: 
          create pay-list. 
          pay-list.flag = 2. 
          pay-list.bezeich = "Room Transfer".
        END. 
        pay-list.foreign = pay-list.foreign - h-journal.fremdwaehrng. 
        pay-list.saldo = pay-list.saldo - h-journal.betrag. 
        t-betrag = t-betrag - h-journal.betrag. 
        t-foreign = t-foreign - h-journal.fremdwaehrng. 
 
        rmno = SUBSTR(h-journal.bezeich, 12, 6).    /*MT 25/07/12 */
        IF SUBSTR(rmno, 6, 1) = "*" THEN            /*MT 25/07/12 */
        DO: 
          rmno = SUBSTR(rmno, 1, 5).    /*MT 25/07/12 */
          billno = INTEGER(SUBSTR(h-journal.bezeich, 17, 10)). 
        END. 
        ELSE billno = INTEGER(SUBSTR(h-journal.bezeich, 18, 10)). 
        FIND FIRST bill WHERE bill.rechnr = billno NO-LOCK. 
        FIND FIRST res-line WHERE res-line.resnr = bill.resnr 
          AND res-line.reslinnr = bill.reslinnr NO-LOCK NO-ERROR. 
        IF AVAILABLE res-line THEN gname = res-line.name. 
        FIND FIRST s-list WHERE s-list.rechnr = h-journal.rechnr NO-LOCK 
          NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.rechnr = h-journal.rechnr. 
        END. 
        s-list.zinr = rmno. 
        s-list.gname = gname. 
      END. 
 
      ELSE IF h-journal.artnr = 0 AND 
        SUBSTR(h-journal.bezeich, 1, 8) = "Transfer" THEN 
      DO: 
        gname = "BillTransfer". 
        billno = INTEGER(SUBSTR(h-journal.bezeich, 11, 10)). 
        FIND FIRST bill WHERE bill.rechnr = billno NO-LOCK NO-ERROR. 
        IF AVAILABLE bill THEN gname = bill.name. 
        FIND FIRST s-list WHERE s-list.rechnr = h-journal.rechnr NO-LOCK 
          NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.rechnr = h-journal.rechnr. 
        END. 
        s-list.gname = gname. 
        FIND FIRST pay-list WHERE pay-list.flag = 3 NO-ERROR. 
        IF NOT AVAILABLE pay-list THEN 
        DO: 
          create pay-list. 
          pay-list.flag = 3. 
          pay-list.bezeich = "Bill Transfer". 
        END. 
        pay-list.foreign = pay-list.foreign - h-journal.fremdwaehrng. 
        pay-list.saldo = pay-list.saldo - h-journal.betrag. 
        t-betrag = t-betrag - h-journal.betrag. 
        t-foreign = t-foreign - h-journal.fremdwaehrng. 
      END. 
 
      ELSE IF h-journal.artnr GT 0 THEN 
      DO: 
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-journal.artnr 
          AND h-artikel.departement = h-journal.departement NO-LOCK. 
 
        IF h-artikel.artart = 2 OR h-artikel.artart = 7 
          OR h-artikel.artart = 6 OR h-artikel.artart = 11 THEN 
        DO: 
          IF h-artikel.artart = 6 THEN 
          DO: 
            FIND FIRST pay-list WHERE pay-list.flag = 1 NO-ERROR. 
            IF NOT AVAILABLE pay-list THEN 
            DO: 
              create pay-list. 
              pay-list.flag = 1. 
              pay-list.bezeich = "Cash". 
            END. 
          END. 
 
          ELSE IF h-artikel.artart = 7 THEN 
          DO: 
            FIND FIRST pay-list WHERE pay-list.flag = 4 NO-ERROR. 
            IF NOT AVAILABLE pay-list THEN 
            DO: 
              create pay-list. 
              ASSIGN
                  pay-list.flag = 4
                  pay-list.bezeich = "Credit Card".
            END. 
          END. 
 
          ELSE IF h-artikel.artart = 2 THEN 
       /* City Ledger  */ 
          DO: 
            FIND FIRST pay-list WHERE pay-list.flag = 5 NO-ERROR. 
            IF NOT AVAILABLE pay-list THEN 
            DO: 
              create pay-list. 
              ASSIGN
                  pay-list.flag = 5
                  pay-list.bezeich = "City Ledger".
            END. 
          END. 
 
          ELSE IF h-artikel.artart = 11  THEN 
       /* complimentary  */ 
          DO: 
            FIND FIRST pay-list WHERE pay-list.flag = 6 NO-ERROR. 
            IF NOT AVAILABLE pay-list THEN 
            DO: 
              create pay-list.
              ASSIGN
                  pay-list.flag = 6
                  pay-list.bezeich = "Compliment".
            END. 
          END. 
          pay-list.foreign = pay-list.foreign - h-journal.fremdwaehrng. 
          pay-list.saldo = pay-list.saldo - h-journal.betrag. 
          t-betrag = t-betrag - h-journal.betrag. 
          t-foreign = t-foreign - h-journal.fremdwaehrng. 
 
          FIND FIRST s-list WHERE s-list.rechnr = h-journal.rechnr NO-LOCK 
          NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.rechnr = h-journal.rechnr. 
          END. 
          s-list.gname = h-artikel.bezeich. 
        END. 
 
        ELSE IF h-artikel.artart = 0 THEN 
        DO: 
          disc-art = NO. 
          qty-i = h-journal.anzahl. 
          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront 
            AND artikel.departement = h-artikel.departement NO-LOCK. 
          IF artikel.endkum = ekumnr THEN 
          DO: 
            disc-art = YES. 
            qty-i = 0. 
          END. 
 
          FIND FIRST wgrpdep WHERE wgrpdep.zknr = h-artikel.zwkum 
            AND wgrpdep.departement = h-artikel.departement NO-LOCK. 
          FIND FIRST s-list WHERE s-list.rechnr = h-journal.rechnr 
            NO-LOCK NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.rechnr = h-journal.rechnr. 
          END. 
          IF wgrpdep.zknr = zknr1 THEN 
          DO: 
            s-list.zknr[1] = wgrpdep.zknr. 
            s-list.anzahl[1] = s-list.anzahl[1] + qty-i. 
            s-list.amount[1] = s-list.amount[1] 
              + h-journal.betrag. 
            t-qty[1] = t-qty[1] + qty-i. 
            t-amt[1] = t-amt[1] + h-journal.betrag. 
          END. 
          ELSE IF wgrpdep.zknr = zknr2 THEN 
          DO: 
            s-list.zknr[2] = wgrpdep.zknr. 
            s-list.anzahl[2] = s-list.anzahl[2] + qty-i. 
            s-list.amount[2] = s-list.amount[2] 
              + h-journal.betrag. 
            t-qty[2] = t-qty[2] + qty-i. 
            t-amt[2] = t-amt[2] + h-journal.betrag. 
          END. 
          ELSE IF wgrpdep.zknr = zknr3 THEN 
          DO: 
            s-list.zknr[3] = wgrpdep.zknr. 
            s-list.anzahl[3] = s-list.anzahl[3] + qty-i. 
            s-list.amount[3] = s-list.amount[3] 
              + h-journal.betrag. 
            t-qty[3] = t-qty[3] + qty-i. 
            t-amt[3] = t-amt[3] + h-journal.betrag. 
          END. 
          ELSE IF wgrpdep.zknr = zknr4 THEN 
          DO: 
            s-list.zknr[4] = wgrpdep.zknr. 
            s-list.anzahl[4] = s-list.anzahl[4] + qty-i. 
            s-list.amount[4] = s-list.amount[4] 
              + h-journal.betrag. 
            t-qty[4] = t-qty[4] + qty-i. 
            t-amt[4] = t-amt[4] + h-journal.betrag. 
          END. 
          ELSE IF wgrpdep.zknr = zknr5 THEN 
          DO: 
            s-list.zknr[5] = wgrpdep.zknr. 
            s-list.anzahl[5] = s-list.anzahl[5] + qty-i. 
            s-list.amount[5] = s-list.amount[5] 
              + h-journal.betrag. 
            t-qty[5] = t-qty[5] + qty-i. 
            t-amt[5] = t-amt[5] + h-journal.betrag. 
          END. 
          ELSE IF wgrpdep.zknr = zknr6 THEN 
          DO: 
            s-list.zknr[6] = wgrpdep.zknr. 
            s-list.anzahl[6] = s-list.anzahl[6] + qty-i. 
            s-list.amount[6] = s-list.amount[6] 
              + h-journal.betrag. 
            t-qty[6] = t-qty[6] + qty-i. 
            t-amt[6] = t-amt[6] + h-journal.betrag. 
          END. 
          tot-qty = tot-qty + qty-i. 
          tot-amt = tot-amt + h-journal.betrag. 
          s-list.tanz = s-list.tanz + qty-i. 
          s-list.tamount = s-list.tamount + h-journal.betrag. 
 
          IF h-journal.fremdwaehrng NE 0 THEN 
            exchg-rate = h-journal.betrag / h-journal.fremdwaehrng. 
 
        END. 
      END. 
    END. 
  END. 
 
  CREATE s-list. 
  IF NOT all-flag THEN s-list.gname = "T o t a l". 
  ELSE s-list.gname = "Total - " + kellner-name. 
 
  s-list.anzahl[1] = t-qty[1]. 
  s-list.anzahl[2] = t-qty[2]. 
  s-list.anzahl[3] = t-qty[3]. 
  s-list.anzahl[4] = t-qty[4]. 
  s-list.anzahl[5] = t-qty[5]. 
  s-list.anzahl[6] = t-qty[6]. 
  s-list.amount[1] = t-amt[1]. 
  s-list.amount[2] = t-amt[2]. 
  s-list.amount[3] = t-amt[3]. 
  s-list.amount[4] = t-amt[4]. 
  s-list.amount[5] = t-amt[5]. 
  s-list.amount[6] = t-amt[6]. 
  s-list.tanz = tot-qty. 
  s-list.tamount = tot-amt. 
 
END. 
