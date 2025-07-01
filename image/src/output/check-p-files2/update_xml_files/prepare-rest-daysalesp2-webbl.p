DEF TEMP-TABLE buf-art
    FIELD artnr       LIKE artikel.artnr
    FIELD bezeich     LIKE artikel.bezeich
    FIELD departement LIKE artikel.departement
    FIELD art-type AS INTEGER.

DEFINE TEMP-TABLE htl-dept
    FIELD dptnr     AS INTEGER COLUMN-LABEL "Number"
    FIELD bezeich   AS CHAR    COLUMN-LABEL "Description" FORMAT "x(24)".

DEF TEMP-TABLE usr1 LIKE kellner
    FIELD rec-id AS INT.

DEFINE TEMP-TABLE other-art
    FIELD artnr         AS INTEGER.

DEFINE OUTPUT PARAMETER errCode         AS CHAR.
DEFINE OUTPUT PARAMETER curr-local      as char. 
DEFINE OUTPUT PARAMETER price-decimal   as INT. 
DEFINE OUTPUT PARAMETER bezeich         as char format "x(1)" extent 21. 
DEFINE OUTPUT PARAMETER show-option     AS LOGICAL INITIAL NO NO-UNDO.
DEFINE OUTPUT PARAMETER oth-flag        AS LOGICAL INITIAL NO NO-UNDO.

DEFINE OUTPUT PARAMETER disc-art1       AS INTEGER INITIAL -1   NO-UNDO. 
DEFINE OUTPUT PARAMETER disc-art2       AS INTEGER INITIAL -1   NO-UNDO. 
DEFINE OUTPUT PARAMETER disc-art3       AS INTEGER INITIAL -1   NO-UNDO.
DEFINE OUTPUT PARAMETER exchg-rate      as decimal format ">>,>>9.99". 
DEFINE OUTPUT PARAMETER str             as char. 
DEFINE OUTPUT PARAMETER curr-foreign    as char.  
DEFINE OUTPUT PARAMETER serv-taxable    as logical initial NO. 
DEFINE OUTPUT PARAMETER dpt-str         AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER art-str         AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER oth-str         AS CHAR NO-UNDO.
DEFINE OUTPUT PARAMETER anzahl          as integer initial 0. 
DEFINE OUTPUT PARAMETER curr-dept       as integer.
DEFINE OUTPUT PARAMETER dept-name       as char.
DEFINE OUTPUT PARAMETER voucher-art     AS INTEGER INITIAL 0.
DEFINE OUTPUT PARAMETER use-voucher     AS LOGICAL INITIAL YES.
DEFINE OUTPUT PARAMETER from-date       as date.
DEFINE OUTPUT PARAMETER to-date         as date. 
DEFINE OUTPUT PARAMETER htl-dept-dptnr  AS INT.
DEFINE OUTPUT PARAMETER err-flag        AS INT INIT 0.
DEFINE OUTPUT PARAMETER p-110           AS DATE.
DEFINE OUTPUT PARAMETER p-240           AS LOGICAL.
DEFINE OUTPUT PARAMETER active-deposit  AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR buf-art.
DEFINE OUTPUT PARAMETER TABLE FOR htl-dept.
DEFINE OUTPUT PARAMETER TABLE FOR usr1.

DEFINE VARIABLE artnr-list  as integer extent 20. 
DEFINE VARIABLE i           as INTEGER. 

RUN prepare-rest-daysalesp2_1-cldbl.p
    (OUTPUT disc-art1, OUTPUT disc-art2, OUTPUT disc-art3,
    OUTPUT exchg-rate, OUTPUT str, OUTPUT curr-foreign,
    OUTPUT serv-taxable, OUTPUT dpt-str, OUTPUT art-str,
    OUTPUT oth-str, OUTPUT anzahl, OUTPUT curr-dept, OUTPUT dept-name,
    OUTPUT voucher-art, OUTPUT use-voucher, OUTPUT from-date,
    OUTPUT to-date, OUTPUT htl-dept-dptnr, OUTPUT err-flag,
    OUTPUT p-110, OUTPUT p-240, OUTPUT active-deposit,
    OUTPUT TABLE buf-art, OUTPUT TABLE htl-dept, OUTPUT TABLE usr1).

IF NUM-ENTRIES(str,";") GT 1 THEN
DO:
    ASSIGN
        curr-local      = ENTRY(1,str,";")
        price-decimal   = INT(ENTRY(2,str,";")).
END.    
ELSE
DO:
    ASSIGN
        curr-local = str.
END.
    
IF err-flag = 1 THEN
DO:
    errCode = STRING(err-flag) + " - Parameter no 732 not yet been setup.".
    RETURN.
END.
IF err-flag = 2 THEN
DO:
    errCode = STRING(err-flag) + " - Department not yet been setup in param 716.".
    RETURN.
END.

RUN rest-daysalesp2-check-dynacol-cldbl.p 
    (TABLE buf-art, art-str, htl-dept-dptnr, OUTPUT anzahl,
    OUTPUT artnr-list, OUTPUT bezeich, OUTPUT show-option).

IF oth-str NE "" THEN
DO:
    bezeich[21] = ENTRY(1, oth-str, ",").
    DO i = 2 TO NUM-ENTRIES(oth-str, ","):
        IF i GT 11 THEN .
        ELSE DO:
            CREATE other-art.
            ASSIGN 
                other-art.artnr = INTEGER(ENTRY(i, oth-str, ",")).
        END.
    END. 
    IF ENTRY(2, oth-str, ",") NE "" THEN
        oth-flag = YES.
END.

errCode = "0 - Retrieve data Success.".
