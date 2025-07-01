DEF TEMP-TABLE usr-list 
    FIELD kellner-nr AS INTEGER 
    FIELD kellnername AS CHAR. 
 
DEFINE TEMP-TABLE s-list 
  FIELD zinr     LIKE zimmer.zinr
  FIELD gname    AS CHAR FORMAT "x(22)" 
  FIELD rechnr   AS INTEGER FORMAT ">>>>>>>" 
  FIELD zknr     AS INTEGER EXTENT 5 
  FIELD anz      AS INTEGER INITIAL 0 
  FIELD anzahl   AS INTEGER FORMAT "->9" EXTENT 5 INITIAL [0,0,0,0,0] 
  FIELD amount   AS DECIMAL FORMAT " ->>>,>>9.99" EXTENT 5 INITIAL [0,0,0,0,0] 
  FIELD tamount  AS DECIMAL FORMAT " ->>>,>>9.99" LABEL "Total-Amount" INITIAL 0 
  FIELD tanz     AS INTEGER FORMAT "->9" LABEL "Qty" INITIAL 0 
  FIELD userinit AS CHAR FORMAT "x(2)" LABEL "ID ". 
 
DEFINE TEMP-TABLE pay-list 
  FIELD flag    AS INTEGER /* 1 cash  2 room  3 CC  4 EL  5 CL  6 Comp  */ 
  FIELD bezeich AS CHAR FORMAT "x(24)" 
  FIELD artnr   AS INTEGER FORMAT ">>>>9 " 
  FIELD rechnr  AS INTEGER FORMAT ">>>>>>9 " 
  FIELD foreign AS DECIMAL FORMAT "->>>,>>9.99" 
  FIELD saldo   AS DECIMAL FORMAT "->>,>>>,>>9.99". 

DEF BUFFER sbuff FOR s-list. 

DEF INPUT PARAMETER pvILanguage  AS INTEGER  NO-UNDO.
DEF INPUT PARAMETER ldry-dept AS INT.
DEF INPUT PARAMETER all-flag AS LOGICAL.
DEF INPUT PARAMETER usr-created AS LOGICAL.
DEF INPUT PARAMETER usr-init AS CHAR.
DEF INPUT PARAMETER from-date AS DATE.
DEF INPUT PARAMETER to-date AS DATE.
DEF INPUT PARAMETER ekumnr AS INT.
DEF INPUT PARAMETER zknr1 AS INT.
DEF INPUT PARAMETER zknr2 AS INT.
DEF INPUT PARAMETER zknr3 AS INT.
DEF INPUT PARAMETER zknr4 AS INT.
DEF INPUT PARAMETER zknr5 AS INT.
DEF OUTPUT PARAMETER t-betrag AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR pay-list.

{supertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "ldry1-report". 

FOR EACH pay-list: 
    DELETE pay-list. 
END. 
FOR EACH s-list: 
    DELETE s-list. 
END. 
t-betrag = 0. 

IF all-flag THEN RUN create-list-all. 
ELSE RUN create-list(usr-init, ""). 

/**************************** PROCEDURES **************************************/
PROCEDURE create-list-all: 
    IF NOT usr-created THEN 
    DO: 
        FOR EACH h-journal WHERE h-journal.departement = ldry-dept 
            AND bill-datum = from-date NO-LOCK: 
          FIND FIRST kellner WHERE kellner.kellner-nr = h-journal.kellner-nr 
              NO-LOCK NO-ERROR. 
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
            sbuff.amount[1] = sbuff.amount[1] + s-list.amount[1]. 
            sbuff.amount[2] = sbuff.amount[2] + s-list.amount[2]. 
            sbuff.amount[3] = sbuff.amount[3] + s-list.amount[3]. 
            sbuff.amount[4] = sbuff.amount[4] + s-list.amount[4]. 
            sbuff.amount[5] = sbuff.amount[5] + s-list.amount[5]. 
            sbuff.tanz = sbuff.tanz + s-list.tanz. 
            sbuff.tamount = sbuff.tamount + s-list.tamount. 
        END. 
    END. 
END. 
 
PROCEDURE create-list: 
DEF INPUT PARAMETER usr-init AS CHAR. 
DEF INPUT PARAMETER kellner-name AS CHAR. 
 
DEFINE VARIABLE curr-date AS DATE. 
DEFINE VARIABLE rmno LIKE zimmer.zinr.
DEFINE VARIABLE rm-flag AS LOGICAL. 
DEFINE VARIABLE billno AS INTEGER. 
DEFINE VARIABLE gname AS CHAR. 
DEFINE VARIABLE t-qty AS INTEGER EXTENT 5 INITIAL 0. 
DEFINE VARIABLE t-amt AS DECIMAL EXTENT 5 INITIAL 0. 
DEFINE VARIABLE tot-qty AS INTEGER INITIAL 0. 
DEFINE VARIABLE tot-amt AS DECIMAL INITIAL 0. 
DEFINE VARIABLE disc-art AS LOGICAL. 
DEFINE VARIABLE qty-i AS INTEGER. 
 
  DO curr-date = from-date TO to-date: 
    FOR EACH h-journal WHERE h-journal.kellner-nr = INTEGER(usr-init) 
      AND h-journal.departement = ldry-dept 
      AND bill-datum = curr-date NO-LOCK, 
      FIRST h-bill WHERE h-bill.rechnr = h-journal.rechnr 
        AND h-bill.departement = h-journal.departement NO-LOCK 
      BY h-journal.rechnr: 
 
      rm-flag = NO. 
      IF SUBSTR(h-journal.bezeich,7,4) = "RmNo" THEN 
      DO: 
        rm-flag = YES. 
        rmno = SUBSTR(h-journal.bezeich, 12, 4). 
        IF SUBSTR(rmno, 4, 1) = "*" OR length(rmno) = 3 THEN 
        DO: 
          rmno = SUBSTR(rmno, 1, 3). 
          billno = INTEGER(SUBSTR(h-journal.bezeich, 10, 10)). 
        END. 
        ELSE billno = INTEGER(SUBSTR(h-journal.bezeich, 11, 10)). 
      END. 
      ELSE IF SUBSTR(h-journal.bezeich,7,4) = "RmNo" THEN 
      DO: 
        rm-flag = YES. 
        rmno = SUBSTR(h-journal.bezeich, 12, 4). 
        IF SUBSTR(rmno, 4, 1) = "*" OR length(rmno) = 3 THEN 
        DO: 
          rmno = SUBSTR(rmno, 1, 3). 
          billno = INTEGER(SUBSTR(h-journal.bezeich, 16, 10)). 
        END. 
        ELSE billno = INTEGER(SUBSTR(h-journal.bezeich, 17, 10)). 
      END. 
 
      IF h-journal.artnr = 0 AND rm-flag THEN 
      DO: 
        FIND FIRST pay-list WHERE pay-list.flag = 2 NO-ERROR. 
        IF NOT AVAILABLE pay-list THEN 
        DO: 
          create pay-list. 
          pay-list.flag = 2. 
          pay-list.bezeich = translateExtended ("Room Transfer",lvCAREA,""). 
        END. 
        pay-list.saldo = pay-list.saldo - h-journal.betrag. 
        t-betrag = t-betrag - h-journal.betrag. 
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
          s-list.userinit = usr-init. 
        END. 
        s-list.zinr = rmno. 
        s-list.gname = gname. 
        IF h-journal.betrag LT 0 THEN s-list.anz = s-list.anz + 1. 
        ELSE IF h-journal.betrag GT 0 THEN s-list.anz = s-list.anz - 1. 
      END. 
 
      ELSE IF h-journal.artnr = 0 AND 
        SUBSTR(h-journal.bezeich, 1, 8) = "Transfer" THEN 
      DO: 
        gname = "". 
        billno = INTEGER(SUBSTR(h-journal.bezeich, 11, 10)). 
        FIND FIRST bill WHERE bill.rechnr = billno NO-LOCK NO-ERROR. 
        IF AVAILABLE bill THEN gname = bill.name. 
        FIND FIRST s-list WHERE s-list.rechnr = h-journal.rechnr NO-LOCK 
          NO-ERROR. 
        IF NOT AVAILABLE s-list THEN 
        DO: 
          create s-list. 
          s-list.rechnr = h-journal.rechnr. 
          s-list.userinit = usr-init. 
        END. 
        s-list.gname = gname. 
        FIND FIRST pay-list WHERE pay-list.flag = 3 NO-ERROR. 
        IF NOT AVAILABLE pay-list THEN 
        DO: 
          create pay-list. 
          pay-list.flag = 3. 
          pay-list.bezeich = translateExtended ("Bill Transfer",lvCAREA,""). 
        END. 
        pay-list.saldo = pay-list.saldo - h-journal.betrag. 
        t-betrag = t-betrag - h-journal.betrag. 
      END. 
 
      ELSE IF h-journal.artnr GT 0 THEN 
      DO: 
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-journal.artnr 
          AND h-artikel.departement = h-journal.departement NO-LOCK. 
 
        IF h-artikel.artart = 6 THEN 
        DO: 
          FIND FIRST s-list WHERE s-list.rechnr = h-journal.rechnr NO-LOCK 
            NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.rechnr = h-journal.rechnr. 
            s-list.userinit = usr-init. 
          END. 
          IF s-list.gname = "" THEN s-list.gname = h-bill.bilname. 
          IF s-list.gname = "" THEN s-list.gname = translateExtended ("CASH",lvCAREA,""). 
          FIND FIRST pay-list WHERE pay-list.flag = 4 NO-ERROR. 
          IF NOT AVAILABLE pay-list THEN 
          DO: 
            create pay-list. 
            pay-list.flag = 4. 
            pay-list.bezeich = translateExtended ("Cash",lvCAREA,""). 
          END. 
          pay-list.saldo = pay-list.saldo - h-journal.betrag. 
          t-betrag = t-betrag - h-journal.betrag. 
        END. 
 
        ELSE IF h-artikel.artart = 2 OR h-artikel.artart = 7 
          OR h-artikel.artart = 11 THEN 
        DO: 
          IF h-artikel.artart = 7 THEN 
          DO: 
            FIND FIRST pay-list WHERE pay-list.flag = 5 NO-ERROR. 
            IF NOT AVAILABLE pay-list THEN 
            DO: 
              create pay-list. 
              pay-list.flag = 5. 
              pay-list.bezeich = translateExtended ("Credit Card",lvCAREA,""). 
            END. 
          END. 
 
          ELSE IF h-artikel.artart = 2 THEN 
       /* City Ledger  */ 
          DO: 
            FIND FIRST pay-list WHERE pay-list.flag = 6 NO-ERROR. 
            IF NOT AVAILABLE pay-list THEN 
            DO: 
              create pay-list. 
              pay-list.flag = 6. 
              pay-list.bezeich = translateExtended ("City Ledger",lvCAREA,""). 
            END. 
          END. 
 
          ELSE IF h-artikel.artart = 11  THEN 
       /* complimentary  */ 
          DO: 
            FIND FIRST pay-list WHERE pay-list.flag = 7 NO-ERROR. 
            IF NOT AVAILABLE pay-list THEN 
            DO: 
              create pay-list. 
              pay-list.flag = 7. 
              pay-list.bezeich = translateExtended ("Compliment",lvCAREA,""). 
            END. 
          END. 
          pay-list.saldo = pay-list.saldo - h-journal.betrag. 
          t-betrag = t-betrag - h-journal.betrag. 
 
          FIND FIRST s-list WHERE s-list.rechnr = h-journal.rechnr NO-LOCK 
          NO-ERROR. 
          IF NOT AVAILABLE s-list THEN 
          DO: 
            create s-list. 
            s-list.rechnr = h-journal.rechnr. 
            s-list.userinit = usr-init. 
          END. 
          IF s-list.gname = "" OR (s-list.gname NE "" AND s-list.anz = 0) THEN 
          DO: 
            /* IF h-bill.bilname NE "" THEN s-list.gname = h-bill.bilname. */ 
            s-list.gname = h-artikel.bezeich. 
            IF h-bill.resnr GT 0 AND s-list.zinr = "" THEN 
            DO: 
              FIND FIRST res-line WHERE res-line.resnr = h-bill.resnr 
                AND res-line.reslinnr = h-bill.reslinnr NO-LOCK NO-ERROR. 
              IF AVAILABLE res-line THEN s-list.zinr = res-line.zinr. 
            END. 
          END. 
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
            s-list.userinit = usr-init. 
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
          tot-qty = tot-qty + qty-i. 
          tot-amt = tot-amt + h-journal.betrag. 
          s-list.tanz = s-list.tanz + qty-i. 
          s-list.tamount = s-list.tamount + h-journal.betrag. 
        END. 
      END. 
    END. 
  END. 
 
  CREATE s-list. 
  IF NOT all-flag THEN s-list.gname = "T o t a l". 
  ELSE s-list.gname = "Total - " + kellner-name. 
 
  s-list.userinit = usr-init. 
  s-list.anzahl[1] = t-qty[1]. 
  s-list.anzahl[2] = t-qty[2]. 
  s-list.anzahl[3] = t-qty[3]. 
  s-list.anzahl[4] = t-qty[4]. 
  s-list.anzahl[5] = t-qty[5]. 
  s-list.amount[1] = t-amt[1]. 
  s-list.amount[2] = t-amt[2]. 
  s-list.amount[3] = t-amt[3]. 
  s-list.amount[4] = t-amt[4]. 
  s-list.amount[5] = t-amt[5]. 
  s-list.tanz = tot-qty. 
  s-list.tamount = tot-amt. 
 
END. 
 

