DEF TEMP-TABLE coa-list
    FIELD old-fibu AS CHAR FORMAT "x(12)"
    FIELD new-fibu AS CHAR FORMAT "x(12)"
    FIELD bezeich AS CHAR FORMAT "x(48)"  /**/
    FIELD coaStat  AS INTEGER INITIAL -1
    FIELD old-main AS INTEGER
    FIELD new-main AS INTEGER
    FIELD bezeichM AS CHAR
    FIELD old-dept AS INTEGER
    FIELD new-dept AS INTEGER
    FIELD bezeichD AS CHAR
    FIELD catno    AS INTEGER
    FIELD acct     AS INTEGER
    FIELD old-acct AS INTEGER
    INDEX coa-ix old-fibu
.
DEF TEMP-TABLE temp-gl-journal LIKE gl-journal.
DEF TEMP-TABLE temp-gl-jourhis LIKE gl-jourhis.


DEFINE INPUT PARAMETER TABLE FOR coa-list.

MESSAGE "start mapping COA 2" VIEW-AS ALERT-BOX.

RUN update-gl.

PROCEDURE update-gl:
    DEF BUFFER gljourBuff2 FOR gl-journal.
    DEF BUFFER jouhisBuff2 FOR gl-jourhis.
    DEF BUFFER acchisBuff2 FOR gl-accthis.
    DEF BUFFER acctBuff    FOR gl-acct.
    DEF BUFFER acctBuff2   FOR gl-acct.

    DEF VAR i AS INT.

    FOR EACH temp-gl-journal:
        DELETE temp-gl-journal.
    END.

    DO TRANSACTION:
        FIND FIRST gl-journal NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-journal:
          FIND FIRST coa-list WHERE coa-list.old-fibu = gl-journal.fibukonto NO-LOCK NO-ERROR.
            IF AVAILABLE coa-list THEN
            DO:
                CREATE temp-gl-journal.
                BUFFER-COPY gl-journal TO temp-gl-journal.
                FIND CURRENT gl-journal EXCLUSIVE-LOCK.
                DELETE gl-journal.
                RELEASE gl-journal.
          END.
          FIND NEXT gl-journal NO-LOCK NO-ERROR.
        END.
    END.

    MESSAGE "done delete gl-journal" VIEW-AS ALERT-BOX.

    FIND FIRST temp-gl-journal NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE temp-gl-journal:
        FIND FIRST coa-list WHERE coa-list.old-fibu = temp-gl-journal.fibukonto
            AND coa-list.new-fibu NE ? NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN
        DO TRANSACTION:
            ASSIGN temp-gl-journal.fibukonto = coa-list.new-fibu.
            CREATE gl-journal.
            BUFFER-COPY temp-gl-journal TO gl-journal.
        END.
        FIND NEXT temp-gl-journal NO-LOCK NO-ERROR.
    END.
    

    MESSAGE "done update gl-journal" VIEW-AS ALERT-BOX.
    
    FOR EACH temp-gl-jourhis:
        DELETE temp-gl-jourhis.
    END.

    DO TRANSACTION:
        FIND FIRST gl-jourhis NO-LOCK NO-ERROR.
        DO WHILE AVAILABLE gl-jourhis:
          FIND FIRST coa-list WHERE coa-list.old-fibu = gl-jourhis.fibukonto NO-LOCK NO-ERROR.
          IF AVAILABLE coa-list THEN
          DO:
            CREATE temp-gl-jourhis.
            BUFFER-COPY gl-jourhis TO temp-gl-jourhis.
            FIND CURRENT gl-jourhis EXCLUSIVE-LOCK.
            DELETE gl-jourhis.
            RELEASE gl-jourhis.
          END.
          FIND NEXT gl-jourhis NO-LOCK NO-ERROR.
        END.
    END.

    MESSAGE "done delete gl-jourhis" VIEW-AS ALERT-BOX.
    
    FIND FIRST temp-gl-jourhis NO-LOCK NO-ERROR.
    DO WHILE AVAILABLE temp-gl-jourhis:
        FIND FIRST coa-list WHERE coa-list.old-fibu = temp-gl-jourhis.fibukonto
            AND coa-list.new-fibu NE ? NO-LOCK NO-ERROR.
        IF AVAILABLE coa-list THEN
        DO TRANSACTION:
            ASSIGN temp-gl-jourhis.fibukonto = coa-list.new-fibu.
            CREATE gl-jourhis.
            BUFFER-COPY temp-gl-jourhis TO gl-jourhis.
        END.
        FIND NEXT temp-gl-jourhis NO-LOCK NO-ERROR.
    END.

    MESSAGE "done update gl-jourhis" VIEW-AS ALERT-BOX.
END.
