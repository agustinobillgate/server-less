DEFINE TEMP-TABLE attchment 
    FIELD nr        AS INTEGER  FORMAT ">>>"   COLUMN-LABEL "No"
    FIELD att-file  AS CHAR     COLUMN-LABEL "Attachment File"
    FIELD bezeich   AS CHAR     COLUMN-LABEL "Description".

DEFINE TEMP-TABLE stock
    FIELD nr          AS INTEGER  FORMAT ">>9"         COLUMN-LABEL "No"
    FIELD stock-nr    AS INTEGER  FORMAT ">>>>>>>"     COLUMN-LABEL "ArticleNo"
    FIELD stock-nm    AS CHAR     FORMAT "x(30)"       COLUMN-LABEL "Article Name"
    /*FIELD stock-qty   AS INTEGER  FORMAT ">>>"         COLUMN-LABEL "Qty"*/
    FIELD stock-qty   AS DECIMAL  FORMAT ">>>9.99"          COLUMN-LABEL "Qty"
    FIELD stock-price AS INTEGER  FORMAT "->>,>>9.999" COLUMN-LABEL "Price"
    FIELD stock-total AS INTEGER  FORMAT ">>,>>>,>>9.999" COLUMN-LABEL "Total"  .

DEFINE TEMP-TABLE history
    FIELD nr        AS INTEGER  FORMAT ">>9"        COLUMN-LABEL "No"
    FIELD fdate     AS DATE     FORMAT "99/99/99"   COLUMN-LABEL "From Date"
    FIELD stime     AS CHAR     FORMAT "x(8)"   COLUMN-LABEL "Time"
    FIELD usrID     AS CHAR     FORMAT "x(2)"       COLUMN-LABEL "ID"
    FIELD username  AS CHAR     FORMAT "x(24)"      COLUMN-LABEL "Person In Charge".

DEF INPUT PARAMETER reqNo AS INT.
DEF OUTPUT PARAMETER TABLE FOR history.
DEF OUTPUT PARAMETER TABLE FOR stock.
DEF OUTPUT PARAMETER TABLE FOR attchment.

DEF BUFFER qbuff FOR eg-queasy.
DEF BUFFER usr   FOR eg-staff.
DEFINE VARIABLE att-ctr     AS INTEGER  INITIAL 0.

FOR EACH history:
    DELETE history.
END.

FOR EACH qbuff WHERE qbuff.KEY = 3 AND qbuff.reqnr = reqNo AND qbuff.usr-nr NE 0 
    USE-INDEX keyreq_ix NO-LOCK:

    FIND FIRST usr WHERE usr.nr = qbuff.usr-nr /*USE-INDEX nr_ix */
        NO-LOCK NO-ERROR.
    IF AVAILABLE usr THEN
    DO:
        CREATE history.
        ASSIGN
            history.nr = qbuff.hist-nr
            history.fdate = qbuff.hist-fdate
            history.stime = STRING(qbuff.hist-time, "HH:MM:SS")
            history.usrid    = string(usr.nr)
            history.username = usr.NAME.
    END.
    ELSE
    DO:
        CREATE history.
        ASSIGN
            history.nr = qbuff.hist-nr
            history.fdate = qbuff.hist-fdate
            history.stime = STRING(qbuff.hist-time, "HH:MM:SS")
            history.usrid    = string(qbuff.usr-nr)
            history.username = "PIC not found".
    END.
END.

RUN create-stock.
RUN create-attchment.


PROCEDURE create-stock:
    DEF VAR counter  AS INTEGER INITIAL 0.
    DEF BUFFER qbuff FOR eg-queasy.

    FOR EACH stock:
        DELETE stock.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 1 AND qbuff.reqnr = reqNo 
        USE-INDEX keyreq_ix NO-LOCK:
        counter = counter + 1.
        CREATE stock.
        ASSIGN
            stock.nr          = counter
            stock.stock-nr    = qbuff.stock-nr 
            /*stock.stock-qty   = qbuff.stock-qty*/
            stock.stock-qty   = qbuff.deci1
            stock.stock-price = qbuff.price
            /*stock.stock-total = qbuff.stock-qty * qbuff.price*/
            stock.stock-total = qbuff.deci1 * qbuff.price.

        FIND FIRST l-artikel WHERE l-artikel.artnr = stock.stock-nr 
            USE-INDEX artnr_ix NO-LOCK NO-ERROR.
        IF AVAILABLE l-artikel THEN
            stock.stock-nm = l-artikel.bezeich.
        ELSE stock.stock-nm = "Unknown".
    END.
END.

PROCEDURE create-attchment:
    DEF BUFFER qbuff FOR eg-queasy.

    FOR EACH attchment :
        DELETE attchment.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 2 AND qbuff.reqnr = reqno 
        USE-INDEX keyreq_ix NO-LOCK:
        att-ctr = att-ctr + 1.
        CREATE attchment.
        ASSIGN
            attchment.nr        = att-ctr
            attchment.att-file  = qbuff.ATTACHMENT
            attchment.bezeich   = qbuff.att-desc.
    END.

END.

