
DEF INPUT PARAMETER closedate AS DATE.

FIND FIRST l-ophdr WHERE (op-typ = "STI" OR op-typ = "STT" OR op-typ = "WIP") 
    AND l-ophdr.datum LE closedate NO-LOCK NO-ERROR. 
DO TRANSACTION WHILE AVAILABLE l-ophdr: 
    FIND CURRENT l-ophdr EXCLUSIVE-LOCK. 
    RUN create-ophhis. 
    DELETE l-ophdr. 
    FIND NEXT l-ophdr WHERE (op-typ = "STI" OR op-typ = "STT" OR op-typ = "WIP")
        AND l-ophdr.datum LE closedate NO-LOCK NO-ERROR.
END.

PROCEDURE create-ophhis: 

    /*MTIF CONNECTED ("vhparch") THEN
    DO:
        RUN closeinv-arch.p('cr-ophhis', RECID(l-ophdr), datum).
    END.
    ELSE
    DO:*/
        CREATE vhp.l-ophhis. 
        ASSIGN
            vhp.l-ophhis.datum      = l-ophdr.datum
            vhp.l-ophhis.op-typ     = l-ophdr.op-typ 
            vhp.l-ophhis.docu-nr    = l-ophdr.docu-nr 
            vhp.l-ophhis.lscheinnr  = l-ophdr.lscheinnr 
            vhp.l-ophhis.fibukonto  = l-ophdr.fibukonto
            . 
        FIND CURRENT vhp.l-ophhis NO-LOCK. 
    /*MTEND.*/
END. 
