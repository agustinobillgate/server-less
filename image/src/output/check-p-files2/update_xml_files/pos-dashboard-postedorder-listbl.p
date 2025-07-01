

DEFINE TEMP-TABLE order-list
    FIELD table-nr   AS INTEGER  
    FIELD pax        AS INTEGER FORMAT ">>>"  
    FIELD order-nr   AS INTEGER
    FIELD guest-name AS CHAR FORMAT "x(40)"
    FIELD room-no    AS CHAR FORMAT "x(8)"
    FIELD order-date AS CHAR 
    FIELD posted     AS LOGICAL
    FIELD guest-nr   AS INT
    FIELD resnr      AS INT
    FIELD reslinnr   AS INT
    FIELD sessionprm AS CHAR
    FIELD billrecid  AS INT
    .
                                
DEFINE TEMP-TABLE order-item    
    FIELD nr        AS INTEGER FORMAT ">>>" LABEL "No"
    FIELD table-nr  AS INTEGER  
    FIELD order-nr  AS INTEGER  
    FIELD bezeich   AS CHARACTER FORMAT "x(35)"
    FIELD qty       AS INTEGER FORMAT ">>>" 
    FIELD sp-req    AS CHARACTER FORMAT "x(40)"
    FIELD confirm   AS LOGICAL
    FIELD remarks   AS CHAR FORMAT "x(20)" LABEL "Remarks"
    FIELD order-date AS CHAR 
    FIELD art-nr AS INT
    FIELD posted AS LOGICAL
    .
                                         
DEFINE INPUT PARAMETER dept AS INT.        
DEFINE OUTPUT PARAMETER TABLE FOR order-list.
DEFINE OUTPUT PARAMETER TABLE FOR order-item.

DEFINE BUFFER b-queasy FOR queasy.
DEFINE BUFFER qbill-line FOR queasy.

DEFINE VARIABLE mess-str AS CHAR.
DEFINE VARIABLE i-str AS INT.
DEFINE VARIABLE mess-token AS CHAR.
DEFINE VARIABLE mess-keyword AS CHAR.
DEFINE VARIABLE mess-value AS CHAR.

DEFINE VARIABLE pax           AS INT.
DEFINE VARIABLE orderdatetime AS CHAR.
DEFINE VARIABLE gname         AS CHAR.
DEFINE VARIABLE room          AS CHAR.
DEFINE VARIABLE gastnr        AS INT.
DEFINE VARIABLE resnr         AS INT.
DEFINE VARIABLE reslinnr      AS INT.
DEFINE VARIABLE billnumber    AS INT.
DEFINE VARIABLE doit          AS LOGICAL INIT NO.
DEFINE VARIABLE posted-flag   AS LOGICAL INIT NO.

/* FDL Change to Find First Do While
FOR EACH queasy WHERE queasy.KEY EQ 225 
    AND queasy.number1 EQ dept 
    AND queasy.char1 EQ "orderbill" 
    AND queasy.logi1 EQ YES NO-LOCK:
*/
FIND FIRST queasy WHERE queasy.KEY EQ 225 
    AND queasy.number1 EQ dept 
    AND queasy.logi1 EQ YES
    AND queasy.char1 EQ "orderbill"
    AND queasy.logi3 EQ YES NO-LOCK NO-ERROR.
