
DEFINE TEMP-TABLE h-list 
    FIELD cat-nr            AS INTEGER
    FIELD cat-name          AS CHARACTER
    FIELD cat-bezeich       AS CHARACTER
    FIELD rez-recipe-nr     AS INTEGER
    FIELD recipe-nr         AS INTEGER
    FIELD artnr             AS INTEGER
    FIELD bezeich           AS CHARACTER
    FIELD portion           AS INTEGER
    FIELD qty               AS DECIMAL FORMAT ">>>,>>9.999"
    FIELD cost              AS DECIMAL
    FIELD loss              AS DECIMAL
    FIELD cost-port         AS DECIMAL
    FIELD r-flag            AS LOGICAL
    FIELD flag              AS CHARACTER
    FIELD mass-unit         AS CHARACTER    /*FD July 21, 2021*/
    .

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER from-artnr       AS INTEGER.
DEFINE INPUT PARAMETER to-artnr         AS INTEGER.
DEFINE INPUT PARAMETER from-kateg       AS INTEGER.
DEFINE INPUT PARAMETER to-kateg         AS INTEGER.
DEFINE INPUT PARAMETER detail           AS LOGICAL.
DEFINE OUTPUT PARAMETER TABLE FOR h-list.
/* for testing
DEFINE VARIABLE from-artnr       AS INTEGER INIT 1021.
DEFINE VARIABLE to-artnr         AS INTEGER INIT 1022.
DEFINE VARIABLE from-kateg       AS INTEGER INIT 10.
DEFINE VARIABLE to-kateg         AS INTEGER INIT 10.
DEFINE VARIABLE detail           AS LOGICAL INIT YES.
*/
DEFINE VARIABLE price-type      AS INTEGER.
DEFINE VARIABLE p-artnr         AS INTEGER.
DEFINE VARIABLE menge           AS DECIMAL INITIAL 1.
DEFINE VARIABLE curr-artnr      AS INTEGER.  /*FD May 10, 2021*/
DEFINE VARIABLE main-portion    AS INTEGER. /*FD July 14, 2021*/
/* BLY - Adding Variable Total Cost and Total Cost per Portion - 96545E */
DEFINE VARIABLE v-total-cost AS DECIMAL INITIAL 0.
DEFINE VARIABLE v-total-portion AS DECIMAL INITIAL 0.
DEFINE BUFFER t-h-list FOR h-list.

FIND FIRST htparam WHERE paramnr = 1024 NO-LOCK. 
price-type = htparam.finteger. 

DO p-artnr = from-artnr TO to-artnr:
    FIND FIRST h-rezept WHERE h-rezept.artnrrezept = p-artnr NO-LOCK NO-ERROR.
    IF AVAILABLE h-rezept THEN
    DO:
        main-portion = h-rezept.portion.
        CREATE h-list.
        ASSIGN
            h-list.recipe-nr    = h-rezept.artnrrezept
            h-list.cat-nr       = h-rezept.kategorie
            h-list.cat-bezeich  = SUBSTR(h-rezept.bezeich,1,24)
            h-list.cat-name     = SUBSTR(h-rezept.bezeich,25,24)
            h-list.flag         = "**".

        RUN create-list(p-artnr, menge).
      
    END.   
    /* BLY - ADDING TOTAL COST AND TOTAL COST PER PORTION - 96545E */
    /*Modify Bernatd B1D73E 2025*/
    FOR EACH h-list WHERE h-list.cost GT 0 AND h-list.flag = "":
        v-total-cost = v-total-cost + h-list.cost.
        IF h-list.portion GT 0 THEN 
            v-total-portion = h-list.portion.
    END.

    FOR EACH h-list WHERE h-list.bezeich = "T O T A L":
        DELETE h-list.
    END.

    CREATE h-list.
    ASSIGN
        h-list.bezeich = "T O T A L"
        h-list.portion = 0
        h-list.flag = ""
        h-list.cat-nr = 0
        h-list.cat-name = ""
        h-list.cat-bezeich = ""
        h-list.rez-recipe-nr = 0
        h-list.recipe-nr = 0
        h-list.artnr = 0
        h-list.qty = 0
        h-list.cost = v-total-cost
        h-list.loss = 0
        h-list.cost-port = v-total-cost / v-total-portion
        h-list.r-flag = FALSE
        h-list.mass-unit = "".
    
    
    /*FOR EACH h-list WHERE h-list.flag = "*":
        DELETE h-list.
    END.*/
    /* End BLY - ADDING TOTAL COST AND TOTAL COST PER PORTION - 96545E */  
    /*End modify Bernatd B1D73E 2025*/ 
END.

PROCEDURE create-list: 
DEFINE INPUT PARAMETER p-artnr AS INTEGER.
DEFINE INPUT PARAMETER menge AS DECIMAL INITIAL 1.

