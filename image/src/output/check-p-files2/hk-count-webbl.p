DEFINE TEMP-TABLE depart-today
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE departed
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE arrival-today
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE arrived
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER
    FIELD arrtime AS CHARACTER
    FIELD rsv-remark AS CHARACTER
    FIELD guest-pref AS CHARACTER
    FIELD room-status AS CHARACTER
    FIELD pci     AS LOGICAL INIT NO.

DEFINE TEMP-TABLE vacant-clean-checked
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE vacant-clean-unchecked
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE occ-clean
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE occ-dirty
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE vacant-dirty
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE ex-depart
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE off-market
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE ooo-room
    FIELD room    AS CHARACTER
    FIELD rmtype  AS CHARACTER
    FIELD gname   AS CHARACTER.

DEFINE TEMP-TABLE queue-room-list LIKE queasy.

DEFINE INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER departed1   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER departed2   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER departing1  AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER departing2  AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER tot-depart1 AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER tot-depart2 AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER arrived1    AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER arrived2    AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER arriving1   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER arriving2   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER tot-arrive1 AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER tot-arrive2 AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 

DEFINE OUTPUT PARAMETER vclean     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER vuncheck   AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER oclean     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER tot-clean  AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER odirty     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER vdirty     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER atoday     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER tot-dirty  AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 

DEFINE OUTPUT PARAMETER oroom1      AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER oroom2      AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER omroom1     AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER omroom2     AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER oooroom1    AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER oooroom2    AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER compRoom1   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER compRoom2   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER houseRoom1  AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE OUTPUT PARAMETER houseRoom2  AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 


DEFINE OUTPUT PARAMETER iroom1     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER iroom2     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER eocc1      AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER eocc2      AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER proz1      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER proz2      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER proz3      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER proz4      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO. 
DEFINE OUTPUT PARAMETER proz5      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR queue-room-list.
DEFINE OUTPUT PARAMETER TABLE FOR depart-today.
DEFINE OUTPUT PARAMETER TABLE FOR departed.
DEFINE OUTPUT PARAMETER TABLE FOR arrival-today.
DEFINE OUTPUT PARAMETER TABLE FOR arrived.
DEFINE OUTPUT PARAMETER TABLE FOR vacant-clean-checked.
DEFINE OUTPUT PARAMETER TABLE FOR vacant-clean-unchecked.
DEFINE OUTPUT PARAMETER TABLE FOR occ-clean.
DEFINE OUTPUT PARAMETER TABLE FOR occ-dirty.
DEFINE OUTPUT PARAMETER TABLE FOR vacant-dirty.
DEFINE OUTPUT PARAMETER TABLE FOR ex-depart.
DEFINE OUTPUT PARAMETER TABLE FOR off-market.
DEFINE OUTPUT PARAMETER TABLE FOR ooo-room.

