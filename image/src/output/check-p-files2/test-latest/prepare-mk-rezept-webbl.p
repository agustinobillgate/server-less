
DEF TEMP-TABLE t-l-artikel LIKE l-artikel.

DEF TEMP-TABLE t-h-rezept LIKE h-rezept
    FIELD cost-percent              AS DECIMAL
    FIELD poten-sell-price          AS DECIMAL.

DEFINE TEMP-TABLE cost-list 
  FIELD artnrrezept AS INTEGER 
  FIELD cost AS DECIMAL FORMAT ">,>>>,>>>,>>9.99". 

DEF TEMP-TABLE t-artikel 
    FIELD artnr-no AS CHAR.

DEFINE INPUT PARAMETER TABLE FOR t-artikel.
DEF OUTPUT PARAMETER price-type AS INT.
DEF OUTPUT PARAMETER TABLE FOR t-l-artikel.
DEF OUTPUT PARAMETER TABLE FOR t-h-rezept.
DEF OUTPUT PARAMETER TABLE FOR cost-list.


DEF VAR curr-i AS INTEGER NO-UNDO. 
FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK.
price-type = htparam.finteger.
/* -START RS 19 feb 2010 add this code to prevent error message "Entry 2 is outside the range of list" */
FOR EACH l-artikel WHERE l-artikel.herkunft = "" EXCLUSIVE-LOCK :
    ASSIGN l-artikel.herkunft = ";;".
END.
RELEASE l-artikel.
/* -END RS 19 feb 2010 */

IF t-artikel.artnr-no NE "" THEN 
DO:
    FIND FIRST t-artikel NO-LOCK.
    FIND FIRST l-artikel WHERE STRING(l-artikel.artnr) EQ t-artikel.artnr-no NO-LOCK.
    IF AVAILABLE l-artikel THEN 
    DO:
        RUN create-list.
        RUN calculate-cost.
    END. 
END.
ELSE 
DO:
    RUN create-all.
    RUN calculate-cost.
END.
/*FIND FIRST t-artikel NO-LOCK.
FIND FIRST l-artikel WHERE STRING(l-artikel.artnr) EQ t-artikel.artnr-no NO-LOCK.
IF AVAILABLE l-artikel THEN 
DO:
    RUN create-list.
    RUN calculate-cost.
END. 
ELSE
DO:
    RUN create-all.
    RUN calculate-cost.
END.*/ 

PROCEDURE create-all:
    FOR EACH l-artikel:
        CREATE t-l-artikel.
        BUFFER-COPY l-artikel TO t-l-artikel.
    END.

    FOR EACH h-rezept:
        CREATE t-h-rezept.
        BUFFER-COPY h-rezept TO t-h-rezept.
    END.
END.

/*bernatd 3DCD4C - 2025 */
PROCEDURE create-list: 
    FOR EACH h-rezlin WHERE h-rezlin.artnrlager EQ l-artikel.artnr NO-LOCK,
        FIRST h-rezept WHERE h-rezept.artnrrezept EQ h-rezlin.artnrrezept NO-LOCK: 
        IF h-rezlin.recipe-flag THEN 
        DO:
            FIND FIRST t-h-rezept WHERE t-h-rezept.artnrrezept EQ h-rezlin.artnrlager NO-LOCK.
            IF NOT AVAILABLE t-h-rezept THEN 
            DO:
                RUN create-list.
            END.  
        END.
        ELSE 
        DO:
            CREATE t-h-rezept.
            BUFFER-COPY h-rezept TO t-h-rezept.
        END.
    END. 
END.
/*end bernatd */

PROCEDURE calculate-cost: 
DEFINE VARIABLE amount AS DECIMAL. 
 
    FOR EACH t-h-rezept NO-LOCK: 
        curr-i = 0. 
        FIND FIRST cost-list WHERE cost-list.artnrrezept = t-h-rezept.artnrrezept 
            NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE cost-list THEN 
        DO: 
            create cost-list. 
            cost-list.artnrrezept = t-h-rezept.artnrrezept. 
            
            amount = 0. 
            RUN cal-cost(t-h-rezept.artnrrezept, 1, INPUT-OUTPUT amount). 
            cost-list.cost = amount. 
            
        END. 
    END. 
END. 

PROCEDURE cal-cost: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER. 
DEFINE INPUT PARAMETER menge AS DECIMAL. 
DEFINE INPUT-OUTPUT PARAMETER cost AS DECIMAL. 

DEFINE VARIABLE inh AS DECIMAL. 
DEF VAR i AS INTEGER NO-UNDO.
DEFINE BUFFER h-recipe FOR t-h-rezept. 
DEFINE BUFFER hrecipe  FOR t-h-rezept.

    /*naufal add no-error & if available*/
    FIND FIRST h-recipe WHERE h-recipe.artnrrezept = p-artnr NO-LOCK NO-ERROR.
    IF AVAILABLE h-recipe THEN
    DO:
        FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = p-artnr NO-LOCK: 
            IF h-rezlin.recipe-flag = YES THEN DO:
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















