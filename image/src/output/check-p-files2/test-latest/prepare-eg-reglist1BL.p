
DEFINE TEMP-TABLE q-133
    FIELD number1   LIKE queasy.number1
    FIELD char1     LIKE queasy.char1.

DEFINE TEMP-TABLE tproperty
    FIELD prop-nr       AS INTEGER
    FIELD prop-nm       AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object Item"
    FIELD prop-selected AS LOGICAL INITIAL NO
    FIELD pcateg-nr     AS INTEGER
    FIELD pcateg        AS CHAR
    FIELD pmain-nr      AS INTEGER
    FIELD pmain         AS CHAR     FORMAT "x(20)"
    FIELD ploc-nr       AS INTEGER
    FIELD ploc          AS CHAR     FORMAT "x(20)"
    FIELD pzinr         AS CHAR     FORMAT "x(20)" .

DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr       AS INTEGER 
    FIELD Main-nm       AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD main-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tcategory
    FIELD categ-nr          AS INTEGER
    FIELD categ-nm          AS CHAR     FORMAT "x(20)"
    FIELD categ-selected    AS LOGICAL  INITIAL NO.

DEFINE TEMP-TABLE tsource
    FIELD source-nr         AS INTEGER
    FIELD source-nm         AS CHAR     FORMAT "x(20)"
    FIELD source-selected   AS LOGICAL  INITIAL NO.

DEFINE TEMP-TABLE troom
    FIELD room-nm       AS CHAR FORMAT "x(15)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr        AS INTEGER 
    FIELD loc-nm        AS CHAR FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected  AS LOGICAL INITIAL NO
    FIELD loc-guest     AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tStatus
    FIELD stat-nr       AS INTEGER
    FIELD stat-nm       AS CHAR FORMAT "x(15)"
    FIELD stat-selected AS LOGICAL INITIAL NO.

DEFINE TEMP-TABLE tpic
    FIELD pic-nr        AS INTEGER
    FIELD pic-nm        AS CHAR FORMAT "x(20)" COLUMN-LABEL "Pic"
    FIELD pic-selected  AS LOGICAL INITIAL NO
    FIELD pic-Dept      AS INTEGER.

DEFINE TEMP-TABLE dept-link 
    FIELD dept-nr AS INTEGER
    FIELD dept-nm AS CHAR.

DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER store-number AS INT.
DEF OUTPUT PARAMETER GroupID AS INT.
DEF OUTPUT PARAMETER EngID AS INT.
DEF OUTPUT PARAMETER p-992 AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR q-133.
DEF OUTPUT PARAMETER TABLE FOR tpic.
DEF OUTPUT PARAMETER TABLE FOR dept-link.

DEF BUFFER qbuff FOR queasy.

RUN htplogic.p(992, OUTPUT p-992).
FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN ci-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 1061 NO-LOCK NO-ERROR.
IF AVAILABLE htparam AND htparam.finteger NE 0 THEN
DO:
  FIND FIRST l-lager WHERE l-lager.lager-nr = htparam.finteger NO-LOCK NO-ERROR.
  IF AVAILABLE l-lager THEN store-number = l-lager.lager-nr.
END.

RUN Define-Group.
RUN Define-engineering.
RUN create-Related-dept.

RUN create-pic. /*for status: 0= no 1 = yes */
RUN create-status.
RUN create-room.

RUN create-queasy.
RUN create-location.
RUN create-main.
RUN create-property.

PROCEDURE define-group :
    FIND FIRST bediener WHERE bediener.userinit = user-init NO-LOCK NO-ERROR.
    IF AVAILABLE bediener THEN ASSIGN GroupID = bediener.user-group.
END PROCEDURE.

PROCEDURE define-engineering :
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
            VIEW-AS ALERT-BOX INFORMATION. */
    END.

END PROCEDURE.

PROCEDURE create-related-dept :
DEF VAR i AS INTEGER NO-UNDO.
    DEF VAR c AS INTEGER NO-UNDO.
    /*DEF BUFFER qbuff FOR queasy.FT serverless*/
        
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
END PROCEDURE.
 
