
/**/
DEFINE INPUT  PARAMETER resnr AS INT.
DEFINE OUTPUT PARAMETER counter AS INT.
/**/
/*
DEFINE VARIABLE resnr AS INT INITIAL 07/13/2023.
DEFINE VARIABLE counter AS INT.
*/

DEFINE VARIABLE new-status AS CHAR INIT "".
counter = 0.

FOR EACH res-line WHERE res-line.resnr = resnr 
        AND res-line.resstatus NE 11
        AND res-line.resstatus NE 13
        AND res-line.l-zuordnung[3] = 0 :

    IF res-line.resstatus LE 5 THEN
        ASSIGN
            new-status = "new".
    IF res-line.resstatus = 6 OR res-line.resstatus = 8 THEN
        ASSIGN
            new-status = "modify".
    IF res-line.resstatus = 9 OR res-line.resstatus = 99 OR res-line.resstatus = 10 THEN
        ASSIGN
            new-status = "cancel".
    
    /* generate trigger as daily XML file */
    DO TRANSACTION.
        CREATE interface.
        ASSIGN
            interface.key         = 10
            interface.zinr        = res-line.zinr
            interface.nebenstelle = ""
            interface.intfield    = 0
            interface.decfield    = 1
            interface.int-time    = TIME
            interface.intdate     = TODAY
            interface.parameters  = new-status
            interface.resnr       = res-line.resnr
            interface.reslinnr    = res-line.reslinnr
            counter               = counter + 1
        .
        FIND CURRENT interface NO-LOCK.
        RELEASE interface.
    END.

END.

