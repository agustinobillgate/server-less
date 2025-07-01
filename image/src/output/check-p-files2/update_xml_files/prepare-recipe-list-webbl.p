DEFINE TEMP-TABLE cost-list 
  FIELD artnrrezept AS INTEGER 
  FIELD cost AS DECIMAL FORMAT ">,>>>,>>>,>>9.99".  
DEFINE TEMP-TABLE t-h-rezept LIKE h-rezept /*bernatd FA7A78 2024*/
    FIELD cost-percent              AS DECIMAL
    FIELD poten-sell-price          AS DECIMAL.

DEF TEMP-TABLE r-list 
    FIELD max-n AS INTEGER INITIAL 0 
    FIELD recipe-nr AS INTEGER EXTENT 99 INITIAL 0. 

DEF OUTPUT PARAMETER TABLE FOR cost-list.
DEF OUTPUT PARAMETER TABLE FOR t-h-rezept.

DEF BUFFER r1-list FOR r-list.

CREATE r1-list. 
CREATE r-list. 
 
DEFINE VARIABLE price-type AS INTEGER. 
DEF VAR curr-i AS INTEGER NO-UNDO. 
FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK. 
price-type = htparam.finteger. 

RUN calculate-cost.

/*start bernatd FA7A78*/
FOR EACH h-rezept:
    CREATE t-h-rezept.
    BUFFER-COPY h-rezept TO t-h-rezept.

    FIND FIRST queasy WHERE queasy.KEY EQ 252 AND queasy.number1 EQ h-rezept.artnrrezept NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
        t-h-rezept.cost-percent             = queasy.deci1
        t-h-rezept.poten-sell-price         = queasy.deci2.
    END.
END.
/*end bernatd*/

PROCEDURE calculate-cost: 
DEFINE VARIABLE amount AS DECIMAL. 
 
    FOR EACH h-rezept NO-LOCK: 
        BUFFER-COPY r1-list TO r-list. 
        curr-i = 0. 
        FIND FIRST cost-list WHERE cost-list.artnrrezept = h-rezept.artnrrezept 
            NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE cost-list THEN 
        DO: 
            create cost-list. 
            cost-list.artnrrezept = h-rezept.artnrrezept. 
            
            amount = 0. 
            RUN cal-cost(h-rezept.artnrrezept, 1, INPUT-OUTPUT amount). 
            cost-list.cost = amount.         /* / h-rezept.portion. */ 
            
        END. 
    END. 
END. 


PROCEDURE cal-cost: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 

DEFINE VARIABLE inh AS DECIMAL. 
DEF VAR i AS INTEGER NO-UNDO.
DEFINE BUFFER h-recipe FOR h-rezept. 
DEFINE BUFFER hrecipe  FOR h-rezept.

    /*naufal add no-error & if available*/
    FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK NO-ERROR.
    IF AVAILABLE h-recipe THEN
    DO:
        FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
            IF h-rezlin.recipe-flag = YES THEN DO:
                /*ITA 101116*/
                /*naufal add no-error & if available*/
                FIND FIRST hrecipe WHERE hrecipe.artnrrezept = h-rezlin.artnrlager NO-LOCK NO-ERROR.
                IF AVAILABLE hrecipe THEN
                DO:
                    IF hrecipe.portion GT 1 THEN
                        ASSIGN inh = menge * h-rezlin.menge / hrecipe.portion.
                    ELSE inh = menge * h-rezlin.menge /* SY 25022016 / h-recipe.portion */. 
                    RUN cal-cost(h-rezlin.artnrlager, inh, INPUT-OUTPUT cost). 
                END.     
            END.
            ELSE 
            DO: 
                inh = menge * h-rezlin.menge /*SY 25022016 / h-recipe.portion */.
                FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK. 
                IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
                  cost = cost + inh / l-artikel.inhalt * l-artikel.vk-preis / (1 - h-rezlin.lostfact / 100).                  
                ELSE   
                  cost = cost + inh / l-artikel.inhalt * /*l-artikel.vk-preis*/ l-artikel.ek-aktuell
                       / (1 - h-rezlin.lostfact / 100).  /*FD Sept 09, 2022 - 252594, change vk-preis to ek-aktuell*/        
            END.  
        END.
    END.
END. 

