
DEF INPUT  PARAMETER hbrecid AS INT.

DEF OUTPUT PARAMETER order-id  AS CHAR.
DEF OUTPUT PARAMETER prdisc-flag AS LOGICAL.
DEF OUTPUT PARAMETER disc-art1 AS INT.
DEF OUTPUT PARAMETER disc-art2 AS INT.
DEF OUTPUT PARAMETER disc-art3 AS INT.
DEF OUTPUT PARAMETER disc-zwkum AS INT.
DEF OUTPUT PARAMETER print-balance AS LOGICAL.
DEF OUTPUT PARAMETER incl-service AS LOGICAL.
DEF OUTPUT PARAMETER incl-mwst AS LOGICAL.
DEF OUTPUT PARAMETER service-taxable AS LOGICAL.
DEF OUTPUT PARAMETER print-fbTotal AS LOGICAL.

DEFINE VARIABLE curr-dept       AS INTEGER NO-UNDO.

FIND FIRST vhp.h-bill WHERE RECID(vhp.h-bill) = hbrecid NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.h-bill AND vhp.h-bill.departement NE ? THEN
DO:
    ASSIGN curr-dept = vhp.h-bill.departement.
    IF vhp.h-bill.betriebsnr NE 0 THEN 
    DO: 
        FIND FIRST vhp.queasy WHERE vhp.queasy.key = 10 
            AND vhp.queasy.number1 = vhp.h-bill.betriebsnr NO-LOCK NO-ERROR. 
        /*IF AVAILABLE vhp.queasy THEN order-id = "/" + vhp.queasy.char1. */
        IF AVAILABLE vhp.queasy THEN order-id = "/" + vhp.queasy.char2. /* Gerald 260220 */
    END. 
END.


FIND FIRST vhp.htparam WHERE paramnr = 857 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.htparam THEN
DO:
    prdisc-flag = vhp.htparam.flogical. 
END.

FIND FIRST vhp.htparam WHERE paramnr = 557 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.htparam AND vhp.htparam.finteger GT 0 THEN
DO:
    disc-art1 = vhp.htparam.finteger. 
END.


FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = disc-art1
    AND vhp.h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-artikel THEN
DO:
    disc-zwkum = vhp.h-artikel.zwkum.
END.

FIND FIRST vhp.htparam WHERE paramnr = 596 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.htparam AND vhp.htparam.finteger GT 0 THEN
DO:
    disc-art2 = vhp.htparam.finteger. 
    IF disc-zwkum = 0 AND disc-art2 NE 0 THEN
    DO:
        FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = disc-art2
            AND vhp.h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
        IF AVAILABLE vhp.h-artikel THEN
        DO:
            disc-zwkum = vhp.h-artikel.zwkum.
        END.
    END.
END.


FIND FIRST vhp.htparam WHERE paramnr = 556 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.htparam AND vhp.htparam.finteger GT 0 THEN
DO:
    disc-art3 = vhp.htparam.finteger. 
    IF disc-zwkum = 0 AND disc-art3 NE 0 THEN
    DO:
        FIND FIRST vhp.h-artikel WHERE vhp.h-artikel.artnr = disc-art3
            AND vhp.h-artikel.departement = curr-dept NO-LOCK NO-ERROR.
        IF AVAILABLE vhp.h-artikel THEN 
        DO:
            disc-zwkum = vhp.h-artikel.zwkum.
        END.
    END.
END.

 
FIND FIRST vhp.htparam WHERE paramnr = 899 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.htparam THEN
DO:
    print-balance = vhp.htparam.flogical. 
END.

 
FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.htparam THEN
DO:
    incl-service = vhp.htparam.flogical. 
END.

 
FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.htparam THEN
DO:
    incl-mwst = vhp.htparam.flogical. 
END.

 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 479 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.htparam THEN
DO:
    service-taxable = vhp.htparam.flogical. 
END.

 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 948 NO-LOCK NO-ERROR. /*Alder - Serverless - Issue 629*/
IF AVAILABLE vhp.htparam THEN
DO:
    IF vhp.htparam.paramgr = 19 AND vhp.htparam.flogical THEN
    DO:
        print-fbTotal = htparam.flogical.
    END.
END.

