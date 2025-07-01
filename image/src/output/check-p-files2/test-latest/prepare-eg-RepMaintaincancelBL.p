
DEFINE TEMP-TABLE tpic
    FIELD pic-nr AS INTEGER
    FIELD pic-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Name"
    FIELD pic-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tFrequency
    FIELD freq-nr AS INTEGER
    FIELD freq-nm AS CHAR FORMAT "x(24)".

DEFINE TEMP-TABLE troom
    FIELD room-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm  AS CHAR       FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected AS LOGICAL INITIAL NO
    FIELD loc-guest AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr  AS INTEGER 
    FIELD Main-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD main-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tcategory
    FIELD categ-nr AS INTEGER
    FIELD categ-nm AS CHAR  FORMAT "x(24)"
    FIELD categ-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tStatus
    FIELD stat-nr AS INTEGER
    FIELD stat-nm AS CHAR           FORMAT "x(24)"
    FIELD stat-selected AS LOGICAL INITIAL NO.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER TABLE FOR tStatus.
DEF OUTPUT PARAMETER TABLE FOR tcategory.
DEF OUTPUT PARAMETER TABLE FOR tMaintask.
DEF OUTPUT PARAMETER TABLE FOR tLocation.
DEF OUTPUT PARAMETER TABLE FOR troom.
DEF OUTPUT PARAMETER TABLE FOR tFrequency.
DEF OUTPUT PARAMETER TABLE FOR tpic.

RUN define-group.
RUN DEFINE-engineering.
RUN create-frequency.
RUN create-status.
RUN create-pic.
RUN create-category.
RUN create-location.

FOR EACH tcategory :
    ASSIGN tcategory.categ-selected = YES.
END.

RUN create-maintask.

FOR EACH tlocation :
    ASSIGN tlocation.loc-selected = YES.
END.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 


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
        ASSIGN EngID = 0.
        /*MTHIDE MESSAGE NO-PAUSE.
        MESSAGE translateExtended("Group No for Engineering Modul not yet defined.", lvCAREA, "":U) 
            SKIP 
            translateExtended( "Please contact your next VHP Support for further Information.", lvCAREA, "":U) 
            VIEW-AS ALERT-BOX INFORMATION. 
        */
    END.
END.

PROCEDURE Define-Group:
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN
    DO:
        ASSIGN GroupID = bediener.user-group.
    END.
END.


PROCEDURE create-frequency:
    FOR EACH tFrequency:
        DELETE tFrequency.
    END.

    CREATE tFrequency.
    ASSIGN tFrequency.freq-nr = 1
           tFrequency.freq-nm = "Weekly".

    CREATE tFrequency.
    ASSIGN tFrequency.freq-nr = 2
           tFrequency.freq-nm = "Monthly".

    CREATE tFrequency.
    ASSIGN tFrequency.freq-nr = 3
           tFrequency.freq-nm = "Quarter".

    CREATE tFrequency.
    ASSIGN tFrequency.freq-nr = 4
           tFrequency.freq-nm = "Half Yearly".

    CREATE tFrequency.
    ASSIGN tFrequency.freq-nr = 5
           tFrequency.freq-nm = "Year".
END.


PROCEDURE create-status:
    FOR EACH tStatus:
        DELETE tStatus. 
    END.
    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 1
           tStatus.stat-nm = "Scheduled"
           tstatus.stat-selected = NO.
    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 2
           tStatus.stat-nm = "Processed"
           tstatus.stat-selected = NO.
    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 3
           tStatus.stat-nm = "Done"
           tstatus.stat-selected = NO.
END.

PROCEDURE create-pic:
    DEF BUFFER qbuff FOR eg-staff.
    FOR EACH tpic:
        DELETE tpic.
    END.
    
    CREATE tpic.
    ASSIGN  tpic.pic-nr = 0
            tpic.pic-nm = ""
            tpic.pic-selected = NO.

    FOR EACH qbuff WHERE qbuff.usergroup = EngID AND qbuff.activeflag = YES NO-LOCK BY qbuff.nr:
        CREATE tpic.
        ASSIGN 
            tpic.pic-nr = qbuff.nr
            tpic.pic-nm = qbuff.NAME
            tpic.pic-selected = NO.
    END.
END.


PROCEDURE create-category:
    DEF BUFFER qbuff FOR queasy.
    FOR EACH tcategory:
        DELETE tcategory.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 132 NO-LOCK:
        CREATE tcategory.
        ASSIGN tcategory.categ-nr = qbuff.number1
            tcategory.categ-nm = qbuff.char1
            tcategory.categ-selected = NO.
    END.
END.


PROCEDURE create-Location:
    DEF BUFFER qbuff FOR eg-location.

    FOR EACH tLocation:
        DELETE tLocation.
    END.

    CREATE tlocation.
    ASSIGN tlocation.loc-nr = 0
        tlocation.loc-nm = "Undefine"
        tlocation.loc-guest = YES.

    FOR EACH qbuff NO-LOCK:
        IF qbuff.guestflag = YES THEN
        DO:
            CREATE tLocation.
            ASSIGN tLocation.loc-nr = qbuff.nr
                tLocation.loc-nm = qbuff.bezeich
                tlocation.loc-selected = YES
                tlocation.loc-guest = YES.
        END.
        ELSE
        DO:
            CREATE tLocation.
            ASSIGN tLocation.loc-nr = qbuff.nr
                tLocation.loc-nm = qbuff.bezeich
                tlocation.loc-selected = YES
                tlocation.loc-guest = NO.
        END.
    END.                                     
END.


PROCEDURE create-maintask:
    DEF BUFFER qbuff FOR queasy.
    DEF BUFFER comCategory FOR tcategory.

    FOR EACH tMaintask:
        DELETE tMaintask.
    END.

    FOR EACH comCategory WHERE comCategory.categ-SELECTED NO-LOCK:
        FOR EACH qbuff WHERE qbuff.KEY = 133 AND qbuff.number2 = comcategory.categ-nr NO-LOCK:
            CREATE tMaintask.
            ASSIGN tMaintask.Main-nr = qbuff.number1
                tMaintask.Main-nm = qbuff.char1
                tmaintask.main-selected = YES.
        END.
    END.                                    
END.

