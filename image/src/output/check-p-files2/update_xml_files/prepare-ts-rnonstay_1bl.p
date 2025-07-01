
DEF TEMP-TABLE q1-list
    FIELD rechnr      LIKE vhp.bill.rechnr
    FIELD resnr       LIKE vhp.bill.resnr
    FIELD bill-name   LIKE bill.name
    FIELD name        LIKE guest.name
    FIELD gastnr      LIKE guest.gastnr
    FIELD anredefirma LIKE vhp.guest.anredefirma
    FIELD vorname1    LIKE vhp.guest.vorname1
    FIELD saldo       LIKE vhp.bill.saldo
    FIELD rec-id      AS INT
    FIELD guest-rec-id AS INT
    FIELD barcode     LIKE vhp.bill.vesrdepot2 /*FD Oct 11, 2022 => Search By Barcode NS Cashless*/
    .

DEF INPUT  PARAMETER dept        AS INT.
DEF OUTPUT PARAMETER overCL-flag AS LOGICAL.
DEF OUTPUT PARAMETER mc-flag     AS LOGICAL.
DEF OUTPUT PARAMETER cashless-lic AS LOGICAL. /*FD Oct 11, 2022 => Search By Barcode NS Cashless*/
DEF OUTPUT PARAMETER min-saldo AS DECIMAL. /*FD Oct 11, 2022 => Validation if amount > min saldo*/
DEF OUTPUT PARAMETER TABLE FOR q1-list.

FIND FIRST htparam WHERE htparam.paramnr = 247 NO-LOCK. 
overCL-flag = htparam.flogical. 

/*FDL - Cashless Payment Feature*/
FIND FIRST htparam WHERE htparam.paramnr = 586 NO-LOCK. 
min-saldo = htparam.fdecimal. 
FIND FIRST htparam WHERE htparam.paramnr EQ 1022
    AND htparam.bezeich NE "not used"
    AND htparam.flogical NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN cashless-lic = YES. 

FIND FIRST htparam WHERE htparam.paramnr = 168 NO-LOCK. 
IF htparam.bezeich NE "Not Used" THEN mc-flag = htparam.flogical. 
IF NOT mc-flag THEN 
DO:    
    FOR EACH vhp.bill WHERE vhp.bill.flag = 0 AND vhp.bill.resnr EQ 0 
        AND vhp.bill.zinr = "" AND vhp.bill.reslinnr = 1 AND billtyp = dept NO-LOCK, 
        FIRST vhp.guest WHERE vhp.guest.gastnr = vhp.bill.gastnr 
        NO-LOCK BY vhp.bill.name BY vhp.bill.resnr:

        CREATE q1-list.
        ASSIGN
            q1-list.rechnr      = vhp.bill.rechnr
            q1-list.resnr       = vhp.bill.resnr
            q1-list.bill-name   = bill.name
            q1-list.name        = guest.name
            q1-list.gastnr      = guest.gastnr
            q1-list.anredefirma = vhp.guest.anredefirma
            q1-list.vorname1    = vhp.guest.vorname1
            q1-list.saldo       = vhp.bill.saldo
            q1-list.rec-id      = RECID(bill)
            q1-list.guest-rec-id = RECID(guest)
            q1-list.barcode     = bill.vesrdepot2
            .

        IF bill.vesrdepot NE "" THEN
            q1-list.vorname1 = q1-list.vorname1 + ";" + bill.vesrdepot.

    END.
    /*MTASSIGN cardNr:READ-ONLY = YES.*/
END.
