DEFINE TEMP-TABLE g-list
    FIELD grecid AS INTEGER
    FIELD fibu   AS CHAR
    INDEX fibu_ix fibu.
DEFINE TEMP-TABLE summary-list
  FIELD acctno AS CHARACTER
  FIELD bezeich AS CHARACTER
  FIELD beg-balance AS DECIMAL
  FIELD t-debit AS DECIMAL
  FIELD t-credit AS DECIMAL
  FIELD net-change AS DECIMAL
  FIELD end-balance AS DECIMAL
  FIELD ytd-balance AS DECIMAL.

DEFINE TEMP-TABLE detail-list
  FIELD datum AS DATE
  FIELD refno AS CHARACTER
  FIELD bezeich AS CHARACTER
  FIELD t-debit AS DECIMAL
  FIELD t-credit AS DECIMAL
  FIELD net-change AS DECIMAL
  FIELD end-balance AS DECIMAL
  FIELD note AS CHARACTER.

DEF INPUT PARAMETER from-depart AS INTEGER.
DEF INPUT PARAMETER from-date   AS DATE .
DEF INPUT PARAMETER to-date     AS DATE.
DEF INPUT PARAMETER close-month AS INTEGER.
DEF INPUT PARAMETER sorttype    AS INTEGER.
DEF INPUT PARAMETER from-fibu   AS CHAR.
DEF INPUT PARAMETER to-fibu     AS CHAR.
DEF INPUT PARAMETER pnl-acct    AS CHAR.
DEF INPUT PARAMETER pbal-flag   AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR summary-list.
DEF OUTPUT PARAMETER TABLE FOR detail-list.

DEFINE VARIABLE sales       AS DECIMAL. 
DEFINE VARIABLE cost        AS DECIMAL. 
DEFINE VARIABLE gop-credit  AS DECIMAL. 
DEFINE VARIABLE gop-debit   AS DECIMAL. 
DEFINE VARIABLE tot-diff    AS DECIMAL. 
DEFINE VARIABLE close-date  AS DATE. 

FUNCTION get-bemerk RETURNS CHAR(bemerk AS CHAR): 
DEF VAR n AS INTEGER. 
DEF VAR s1 AS CHAR. 
  n = INDEX(bemerk, ";&&"). 
  IF n > 0 THEN RETURN SUBSTR(bemerk, 1, n - 1). 
  ELSE RETURN bemerk. 
END. 

MESSAGE "masuk sini" month(from-date) to-date VIEW-AS ALERT-BOX.

FIND FIRST htparam WHERE paramnr = 597 no-lock.    /* Curr Accounting Period */ 
close-date = htparam.fdate. 

RUN create-glist.

IF from-depart GT 0 THEN RUN create-trial-list1. 
ELSE RUN create-trial-list2. 


PROCEDURE create-glist:
    FOR EACH g-list:
        DELETE g-list.
    END.

    IF from-depart GT 0 THEN
    FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date
        AND gl-jouhdr.datum LE to-date NO-LOCK BY gl-jouhdr.datum:
        FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK,
            FIRST gl-acct WHERE gl-acct.deptnr = from-depart NO-LOCK:
            CREATE g-list.
            ASSIGN
                g-list.grecid = RECID(gl-journal)
                g-list.fibu   = gl-journal.fibukonto.
        END.
    END.
    ELSE
    FOR EACH gl-jouhdr WHERE gl-jouhdr.datum GE from-date
        AND gl-jouhdr.datum LE to-date NO-LOCK BY gl-jouhdr.datum:
        FOR EACH gl-journal WHERE gl-journal.jnr = gl-jouhdr.jnr NO-LOCK,
          FIRST gl-acct WHERE gl-acct.fibukonto = gl-journal.fibukonto
            AND gl-acct.acc-type NE 3 AND gl-acct.acc-type NE 4 NO-LOCK:
            CREATE g-list.
            ASSIGN
                g-list.grecid = RECID(gl-journal)
                g-list.fibu   = gl-journal.fibukonto.
        END.
    END.
