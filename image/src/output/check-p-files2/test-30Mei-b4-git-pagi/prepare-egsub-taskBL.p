DEFINE TEMP-TABLE t-eg-subtask LIKE eg-subtask
    FIELD rec-id AS INT. 

DEFINE TEMP-TABLE department
    FIELD dept-nr AS INTEGER
    FIELD department AS CHAR FORMAT "x(24)" COLUMN-LABEL "Department".

DEFINE TEMP-TABLE maintask
    FIELD main-nr  AS INTEGER 
    FIELD maintask AS CHAR FORMAT "x(36)" COLUMN-LABEL "Object"
    FIELD main-grp AS CHAR. /*FD For Web*/

DEFINE TEMP-TABLE sduration
    FIELD duration-nr  AS INTEGER /*Alder - Serverless - Issue 700*/ /*Duration-nr -> duration-nr*/
    FIELD time-str AS CHAR FORMAT "X(100)" COLUMN-LABEL "Duration".

DEFINE TEMP-TABLE dept-link 
    FIELD dept-nr AS INTEGER
    FIELD dept-nm AS CHAR.

DEFINE TEMP-TABLE queasy-133 LIKE queasy.

DEFINE TEMP-TABLE t-eg-request LIKE eg-request.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER TABLE FOR department.
DEF OUTPUT PARAMETER TABLE FOR maintask.
DEF OUTPUT PARAMETER TABLE FOR sduration.
DEF OUTPUT PARAMETER TABLE FOR dept-link.
DEF OUTPUT PARAMETER TABLE FOR t-eg-subtask.
DEF OUTPUT PARAMETER TABLE FOR t-eg-request.
DEF OUTPUT PARAMETER TABLE FOR queasy-133.

RUN define-group.
RUN define-engineering.

RUN create-Related-dept.
RUN create-duration.

RUN create-main.
RUN create-dept.

FOR EACH eg-request:
    CREATE t-eg-request.
    BUFFER-COPY eg-request TO t-eg-request.
END.

FOR EACH eg-subtask:
    CREATE t-eg-subtask.
    BUFFER-COPY eg-subtask TO t-eg-subtask.
    ASSIGN t-eg-subtask.rec-id = RECID(eg-subtask).
END.

FOR EACH queasy WHERE queasy.KEY = 133:
    CREATE queasy-133.
    BUFFER-COPY queasy TO queasy-133.
END.

PROCEDURE Define-engineering:
/*
    FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.CHAR3 = "Engineering" NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN EngID = queasy.number1.
    END.
*/
    FIND FIRST htparam WHERE htparam.paramnr = 1200 AND htparam.feldtyp = 1 NO-LOCK NO-ERROR.
    IF AVAILABLE htparam THEN
    DO:
        ASSIGN EngID = htparam.finteger.
    END.
    ELSE
    DO:
        /*MTHIDE MESSAGE NO-PAUSE.
        MESSAGE translateExtended("Group No for Engineering Modul not yet defined.", lvCAREA, "":U) 
            SKIP 
            translateExtended( "Please contact your next VHP Support for further Information.", lvCAREA, "":U) 
            VIEW-AS ALERT-BOX INFORMATION. */
    END.
END.

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.

PROCEDURE create-Related-dept:
    DEF VAR i AS INTEGER NO-UNDO.
    DEF VAR c AS INTEGER NO-UNDO.
    DEF BUFFER qbuff FOR queasy.
        
    FOR EACH dept-link:
        DELETE dept-link.
    END.

    FIND FIRST queasy WHERE queasy.KEY = 19 AND queasy.number1 = EngId
        NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN 
    DO: 
        CREATE dept-link.
        ASSIGN

            dept-link.dept-nr   = EngId
            dept-link.dept-nm   = queasy.char3
            .

        DO i = 1 TO NUM-ENTRIES(queasy.char2, ";"):
            c = INTEGER(ENTRY(i, queasy.char2, ";")).
            FIND FIRST qbuff WHERE qbuff.KEY = 19 AND qbuff.number1 = 
                INTEGER(ENTRY(i, queasy.char2, ";")) NO-LOCK NO-ERROR.
            IF AVAILABLE qbuff THEN
            DO:
                CREATE dept-link.
                ASSIGN 
                    dept-link.dept-nr   = c
                    dept-link.dept-nm   = qbuff.char3
                    .
            END.                
        END.
    END.
END.

PROCEDURE create-duration:
    DEF BUFFER qbuff FOR eg-Duration.
    DEF VAR str AS CHAR NO-UNDO.

    FOR EACH sduration:
        DELETE sduration.
    END.

    CREATE sduration.
    ASSIGN sduration.duration-nr  = 0                       /*Alder - Serverless - Issue 700*/ /*Duration-nr -> duration-nr*/
               sduration.time-str = "User Defineable".

    FOR EACH qbuff NO-LOCK BY qbuff.duration-nr:            /*Alder - Serverless - Issue 700*/ /*Duration-nr -> duration-nr*/
        IF qbuff.days = 0 THEN                              /*Alder - Serverless - Issue 700*/ /*day -> days*/
        DO:
            str = "".
        END.
        ELSE 
        DO:
            str = STRING(qbuff.days).                       /*Alder - Serverless - Issue 700*/ /*day -> days*/
            IF qbuff.days > 1 THEN str = str + " days ".    /*Alder - Serverless - Issue 700*/ /*day -> days*/
            ELSE str = str + " day ".
        END.

        IF qbuff.hour = 0 THEN
        DO:
            str = str.
        END.
        ELSE 
        DO:
            str = str + string(qbuff.hour).
            IF qbuff.hour > 1 THEN str = str + " hrs ".
            ELSE str = str + " hr ".
        END.

        IF qbuff.minute = 0 THEN
        DO:
            str = str .
        END.
        ELSE 
        DO:
            str = str + string(qbuff.minute) + " min ".
        END.

        CREATE sduration.
        ASSIGN sduration.duration-nr  = qbuff.duration-nr   /*Alder - Serverless - Issue 700*/ /*Duration-nr -> duration-nr*/
               sduration.time-str = str.
    END.
END.

PROCEDURE create-main:
    DEF BUFFER qbuff FOR queasy.

    FOR EACH maintask:
        DELETE maintask.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 133 NO-LOCK:
        CREATE maintask.
        ASSIGN maintask.main-nr = qbuff.number1
            maintask.maintask = qbuff.char1.

        FIND FIRST queasy WHERE queasy.KEY EQ 132 AND queasy.number1 EQ qbuff.number2 NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN maintask.main-grp = queasy.char1.
    END.                                    
END.

PROCEDURE create-dept:
    DEF BUFFER qbuff FOR queasy.

    FOR EACH department:
        DELETE department.
    END.

    CREATE department.
    ASSIGN department.dept-nr   = 0
           department.department = "All Related Department".

    FOR EACH qbuff WHERE qbuff.KEY = 19 NO-LOCK:
        CREATE department.
        ASSIGN department.dept-nr = qbuff.number1
            department.department = qbuff.char3.
    END.                                    
END.

