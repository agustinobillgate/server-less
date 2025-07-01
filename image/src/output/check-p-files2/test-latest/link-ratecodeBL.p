DEF INPUT PARAMETER child-code   AS CHAR    NO-UNDO.
DEF INPUT PARAMETER parent-code  AS CHAR    NO-UNDO.
DEF INPUT PARAMETER tb1-char3    AS CHAR    NO-UNDO.
DEF INPUT PARAMETER in-percent   AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER adjust-value AS DECIMAL NO-UNDO.

DEF TEMP-TABLE product-list
    FIELD market    AS INTEGER
    FIELD i-product AS INTEGER
.
DEF VARIABLE ci-date        AS DATE     NO-UNDO.
DEF VARIABLE round-betrag   AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE round-method   AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE length-round   AS INTEGER  NO-UNDO.
DEF VARIABLE curr-i         AS INTEGER  NO-UNDO.
DEF VARIABLE rate-str       AS CHAR     NO-UNDO.
DEF VARIABLE rounded-rate   AS DECIMAL  NO-UNDO.
DEF VARIABLE found-flag     AS LOGICAL  NO-UNDO.

DEF BUFFER rbuff  FOR ratecode.
DEF BUFFER prbuff FOR prtable.

FIND FIRST htparam WHERE htparam.paramnr = 1013 NO-LOCK.
IF htparam.feldtyp = 1 THEN
ASSIGN 
    round-betrag = htparam.finteger
    length-round = LENGTH(STRING(round-betrag))
.
ELSE IF htparam.feldtyp = 5 AND NUM-ENTRIES(htparam.fchar,";") GT 1 THEN
ASSIGN 
    round-betrag = INTEGER(ENTRY(1, htparam.fchar,";"))
    length-round = LENGTH(STRING(round-betrag))
    round-method = INTEGER(ENTRY(2, htparam.fchar,";")) NO-ERROR
.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK.
ASSIGN ci-date = htparam.fdate.

FOR EACH ratecode WHERE ratecode.CODE = child-code:
    FIND FIRST rbuff WHERE rbuff.CODE = parent-code
        AND rbuff.marknr  = ratecode.marknr
        AND rbuff.zikatnr = ratecode.zikatnr
        AND rbuff.argtnr  = ratecode.argtnr NO-LOCK NO-ERROR.
    IF AVAILABLE rbuff THEN DELETE ratecode.
END.

FOR EACH prtable WHERE prtable.prcode = child-code:
  DO curr-i = 1 TO 99:
    IF prtable.product[curr-i] = 0 THEN LEAVE.
/* SY 28/07/2014 */    
    IF prtable.product[curr-i] GE 90001 THEN
    FIND FIRST rbuff WHERE rbuff.CODE = prtable.prcode
        AND rbuff.marknr = prtable.marknr
        AND ((90 + rbuff.zikatnr) * 1000 + rbuff.argtnr) = prtable.product[curr-i]
        NO-LOCK NO-ERROR.    
    ELSE IF prtable.product[curr-i] GE 10001 THEN
    FIND FIRST rbuff WHERE rbuff.CODE = prtable.prcode
        AND rbuff.marknr = prtable.marknr
        AND (rbuff.zikatnr * 1000 + rbuff.argtnr) = prtable.product[curr-i]
        NO-LOCK NO-ERROR.    
    ELSE
    FIND FIRST rbuff WHERE rbuff.CODE = prtable.prcode
        AND rbuff.marknr = prtable.marknr
        AND (rbuff.zikatnr * 100 + rbuff.argtnr) = prtable.product[curr-i]
        NO-LOCK NO-ERROR.
    IF AVAILABLE rbuff THEN
    DO:
      CREATE product-list.
      ASSIGN
          product-list.market = prtable.marknr
          product-list.i-product = prtable.product[curr-i]
      .
    END.
  END.
  DELETE prtable.
END.

FOR EACH ratecode WHERE ratecode.CODE = parent-code 
    AND ratecode.endperiode GE ci-date NO-LOCK:
    CREATE rbuff.
    BUFFER-COPY ratecode EXCEPT CODE TO rbuff.
    ASSIGN rbuff.CODE = child-code.
    IF in-percent THEN 
    DO:    
        rbuff.zipreis = rbuff.zipreis * (1 + adjust-value * 0.01).
        IF round-betrag NE 0 AND rbuff.zipreis GE (round-betrag * 10) THEN
        DO:
            RUN round-it (rbuff.zipreis, OUTPUT rounded-rate).
            ASSIGN rbuff.zipreis = rounded-rate.
        END.
    END.
    ELSE rbuff.zipreis = rbuff.zipreis + adjust-value.
END.

FOR EACH prtable WHERE prtable.prcode = parent-code NO-LOCK:
    CREATE prbuff.
    BUFFER-COPY prtable EXCEPT prcode TO prbuff.
    ASSIGN prbuff.prcode = child-code.
    FOR EACH product-list WHERE product-list.market = prbuff.marknr:
        DO curr-i = 1 TO 99:
            IF prbuff.product[curr-i] = 0 THEN
            DO:
                ASSIGN 
                  prbuff.product[curr-i] = product-list.i-product.
                DELETE product-list.
                curr-i = 9999.
            END.
        END.
    END.
END.

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = child-code.
ASSIGN queasy.char3 = tb1-char3.
FIND CURRENT queasy NO-LOCK.

{ round-it.i }
