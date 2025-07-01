DEFINE TEMP-TABLE res-grplist
    FIELD res-month     AS CHARACTER
    FIELD res-no        AS INTEGER
    FIELD resline-no    AS INTEGER
    FIELD group-name    AS CHARACTER
    FIELD arrival-date  AS CHARACTER
    FIELD depart-date   AS CHARACTER
    FIELD night         AS INTEGER
    FIELD pax           AS INTEGER
    FIELD room-stay     AS INTEGER
    FIELD room-night    AS INTEGER
    FIELD ta-company    AS CHARACTER
    FIELD purpose-stay  AS CHARACTER
    FIELD nationality   AS CHARACTER
.

DEFINE TEMP-TABLE payload-list
    FIELD sorttype      AS INTEGER
    FIELD from-month    AS CHARACTER.

DEFINE TEMP-TABLE output-list
    FIELD month-report  AS INTEGER
    FIELD year-report   AS INTEGER
    .
/* 
DEFINE INPUT PARAMETER sorttype     AS INTEGER.
DEFINE INPUT PARAMETER from-month   AS CHARACTER.
*/

DEFINE INPUT PARAMETER TABLE FOR payload-list.
DEFINE OUTPUT PARAMETER TABLE FOR res-grplist.
DEFINE OUTPUT PARAMETER TABLE FOR output-list.

DEFINE VARIABLE grp-name    AS CHARACTER.
DEFINE VARIABLE room        AS CHARACTER.
DEFINE VARIABLE str         AS CHARACTER.
DEFINE VARIABLE purpose-no  AS INTEGER.
DEFINE VARIABLE mm          AS INTEGER.
DEFINE VARIABLE yy          AS INTEGER.
DEFINE VARIABLE i           AS INTEGER.
DEFINE VARIABLE res-no      AS INTEGER.
DEFINE VARIABLE night-stay  AS INTEGER.
DEFINE VARIABLE tot-pax     AS INTEGER.
DEFINE VARIABLE tot-room    AS INTEGER.
DEFINE VARIABLE tot-rmnight AS INTEGER.
DEFINE VARIABLE ci-date     AS DATE.
DEFINE VARIABLE month-int   AS INTEGER. 
DEFINE VARIABLE year-int    AS INTEGER. 


FIND FIRST payload-list NO-ERROR.
CREATE output-list.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
  ci-date = htparam.fdate.

month-int = INT(MONTH(ci-date)).
year-int = INT(YEAR(ci-date)).

ASSIGN
    output-list.month-report = month-int
    output-list.year-report = year-int.

mm = INTEGER(SUBSTR(payload-list.from-month,1,2)).
yy = INTEGER(SUBSTR(payload-list.from-month,3,4)).


FOR EACH res-grplist:
    DELETE res-grplist.
END.

IF sorttype EQ 1 THEN
DO:
    FOR EACH genstat WHERE MONTH(genstat.datum) EQ mm 
        AND YEAR(genstat.datum) EQ yy
        AND genstat.res-char[3] NE "" NO-LOCK,
        FIRST reservation WHERE reservation.resnr EQ genstat.resnr
        NO-LOCK BY genstat.resnr BY genstat.res-char[3]:
        IF grp-name NE genstat.res-char[3] THEN
        DO:
            CREATE res-grplist.
            ASSIGN
                res-grplist.group-name      = genstat.res-char[3]
                res-grplist.arrival-date    = STRING(genstat.res-date[1])
                res-grplist.depart-date     = STRING(genstat.res-date[2])
                res-grplist.night           = genstat.res-date[2] - genstat.res-date[1]
                res-grplist.pax             = genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2            
                res-grplist.ta-company      = reservation.NAME  
                res-grplist.room-stay       = 1
            .        
                
            night-stay = genstat.res-date[2] - genstat.res-date[1].
    
            FIND FIRST res-line WHERE res-line.resnr EQ genstat.resnr
                AND res-line.zimmer-wunsch MATCHES "*SEGM_PUR*" NO-LOCK NO-ERROR.
            IF AVAILABLE res-line THEN
            DO:
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";"):
                    str = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(str,1,8)  = "SEGM_PUR" THEN
                    DO:
                        purpose-no = INT(SUBSTR(str,9)).
                        FIND FIRST queasy WHERE queasy.KEY EQ 143 
                            AND queasy.number1 EQ purpose-no NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN
                        DO:
                            res-grplist.purpose-stay = queasy.char3.
                        END.                        
                    END.
                END.
            END.
    
            FIND FIRST guest WHERE guest.gastnr EQ genstat.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
                FIND FIRST nation WHERE nation.kurzbez EQ guest.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    res-grplist.nationality = nation.bezeich.
                END.
            END.
            
            room = genstat.zinr.
            grp-name = genstat.res-char[3].
        END.
    
        ASSIGN
            res-grplist.pax = res-grplist.pax + genstat.erwachs + genstat.gratis + genstat.kind1 + genstat.kind2
            .
    
        IF room NE genstat.zinr THEN
        DO:
            res-grplist.room-stay = res-grplist.room-stay + 1.
            room = genstat.zinr.
        END.    
    END.