DO WHILE AVAILABLE queasy:

    mess-str = queasy.char2.
    DO i-str = 1 TO NUM-ENTRIES(mess-str, "|"):
        mess-token = ENTRY(i-str,mess-str,"|").
        mess-keyword = ENTRY(1,mess-token,"=").
        mess-value = ENTRY(2,mess-token,"=").
        IF mess-keyword EQ "RN" THEN room = mess-value.
        ELSE IF mess-keyword EQ "PX" THEN pax = INT(mess-value).
        ELSE IF mess-keyword EQ "NM" THEN gname = mess-value.
        ELSE IF mess-keyword EQ "DT" THEN orderdatetime = mess-value.
        ELSE IF mess-keyword EQ "GN" THEN gastnr = INT(mess-value).
        ELSE IF mess-keyword EQ "RS" THEN resnr = INT(mess-value).
        ELSE IF mess-keyword EQ "RL" THEN reslinnr = INT(mess-value).
        ELSE IF mess-keyword EQ "BL" THEN billnumber = INT(mess-value).
    END.

    IF billnumber NE 0 OR queasy.betriebsnr NE 0 THEN
    DO:
        FIND FIRST h-bill WHERE h-bill.rechnr EQ billnumber AND h-bill.departement EQ dept NO-LOCK NO-ERROR.
        IF NOT AVAILABLE h-bill THEN
            FIND FIRST h-bill WHERE RECID(h-bill) EQ queasy.betriebsnr NO-LOCK NO-ERROR.

        IF AVAILABLE h-bill AND h-bill.flag EQ 0 THEN
        DO:
            /*IF h-bill.departement EQ 1 AND h-bill.flag EQ 0 THEN doit = yes.
            IF h-bill.departement NE 1 THEN doit = yes.*/

            doit = yes.
            IF doit THEN
            DO:
                CREATE order-list.
                ASSIGN
                    order-list.table-nr   = queasy.number2
                    order-list.pax        = pax
                    order-list.order-nr   = queasy.number3
                    order-list.guest-name = gname
                    order-list.room-no    = room
                    order-list.order-date = orderdatetime
                    order-list.guest-nr   = gastnr
                    order-list.resnr      = resnr
                    order-list.reslinnr   = reslinnr
                    order-list.sessionprm = queasy.char3
                    order-list.posted     = queasy.logi3
                    order-list.billrecid  = queasy.betriebsnr
                    .
            END.
            doit = NO.
        END.
    END.
    ELSE
    DO:
        CREATE order-list.
        ASSIGN
            order-list.table-nr   = queasy.number2
            order-list.pax        = pax
            order-list.order-nr   = queasy.number3
            order-list.guest-name = gname
            order-list.room-no    = room
            order-list.order-date = orderdatetime
            order-list.guest-nr   = gastnr
            order-list.resnr      = resnr
            order-list.reslinnr   = reslinnr
            order-list.sessionprm = queasy.char3
            order-list.posted     = queasy.logi3
            order-list.billrecid  = queasy.betriebsnr
            .
    END.

    FOR EACH qbill-line WHERE qbill-line.KEY EQ 225
        AND qbill-line.char1 EQ "orderbill-line"
        AND qbill-line.number2 EQ queasy.number2
        AND qbill-line.number1 EQ queasy.number3
        AND ENTRY(4,qbill-line.char2,"|") EQ queasy.char3
        AND ENTRY(3,qbill-line.char2,"|") EQ orderdatetime
        AND INT(ENTRY(1,qbill-line.char2,"|")) EQ dept NO-LOCK:

        mess-str = qbill-line.char3.
        CREATE order-item.
        ASSIGN order-item.table-nr   = queasy.number2
               order-item.order-nr   = queasy.number3
               order-item.bezeich    = ENTRY(3,mess-str,"|")
               order-item.qty        = INT(ENTRY(4,mess-str,"|"))
               order-item.sp-req     = ENTRY(6,mess-str,"|")
               order-item.confirm    = qbill-line.logi2
               order-item.remarks    = ""
               order-item.order-date = ENTRY(3,qbill-line.char2,"|")
               order-item.nr         = qbill-line.number3
               order-item.art-nr     = INT(ENTRY(2,mess-str,"|"))
               order-item.posted     = qbill-line.logi3
            .
    END.

    FIND FIRST qbill-line WHERE qbill-line.KEY EQ 225
        AND qbill-line.char1 EQ "orderbill-line"
        AND qbill-line.number2 EQ queasy.number2
        AND qbill-line.number1 EQ queasy.number3
        AND INT(ENTRY(1,qbill-line.char2,"|")) EQ dept
        AND ENTRY(3,qbill-line.char2,"|") EQ orderdatetime
        AND ENTRY(4,qbill-line.char2,"|") EQ queasy.char3
        AND qbill-line.logi2 NO-LOCK NO-ERROR.
    IF AVAILABLE qbill-line THEN
    DO:
        FIND FIRST b-queasy WHERE b-queasy.KEY EQ 225
            AND b-queasy.number1 EQ dept
            AND b-queasy.char1 EQ "orderbill"
            AND b-queasy.betriebsnr EQ queasy.betriebsnr
            AND b-queasy.number3 EQ queasy.number3
            AND b-queasy.number2 EQ queasy.number2
            AND b-queasy.char3 EQ queasy.char3 EXCLUSIVE-LOCK NO-ERROR.
        IF AVAILABLE b-queasy THEN
        DO:
            b-queasy.logi3 = YES.
            order-list.posted = YES.
            FIND CURRENT b-queasy NO-LOCK.
            RELEASE b-queasy.
        END.
    END.
    room = "".
    pax = 0.
    gname = "".
    orderdatetime = "".
    gastnr = 0.
    resnr = 0.
    reslinnr = 0.
    billnumber = 0.

    FIND NEXT queasy WHERE queasy.KEY EQ 225 
        AND queasy.number1 EQ dept 
        AND queasy.logi1 EQ YES
        AND queasy.char1 EQ "orderbill"
        AND queasy.logi3 EQ YES NO-LOCK NO-ERROR.
