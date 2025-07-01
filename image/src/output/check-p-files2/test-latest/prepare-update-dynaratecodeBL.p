
DEF TEMP-TABLE t-zimkateg
    FIELD kurzbez LIKE zimkateg.kurzbez.
DEF TEMP-TABLE queasy2
    FIELD char1 LIKE queasy.char1.

DEF OUTPUT PARAMETER ci-date    AS DATE NO-UNDO.
DEF OUTPUT PARAMETER i-param439 AS INT NO-UNDO.
DEF OUTPUT PARAMETER TABLE FOR queasy2.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.

RUN htpdate.p(87, OUTPUT ci-date).
RUN htpint.p(439, OUTPUT i-param439).

FOR EACH queasy WHERE queasy.KEY = 2 AND queasy.logi2 NO-LOCK 
    BY queasy.char1:

    CREATE queasy2.
    ASSIGN
    queasy2.char1 = queasy.char1.
END.

FOR EACH zimkateg NO-LOCK:
    CREATE t-zimkateg.
    ASSIGN t-zimkateg.kurzbez = zimkateg.kurzbez.
END.