END.

PROCEDURE create-trial-list1: 
DEFINE VARIABLE konto LIKE gl-acct.fibukonto INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE ind AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-month AS INTEGER. 
 
DEFINE VARIABLE t-debit AS DECIMAL.
DEFINE VARIABLE t-credit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE p-bal AS DECIMAL. 
DEFINE VARIABLE t-bal AS DECIMAL. 
DEFINE VARIABLE y-bal AS DECIMAL. 
 
DEFINE VARIABLE tot-debit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-credit LIKE t-credit INITIAL 0. 
DEFINE VARIABLE t-ybal AS DECIMAL.
DEFINE VARIABLE tt-ybal AS DECIMAL.
 
DEFINE VARIABLE prev-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE diff AS DECIMAL. 
 
DEFINE VARIABLE tt-debit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-credit LIKE t-credit INITIAL 0. 
DEFINE VARIABLE tt-pbal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-diff AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE act-flag AS INTEGER INITIAL 0. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE buffer gl-account FOR gl-acct. 
 
  sales = 0. 
  cost = 0. 
  gop-credit = 0. 
  gop-debit = 0. 
  tot-diff = 0. 
 
  IF to-date LE DATE(month(close-date), 1, year(close-date)) - 1 THEN 
    act-flag = 1. 
 
  curr-month = close-month. 

  IF sorttype = 1 THEN 
  DO: 
    FOR EACH gl-acct WHERE gl-acct.fibukonto GE from-fibu 
      AND gl-acct.fibukonto LE to-fibu 
      AND gl-acct.deptnr = from-depart 
      AND (gl-acct.acc-type = 1 OR gl-acct.acc-type = 2 OR gl-acct.acc-type = 5) 
      NO-LOCK BY gl-acct.fibukonto:
      CREATE detail-list.
      RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
      detail-list.refno = c.
      detail-list.bezeich = gl-acct.bezeich.
      
      ASSIGN
        t-debit = 0
        t-credit = 0
        p-bal = 0
        t-bal = 0
        konto = gl-acct.fibukonto.
 
      FOR EACH g-list WHERE g-list.fibu EQ gl-acct.fibukonto 
          USE-INDEX fibu_ix:
        FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
        FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
        DELETE g-list.

        IF gl-acct.fibukonto = pnl-acct THEN 
        DO: 
          gop-credit = gop-credit + gl-journal.credit. 
          gop-debit = gop-debit + gl-journal.debit. 
        END. 
 
        IF gl-acct.acc-type = 1 THEN 
          sales = sales + gl-journal.credit - gl-journal.debit. 
        ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
          cost = cost + gl-journal.debit - gl-journal.credit. 
 
        t-debit = t-debit + gl-journal.debit. 
        t-credit = t-credit + gl-journal.credit. 
 
        IF acc-type = 1 OR acc-type = 4 THEN 
          t-bal = t-bal - gl-journal.debit + gl-journal.credit. 
        ELSE t-bal = t-bal + gl-journal.debit - gl-journal.credit. 
 
        tot-debit = tot-debit + gl-journal.debit. 
        tot-credit = tot-credit + gl-journal.credit. 
        IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
            tot-bal = tot-bal - gl-journal.debit + gl-journal.credit. 
        ELSE tot-bal = tot-bal + gl-journal.debit - gl-journal.credit. 
 
        
        CREATE detail-list.
        ASSIGN
          detail-list.datum = gl-jouhdr.datum
          detail-list.refno = gl-jouhdr.refno
          detail-list.t-debit = gl-journal.debit
          detail-list.t-credit = gl-journal.credit
          detail-list.note = get-bemerk(gl-journal.bemerk).
      END. 
          
      IF p-bal NE 0 OR t-debit NE 0 OR t-credit NE 0 THEN 
      DO: 
        IF acc-type = 1 OR acc-type = 4 THEN 
        DO: 
          diff = t-credit - t-debit. 
          tot-diff = tot-diff + t-credit - t-debit. 
        END. 
        ELSE 
        DO: 
          diff = t-debit - t-credit. 
          tot-diff = tot-diff - t-credit + t-debit. 
        END. 
        
        CREATE detail-list.
        ASSIGN
          detail-list.refno = "T O T A L"
          detail-list.t-debit = t-debit
          detail-list.t-credit = t-credit
          detail-list.net-change = diff
          detail-list.end-balance = t-bal.

        CREATE detail-list.
      END. 
      ELSE
      DO:
        /* have NO journals ==> record deleted */ 
        DELETE detail-list.
      END.                   
    END. 
 
    IF prev-bal NE 0 OR tot-debit NE 0 OR tot-credit NE 0 THEN 
    DO: 
        CREATE detail-list.
        ASSIGN
          detail-list.refno = "Grand TOTAL"
          detail-list.t-debit = tot-debit
          detail-list.t-credit = tot-credit
          detail-list.net-change = tot-diff
          detail-list.end-balance = tot-bal.
    END.                                    
  END.                                      
  ELSE IF sorttype = 2 THEN 
  DO: 
    FOR EACH gl-department WHERE gl-department.nr = from-depart NO-LOCK: 
      prev-bal = 0. 
      tot-debit = 0. 
      tot-credit = 0. 
      t-ybal = 0. 
      tot-bal = 0. 
      diff = 0. 
      tot-diff = 0. 
      CREATE summary-list.
      summary-list.bezeich = STRING(gl-depart.nr, ">>9") + " - " 
        + SUBSTR(gl-depart.bezeich, 1, 32). 
      FOR EACH gl-acct WHERE gl-acct.deptnr = gl-depart.nr 
        NO-LOCK BY gl-acct.fibukonto: 
        t-debit = 0. 
        t-credit = 0. 
        p-bal = 0. 
        t-bal = 0. 
        y-bal = 0. 
        konto = gl-acct.fibukonto. 
 
        FOR EACH g-list WHERE g-list.fibu EQ gl-acct.fibukonto 
            USE-INDEX fibu_ix:
          FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
          FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
          DELETE g-list.
 
          IF gl-acct.fibukonto = pnl-acct THEN 
          DO: 
            gop-credit = gop-credit + gl-journal.credit. 
            gop-debit = gop-debit + gl-journal.debit. 
          END. 
 
          IF gl-acct.acc-type = 1 THEN 
            sales = sales + gl-journal.credit - gl-journal.debit. 
          ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
            cost = cost + gl-journal.debit - gl-journal.credit. 
 
          t-debit = t-debit + gl-journal.debit. 
          t-credit = t-credit + gl-journal.credit. 
 
          tot-debit = tot-debit + gl-journal.debit. 
          tot-credit = tot-credit + gl-journal.credit. 
 
          tt-debit = tt-debit + gl-journal.debit. 
          tt-credit = tt-credit + gl-journal.credit. 
 
          IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
            t-bal = t-bal - gl-journal.debit + gl-journal.credit. 
          ELSE t-bal = t-bal + gl-journal.debit - gl-journal.credit. 
          tot-bal = tot-bal - gl-journal.debit + gl-journal.credit. 
          tt-bal = tt-bal - gl-journal.debit + gl-journal.credit. 
        END. 
        IF gl-acct.acc-type = 1 THEN 
        DO: 
          IF year(close-date) = year(to-date) THEN 
          DO n = 1 TO month(to-date): 
            IF n LT month(to-date) AND pbal-flag THEN 
              p-bal = p-bal - gl-acct.actual[n]. 
            y-bal = y-bal - gl-acct.actual[n]. 
          END. 
          ELSE IF year(close-date) = year(to-date) + 1 THEN 
          DO n = 1 TO month(to-date): 
            IF n LT month(to-date) AND pbal-flag THEN 
              p-bal = p-bal - gl-acct.last-yr[n]. 
            y-bal = y-bal - gl-acct.last-yr[n]. 
          END. 
          t-ybal = t-ybal + y-bal. 
          tt-ybal = tt-ybal + y-bal. 
        END. 
        ELSE IF (gl-acct.acc-type = 2 OR gl-acct.acc-type = 5) THEN 
        DO: 
          IF year(close-date) = year(to-date) THEN 
          DO n = 1 TO month(to-date): 
            IF n LT month(to-date) AND pbal-flag THEN 
              p-bal = p-bal + gl-acct.actual[n]. 
            y-bal = y-bal + gl-acct.actual[n]. 
          END. 
          ELSE IF year(close-date) = year(to-date) - 1 THEN 
          DO n = 1 TO month(to-date): 
            IF n LT month(to-date) AND pbal-flag THEN 
              p-bal = p-bal + gl-acct.last-yr[n]. 
            y-bal = y-bal + gl-acct.last-yr[n]. 
          END. 
          t-ybal = t-ybal - y-bal. 
          tt-ybal = tt-ybal - y-bal. 
        END. 
        IF p-bal NE 0 OR t-debit NE 0 OR t-credit NE 0 
          OR y-bal NE 0 THEN 
        DO: 
          CREATE summary-list.
          RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
          ASSIGN
            summary-list.acctno = c
            summary-list.bezeich = gl-acct.bezeich
            summary-list.beg-balance = p-bal
            summary-list.t-debit = t-debit
            summary-list.t-credit = t-credit
          .
          IF gl-acct.acc-type = 1 OR gl-acct.acc-typ = 4 THEN 
            diff = - t-debit + t-credit. 
          ELSE diff = t-debit - t-credit. 
          tot-diff = tot-diff + t-credit - t-debit. 
          tt-diff = tt-diff + t-credit - t-debit.
          ASSIGN
            summary-list.net-change = diff
            summary-list.end-balance = t-bal
            summary-list.ytd-balance = y-bal.
        END. 
      END. 
 
      CREATE summary-list.
      ASSIGN
        summary-list.bezeich = " S U B T O T A L"
        summary-list.beg-balance = prev-bal
        summary-list.t-debit = tot-debit
        summary-list.t-credit = tot-credit
        summary-list.net-change = tot-diff
        summary-list.end-bal = tot-bal
        summary-list.ytd-bal = t-ybal.
      CREATE summary-list.
    END. 
    CREATE summary-list.
    ASSIGN
      summary-list.bezeich = "T O T A L"
      summary-list.beg-bal = tt-pbal
      summary-list.t-debit = tt-debit
      summary-list.t-credit = tt-credit
      summary-list.net-change = tt-diff
      summary-list.end-bal = tt-bal
      summary-list.ytd-bal = tt-ybal.
  END. 
