
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER hostnr AS INT.
DEF INPUT PARAMETER pax    AS INT.
DEF INPUT PARAMETER gname  AS CHAR.
DEF INPUT PARAMETER hoga-resnr AS INT.
DEF INPUT PARAMETER hoga-reslinnr AS INT.
DEF INPUT PARAMETER segment-code AS INT. /*FDL April 15, 2024 => Ticket 65C56B | CD4BDA*/

IF gname EQ ? THEN gname = "".

FIND FIRST h-bill WHERE RECID(h-bill) = rec-id EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    /* FDL Comment
    vhp.h-bill.resnr = hoga-resnr.
    vhp.h-bill.reslinnr = hoga-reslinnr. /*MT*/
    */
    IF h-bill.bilname NE gname THEN
    DO:
        h-bill.resnr = hoga-resnr.
        h-bill.reslinnr = hoga-reslinnr.
    END.
    h-bill.service[2] = hostnr. 
    h-bill.belegung = pax. 
    h-bill.bilname = gname.

    IF h-bill.segmentcode NE segment-code THEN
    DO:
        h-bill.segmentcode = segment-code.
    END.
    ELSE IF h-bill.bilname EQ "" OR h-bill.bilname EQ ? THEN
    DO:
        h-bill.segmentcode = 0.
    END.

    FIND CURRENT h-bill NO-LOCK.    
    RELEASE h-bill.
END.

