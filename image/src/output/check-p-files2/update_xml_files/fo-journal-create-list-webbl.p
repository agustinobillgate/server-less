
DEFINE TEMP-TABLE fo-journal-list
    FIELD datum         AS DATE
    FIELD c             AS CHARACTER FORMAT "x(2)"
    FIELD roomnumber    AS CHARACTER 
    FIELD nsflag        AS CHARACTER FORMAT "x(1)"
    FIELD mbflag        AS CHARACTER FORMAT "x(1)"
    FIELD shift         AS CHARACTER FORMAT "x(2)"
    FIELD billno        AS INTEGER   FORMAT ">>>>>>>>>"
    FIELD artno         AS INTEGER   FORMAT ">>>>"
    FIELD bezeich       AS CHARACTER FORMAT "x(50)"
    FIELD voucher       AS CHARACTER FORMAT "x(40)"
    FIELD depart        AS CHARACTER FORMAT "x(12)"
    FIELD outlet        AS CHARACTER FORMAT "x(6)"
    FIELD qty           AS INTEGER   FORMAT "->>>>"
    FIELD amount        AS DECIMAL   FORMAT "->>,>>>,>>>,>>9.99"
    FIELD guestname     AS CHARACTER FORMAT "x(25)"
    FIELD billrcvr      AS CHARACTER FORMAT "x(24)"
    FIELD zeit          AS CHARACTER FORMAT "x(8)"
    FIELD id            AS CHARACTER FORMAT "x(4)"
    FIELD sysdate       AS DATE
    FIELD remark        AS CHARACTER FORMAT "x(24)"
    FIELD checkin       AS DATE
    FIELD checkout      AS DATE
    FIELD segcode       AS CHAR 
    FIELD amt-nett      AS DECIMAL
    FIELD service       AS DECIMAL
    FIELD vat           AS DECIMAL
    FIELD vat-percentage  AS DECIMAL
    FIELD serv-percentage AS DECIMAL
    FIELD deptno        AS INT
    FIELD nationality   AS CHAR
    FIELD resnr         AS INT
    FIELD book-source   AS CHAR
    FIELD resname       AS CHARACTER FORMAT "x(25)" 
.

DEFINE INPUT PARAMETER id-flag          AS CHARACTER.
DEFINE OUTPUT PARAMETER done-flag    AS LOGICAL NO-UNDO INITIAL NO.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR fo-journal-list.

DEFINE VARIABLE counter   AS INTEGER NO-UNDO INITIAL 0.
DEFINE VARIABLE queasy-str1  AS CHARACTER NO-UNDO. 
DEFINE VARIABLE queasy-str2  AS CHARACTER NO-UNDO. 
DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.

