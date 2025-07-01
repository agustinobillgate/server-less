DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line  
    FIELD rec-id AS INT.  
  
  
DEF INPUT PARAMETER pvILanguage         AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER dept                AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER rec-id-h-bill       AS INTEGER NO-UNDO.  
  
DEF INPUT PARAMETER multi-cash          AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER cash-artno          AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER cash-foreign        AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER pay-voucher         AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER full-paid           AS LOGICAL NO-UNDO.  
DEF INPUT PARAMETER voucher-nr          AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER amt                 AS DECIMAL NO-UNDO.  
DEF INPUT PARAMETER changed             AS DECIMAL NO-UNDO.  
DEF INPUT PARAMETER changed-foreign     AS DECIMAL NO-UNDO.  
DEF INPUT PARAMETER lchange             AS DECIMAL NO-UNDO.  
  
DEF INPUT PARAMETER amount              AS DECIMAL NO-UNDO.  
DEF INPUT PARAMETER transdate           AS DATE    NO-UNDO.  
DEF INPUT PARAMETER change-str          AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER tischnr             AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER add-zeit            AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER curr-select         AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER hoga-card           AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER cancel-str          AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER curr-waiter         AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER amount-foreign      AS DECIMAL NO-UNDO.  
DEF INPUT PARAMETER curr-room           AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER user-init           AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER cc-comment          AS CHAR    NO-UNDO.  
DEF INPUT PARAMETER guestnr             AS INTEGER NO-UNDO.  
DEF INPUT PARAMETER cash-type           AS INTEGER NO-UNDO.  
  
DEF OUTPUT PARAMETER billart            AS INTEGER NO-UNDO.  
DEF OUTPUT PARAMETER qty                AS INTEGER NO-UNDO.  
DEF OUTPUT PARAMETER description        AS CHAR    NO-UNDO.  
DEF OUTPUT PARAMETER price              AS DECIMAL NO-UNDO.  
DEF OUTPUT PARAMETER answer             AS LOGICAL NO-UNDO.  
DEF OUTPUT PARAMETER bill-date          AS DATE    NO-UNDO.  
DEF OUTPUT PARAMETER fl-code            AS INTEGER NO-UNDO INIT 0.  

DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.  
  
{supertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "TS-splitbill".  

DEFINE VARIABLE price-decimal AS INTEGER.
  
IF multi-cash OR cash-type = 1 THEN billart = cash-artno.   
ELSE   
DO:   
    IF cash-foreign THEN FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 854 NO-LOCK.   
    ELSE   
    DO:   
        IF NOT pay-voucher THEN FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 855 NO-LOCK.   
        ELSE FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 1001 NO-LOCK.   
    END.   
    billart = vhp.htparam.finteger.   
END.   
FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = dept   
    AND vhp.h-artikel.artnr = billart NO-LOCK.   
  
qty = 1.  
description = vhp.h-artikel.bezeich.

IF cash-type = 1 THEN ASSIGN DESCRIPTION = REPLACE(DESCRIPTION, " ", "").

IF voucher-nr NE "" THEN DESCRIPTION = DESCRIPTION + " " + voucher-nr.   
price = 0.  
/*MT  
RUN update-bill(h-artikel.artart, vhp.h-artikel.artnrfront).  
*/  
RUN ts-splitbill-update-billbl.p  
    (rec-id-h-bill, RECID(h-artikel), h-artikel.artart, vhp.h-artikel.artnrfront, dept, amount, transdate, billart, description, change-str, qty, tischnr,  
     price, add-zeit, curr-select, hoga-card, cancel-str, curr-waiter, amount-foreign,  
     curr-room, user-init, cc-comment, guestnr, OUTPUT bill-date).  
answer = NO.  
  
/***********************************/     
FIND FIRST h-bill WHERE RECID(h-bill) = rec-id-h-bill NO-LOCK NO-ERROR.  /*FDL Ticket Serverless #521 - add if available*/
IF AVAILABLE h-bill THEN
DO:
    FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 491 NO-LOCK NO-ERROR.   
    IF AVAILABLE htparam THEN price-decimal = vhp.htparam.finteger.   /* non-digit OR digit version */ 

    IF full-paid AND amt NE 0 THEN   
    DO:   
        add-zeit = 1.   
        IF multi-cash THEN   
        DO:   
            IF changed NE 0 THEN   
            DO:   
                amount = changed.   
                amount-foreign = changed-foreign.   
                change-str = translateExtended ("(Change)",lvCAREA,"").   
                RUN ts-splitbill-update-billbl.p  
                    (rec-id-h-bill, RECID(h-artikel), h-artikel.artart, vhp.h-artikel.artnrfront, dept, amount, transdate, billart, description, change-str, qty, tischnr,  
                     price, add-zeit, curr-select, hoga-card, cancel-str, curr-waiter, amount-foreign,  
                     curr-room, user-init, cc-comment, guestnr, OUTPUT bill-date).  
            END.   
            IF lchange NE 0 THEN   
            DO:   
                add-zeit = add-zeit + 1.   
                amount = lchange.   
                amount-foreign = lchange.   
                change-str = translateExtended ("(Change)",lvCAREA,"").   
                FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 855 NO-LOCK.   
                billart = vhp.htparam.finteger.   
                FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.departement = dept   
                  AND vhp.h-artikel.artnr = billart NO-LOCK.   
                description = vhp.h-artikel.bezeich.   
                change-str = translateExtended ("(Change)",lvCAREA,"").   
                RUN ts-splitbill-update-billbl.p  
                    (rec-id-h-bill, RECID(h-artikel), h-artikel.artart, vhp.h-artikel.artnrfront, dept, amount, transdate, billart, description, change-str, qty, tischnr,  
                     price, add-zeit, curr-select, hoga-card, cancel-str, curr-waiter, amount-foreign,  
                     curr-room, user-init, cc-comment, guestnr, OUTPUT bill-date).  
            END.   
        END.   
        ELSE   
        DO:   
            amount = - amt. /* change */   
            change-str = translateExtended ("(Change)",lvCAREA,"").   
            RUN ts-splitbill-update-billbl.p  
                (rec-id-h-bill, RECID(h-artikel), h-artikel.artart, vhp.h-artikel.artnrfront, dept, amount, transdate, billart, description, change-str, qty, tischnr,  
                 price, add-zeit, curr-select, hoga-card, cancel-str, curr-waiter, amount-foreign,  
                 curr-room, user-init, cc-comment, guestnr, OUTPUT bill-date).  
        END.   
    END.   
   
    add-zeit = 0.   
   
    IF ROUND(vhp.h-bill.saldo, price-decimal) = 0 THEN   
    DO:   
        /* FDL Comment Ticket Serverless #521 - takeout from procedure
        RUN del-queasy.   
        */
        FOR EACH vhp.queasy WHERE vhp.queasy.key = 4   
            AND vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
            AND vhp.queasy.number2 GE 0 AND vhp.queasy.deci2 GE 0 EXCLUSIVE-LOCK:   
            DELETE vhp.queasy.   
        END.           

        FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK.   
        vhp.h-bill.flag = 1.   
        FIND CURRENT vhp.h-bill NO-LOCK.  
        fl-code = 1.          
    END.   
    ELSE   
    DO:   
        fl-code = 2.        
    END.

    FOR EACH h-bill-line WHERE h-bill-line.departement = dept
        AND h-bill-line.rechnr = h-bill.rechnr NO-LOCK:  

        CREATE t-h-bill-line.  
        BUFFER-COPY h-bill-line TO t-h-bill-line.  
        ASSIGN t-h-bill-line.rec-id = RECID(h-bill-line).  
    END.  
END.
/* FDL Comment Ticket Serverless #521 - Move Above takeout from procedure
PROCEDURE del-queasy:   
  FOR EACH vhp.queasy WHERE vhp.queasy.key = 4   
    AND vhp.queasy.number1 = (vhp.h-bill.departement + vhp.h-bill.rechnr * 100)   
    AND vhp.queasy.number2 GE 0 AND vhp.queasy.deci2 GE 0 EXCLUSIVE-LOCK:   
    DELETE vhp.queasy.   
  END.   
  RELEASE vhp.queasy.
END.   
*/  