END.
ELSE
DO:
    FOR EACH res-line WHERE MONTH(res-line.ankunft) EQ mm 
        AND YEAR(res-line.ankunft) EQ yy
        AND MONTH(res-line.abreise) EQ mm 
        AND YEAR(res-line.abreise) EQ yy NO-LOCK,
        FIRST reservation WHERE reservation.resnr EQ res-line.resnr
        AND reservation.groupname NE ""
        NO-LOCK BY reservation.resnr BY reservation.groupname:

        IF grp-name NE reservation.groupname THEN
        DO:
            CREATE res-grplist.
            ASSIGN
                res-grplist.group-name      = reservation.groupname
                res-grplist.arrival-date    = STRING(res-line.ankunft)
                res-grplist.depart-date     = STRING(res-line.abreise)
                res-grplist.night           = res-line.abreise - res-line.ankunft
                res-grplist.pax             = res-line.erwachs + res-line.gratis + res-line.kind1 + res-line.kind2            
                res-grplist.ta-company      = reservation.NAME  
                res-grplist.room-stay       = 1
            .       

            IF res-line.zimmer-wunsch MATCHES "*SEGM_PUR*" THEN
            DO:
                DO i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";"):
                    str = ENTRY(i, res-line.zimmer-wunsch, ";").
                    IF SUBSTR(str,1,8)  = "SEGM_PUR" THEN
                    DO:
                        purpose-no = INT(SUBSTR(str,9)).
                        FIND FIRST queasy WHERE queasy.KEY EQ 143 
                            AND queasy.number1 EQ purpose-no NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN
                        DO:
                            res-grplist.purpose-stay = queasy.char3.
                        END.                        
                    END.
                END.
            END.

            FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnr NO-LOCK NO-ERROR.
            IF AVAILABLE guest THEN
            DO:
                FIND FIRST nation WHERE nation.kurzbez EQ guest.land NO-LOCK NO-ERROR.
                IF AVAILABLE nation THEN
                DO:
                    res-grplist.nationality = nation.bezeich.
                END.
            END.

            room = res-line.zinr.
            grp-name = reservation.groupname.
        END.

        ASSIGN
            res-grplist.pax = res-grplist.pax + res-line.erwachs + res-line.gratis + res-line.kind1 + res-line.kind2
            .

        IF room NE res-line.zinr THEN
        DO:
            res-grplist.room-stay = res-grplist.room-stay + 1.
            room = res-line.zinr.
        END.  
    END.
END.
    
tot-pax     = 0.
tot-room    = 0.
tot-rmnight = 0.

FOR EACH res-grplist:
    res-grplist.room-night = res-grplist.night * res-grplist.room-stay.
    tot-pax     = tot-pax + res-grplist.pax.
    tot-room    = tot-room + res-grplist.room-stay.
    tot-rmnight = tot-rmnight + res-grplist.room-night.
END.

FIND FIRST res-grplist NO-LOCK NO-ERROR.
IF AVAILABLE res-grplist THEN
DO:
    CREATE res-grplist.
    ASSIGN
        res-grplist.group-name  = "T O T A L"
        res-grplist.pax         = tot-pax
        res-grplist.room-stay   = tot-room   
        res-grplist.room-night  = tot-rmnight
    .
END.
