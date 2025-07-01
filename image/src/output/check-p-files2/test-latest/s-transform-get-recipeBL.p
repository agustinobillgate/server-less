
DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD bezeich LIKE l-artikel.bezeich
    FIELD username LIKE bediener.username.
DEFINE TEMP-TABLE t-op-list LIKE op-list.



DEFINE INPUT PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER hrecipe-nr     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER qty            AS DECIMAL NO-UNDO.
DEFINE INPUT PARAMETER curr-lager     AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER transdate      AS DATE    NO-UNDO.
DEFINE INPUT PARAMETER bediener-nr    AS INTEGER NO-UNDO.
DEFINE INPUT PARAMETER lscheinnr   LIKE l-op.lscheinnr.
DEFINE INPUT-OUTPUT PARAMETER TABLE FOR t-op-list.
DEFINE OUTPUT PARAMETER err-flag   AS INTEGER NO-UNDO. 
DEFINE OUTPUT PARAMETER msg-str    AS CHAR    NO-UNDO.



DEFINE VARIABLE anzahl    AS DECIMAL FORMAT "->,>>>,>>9.999". 
DEFINE VARIABLE stock-oh  AS DECIMAL NO-UNDO.
DEFINE VARIABLE t-logical AS LOGICAL NO-UNDO.
DEFINE BUFFER sys-user FOR bediener. 

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "s-transform".


DEFINE BUFFER brezept FOR h-rezept.
DEFINE BUFFER brezlin FOR h-rezlin.


FIND FIRST htparam WHERE htparam.paramnr = 232 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN t-logical = htparam.flogical.

IF t-logical THEN DO:
    ASSIGN err-flag = 3.
    RETURN.
END.

FIND FIRST h-rezept WHERE h-rezept.artnrrezept = hrecipe-nr NO-LOCK NO-ERROR.
IF AVAILABLE h-rezept THEN DO:
    FOR EACH h-rezlin WHERE h-rezlin.artnrrezept = hrecipe-nr NO-LOCK:

        IF h-rezlin.recipe-flag = YES THEN RUN create-op(h-rezlin.artnrlager, h-rezlin.menge).
        ELSE DO:
            FIND FIRST l-artikel WHERE l-artikel.artnr = h-rezlin.artnrlager NO-LOCK NO-ERROR. 
            IF AVAILABLE l-artikel THEN DO:
                
                anzahl = qty * ((1 * h-rezlin.menge / h-rezept.portion) / l-artikel.inhalt).
                IF anzahl = 0 THEN DO:
                    ASSIGN err-flag = 1.
                    RETURN.               
                END.
                ELSE IF anzahl LT 0 THEN DO:
                    ASSIGN err-flag = 2.
                    RETURN.               
                END.
                ELSE DO:
                    FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
                            AND l-bestand.artnr = h-rezlin.artnrlager NO-LOCK NO-ERROR. 
                    IF AVAILABLE l-bestand THEN DO:
                        stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                                   - l-bestand.anz-ausgang.                     
                    END.
                    IF anzahl GT stock-oh THEN DO:
                        ASSIGN msg-str = msg-str + CHR(2)
                              + translateExtended ("Wrong quantity: ",lvCAREA ,"") 
                              + STRING(l-artikel.artnr) + " - " 
                              + l-artikel.bezeich 
                              + CHR(10)
                              + translateExtended ("Inputted quantity =",lvCAREA,"") + " " 
                              + STRING(anzahl, "->>>,>>>9.99") 
                              + translateExtended (" - Stock onhand =",lvCAREA,"") + " " 
                              + STRING(stock-oh, "->>>,>>>9.99") 
                              + CHR(10)
                              + translateExtended (" From Recipe No =",lvCAREA,"") + " " 
                              + STRING(h-rezlin.artnrrezept, ">>>>>>>>9") 
                              + CHR(10)
                              + translateExtended ("POSTING NOT POSSIBLE",lvCAREA,"") .
                        RETURN. 
                    END.
                END.
                
                CREATE op-list.
                ASSIGN 
                    op-list.datum           = transdate
                    op-list.lager-nr        = curr-lager 
                    op-list.artnr           = h-rezlin.artnrlager 
                    op-list.zeit            = TIME 
                    op-list.anzahl          = anzahl 
                    op-list.einzelpreis     = l-artikel.vk-preis 
                    op-list.warenwert       = anzahl * l-artikel.vk-preis 
                    op-list.op-art          = 4 
                    op-list.herkunftflag    = 3    /* 1 = regular, 4 = inventory !!! */ 
                    op-list.lscheinnr       = lscheinnr 
                    op-list.fuellflag       = bediener-nr 
                    op-list.pos             = 1
                    op-list.bezeich         = l-artikel.bezeich.
            END.

        END.        
    END.
