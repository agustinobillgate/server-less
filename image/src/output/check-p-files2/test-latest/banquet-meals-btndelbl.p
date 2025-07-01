DEFINE TEMP-TABLE meal-list
    FIELD nr        AS INTEGER   FORMAT ">>>"   LABEL "No"
    FIELD meals     AS CHARACTER FORMAT "x(25)" LABEL "Meals"
    FIELD times     AS CHARACTER FORMAT "x(13)" LABEL "Time"
    FIELD venue     AS CHARACTER FORMAT "x(24)" LABEL "Venue"
    FIELD pax       AS INTEGER   FORMAT ">>>>"   LABEL "Pax"
    FIELD setup     AS CHARACTER FORMAT "x(24)" LABEL "Setup"
    .

DEFINE INPUT PARAMETER resnr    AS INTEGER.
DEFINE INPUT PARAMETER reslinno AS INTEGER.
DEFINE INPUT PARAMETER TABLE FOR meal-list. 
DEFINE VARIABLE str1        AS CHAR.
DEFINE VARIABLE str         AS CHAR.
DEFINE VARIABLE tokcounter  AS INTEGER               NO-UNDO.
DEFINE VARIABLE gpDelimiter AS CHAR     INITIAL ";"  NO-UNDO.
DEFINE VARIABLE mesToken    AS CHAR                  NO-UNDO.
DEFINE VARIABLE mesValue    AS CHAR                  NO-UNDO.
DEFINE VARIABLE stringcount AS INTEGER               NO-UNDO.
DEFINE VARIABLE getstring   AS CHAR                  NO-UNDO.

FOR EACH meal-list:
    ASSIGN str1 = str1 + "|" + string(meal-list.nr   ) + ";"
                           + string(meal-list.meals) + ";"  
                           + string(meal-list.times) + ";"  
                           + string(meal-list.venue) + ";"  
                           + string(meal-list.pax  ) + ";"  
                           + string(meal-list.setup).   
END.

FIND FIRST bk-func WHERE bk-func.veran-nr EQ resnr 
AND bk-func.veran-seite EQ reslinno EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE bk-func THEN
DO:
    IF NUM-ENTRIES(bk-func.f-menu[1],"$") GT 1 THEN
    DO:
        ASSIGN ENTRY(2,bk-func.f-menu[1],"$") = "". 
        ASSIGN ENTRY(2,bk-func.f-menu[1],"$") = str1. 
        ASSIGN str = ENTRY(2,bk-func.f-menu[1],"$").  
    END.
    ELSE 
    ASSIGN bk-func.f-menu[1] = bk-func.f-menu[1] + "$" + str1. 
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

