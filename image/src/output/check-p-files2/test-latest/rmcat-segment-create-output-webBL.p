DEFINE TEMP-TABLE rmcat-segm-list
    FIELD flag          AS INTEGER
    FIELD segment       AS CHARACTER FORMAT "x(40)"
    FIELD room          AS CHARACTER FORMAT "x(8)"
    FIELD pax           AS CHARACTER FORMAT "x(8)"
    FIELD logis         AS CHARACTER FORMAT "x(19)"
    FIELD proz          AS CHARACTER FORMAT "x(6)"
    FIELD avrgrate      AS CHARACTER FORMAT "x(19)"
    FIELD m-room        AS CHARACTER FORMAT "x(8)"
    FIELD m-pax         AS CHARACTER FORMAT "x(8)"
    FIELD m-logis       AS CHARACTER FORMAT "x(19)"
    FIELD m-proz        AS CHARACTER FORMAT "x(6)"
    FIELD m-avrgrate    AS CHARACTER FORMAT "x(19)"
    FIELD y-room        AS CHARACTER FORMAT "x(8)"
    FIELD y-pax         AS CHARACTER FORMAT "x(8)"
    FIELD y-logis       AS CHARACTER FORMAT "x(19)"
    FIELD y-proz        AS CHARACTER FORMAT "x(6)"
    FIELD y-avrgrate    AS CHARACTER FORMAT "x(19)"
    FIELD rmnite1       AS CHARACTER FORMAT "x(8)"
    FIELD rmrev1        AS CHARACTER FORMAT "x(19)"
    FIELD rmnite        AS CHARACTER FORMAT "x(8)"
    FIELD rmrev         AS CHARACTER FORMAT "x(19)"
    FIELD rmcat         AS CHARACTER FORMAT "x(3)"
    FIELD segm-code     AS INTEGER
.

DEFINE OUTPUT PARAMETER doneFlag AS LOGICAL NO-UNDO INITIAL NO.
DEFINE OUTPUT PARAMETER TABLE FOR rmcat-segm-list.

DEFINE VARIABLE counter   AS INTEGER NO-UNDO INITIAL 0.

DEFINE BUFFER bqueasy FOR queasy.
DEFINE BUFFER pqueasy FOR queasy.
DEFINE BUFFER tqueasy FOR queasy.

FOR EACH queasy WHERE queasy.KEY EQ 280 AND queasy.char1 EQ "Guest Segment By Room Type" NO-LOCK BY queasy.number1:
    counter = counter + 1.
    IF counter GT 1000 THEN LEAVE.

    CREATE rmcat-segm-list.
    ASSIGN
        rmcat-segm-list.flag        = INT(ENTRY(1, queasy.char2 ,"|"))
        rmcat-segm-list.segment     = ENTRY(2, queasy.char2 ,"|")
        rmcat-segm-list.room        = ENTRY(3, queasy.char2 ,"|")
        rmcat-segm-list.pax         = ENTRY(4, queasy.char2 ,"|")
        rmcat-segm-list.logis       = ENTRY(5, queasy.char2 ,"|")
        rmcat-segm-list.proz        = ENTRY(6, queasy.char2 ,"|")
        rmcat-segm-list.avrgrate    = ENTRY(7, queasy.char2 ,"|")
        rmcat-segm-list.m-room      = ENTRY(8, queasy.char2 ,"|")
        rmcat-segm-list.m-pax       = ENTRY(9, queasy.char2 ,"|")
        rmcat-segm-list.m-logis     = ENTRY(10, queasy.char2 ,"|")
        rmcat-segm-list.m-proz      = ENTRY(11, queasy.char2 ,"|")
        rmcat-segm-list.m-avrgrate  = ENTRY(12, queasy.char2 ,"|")
        rmcat-segm-list.y-room      = ENTRY(13, queasy.char2 ,"|")
        rmcat-segm-list.y-pax       = ENTRY(14, queasy.char2 ,"|")
        rmcat-segm-list.y-logis     = ENTRY(15, queasy.char2 ,"|")
        rmcat-segm-list.y-proz      = ENTRY(16, queasy.char2 ,"|")
        rmcat-segm-list.y-avrgrate  = ENTRY(17, queasy.char2 ,"|")
        rmcat-segm-list.rmnite1     = ENTRY(18, queasy.char2 ,"|")
        rmcat-segm-list.rmrev1      = ENTRY(19, queasy.char2 ,"|")
        rmcat-segm-list.rmnite      = ENTRY(20, queasy.char2 ,"|")
        rmcat-segm-list.rmrev       = ENTRY(21, queasy.char2 ,"|")
        rmcat-segm-list.rmcat       = ENTRY(22, queasy.char2 ,"|")
        rmcat-segm-list.segm-code   = INT(ENTRY(23, queasy.char2 ,"|"))
        .

    FIND FIRST bqueasy WHERE RECID(bqueasy) EQ RECID(queasy) EXCLUSIVE-LOCK.
    DELETE bqueasy.
    RELEASE bqueasy.
END.

FIND FIRST pqueasy WHERE pqueasy.KEY EQ 280 AND pqueasy.char1 EQ "Guest Segment By Room Type"
    AND pqueasy.char3 EQ "PROCESS" NO-LOCK NO-ERROR.
IF AVAILABLE pqueasy THEN ASSIGN doneFlag = NO.
ELSE DO:
    FIND FIRST tqueasy WHERE tqueasy.KEY EQ 285 
        AND tqueasy.char1 EQ "Guest Segment By Room Type" AND tqueasy.number1 EQ 1 NO-LOCK NO-ERROR.
    IF AVAILABLE tqueasy THEN ASSIGN doneFlag = NO.
    ELSE ASSIGN doneFlag = YES.
END.