END. 
 
PROCEDURE create-trial-list2: 
DEFINE VARIABLE konto LIKE gl-acct.fibukonto INITIAL "". 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE c AS CHAR. 
DEFINE VARIABLE ind AS INTEGER INITIAL 0. 
DEFINE VARIABLE curr-month AS INTEGER. 
 
DEFINE VARIABLE t-debit AS DECIMAL.
DEFINE VARIABLE t-credit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE p-bal AS DECIMAL. 
DEFINE VARIABLE t-bal AS DECIMAL. 
DEFINE VARIABLE y-bal AS DECIMAL. 
 
DEFINE VARIABLE tot-debit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-credit LIKE t-credit INITIAL 0. 
DEFINE VARIABLE t-ybal AS DECIMAL.
DEFINE VARIABLE tt-ybal AS DECIMAL.
 
DEFINE VARIABLE prev-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tot-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE diff AS DECIMAL. 
 
DEFINE VARIABLE tt-debit LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-credit LIKE t-credit INITIAL 0. 
DEFINE VARIABLE tt-pbal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-bal LIKE t-debit INITIAL 0. 
DEFINE VARIABLE tt-diff AS DECIMAL INITIAL 0. 
 
DEFINE VARIABLE act-flag AS INTEGER INITIAL 0. 
DEFINE VARIABLE n AS INTEGER. 
DEFINE buffer gl-account FOR gl-acct. 
 
  sales = 0. 
  cost = 0. 
  gop-credit = 0. 
  gop-debit = 0. 
  tot-diff = 0. 
 
  IF to-date LE DATE(month(close-date), 1, year(close-date)) - 1 THEN 
    act-flag = 1. 
 
  curr-month = close-month. 

  IF sorttype = 1 THEN 
  FOR EACH gl-department WHERE gl-department.nr GT 0 NO-LOCK BY
    gl-department.nr:
    CREATE detail-list.
    CREATE detail-list.
    detail-list.bezeich = gl-department.bezeich.

    FOR EACH gl-acct WHERE gl-acct.fibukonto GE from-fibu 
      AND gl-acct.fibukonto LE to-fibu 
      AND gl-acct.deptnr = gl-department.nr 
      AND (gl-acct.acc-type = 1 OR gl-acct.acc-type = 2 OR gl-acct.acc-type = 5) 
      NO-LOCK BY gl-acct.fibukonto: 
      RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
      CREATE detail-list.
      ASSIGN
        detail-list.refno = c
        detail-list.bezeich = gl-acct.bezeich.

      t-debit = 0. 
      t-credit = 0. 
      p-bal = 0. 
      t-bal = 0. 
      konto = gl-acct.fibukonto. 
 
      FOR EACH g-list WHERE g-list.fibu EQ gl-acct.fibukonto 
          USE-INDEX fibu_ix:
        FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
        FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
        DELETE g-list.

        IF gl-acct.fibukonto = pnl-acct THEN 
        DO: 
          gop-credit = gop-credit + gl-journal.credit. 
          gop-debit = gop-debit + gl-journal.debit. 
        END. 
 
        IF gl-acct.acc-type = 1 THEN 
          sales = sales + gl-journal.credit - gl-journal.debit. 
        ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
          cost = cost + gl-journal.debit - gl-journal.credit. 
 
        t-debit = t-debit + gl-journal.debit. 
        t-credit = t-credit + gl-journal.credit. 
 
        IF acc-type = 1 OR acc-type = 4 THEN 
          t-bal = t-bal - gl-journal.debit + gl-journal.credit. 
        ELSE t-bal = t-bal + gl-journal.debit - gl-journal.credit. 
 
        tot-debit = tot-debit + gl-journal.debit. 
        tot-credit = tot-credit + gl-journal.credit. 
        IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
            tot-bal = tot-bal - gl-journal.debit + gl-journal.credit. 
        ELSE tot-bal = tot-bal + gl-journal.debit - gl-journal.credit. 
 
        CREATE detail-list.
        ASSIGN
          detail-list.datum = gl-jouhdr.datum
          detail-list.refno = gl-jouhdr.refno
          detail-list.t-debit = gl-journal.debit
          detail-list.t-credit = gl-journal.credit
          detail-list.note = get-bemerk(gl-journal.bemerk).
      END. 
          
      IF p-bal NE 0 OR t-debit NE 0 OR t-credit NE 0 THEN 
      DO: 
        IF acc-type = 1 OR acc-type = 4 THEN 
        DO: 
          diff = t-credit - t-debit. 
          tot-diff = tot-diff + t-credit - t-debit. 
        END. 
        ELSE 
        DO: 
          diff = t-debit - t-credit. 
          tot-diff = tot-diff - t-credit + t-debit. 
        END. 
        CREATE detail-list.
        ASSIGN
          detail-list.refno = "T O T A L"
          detail-list.t-debit = t-debit
          detail-list.t-credit = t-credit
          detail-list.net-change = diff
          detail-list.end-bal = t-bal.
        CREATE detail-list.
      END. 
      ELSE
      DO:
        /* have NO journals ==> record deleted */ 
        DELETE detail-list.
      END.
    END. 
  END.
  IF sorttype = 1 AND (prev-bal NE 0 OR tot-debit NE 0 OR tot-credit NE 0) THEN 
  DO: 
    tot-diff = tot-credit - tot-debit.
    tot-bal  = tot-diff.

    CREATE detail-list.
    ASSIGN
      detail-list.refno = "Grand TOTAL"
      detail-list.t-debit = tot-debit
      detail-list.t-credit = tot-credit
      detail-list.net-change = tot-diff
      detail-list.end-bal = tot-bal.
  END. 

  IF sorttype = 2 THEN 
  DO: 
    FOR EACH gl-department WHERE gl-department.nr GT 0 NO-LOCK, 
      FIRST gl-account WHERE gl-account.deptnr = gl-department.nr 
      BY gl-department.nr: 
      prev-bal = 0. 
      tot-debit = 0. 
      tot-credit = 0. 
      t-ybal = 0. 
      tot-bal = 0. 
      diff = 0. 
      tot-diff = 0. 
      CREATE summary-list.
      ASSIGN
        summary-list.bezeich = STRING(gl-depart.nr, ">>9") + " - " 
        + SUBSTR(gl-depart.bezeich, 1, 32). 
      FOR EACH gl-acct WHERE gl-acct.deptnr = gl-depart.nr 
        NO-LOCK BY gl-acct.fibukonto: 
        t-debit = 0. 
        t-credit = 0. 
        p-bal = 0. 
        t-bal = 0. 
        y-bal = 0. 
        konto = gl-acct.fibukonto. 
 
        FOR EACH g-list WHERE g-list.fibu EQ gl-acct.fibukonto 
            USE-INDEX fibu_ix:
          FIND FIRST gl-journal WHERE RECID(gl-journal) = g-list.grecid NO-LOCK.
          FIND FIRST gl-jouhdr WHERE gl-jouhdr.jnr = gl-journal.jnr NO-LOCK NO-ERROR.
          DELETE g-list.
 
          IF gl-acct.fibukonto = pnl-acct THEN 
          DO: 
            gop-credit = gop-credit + gl-journal.credit. 
            gop-debit = gop-debit + gl-journal.debit. 
          END. 
 
          IF gl-acct.acc-type = 1 THEN 
            sales = sales + gl-journal.credit - gl-journal.debit. 
          ELSE IF gl-acct.acc-type = 2 OR gl-acct.acc-type = 5 THEN 
            cost = cost + gl-journal.debit - gl-journal.credit. 
 
          t-debit = t-debit + gl-journal.debit. 
          t-credit = t-credit + gl-journal.credit. 
 
          tot-debit = tot-debit + gl-journal.debit. 
          tot-credit = tot-credit + gl-journal.credit. 
 
          tt-debit = tt-debit + gl-journal.debit. 
          tt-credit = tt-credit + gl-journal.credit. 
 
          IF gl-acct.acc-type = 1 OR gl-acct.acc-type = 4 THEN 
            t-bal = t-bal - gl-journal.debit + gl-journal.credit. 
          ELSE t-bal = t-bal + gl-journal.debit - gl-journal.credit. 
          tot-bal = tot-bal - gl-journal.debit + gl-journal.credit. 
          tt-bal = tt-bal - gl-journal.debit + gl-journal.credit. 
        END. 
        IF gl-acct.acc-type = 1 THEN 
        DO: 
          IF year(close-date) = year(to-date) THEN 
          DO n = 1 TO month(to-date): 
            IF n LT month(to-date) AND pbal-flag THEN 
              p-bal = p-bal - gl-acct.actual[n]. 
            y-bal = y-bal - gl-acct.actual[n]. 
          END. 
          ELSE IF year(close-date) = year(to-date) + 1 THEN 
          DO n = 1 TO month(to-date): 
            IF n LT month(to-date) AND pbal-flag THEN 
              p-bal = p-bal - gl-acct.last-yr[n]. 
            y-bal = y-bal - gl-acct.last-yr[n]. 
          END. 
          t-ybal = t-ybal + y-bal. 
          tt-ybal = tt-ybal + y-bal. 
        END. 
        ELSE IF (gl-acct.acc-type = 2 OR gl-acct.acc-type = 5) THEN 
        DO: 
          IF year(close-date) = year(to-date) THEN 
          DO n = 1 TO month(to-date): 
            IF n LT month(to-date) AND pbal-flag THEN 
              p-bal = p-bal + gl-acct.actual[n]. 
            y-bal = y-bal + gl-acct.actual[n]. 
          END. 
          ELSE IF year(close-date) = year(to-date) - 1 THEN 
          DO n = 1 TO month(to-date): 
            IF n LT month(to-date) AND pbal-flag THEN 
              p-bal = p-bal + gl-acct.last-yr[n]. 
            y-bal = y-bal + gl-acct.last-yr[n]. 
          END. 
          t-ybal = t-ybal - y-bal. 
          tt-ybal = tt-ybal - y-bal. 
        END. 
        IF p-bal NE 0 OR t-debit NE 0 OR t-credit NE 0 
          OR y-bal NE 0 THEN 
        DO: 
          RUN convert-fibu(gl-acct.fibukonto, OUTPUT c). 
          CREATE summary-list.
          ASSIGN
            summary-list.acctno = c
            summary-list.bezeich = gl-acct.bezeich
            summary-list.beg-bal = p-bal
            summary-list.t-debit = t-debit
            summary-list.t-credit = t-credit.
          IF gl-acct.acc-type = 1 OR gl-acct.acc-typ = 4 THEN 
            diff = - t-debit + t-credit. 
          ELSE diff = t-debit - t-credit. 
          tot-diff = tot-diff + t-credit - t-debit. 
          tt-diff = tt-diff + t-credit - t-debit. 
          ASSIGN 
            summary-list.net-change = diff
            summary-list.end-bal = t-bal
            summary-list.ytd-bal = y-bal.
        END. 
      END. 
 
      CREATE summary-list.
      ASSIGN
        summary-list.bezeich = "S U B T O T A L"
        summary-list.beg-bal = prev-bal
        summary-list.t-debit = tot-debit
        summary-list.t-credit = tot-credit
        summary-list.net-change = tot-diff
        summary-list.end-bal = tot-bal
        summary-list.ytd-bal = t-ybal.
      CREATE summary-list.
    END. 
    CREATE summary-list.
    ASSIGN
      summary-list.bezeich = "T O T A L"
      summary-list.beg-bal = tt-pbal
      summary-list.t-debit = tt-debit
      summary-list.t-credit = tt-credit
      summary-list.net-change = tt-diff
      summary-list.end-bal = tt-bal
      summary-list.ytd-bal = tt-ybal.
  END.
END. 

PROCEDURE convert-fibu: 
DEFINE INPUT PARAMETER konto AS CHAR. 
DEFINE OUTPUT PARAMETER s AS CHAR INITIAL "". 
DEFINE VARIABLE ch AS CHAR. 
DEFINE VARIABLE i AS INTEGER. 
DEFINE VARIABLE j AS INTEGER. 
  FIND FIRST htparam WHERE paramnr = 977 NO-LOCK. 
  ch = htparam.fchar. 
  j = 0. 
  DO i = 1 TO length(ch): 
    IF SUBSTR(ch, i, 1) GE "0" AND SUBSTR(ch, i, 1) LE  "9" THEN 
    DO: 
      j = j + 1. 
      s = s + SUBSTR(konto, j, 1). 
    END. 
    ELSE s = s + SUBSTR(ch, i, 1). 
  END. 
END. 
