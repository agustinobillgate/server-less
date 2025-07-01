
DEF INPUT  PARAMETER case-type      AS INT.
DEF INPUT  PARAMETER bill-no        AS CHAR.
DEF INPUT  PARAMETER i-datum        AS DATE.
DEF OUTPUT PARAMETER datum          AS DATE.
DEF OUTPUT PARAMETER saldo          AS DECIMAL.
DEF OUTPUT PARAMETER avail-kredit   AS LOGICAL INIT NO.

IF case-type = 1 THEN
DO:
    FIND FIRST l-kredit WHERE l-kredit.lscheinnr = bill-no 
    AND l-kredit.zahlkonto = 0 AND l-kredit.counter NE 0 NO-LOCK NO-ERROR. 
    IF AVAILABLE l-kredit THEN 
    DO:
       avail-kredit = YES.
       datum = l-kredit.rgdatum.
       saldo = l-kredit.saldo.
    END.
END.
ELSE IF case-type = 2 THEN
DO:
  FIND FIRST l-kredit WHERE l-kredit.lscheinnr = bill-no 
    AND l-kredit.rgdatum = i-datum 
    AND l-kredit.zahlkonto = 0 
    AND l-kredit.counter NE 0 NO-LOCK NO-ERROR.
  IF AVAILABLE l-kredit THEN 
      ASSIGN saldo = l-kredit.saldo
             avail-kredit = YES.
END.
