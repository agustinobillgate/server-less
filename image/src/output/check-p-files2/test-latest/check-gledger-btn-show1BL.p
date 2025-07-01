
DEF TEMP-TABLE t1-list
    FIELD dept    AS INTEGER
    FIELD rechnr  AS INTEGER
    FIELD pay     AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD rmTrans AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD compli  AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
    FIELD coupon  AS DECIMAL INITIAL 0 FORMAT "->>,>>>,>>9"
.
DEF TEMP-TABLE s1-list
    FIELD flag      AS INTEGER INITIAL 0
    FIELD nr        AS INTEGER
    FIELD artnr     AS INTEGER FORMAT ">>>>>" COLUMN-LABEL "ArtNo"
    FIELD bezeich   AS CHAR FORMAT "x(24)" COLUMN-LABEL "Description"
    FIELD artart    AS INTEGER
    FIELD dept      AS INTEGER FORMAT "99" COLUMN-LABEL "Dept"
    FIELD amt       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" 
                    COLUMN-LABEL "Bill Amount"
    FIELD ums       AS DECIMAL FORMAT "->,>>>,>>>,>>9.99"
                    COLUMN-LABEL "Revenue Amount"
.

DEF INPUT  PARAMETER currdate AS DATE.
DEF OUTPUT PARAMETER s        AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR s1-list.
/*
DEF VAR currdate AS DATE INITIAL 3/14/19.
DEF VAR s        AS DECIMAL.*/

RUN show-bill-vs-rev.

PROCEDURE show-bill-vs-rev:
DEF VAR curr-i      AS INTEGER INITIAL 0.
DEF VAR curr-dept   AS INTEGER.
DEF VAR tot-billamt AS DECIMAL INITIAL 0.
DEF VAR tot-revamt  AS DECIMAL INITIAL 0.
DEF BUFFER s1buff   FOR s1-list.

  FOR EACH s1-list:
      DELETE s1-list.
  END.
  FOR EACH t1-list:
      DELETE t1-list.
  END.

  FOR EACH h-bill-line WHERE h-bill-line.bill-datum = currdate NO-LOCK
      BY h-bill-line.departement BY h-bill-line.rechnr
      BY h-bill-line.zeit:
      FIND FIRST t1-list WHERE t1-list.rechnr = h-bill-line.rechnr
          AND t1-list.dept = h-bill-line.departement NO-ERROR.
      IF NOT AVAILABLE t1-list THEN
      DO:
          CREATE t1-list.
          ASSIGN
              t1-list.rechnr = h-bill-line.rechnr
              t1-list.dept   = h-bill-line.departement
          .
      END.
      IF h-bill-line.artnr = 0 THEN 
        t1-list.rmtrans = t1-list.rmtrans + h-bill-line.betrag.                     /* Rulita 210225 | Fixing from rmTrans to rmtrans serverless issue git 624 */
      ELSE
      DO:
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr AND
            h-artikel.departement = h-bill-line.departement NO-LOCK.
        IF h-artikel.artart = 11 THEN
            t1-list.compli = t1-list.compli + h-bill-line.betrag.
        ELSE IF h-artikel.artart = 12 THEN
            t1-list.coupon = t1-list.coupon + h-bill-line.betrag.
        ELSE IF h-artikel.artart NE 0 THEN
            t1-list.pay = t1-list.pay + h-bill-line.betrag.
      END.
    END.
    
  FOR EACH t1-list:
      IF t1-list.pay NE 0 OR t1-list.rmtrans NE 0 THEN .                      /* Rulita 210225 | Fixing from rmTrans to rmtrans serverless issue git 624 */
      ELSE DELETE t1-list.
  END.
    
  FOR EACH h-bill-line WHERE h-bill-line.bill-datum = currdate 
    AND h-bill-line.artnr NE 0 NO-LOCK:
    FIND FIRST t1-list WHERE t1-list.rechnr = h-bill-line.rechnr
        AND t1-list.dept = h-bill-line.departement NO-ERROR.
    IF AVAILABLE t1-list THEN
    DO:
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
        AND h-artikel.departement = h-bill-line.departement NO-LOCK.
        IF h-artikel.artart = 0 THEN
        DO:
            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
                AND artikel.departement = h-artikel.departement NO-LOCK.
            FIND FIRST s1-list WHERE s1-list.artnr = artikel.artnr
                AND s1-list.dept = artikel.departement NO-ERROR.
            IF NOT AVAILABLE s1-list THEN
            DO:
                CREATE s1-list.
                ASSIGN
                    s1-list.artnr   = artikel.artnr
                    s1-list.bezeich = artikel.bezeich
                    s1-list.dept    = artikel.departement
                .
            END.
            s1-list.amt = s1-list.amt + h-bill-line.betrag.
        END.
        ELSE IF h-artikel.artart = 6 OR h-artikel.artart = 5 THEN /*FDL Dec 26, 2022 => artart eq 5 Feature Deposit Resto*/
        DO:
            FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
                AND artikel.departement = 0 NO-LOCK.
            FIND FIRST s1-list WHERE s1-list.artnr = artikel.artnr
                AND s1-list.dept = 0 NO-ERROR.
            IF NOT AVAILABLE s1-list THEN
            DO:
                CREATE s1-list.
                ASSIGN
                    s1-list.artnr   = artikel.artnr
                    s1-list.dept    = 0
                    s1-list.bezeich = artikel.bezeich
                    s1-list.artart  = artikel.artart
                .
            END.
            s1-list.amt = s1-list.amt + h-bill-line.betrag.
        END.
    END.
  END.

  FOR EACH umsatz WHERE umsatz.datum = currdate NO-LOCK:
    FIND FIRST artikel WHERE artikel.artnr = umsatz.artnr
    AND artikel.departement = umsatz.departement NO-LOCK NO-ERROR.
