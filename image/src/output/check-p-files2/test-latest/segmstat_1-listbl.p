
DEFINE TEMP-TABLE segmstat-list
    FIELD segmentcode   AS INTEGER  
    FIELD descrip       AS CHARACTER    FORMAT "x(32)"
    FIELD room          AS INTEGER      FORMAT ">>>>9"
    FIELD budget        AS INTEGER      FORMAT ">>>>9"
    FIELD percent       AS CHARACTER    FORMAT "x(10)" 
    FIELD g-room        AS INTEGER      FORMAT ">>>>9"
    FIELD g-budget      AS INTEGER      FORMAT ">>>>9"
    FIELD g-percent     AS CHARACTER    FORMAT "x(10)" 
    FIELD t-room        AS DECIMAL      FORMAT "->>,>>>,>>>,>>>,>>9.99"
    FIELD t-budget      AS DECIMAL      FORMAT "->>,>>>,>>>,>>>,>>9.99"
    FIELD t-percent     AS CHARACTER    FORMAT "x(10)"
    FIELD room-ytd      AS INTEGER      FORMAT ">>>>9"                 
    FIELD budget-ytd    AS INTEGER      FORMAT ">>>>9"                 
    FIELD percent-ytd   AS CHARACTER    FORMAT "x(10)"                 
    FIELD g-room-ytd    AS INTEGER      FORMAT ">>>>9"                 
    FIELD g-budget-ytd  AS INTEGER      FORMAT ">>>>9"                 
    FIELD g-percent-ytd AS CHARACTER    FORMAT "x(10)"                 
    FIELD t-room-ytd    AS DECIMAL      FORMAT "->>,>>>,>>>,>>>,>>9.99"
    FIELD t-budget-ytd  AS DECIMAL      FORMAT "->>,>>>,>>>,>>>,>>9.99"
    FIELD t-percent-ytd AS CHARACTER    FORMAT "x(10)"              
    .

DEFINE TEMP-TABLE t-segmstat-list
    FIELD descrip       AS CHARACTER    FORMAT "x(32)"
    FIELD room-ytd      AS INTEGER      FORMAT ">>>>9" 
    FIELD budget-ytd    AS INTEGER      FORMAT ">>>>9"
    FIELD percent-ytd   AS CHARACTER    FORMAT "x(10)"
    FIELD g-room-ytd    AS INTEGER      FORMAT ">>>>9"
    FIELD g-budget-ytd  AS INTEGER      FORMAT ">>>>9" 
    FIELD g-percent-ytd AS CHARACTER    FORMAT "x(10)" 
    FIELD t-room-ytd    AS DECIMAL      FORMAT "->>,>>>,>>>,>>>,>>9.99"
    FIELD t-budget-ytd  AS DECIMAL      FORMAT "->>,>>>,>>>,>>>,>>9.99"
    FIELD t-percent-ytd AS CHARACTER    FORMAT "x(10)" 
    .

DEFINE INPUT PARAMETER from-date    AS DATE.
DEFINE INPUT PARAMETE to-date       AS DATE.
DEFINE OUTPUT PARAMETER TABLE FOR segmstat-list.

DEFINE VARIABLE black-list      AS INTEGER NO-UNDO.
DEFINE VARIABLE price-decimal   AS INTEGER NO-UNDO. 

DEFINE VARIABLE room        AS INTEGER NO-UNDO. 
DEFINE VARIABLE person      AS INTEGER NO-UNDO. 
DEFINE VARIABLE broom       AS INTEGER NO-UNDO. 
DEFINE VARIABLE bperson     AS INTEGER NO-UNDO. 
DEFINE VARIABLE proz1       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE proz2       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE proz3       AS DECIMAL NO-UNDO. 
DEFINE VARIABLE lodging     AS DECIMAL NO-UNDO. 
DEFINE VARIABLE blodging    AS DECIMAL NO-UNDO. 

DEFINE VARIABLE t-room      AS INTEGER NO-UNDO INITIAL 0. 
DEFINE VARIABLE t-broom     AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE t-person    AS INTEGER NO-UNDO INITIAL 0. 
DEFINE VARIABLE t-bperson   AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE t-lodging   AS DECIMAL NO-UNDO INITIAL 0. 
DEFINE VARIABLE t-blodging  AS DECIMAL NO-UNDO INITIAL 0. 