END.

/* FDL Comment
FIND FIRST order-list NO-LOCK NO-ERROR.
IF AVAILABLE order-list THEN
DO:
    /* Move Above
    FOR EACH order-list NO-LOCK BY order-list.order-nr:
        FOR EACH queasy WHERE queasy.KEY EQ 225 
            AND queasy.char1 EQ "orderbill-line"
            AND queasy.number2 EQ order-list.table-nr
            AND queasy.number1 EQ order-list.order-nr 
            AND ENTRY(3,queasy.char2,"|") EQ order-list.order-date NO-LOCK:

            mess-str = queasy.char3.
            CREATE order-item.
            ASSIGN order-item.table-nr   = order-list.table-nr   
                   order-item.order-nr   = order-list.order-nr 
                   order-item.bezeich    = ENTRY(3,mess-str,"|")
                   order-item.qty        = INT(ENTRY(4,mess-str,"|"))
                   order-item.sp-req     = ENTRY(6,mess-str,"|")
                   order-item.confirm    = queasy.logi2
                   order-item.remarks    = ""
                   order-item.order-date = ENTRY(3,queasy.char2,"|")
                   order-item.nr         = queasy.number3
                   order-item.art-nr     = INT(ENTRY(2,mess-str,"|"))
                   order-item.posted     = queasy.logi3
                .
        END.
    END.
    

    FOR EACH order-list BY order-list.order-nr:
        FIND FIRST queasy WHERE queasy.KEY EQ 225 
            AND queasy.char1 EQ "orderbill-line"
            AND queasy.number2 EQ order-list.table-nr
            AND queasy.number1 EQ order-list.order-nr 
            AND ENTRY(3,queasy.char2,"|") EQ order-list.order-date
            AND queasy.logi2 NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            FIND FIRST b-queasy WHERE KEY EQ 225 
                AND b-queasy.number1 EQ dept 
                AND b-queasy.char1 EQ "orderbill"
                AND b-queasy.betriebsnr EQ order-list.billrecid
                AND b-queasy.number3 EQ order-list.order-nr
                AND b-queasy.number2 EQ order-list.table-nr
                AND b-queasy.char3 EQ order-list.sessionprm EXCLUSIVE-LOCK NO-ERROR.
            IF AVAILABLE b-queasy THEN
            DO:
                b-queasy.logi3 = YES.
                order-list.posted = YES.
                FIND CURRENT b-queasy NO-LOCK.
                RELEASE b-queasy.
            END.
        END.
    END.
    */
    /*
    /*FD May 17, 2022 => Delete Order-List When Order Item All Cancel*/
    FOR EACH order-list WHERE order-list.posted EQ YES BY order-list.order-nr:
        FOR EACH order-item WHERE order-item.table-nr EQ order-list.table-nr
            AND order-item.order-nr EQ order-list.order-nr
            AND order-item.order-date EQ order-list.order-date 
            AND order-item.confirm EQ YES 
            AND order-item.posted EQ YES NO-LOCK:
            
            posted-flag = YES.
            LEAVE.
        END.

        IF NOT posted-flag THEN
        DO:
            DELETE order-list.            
        END.
        posted-flag = NO. /*Return Flag*/
    END.
    */
END.
*/

DEFINE BUFFER orderhdr FOR order-list.
FOR EACH orderhdr WHERE orderhdr.billrecid NE 0:
    FIND FIRST order-list WHERE order-list.sessionprm EQ orderhdr.sessionprm AND order-list.billrecid EQ 0 NO-ERROR.
    IF AVAILABLE order-list THEN order-list.billrecid = orderhdr.billrecid.
END.
