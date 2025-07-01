
DEFINE TEMP-TABLE op-list LIKE l-op
    FIELD bezeich LIKE l-artikel.bezeich
    FIELD username LIKE bediener.username.

DEF INPUT PARAMETER TABLE FOR op-list.
DEF INPUT  PARAMETER pvILanguage    AS INTEGER NO-UNDO.
DEF OUTPUT PARAMETER its-ok         AS LOGICAL INITIAL YES. 
DEF OUTPUT PARAMETER msg-str        AS CHAR    NO-UNDO.

DEF BUFFER b-bestand FOR l-bestand.
DEF VARIABLE curr-store AS CHAR NO-UNDO.

{SupertransBL.i} 
DEF VAR lvCAREA AS CHAR INITIAL "s-transform".

FOR EACH op-list:
    FIND FIRST l-bestand WHERE l-bestand.artnr = op-list.artnr 
      AND l-bestand.lager-nr = op-list.lager-nr NO-LOCK. 
    IF NOT AVAILABLE l-bestand THEN DO:
        FIND FIRST l-artikel WHERE l-artikel.artnr = op-list.artnr NO-LOCK. 
        FIND FIRST l-lager WHERE l-lager.lager-nr = op-list.lager-nr NO-LOCK NO-ERROR.

        FIND FIRST b-bestand WHERE b-bestand.artnr = op-list.artnr
            AND b-bestand.lager-nr NE 0 NO-LOCK NO-ERROR.
        IF AVAILABLE b-bestand THEN DO:
             FIND FIRST l-lager WHERE l-lager.lager-nr = op-list.lager-nr NO-LOCK NO-ERROR.
             IF AVAILABLE l-lager THEN curr-store = l-lager.bezeich.
        END.
        msg-str = msg-str + CHR(2)
                  + translateExtended ("Wrong Store: ",lvCAREA,"") 
                  + STRING(l-artikel.artnr) + " - " 
                  + l-artikel.bezeich 
                  + CHR(10)
                  + translateExtended ("Inputted Store =",lvCAREA,"") + " " 
                  + STRING(l-lager.bezeich) 
                  + translateExtended (" - Artikel Store =",lvCAREA,"") + " " 
                  + STRING(curr-store) 
                  + CHR(10)
                  + translateExtended ("POSTING NOT POSSIBLE",lvCAREA,"") .
        its-ok = NO.
        RETURN. 
    END.
END.
