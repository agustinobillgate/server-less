DEF TEMP-TABLE t-list
    FIELD dept    AS INTEGER
    FIELD rechnr  AS INTEGER
    FIELD pay     AS DECIMAL INITIAL 0
    FIELD compli  AS DECIMAL INITIAL 0
.

DEF TEMP-TABLE p-list
    FIELD bstr    AS CHAR    FORMAT "x(1)"              LABEL " "
    FIELD dept    AS INTEGER FORMAT "99"                LABEL "Dept"
    FIELD billno  AS INTEGER FORMAT ">>>>>>>>9"         LABEL "FO-BillNo"
    FIELD posbill AS INTEGER FORMAT ">>>>>>>>9"         LABEL "POS-BillNo"
    FIELD billamt AS DECIMAL FORMAT "->>>,>>>,>>9.99"   LABEL "F/O Amount"
    FIELD posamt  AS DECIMAL FORMAT "->>>,>>>,>>9.99"   LABEL "POS Amount"
.

DEF TEMP-TABLE s-list
    FIELD dept AS INTEGER  FORMAT "99"              LABEL "Dept"
    FIELD artnr AS INTEGER FORMAT ">>>9"            LABEL "ArtNo"
    FIELD artart AS INTEGER
    FIELD bez AS CHAR FORMAT "x(32)"                LABEL "Description"
    FIELD betrag AS DECIMAL FORMAT "->>>,>>>,>>9"   LABEL "Bill Amount"
    FIELD ums AS DECIMAL FORMAT "->>>,>>>,>>9"      LABEL "Rev Amount"
    FIELD ums1 AS DECIMAL FORMAT "->>>,>>>,>>9"     LABEL "Argt RevAmt"
.

DEF TEMP-TABLE dept-list
    FIELD dptnr AS INTEGER.

DEF INPUT  PARAMETER currdate   AS DATE.
DEF OUTPUT PARAMETER gl-bal     AS DECIMAL.
DEF OUTPUT PARAMETER diff-u     AS DECIMAL.
DEF OUTPUT PARAMETER u          AS DECIMAL.
DEF OUTPUT PARAMETER diff-s     AS DECIMAL.
DEF OUTPUT PARAMETER s          AS DECIMAL.
DEF OUTPUT PARAMETER flag       AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR s-list.
DEF OUTPUT PARAMETER TABLE FOR p-list.

DEF VAR sysID      AS CHAR.
DEF VAR acct       AS CHAR.

FIND FIRST htparam WHERE htparam.paramnr = 104 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN sysID = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 998 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
  acct = htparam.fchar.
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = acct NO-LOCK.
END.

RUN check-dept.

FOR EACH gl-jouhdr WHERE gl-jouhdr.datum = currdate NO-LOCK:
    FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr
       AND gl-journal.fibukonto = acct NO-LOCK:
       gl-bal = gl-bal + gl-journal.debit - gl-journal.credit.
    END.
END.

FOR EACH umsatz WHERE umsatz.datum = currdate NO-LOCK,
    FIRST artikel WHERE artikel.artnr = umsatz.artnr
    AND artikel.departement = umsatz.departement NO-LOCK,
      FIRST dept-list WHERE dept-list.dptnr = umsatz.departement NO-LOCK:
    IF artart = 0 OR artart = 2 OR artart = 5 OR artart = 6 OR artart = 7 OR artart = 8
      THEN u = u + umsatz.betrag.
END.
diff-u = gl-bal - u.

FOR EACH bill-line WHERE bill-line.bill-datum EQ currdate NO-LOCK,
    FIRST dept-list WHERE dept-list.dptnr = bill-line.departement NO-LOCK:
    s = s + bill-line.betrag.
END.

diff-s = gl-bal - s.
  
IF (u - s) NE 0 THEN 
DO:    
    RUN create-fo.
    RUN create-fb.
    flag = YES.
END.

