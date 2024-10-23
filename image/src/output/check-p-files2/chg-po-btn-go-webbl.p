DEFINE TEMP-TABLE s-order LIKE l-order
    FIELD rec-id        AS INT
    FIELD lief-einheit  AS DECIMAL FORMAT ">>>,>>9.999"
    FIELD addvat-no     AS INTEGER
    FIELD addvat-value  AS DECIMAL
    FIELD disc        AS DECIMAL FORMAT ">9.99"               
    FIELD disc2       AS DECIMAL FORMAT ">9.99"               
    FIELD vat         AS DECIMAL FORMAT ">9.99"               
    FIELD disc-val    AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   
    FIELD disc2-val   AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   
    FIELD vat-val     AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   
.

DEFINE TEMP-TABLE disc-list 
  FIELD l-recid     AS INTEGER 
  FIELD price0      AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Unit-Price" 
  FIELD brutto      AS DECIMAL FORMAT "->,>>>,>>>,>>9.999"  LABEL "Gross Amount" 
  FIELD disc        AS DECIMAL FORMAT ">9.99"               LABEL "Disc" 
  FIELD disc2       AS DECIMAL FORMAT ">9.99"               LABEL "Disc2" 
  FIELD vat         AS DECIMAL FORMAT ">9.99"               LABEL "VAT"
  FIELD disc-val    AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc Value" 
  FIELD disc2-val   AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "Disc2 Value"
  FIELD vat-val     AS DECIMAL FORMAT ">,>>>,>>>,>>9.999"   LABEL "VAT-Value". 

DEFINE TEMP-TABLE t-l-orderhdr LIKE l-orderhdr
    FIELD rec-id AS INT.

DEF INPUT PARAMETER TABLE FOR t-l-orderhdr.
DEF INPUT PARAMETER TABLE FOR s-order.
DEF INPUT PARAMETER TABLE FOR disc-list.
DEF INPUT PARAMETER lief-nr                 AS INT.
DEF INPUT PARAMETER pr                      AS CHAR.
DEF INPUT PARAMETER tp-bediener-username    AS CHAR.

/* SY 30/09/14 add global disc */
DEF VARIABLE remark     AS CHAR    NO-UNDO.
DEF VARIABLE globaldisc AS DECIMAL NO-UNDO INIT 0.
DEF VARIABLE logstring  AS CHAR    NO-UNDO.

FIND FIRST t-l-orderhdr.
FIND FIRST l-orderhdr WHERE RECID(l-orderhdr) = t-l-orderhdr.rec-id.

remark = ENTRY(1, t-l-orderhdr.lief-fax[3], CHR(2)).
IF NUM-ENTRIES(t-l-orderhdr.lief-fax[3], CHR(2)) GT 1 THEN
    ASSIGN globaldisc = DECIMAL(ENTRY(2,t-l-orderhdr.lief-fax[3],CHR(2))) / 100.

IF l-orderhdr.lief-nr NE t-l-orderhdr.lief-nr THEN
DO:
    logstring = "[CHG ORDERHDR]DOC NO: " + t-l-orderhdr.docu-nr + " Supplier Number Changed From: " + STRING(l-orderhdr.lief-nr) + " To: " + STRING(t-l-orderhdr.lief-nr).
    RUN create-log(logstring).
END.
IF l-orderhdr.lieferdatum NE t-l-orderhdr.lieferdatum THEN
DO:
    logstring = "[CHG ORDERHDR]DOC NO: " + t-l-orderhdr.docu-nr + " Delivery Date Changed From: " + STRING(l-orderhdr.lieferdatum) + " To: " + STRING(t-l-orderhdr.lieferdatum).
    RUN create-log(logstring).
END.
IF l-orderhdr.bestellart NE t-l-orderhdr.bestellart THEN
DO:
    logstring = "[CHG ORDERHDR]DOC NO: " + t-l-orderhdr.docu-nr + " Order Type Changed From: " + STRING(l-orderhdr.bestellart) + " To: " + STRING(t-l-orderhdr.bestellart).
    RUN create-log(logstring).