/***************************************************************************/

FIND FIRST htparam WHERE paramnr = 709 NO-LOCK. 
black-list = htparam.finteger. 

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger.   /* non-digit OR digit version */ 
 
FOR EACH segment WHERE segment.segmentcode NE black-list 
    AND NOT segment.bezeich MATCHES ("*$$0*")   /*FD Dec 08, 2021 => get validation for active segment*/
    NO-LOCK BY segment.segmentcode: 
   
    room        = 0. 
    person      = 0. 
    broom       = 0. 
    bperson     = 0. 
    lodging     = 0. 
    blodging    = 0. 
    proz1       = 0. 
    proz2       = 0. 
    proz3       = 0. 

    CREATE segmstat-list. 
    segmstat-list.segmentcode = segment.segmentcode.
    segmstat-list.descrip     = STRING(segment.segmentcode, ">>9") + " - " + 
                                STRING(ENTRY(1, segment.bezeich, "$$0"), "x(21)"). 

    FOR EACH segmentstat WHERE segmentstat.segmentcode = segment.segmentcode 
        AND segmentstat.datum GE from-date AND segmentstat.datum LE to-date 
        NO-LOCK: 
        ASSIGN  t-room      = t-room + segmentstat.zimmeranz
                t-broom     = t-broom + segmentstat.budzimmeranz
                t-person    = t-person + segmentstat.persanz + 
                              segmentstat.kind1 + segmentstat.kind2 + 
                              segmentstat.gratis
                t-bperson   = t-bperson + segmentstat.budpersanz
                t-lodging   = t-lodging + segmentstat.logis
                t-blodging  = t-blodging + segmentstat.budlogis
                room        = room + segmentstat.zimmeranz
                person      = person + segmentstat.persanz + 
                              segmentstat.kind1 + segmentstat.kind2 + 
                              segmentstat.gratis
                broom       = broom + segmentstat.budzimmeranz
                bperson     = bperson + segmentstat.budpersanz
                lodging     = lodging + segmentstat.logis
                blodging    = blodging + segmentstat.budlogis
                .
    END. 

    IF broom NE 0 THEN proz1 = room / broom * 100. 
    IF bperson NE 0 THEN proz2 = person / bperson * 100. 
    IF blodging NE 0 THEN proz3 = lodging / blodging * 100. 
    
    ASSIGN  
        segmstat-list.room      = room 
        segmstat-list.budget    = broom 
        segmstat-list.g-room    = person 
        segmstat-list.g-budget  = bperson 
        .

    ASSIGN  
        segmstat-list.t-room    = lodging 
        segmstat-list.t-budget  = blodging 
        segmstat-list.percent   = STRING(proz1, ">,>>9.99")
        segmstat-list.g-percent = STRING(proz2, ">,>>9.99")
        segmstat-list.t-percent = STRING(proz3, ">,>>9.99")
        .
END. 

CREATE segmstat-list.

ASSIGN  
    segmstat-list.descrip   = "T O T A L" 
    segmstat-list.room      = t-room 
    segmstat-list.budget    = t-broom 
    segmstat-list.percent   = ""
    segmstat-list.g-room    = t-person 
    segmstat-list.g-budget  = t-bperson 
    segmstat-list.g-percent = ""  
    segmstat-list.t-percent = ""
    . 

ASSIGN  
    segmstat-list.t-room    = t-lodging
    segmstat-list.t-budget  = t-blodging 
    .

t-room      = 0.   
t-broom     = 0.  
t-person    = 0.
t-bperson   = 0.
t-lodging   = 0.
t-blodging  = 0.