/*
DEFINE VAR departed1   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR departed2   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR departing1  AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR departing2  AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR tot-depart1 AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR tot-depart2 AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR arrived1    AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR arrived2    AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR arriving1   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR arriving2   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR tot-arrive1 AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR tot-arrive2 AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 

DEFINE VAR vclean     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR vuncheck   AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR oclean     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR tot-clean  AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR odirty     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR vdirty     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR atoday     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR tot-dirty  AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 

DEFINE VAR oroom1      AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR oroom2      AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR omroom1     AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR omroom2     AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR oooroom1    AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR oooroom2    AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR compRoom1   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR compRoom2   AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR houseRoom1  AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 
DEFINE VAR houseRoom2  AS INTEGER FORMAT "   >,>>9"   NO-UNDO. 


DEFINE VAR iroom1     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR iroom2     AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR eocc1      AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR eocc2      AS INTEGER FORMAT "   >,>>9"    NO-UNDO. 
DEFINE VAR proz1      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO. 
DEFINE VAR proz2      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO. 
DEFINE VAR proz3      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO. 
DEFINE VAR proz4      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO. 
DEFINE VAR proz5      AS DECIMAL FORMAT "   >>9.9"    NO-UNDO.
*/
/*************** MAIN LOGIC ***************/
{SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR.
DEFINE VARIABLE ci-date AS DATE NO-UNDO.
DEFINE VARIABLE loop-i AS INTEGER.
DEFINE VARIABLE str AS CHAR.
DEFINE VARIABLE str1 AS CHAR.
DEFINE VARIABLE loop-j AS INTEGER.
DEFINE VARIABLE loopj AS INTEGER.
DEFINE VARIABLE resbemerk AS CHAR NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
    ci-date = htparam.fdate.

RUN init-var. 
RUN read-queasybl.p (3, 162, 0, "", OUTPUT TABLE queue-room-list).
FOR EACH queue-room-list:
    IF queue-room-list.number1 = 0 THEN queue-room-list.char3 = translateExtended("On Progress",lvCAREA,"").
    ELSE IF queue-room-list.number1 = 1 THEN queue-room-list.char3 = translateExtended("DONE",lvCAREA,"").
END.

/*************** PROCEDURES ***************/
PROCEDURE init-var: 
  DEFINE VARIABLE tot-zimmer AS INTEGER               NO-UNDO. 
  DEFINE VARIABLE rm-active AS LOGICAL                NO-UNDO. 
  
    ASSIGN 
        departed1     = 0 
        departed2     = 0 
        departing1    = 0 
        departing2    = 0 
        arrived1      = 0 
        arrived2      = 0 
        arriving1     = 0 
        arriving2     = 0 
        vclean        = 0 
        vuncheck      = 0 
        oclean        = 0 
        vdirty        = 0 
        odirty        = 0 
        atoday        = 0 
        omroom1       = 0
        oroom1        = 0 
        oroom2        = 0 
        oooroom1      = 0 
        oooroom2      = 0 
        iroom1        = 0 
        iroom2        = 0 
        eocc1         = 0 
        eocc2         = 0 
        houseRoom1    = 0 
        houseRoom2    = 0 
        compRoom1     = 0 
        compRoom2     = 0 
        tot-zimmer    = 0 
        . 
 
    FOR EACH res-line NO-LOCK WHERE 
            res-line.active-flag    = 1         AND 
            res-line.resstatus      NE 12       AND 
            res-line.ankunft        LE ci-date  AND 
            res-line.abreise        = ci-date   AND
            res-line.l-zuordnung[3] = 0, 
        FIRST zimmer NO-LOCK WHERE 
            zimmer.zinr             = res-line.zinr 
        /* AND zimmer.sleeping         EQ TRUE */ : 
        IF res-line.resstatus = 6 THEN
        DO: 
            departing1 = departing1 + 1. 
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            CREATE departed.
            ASSIGN
                departed.room = res-line.zinr
                departed.rmtype = zimkateg.kurzbez
                departed.gname = guest.name + ", " + guest.vorname1 
                        + " " + guest.anrede1. 

        END.
            
        departing2 = departing2 + res-line.erwachs + res-line.gratis 
          + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
    END. 
 
    /* resident guest OF active rooms */ 
    FOR EACH res-line NO-LOCK WHERE 
            res-line.active-flag EQ 1           AND 
            res-line.resstatus      NE 12       AND 
            res-line.ankunft        LE ci-date  AND 
            res-line.abreise        GE ci-date  AND
            res-line.l-zuordnung[3] = 0, 
        FIRST zimmer NO-LOCK WHERE 
            zimmer.zinr             = res-line.zinr, 
        FIRST reservation NO-LOCK WHERE reservation.resnr = res-line.resnr
            BY res-line.resnr: 
        FIND FIRST segment WHERE 
            segment.segmentcode     = reservation.segmentcode NO-LOCK NO-ERROR.
            
        IF zimmer.sleeping AND ((res-line.abreise GT ci-date) OR 
            (res-line.ankunft = ci-date AND res-line.abreise = ci-date 
            AND res-line.zipreis GT 0)) THEN 
        DO: 
            IF res-line.resstatus = 6 THEN ASSIGN 
                oroom1    = oroom1 + 1 
                eocc1     = eocc1 + 1. 
            oroom2 = oroom2 + res-line.erwachs + res-line.gratis 
              + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
            eocc2 = eocc2 + res-line.erwachs + res-line.gratis 
              + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
        END. 
        IF res-line.ankunft = ci-date THEN DO: 
            IF res-line.resstatus = 6 THEN 
            DO:
                arrived1 = arrived1 + 1. 
                FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.
                FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                CREATE arrival-today.
                ASSIGN
                    arrival-today.room = res-line.zinr
                    arrival-today.rmtype = zimkateg.kurzbez
                    arrival-today.gname = guest.name + ", " + guest.vorname1 
                        + " " + guest.anrede1. 
            END.
            arrived2 = arrived2 + (res-line.erwachs + res-line.gratis 
                + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]). 
        END. 
        IF AVAILABLE segment THEN
        DO:
            IF segment.betriebsnr EQ 2 THEN DO: 
                IF res-line.resstatus = 6 THEN ASSIGN 
                    houseRoom1 = houseRoom1 + 1. 
                houseRoom2 = houseRoom2 + res-line.erwachs + res-line.gratis 
                    + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
            END. 
            ELSE IF segment.betriebsnr EQ 1 OR res-line.gratis GT 0 THEN DO: 
                IF res-line.resstatus = 6 THEN ASSIGN 
                    compRoom1 = compRoom1 + 1. 
                compRoom2 = compRoom2 + res-line.erwachs + res-line.gratis 
                  + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
            END. 
        END.
        IF NOT zimmer.sleeping THEN 
            iroom2 = iroom2 + res-line.erwachs + res-line.gratis 
                + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
    END. 
 
    /* today departed guests */ 
    FOR EACH res-line NO-LOCK WHERE 
            res-line.active-flag    = 2             AND 
            res-line.resstatus      = 8             AND 
            res-line.ankunft        LE ci-date      AND 
            res-line.abreise        EQ ci-date      AND
            res-line.l-zuordnung[3] EQ 0, 
        FIRST zimmer NO-LOCK WHERE 
            zimmer.zinr             = res-line.zinr 
        /*  AND zimmer.sleeping         = TRUE */ : 
        IF NOT res-line.zimmerfix THEN 
        DO:
            departed1 = departed1 + 1.
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = zimmer.zikatnr NO-LOCK NO-ERROR.
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            CREATE depart-today.
            ASSIGN
                depart-today.room = res-line.zinr
                depart-today.rmtype = zimkateg.kurzbez
                depart-today.gname = guest.name + ", " + guest.vorname1 
                        + " " + guest.anrede1. 
        END.
            
        ASSIGN 
            departed2 = departed2 + res-line.erwachs + res-line.gratis 
              + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]. 
    END. 
    ASSIGN 
        tot-depart1 = departed1 + departing1 
        tot-depart2 = departed2 + departing2. 
 
    /* arriving guests OF active rooms */ 
    FOR EACH res-line NO-LOCK WHERE 
            res-line.active-flag    = 0             AND 
            res-line.ankunft        = ci-date       AND
            res-line.l-zuordnung[3] = 0: 
        FIND FIRST zimmer WHERE zimmer.zinr EQ res-line.zinr NO-LOCK NO-ERROR. 
        rm-active = YES. 
        IF (AVAILABLE zimmer AND NOT zimmer.sleeping) THEN 
            rm-active = NO. 
 
        IF (res-line.resstatus = 1 OR res-line.resstatus = 2 OR res-line.resstatus = 5) THEN 
        DO: 
            /*html ragung*/
            resbemerk = res-line.bemerk.
            resbemerk = REPLACE(resbemerk,CHR(10),"").
            resbemerk = REPLACE(resbemerk,CHR(13),"").
            resbemerk = REPLACE(resbemerk,"~n","").
            resbemerk = REPLACE(resbemerk,"\n","").
            resbemerk = REPLACE(resbemerk,"~r","").
            resbemerk = REPLACE(resbemerk,"~r~n","").
            resbemerk = REPLACE(resbemerk,"&nbsp;"," ").
            resbemerk = REPLACE(resbemerk,"</p>","</p></p>").
            resbemerk = REPLACE(resbemerk,"</p>",CHR(13)).
            resbemerk = REPLACE(resbemerk,"<BR>",CHR(13)).
            resbemerk = REPLACE(resbemerk,CHR(10) + CHR(13),"").
        
            IF LENGTH(resbemerk) LT 3 THEN resbemerk = REPLACE(resbemerk,CHR(32),"").
            IF LENGTH(resbemerk) LT 3 THEN resbemerk = "".
            IF LENGTH(resbemerk) EQ ? THEN resbemerk = "".
            /*end agung*/

            arriving1 = arriving1 + 1 /*res-line.zimmeranz*/ .
            FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
            CREATE arrived.
            ASSIGN
                arrived.room = res-line.zinr
                arrived.gname = guest.name + ", " + guest.vorname1 
                        + " " + guest.anrede1
                arrived.arrtime = STRING(res-line.ankzeit,"HH:MM:SS")
                arrived.rsv-remark = resbemerk. 
            FIND FIRST zimkateg WHERE zimkateg.zikatnr = res-line.zikatnr NO-LOCK NO-ERROR.
            IF AVAILABLE zimkateg THEN arrived.rmtype = zimkateg.kurzbez.
            IF res-line.zimmer-wunsch MATCHES "*PCIFLAG=YES*" THEN
                arrived.pci = YES.
            IF rm-active THEN eocc1 = eocc1 + res-line.zimmeranz. 
            IF AVAILABLE zimmer THEN
            DO:
                IF zimmer.zistatus = 0 THEN 
                   arrived.room-status = "Vacant Clean Checked".
                ELSE IF zimmer.zistatus = 1 THEN 
                   arrived.room-status = "Vacant Clean Unchecked".
                ELSE IF zimmer.zistatus = 2 THEN 
                   arrived.room-status = "Vacant Dirty".
                ELSE IF zimmer.zistatus = 3 THEN 
                   arrived.room-status = "Expected Departure".
                ELSE IF zimmer.zistatus = 4 THEN 
                   arrived.room-status = "Occupied Dirty".
                ELSE IF zimmer.zistatus = 5 THEN 
                   arrived.room-status = "Occupied Cleaned".
                ELSE IF zimmer.zistatus = 6 THEN 
                   arrived.room-status = "Out Of Order".
                ELSE IF zimmer.zistatus = 7 THEN 
                   arrived.room-status = "Off Market".
                ELSE IF zimmer.zistatus = 8 THEN 
                   arrived.room-status = "Do Not Disturb".
            END.
            DO loop-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";") - 1:
                str = ENTRY(loop-i,res-line.zimmer-wunsch,";").
                IF str MATCHES "*WCI-req*" THEN
                DO:
                    str1 = ENTRY(2,str,"=").
                    DO loop-j = 1 TO NUM-ENTRIES(str1,","):
                        FIND FIRST queasy WHERE queasy.KEY = 160
                            AND queasy.number1 = INT(ENTRY(loop-j,str1,",")) NO-LOCK NO-ERROR.
                        IF AVAILABLE queasy THEN
                        DO:
                            DO loopj = 1 TO NUM-ENTRIES(queasy.char1, ";"):
                                IF ENTRY(loopj, queasy.char1, ";") MATCHES "*en*" THEN
                                DO:
                                    ASSIGN arrived.guest-pref = ENTRY(2, ENTRY(loopj, queasy.char1, ";"), "=") + ", " + arrived.guest-pref.
                                    LEAVE.
                                END.
                            END.
                        END.
                    END.
                END.
            END.    
        END. 
 
        IF (res-line.resstatus = 1 OR res-line.resstatus = 2 
            OR res-line.resstatus = 5
            OR res-line.resstatus = 11) THEN 
        DO: 
            arriving2 = arriving2 + res-line.zimmeranz 
              * (res-line.erwachs + res-line.gratis 
               + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]). 
            eocc2 = eocc2 + res-line.zimmeranz 
              * (res-line.erwachs + res-line.gratis 
               + res-line.kind1 + res-line.kind2 + res-line.l-zuordnung[4]). 
        END. 
    END. 
 
    tot-arrive1 = arrived1 + arriving1. 
    tot-arrive2 = arrived2 + arriving2. 
 
    FOR EACH zimmer NO-LOCK, 
        FIRST zimkateg NO-LOCK WHERE zimkateg.zikatnr = zimmer.zikatnr: 
        IF zimkateg.verfuegbarkeit THEN 
        DO: 
          FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
            AND outorder.gespstart LE ci-date AND outorder.gespende GE ci-date
            AND outorder.betriebsnr = 2 NO-LOCK NO-ERROR.
          IF AVAILABLE outorder THEN 
          DO:
            omroom1 = omroom1 + 1.
            CREATE off-market.
            ASSIGN
                off-market.room = zimmer.zinr
                off-market.rmtype = zimkateg.kurzbez
                off-market.gname = outorder.gespgrund.
          END.                                       
