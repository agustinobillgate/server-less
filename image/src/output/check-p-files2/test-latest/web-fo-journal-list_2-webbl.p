DEFINE TEMP-TABLE output-list 
    FIELD bezeich     AS CHAR 
    FIELD c           AS CHAR FORMAT "x(2)" 
    FIELD NS          AS CHAR FORMAT "x(1)"
    FIELD MB          AS CHAR FORMAT "x(1)"
    FIELD shift       AS CHAR FORMAT "x(2)"
    FIELD dept        AS CHAR FORMAT "x(2)"
    FIELD STR         AS CHAR
    FIELD remark      AS CHAR FORMAT "x(24)" LABEL "Remark"
    FIELD gname       AS CHAR FORMAT "x(24)" LABEL "Bill Receiver"
    FIELD descr       AS CHAR
    FIELD voucher     AS CHAR
    FIELD checkin     AS DATE
    FIELD checkout    AS DATE
    FIELD guestname   AS CHAR
    FIELD segcode     AS CHAR /* add by damen */
    FIELD amt-nett    AS DECIMAL
    FIELD service     AS DECIMAL
    FIELD vat         AS DECIMAL
    FIELD zinr        AS CHAR
    FIELD deptno      AS INT
    /* Dzikri B6184F - Add new field */
    FIELD nationality AS CHAR
    FIELD resnr       AS INT
    FIELD book-source AS CHAR
    /* Dzikri B6184F - END */
    /* Dzikri 706CDB - Add reserve name */
    FIELD resname       AS CHARACTER FORMAT "x(25)"
    /* Dzikri 706CDB - END */
 .                    

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
    FIELD segcode       AS CHAR /* add by damen */ /*notes: please tell backend team if there is enhancement on Backend Program*/
    FIELD amt-nett      AS DECIMAL
    FIELD service       AS DECIMAL
    FIELD vat           AS DECIMAL
    FIELD vat-percentage  AS DECIMAL
    FIELD serv-percentage AS DECIMAL
    FIELD deptno        AS INT
    /* Dzikri B6184F - Add new field */
    FIELD nationality   AS CHAR
    FIELD resnr         AS INT
    FIELD book-source   AS CHAR
    /* Dzikri B6184F - END */
    FIELD resname       AS CHARACTER FORMAT "x(25)"  /* Dzikri 706CDB - Add reserve name */
.
/**/
DEFINE INPUT PARAMETER from-art         AS INTEGER.
DEFINE INPUT PARAMETER to-art           AS INTEGER.
DEFINE INPUT PARAMETER from-dept        AS INTEGER.
DEFINE INPUT PARAMETER to-dept          AS INTEGER.
DEFINE INPUT PARAMETER from-date        AS DATE.
DEFINE INPUT PARAMETER to-date          AS DATE.
DEFINE INPUT PARAMETER sorttype         AS INTEGER.
DEFINE INPUT PARAMETER exclude-ARTrans  AS LOGICAL.
DEFINE INPUT PARAMETER long-digit       AS LOGICAL.
DEFINE INPUT PARAMETER foreign-flag     AS LOGICAL.
DEFINE INPUT PARAMETER onlyjournal      AS LOGICAL.
DEFINE INPUT PARAMETER excljournal      AS LOGICAL.
DEFINE INPUT PARAMETER mi-post          AS LOGICAL.
DEFINE INPUT PARAMETER mi-showrelease   AS LOGICAL.
DEFINE INPUT PARAMETER mi-break         AS LOGICAL.
DEFINE INPUT PARAMETER id-flag          AS CHARACTER. /* Dzikri 725A15 - create partial program */
DEFINE OUTPUT PARAMETER TABLE FOR fo-journal-list.
DEFINE OUTPUT PARAMETER done-flag    AS LOGICAL NO-UNDO INITIAL NO. /* Dzikri 725A15 - create partial program */

/*
DEFINE VARIABLE from-art         AS INTEGER INIT 1.
DEFINE VARIABLE to-art           AS INTEGER INIT 3050.
DEFINE VARIABLE from-dept        AS INTEGER INIT 0.
DEFINE VARIABLE to-dept          AS INTEGER INIT 0.
DEFINE VARIABLE from-date        AS DATE    INIT 04/01/24.
DEFINE VARIABLE to-date          AS DATE    INIT 04/20/24.
DEFINE VARIABLE sorttype         AS INTEGER INIT 0.
DEFINE VARIABLE exclude-ARTrans  AS LOGICAL INIT NO.
DEFINE VARIABLE long-digit       AS LOGICAL INIT NO.
DEFINE VARIABLE foreign-flag     AS LOGICAL INIT NO.
DEFINE VARIABLE onlyjournal   AS LOGICAL INIT NO.
DEFINE VARIABLE excljournal   AS LOGICAL INIT YES.
DEFINE VARIABLE mi-post          AS LOGICAL INIT YES.
DEFINE VARIABLE mi-showrelease   AS LOGICAL INIT YES.
DEFINE VARIABLE mi-break         AS LOGICAL INIT YES.
*/
DEFINE VARIABLE gtot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 

