
DEF INPUT PARAMETER rechnr      AS INT.
DEF INPUT PARAMETER bil-rec-id  AS INT.
DEF INPUT PARAMETER dept        AS INT.

FIND FIRST h-bill WHERE RECID(h-bill) = bil-rec-id
    AND h-bill.departement = dept NO-LOCK.

FIND FIRST vhp.bill WHERE RECID(vhp.bill) = rechnr NO-LOCK NO-ERROR.
IF AVAILABLE vhp.bill THEN
DO:
    FIND CURRENT vhp.h-bill EXCLUSIVE-LOCK NO-WAIT NO-ERROR.
    IF AVAILABLE vhp.h-bill THEN
    DO:
        ASSIGN
            vhp.h-bill.resnr = vhp.bill.resnr
            vhp.h-bill.reslinnr = vhp.bill.reslinnr.
        FIND CURRENT vhp.h-bill NO-LOCK.
    END.
END.
