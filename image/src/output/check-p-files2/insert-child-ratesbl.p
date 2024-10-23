DEF INPUT PARAMETER child-code  AS CHAR NO-UNDO.
DEF INPUT PARAMETER from-date   AS DATE NO-UNDO.
DEF INPUT PARAMETER to-date     AS DATE NO-UNDO.
DEF OUTPUT PARAMETER found-flag AS LOGICAL NO-UNDO INIT NO.

DEF TEMP-TABLE child-ratecode LIKE ratecode.

DEF BUFFER rbuff FOR ratecode.

DEF VARIABLE parent-code  AS CHAR    NO-UNDO.
DEF VARIABLE in-percent   AS LOGICAL NO-UNDO.
DEF VARIABLE adjust-value AS DECIMAL NO-UNDO.
DEF VARIABLE round-betrag AS INTEGER NO-UNDO.
DEF VARIABLE round-method AS INTEGER  NO-UNDO INIT 0.
DEF VARIABLE length-round AS INTEGER NO-UNDO.
DEF VARIABLE rounded-rate AS DECIMAL NO-UNDO.

FIND FIRST queasy WHERE queasy.KEY = 2
    AND queasy.char1 = child-code NO-LOCK.

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
ASSIGN 
    parent-code  = ENTRY(2, queasy.char3, ";")
    in-percent   = SUBSTR(ENTRY(3, queasy.char3, ";"),1,1) = "%"
    adjust-value = DECIMAL(SUBSTR(ENTRY(3, queasy.char3, ";"),2)) / 100
.

FOR EACH ratecode WHERE ratecode.CODE = parent-code
    AND ratecode.startperiode LE from-date
    AND ratecode.endperiode   GE to-date NO-LOCK:
    CREATE child-ratecode.
    BUFFER-COPY ratecode EXCEPT CODE TO child-ratecode.
    ASSIGN
        found-flag                  = YES
        child-ratecode.CODE         = child-code
        child-ratecode.startperiode = from-date
        child-ratecode.endperiode   = to-date
    .
    IF adjust-value NE 0 THEN
    DO:
      IF in-percent THEN 
      DO:    
        child-ratecode.zipreis = child-ratecode.zipreis * (1 + adjust-value * 0.01).
        IF round-betrag NE 0 AND child-ratecode.zipreis GE (round-betrag * 10) THEN
        DO:
            RUN round-it (child-ratecode.zipreis, OUTPUT rounded-rate).
            child-ratecode.zipreis = rounded-rate.
        END.
      END.
      ELSE child-ratecode.zipreis = child-ratecode.zipreis + adjust-value.
    END.
END.

FOR EACH child-ratecode:
    FOR EACH ratecode WHERE ratecode.marknr = child-ratecode.marknr 
      AND ratecode.code    = child-code 
      AND ratecode.argtnr  = child-ratecode.argtnr 
      AND ratecode.zikatnr = child-ratecode.zikatnr
      AND ratecode.erwachs = child-ratecode.erwachs
      AND ratecode.kind1   = child-ratecode.kind1 
      AND ratecode.kind2   = child-ratecode.kind2 
      AND ratecode.wday    = child-ratecode.wday
      AND NOT ratecode.endperiode LT child-ratecode.startperiode
      AND NOT ratecode.startperiode GT child-ratecode.endperiode: 
      IF ratecode.startperiode LT child-ratecode.startperiode THEN
        ratecode.endperiode = child-ratecode.startperiode - 1.
      ELSE IF (ratecode.startperiode GE child-ratecode.startperiode)
        AND (ratecode.endperiode LE child-ratecode.endperiode) THEN
        DELETE ratecode.
      ELSE IF (ratecode.startperiode GE child-ratecode.startperiode)
        AND (ratecode.endperiode GT child-ratecode.endperiode) THEN
        ratecode.startperiode = child-ratecode.endperiode + 1.
    END.
END.
RELEASE ratecode.

FOR EACH child-ratecode:
    CREATE rbuff.
    BUFFER-COPY child-ratecode TO rbuff.
END.

{round-it.i }