END.
IF l-orderhdr.angebot-lief[1] NE t-l-orderhdr.angebot-lief[1] THEN
DO:
    logstring = "[CHG ORDERHDR]DOC NO: " + t-l-orderhdr.docu-nr + " Department Changed From: " + STRING(l-orderhdr.angebot-lief[1]) + " To: " + STRING(t-l-orderhdr.angebot-lief[1]).
    RUN create-log(logstring).
END.
IF l-orderhdr.lief-fax[2] NE t-l-orderhdr.lief-fax[2] THEN
DO:
    logstring = "[CHG ORDERHDR]DOC NO: " + t-l-orderhdr.docu-nr + " Credit Term Changed From: " + STRING(l-orderhdr.lief-fax[2]) + " To: " + STRING(t-l-orderhdr.lief-fax[2]).
    RUN create-log(logstring).
END.
IF l-orderhdr.lief-fax[3] NE remark THEN
DO:
    logstring = "[CHG ORDERHDR]DOC NO: " + t-l-orderhdr.docu-nr + " Remarks Changed From: " + STRING(l-orderhdr.lief-fax[3]) + " To: " + STRING(remark).
    RUN create-log(logstring).
END.

FIND CURRENT l-orderhdr EXCLUSIVE-LOCK. 
ASSIGN 
    l-orderhdr.lief-nr          = t-l-orderhdr.lief-nr 
    l-orderhdr.lieferdatum      = t-l-orderhdr.lieferdatum 
    l-orderhdr.bestellart       = t-l-orderhdr.bestellart 
    l-orderhdr.angebot-lief[1]  = t-l-orderhdr.angebot-lief[1] 
    l-orderhdr.angebot-lief[2]  = t-l-orderhdr.angebot-lief[2] 
    l-orderhdr.lief-fax[2]      = t-l-orderhdr.lief-fax[2] 
    l-orderhdr.lief-fax[3]      = remark
    l-orderhdr.gedruckt         = t-l-orderhdr.gedruckt
. 
FIND CURRENT l-orderhdr NO-LOCK. 

/*====================*/
FIND FIRST l-order WHERE l-order.docu-nr = l-orderhdr.docu-nr AND l-order.pos = 0 EXCLUSIVE-LOCK. 
IF l-order.lief-nr NE lief-nr THEN
DO:
    logstring = "[CHG LORDER]DOC NO: " + t-l-orderhdr.docu-nr + " Supplier Number Changed From: " + STRING(l-order.lief-nr) + " To: " + STRING(lief-nr).
    RUN create-log(logstring).
END.
IF l-orderhdr.lief-fax[1] NE pr THEN
DO:
    logstring = "[CHG LORDER]DOC NO: " + t-l-orderhdr.docu-nr + " PR Number Changed From: " + STRING(l-orderhdr.lief-fax[1]) + " To: " + STRING(pr).
    RUN create-log(logstring).
END.
IF l-order.warenwert NE globaldisc THEN
DO:
    logstring = "[CHG LORDER]DOC NO: " + t-l-orderhdr.docu-nr + " GLobal Discount Changed From: " + STRING(l-order.warenwert) + " To: " + STRING(globaldisc).
    RUN create-log(logstring).
END.
ASSIGN 
    l-order.lief-nr     = lief-nr 
    l-order.lief-fax[1] = pr
    l-order.warenwert   = globaldisc
. 
FIND CURRENT l-order NO-LOCK. 
RELEASE l-order.


