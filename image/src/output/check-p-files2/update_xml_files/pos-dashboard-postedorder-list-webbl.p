DEFINE TEMP-TABLE input-list
    FIELD dept          AS INTEGER  
    FIELD search-type   AS INTEGER 
    FIELD table-nr      AS INTEGER  
    FIELD order-nr      AS INTEGER
    FIELD order-date    AS CHARACTER 
    FIELD sessionprm    AS CHARACTER
.

DEFINE TEMP-TABLE order-list
    FIELD table-nr      AS INTEGER  
    FIELD pax           AS INTEGER FORMAT ">>>"  
    FIELD order-nr      AS INTEGER
    FIELD guest-name    AS CHARACTER FORMAT "x(40)"
    FIELD room-no       AS CHARACTER FORMAT "x(8)"
    FIELD order-date    AS CHARACTER 
    FIELD posted        AS LOGICAL
    FIELD guest-nr      AS INTEGER
    FIELD resnr         AS INTEGER
    FIELD reslinnr      AS INTEGER
    FIELD sessionprm    AS CHARACTER
    FIELD billrecid     AS INTEGER
.
                                
DEFINE TEMP-TABLE order-item    
    FIELD nr            AS INTEGER FORMAT ">>>" LABEL "No"
    FIELD table-nr      AS INTEGER  
    FIELD order-nr      AS INTEGER  
    FIELD bezeich       AS CHARACTER FORMAT "x(35)"
    FIELD qty           AS INTEGER FORMAT ">>>" 
    FIELD sp-req        AS CHARACTER FORMAT "x(40)"
    FIELD confirm       AS LOGICAL
    FIELD remarks       AS CHARACTER FORMAT "x(20)" LABEL "Remarks"
    FIELD order-date    AS CHARACTER 
    FIELD art-nr        AS INTEGER
    FIELD posted        AS LOGICAL
.
                                           
DEFINE INPUT PARAMETER TABLE    FOR input-list.  
DEFINE OUTPUT PARAMETER TABLE   FOR order-list.
DEFINE OUTPUT PARAMETER TABLE   FOR order-item.

FIND FIRST input-list NO-LOCK NO-ERROR.
IF NOT AVAILABLE input-list THEN RETURN.

DEFINE BUFFER b-queasy      FOR queasy.
DEFINE BUFFER qbill-line    FOR queasy.
DEFINE BUFFER orderhdr      FOR order-list.

DEFINE VARIABLE mess-str AS CHARACTER.

/* FDL Change to Find First Do While
FOR EACH queasy WHERE queasy.KEY EQ 225 
    AND queasy.number1 EQ dept 
    AND queasy.char1 EQ "orderbill" 
    AND queasy.logi1 EQ YES NO-LOCK:
*/
IF input-list.search-type EQ 1 THEN RUN create-list.
ELSE IF input-list.search-type EQ 2 THEN RUN create-detail.

PROCEDURE create-list:
    DEFINE VARIABLE i-str AS INTEGER.
    DEFINE VARIABLE mess-token AS CHARACTER.
    DEFINE VARIABLE mess-keyword AS CHARACTER.
    DEFINE VARIABLE mess-value AS CHARACTER.
    
    DEFINE VARIABLE pax           AS INTEGER.
    DEFINE VARIABLE orderdatetime AS CHARACTER.
    DEFINE VARIABLE gname         AS CHARACTER.
    DEFINE VARIABLE room          AS CHARACTER.
    DEFINE VARIABLE gastnr        AS INTEGER.
    DEFINE VARIABLE resnr         AS INTEGER.
    DEFINE VARIABLE reslinnr      AS INTEGER.
    DEFINE VARIABLE billnumber    AS INTEGER.
    DEFINE VARIABLE doit          AS LOGICAL INIT NO.
    DEFINE VARIABLE posted-flag   AS LOGICAL INIT NO.
    
    FIND FIRST queasy WHERE queasy.KEY EQ 225 
        AND queasy.number1 EQ input-list.dept 
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
            FIND FIRST h-bill WHERE h-bill.rechnr EQ billnumber AND h-bill.departement EQ input-list.dept NO-LOCK NO-ERROR.
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

        FIND FIRST qbill-line WHERE qbill-line.KEY EQ 225
            AND qbill-line.char1 EQ "orderbill-line"
            AND qbill-line.number2 EQ queasy.number2
            AND qbill-line.number1 EQ queasy.number3
            AND INT(ENTRY(1,qbill-line.char2,"|")) EQ input-list.dept
            AND ENTRY(3,qbill-line.char2,"|") EQ orderdatetime
            AND ENTRY(4,qbill-line.char2,"|") EQ queasy.char3
            AND qbill-line.logi2 NO-LOCK NO-ERROR.
        IF AVAILABLE qbill-line THEN
        DO:
            FIND FIRST b-queasy WHERE b-queasy.KEY EQ 225
                AND b-queasy.number1 EQ input-list.dept
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
            AND queasy.number1 EQ input-list.dept 
            AND queasy.logi1 EQ YES
            AND queasy.char1 EQ "orderbill"
            AND queasy.logi3 EQ YES NO-LOCK NO-ERROR.
    END.


    FOR EACH orderhdr WHERE orderhdr.billrecid NE 0:
        FIND FIRST order-list WHERE order-list.sessionprm EQ orderhdr.sessionprm AND order-list.billrecid EQ 0 NO-ERROR.
        IF AVAILABLE order-list THEN order-list.billrecid = orderhdr.billrecid.
    END.
END PROCEDURE.

PROCEDURE create-detail:
    FOR EACH qbill-line WHERE qbill-line.KEY EQ 225
        AND qbill-line.char1 EQ "orderbill-line"
        AND qbill-line.number2 EQ input-list.table-nr
        AND qbill-line.number1 EQ input-list.order-nr
        AND ENTRY(4,qbill-line.char2,"|") EQ input-list.sessionprm
        AND ENTRY(3,qbill-line.char2,"|") EQ input-list.order-date
        AND INT(ENTRY(1,qbill-line.char2,"|")) EQ input-list.dept NO-LOCK:

        mess-str = qbill-line.char3.
        CREATE order-item.
        ASSIGN order-item.table-nr   = qbill-line.number2
               order-item.order-nr   = qbill-line.number1
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
END PROCEDURE.