PROCEDURE create-pic :
/*DEF BUFFER qbuff FOR eg-staff.
DEF BUFFER qbuff1 FOR bediener. FT serverless*/

    FOR EACH tpic:
        DELETE tpic.
    END.

    CREATE tpic.
    ASSIGN  tpic.pic-nr = 0
            tpic.pic-nm = ""
            tpic.pic-selected = NO.

    FOR EACH eg-staff WHERE eg-staff.usergroup = EngID AND eg-staff.activeflag = YES NO-LOCK BY eg-staff.nr:
        CREATE tpic.
        ASSIGN 
            tpic.pic-nr = eg-staff.nr
            tpic.pic-nm = eg-staff.NAME
            tpic.pic-dept = eg-staff.usergroup
            tpic.pic-selected = NO.
    END.

END PROCEDURE.

PROCEDURE create-status :
    FOR EACH tStatus:
        DELETE tStatus. 
    END.

    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 1
           tStatus.stat-nm = "New"
           tstatus.stat-selected = NO.

    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 2
           tStatus.stat-nm = "Processed"
           tstatus.stat-selected = NO.

    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 3
           tStatus.stat-nm = "Done"
           tstatus.stat-selected = NO.

    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 4
           tStatus.stat-nm = "Postponed"
           tstatus.stat-selected = NO.
    
    CREATE tStatus.
    ASSIGN tStatus.stat-nr = 5
           tStatus.stat-nm = "Closed"
           tstatus.stat-selected = NO.

END PROCEDURE.

PROCEDURE create-room:
    DEF VAR i AS INTEGER NO-UNDO.
    /*DEF BUFFER qbuff FOR zimmer.
    DEF BUFFER qbuff1 FOR tlocation.FT serverless*/

    FOR EACH troom:
        DELETE troom.
    END.    

    FIND FIRST tlocation WHERE tlocation.loc-selected = YES 
        AND tlocation.loc-guest = YES NO-LOCK NO-ERROR.
    IF AVAILABLE tlocation THEN
    DO:
        FOR EACH zimmer NO-LOCK:
            CREATE troom.
            ASSIGN 
                troom.room-nm = zimmer.zinr
                troom.room-SELECTED = NO.
        END.
    END.
END.

PROCEDURE create-source :
    CREATE tsource.
    ASSIGN 
        tsource.source-nr = qbuff.number1
        tsource.source-nm = qbuff.char1
        tsource.source-selected = NO.
END PROCEDURE.

PROCEDURE create-category :
    CREATE tcategory.
    ASSIGN 
        tcategory.categ-nr = qbuff.number1
        tcategory.categ-nm = qbuff.char1
        tcategory.categ-selected = NO.
END PROCEDURE.

PROCEDURE create-maintask :
    CREATE tMaintask.
    ASSIGN 
        tMaintask.Main-nr = qbuff.number1
        tMaintask.Main-nm = qbuff.char1
        tmaintask.main-selected = NO.


    CREATE q-133.
    ASSIGN
        q-133.number1   = qbuff.number1
        q-133.char1     = qbuff.char1.
END PROCEDURE.

PROCEDURE create-Location:
    /*DEF BUFFER qbuff FOR eg-location.*/

    FOR EACH tLocation:
        DELETE tLocation.
    END.

    CREATE tlocation.
    ASSIGN tlocation.loc-nr = 0
        tlocation.loc-nm = "Undefine"
        tlocation.loc-guest = NO.

    FOR EACH eg-location NO-LOCK:
        IF eg-location.guestflag = YES THEN
        DO:
            CREATE tLocation.
            ASSIGN tLocation.loc-nr = eg-location.nr
                tLocation.loc-nm = eg-location.bezeich
                tlocation.loc-selected = YES
                tlocation.loc-guest = YES.
        END.
        ELSE
        DO:
            CREATE tLocation.
            ASSIGN tLocation.loc-nr = eg-location.nr
                tLocation.loc-nm = eg-location.bezeich
                tlocation.loc-selected = YES
                tlocation.loc-guest = NO.
        END.
    END.

    /*FOR EACH qbuff :
        ASSIGN qbuff.logi1 = NO.
    END.  FT serverless  */
END.

PROCEDURE create-main :
  DEF VAR    do-it  AS LOGICAL INITIAL NO.

  FIND FIRST eg-property WHERE eg-property.nr = 0 
      AND eg-property.bezeich = "" NO-LOCK NO-ERROR.
  IF NOT AVAILABLE eg-property THEN
  DO:
     CREATE eg-property.
     ASSIGN
         eg-property.nr      = 0
         eg-property.bezeich = "".
  END.
  ELSE 
  DO:
      do-it = YES.
  END.

  FIND FIRST eg-location WHERE eg-location.nr = 0 
      AND eg-location.bezeich = "" NO-LOCK NO-ERROR.
  IF NOT AVAILABLE eg-location THEN
  DO:
      CREATE eg-location.
      ASSIGN
          eg-location.nr      = 0
          eg-location.bezeich = ""
          eg-location.logi1   = NO.
  END.
  ELSE 
  DO:
      do-it = YES.
  END.

  IF do-it THEN
  DO:
      RETURN.
  END.    
