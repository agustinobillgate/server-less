DEF TEMP-TABLE t-gl-jouhdr          LIKE gl-jouhdr.
DEF TEMP-TABLE t-gl-journal         LIKE gl-journal.

DEF INPUT PARAMETER lic-nr          AS CHAR NO-UNDO INIT "".
DEF INPUT PARAMETER TABLE FOR t-gl-jouhdr.
DEF INPUT PARAMETER TABLE FOR t-gl-journal.

FOR EACH t-gl-jouhdr NO-LOCK BY t-gl-jouhdr.jnr:
  DO TRANSACTION:
    FIND FIRST gl-htljournal WHERE gl-htljournal.htl-jnr = t-gl-jouhdr.jnr 
        AND gl-htljournal.htl-license = lic-nr NO-LOCK NO-ERROR.
    IF AVAILABLE gl-htljournal THEN
    DO: /* delete previous journal due to re-closing */
        FOR EACH gl-jouhdr WHERE gl-jouhdr.jnr = gl-htljournal.jnr:
            DELETE gl-jouhdr.
        END.
        FOR EACH gl-journal WHERE gl-journal.jnr = gl-htljournal.jnr:
            DELETE gl-journal.
        END.
    END.
    ELSE
    DO:
      FIND FIRST counters WHERE counters.counter-no = 25 EXCLUSIVE-LOCK NO-ERROR. 
      IF NOT AVAILABLE counters THEN 
      DO: 
        CREATE counters.
        ASSIGN
          counters.counter-no  = 25 
          counters.counter-bez = "G/L Transaction Journal"
        . 
      END. 
      ASSIGN counters.counter = counters.counter + 1. 
      FIND CURRENT counter NO-LOCK. 
      CREATE gl-htljournal.
      ASSIGN
        gl-htljournal.htl-jnr     = t-gl-jouhdr.jnr
        gl-htljournal.jnr         = counters.counter
        gl-htljournal.htl-license = lic-nr
        gl-htljournal.datum       = t-gl-jouhdr.datum
      .
      RELEASE counters.
    END.
    CREATE gl-jouhdr. 
    BUFFER-COPY t-gl-jouhdr EXCEPT t-gl-jouhdr.jnr TO gl-jouhdr.
    ASSIGN
        gl-jouhdr.jnr        = gl-htljournal.jnr
        gl-jouhdr.jtype      = gl-jouhdr.jtype + 10
        gl-jouhdr.activeflag = 0
    .
    FOR EACH t-gl-journal WHERE t-gl-journal.jnr = t-gl-jouhdr.jnr NO-LOCK:
        CREATE gl-journal.
        BUFFER-COPY t-gl-journal EXCEPT t-gl-journal.jnr TO gl-journal.
        ASSIGN 
            gl-journal.jnr        = gl-htljournal.jnr
            gl-journal.activeflag = 0
        .
        DELETE t-gl-journal.
        FIND CURRENT gl-journal NO-LOCK.
        RELEASE gl-journal.
    END.
    FIND CURRENT gl-htljournal NO-LOCK.
    RELEASE gl-htljournal.
    FIND CURRENT gl-jouhdr NO-LOCK.
    RELEASE gl-jouhdr.
  END.
END.
