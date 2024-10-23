DEFINE TEMP-TABLE room LIKE zimmer
    FIELD rmtype  AS CHAR FORMAT "x(36)".

DEFINE TEMP-TABLE inhouse
    FIELD gname   AS CHAR FORMAT "x(30)"    LABEL "Guest Name"
    FIELD arrival AS DATE FORMAT "99/99/99" LABEL "Arrival"
    FIELD depart  AS DATE FORMAT "99/99/99" LABEL "Departure"
    FIELD adult   AS INTEGER FORMAT ">9"    LABEL "Adult(s)"
    FIELD child   AS INTEGER FORMAT ">9"    LABEL "Child(ren)"
    .

DEFINE TEMP-TABLE arrival 
    FIELD gname     AS CHAR FORMAT "x(24)"    COLUMN-LABEL "Guest Name"
    FIELD arrival   AS DATE FORMAT "99/99/99" COLUMN-LABEL "Arrival"
    FIELD depart    AS DATE FORMAT "99/99/99" COLUMN-LABEL "Departure"
    FIELD adult     AS INTEGER FORMAT ">9"    COLUMN-LABEL "Adult"
    FIELD child     AS INTEGER FORMAT ">9"    COLUMN-LABEL "Child" 
    FIELD resstatus AS CHAR FORMAT "x(16)"    COLUMN-LABEL "ResStatus"
    .

DEFINE TEMP-TABLE t-outorder LIKE outorder.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER NO-UNDO.
DEFINE INPUT  PARAMETER rmNo    AS CHAR.

DEFINE OUTPUT PARAMETER o-str   AS CHAR.
DEFINE OUTPUT PARAMETER s-str   AS CHAR.
DEFINE OUTPUT PARAMETER rm-col  AS CHAR.
DEFINE OUTPUT PARAMETER bcol    AS INT.
DEFINE OUTPUT PARAMETER fcol    AS INT.
DEFINE OUTPUT PARAMETER fr-title AS CHAR.
DEFINE OUTPUT PARAMETER rm-stat AS CHAR FORMAT "x(24)".
DEFINE OUTPUT PARAMETER finteger AS INT.
DEFINE OUTPUT PARAMETER TABLE FOR room.
DEFINE OUTPUT PARAMETER TABLE FOR inhouse.
DEFINE OUTPUT PARAMETER TABLE FOR arrival.
DEFINE OUTPUT PARAMETER TABLE FOR t-outorder.


{supertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "rminfo".

DEFINE VARIABLE stat-list AS CHAR EXTENT 13 FORMAT "x(9)" NO-UNDO. 
stat-list[1] = translateExtended ("Guaranted",lvCAREA,""). 
stat-list[2] = translateExtended ("6 PM",lvCAREA,""). 
stat-list[3] = translateExtended ("Tentative",lvCAREA,""). 
stat-list[4] = translateExtended ("WaitList",lvCAREA,""). 
stat-list[5] = translateExtended ("OralConfirm",lvCAREA,""). 
stat-list[6] = translateExtended ("Inhouse",lvCAREA,""). 
stat-list[7] = "". 
stat-list[8] = translateExtended ("Departed",lvCAREA,""). 
stat-list[9] = translateExtended ("Cancelled",lvCAREA,""). 
stat-list[10] = translateExtended ("NoShow",lvCAREA,""). 
stat-list[11] = translateExtended ("ShareRes",lvCAREA,""). 
stat-list[12] = "". 
stat-list[13] = translateExtended ("RmSharer",lvCAREA,""). 

RUN htpint.p (297, OUTPUT finteger).
CREATE room.
RUN create-room.


/*************** PROCEDURE ***************/
PROCEDURE create-room:
    DEF BUFFER guest1 FOR guest.
    DEF BUFFER reslin1 FOR res-line.
    DEF BUFFER rbuff FOR zimmer.
    DEF VAR curr-date AS DATE.

    FIND FIRST zimmer WHERE zimmer.zinr = rmNo NO-LOCK NO-ERROR.
    IF AVAILABLE zimmer THEN
    DO:         
        BUFFER-COPY zimmer TO room.
    END.

    FIND FIRST room.

    FIND FIRST htparam WHERE paramnr = 87 NO-LOCK.
    curr-date = htparam.fdate.

    FIND FIRST paramtext WHERE paramtext.txtnr = 230 AND 
      paramtext.sprachcode = room.typ NO-LOCK NO-ERROR.
    IF AVAILABLE paramtext THEN o-str = paramtext.ptexte.
    ELSE o-str = "".

    FIND FIRST paramtext WHERE paramtext.txtnr = (room.setup + 9200) 
        NO-LOCK NO-ERROR.
    IF AVAILABLE paramtext THEN s-str = paramtext.ptexte.
    ELSE s-str = "".

    RUN create-status(room.zistatus).

    CREATE inhouse.
    FIND FIRST reslin1 WHERE reslin1.zinr = rmNo AND reslin1.active-flag = 1 
        USE-INDEX zinr_index NO-LOCK NO-ERROR.
    IF AVAILABLE reslin1 THEN
    DO:            
        FIND FIRST guest1 WHERE guest1.gastnr = reslin1.gastnrmember
            USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        IF AVAILABLE guest1 THEN
        DO:
            inhouse.gname = guest1.NAME + " " + guest1.vorname1 
                + guest1.anredefirma.
        END.
        inhouse.arrival = reslin1.ankunft.
        inhouse.depart  = reslin1.abreise.
        inhouse.adult   = reslin1.erwachs.
        inhouse.child   = reslin1.kind1.
    END.

    FOR EACH outorder WHERE outorder.zinr = rmNo AND
        outorder.gespende GE curr-date BY outorder.gespstart:
        CREATE t-outorder.
        BUFFER-COPY outorder TO t-outorder.
    END.
    
    FOR EACH reslin1 WHERE reslin1.zinr = rmNo AND reslin1.active-flag = 0 NO-LOCK:
        FIND FIRST guest1 WHERE guest1.gastnr = reslin1.gastnrmember 
            USE-INDEX gastnr_index NO-LOCK NO-ERROR.
        CREATE arrival.
        ASSIGN 
            arrival.gname = guest1.NAME + " " + guest1.vorname1 
                + guest1.anredefirma
            arrival.arrival = reslin1.ankunft
            arrival.depart  = reslin1.abreise
            arrival.adult   = reslin1.erwachs
            arrival.child   = reslin1.kind1
            arrival.resstatus = stat-list[reslin1.resstatus]
            .
    END.

    fr-title = translateExtended("Room Info", lvCAREA, "") + " ("
        + rmNo + ")".
END.

PROCEDURE create-status:
    DEF INPUT PARAMETER zistatus AS INTEGER                     NO-UNDO.
    DEF VAR stat               AS CHAR      FORMAT "x(4)"       NO-UNDO.

    DEFINE VARIABLE item-fgcol AS INTEGER EXTENT 15 INITIAL 
    [15,15,15,15,15,15,15,0,15,0,0,15,0,0,0] NO-UNDO. 

    IF zistatus = 0 THEN 
    ASSIGN
        bcol    = 8
        rm-col  = " VC "
        rm-stat = translateExtended ("Vacant Clean",lvCAREA,"").
    ELSE IF zistatus = 1 THEN 
    ASSIGN
        bcol    = 11
        rm-col  = " CU "
        rm-stat = translateExtended ("Clean Unchecked",lvCAREA,"").
    ELSE IF zistatus = 2 THEN 
    ASSIGN
        bcol    =  2
        rm-col  = " VD "
        rm-stat = translateExtended ("Vacant Dirty",lvCAREA,"").
    ELSE IF zistatus = 3 THEN 
    ASSIGN
        bcol    =  1
        rm-col  = " ED "
        rm-stat = translateExtended ("Expected Departure",lvCAREA,"").
    ELSE IF zistatus = 4 THEN 
    ASSIGN
        bcol    =  14
        rm-col  = " OD "
        rm-stat = translateExtended ("Occupied Dirty",lvCAREA,"").
    ELSE IF zistatus = 5 THEN
    ASSIGN
        bcol    =  15
        rm-col  = " OC "
        rm-stat = translateExtended ("Occupied Clean",lvCAREA,"").
    ELSE IF zistatus = 6 THEN
    ASSIGN
        bcol    =  12
        rm-col  = " OO "
        rm-stat = translateExtended ("Out Of Order",lvCAREA,"").
    ELSE IF zistatus = 7 THEN 
    ASSIGN
        bcol    =  4
        rm-col  = " OM "
        rm-stat = translateExtended ("Off Market",lvCAREA,"").
    ELSE IF zistatus = 8 THEN 
    ASSIGN
        bcol    =  5
        rm-col  = " DD "
        rm-stat = translateExtended ("Do not Disturb",lvCAREA,"").
    ELSE IF zistatus = 9 THEN
    ASSIGN
        bcol    =  13
        rm-col  = " OS "
        rm-stat = translateExtended ("Out Of Service",lvCAREA,"").

    fcol = item-fgcol[bcol].
END.
