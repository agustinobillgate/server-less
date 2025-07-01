
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
    FIELD segcode     AS CHAR /* add by damen */.

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
    FIELD voucher       AS CHARACTER FORMAT "x(20)"
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
    .

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
DEFINE OUTPUT PARAMETER TABLE FOR fo-journal-list.

DEFINE VARIABLE gtot AS DECIMAL FORMAT "->,>>>,>>>,>>9.99" INITIAL 0. 

RUN fo-journal-cldbl.p (from-art, to-art, from-dept, to-dept, from-date, to-date,
    sorttype, exclude-ARTrans, long-digit, foreign-flag,
    onlyjournal, excljournal, mi-post, mi-showrelease, OUTPUT gtot, OUTPUT TABLE output-list).

FOR EACH fo-journal-list:
    DELETE fo-journal-list.
END.

FOR EACH output-list:
    CREATE fo-journal-list.
    ASSIGN 
        fo-journal-list.datum      = DATE(SUBSTRING(output-list.str, 1,8))  
        fo-journal-list.c          = output-list.c  
        fo-journal-list.roomnumber = SUBSTRING(output-list.STR,9,6) 
        fo-journal-list.nsflag     = output-list.ns  
        fo-journal-list.mbflag     = output-list.mb  
        fo-journal-list.shift      = output-list.shift  
        fo-journal-list.billno     = INTEGER(SUBSTRING(output-list.STR,15,9)) 
        fo-journal-list.artno      = INTEGER(SUBSTRING(output-list.STR,24,4)) 
        fo-journal-list.bezeich    = output-list.descr  
        fo-journal-list.voucher    = output-list.voucher  
        fo-journal-list.depart     = SUBSTRING(output-list.STR,78, 12) 
        fo-journal-list.outlet     = SUBSTRING(output-list.STR,90, 6)   
        fo-journal-list.qty        = INTEGER(SUBSTRING(output-list.STR,96,5)) 
        fo-journal-list.amount     = DECIMAL(SUBSTRING(output-list.STR,101,22))  
        fo-journal-list.guestname  = output-list.guestname
        fo-journal-list.billrcvr   = output-list.gname   
        fo-journal-list.zeit       = SUBSTRING(output-list.STR,123, 8)
        fo-journal-list.id         = SUBSTRING(output-list.STR,131, 4)  
        fo-journal-list.sysdate    = DATE(SUBSTRING(output-list.STR,135,8))
        fo-journal-list.remark     = output-list.remark
        fo-journal-list.checkin    = output-list.checkin
        fo-journal-list.checkout   = output-list.checkout
        fo-journal-list.segcode    = output-list.segcode /* add by damen */
        .
END.