/*====================*/
FOR EACH s-order NO-LOCK: 
    FIND FIRST disc-list WHERE disc-list.l-recid = s-order.rec-id NO-LOCK. 
    FIND FIRST l-order WHERE RECID(l-order) = s-order.rec-id EXCLUSIVE-LOCK. 

    IF l-order.lief-nr NE lief-nr THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr + " Article No: " + STRING(s-order.artnr) 
            + " Supplier Number Changed From: " + STRING(l-order.lief-nr) + " To: " + STRING(lief-nr).
        RUN create-log(logstring).
    END.
    IF l-order.lief-fax[1] NE pr THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr + " Article No: " + STRING(s-order.artnr) 
            + " PR Number Changed From: " + STRING(l-order.lief-fax[1]) + " To: " + STRING(pr).
        RUN create-log(logstring).
    END.
    IF l-order.lief-fax[2] NE tp-bediener-username THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr + " Article No: " + STRING(s-order.artnr) 
            + " Username Changed From: " + STRING(l-order.lief-fax[2]) + " To: " + STRING(tp-bediener-username).
        RUN create-log(logstring).
    END.
    IF l-order.anzahl NE s-order.anzahl THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr + " Article No: " + STRING(s-order.artnr) 
            + " QTY Changed From: " + STRING(l-order.anzahl) + " To: " + STRING(s-order.anzahl).
        RUN create-log(logstring).
    END.
    IF l-order.einzelpreis NE s-order.einzelpreis THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr + " Article No: " + STRING(s-order.artnr) 
            + " Nett Price Changed From: " + STRING(l-order.einzelpreis) + " To: " + STRING(s-order.einzelpreis).
        RUN create-log(logstring).
    END.
    IF l-order.besteller NE s-order.besteller THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr + " Article No: " + STRING(s-order.artnr) 
            + " Remark Changed From: " + STRING(l-order.besteller) + " To: " + STRING(s-order.besteller).
        RUN create-log(logstring).
    END.
    IF l-order.quality NE s-order.quality THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr + " Article No: " + STRING(s-order.artnr) 
            + " Disc Changed From: " + STRING(l-order.quality) + " To: " + STRING(s-order.quality).
        RUN create-log(logstring).
    END.
    IF l-order.warenwert NE s-order.warenwert THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr + " Article No: " + STRING(s-order.artnr) 
            + " Net Amount Changed From: " + STRING(l-order.warenwert) + " To: " + STRING(s-order.warenwert).
        RUN create-log(logstring).
    END.
    IF l-order.stornogrund NE s-order.stornogrund THEN
    DO:
        logstring = "[CHG LORDER]DOC NO: " + l-order.docu-nr + " Article No: " + STRING(s-order.artnr) 
            + " AcctNo Changed From: " + STRING(l-order.stornogrund) + " To: " + STRING(s-order.stornogrund).
        RUN create-log(logstring).
    END.

    ASSIGN 
      l-order.lief-nr     = lief-nr 
      l-order.lieferdatum = today 
      l-order.lief-fax[1] = pr 
      l-order.lief-fax[2] = tp-bediener-username 
      l-order.anzahl      = s-order.anzahl 
      l-order.einzelpreis = s-order.einzelpreis 
      l-order.besteller   = s-order.besteller
      /*l-order.quality     = s-order.quality */
      l-order.warenwert   = s-order.warenwert 
      l-order.stornogrund = s-order.stornogrund. 

    l-order.quality = STRING(s-order.disc, "99.99 ") 
        + STRING(s-order.vat, "99.99") + STRING(s-order.disc2, " 99.99")
        + STRING(s-order.disc-val, " >,>>>,>>>,>>9.999") + STRING(s-order.disc2-val, " >,>>>,>>>,>>9.999")
        + STRING(s-order.vat-val, " >,>>>,>>>,>>9.999").


    FIND FIRST queasy WHERE queasy.KEY = 304 AND queasy.char1 = l-order.docu-nr
        AND queasy.number1 = l-order.artnr NO-LOCK NO-ERROR.
    IF AVAILABLE queasy  THEN DO:
        FIND CURRENT queasy EXCLUSIVE-LOCK.
        ASSIGN queasy.number2 = s-order.addvat-no
               queasy.deci1   = s-order.addvat-value.
        FIND CURRENT queasy NO-LOCK.
        RELEASE queasy.
    END.

    FIND CURRENT l-order NO-LOCK. 
    RELEASE l-order.
END.

PROCEDURE create-log:
    DEFINE INPUT PARAMETER aend-str AS CHAR.
    FIND FIRST bediener WHERE bediener.username = tp-bediener-username NO-LOCK.
    CREATE res-history.
    ASSIGN 
        res-history.nr        = bediener.nr
        res-history.datum     = TODAY
        res-history.zeit      = TIME
        res-history.action    = "Purchase Order"
        res-history.aenderung = aend-str
        .
    
    FIND CURRENT res-history NO-LOCK.
    RELEASE res-history.
END.

