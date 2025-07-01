/*FD Dec 15, 2020 => BL for vhpweb based move from ui to BL*/
DEFINE TEMP-TABLE t-eg-maintain LIKE eg-maintain.

DEFINE TEMP-TABLE smaintain
    FIELD maintainnr    AS INTEGER
    FIELD estWorkDate   AS DATE
    FIELD workdate      AS DATE
    FIELD donedate      AS DATE
    FIELD stat-nr       AS INTEGER
    FIELD stat-nm       AS CHAR     FORMAT "x(20)"
    FIELD freq          AS CHAR     FORMAT "x(20)"
    FIELD category-str  AS CHAR     FORMAT "x(20)"
    FIELD maintask      AS CHAR     FORMAT "x(24)"
    FIELD location      AS CHAR     FORMAT "x(24)"
    FIELD zinr          AS CHAR     FORMAT "x(20)"
    FIELD property      AS CHAR     FORMAT "x(40)"
    FIELD comments      AS CHAR     FORMAT "x(30)"
    FIELD pic           AS CHAR     FORMAT "x(20)"
    FIELD str           AS CHAR     FORMAT "x(2)" INITIAL ""

    INDEX typealldatum      stat-nr estworkdate workdate    donedate
.

DEFINE TEMP-TABLE tStatus
    FIELD stat-nr AS INTEGER
    FIELD stat-nm AS CHAR           FORMAT "x(24)"
    FIELD stat-selected AS LOGICAL INITIAL NO
.

DEFINE TEMP-TABLE tLocation
    FIELD loc-nr  AS INTEGER 
    FIELD loc-nm  AS CHAR       FORMAT "x(24)" COLUMN-LABEL "Location"
    FIELD loc-selected AS LOGICAL INITIAL NO
    FIELD loc-guest AS LOGICAL INITIAL NO
.

DEFINE TEMP-TABLE tMaintask
    FIELD Main-nr  AS INTEGER 
    FIELD Main-nm  AS CHAR FORMAT "x(24)" COLUMN-LABEL "Object"
    FIELD main-selected AS LOGICAL INITIAL NO
.

DEFINE TEMP-TABLE troom
    FIELD room-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Room"
    FIELD room-Selected AS LOGICAL INITIAL NO
.

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
    FIELD pzinr         AS CHAR     FORMAT "x(20)" 
.

DEFINE TEMP-TABLE tpic
    FIELD pic-nr AS INTEGER
    FIELD pic-nm AS CHAR FORMAT "x(24)" COLUMN-LABEL "Name"
    FIELD pic-selected AS LOGICAL INITIAL NO
.

DEFINE TEMP-TABLE tFrequency
    FIELD freq-nr AS INTEGER
    FIELD freq-nm AS CHAR FORMAT "x(24)"
.

DEFINE INPUT PARAMETER all-room     AS LOGICAL.
DEFINE INPUT PARAMETER all-status   AS LOGICAL.
DEFINE INPUT PARAMETER all-location AS LOGICAL.
DEFINE INPUT PARAMETER all-property AS LOGICAL.
DEFINE INPUT PARAMETER all-pic      AS LOGICAL.
DEFINE INPUT PARAMETER fdate        AS DATE.
DEFINE INPUT PARAMETER tdate        AS DATE.
DEFINE INPUT PARAMETER main-date    AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR tMaintask.
DEFINE INPUT PARAMETER TABLE FOR tFrequency.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tStatus.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tLocation.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR troom.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tproperty.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR tpic.
DEFINE OUTPUT PARAMETER TABLE FOR smaintain.

DEFINE VARIABLE int-str AS CHAR EXTENT 6
    INITIAL ["Weekly", "Monthly", "Quarter", "Half Yearly", "Year"].

FOR EACH smaintain:
    DELETE smaintain.
END.

RUN eg-repmaintain-all-locationbl.p
    (all-room, INPUT TABLE tLocation, INPUT TABLE tMaintask,
        OUTPUT TABLE troom, OUTPUT TABLE tproperty).

IF all-status THEN
    FOR EACH tstatus:
        ASSIGN tstatus.stat-selected = YES.
    END.

