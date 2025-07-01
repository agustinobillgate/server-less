DEF TEMP-TABLE t-h-bill-line LIKE h-bill-line.

DEF INPUT  PARAMETER dept AS INT.
DEF INPUT  PARAMETER tischnr AS INT.

DEF OUTPUT PARAMETER price-decimal AS INT.
DEF OUTPUT PARAMETER exchg-rate AS DECIMAL.

DEF OUTPUT PARAMETER p-134 AS LOGICAL.
DEF OUTPUT PARAMETER p-135 AS LOGICAL.
DEF OUTPUT PARAMETER p-479 AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill-line.

/*Alder - Serverless - Issue 519 - Start*/
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr EQ 491 NO-LOCK NO-ERROR.
IF AVAILABLE vhp.htparam THEN
DO:
    ASSIGN price-decimal = vhp.htparam.finteger. 
END.
 
FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr EQ 144 NO-LOCK NO-ERROR.
IF AVAILABLE vhp.htparam THEN
DO:
    FIND FIRST vhp.waehrung WHERE vhp.waehrung.wabkurz EQ vhp.htparam.fchar NO-LOCK NO-ERROR. 
    IF AVAILABLE vhp.waehrung THEN
    DO:
        ASSIGN exchg-rate = vhp.waehrung.ankauf / vhp.waehrung.einheit.
    END.
    ELSE
    DO:
        ASSIGN exchg-rate = 1.
    END.
END.
 
FIND FIRST vhp.h-bill WHERE vhp.h-bill.departement EQ dept 
    AND vhp.h-bill.tischnr EQ tischnr 
    AND vhp.h-bill.flag EQ 0 
    NO-LOCK NO-ERROR.
IF AVAILABLE vhp.h-bill THEN
DO:
    FOR EACH vhp.h-bill-line WHERE vhp.h-bill-line.rechnr EQ vhp.h-bill.rechnr 
        AND vhp.h-bill-line.departement EQ dept NO-LOCK BY vhp.h-bill-line.bezeich:
        CREATE t-h-bill-line.
        BUFFER-COPY h-bill-line TO t-h-bill-line.
    END.
END.

FIND FIRST vhp.htparam WHERE paramnr = 134 NO-LOCK NO-ERROR.
IF AVAILABLE vhp.htparam THEN
DO:
    ASSIGN p-134 = vhp.htparam.flogical.
END.

FIND FIRST vhp.htparam WHERE paramnr = 135 NO-LOCK NO-ERROR. 
IF AVAILABLE vhp.htparam THEN
DO:
    ASSIGN p-135 = vhp.htparam.flogical.
END.

FIND FIRST vhp.htparam WHERE paramnr = 479 NO-LOCK NO-ERROR.
IF AVAILABLE vhp.htparam THEN
DO:
    ASSIGN p-479 = vhp.htparam.flogical. 
END.
/*Alder - Serverless - Issue 519 - End*/
