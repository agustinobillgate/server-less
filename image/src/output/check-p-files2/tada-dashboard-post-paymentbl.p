DEFINE INPUT PARAMETER user-init      AS CHAR.
DEFINE INPUT PARAMETER deptNo         AS INT.
DEFINE INPUT PARAMETER orderid        AS INT.
DEFINE INPUT PARAMETER payment-artnr  AS INT.
DEFINE INPUT PARAMETER payment-amount AS DECIMAL.

DEFINE OUTPUT PARAMETER result-message AS CHAR NO-UNDO.

DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF TEMP-TABLE t-submenu-list
    FIELD menurecid    AS INTEGER 
    FIELD zeit         AS INTEGER 
    FIELD nr           AS INTEGER 
    FIELD artnr        LIKE h-artikel.artnr 
    FIELD bezeich      LIKE h-artikel.bezeich 
    FIELD anzahl       AS INTEGER 
    FIELD zknr         AS INTEGER 
    FIELD request      AS CHAR. 

DEF TEMP-TABLE t-kellner1   LIKE vhp.kellner.

DEFINE BUFFER tablecolor FOR queasy.
DEFINE BUFFER orderhdr   FOR queasy.
DEFINE BUFFER orderline  FOR queasy.
DEFINE BUFFER mapping    FOR queasy. /*queasy 270 number1 3*/

DEFINE VARIABLE vhp-artno    AS INTEGER.
DEFINE VARIABLE vhp-artdep   AS INTEGER.

DEFINE VARIABLE i-str           AS INT.
DEFINE VARIABLE mess-token      AS CHAR.
DEFINE VARIABLE mess-keyword    AS CHAR.
DEFINE VARIABLE mess-value      AS CHAR.

DEFINE VARIABLE language-code   AS INT INIT 1.
DEFINE VARIABLE service-code    AS INT.
DEFINE VARIABLE rec-id          AS INT.
DEFINE VARIABLE tischnr         AS INT.
DEFINE VARIABLE curr-dept       AS INT.
DEFINE VARIABLE pax             AS INT.
DEFINE VARIABLE resnr           AS INT.
DEFINE VARIABLE reslinnr        AS INT.
DEFINE VARIABLE fl-code         AS INT INIT 0.
DEFINE VARIABLE fl-code1        AS INT INIT 0.
DEFINE VARIABLE fl-code2        AS INT INIT 0.
DEFINE VARIABLE fl-code3        AS INT INIT 0.
DEFINE VARIABLE bill-date       AS DATE.
DEFINE VARIABLE cancel-flag     AS LOGICAL.
DEFINE VARIABLE mwst            LIKE vhp.h-bill-line.betrag INIT 0.
DEFINE VARIABLE mwst-foreign    LIKE vhp.h-bill-line.betrag INIT 0.
DEFINE VARIABLE balance         AS DECIMAL.
DEFINE VARIABLE bcol            AS INT.
DEFINE VARIABLE balance-foreign AS DECIMAL.
DEFINE VARIABLE p-88            AS LOGICAL.
DEFINE VARIABLE closed          AS LOGICAL.
DEFINE VARIABLE rechnr          AS INT.


curr-dept = deptNo.
pax       = 1.


FIND FIRST orderhdr WHERE orderhdr.KEY EQ 271 
    AND orderhdr.betriebsnr EQ 1 
    AND orderhdr.number1 EQ deptNo
    AND orderhdr.number2 EQ orderid NO-LOCK NO-ERROR.
IF AVAILABLE orderhdr THEN
DO:
    rechnr  = orderhdr.number3.
    tischnr = INT(ENTRY(2,orderhdr.char2,"|")).
END.
       
FIND FIRST mapping WHERE mapping.KEY EQ 270 
    AND mapping.number1 EQ 3 
    AND mapping.number2 EQ payment-artnr 
    AND mapping.betriebsnr EQ deptNo NO-LOCK NO-ERROR.
IF AVAILABLE mapping THEN 
DO:
    vhp-artno  = mapping.number3.
    vhp-artdep = mapping.betriebsnr.
END.

FIND FIRST h-artikel WHERE h-artikel.departement EQ vhp-artdep AND h-artikel.artnr EQ vhp-artno NO-LOCK NO-ERROR.
                            
RUN tada-post-paymentbl (language-code, rec-id, RECID(h-artikel), "", ?,
    h-artikel.artart, NO, h-artikel.service-code, - DECIMAL(payment-amount),
    - DECIMAL(payment-amount),0,NO, 1,1,0, user-init, tischnr, curr-dept, user-init, "", pax, 0,
    0, h-artikel.artnr, h-artikel.bezeich, "", "","", "", "", "", YES,NO, h-artikel.artnrfront, 
    0, 0, "",NO, NO, "", user-init, resnr, reslinnr,
    INPUT TABLE t-submenu-list, OUTPUT bill-date,
    OUTPUT cancel-flag, OUTPUT fl-code, OUTPUT mwst,
    OUTPUT mwst-foreign, OUTPUT rechnr, OUTPUT balance,
    OUTPUT bcol, OUTPUT balance-foreign, OUTPUT fl-code1,
    OUTPUT fl-code2, OUTPUT fl-code3, OUTPUT p-88, OUTPUT closed,
    OUTPUT TABLE t-h-bill, OUTPUT TABLE t-kellner1).

    /*MESSAGE "fl-code  : " + string(fl-code ) skip
            "fl-code1 : " + string(fl-code1) skip
            "fl-code2 : " + string(fl-code2) skip
            "fl-code3 : " + string(fl-code3) skip
            "rechnr : " + STRING(rechnr)
        VIEW-AS ALERT-BOX INFO BUTTONS OK.*/
                 
IF closed THEN
DO:                                
    /*CHECK TABLE IN QUEASY 31 KEMBALIKAN KE COLOR IJO*/
    FIND FIRST tablecolor WHERE tablecolor.key EQ 31 AND tablecolor.number1 EQ curr-dept
        AND tablecolor.betriebsnr EQ 0 
        AND tablecolor.number2 EQ tischnr EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE tablecolor THEN
    DO:
        FIND FIRST tisch WHERE tisch.departement EQ tablecolor.number1
        AND tisch.tischnr = tablecolor.number2 NO-LOCK NO-ERROR.
        IF AVAILABLE tisch THEN
        DO:
            ASSIGN tablecolor.date1   = ?
                   tablecolor.number3 = 0.
        END.
    END.
END.       
result-message = "0 - Post Payment Success!".

