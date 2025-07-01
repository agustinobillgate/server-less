DEFINE TEMP-TABLE output-list
    FIELD timestamp     AS CHAR
    FIELD billnumber    AS INT
    FIELD amount        AS DECIMAL FORMAT "->>>>>>>>9"
    FIELD terminalid    AS CHAR
    FIELD phone         AS CHAR
    FIELD programid     AS CHAR
    FIELD walletid      AS CHAR
    FIELD sku           AS CHAR FORMAT "x(10)"
    FIELD itemname      AS CHAR FORMAT "x(40)"
    FIELD qty           AS CHAR FORMAT "x(10)"
    FIELD price         AS DECIMAL FORMAT "->>>>>>>>9"
    FIELD price-str     AS CHAR FORMAT "x(30)"
    FIELD paymentmethod AS CHAR FORMAT "x(40)"
    FIELD zinr          AS CHAR
    FIELD resnr         AS INT
    FIELD reslinnr      AS INT
    FIELD gastnrmember  AS INT
    FIELD segment       AS CHAR FORMAT "x(30)" 
    FIELD sob           AS CHAR FORMAT "x(30)"
    FIELD send-date     AS DATE
    FIELD data-date     AS DATE
    .
/*  
/*===================================================*/
/*UBAH VALUE FROM DATE DAN TO DATE*/
DEFINE VARIABLE from-date AS DATE INIT 07/31/24.
DEFINE VARIABLE to-date   AS DATE INIT 07/31/24. 
/*===================================================*/
*/
DEFINE INPUT PARAMETER from-date AS DATE.
DEFINE INPUT PARAMETER to-date AS DATE.
DEFINE OUTPUT PARAMETER sftp-localpath AS CHAR.
DEFINE OUTPUT PARAMETER filetimestamp AS CHAR.
DEFINE OUTPUT PARAMETER terminalid AS CHAR.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE deptnr     AS INT.
DEFINE VARIABLE programid  AS CHAR.
DEFINE VARIABLE walletid   AS CHAR.
DEFINE VARIABLE tada-sku   AS CHAR.
DEFINE VARIABLE tada-item  AS CHAR.
DEFINE VARIABLE segment-list  AS CHAR.

DEFINE BUFFER bline FOR bill-line.

FOR EACH queasy WHERE queasy.KEY EQ 270 
    AND queasy.number1 EQ 1 
    AND queasy.betriebsnr EQ 1 NO-LOCK:

         IF queasy.number2 EQ 6  THEN programid      = queasy.char2.
    ELSE IF queasy.number2 EQ 7  THEN walletid       = queasy.char2.
    ELSE IF queasy.number2 EQ 11 THEN terminalid     = queasy.char2.
    ELSE IF queasy.number2 EQ 17 THEN sftp-localpath = queasy.char2.
    ELSE IF queasy.number2 EQ 18 THEN segment-list   = queasy.char2.
    ELSE IF queasy.number2 EQ 19 THEN deptnr         = INT(queasy.char2).
END.

