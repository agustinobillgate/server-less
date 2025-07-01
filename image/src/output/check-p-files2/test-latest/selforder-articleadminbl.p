DEFINE TEMP-TABLE t-article
    FIELD nr            AS INT
    FIELD artnr         AS INTEGER   FORMAT ">>>>>>>9" LABEL "ArtNo"
    FIELD dept          AS INTEGER   FORMAT ">>9"
    FIELD bezeich       AS CHARACTER FORMAT "x(30)"  LABEL "Article Name"
    FIELD img           AS CHARACTER FORMAT "x(50)"
    FIELD remark        AS CHARACTER FORMAT "x(78)" LABEL "Description"
    FIELD activ-art     AS LOGICAL
    FIELD sold-out      AS LOGICAL
    FIELD selected-art  AS LOGICAL INITIAL NO
    .

DEFINE INPUT PARAMETER case-type AS INT.
DEFINE INPUT PARAMETER art-dept  AS INT. 
DEFINE INPUT PARAMETER art-nr    AS INT. 
DEFINE INPUT PARAMETER art-name  AS CHAR.
DEFINE INPUT PARAMETER art-desc  AS CHAR.
DEFINE INPUT PARAMETER art-img   AS CHAR.
DEFINE INPUT PARAMETER art-flag  AS LOGICAL.
DEFINE INPUT PARAMETER soldout   AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR t-article.

DEF VAR nr AS INT.

IF art-name EQ ? THEN art-name = "".
IF art-desc EQ ? THEN art-desc = "".
IF art-img EQ ? THEN art-img = "".

IF case-type EQ 1 THEN /*add or modify*/
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 222 
         AND queasy.number1 EQ 2 
         AND queasy.number2 EQ art-nr
         AND queasy.number3 EQ art-dept EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN 
            queasy.char2 = art-img 
            queasy.char3 = art-desc
            queasy.logi1 = art-flag
            queasy.logi2 = soldout.
    END.
    ELSE
    DO:
        CREATE queasy.
        ASSIGN 
            queasy.KEY = 222
            queasy.number1 = 2
            queasy.number2 = art-nr
            queasy.number3 = art-dept
            queasy.char2 = art-img 
            queasy.char3 = art-desc
            queasy.logi1 = art-flag
            queasy.logi2 = soldout
            .
    END.
END.
ELSE IF case-type EQ 2 THEN /*delete*/
DO:
    FIND FIRST queasy WHERE queasy.KEY EQ 222 
         AND queasy.number1 EQ 2 
         AND queasy.number2 EQ art-nr
         AND queasy.number3 EQ art-dept EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN 
            queasy.char2 = "".
    END. 
END.

FOR EACH h-artikel WHERE h-artikel.departement EQ art-dept
    AND h-artikel.activeflag EQ YES 
    AND h-artikel.artart EQ 0 
    AND h-artikel.epreis1 NE 0 NO-LOCK:
    FIND FIRST queasy WHERE queasy.KEY EQ 222 
        AND queasy.number1 EQ 2 
        AND queasy.number2 EQ h-artikel.artnr 
        AND queasy.number3 EQ h-artikel.departement NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        CREATE t-article.
        ASSIGN
            t-article.artnr     = queasy.number2
            t-article.dept      = queasy.number3
            t-article.bezeich   = h-artikel.bezeich
            t-article.img       = queasy.char2
            t-article.remark    = queasy.char3
            t-article.activ-art = queasy.logi1 
            t-article.sold-out  = queasy.logi2 
            .
    END.
    ELSE
    DO:
        CREATE t-article.
        ASSIGN                   
            t-article.artnr     = h-artikel.artnr
            t-article.dept      = h-artikel.departement
            t-article.bezeich   = h-artikel.bezeich
            .
    END.
END.

nr = 0.
FOR EACH t-article BY t-article.activ-art DESC BY t-article.bezeich.
    nr = nr + 1.
    t-article.nr = nr.
END.