PROCEDURE check-dept:
    DEF VAR nm AS INTEGER NO-UNDO.
    FOR EACH dept-list:
        DELETE dept-list.
    END.
    FIND FIRST htparam WHERE paramnr = 793 NO-LOCK.
    IF fchar = "" THEN
    DO:
        FOR EACH hoteldpt NO-LOCK:
            CREATE dept-list.
            ASSIGN dept-list.dptnr = hoteldpt.num.
        END.
    END.
    ELSE
    DO:
        DO nm = 1 TO NUM-ENTRIES(fchar, ","):
            FIND FIRST hoteldpt WHERE hoteldpt.num = INTEGER(ENTRY(nm, fchar, ","))
                NO-LOCK NO-ERROR.
            IF AVAILABLE hoteldpt THEN
            DO:
                CREATE dept-list.
                ASSIGN dept-list.dptnr = hoteldpt.num.
            END.
        END.
    END.
END.

PROCEDURE create-fo:
DEF VAR pos-billNo AS INTEGER.
  FOR EACH s-list:
    DELETE s-list.
  END.

  FOR EACH bill-line WHERE bill-datum = currdate NO-LOCK:
    FIND FIRST artikel WHERE artikel.artnr = bill-line.artnr
        AND artikel.departement = bill-line.departement NO-LOCK.
    IF artikel.artart NE 1 THEN
    DO:
      FIND FIRST s-list WHERE s-list.artnr = bill-line.artnr
        AND s-list.dept = bill-line.departement NO-ERROR.
      IF NOT AVAILABLE s-list THEN
      DO:
        CREATE s-list.
        ASSIGN
          s-list.artnr = bill-line.artnr
          s-list.dept  = bill-line.departement
          s-list.bez   = artikel.bezeich
          s-list.artart = artikel.artart
        .
      END.
      ASSIGN s-list.betrag = s-list.betrag + bill-line.betrag.
    END.
    ELSE
    DO:
      pos-billNo = 0.
      pos-billNo = INTEGER(SUBSTR(bill-line.bezeich, 
        INDEX(bill-line.bezeich, " *") + 2)) NO-ERROR.
      FIND FIRST h-bill-line WHERE h-bill-line.departement = bill-line.departement
          AND h-bill-line.rechnr = pos-billNo
          AND h-bill-line.bezeich MATCHES("*" + STRING(bill-line.rechnr) + "*")
          AND h-bill-line.zeit LE bill-line.zeit
          AND h-bill-line.zeit GE (bill-line.zeit - 3)
          NO-LOCK NO-ERROR.
      IF AVAILABLE h-bill-line AND (h-bill-line.betrag + bill-line.betrag) NE 0 THEN
      DO:
          CREATE p-list.
          ASSIGN
              p-list.dept    = h-bill-line.departement
              p-list.billno  = bill-line.rechnr
              p-list.posbill = h-bill-line.rechnr
              p-list.billamt = - bill-line.betrag
              p-list.posamt  = h-bill-line.betrag
          .
      END.
    END.
  END.

  FOR EACH umsatz WHERE umsatz.datum = currdate NO-LOCK:
    FIND FIRST artikel WHERE artikel.artnr = umsatz.artnr
      AND artikel.departement = umsatz.departement NO-LOCK NO-ERROR.
    IF (AVAILABLE artikel AND artikel.artart NE 1 AND artikel.artart NE 9) THEN
    DO:
        FIND FIRST s-list WHERE s-list.artnr = umsatz.artnr
          AND s-list.dept = umsatz.departement NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
          CREATE s-list.
          ASSIGN
            s-list.artnr  = umsatz.artnr
            s-list.dept   = umsatz.departement
            s-list.artart = artikel.artart
          .
          IF AVAILABLE artikel THEN s-list.bez   = artikel.bezeich.
        END.
        ASSIGN s-list.ums = umsatz.betrag.
    END.
    ELSE IF NOT AVAILABLE artikel AND umsatz.betrag NE 0 THEN
    DO:
      HIDE MESSAGE NO-PAUSE.
      MESSAGE "No artikel record found following Revenue Record:"
          SKIP
          STRING(umsatz.departement,"99") + " " + STRING(umsatz.artnr)
          + " - " + STRING(umsatz.betrag)
          VIEW-AS ALERT-BOX WARNING.
    END.
  END.

  FOR EACH billjournal WHERE billjournal.bill-datum = currdate 
      AND billjournal.anzahl NE 0 AND billjournal.userinit = sysID NO-LOCK:
      FIND FIRST artikel WHERE artikel.artnr = billjournal.artnr
        AND artikel.departement = billjournal.departement NO-LOCK NO-ERROR.
      IF AVAILABLE artikel AND artikel.artart NE 9 THEN
      DO:
        FIND FIRST s-list WHERE s-list.artnr = billjournal.artnr
          AND s-list.dept = billjournal.departement NO-ERROR.
        IF NOT AVAILABLE s-list THEN
        DO:
          CREATE s-list. 
          ASSIGN
            s-list.artnr = billjournal.artnr
            s-list.dept  = billjournal.departement
            s-list.bez   = artikel.bezeich
            s-list.artart = artikel.artart
          .
        END.
        ASSIGN s-list.ums1 = s-list.ums1 + billjournal.betrag.
        ASSIGN s-list.ums  = s-list.ums  - billjournal.betrag.
      END.
      ELSE IF NOT AVAILABLE billjournal THEN
      DO:
        HIDE MESSAGE NO-PAUSE.
        MESSAGE "No artikel record found following Bill Journal Record:"
              SKIP
              STRING(billjournal.departement,"99") + " " 
              + STRING(billjournal.artnr) + " " + billjournal.bezeich
              + " - " + STRING(billjournal.betrag)
              VIEW-AS ALERT-BOX WARNING.
      END.
  END.