END PROCEDURE.


PROCEDURE create-property:
    /*DEF BUFFER qbuff FOR eg-property. FT serverless*/
    DEF BUFFER comlocat FOR tlocation.
    DEF BUFFER comMain FOR tmaintask.
    DEF BUFFER comRoom FOR troom.
    DEF BUFFER ques FOR queasy.

    FOR EACH tproperty:
        DELETE tproperty.
    END.

    CREATE tproperty.
    ASSIGN tproperty.prop-nr = 0
           tproperty.prop-nm = "Undefine".


    FOR EACH comlocat WHERE comlocat.loc-selected NO-LOCK,
        FIRST eg-property WHERE eg-property.location = comlocat.loc-nr 
        USE-INDEX mtloczin_x NO-LOCK BY eg-property.location:
        IF comlocat.loc-guest = YES THEN
        DO:
            FIND FIRST commain WHERE commain.main-nr = eg-property.maintask 
                AND commain.main-selected NO-LOCK NO-ERROR.
            IF AVAILABLE commain THEN
            DO:
                FIND FIRST comroom WHERE comroom.room-nm = eg-property.zinr 
                  AND comroom.room-selected NO-LOCK NO-ERROR.
                IF AVAILABLE comroom THEN
                DO:
                    CREATE tproperty.

                    ASSIGN tproperty.prop-nr = eg-property.nr
                           tproperty.prop-nm = eg-property.bezeich + "(" + trim(string(eg-property.nr , ">>>>>>9")) + ")"
                           tproperty.pzinr   = eg-property.zinr 
                           tproperty.pmain-nr = eg-property.maintask
                           tproperty.ploc-nr  = eg-property.location.

                    FIND FIRST queasy WHERE queasy.KEY = 133 AND queasy.number1 = eg-property.maintask NO-LOCK NO-ERROR.
                    IF AVAILABLE queasy THEN
                    DO:
                        ASSIGN tproperty.pmain = queasy.char1
                               tproperty.pcateg-nr = queasy.number2.

                        FIND FIRST ques WHERE ques.KEY = 132 AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
                        IF AVAILABLE ques THEN
                        DO:
                            ASSIGN tproperty.pcateg = ques.char1.
                        END.
                    END.
                    ELSE
                    DO:
                        ASSIGN tproperty.pmain = ""
                               tproperty.pcateg-nr = 0
                               tproperty.pcateg = "".
                    END.

                    FIND FIRST eg-location WHERE eg-location.nr = eg-property.location NO-LOCK NO-ERROR.
                    IF AVAILABLE eg-location THEN
                        ASSIGN tproperty.ploc = eg-location.bezeich.
                    ELSE
                        ASSIGN  tproperty.ploc = "".
                END.
            END.
        END.
        ELSE
        DO:
            FIND FIRST commain WHERE commain.main-nr = eg-property.maintask 
                AND commain.main-selected NO-LOCK NO-ERROR.
            IF AVAILABLE commain THEN
            DO:
                CREATE tproperty.
                ASSIGN tproperty.prop-nr = eg-property.nr
                       tproperty.prop-nm = eg-property.bezeich + "(" + trim(string(eg-property.nr , ">>>>>>9")) + ")"
                       tproperty.pzinr   = eg-property.zinr 
                       tproperty.pmain-nr = eg-property.maintask
                       tproperty.ploc-nr  = eg-property.location.

                FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = eg-property.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    ASSIGN tproperty.pmain = queasy.char1
                           tproperty.pcateg-nr = queasy.number2.

                    FIND FIRST ques WHERE ques.KEY = 132 AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
                    IF AVAILABLE ques THEN
                    DO:
                        ASSIGN tproperty.pcateg = ques.char1.
                    END.
                END.
                ELSE
                DO:
                    ASSIGN tproperty.pmain = ""
                           tproperty.pcateg-nr = 0
                           tproperty.pcateg = "".
                END.

                FIND FIRST eg-location WHERE eg-location.nr = eg-property.location NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN ASSIGN tproperty.ploc = eg-location.bezeich.
                ELSE ASSIGN tproperty.ploc = "".
            END.
        END.
    END.


    /*MT
    FOR EACH comlocat WHERE comlocat.loc-selected NO-LOCK:
        IF comlocat.loc-guest = YES THEN
        DO:
            FOR EACH qbuff WHERE qbuff.location = comlocat.loc-nr USE-INDEX mtloczin_x NO-LOCK,
                FIRST commain WHERE commain.main-nr = qbuff.maintask AND commain.main-selected NO-LOCK,
                FIRST comroom WHERE comroom.room-nm = qbuff.zinr AND comroom.room-selected NO-LOCK:
                CREATE tproperty.
    
                ASSIGN tproperty.prop-nr = qbuff.nr
                       tproperty.prop-nm = qbuff.bezeich + "(" + trim(string(qbuff.nr , ">>>>>>9")) + ")"
                       tproperty.pzinr   = qbuff.zinr 
                       tproperty.pmain-nr = qbuff.maintask
                       tproperty.ploc-nr  = qbuff.location.
            
                FIND FIRST queasy WHERE queasy.KEY = 133 AND queasy.number1 = qbuff.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    ASSIGN tproperty.pmain = queasy.char1
                           tproperty.pcateg-nr = queasy.number2.

                    FIND FIRST ques WHERE ques.KEY = 132 AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
                    IF AVAILABLE ques THEN
                    DO:
                        ASSIGN tproperty.pcateg = ques.char1.
                    END.
                END.
                ELSE
                DO:
                    ASSIGN tproperty.pmain = ""
                           tproperty.pcateg-nr = 0
                           tproperty.pcateg = "".
                END.
            
                FIND FIRST eg-location WHERE eg-location.nr = qbuff.location NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN
                    ASSIGN tproperty.ploc = eg-location.bezeich.
                ELSE
                    ASSIGN  tproperty.ploc = "".
            END.
        END.
        ELSE
        DO:
            FOR EACH qbuff WHERE qbuff.location = comlocat.loc-nr USE-INDEX location_ix NO-LOCK,
                FIRST commain WHERE commain.main-nr = qbuff.maintask AND commain.main-selected NO-LOCK:

                CREATE tproperty.
                ASSIGN tproperty.prop-nr = qbuff.nr
                       tproperty.prop-nm = qbuff.bezeich + "(" + trim(string(qbuff.nr , ">>>>>>9")) + ")"
                       tproperty.pzinr   = qbuff.zinr 
                       tproperty.pmain-nr = qbuff.maintask
                       tproperty.ploc-nr  = qbuff.location.
            
                FIND FIRST queasy WHERE queasy.KEY= 133 AND queasy.number1 = qbuff.maintask NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    ASSIGN tproperty.pmain = queasy.char1
                           tproperty.pcateg-nr = queasy.number2.

                    FIND FIRST ques WHERE ques.KEY = 132 AND ques.number1 = queasy.number2 NO-LOCK NO-ERROR.
                    IF AVAILABLE ques THEN
                    DO:
                        ASSIGN tproperty.pcateg = ques.char1.
                    END.
                END.
                ELSE
                DO:
                    ASSIGN tproperty.pmain = ""
                           tproperty.pcateg-nr = 0
                           tproperty.pcateg = "".
                END.
            
                FIND FIRST eg-location WHERE eg-location.nr = qbuff.location NO-LOCK NO-ERROR.
                IF AVAILABLE eg-location THEN ASSIGN tproperty.ploc = eg-location.bezeich.
                ELSE ASSIGN tproperty.ploc = "".
            END.
        END.
    END.
    */
END.

PROCEDURE create-queasy:
    FOR EACH tsource:
        DELETE tsource.
    END.  
    FOR EACH tcategory:
        DELETE tcategory.
    END.
    FOR EACH tMaintask:
        DELETE tMaintask.
    END.

    FOR EACH qbuff WHERE qbuff.KEY = 130 OR qbuff.KEY = 132 OR qbuff.KEY = 133
        NO-LOCK:
        IF qbuff.KEY = 130 THEN RUN create-source.
        IF qbuff.KEY = 132 THEN RUN create-category.
        IF qbuff.KEY = 133 THEN RUN create-maintask.
    END.

END.
