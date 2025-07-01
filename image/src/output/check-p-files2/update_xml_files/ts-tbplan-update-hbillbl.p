
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER hostnr AS INT.
DEF INPUT PARAMETER pax    AS INT.
DEF INPUT PARAMETER gname  AS CHAR.
DEF INPUT PARAMETER hoga-resnr AS INT.
DEF INPUT PARAMETER hoga-reslinnr AS INT.

IF gname EQ ? THEN gname = "".

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id /*EXCLUSIVE-LOCK*/ NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    /* FDL Comment
    vhp.h-bill.resnr = hoga-resnr.
    vhp.h-bill.reslinnr = hoga-reslinnr. /*MT*/
    */
    FIND CURRENT h-bill EXCLUSIVE-LOCK. /*FDL CHG to Find Current Stack Trace Zin Canggu*/
    IF h-bill.bilname NE gname THEN
    DO:
        h-bill.resnr = hoga-resnr.
        h-bill.reslinnr = hoga-reslinnr.
    END.
    h-bill.service[2] = hostnr. 
    h-bill.belegung = pax. 
    h-bill.bilname = gname.

    FIND CURRENT h-bill NO-LOCK.   
    RELEASE h-bill.
END.

