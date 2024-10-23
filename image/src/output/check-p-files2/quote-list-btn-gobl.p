DEFINE TEMP-TABLE t-quote 
    FIELD artnr         LIKE l-quote.artnr          FORMAT "9999999"
    FIELD lief-nr       LIKE l-quote.lief-nr        FORMAT ">,>>>,>>9"
    FIELD supName       AS CHAR                     FORMAT "x(20)"
    FIELD artName       LIKE l-artikel.bezeich      FORMAT "x(20)"
    FIELD devUnit       LIKE l-artikel.traubensort  FORMAT "x(8)"
    FIELD content       LIKE l-artikel.lief-einheit FORMAT ">>9.99"
    FIELD unitprice     LIKE l-quote.unitprice      FORMAT ">>>,>>>,>>>,>>9.99" /*william 08EE84 add more >>>*/
    FIELD curr          LIKE l-quote.reserve-char[1]FORMAT "x(4)"     
    FIELD from-date     LIKE l-quote.from-date      FORMAT "99/99/99"     
    FIELD to-Date       LIKE l-quote.to-date        FORMAT "99/99/99"
    FIELD remark        LIKE l-quote.remark         FORMAT "x(20)"
    FIELD filname       LIKE l-quote.filname        FORMAT "x(20)"
    FIELD activeFlag    LIKE l-quote.activeflag     INIT YES
    FIELD docu-nr       LIKE l-quote.docu-nr        FORMAT "x(12)"
    FIELD minQty        AS DEC      INIT 0          FORMAT ">>9.99"
    FIELD delivDay      AS INT      INIT 0          FORMAT ">>9"
    FIELD disc          AS DEC      INIT 0          FORMAT ">>9.99"
    FIELD avl           AS LOGICAL  INIT YES
    .

DEFINE TEMP-TABLE t-quote1  LIKE t-quote.
DEFINE BUFFER b-lquote      FOR l-quote.

DEFINE INPUT PARAMETER PvILanguage      AS INT  NO-UNDO.
DEFINE INPUT PARAMETER curr-type        AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER user-init        AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER TABLE FOR t-quote.
DEFINE INPUT PARAMETER TABLE FOR t-quote1.
DEFINE OUTPUT PARAMETER msg-str          AS CHAR NO-UNDO INIT "".

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "quote-list". 

FIND FIRST t-quote NO-LOCK.
IF curr-type EQ "new" THEN
DO:
    FIND FIRST l-quote WHERE l-quote.artnr = t-quote.artnr
        AND l-quote.lief-nr = t-quote.lief-nr
        AND l-quote.docu-nr = t-quote.docu-nr
        AND l-quote.from-date = t-quote.from-date 
        AND l-quote.to-date = t-quote.to-date
        NO-LOCK NO-ERROR.
    IF AVAILABLE l-quote AND l-quote.reserve-int[5] LE 1 THEN
        msg-str = translateExtended ("Article already exist for the same Supplier, same DocuNo and same periode.",
                                     lvCAREA,""). 
                
    CREATE l-quote.
    BUFFER-COPY t-quote TO l-quote.
    ASSIGN l-quote.createID     = user-init
           l-quote.createDate   = DATE(MONTH(TODAY), DAY(TODAY), YEAR(TODAY))
           l-quote.createTime   = TIME
           l-quote.reserve-char[1] = t-quote.curr
           l-quote.reserve-deci[1]   = t-quote.minqty
           l-quote.reserve-deci[2]   = t-quote.disc
           l-quote.reserve-logic[1]  = NOT t-quote.avl
           l-quote.reserve-int[1]    = t-quote.delivDay
    .
    IF t-quote.activeFlag = YES THEN l-quote.reserve-int[5] = 1.
    ELSE l-quote.reserve-int[5] = 0.
    RELEASE l-quote.
END.
ELSE IF curr-type EQ "chg" THEN
DO:
    FIND FIRST t-quote1.
    FIND FIRST l-quote WHERE l-quote.artnr = t-quote1.artnr
        AND l-quote.lief-nr = t-quote1.lief-nr 
        AND l-quote.docu-nr = t-quote1.docu-nr
        AND l-quote.from-date = t-quote1.from-date
        AND l-quote.to-date = t-quote1.to-date
        AND l-quote.unitprice = t-quote1.unitprice
        AND l-quote.reserve-char[1] = t-quote1.curr
        AND l-quote.remark = t-quote1.remark
        AND l-quote.filname = t-quote1.filname
        AND l-quote.activeflag = t-quote1.activeflag NO-LOCK NO-ERROR.
    IF AVAILABLE l-quote THEN
    DO:
        IF (l-quote.from-date NE t-quote.from-date 
            AND l-quote.to-date NE t-quote.to-date) 
            OR l-quote.docu-nr NE t-quote.docu-nr THEN
        DO:
            FIND FIRST b-lquote WHERE b-lquote.artnr = t-quote.artnr
                AND b-lquote.lief-nr = t-quote.lief-nr
                AND b-lquote.docu-nr = t-quote.docu-nr
                AND b-lquote.from-date = t-quote.from-date 
                AND b-lquote.to-date = t-quote.to-date 
                AND b-lquote.activeflag NO-LOCK NO-ERROR.
            IF AVAILABLE b-lquote AND b-lquote.reserve-int[5] LE 1 THEN
                msg-str = translateExtended 
                        ("Article already exist for the same Supplier, same DocuNo and same periode.",
                         lvCAREA,""). 
        END.
        FIND CURRENT l-quote EXCLUSIVE-LOCK.
        BUFFER-COPY t-quote TO l-quote.
        ASSIGN 
            l-quote.chgID             = user-init
            l-quote.chgDate           = DATE(MONTH(TODAY), DAY(TODAY), YEAR(TODAY))
            l-quote.chgTime           = TIME
            l-quote.reserve-char[1]   = t-quote.curr
            l-quote.reserve-deci[1]   = t-quote.minqty
            l-quote.reserve-deci[2]   = t-quote.disc
            l-quote.reserve-logic[1]  = NOT t-quote.avl
            l-quote.reserve-int[1]    = t-quote.delivDay
        .
        IF t-quote.activeFlag = YES THEN l-quote.reserve-int[5] = 1.
        ELSE l-quote.reserve-int[5] = 0.
        FIND CURRENT l-quote NO-LOCK.
    END.
END.
ELSE IF curr-type EQ "del" THEN
DO:
    FIND FIRST l-quote WHERE l-quote.artnr = t-quote.artnr
        AND l-quote.lief-nr = t-quote.lief-nr
        AND l-quote.from-date = t-quote.from-date 
        AND l-quote.to-date = t-quote.to-date NO-LOCK NO-ERROR. 
    IF AVAILABLE l-quote THEN
    DO:
        FIND CURRENT l-quote EXCLUSIVE-LOCK.
        /*
        ASSIGN l-quote.chgID     = user-init
               l-quote.chgDate   = DATE(MONTH(TODAY), DAY(TODAY), YEAR(TODAY))
               l-quote.chgTime   = TIME
               l-quote.reserve-int[5] = 2.
        FIND CURRENT l-quote NO-LOCK.
        */
        DELETE l-quote. /* Frans: #C59B5E */
        RELEASE l-quote.
    END.
END.