DEFINE VARIABLE cost AS DECIMAL.
DEFINE buffer h-recipe FOR h-rezept.
DEFINE BUFFER t-h-rezlin FOR h-rezlin.

    FOR EACH h-rezlin WHERE h-rezlin.artnrrezept /*GE from-artnr
        AND h-rezlin.artnrrezept LE to-artnr*/ = p-artnr NO-LOCK:
        IF detail = YES THEN
        DO:            
            IF h-rezlin.recipe-flag = YES THEN
            DO:
                FIND FIRST h-recipe WHERE h-recipe.artnrrezept = h-rezlin.artnrlager NO-LOCK NO-ERROR.
                IF AVAILABLE h-recipe THEN
                DO:
                    curr-artnr = p-artnr. 
                    CREATE h-list.
                    ASSIGN
                        h-list.recipe-nr    = /*h-rezlin.artnrrezept*/  p-artnr
                        h-list.rez-recipe-nr = h-recipe.artnrrezept
                        h-list.cat-nr       = h-recipe.kategorie
                        h-list.cat-bezeich  = SUBSTR(h-recipe.bezeich,1,24)
                        h-list.cat-name     = SUBSTR(h-recipe.bezeich,25,24)
                        h-list.artnr        = h-recipe.artnrrezept
                        h-list.bezeich      = h-recipe.bezeich
                        h-list.qty          = h-rezlin.menge 
                        h-list.portion      = main-portion
                        h-list.r-flag       = YES
                        .
                END.                
                RUN create-list(h-rezlin.artnrlager, menge * h-rezlin.menge / h-recipe.portion).
            END.
            ELSE
            DO:
                CREATE h-list.
                FIND FIRST h-recipe WHERE h-recipe.artnrrezept = /*h-rezlin.artnrrezept*/ p-artnr NO-LOCK. 
                FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK.
                FIND FIRST t-h-rezlin WHERE t-h-rezlin.artnrrezept = curr-artnr
                    AND t-h-rezlin.artnrlager = p-artnr NO-LOCK NO-ERROR. /*FD May 10, 2021*/
                IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
                cost = (menge * h-rezlin.menge / l-artikel.inhalt * l-artikel.vk-preis) 
                 / ( 1 - h-rezlin.lostfact / 100). 
                ELSE 
                cost = (menge * h-rezlin.menge / l-artikel.inhalt * l-artikel.ek-aktuell) 
                 / ( 1 - h-rezlin.lostfact / 100).
                
                h-list.cat-nr           = h-recipe.kategorie.
                h-list.cat-bezeich      = SUBSTR(h-recipe.bezeich,1,24).
                h-list.cat-name         = SUBSTR(h-recipe.bezeich,25,24).
                h-list.recipe-nr        = /*h-rezlin.artnrrezept*/ p-artnr.
                h-list.rez-recipe-nr    = h-recipe.artnrrezept.
                h-list.artnr            = l-artikel.artnr.
                h-list.bezeich          = l-artikel.bezeich. 
                h-list.loss             = h-rezlin.lostfact. 
                h-list.qty              = h-rezlin.menge * menge. 
                h-list.cost             = cost.
                h-list.mass-unit        = l-artikel.masseinheit.
                h-list.portion          = main-portion.

                IF AVAILABLE t-h-rezlin AND t-h-rezlin.recipe-flag = YES THEN
                    h-list.cost-port = cost / /*t-h-rezlin.menge*/ main-portion.
                ELSE
                DO:
                    h-list.cost-port = cost / /*h-recipe.portion*/ main-portion.                    
                END.                  
            END.
        END.
    END.
END.

/*
PROCEDURE create-list-item:
DEFINE INPUT PARAMETER p-artnr AS INTEGER.
DEFINE INPUT PARAMETER menge AS DECIMAL.
DEFINE INPUT PARAMETER r-nr AS INTEGER.
DEFINE VARIABLE cost1 AS DECIMAL.
DEFINE BUFFER t-h-rezlin FOR h-rezlin.

    FOR EACH t-h-rezlin WHERE t-h-rezlin.artnrrezept = p-artnr NO-LOCK:
        CREATE h-list.
        ASSIGN
            h-list.recipe-nr    = t-h-rezlin.artnrrezept            
            h-list.loss         = t-h-rezlin.lostfact 
            h-list.qty          = t-h-rezlin.menge * menge.

        FIND FIRST l-artikel WHERE l-artikel.artnr = t-h-rezlin.artnrlager NO-LOCK NO-ERROR.
        IF AVAILABLE l-artikel THEN
        DO:
            IF price-type = 0 OR l-artikel.ek-aktuell = 0 THEN 
            cost1 = (menge * t-h-rezlin.menge / l-artikel.inhalt * l-artikel.vk-preis) 
             / ( 1 - h-rezlin.lostfact / 100). 
            ELSE 
            cost1 = (menge * t-h-rezlin.menge / l-artikel.inhalt * l-artikel.ek-aktuell) 
             / ( 1 - h-rezlin.lostfact / 100).

            h-list.artnr        = l-artikel.artnr.
            h-list.bezeich      = l-artikel.bezeich.
            h-list.cost         = cost1.
        END.  

        FIND FIRST h-rezept WHERE h-rezept.artnrrezept = t-h-rezlin.artnrrezept NO-LOCK NO-ERROR.
        IF AVAILABLE h-rezept THEN
        DO:
            ASSIGN
                h-list.cat-nr       = h-rezept.kategorie
                h-list.cat-bezeich  = SUBSTR(h-rezept.bezeich,1,24)
                h-list.cat-name     = SUBSTR(h-rezept.bezeich,25,24)
                h-list.cost-port    = cost1 / h-rezept.portion.
        END.
    END.
    
END.
*/