FOR EACH queasy WHERE queasy.KEY = 280 AND queasy.char1 = "FO Transaction"
    AND queasy.char2 = id-flag NO-LOCK BY queasy.number1:

        ASSIGN 
            counter = counter + 1
            queasy-str1 = ENTRY(1,queasy.char3,"|")
            queasy-str2 = ENTRY(2,queasy.char3,"|")
        .
        /* */
        IF counter GT 1000 THEN LEAVE.

        CREATE fo-journal-list.
        ASSIGN 
            fo-journal-list.datum       = DATE(SUBSTRING(queasy-str1, 1,8))                 
            fo-journal-list.c           = TRIM(SUBSTRING(queasy-str2, 1,2) )                
            fo-journal-list.roomnumber  = TRIM(SUBSTRING(queasy-str2, 3,6) )                
            fo-journal-list.nsflag      = TRIM(SUBSTRING(queasy-str2, 9,1) )                
            fo-journal-list.mbflag      = TRIM(SUBSTRING(queasy-str2, 10,1))                
            fo-journal-list.shift       = TRIM(SUBSTRING(queasy-str2, 11,2))                
            fo-journal-list.billno      = INTEGER(SUBSTRING(queasy-str1,15,9))              
            fo-journal-list.artno       = INTEGER(SUBSTRING(queasy-str1,24,4))              
            fo-journal-list.bezeich     = TRIM(SUBSTRING(queasy-str2, 13,50))               
            fo-journal-list.voucher     = TRIM(SUBSTRING(queasy-str2, 63,40))               
            fo-journal-list.depart      = SUBSTRING(queasy-str1,78, 12)                     
            fo-journal-list.outlet      = SUBSTRING(queasy-str1,90, 6)                      
            fo-journal-list.qty         = INTEGER(SUBSTRING(queasy-str1,96,5))              
            fo-journal-list.amount      = DECIMAL(SUBSTRING(queasy-str1,101,22))            
            fo-journal-list.guestname   = TRIM(SUBSTRING(queasy-str2, 103,25))              
            fo-journal-list.billrcvr    = TRIM(SUBSTRING(queasy-str2, 128,24))              
            fo-journal-list.zeit        = SUBSTRING(queasy-str1,123, 8)                     
            fo-journal-list.id          = SUBSTRING(queasy-str1,131, 4)                     
            fo-journal-list.sysdate     = DATE(SUBSTRING(queasy-str1,135,8))                
            fo-journal-list.remark      = TRIM(SUBSTRING(queasy-str2, 152,124))              
            fo-journal-list.checkin     = DATE(SUBSTRING(queasy-str2, 276,8))               
            fo-journal-list.checkout    = DATE(SUBSTRING(queasy-str2, 284,8))               
            fo-journal-list.segcode     = TRIM(SUBSTRING(queasy-str2, 292,20))              
            fo-journal-list.deptno      = INTEGER(TRIM(SUBSTRING(queasy-str2, 312,2)))      
            fo-journal-list.nationality = TRIM(SUBSTRING(queasy-str2, 314,5))               
            fo-journal-list.resnr       = INTEGER(TRIM(SUBSTRING(queasy-str2, 319,10)))     
            fo-journal-list.book-source = TRIM(SUBSTRING(queasy-str2, 329,20))              
            fo-journal-list.resname     = TRIM(SUBSTRING(queasy-str2, 349,25))              
            .


        IF queasy.logi1 THEN
        DO:
            ASSIGN fo-journal-list.amt-nett = DECIMAL(SUBSTRING(queasy-str2, 374,21))      
                   fo-journal-list.service  = DECIMAL(SUBSTRING(queasy-str2, 395,21))      
                   fo-journal-list.vat      = DECIMAL(SUBSTRING(queasy-str2, 416,21))      
                .                                                                          

            FIND FIRST artikel WHERE artikel.departement EQ fo-journal-list.deptno 
                AND artikel.artnr EQ fo-journal-list.artno NO-LOCK NO-ERROR.
            IF AVAILABLE artikel THEN
            DO:
                FIND FIRST htparam WHERE paramnr EQ artikel.mwst-code NO-LOCK NO-ERROR.
                IF AVAILABLE htparam THEN fo-journal-list.vat-percentage = htparam.fdecimal.
                ELSE fo-journal-list.vat-percentage = 0.

                FIND FIRST htparam WHERE paramnr EQ artikel.service-code NO-LOCK NO-ERROR.
                IF AVAILABLE htparam THEN fo-journal-list.serv-percentage = htparam.fdecimal.
                ELSE fo-journal-list.serv-percentage = 0.

            END.
        END.

        FIND FIRST bqueasy WHERE RECID(bqueasy) = RECID(queasy) EXCLUSIVE-LOCK.
        DELETE bqueasy.
        RELEASE bqueasy. 
END. 

FIND FIRST pqueasy WHERE pqueasy.KEY = 280
    AND pqueasy.char1 = "FO Transaction"
    AND pqueasy.char2 = id-flag NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN DO:
    ASSIGN done-flag = NO.
END.
ELSE DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY = 285
        AND tqueasy.char1 = "FO Transaction"
        AND tqueasy.number1 = 1
        AND tqueasy.char2 = id-flag NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN DO:
        ASSIGN done-flag = NO.
    END.
    ELSE DO:
        ASSIGN done-flag = YES.
    END.
END.

FIND FIRST tqueasy WHERE tqueasy.KEY = 285
    AND tqueasy.char1 = "FO Transaction"
    AND tqueasy.number1 = 0
    AND tqueasy.char2 = id-flag NO-LOCK NO-ERROR.
IF AVAILABLE tqueasy THEN DO:
    FIND CURRENT tqueasy EXCLUSIVE-LOCK.
    DELETE tqueasy.
    RELEASE tqueasy.
END.

