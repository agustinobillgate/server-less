DEF TEMP-TABLE t-gl-acct LIKE gl-acct.
DEF TEMP-TABLE t-gl-accthis LIKE gl-accthis.

DEF TEMP-TABLE hotel-list
    FIELD selectFlag     AS LOGICAL INIT NO
    FIELD htl-code       AS CHAR
    FIELD i-hotel        AS INTEGER
    FIELD c-hotel        AS CHAR FORMAT "x(24)"
    FIELD i-brand        AS INTEGER
    FIELD i-country      AS INTEGER
    FIELD i-region       AS INTEGER
    FIELD i-area         AS INTEGER
    FIELD i-city         AS INTEGER
    FIELD dispFlag       AS LOGICAL INIT YES
    FIELD c-users        AS CHAR
.

DEF INPUT PARAMETER htl-code      AS CHAR    NO-UNDO.
DEF INPUT PARAMETER close-month   AS DATE    NO-UNDO.
DEF INPUT PARAMETER close-year    AS DATE    NO-UNDO.
DEF INPUT PARAMETER TABLE         FOR t-gl-acct.
DEF INPUT PARAMETER TABLE         FOR t-gl-accthis.
DEF OUTPUT PARAMETER success-flag AS LOGICAL NO-UNDO INIT NO.

DEF VARIABLE curr-i  AS INTEGER NO-UNDO.
DEF VARIABLE curr-ct AS CHAR    NO-UNDO.
DEF VARIABLE ct      AS CHAR    NO-UNDO.
DEF VARIABLE c-code  AS CHAR    NO-UNDO.
DEF VARIABLE i-year  AS INTEGER NO-UNDO.

DEF BUFFER qbuff  FOR queasy.
DEF BUFFER gbuff  FOR gl-acctgrp.
DEF BUFFER ghbuff FOR gl-acctgrphis.


FIND FIRST queasy WHERE queasy.KEY = 185 AND queasy.char1 = htl-code NO-LOCK NO-ERROR.
IF NOT AVAILABLE queasy THEN RETURN.


success-flag = YES.

FIND FIRST htparam WHERE htparam.paramnr = 597 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    FIND CURRENT htparam EXCLUSIVE-LOCK.
    ASSIGN htparam.fdate = close-month.
    FIND CURRENT htparam NO-LOCK.
    RELEASE htparam.
END.

CREATE hotel-list.
ASSIGN
    hotel-list.i-hotel  = queasy.number1
    hotel-list.htl-code = queasy.char1 
    hotel-list.c-hotel  = queasy.char2
    ct                  = queasy.char3
.
DO curr-i = 1 TO NUM-ENTRIES(ct, ";"):
    curr-ct = ENTRY(curr-i, ct, ";").
    IF curr-ct NE "" THEN
    DO:
        IF SUBSTR(curr-ct, 1, 6) = "$brand" THEN
        DO:
            c-code = SUBSTR(curr-ct, 7).
            FIND FIRST qbuff WHERE qbuff.KEY = 180 
                AND qbuff.char1 = c-code NO-LOCK.
            ASSIGN hotel-list.i-brand = qbuff.number1.
        END.
        ELSE IF SUBSTR(curr-ct, 1, 3) = "$CN" THEN
        DO:
            c-code = SUBSTR(curr-ct, 4).
            FIND FIRST qbuff WHERE qbuff.KEY = 183 
                AND qbuff.char1 = c-code NO-LOCK.
            ASSIGN hotel-list.i-country = qbuff.number1.
        END.
        ELSE IF SUBSTR(curr-ct, 1, 3) = "$RG" THEN
        DO:
            c-code = SUBSTR(curr-ct, 4).
            FIND FIRST qbuff WHERE qbuff.KEY = 182 
                AND qbuff.char1 = c-code NO-LOCK.
            ASSIGN hotel-list.i-region = qbuff.number1.
        END.
        ELSE IF SUBSTR(curr-ct, 1, 5) = "$AREA" THEN
        DO:
            c-code = SUBSTR(curr-ct, 6).
            FIND FIRST qbuff WHERE qbuff.KEY = 184 
                AND qbuff.char1 = c-code NO-LOCK.
            ASSIGN hotel-list.i-area = qbuff.number1.
        END.
        ELSE IF SUBSTR(curr-ct, 1, 3) = "$CT" THEN
        DO:
           c-code = SUBSTR(curr-ct, 4).
           FIND FIRST qbuff WHERE qbuff.KEY = 181 
               AND qbuff.char1 = c-code NO-LOCK NO-ERROR.
           IF AVAILABLE qbuff THEN
               ASSIGN hotel-list.i-city = qbuff.number1.
        END.
        ELSE IF SUBSTR(curr-ct, 1, 5) = "$USER" THEN
        DO:
           ASSIGN hotel-list.c-users = SUBSTR(curr-ct, 6).
        END.
    END.
