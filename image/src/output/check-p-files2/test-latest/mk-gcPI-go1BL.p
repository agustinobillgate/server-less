DEFINE TEMP-TABLE pbuff LIKE gc-pi.

DEF INPUT-OUTPUT PARAMETER TABLE FOR pbuff.
DEF INPUT PARAMETER billdate  AS DATE.
DEF INPUT PARAMETER rcvname   AS CHAR.
DEF INPUT PARAMETER pi-type   AS CHAR.
DEF INPUT PARAMETER bemerk    AS CHAR.
DEF INPUT PARAMETER pi-acctNo AS CHAR.
DEFINE OUTPUT PARAMETER pi-docuNo  AS CHAR INITIAL "".

FIND FIRST pbuff.
RUN go1.

PROCEDURE go1:
DEF VAR printer-nr   AS INTEGER NO-UNDO.
DEF BUFFER gc-pibuff FOR gc-pi.

    DO TRANSACTION:
      pbuff.pay-datum = billdate.
      FIND FIRST counters WHERE counters.counter-no = 42 EXCLUSIVE-LOCK
        NO-ERROR.
      IF NOT AVAILABLE counters THEN
      DO:
        CREATE counters.
        ASSIGN
            counters.counter-no = 42
            counters.counter-bez = "GC Proforma Invoice Counter No"
        .
      END.
      FIND FIRST gc-pibuff WHERE SUBSTR(gc-pibuff.docu-nr, 1, 9) 
          = ("PI" + STRING(MONTH(billdate),"99") + STRING(YEAR(billdate),"9999") 
          + "-") NO-LOCK NO-ERROR.
      IF NOT AVAILABLE gc-pibuff THEN ASSIGN counters.counter = 0.

      ASSIGN counters.counter = counters.counter + 1.
      IF counters.counter GT 9999 THEN counters.counter = 1.

      FIND CURRENT counters NO-LOCK.
      ASSIGN pbuff.docu-nr = "PI" + STRING(MONTH(billdate),"99")
                           + STRING(YEAR(billdate),"9999") + "-"
                           + STRING(counter.counter,"9999")
             pbuff.rcvname = rcvname
      .
      
      FIND FIRST gc-pitype WHERE 
          gc-pitype.bezeich = pi-type NO-LOCK.
      CREATE gc-PI.
      BUFFER-COPY pbuff TO gc-PI.
      ASSIGN 
          pi-docuNo        = pbuff.docu-nr
          gc-PI.rcvName    = rcvName
          gc-PI.bemerk     = bemerk
          gc-PI.pi-type    = gc-pitype.nr
          gc-PI.debit-fibu = pi-acctNo
      .
    END.
END.
