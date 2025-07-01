
DEFINE TEMP-TABLE t-quote 
    FIELD artnr         LIKE l-quote.artnr          FORMAT "9999999"
    FIELD lief-nr       LIKE l-quote.lief-nr        FORMAT ">,>>>,>>9"
    FIELD supName       AS CHAR                     FORMAT "x(20)"
    FIELD artName       LIKE l-artikel.bezeich      FORMAT "x(20)"
    FIELD devUnit       LIKE l-artikel.traubensort  FORMAT "x(8)"
    FIELD content       LIKE l-artikel.lief-einheit FORMAT ">>9.99"
    FIELD unitprice     LIKE l-quote.unitprice      FORMAT ">>>,>>>,>>9.99"
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

DEFINE INPUT PARAMETER user-init AS CHAR.
DEFINE INPUT PARAMETER TABLE FOR t-quote.

DEFINE VARIABLE local-curr AS CHAR.


FIND FIRST htparam WHERE htparam.paramnr = 152 NO-LOCK. 
FIND FIRST waehrung WHERE waehrung.wabkurz = htparam.fchar NO-LOCK NO-ERROR.
IF AVAILABLE waehrung THEN ASSIGN local-curr = waehrung.wabkurz.

FOR EACH t-quote NO-LOCK.
  FIND FIRST l-quote WHERE l-quote.artnr = t-quote.artnr
      AND l-quote.lief-nr = t-quote.lief-nr
      AND l-quote.from-date = t-quote.from-date
      AND l-quote.to-date = t-quote.to-date NO-LOCK NO-ERROR.
  IF NOT AVAILABLE l-quote THEN
  DO:
    CREATE l-quote.
    BUFFER-COPY t-quote TO l-quote.
    ASSIGN 
        l-quote.createID          = user-init
        l-quote.createDate        = DATE(MONTH(TODAY), DAY(TODAY), YEAR(TODAY))
        l-quote.createTime        = TIME
        l-quote.reserve-char[1]   = local-curr
        l-quote.reserve-deci[1]   = t-quote.minqty
        l-quote.reserve-deci[2]   = t-quote.disc
        l-quote.reserve-logic[1]  = NOT t-quote.avl
        l-quote.reserve-int[1]    = t-quote.delivDay
        l-quote.reserve-int[5]    = 1.
        .
  END.
END.