/*    
    IF NOT AVAILABLE artikel AND umsatz.betrag NE 0 THEN
        DISP umsatz.artnr umsatz.departement umsatz.betrag.
*/
    IF AVAILABLE artikel AND artikel.artart NE 10 THEN
    DO:
      s = 0.
      FOR EACH billjournal WHERE billjournal.artnr = umsatz.artnr
        AND billjournal.departement = umsatz.departement 
        AND billjournal.bill-datum = currdate 
        AND billjournal.anzahl NE 0 NO-LOCK:
        s = s + billjournal.betrag.
      END.
      FIND FIRST s1-list WHERE s1-list.artnr = umsatz.artnr
        AND s1-list.dept = umsatz.departement NO-ERROR.
      IF NOT AVAILABLE s1-list THEN
      DO:
          FIND FIRST artikel WHERE artikel.artnr = umsatz.artnr
              AND artikel.departement = umsatz.departement NO-LOCK.
          CREATE s1-list.
          ASSIGN
              s1-list.artnr   = artikel.artnr
              s1-list.dept    = artikel.departement
              s1-list.bezeich = artikel.bezeich
              s1-list.artart  = artikel.artart
          .
      END.
      ASSIGN
          s1-list.amt = s1-list.amt + s
          s1-list.ums = umsatz.betrag
      .    
    END.
  END.

  FOR EACH s1-list WHERE s1-list.flag = 0 BY s1-list.dept BY s1-list.artnr:
      curr-i = curr-i + 1.
      IF curr-i = 1 THEN
      ASSIGN curr-dept   = s1-list.dept.

      IF curr-dept NE s1-list.dept THEN
      DO:
          CREATE s1buff.
          ASSIGN
              s1buff.flag       = 1
              s1buff.nr         = curr-i
              s1buff.dept       = curr-dept
              s1buff.bezeich    = "T O T A L"
              s1buff.amt        = tot-billamt
              s1buff.ums        = tot-revamt
              curr-dept         = s1-list.dept
              curr-i            = curr-i + 1
              s1-list.nr        = curr-i 
              tot-billamt       = s1-list.amt
              tot-revamt        = s1-list.ums
          .
      END.
      ELSE 
      ASSIGN  
          tot-billamt = tot-billamt + s1-list.amt
          tot-revamt  = tot-revamt + s1-list.ums
          s1-list.nr = curr-i
      .
  END.
  CREATE s1buff.
  ASSIGN
      s1buff.flag       = 1
      s1buff.nr         = curr-i
      s1buff.dept       = curr-dept
      s1buff.bezeich    = "T O T A L"
      s1buff.amt        = tot-billamt
      s1buff.ums        = tot-revamt
      curr-dept         = curr-dept
      curr-i            = curr-i + 1
  .
END.
