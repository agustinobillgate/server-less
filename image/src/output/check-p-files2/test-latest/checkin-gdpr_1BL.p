
DEFINE TEMP-TABLE nation-list
    FIELD nr        AS INTEGER
    FIELD kurzbez   AS CHAR
    FIELD bezeich   AS CHAR FORMAT "x(32)".

DEFINE INPUT PARAMETER gastnr    AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER err-flag AS INTEGER NO-UNDO.
DEFINE OUTPUT PARAMETER save-day AS INTEGER NO-UNDO.

DEFINE VARIABLE curr-nat     AS CHAR    NO-UNDO.
DEFINE VARIABLE do-it        AS LOGICAL NO-UNDO.

DEFINE VARIABLE list-region         AS CHAR    NO-UNDO.
DEFINE VARIABLE list-nat            AS CHAR    NO-UNDO.
DEFINE VARIABLE loopi               AS INTEGER NO-UNDO.


FIND FIRST htparam WHERE htparam.paramnr = 466 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN save-day = htparam.fint.


FOR EACH nation WHERE nation.natcode = 0 NO-LOCK,
    FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe
        AND queasy.char1 MATCHES "*europe*" NO-LOCK BY nation.kurzbez:
    CREATE nation-list.
    ASSIGN nation-list.nr      = nation.nationnr
           nation-list.kurzbez = nation.kurzbez
           nation-list.bezeich = ENTRY(1, nation.bezeich, ";").           
END.

FIND FIRST htparam WHERE htparam.paramnr = 448 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN list-region = htparam.fchar.

FIND FIRST htparam WHERE htparam.paramnr = 449 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN ASSIGN list-nat = htparam.fchar. 

IF list-region NE "" THEN DO:
    DO loopi = 1 TO NUM-ENTRIES(list-region, ";"):
        FOR EACH nation WHERE nation.natcode = 0 
            AND nation.untergruppe = INTEGER(ENTRY(loopi, list-region, ";")) NO-LOCK BY nation.kurzbez:
            FIND FIRST nation-list WHERE nation-list.nr = nation.nationnr NO-ERROR.
            IF NOT AVAILABLE nation-list THEN DO:                    
                CREATE nation-list.
                ASSIGN nation-list.nr      = nation.nationnr
                       nation-list.kurzbez = nation.kurzbez
                       nation-list.bezeich = ENTRY(1, nation.bezeich, ";").           
            END.
        END.
    END.        
END.
/*ELSE DO:
    FOR EACH nation WHERE nation.natcode = 0 NO-LOCK,
        FIRST queasy WHERE queasy.KEY = 6 AND queasy.number1 = nation.untergruppe
            AND queasy.char1 MATCHES "*europe*" NO-LOCK BY nation.kurzbez:
        FIND FIRST nation-list WHERE nation-list.nr = nation.nationnr NO-ERROR.
        IF NOT AVAILABLE nation-list THEN DO:                    
            CREATE nation-list.
            ASSIGN nation-list.nr      = nation.nationnr
                   nation-list.kurzbez = nation.kurzbez
                   nation-list.bezeich = ENTRY(1, nation.bezeich, ";").           
        END.          
    END.
END.*/

IF list-nat NE "" THEN DO:
    DO loopi = 1 TO NUM-ENTRIES(list-nat, ";"):
        FOR EACH nation WHERE nation.natcode = 0 
            AND nation.nationnr = INTEGER(ENTRY(loopi, list-nat, ";")) NO-LOCK BY nation.kurzbez:
            FIND FIRST nation-list WHERE nation-list.nr = nation.nationnr NO-ERROR.
            IF NOT AVAILABLE nation-list THEN DO:                    
                CREATE nation-list.
                ASSIGN nation-list.nr      = nation.nationnr
                       nation-list.kurzbez = nation.kurzbez
                       nation-list.bezeich = ENTRY(1, nation.bezeich, ";").           
            END.           
        END.
    END.       
END.

FIND FIRST guest WHERE guest.gastnr = gastnr NO-LOCK NO-ERROR.
IF AVAILABLE guest THEN DO:
    /*gerald gdpr can't active if has membership card 180121*/
    FIND FIRST mc-guest WHERE mc-guest.gastnr = guest.gastnr NO-LOCK NO-ERROR.
    IF AVAILABLE mc-guest THEN DO: 
        ASSIGN err-flag = 2.            
        RETURN.
    END.

    ASSIGN do-it = YES.
    IF do-it THEN DO:
        IF guest.land NE " " THEN DO : 
            ASSIGN curr-nat = guest.land.
            FIND FIRST nation-list WHERE nation-list.kurzbez = curr-nat NO-LOCK NO-ERROR.
            IF AVAILABLE nation-list THEN ASSIGN do-it = YES.
            ELSE ASSIGN do-it = NO.
        END.
        
        IF do-it = NO THEN DO:
            IF guest.nation1 NE " " THEN DO:
                 ASSIGN curr-nat = guest.nation1.
                 FIND FIRST nation-list WHERE nation-list.kurzbez = curr-nat NO-LOCK NO-ERROR.
                 IF AVAILABLE nation-list THEN ASSIGN do-it = YES.
                 ELSE ASSIGN do-it = NO.
            END.               
        END.
    END.
    
    IF do-it = YES THEN DO:
        ASSIGN err-flag = 1.
        RETURN.
    END.
       
END.
