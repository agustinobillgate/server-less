DEFINE TEMP-TABLE venue-list
    FIELD venuecode AS CHARACTER FORMAT "x(5)"  LABEL "No"
    FIELD venue     AS CHARACTER FORMAT "x(35)" LABEL "Venue"
    FIELD pax       AS INTEGER   FORMAT ">>>"   LABEL "Pax"
    .

DEFINE TEMP-TABLE meal-list
    FIELD nr        AS INTEGER   FORMAT ">>>"   LABEL "No"
    FIELD meals     AS CHARACTER FORMAT "x(25)" LABEL "Meals"
    FIELD times     AS CHARACTER FORMAT "x(13)" LABEL "Time"
    FIELD venue     AS CHARACTER FORMAT "x(24)" LABEL "Venue"
    FIELD pax       AS INTEGER   FORMAT ">>>>"   LABEL "Pax"
    FIELD setup     AS CHARACTER FORMAT "x(24)" LABEL "Setup"
    .

DEFINE TEMP-TABLE event-list
    FIELD eventcode AS CHARACTER FORMAT "x(5)"  
    FIELD eventname AS CHARACTER FORMAT "x(35)"   
    .

DEFINE TEMP-TABLE setup-list
    FIELD setupcode AS CHARACTER FORMAT "x(5)"  
    FIELD setupname AS CHARACTER FORMAT "x(35)" 
    .

DEFINE INPUT PARAMETER resnr    AS INTEGER.
DEFINE INPUT PARAMETER reslinno AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR venue-list. 
DEFINE OUTPUT PARAMETER TABLE FOR meal-list. 
DEFINE OUTPUT PARAMETER TABLE FOR event-list. 
DEFINE OUTPUT PARAMETER TABLE FOR setup-list.
DEFINE OUTPUT PARAMETER menu1 AS CHARACTER.

DEFINE VARIABLE str         AS CHAR.
DEFINE VARIABLE tokcounter  AS INTEGER               NO-UNDO.
DEFINE VARIABLE gpDelimiter AS CHAR     INITIAL ";"  NO-UNDO.
DEFINE VARIABLE mesToken    AS CHAR                  NO-UNDO.
DEFINE VARIABLE mesValue    AS CHAR                  NO-UNDO.
DEFINE VARIABLE stringcount AS INTEGER               NO-UNDO.
DEFINE VARIABLE getstring   AS CHAR                  NO-UNDO.

FOR EACH bk-raum:
    CREATE venue-list.
    ASSIGN 
        venue-list.venuecode = bk-raum.raum
        venue-list.venue     = bk-raum.bezeich
        venue-list.pax       = bk-raum.personen.
END.

FIND FIRST bk-func WHERE bk-func.veran-nr EQ resnr 
    AND bk-func.veran-seite EQ reslinno EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE bk-func THEN
DO:
    IF NUM-ENTRIES(bk-func.f-menu[1],"$") GT 1 THEN
    DO:
        ASSIGN str   = ENTRY(2,bk-func.f-menu[1],"$") 
               menu1 = ENTRY(1,bk-func.f-menu[1],"$").
    END.
END.

DO tokcounter = 1 TO NUM-ENTRIES(str, "|"):
    mesToken = ENTRY(tokcounter, str, "|").
    CREATE meal-list.
    IF mestoken NE "" THEN
    DO:
        DO stringcount = 1 TO NUM-ENTRIES (mesToken, gpDelimiter):
            getstring = ENTRY(stringcount, mesToken, gpDelimiter).
            IF getstring = "" THEN LEAVE.
            CASE stringcount:
                WHEN 1 THEN meal-list.nr    = INT(getstring).
                WHEN 2 THEN meal-list.meals = getstring.
                WHEN 3 THEN meal-list.times = getstring.
                WHEN 4 THEN meal-list.venue = getstring.
                WHEN 5 THEN meal-list.pax   = INT(getstring).
                WHEN 6 THEN meal-list.setup = getstring.
            END CASE.
        END.  /* DO stringcount... */
    END.
END. /* DO tokcounter... */

FOR EACH bk-setup NO-LOCK BY bk-setup.setup-id:
    CREATE setup-list.
    ASSIGN 
        setup-list.setupcode = STRING(bk-setup.setup-id)
        setup-list.setupname = bk-setup.bezeichnung
        .
END.

FOR EACH ba-typ NO-LOCK BY ba-typ.typ-id:
    CREATE event-list.
    ASSIGN 
        event-list.eventcode = STRING(ba-typ.typ-id)
        event-list.eventname = ba-typ.bezeichnung
        .
END.
