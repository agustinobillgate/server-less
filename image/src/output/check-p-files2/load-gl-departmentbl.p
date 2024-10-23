DEF TEMP-TABLE t-gl-department LIKE gl-department.

DEF OUTPUT PARAMETER TABLE  FOR t-gl-department.
FOR EACH gl-department NO-LOCK:
    CREATE t-gl-department.
    BUFFER-COPY gl-department TO t-gl-department.
END.