END.


FIND FIRST t-gl-acct NO-ERROR.
DO WHILE AVAILABLE t-gl-acct:
    FIND FIRST gl-acctgrp WHERE 
        gl-acctgrp.fibukonto = t-gl-acct.fibukonto AND
        gl-acctgrp.htlcode   = htl-code NO-LOCK NO-ERROR.
    DO TRANSACTION:
        IF NOT AVAILABLE gl-acctgrp THEN
        DO:
            CREATE gl-acctgrp.
            ASSIGN gl-acctgrp.htlcode = htl-code.
            FIND CURRENT gl-acctgrp NO-LOCK.
        END.
        FIND FIRST gbuff WHERE RECID(gbuff) = RECID(gl-acctgrp)
            EXCLUSIVE-LOCK.
        BUFFER-COPY t-gl-acct TO gbuff.
        ASSIGN
            gbuff.brand   = hotel-list.i-brand
            gbuff.country = hotel-list.i-country
            gbuff.region  = hotel-list.i-region
            gbuff.area    = hotel-list.i-area
            gbuff.city    = hotel-list.i-city
        .
        FIND CURRENT gbuff NO-LOCK.
        RELEASE gl-acctgrp.
        RELEASE gbuff.
    END.
    FIND NEXT t-gl-acct NO-ERROR.
END.

IF close-year NE ? THEN i-year = YEAR(close-year).

FIND FIRST t-gl-accthis NO-ERROR.
DO WHILE AVAILABLE t-gl-accthis:
    FIND FIRST gl-acctgrphis WHERE 
        gl-acctgrphis.fibukonto = t-gl-acct.fibukonto AND
        gl-acctgrphis.htlcode   = htl-code AND 
        gl-acctgrphis.YEAR      = i-year
        NO-LOCK NO-ERROR.
    DO TRANSACTION:
        IF NOT AVAILABLE gl-acctgrphis THEN
        DO:
            CREATE gl-acctgrphis.
            ASSIGN gl-acctgrphis.htlcode = htl-code.
            FIND CURRENT gl-acctgrphis NO-LOCK.
        END.
        FIND FIRST ghbuff WHERE 
            RECID(ghbuff) = RECID(gl-acctgrphis)EXCLUSIVE-LOCK.
        BUFFER-COPY t-gl-accthis TO ghbuff.
        ASSIGN
            ghbuff.brand   = hotel-list.i-brand
            ghbuff.country = hotel-list.i-country
            ghbuff.region  = hotel-list.i-region
            ghbuff.area    = hotel-list.i-area
            ghbuff.city    = hotel-list.i-city
        .
        FIND CURRENT ghbuff NO-LOCK.
        RELEASE gl-acctgrphis.
        RELEASE ghbuff.
    END.
    FIND NEXT t-gl-accthis NO-ERROR.
END.

FIND FIRST queasy WHERE queasy.KEY = 188 
    AND queasy.char1 = htl-code NO-LOCK NO-ERROR.
DO TRANSACTION:
    IF NOT AVAILABLE queasy THEN
    DO:
        CREATE queasy.
        ASSIGN
            queasy.KEY = 188
            queasy.char1 = htl-code
        .
        FIND CURRENT queasy NO-LOCK.
    END.
    FIND FIRST qbuff WHERE RECID(qbuff) = RECID(queasy)
        EXCLUSIVE-LOCK.
    ASSIGN qbuff.date1 = close-month.
    IF close-year NE ? THEN qbuff.date2 = close-year.
    FIND CURRENT qbuff NO-LOCK.
    RELEASE qbuff.
END.