END.

FOR EACH op-list:
    FIND FIRST sys-user WHERE sys-user.nr = op-list.fuellflag 
        NO-LOCK NO-ERROR.
    CREATE t-op-list.
    BUFFER-COPY op-list TO t-op-list.
    ASSIGN t-op-list.username = sys-user.username.
END.


PROCEDURE create-op:
    DEFINE INPUT PARAMETER recipe-no AS INTEGER NO-UNDO.
    DEFINE INPUT PARAMETER menge     AS DECIMAL NO-UNDO.

    FIND FIRST brezept WHERE brezept.artnrrezept = recipe-no NO-LOCK NO-ERROR.
    IF AVAILABLE brezept THEN DO:
        FOR EACH brezlin WHERE brezlin.artnrrezept = recipe-no NO-LOCK:
            IF brezlin.recipe-flag = YES THEN RUN create-op(brezlin.artnrlager, brezlin.menge).
            ELSE DO:

                FIND FIRST l-artikel WHERE l-artikel.artnr = brezlin.artnrlager NO-LOCK NO-ERROR. 
                IF AVAILABLE l-artikel THEN DO:
                    
                    anzahl = qty * (menge * ((1 * brezlin.menge / brezept.portion) / l-artikel.inhalt)).
                    IF anzahl = 0 THEN DO:
                        ASSIGN err-flag = 1.
                        RETURN.               
                    END.
                    ELSE IF anzahl LT 0 THEN DO:
                        ASSIGN err-flag = 2.
                        RETURN.               
                    END.
                    ELSE DO:
                        FIND FIRST l-bestand WHERE l-bestand.lager-nr = curr-lager 
                                AND l-bestand.artnr = brezlin.artnrlager NO-LOCK NO-ERROR. 
                        IF AVAILABLE l-bestand THEN DO:
                            stock-oh = l-bestand.anz-anf-best + l-bestand.anz-eingang 
                                       - l-bestand.anz-ausgang.                     
                        END.
                        IF anzahl GT stock-oh THEN DO:
                            ASSIGN msg-str = msg-str + CHR(2)
                                  + translateExtended ("Wrong quantity: ",lvCAREA ,"") 
                                  + STRING(l-artikel.artnr) + " - " 
                                  + l-artikel.bezeich 
                                  + CHR(10)
                                  + translateExtended ("Inputted quantity =",lvCAREA,"") + " " 
                                  + STRING(anzahl, "->>>,>>>9.99") 
                                  + translateExtended (" - Stock onhand =",lvCAREA,"") + " " 
                                  + STRING(stock-oh, "->>>,>>>9.99") 
                                  + CHR(10)
                                  + translateExtended (" From Recipe No =",lvCAREA,"") + " " 
                                  + STRING(brezlin.artnrrezept, ">>>>>>>>9") 
                                  + CHR(10)
                                  + translateExtended ("POSTING NOT POSSIBLE",lvCAREA,"") .
                            RETURN. 
                        END.
                    END.
                    
                    CREATE op-list.
                    ASSIGN 
                        op-list.datum           = transdate
                        op-list.lager-nr        = curr-lager 
                        op-list.artnr           = brezlin.artnrlager 
                        op-list.zeit            = TIME 
                        op-list.anzahl          = anzahl 
                        op-list.einzelpreis     = l-artikel.vk-preis 
                        op-list.warenwert       = anzahl * l-artikel.vk-preis 
                        op-list.op-art          = 4 
                        op-list.herkunftflag    = 3    /* 1 = regular, 4 = inventory !!! */ 
                        op-list.lscheinnr       = lscheinnr 
                        op-list.fuellflag       = bediener-nr 
                        op-list.pos             = 1
                        op-list.bezeich         = l-artikel.bezeich.
                END.
            END.
        END.
    END.
END.


