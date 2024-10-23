
DEFINE VARIABLE pvILanguage AS INTEGER NO-UNDO.
DEFINE VARIABLE lvCAREA AS CHARACTER INITIAL "ts-restinv".
{supertransbl.i}

DEF TEMP-TABLE t-h-bill LIKE h-bill
    FIELD rec-id AS INT.

DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER tischnr AS INT.
DEF INPUT PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-h-bill.

IF case-type = 1 THEN
FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tischnr
    AND vhp.h-bill.departement = curr-dept
    AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR.
ELSE IF case-type = 2 THEN
FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tischnr
    AND vhp.h-bill.departement = curr-dept NO-LOCK NO-ERROR.

ELSE IF case-type = 3 THEN DO:
    FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tischnr
    AND vhp.h-bill.departement = curr-dept
    AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR.
    IF AVAILABLE vhp.h-bill THEN DO:
        EMPTY TEMP-TABLE t-h-bill.
        CREATE t-h-bill.
        ASSIGN
            t-h-bill.bilname = translateExtended("Table already has an active bill",lvCAREA,"").
        RETURN.
    END.
    ELSE RETURN.
END.

ELSE IF case-type = 4 THEN DO:
    FIND FIRST vhp.h-bill WHERE vhp.h-bill.tischnr = tischnr
    AND vhp.h-bill.departement = curr-dept
    AND vhp.h-bill.flag = 0 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE vhp.h-bill THEN DO:
        EMPTY TEMP-TABLE t-h-bill.
        CREATE t-h-bill.
        ASSIGN
            t-h-bill.bilname = translateExtended("There is no bill active on this table" + CHR(10) + 
                                                 "Or bill on this table has been closed" + CHR(10) +  
                                                 "Payment not possible",lvCAREA,"").
        RETURN.
    END.
    ELSE RETURN.
END.

IF AVAILABLE h-bill THEN 
DO:
    CREATE t-h-bill.
    BUFFER-COPY h-bill TO t-h-bill.
    ASSIGN t-h-bill.rec-id = RECID(h-bill).
END.

