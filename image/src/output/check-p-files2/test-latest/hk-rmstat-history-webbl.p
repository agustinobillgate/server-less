
DEFINE TEMP-TABLE input-report
    FIELD usrID          AS CHARACTER
    FIELD room           AS CHARACTER
    FIELD from-date      AS DATE
    FIELD to-date        AS DATE
    FIELD pvILanguages   AS INTEGER
.

DEF BUFFER ubuff FOR bediener.

DEFINE TEMP-TABLE b1-list
    FIELD datum     LIKE res-history.datum
    FIELD zinr      LIKE zimmer.zinr
    FIELD from-stat LIKE res-history.aenderung
    FIELD to-stat   LIKE res-history.aenderung
    FIELD remark    LIKE res-history.aenderung
    FIELD username  LIKE ubuff.username
    FIELD zeit      LIKE res-history.zeit
.

DEF INPUT PARAMETER TABLE FOR input-report.
DEF OUTPUT PARAMETER TABLE FOR b1-list.


DEF VAR pvILanguage    AS INTEGER NO-UNDO.

FIND FIRST input-report WHERE input-report.from-date NE ? AND input-report.to-date NE ? NO-LOCK NO-ERROR.
IF AVAILABLE input-report THEN 
DO:
    pvILanguage = input-report.pvILanguages.

    {supertransBL.i} 
    DEF VAR lvCAREA AS CHAR INITIAL "hk-statadmin".
    DEFINE VARIABLE stat-list AS CHAR EXTENT 10 FORMAT "x(23)" NO-UNDO. 
    stat-list[1] = translateExtended ("Vacant Clean Checked", lvCAREA,""). 
    stat-list[2] = translateExtended ("Vacant Clean Unchecked", lvCAREA,""). 
    stat-list[3] = translateExtended ("Vacant Dirty", lvCAREA,""). 
    stat-list[4] = translateExtended ("Expected Departure", lvCAREA,""). 
    stat-list[5] = translateExtended ("Occupied Dirty", lvCAREA,""). 
    stat-list[6] = translateExtended ("Occupied Cleaned", lvCAREA,""). 
    stat-list[7] = translateExtended ("Out-of-Order", lvCAREA,""). 
    stat-list[8] = translateExtended ("Off-Market", lvCAREA,""). 
    stat-list[9] = translateExtended ("Do not Disturb", lvCAREA,""). 
    stat-list[10] = translateExtended ("Out-of-Service",lvCAREA,"").

    RUN disp-it.
END.

PROCEDURE disp-it:
    IF input-report.usrID NE "" AND input-report.room NE "" THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit = TRIM(ENTRY(1, usrID, "-"))
            NO-LOCK.
        FOR EACH res-history WHERE res-history.datum GE from-date
            AND res-history.datum LE to-date 
            AND res-history.action EQ "HouseKeeping"
            AND NUM-ENTRIES(res-history.aenderung,"|") GT 3
            AND res-history.nr EQ bediener.nr
            AND ENTRY(2,res-history.aenderung," ") EQ input-report.room NO-LOCK,
            FIRST ubuff WHERE ubuff.nr EQ res-history.nr NO-LOCK
            BY res-history.datum BY res-history.zeit:
            RUN assign-it.
        END.
        RETURN.
    END.
    
    ELSE IF usrID NE "" AND input-report.room EQ "" THEN
    DO:
        FIND FIRST bediener WHERE bediener.userinit = TRIM(ENTRY(1, usrID, "-"))
            NO-LOCK.
        FOR EACH res-history WHERE res-history.datum GE from-date
            AND res-history.datum LE to-date 
            AND res-history.action EQ "HouseKeeping"
            AND NUM-ENTRIES(res-history.aenderung,"|") GT 3
            AND res-history.nr = bediener.nr NO-LOCK,
            FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK
            BY res-history.datum BY res-history.zeit:
            RUN assign-it.
        END.
        RETURN.
    END.

    ELSE IF usrID EQ "" AND input-report.room NE "" THEN
    DO:
        FOR EACH res-history WHERE res-history.datum GE from-date
            AND res-history.datum LE to-date 
            AND res-history.action EQ "HouseKeeping"
            AND NUM-ENTRIES(res-history.aenderung,"|") GT 3
            AND ENTRY(2,res-history.aenderung," ") EQ input-report.room NO-LOCK,
            FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK
            BY res-history.datum BY res-history.zeit:
            RUN assign-it.
        END.
        RETURN.
    END.

    ELSE 
    DO:
        FOR EACH res-history WHERE res-history.datum GE from-date
            AND res-history.datum LE to-date 
            AND res-history.action EQ "HouseKeeping"
            AND NUM-ENTRIES(res-history.aenderung,"|") GT 3 NO-LOCK,
            FIRST ubuff WHERE ubuff.nr = res-history.nr NO-LOCK
            BY res-history.datum BY res-history.zeit:
            RUN assign-it.
        END.
        RETURN.
    END.
END.

PROCEDURE assign-it:
    CREATE b1-list.
    ASSIGN
        b1-list.datum     = res-history.datum
        b1-list.zinr      = ENTRY(2,res-history.aenderung," ")
        b1-list.from-stat = stat-list[INT(ENTRY(2,res-history.aenderung,"|")) + 1]
        b1-list.to-stat   = stat-list[INT(ENTRY(3,res-history.aenderung,"|")) + 1]
        b1-list.remark    = SUBSTRING(ENTRY(4,res-history.aenderung,"|Reason:"),8)
        b1-list.zeit      = res-history.zeit.
    IF AVAILABLE ubuff THEN b1-list.username  = ubuff.username.
END.




