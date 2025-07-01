DEFINE TEMP-TABLE t-setup
    FIELD room      AS CHARACTER
    FIELD setup     AS CHARACTER
    FIELD maxPerson AS INTEGER
    FIELD roomSpace AS INTEGER
    FIELD prepTime  AS INTEGER
    FIELD extention AS CHARACTER.    

/**/    
DEFINE INPUT PARAMETER raum     AS CHARACTER.
DEFINE OUTPUT PARAMETER TABLE FOR t-setup.    
/**/

/*
DEFINE VARIABLE raum    AS CHARACTER    NO-UNDO INITIAL "LRJ".
*/

FOR EACH bk-rset WHERE bk-rset.raum EQ raum:
    FIND FIRST bk-raum WHERE bk-raum.raum EQ bk-rset.raum NO-LOCK NO-ERROR.
    IF AVAILABLE bk-raum THEN
    DO:
        FIND FIRST bk-setup WHERE bk-setup.setup-id eq bk-rset.setup-id NO-LOCK NO-ERROR.
        IF AVAILABLE bk-setup THEN 
        DO:
            CREATE t-setup.
            ASSIGN 
                t-setup.room        = bk-raum.bezeich
                t-setup.setup       = bk-setup.bezeich
                t-setup.maxPerson   = bk-rset.personen
                t-setup.roomSpace   = bk-rset.groesse
                t-setup.prepTime    = bk-rset.vorbereit
                t-setup.extention   = bk-rset.nebenstelle.            
        END.            
    END.    
END.