END.

PROCEDURE create-fb:
DEF VAR fo-billNo  AS INTEGER.
DEF VAR pos-billNo AS INTEGER INITIAL 0.
DEF VAR dept       AS INTEGER INITIAL 0.
DEF VAR balance    AS DECIMAL INITIAL 0.
  FOR EACH t-list:
      DELETE t-list.
  END.

  FOR EACH h-bill-line WHERE h-bill-line.bill-datum = currdate NO-LOCK
      BY h-bill-line.departement BY h-bill-line.rechnr:
      
      IF pos-billNo = 0 THEN
      DO:
        pos-billNo = h-bill-line.rechnr.
        dept = h-bill-line.departement.
      END.
      IF ((pos-billNo NE h-bill-line.rechnr) 
        OR (dept NE h-bill-line.departement)) THEN
      DO:
        IF balance NE 0 THEN
        DO:
          CREATE p-list.
          ASSIGN
            p-list.bstr    = "*"
            p-list.dept    = dept
            p-list.posbill = pos-billNo
            p-list.posamt  = balance
          .
        END.
        balance = 0.
        pos-billNo = h-bill-line.rechnr.
        dept = h-bill-line.departement.
      END.
      balance = balance + betrag.

      IF h-bill-line.artnr = 0 THEN
      DO:
        FIND FIRST t-list WHERE t-list.dept = h-bill-line.departement
            AND t-list.rechnr = h-bill-line.rechnr NO-ERROR.
        IF NOT AVAILABLE t-list THEN
        DO:
          CREATE t-list.
          ASSIGN
              t-list.dept   = h-bill-line.departement
              t-list.rechnr = h-bill-line.rechnr.
        END.
        t-list.pay = t-list.pay + h-bill-line.betrag.
      END.
      ELSE
      DO:
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
            AND h-artikel.departement = h-bill-line.departement NO-LOCK.
        IF h-artikel.artart NE 0 THEN
        DO:
          FIND FIRST t-list WHERE t-list.dept = h-bill-line.departement
            AND t-list.rechnr = h-bill-line.rechnr NO-ERROR.
          IF NOT AVAILABLE t-list THEN
          DO:
            CREATE t-list.
            ASSIGN
              t-list.dept   = h-bill-line.departement
              t-list.rechnr = h-bill-line.rechnr.
          END.
          IF h-artikel.artart LE 7 THEN 
              t-list.pay = t-list.pay + h-bill-line.betrag.
          ELSE t-list.compli = t-list.compli + h-bill-line.betrag.
        END.
      END.
  END.
  IF balance NE 0 THEN
  DO:
    CREATE p-list.
    ASSIGN
        p-list.bstr    = "*"
        p-list.dept    = dept
        p-list.posbill = pos-billNo
        p-list.posamt  = balance
    .
  END.

  FOR EACH t-list WHERE t-list.pay NE 0:
    FOR EACH h-bill-line WHERE h-bill-line.rechnr = t-list.rechnr
      AND h-bill-line.departement = t-list.dept NO-LOCK
      BY h-bill-line.departement BY h-bill-line.rechnr:
      IF h-bill-line.artnr NE 0 THEN
      DO:
        FIND FIRST h-artikel WHERE h-artikel.artnr = h-bill-line.artnr
          AND h-artikel.departement = h-bill-line.departement NO-LOCK.
        IF h-artikel.artart LE 7 THEN
        DO:
          IF h-artikel.artart = 0 THEN
          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
            AND artikel.departement = h-artikel.departement NO-LOCK.
          ELSE
          FIND FIRST artikel WHERE artikel.artnr = h-artikel.artnrfront
            AND artikel.departement = 0 NO-LOCK.
          FIND FIRST umsatz WHERE umsatz.artnr = artikel.artnr
              AND umsatz.departement = artikel.artnr
              AND umsatz.datum = currdate NO-LOCK NO-ERROR.
          FIND FIRST s-list WHERE s-list.artnr = artikel.artnr
            AND s-list.dept = artikel.departement NO-ERROR.
          IF NOT AVAILABLE s-list THEN
          DO:
            CREATE s-list.
            ASSIGN s-list.bez = artikel.bezeich.
            IF AVAILABLE umsatz THEN
            ASSIGN
              s-list.artnr = umsatz.artnr
              s-list.dept  = umsatz.departement
              s-list.ums = umsatz.betrag
            .
          END.
          s-list.betrag = s-list.betrag + h-bill-line.betrag.
        END.
      END.
      ELSE
      DO:
        fo-billNo = 0.
        fo-billNo = INTEGER(SUBSTR(h-bill-line.bezeich, 
          INDEX(h-bill-line.bezeich, " *") + 2)) NO-ERROR.
        FIND FIRST billjournal WHERE billjournal.rechnr = fo-billNo 
            AND billjournal.bill-datum = h-bill-line.bill-datum
            AND billjournal.bezeich MATCHES("*" + STRING(h-bill-line.rechnr) + "*")
            AND billjournal.zeit GE h-bill-line.zeit
            AND billjournal.zeit LE (h-bill-line.zeit + 3)
            NO-LOCK NO-ERROR.
        IF AVAILABLE billjournal 
          AND (h-bill-line.betrag + billjournal.betrag) NE 0 THEN
        DO:
          CREATE p-list.
          ASSIGN
              p-list.dept    = h-bill-line.departement
              p-list.billno  = billjournal.rechnr
              p-list.posbill = h-bill-line.rechnr
              p-list.billamt = billjournal.betrag
              p-list.posamt  = - h-bill-line.betrag
          .
        END.
        ELSE IF NOT AVAILABLE billjournal THEN 
        DO:
          CREATE p-list.
          ASSIGN
              p-list.dept    = h-bill-line.departement
              p-list.posbill = h-bill-line.rechnr
              p-list.posamt  = - h-bill-line.betrag
          .
        END.
      END.
    END.
  END.
  FOR EACH s-list WHERE s-list.ums = 0 AND s-list.betrag = 0 AND s-list.ums1 = 0:
      DELETE s-list.
  END.

END.

