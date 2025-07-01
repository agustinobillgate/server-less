DEF INPUT  PARAMETER dept            AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER c-param870      AS CHAR    NO-UNDO.
DEF OUTPUT PARAMETER double-currency AS LOGICAL NO-UNDO.
DEF OUTPUT PARAMETER voucher-found   AS LOGICAL NO-UNDO.

RUN htpchar.p (870, OUTPUT c-param870).
RUN htplogic.p (240, OUTPUT double-currency).

FIND FIRST htparam WHERE htparam.paramnr = 1001 NO-LOCK. 
IF htparam.finteger > 0 THEN 
DO: 
  FIND FIRST h-artikel WHERE h-artikel.artnr = htparam.finteger 
    AND h-artikel.departement = dept NO-LOCK NO-ERROR. 
  voucher-found = AVAILABLE h-artikel. 
END. 
