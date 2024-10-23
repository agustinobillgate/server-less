DEFINE TEMP-TABLE order-list   
    FIELD outlet-no    AS INTEGER FORMAT ">>>>" 
    FIELD order-id     AS INTEGER FORMAT ">>>>>>"
    FIELD guest-name   AS CHAR FORMAT "x(25)"
    FIELD guest-email  AS CHAR FORMAT "x(25)"
    FIELD guest-phone  AS CHAR FORMAT "x(25)"
    FIELD bill-number  AS CHAR FORMAT "x(26)"
    FIELD order-date   AS CHAR FORMAT "x(21)"
    FIELD order-type   AS CHAR FORMAT "x(13)"
    FIELD status-order AS CHAR FORMAT "x(15)"
    FIELD posted       AS LOGICAL
    FIELD billrecid    AS INT
    FIELD table-no     AS CHAR
    FIELD vhp-bill     AS INT
    FIELD courier-mtd  AS CHAR
    FIELD payment      AS CHAR
    FIELD payment-amt  AS DECIMAL
    FIELD payment-art  AS INT
    .                              

DEFINE TEMP-TABLE order-detail  
    FIELD nr          AS INTEGER FORMAT ">>>" LABEL "No"
    FIELD outlet-no   AS INTEGER FORMAT ">>>>" 
    FIELD order-id    AS INTEGER FORMAT ">>>>>>" 
    FIELD bezeich     AS CHARACTER FORMAT "x(50)"
    FIELD qty         AS INTEGER FORMAT ">>>" 
    FIELD sp-req      AS CHARACTER FORMAT "x(27)"
    FIELD confirm     AS LOGICAL LABEL "Confirm"
    FIELD remarks     AS CHAR FORMAT "x(20)" LABEL "Remarks"
    FIELD order-date  AS CHAR FORMAT "x(20)"
    FIELD art-nr      AS INT
    FIELD posted      AS LOGICAL LABEL "Posted"
    FIELD table-no    AS CHAR
    FIELD payment     AS CHAR
    FIELD payment-amt AS DECIMAL
    FIELD payment-art AS INT
    .

DEFINE INPUT PARAMETER deptno AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR order-list.
DEFINE OUTPUT PARAMETER TABLE FOR order-detail.

DEFINE VARIABLE tableno AS INT.


FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ deptno
    AND queasy.number2 EQ 5 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN tableno = INT(queasy.char2).

FIND FIRST queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ deptno
    AND queasy.number2 EQ 4 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN deptno = INT(queasy.char2).

DEFINE BUFFER orderhdr  FOR queasy.
DEFINE BUFFER orderline FOR queasy.

DEFINE VARIABLE nr AS INT.

FOR EACH orderhdr WHERE orderhdr.KEY EQ 271 
    AND orderhdr.betriebsnr EQ 1 
    AND orderhdr.number1 EQ deptno NO-LOCK:

    CREATE order-list.
    ASSIGN 
        order-list.outlet-no    = orderhdr.number1
        order-list.order-id     = orderhdr.number2 
        order-list.guest-name   = CAPS(ENTRY(3, orderhdr.char2, "|"))
        order-list.guest-email  = CAPS(ENTRY(5, orderhdr.char2, "|"))
        order-list.guest-phone  = CAPS(ENTRY(6, orderhdr.char2, "|"))
        order-list.bill-number  = ENTRY(4, orderhdr.char2, "|")
        order-list.order-date   = ENTRY(1, orderhdr.char2, "|")
        order-list.order-type   = ENTRY(1, orderhdr.char1, "|")
        order-list.status-order = ENTRY(2, orderhdr.char1, "|")
        order-list.posted       = orderhdr.logi1
        order-list.table-no     = ENTRY(2, orderhdr.char2, "|")
        order-list.vhp-bill     = orderhdr.number3
        order-list.courier-mtd  = ENTRY(3, orderhdr.char1, "|").

    IF order-list.table-no EQ "null" THEN order-list.table-no = "".
    ELSE IF order-list.table-no MATCHES "*room*" THEN order-list.table-no = ENTRY(2,order-list.table-no," ").

    nr = 0.
    FOR EACH orderline WHERE orderline.KEY EQ 271 
        AND orderline.betriebsnr EQ 2 
        AND orderline.number2 EQ orderhdr.number2 NO-LOCK.
        nr = nr + 1.
        CREATE order-detail.
        ASSIGN 
            order-detail.nr         = nr
            order-detail.outlet-no  = deptno
            order-detail.order-id   = orderline.number2
            order-detail.bezeich    = CAPS(ENTRY(2, orderline.char1, "|"))
            order-detail.qty        = INT(ENTRY(1, orderline.char1, "|"))
            order-detail.sp-req     = CAPS(ENTRY(2, orderline.char2, "|"))
            order-detail.remarks    = ENTRY(3, orderline.char2, "|")
            order-detail.order-date = ENTRY(1, orderline.char2, "|")
            order-detail.art-nr     = orderline.number1
            order-detail.posted     = orderline.logi1
            order-detail.payment    = CAPS(ENTRY(3, orderline.char1, "|"))
            order-detail.payment-amt = DECIMAL(ENTRY(4, orderline.char1, "|"))
            order-detail.payment-art = INT(ENTRY(5, orderline.char1, "|"))
            .

        IF order-detail.sp-req EQ "null" THEN order-detail.sp-req = "".
    END.
END.

FOR EACH order-list:
    IF order-list.status-order EQ "EXPIRED" THEN DELETE order-list.
    ELSE IF order-list.status-order EQ "HAVE_ISSUE" THEN DELETE order-list.
    ELSE
    DO:
        FIND FIRST order-detail WHERE order-detail.order-id EQ order-list.order-id NO-LOCK NO-ERROR.
        IF AVAILABLE order-detail THEN
        DO:
            order-list.payment     = order-detail.payment.    
            order-list.payment-amt = order-detail.payment-amt.
            order-list.payment-art = order-detail.payment-art.
        END.
    END.
END.