FOR EACH bill-line WHERE bill-line.bill-datum GE from-date 
    AND bill-line.bill-datum LE to-date
    AND bill-line.departemen EQ 0
    AND bill-line.artnr EQ 99
    AND bill-line.betrag GT 0 NO-LOCK:
    FIND FIRST bill WHERE bill.rechnr EQ bill-line.rechnr NO-LOCK NO-ERROR.
    FIND FIRST res-line WHERE res-line.resnr EQ bill.resnr AND res-line.zinr EQ bill-line.zinr NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK NO-ERROR.
        FIND FIRST segment WHERE segment.segmentcode EQ reservation.segmentcode NO-LOCK NO-ERROR.
        FIND FIRST sourccod WHERE sourccod.source-code EQ reservation.resart NO-LOCK NO-ERROR.
        FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
        FIND FIRST zimmer WHERE zimmer.zinr EQ bill-line.zinr NO-LOCK NO-ERROR.

        FIND FIRST output-list WHERE output-list.billnumber EQ bill.rechnr NO-ERROR.
        IF NOT AVAILABLE output-list THEN
        DO:
            CREATE output-list.
            ASSIGN 
            output-list.timestamp     = STRING(YEAR(TODAY),"9999") + "-" + STRING(MONTH(TODAY),"99") + "-" + STRING(DAY(TODAY),"99") + "T" + STRING(TIME,"HH:MM:SS") + "Z"
            output-list.billnumber    = bill.rechnr
            output-list.terminalid    = terminalid
            output-list.programid     = programid
            output-list.walletid      = walletid
            output-list.zinr          = res-line.zinr
            output-list.resnr         = res-line.resnr        
            output-list.reslinnr      = res-line.reslinnr          
            output-list.gastnrmember  = res-line.gastnrmember
            output-list.segment       = segment.bezeich
            output-list.sob           = sourccod.bezeich
            output-list.send-date     = TODAY
            output-list.data-date     = res-line.abreise
            output-list.price         = (bill-line.betrag / 1.21)
            output-list.price-str     = TRIM(STRING(bill-line.betrag / 1.21, "->>>>>>>>9")) + ";"
            output-list.amount        = (bill-line.betrag / 1.21) 
            output-list.sku           = bill-line.zinr + ";"
            output-list.itemname      = zimmer.bezeich + ";"
            output-list.qty           = "1;"            
            .
            IF guest.mobil-telefon NE "" THEN output-list.phone = guest.mobil-telefon.
            ELSE output-list.phone = guest.telefon.
        
            IF output-list.phone NE "" THEN
            DO:
                DEF VAR prefix AS CHAR.
                DEF VAR phnumb AS CHAR.
                prefix = SUBSTRING(output-list.phone,1,1).
                phnumb = SUBSTRING(output-list.phone,2,LENGTH(output-list.phone)).
        
                IF prefix EQ "0" THEN
                DO:
                    prefix = "+62".
                    output-list.phone = prefix + phnumb.
                END. 
            END.
        END.
        ELSE
        DO:
            output-list.sku       = bill-line.zinr           + ";" + output-list.sku. 
            output-list.itemname  = zimmer.bezeich           + ";" + output-list.itemname. 
            output-list.qty       = "1"                      + ";" + output-list.qty.
            output-list.price     = (bill-line.betrag / 1.21) + output-list.price.
            output-list.price-str = TRIM(STRING(bill-line.betrag / 1.21, "->>>>>>>>9")) + ";" + output-list.price-str.
            output-list.amount    = (bill-line.betrag / 1.21) + output-list.amount.
        END.
        /*DISP bill-line.rechnr bill-line.bill-datum bill-line.betrag bill-line.bezeich bill.zinr bill-line.zinr res-line.resnr res-line.NAME WITH WIDTH 140.*/
    END.
END.
/**/
FOR EACH output-list WHERE output-list.amount EQ 0:
    DELETE output-list.
END.

FOR EACH output-list:
    FOR EACH bill-line WHERE bill-line.rechnr EQ output-list.billnumber 
        AND bill-line.zinr EQ output-list.zinr 
        AND bill-line.betrag LT 0 NO-LOCK:
        output-list.paymentmethod = bill-line.bezeich.
    END.
    IF LENGTH(output-list.itemname ) GT 0 THEN output-list.itemname  = SUBSTRING(output-list.itemname, 1,LENGTH(output-list.itemname ) - 1).
    IF LENGTH(output-list.price-str) GT 0 THEN output-list.price-str = SUBSTRING(output-list.price-str,1,LENGTH(output-list.price-str) - 1).
    IF LENGTH(output-list.sku      ) GT 0 THEN output-list.sku       = SUBSTRING(output-list.sku,      1,LENGTH(output-list.sku      ) - 1).
    IF LENGTH(output-list.qty      ) GT 0 THEN output-list.qty       = SUBSTRING(output-list.qty,      1,LENGTH(output-list.qty      ) - 1).
END.

IF segment-list NE "" THEN
DO:
    FOR EACH output-list WHERE NOT segment-list MATCHES "*" + output-list.segment + "*" EXCLUSIVE-LOCK:
        DELETE output-list.
    END.
END.

