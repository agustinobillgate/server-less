
DEF INPUT PARAMETER child-code   AS CHAR    NO-UNDO.
DEF INPUT PARAMETER parent-code  AS CHAR    NO-UNDO.
DEF INPUT PARAMETER tb1-char3    AS CHAR    NO-UNDO.
DEF INPUT PARAMETER in-percent   AS LOGICAL NO-UNDO.
DEF INPUT PARAMETER adjust-value AS DECIMAL NO-UNDO.

/*
DEF VARIABLE child-code   AS CHAR    NO-UNDO INIT "IND1SDTZ".
DEF VARIABLE parent-code  AS CHAR    NO-UNDO INIT "BFR1".
DEF VARIABLE tb1-char3    AS CHAR    NO-UNDO INIT "IND;BFR1;%1100".
DEF VARIABLE in-percent   AS LOGICAL NO-UNDO INIT "YES".
DEF VARIABLE adjust-value AS DECIMAL NO-UNDO INIT "-10".
*/


DEF VARIABLE ci-date        AS DATE     NO-UNDO.
DEF VARIABLE round-betrag   AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE round-method   AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE length-round   AS INTEGER  NO-UNDO.
DEF VARIABLE rounded-rate   AS DECIMAL  NO-UNDO.
DEF VARIABLE prefix-str     AS CHAR     NO-UNDO INIT "A".

DEF BUFFER rbuff  FOR ratecode.

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

FOR EACH ratecode WHERE ratecode.CODE = child-code 
    AND ratecode.endperiode GE ci-date:
    FIND FIRST rbuff WHERE rbuff.marknr = ratecode.marknr 
        AND rbuff.code    = parent-code 
        AND rbuff.argtnr  = ratecode.argtnr
        AND rbuff.zikatnr = ratecode.zikatnr
        AND rbuff.erwachs = ratecode.erwachs
        AND rbuff.kind1   = ratecode.kind1
        AND rbuff.kind2   = ratecode.kind2
        AND rbuff.wday    = ratecode.wday
        AND rbuff.startperiode LE ratecode.startperiode
        AND rbuff.endperiode   GE ratecode.endperiode
        NO-LOCK NO-ERROR.
    IF AVAILABLE rbuff THEN 
    DO:    
        ratecode.zipreis = rbuff.zipreis.
        IF in-percent THEN 
        DO:    
            ratecode.zipreis = ratecode.zipreis * (1 + adjust-value * 0.01).
            IF round-betrag NE 0 AND ratecode.zipreis GE (round-betrag * 10) THEN 
            DO:
                RUN round-it (ratecode.zipreis, OUTPUT rounded-rate).
                ASSIGN ratecode.zipreis = rounded-rate.
            END.
        END.
        ELSE ratecode.zipreis = ratecode.zipreis + adjust-value.
    END.
END.

FIND FIRST queasy WHERE queasy.KEY = 2 AND queasy.char1 = child-code.

IF in-percent THEN prefix-str = "%".
queasy.char3 = ENTRY(1,tb1-char3,";") + ";"
             + ENTRY(2,tb1-char3,";") + ";" 
             + prefix-str + STRING(adjust-value * 100).

FIND CURRENT queasy NO-LOCK.

{ round-it.i }
