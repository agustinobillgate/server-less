DEFINE TEMP-TABLE maintain
    FIELD maintainnr    AS INTEGER      FORMAT ">>>>>>9"
    FIELD workdate      AS DATE
    FIELD estworkdate   AS DATE
    FIELD donedate      AS DATE
    FIELD TYPE          AS INTEGER
    FIELD maintask      AS INTEGER
    FIELD location      AS INTEGER
    FIELD zinr          AS CHAR
    FIELD propertynr    AS INTEGER
    FIELD pic           AS INTEGER
    INDEX alldatum  estworkdate workdate.

DEF INPUT PARAMETER t-maintainnr AS INT.
DEF INPUT PARAMETER user-init AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR maintain.

FIND FIRST eg-maintain WHERE eg-maintain.maintainnr = t-maintainnr NO-ERROR.
IF AVAILABLE eg-maintain THEN
ASSIGN eg-maintain.delete-flag = YES
       eg-maintain.cancel-date = TODAY
       eg-maintain.cancel-time = TIME
       eg-maintain.cancel-by = user-init.


RUN create-maintain.

PROCEDURE create-maintain:
    DEF BUFFER qbuff FOR eg-maintain.
    
    FOR EACH maintain:
        DELETE maintain.
    END.

    FOR EACH qbuff WHERE qbuff.delete-flag = NO NO-LOCK:

        IF qbuff.propertynr NE 0 THEN
        DO:
            FIND FIRST eg-property WHERE eg-property.nr = qbuff.propertynr NO-LOCK NO-ERROR.
            IF AVAILABLE eg-property THEN
            DO:
                
                CREATE maintain.
                ASSIGN  maintain.maintainnr    = qbuff.maintainnr
                        maintain.workdate      = qbuff.workdate
                        maintain.estworkdate   = qbuff.estworkdate
                        maintain.donedate      = qbuff.donedate
                        maintain.TYPE          = qbuff.TYPE
                        maintain.maintask      = eg-property.maintask 
                        maintain.location      = qbuff.location 
                        maintain.zinr          = qbuff.zinr
                        maintain.propertynr    = qbuff.propertynr
                        maintain.pic           = qbuff.pic. 
            END.
            ELSE
            DO:

            END.
  
        END.
        ELSE
        DO:
            CREATE maintain.
            ASSIGN  maintain.maintainnr    = qbuff.maintainnr
                        maintain.workdate      = qbuff.workdate
                        maintain.estworkdate   = qbuff.estworkdate
                        maintain.donedate      = qbuff.donedate
                        maintain.TYPE          = qbuff.TYPE
                        maintain.maintask      = eg-property.maintask /*tproperty.pmain-nr*/
                        maintain.location      = qbuff.location /*tproperty.ploc-nr*/
                        maintain.zinr          = qbuff.zinr
                        maintain.propertynr    = qbuff.propertynr
                        maintain.pic           = qbuff.pic. 
        END.
    END.
END.