/*        ELSE  to be checked if this is correct */
          DO:
            IF (zimmer.zistatus = 0 OR zimmer.zistatus = 1 
              OR zimmer.zistatus = 5) THEN 
            DO: 
                IF zimmer.zistatus = 0 THEN 
                DO:
                    vclean = vclean + 1. 
                    CREATE vacant-clean-checked.
                    ASSIGN
                        vacant-clean-checked.room = zimmer.zinr
                        vacant-clean-checked.rmtype = zimkateg.kurzbez.
                END.
                ELSE IF zimmer.zistatus = 1 THEN
                DO:
                    vuncheck = vuncheck + 1. 
                    CREATE vacant-clean-unchecked.
                    ASSIGN
                        vacant-clean-unchecked.room = zimmer.zinr
                        vacant-clean-unchecked.rmtype = zimkateg.kurzbez.
                END.
                ELSE IF zimmer.zistatus = 5 THEN 
                DO:
                    oclean = oclean + 1.
                    CREATE occ-clean.
                    ASSIGN
                        occ-clean.room = zimmer.zinr
                        occ-clean.rmtype = zimkateg.kurzbez.
                    FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr
                        AND res-line.resstatus = 6 
                        AND res-line.active-flag = 1 NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN
                    DO:
                        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN
                            occ-clean.gname = guest.name + ", " + guest.vorname1 
                                + " " + guest.anrede1. 
                    END.
                END.                    
            END. 
            ELSE IF (zimmer.zistatus = 2 OR zimmer.zistatus = 3 
                OR zimmer.zistatus = 4) THEN 
            DO: 
                IF zimmer.zistatus = 2 THEN 
                DO:
                    vdirty = vdirty + 1. 
                    CREATE vacant-dirty.
                    ASSIGN
                        vacant-dirty.room = zimmer.zinr
                        vacant-dirty.rmtype = zimkateg.kurzbez.
                END.                
                ELSE IF zimmer.zistatus = 4 THEN
                DO:
                    odirty = odirty + 1. 
                    CREATE occ-dirty.
                    ASSIGN
                        occ-dirty.room = zimmer.zinr
                        occ-dirty.rmtype = zimkateg.kurzbez.
                    FIND FIRST res-line WHERE res-line.zinr = zimmer.zinr
                        AND res-line.resstatus = 6 
                        AND res-line.active-flag = 1 NO-LOCK NO-ERROR.
                    IF AVAILABLE res-line THEN
                    DO:
                        FIND FIRST guest WHERE guest.gastnr = res-line.gastnrmember NO-LOCK NO-ERROR.
                        IF AVAILABLE guest THEN
                            occ-dirty.gname = guest.name + ", " + guest.vorname1 
                                + " " + guest.anrede1. 
                    END.
                END.
                ELSE IF zimmer.zistatus = 3 THEN 
                DO:
                    atoday = atoday + 1. 
                    CREATE ex-depart.
                    ASSIGN
                        ex-depart.room = zimmer.zinr
                        ex-depart.rmtype = zimkateg.kurzbez.
                END.             
            END. 
            ELSE IF zimmer.zistatus = 6 THEN 
            DO:
                oooroom1 = oooroom1 + 1. 
                CREATE ooo-room.
                ASSIGN
                    ooo-room.room = zimmer.zinr
                    ooo-room.rmtype = zimkateg.kurzbez.
                FIND FIRST outorder WHERE outorder.zinr = zimmer.zinr
                    AND outorder.gespstart LE ci-date AND outorder.gespende GE ci-date
                    AND outorder.betriebsnr NE 2 NO-LOCK NO-ERROR.
                IF AVAILABLE outorder THEN
                    ooo-room.gname = outorder.gespgrund.
            END.                                        
            IF NOT zimmer.sleeping THEN iroom1 = iroom1 + 1. 
            IF zimmer.sleeping THEN tot-zimmer = tot-zimmer + 1. 
          END. 
        END.
    END. 
 
    proz1 = oroom1 * 100 / tot-zimmer. 
    proz2 = oooroom1 * 100 / tot-zimmer. 
    proz3 = eocc1 * 100 / tot-zimmer. 
    proz4 = compRoom1 * 100 / tot-zimmer. 
    proz5 = houseRoom1 * 100 / tot-zimmer. 
END. 
