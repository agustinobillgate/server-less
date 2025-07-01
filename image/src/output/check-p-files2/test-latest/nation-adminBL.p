
DEF TEMP-TABLE t-nation1 LIKE nation.

DEF TEMP-TABLE t-nation  LIKE nation
    FIELD marksegm AS CHAR
    FIELD rec-id AS INT.

DEF INPUT PARAMETER int1 AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-nation.
DEF OUTPUT PARAMETER TABLE FOR t-nation1.
 
DEF VAR a AS INT.

FOR EACH nation WHERE nation.natcode = int1 NO-LOCK BY nation.kurzbez:
    CREATE t-nation.
    BUFFER-COPY nation TO t-nation.
    ASSIGN t-nation.rec-id = RECID(nation).

    a = INTEGER(ENTRY(2, nation.bezeich, ";")) NO-ERROR.
    FIND FIRST prmarket WHERE prmarket.nr = a NO-LOCK NO-ERROR.
    IF AVAILABLE prmarket THEN ASSIGN t-nation.marksegm = prmarket.bezeich.
END. 

FOR EACH nation NO-LOCK:
    CREATE t-nation1.
    BUFFER-COPY nation TO t-nation1.
END.
