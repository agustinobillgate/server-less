DEF INPUT PARAMETER foot1 AS CHAR.
DEF INPUT PARAMETER foot2 AS CHAR.
DEF INPUT PARAMETER foot3 AS CHAR.

RUN update-it. 

PROCEDURE update-it: 
    FIND FIRST paramtext WHERE paramtext.txtnr = 711 EXCLUSIVE-LOCK NO-ERROR. 
    IF AVAILABLE paramtext THEN
    DO:
        paramtext.ptexte = foot1.
        RELEASE paramtext.
    END.       
    FIND FIRST paramtext WHERE paramtext.txtnr = 712 EXCLUSIVE-LOCK NO-ERROR.
    IF AVAILABLE paramtext THEN
    DO:
        paramtext.ptexte = foot2.
        RELEASE paramtext.
    END.
    
    FIND FIRST paramtext WHERE paramtext.txtnr = 713 NO-LOCK NO-ERROR.
    IF NOT AVAILABLE paramtext THEN
    DO:
        CREATE paramtext.
        paramtext.txtnr = 713.
        paramtext.ptexte = foot3.
    END.    
    ELSE
    DO:
        FIND CURRENT paramtext EXCLUSIVE-LOCK.
        paramtext.ptexte = foot3.
        FIND CURRENT paramtext NO-LOCK.
        RELEASE paramtext.
    END.
END. 
