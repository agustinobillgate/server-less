
DEF INPUT PARAMETER r-sub-task AS CHAR.
DEFINE INPUT PARAMETER inTime AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER inDate AS DATE NO-UNDO.

DEF OUTPUT PARAMETER r-ex-finishdate AS DATE.
DEF OUTPUT PARAMETER r-ex-finishtime AS INT.
DEF OUTPUT PARAMETER estfin-str AS CHAR.

DEF VAR adTime AS INTEGER NO-UNDO INITIAL 0.
DEF VAR sTime AS INTEGER NO-UNDO.
DEF VAR d AS DATE NO-UNDO.
DEF VAR e AS DATE NO-UNDO.
DEF VAR f AS INTEGER NO-UNDO.

FIND FIRST eg-subtask WHERE eg-subtask.sub-code = r-sub-task NO-LOCK NO-ERROR.
IF AVAILABLE eg-subtask THEN
DO:
    FIND FIRST eg-duration WHERE eg-duration.duration-nr = eg-subtask.dur-nr NO-LOCK NO-ERROR.
    IF AVAILABLE eg-duration THEN
    DO:
        IF eg-duration.hour NE 0 THEN
        DO:
            adtime = eg-duration.hour * 3600.
        END.

        IF eg-duration.minute NE 0 THEN
        DO:
            adtime = adtime + (eg-duration.minute * 60).
        END.

        sTime = inTime /*request1.process-time*/ + adtime.

        IF stime < 86399 THEN
        DO:
            d = inDate /*request1.process-date*/.
            f = stime.
        END.
        ELSE
        DO:
            d = inDate /*request1.process-date*/.
            DO WHILE (stime > 86399) :
                d = d + 1 .
                stime = stime - 86399.
                f = stime.
            END.
            
        END.

        IF eg-duration.DAY NE 0 THEN
        DO:
            e = d + eg-duration.DAY.
        END.
        ELSE
        DO:
            e = d.
        END.

            ASSIGN r-ex-finishdate = e
                   r-ex-finishtime = f
                   estfin-str = replace( STRING(f, "HH:MM") , ":", "") .
            /*MTDISP request1.ex-finishdate estfin-str WITH FRAME frame1.*/

    END.
END.