IF all-location THEN
    FOR EACH tlocation :
        ASSIGN tlocation.loc-selected = YES.
    END.

IF all-property THEN
    FOR EACH tproperty:
        ASSIGN tproperty.prop-selected = YES.
    END.

IF all-pic THEN
    FOR EACH tpic:
        ASSIGN tpic.pic-selected = YES.
    END.

RUN eg-repmaintain-open-querybl.p (fdate, tdate, OUTPUT TABLE t-eg-maintain).

IF main-date = 1 THEN
DO:
    FOR EACH t-eg-maintain NO-LOCK ,
        FIRST tLocation WHERE tLocation.loc-nr = t-eg-maintain.location AND tLocation.loc-selected NO-LOCK, 
        FIRST tproperty WHERE tproperty.prop-nr = t-eg-maintain.propertynr AND tproperty.prop-selected NO-LOCK,
        FIRST tstatus WHERE tstatus.stat-nr = t-eg-maintain.TYPE AND tstatus.stat-selected NO-LOCK ,
        FIRST tpic WHERE tpic.pic-nr = t-eg-maintain.pic AND tpic.pic-selected NO-LOCK ,
        FIRST tFrequency WHERE tFrequency.freq-nr = t-eg-maintain.TYPE NO-LOCK .
        RUN create-temp.
    END.

END.
ELSE IF main-date = 2 THEN
DO:
    FOR EACH t-eg-maintain NO-LOCK ,
        FIRST tLocation WHERE tLocation.loc-nr = t-eg-maintain.location AND tLocation.loc-selected NO-LOCK, 
        FIRST tproperty WHERE tproperty.prop-nr = t-eg-maintain.propertynr AND tproperty.prop-selected NO-LOCK,
        FIRST tstatus WHERE tstatus.stat-nr = t-eg-maintain.TYPE AND tstatus.stat-selected NO-LOCK ,
        FIRST tpic WHERE tpic.pic-nr = t-eg-maintain.pic AND tpic.pic-selected NO-LOCK ,
        FIRST tFrequency WHERE tFrequency.freq-nr = t-eg-maintain.TYPE NO-LOCK .
        RUN create-temp.
    END.
END.
ELSE IF main-date = 3 THEN
DO:
    FOR EACH t-eg-maintain NO-LOCK ,
        FIRST tLocation WHERE tLocation.loc-nr = t-eg-maintain.location AND tLocation.loc-selected NO-LOCK, 
        FIRST tproperty WHERE tproperty.prop-nr = t-eg-maintain.propertynr AND tproperty.prop-selected NO-LOCK,
        FIRST tstatus WHERE tstatus.stat-nr = t-eg-maintain.TYPE AND tstatus.stat-selected NO-LOCK ,
        FIRST tpic WHERE tpic.pic-nr = t-eg-maintain.pic AND tpic.pic-selected NO-LOCK ,
        FIRST tFrequency WHERE tFrequency.freq-nr = t-eg-maintain.TYPE NO-LOCK .
        RUN create-temp.
    END.
END.

/********************************************************************************************/
PROCEDURE create-temp:
    CREATE smaintain.
    ASSIGN  
        smaintain.maintainnr    = t-eg-maintain.maintainnr   
        smaintain.estWorkDate   = t-eg-maintain.estWorkDate  
        smaintain.workdate      = t-eg-maintain.workdate      
        smaintain.donedate      = t-eg-maintain.donedate   
        smaintain.stat-nr       = t-eg-maintain.TYPE
        smaintain.stat-nm       = tstatus.stat-nm      
        smaintain.freq          = int-str[t-eg-maintain.typework]  
        smaintain.category      = tproperty.pcateg
        smaintain.maintask      = tproperty.pmain     
        smaintain.location      = tLocation.loc-nm /*t-eg-maintain.location tproperty.ploc*/     
        smaintain.zinr          = t-eg-maintain.zinr  /*tproperty.pzinr */       
        smaintain.property      = tproperty.prop-nm     
        smaintain.comments      = t-eg-maintain.comments     
        smaintain.pic           = tpic.pic-nm
    .
END.
