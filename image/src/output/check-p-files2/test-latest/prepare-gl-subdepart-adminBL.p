.
DEF TEMP-TABLE t-queasy      LIKE queasy.
DEF TEMP-TABLE t-gl-depart   LIKE gl-department.

DEF OUTPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER TABLE FOR t-gl-depart.

FOR EACH queasy WHERE queasy.KEY = 155 NO-LOCK:
    CREATE t-queasy.
    BUFFER-COPY queasy TO t-queasy.
END.

FOR EACH gl-department NO-LOCK:
    CREATE t-gl-depart.
    BUFFER-COPY gl-department TO t-gl-depart.
END.
