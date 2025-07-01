
DEF TEMP-TABLE t-printer1 LIKE printer.
DEF TEMP-TABLE t-printer2 LIKE printer.

DEF INPUT PARAMETER avail-t-h-bill  AS LOGICAL.
DEF INPUT PARAMETER from-acct       AS LOGICAL.
DEF INPUT PARAMETER prOrder         AS INT.
DEF INPUT PARAMETER prOrder2        AS INT.

DEF OUTPUT PARAMETER close-it       AS LOGICAL INIT YES.
DEF OUTPUT PARAMETER err-code1      AS INT INIT 0.
DEF OUTPUT PARAMETER err-code2      AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-printer1.
DEF OUTPUT PARAMETER TABLE FOR t-printer2.

IF avail-t-h-bill AND NOT from-acct THEN 
DO: 
    IF prOrder2 GT 0 THEN
    DO:
      FIND FIRST vhp.printer WHERE vhp.printer.nr = prOrder2 NO-LOCK NO-ERROR. 
      IF AVAILABLE vhp.PRINTER THEN close-it = NO.
    END.
    FIND FIRST vhp.printer WHERE vhp.printer.nr = prOrder NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE PRINTER OR (prOrder = 0) THEN
    DO:
        err-code1 = 1.
        RETURN NO-APPLY.
    END.
    err-code1 = 2.
    CREATE t-printer1.
    BUFFER-COPY printer TO t-printer1.
END. 
IF prOrder2 NE 0 THEN
DO:
    FIND FIRST vhp.printer WHERE vhp.printer.nr = prOrder2 NO-LOCK NO-ERROR. 
    IF NOT AVAILABLE PRINTER THEN
    DO:
      err-code2 = 1.
      RETURN NO-APPLY.
    END.
    err-code2 = 2.
    CREATE t-printer2.
    BUFFER-COPY printer TO t-printer2.
END.
