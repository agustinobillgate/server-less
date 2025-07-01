DEFINE TEMP-TABLE meal-list
    FIELD nr        AS INTEGER   FORMAT ">>>"   LABEL "No"
    FIELD meals     AS CHARACTER FORMAT "x(25)" LABEL "Meals"
    FIELD times     AS CHARACTER FORMAT "x(13)" LABEL "Time"
    FIELD venue     AS CHARACTER FORMAT "x(24)" LABEL "Venue"
    FIELD pax       AS INTEGER   FORMAT ">>>>"   LABEL "Pax"
    FIELD setup     AS CHARACTER FORMAT "x(24)" LABEL "Setup"
    .

DEFINE INPUT PARAMETER TABLE FOR meal-list.
DEFINE INPUT PARAMETER resno    AS INTEGER.
DEFINE INPUT PARAMETER reslinno AS INTEGER.

DEFINE VARIABLE str AS CHAR.
FOR EACH meal-list:
    ASSIGN str = str + "|" + string(meal-list.nr   ) + ";"
                           + string(meal-list.meals) + ";"  
                           + string(meal-list.times) + ";"  
                           + string(meal-list.venue) + ";"  
                           + string(meal-list.pax  ) + ";"  
                           + string(meal-list.setup).   
END.

FIND FIRST bk-func WHERE bk-func.veran-nr EQ resno 
AND bk-func.veran-seite EQ reslinno EXCLUSIVE-LOCK NO-ERROR.
IF AVAILABLE bk-func THEN
DO:
    IF NUM-ENTRIES(bk-func.f-menu[1],"$") GT 1 THEN
    DO:
        ASSIGN ENTRY(2,bk-func.f-menu[1],"$") = "". 
        ASSIGN ENTRY(2,bk-func.f-menu[1],"$") = str. 
    END.
    ELSE 
    ASSIGN bk-func.f-menu[1] = bk-func.f-menu[1] + "$" + str. 
END.
