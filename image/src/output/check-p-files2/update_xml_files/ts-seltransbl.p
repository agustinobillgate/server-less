DEF OUTPUT PARAMETER rest-flag              AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER hogatex-flag           AS LOGICAL  NO-UNDO.
DEF OUTPUT PARAMETER integer-flag           AS INTEGER  NO-UNDO.

DEFINE INPUT-OUTPUT PARAMETER combo-pf-file1 AS CHAR    NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-pf-file2 AS CHAR    NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-gastnr   AS INTEGER NO-UNDO.
DEFINE INPUT-OUTPUT PARAMETER combo-ledger   AS INTEGER NO-UNDO.

FIND FIRST vhp.htparam WHERE paramnr = 975 no-lock.   /* VHP Front multi user */ 
rest-flag = (vhp.htparam.finteger EQ 1). 
 
FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 300 NO-LOCK. 
hogatex-flag = vhp.htparam.flogical. 

FIND FIRST vhp.htparam WHERE vhp.htparam.paramnr = 888 NO-LOCK. 
integer-flag = vhp.htparam.finteger.

IF combo-gastnr = ? THEN
DO:
    FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 155 NO-LOCK. 
    combo-gastnr = vhp.htparam.finteger.
    IF combo-gastnr GT 0 THEN
    DO:
        FIND FIRST guest WHERE guest.gastnr = combo-gastnr NO-LOCK NO-ERROR.
        IF NOT AVAILABLE guest THEN combo-gastnr = 0.
        ELSE ASSIGN combo-ledger = guest.zahlungsart.
        IF combo-ledger GT 0 THEN
        DO:
            FIND FIRST artikel WHERE artikel.artnr = combo-ledger
                AND artikel.departement = 0
                AND artikel.artart = 2 NO-LOCK NO-ERROR.
            IF NOT AVAILABLE artikel THEN
            ASSIGN
                combo-gastnr = 0
                combo-ledger = 0
            .
        END.
        ELSE combo-gastnr = 0.
    END.
    ELSE combo-gastnr = 0.
END.
IF combo-gastnr GT 0 THEN
DO:

    FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 339 NO-LOCK. 
    combo-pf-file1 = vhp.htparam.fchar. 
    FIND FIRST vhp.htparam WHERE vhp.htpara.paramnr = 340 NO-LOCK. 
    combo-pf-file2 = vhp.htparam.fchar. 
END.