/* Add by Michael @ 13/12/2018 for B Hotel request - ticket no F693E0 */
/* for YTD */
FOR EACH segment WHERE segment.segmentcode NE black-list 
    NO-LOCK BY segment.segmentcode: 
    CREATE t-segmstat-list. 
    room        = 0. 
    person      = 0. 
    broom       = 0. 
    bperson     = 0. 
    lodging     = 0. 
    blodging    = 0. 
    proz1       = 0. 
    proz2       = 0. 
    proz3       = 0. 

    t-segmstat-list.descrip = STRING(segment.segmentcode, ">>9") + " - " + 
                            STRING(ENTRY(1, segment.bezeich, "$$0"), "x(21)"). 

    ASSIGN from-date = DATE(1, 1, YEAR(to-date)).
    FOR EACH segmentstat WHERE segmentstat.segmentcode = segment.segmentcode 
        AND segmentstat.datum GE from-date AND segmentstat.datum LE to-date 
        NO-LOCK: 
        ASSIGN  t-room      = t-room + segmentstat.zimmeranz
                t-broom     = t-broom + segmentstat.budzimmeranz
                t-person    = t-person + segmentstat.persanz + 
                              segmentstat.kind1 + segmentstat.kind2 + 
                              segmentstat.gratis
                t-bperson   = t-bperson + segmentstat.budpersanz
                t-lodging   = t-lodging + segmentstat.logis
                t-blodging  = t-blodging + segmentstat.budlogis
                room        = room + segmentstat.zimmeranz
                person      = person + segmentstat.persanz + 
                              segmentstat.kind1 + segmentstat.kind2 + 
                              segmentstat.gratis
                broom       = broom + segmentstat.budzimmeranz
                bperson     = bperson + segmentstat.budpersanz
                lodging     = lodging + segmentstat.logis
                blodging    = blodging + segmentstat.budlogis
                .
    END. 

    IF broom NE 0 THEN proz1 = room / broom * 100. 
    IF bperson NE 0 THEN proz2 = person / bperson * 100. 
    IF blodging NE 0 THEN proz3 = lodging / blodging * 100. 
    
    ASSIGN  
        t-segmstat-list.room-ytd      = room 
        t-segmstat-list.budget-ytd    = broom
        t-segmstat-list.g-room-ytd    = person
        t-segmstat-list.g-budget-ytd  = bperson 
        . 

    ASSIGN  
        t-segmstat-list.t-room-ytd    = lodging
        t-segmstat-list.t-budget-ytd  = blodging
        t-segmstat-list.percent-ytd   = STRING(proz1, ">>>9.99")
        t-segmstat-list.t-percent-ytd = STRING(proz2, ">>>9.99")
        t-segmstat-list.g-percent-ytd = STRING(proz3, ">>>9.99")
        .
END. 

CREATE t-segmstat-list.

ASSIGN  t-segmstat-list.descrip       = "T O T A L" 
        t-segmstat-list.room-ytd      = t-room 
        t-segmstat-list.budget-ytd    = t-broom 
        t-segmstat-list.percent-ytd   = "" 
        t-segmstat-list.g-room-ytd    = t-person 
        t-segmstat-list.g-budget-ytd  = t-bperson 
        t-segmstat-list.g-percent-ytd = "" 
        t-segmstat-list.t-percent-ytd = ""
    . 

ASSIGN  
    t-segmstat-list.t-room-ytd    = t-lodging
    t-segmstat-list.t-budget-ytd  = t-blodging
    .

FOR EACH t-segmstat-list, 
    FIRST segmstat-list WHERE segmstat-list.descrip EQ t-segmstat-list.descrip:    
    ASSIGN 
        segmstat-list.room-ytd = t-segmstat-list.room-ytd
        segmstat-list.budget-ytd = t-segmstat-list.budget-ytd
        segmstat-list.percent-ytd = t-segmstat-list.percent-ytd
        segmstat-list.g-room-ytd = t-segmstat-list.g-room-ytd
        segmstat-list.g-budget-ytd = t-segmstat-list.g-budget-ytd
        segmstat-list.g-percent-ytd = t-segmstat-list.g-percent-ytd
        segmstat-list.t-percent-ytd = t-segmstat-list.t-percent-ytd
        segmstat-list.t-room-ytd = t-segmstat-list.t-room-ytd
        segmstat-list.t-budget-ytd = t-segmstat-list.t-budget-ytd
        .
END.
/* End of add */