/* Dzikri 725A15 - create partial program */
DEF BUFFER bqueasy FOR queasy.

CREATE queasy.
ASSIGN queasy.KEY = 285
       queasy.char1 = "FO Transaction"
       queasy.number1 = 1
       queasy.char2 = id-flag.
RELEASE queasy.

RUN fo-journal-cld_3bl.p (from-art, to-art, from-dept, to-dept, from-date, to-date,
    sorttype, exclude-ARTrans, long-digit, foreign-flag,
    onlyjournal, excljournal, mi-post, mi-showrelease, mi-break, id-flag,
    OUTPUT gtot, OUTPUT TABLE output-list).

FIND FIRST bqueasy WHERE bqueasy.KEY = 285
    AND bqueasy.char1 = "FO Transaction"
    AND bqueasy.char2 = id-flag NO-LOCK NO-ERROR.
IF AVAILABLE bqueasy THEN DO:
    done-flag = YES.
    FIND CURRENT bqueasy EXCLUSIVE-LOCK.
    ASSIGN bqueasy.number1 = 0.
    FIND CURRENT bqueasy NO-LOCK.
    RELEASE bqueasy.
END.
/* Dzikri 725A15 - END */

EMPTY TEMP-TABLE fo-journal-list.
FOR EACH output-list:
    CREATE fo-journal-list.
    ASSIGN 
        fo-journal-list.datum       = DATE(SUBSTRING(output-list.str, 1,8))  
        fo-journal-list.c           = output-list.c  
        fo-journal-list.roomnumber  = output-list.zinr
        fo-journal-list.nsflag      = output-list.ns  
        fo-journal-list.mbflag      = output-list.mb  
        fo-journal-list.shift       = output-list.shift  
        fo-journal-list.billno      = INTEGER(SUBSTRING(output-list.STR,15,9)) 
        fo-journal-list.artno       = INTEGER(SUBSTRING(output-list.STR,24,4)) 
        fo-journal-list.bezeich     = output-list.descr  
        fo-journal-list.voucher     = output-list.voucher  
        fo-journal-list.depart      = SUBSTRING(output-list.STR,78, 12) 
        fo-journal-list.outlet      = SUBSTRING(output-list.STR,90, 6)   
        fo-journal-list.qty         = INTEGER(SUBSTRING(output-list.STR,96,5)) 
        fo-journal-list.amount      = DECIMAL(SUBSTRING(output-list.STR,101,22))  
        fo-journal-list.guestname   = output-list.guestname
        fo-journal-list.billrcvr    = output-list.gname   
        fo-journal-list.zeit        = SUBSTRING(output-list.STR,123, 8)
        fo-journal-list.id          = SUBSTRING(output-list.STR,131, 4)  
        fo-journal-list.sysdate     = DATE(SUBSTRING(output-list.STR,135,8))
        fo-journal-list.remark      = output-list.remark
        fo-journal-list.checkin     = output-list.checkin
        fo-journal-list.checkout    = output-list.checkout
        fo-journal-list.segcode     = output-list.segcode /* add by damen */
        fo-journal-list.deptno      = output-list.deptno
        /* Dzikri B6184F - Add new field */
        fo-journal-list.nationality = output-list.nationality
        fo-journal-list.resnr       = output-list.resnr
        fo-journal-list.book-source = output-list.book-source
        /* Dzikri B6184F - END */
        /* Dzikri 706CDB - Add reserve name */
        fo-journal-list.resname     = output-list.resname
        /* Dzikri 706CDB - END */
        .


    IF mi-break THEN
    DO:
        ASSIGN fo-journal-list.amt-nett = output-list.amt-nett
               fo-journal-list.service  = output-list.service
               fo-journal-list.vat      = output-list.vat
            .

        /*masdod 020724 tiket damen 61FE1A*/
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
END.
/*
CURRENT-WINDOW:WIDTH = 250.
FOR EACH fo-journal-list:
    DISP fo-journal-list.datum
         fo-journal-list.roomnumber
         fo-journal-list.billno   
         fo-journal-list.artno   
         fo-journal-list.bezeich
         fo-journal-list.guestname
         fo-journal-list.billrcvr WITH WIDTH 240. 
END.*/
