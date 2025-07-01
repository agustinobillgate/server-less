
DEFINE TEMP-TABLE usr 
    FIELD nr    AS INT  
    FIELD NAME  AS CHAR     FORMAT "x(24)"     
    FIELD skill AS CHAR     FORMAT "x(256)".

DEFINE INPUT PARAMETER dept-nr      AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR usr.

DEFINE BUFFER usr1 FOR eg-staff.

RUN create-user.


PROCEDURE create-user:

    DEF VAR a AS CHAR NO-UNDO.
    DEF VAR i AS INTEGER.
    DEF VAR j AS CHAR.
    DEF VAR c AS CHAR.
    DEF VAR curr-num AS INTEGER.

    FOR EACH usr :
        DELETE usr.
    END.

    /*FDL: #689 add NO-LOCK & Add curr-num*/ 
    FOR EACH usr1 WHERE usr1.usergroup = dept-nr AND usr1.activeflag = YES NO-LOCK:
        a =  usr1.skill.
        IF a NE "" THEN
        DO:
            DO i = 1 TO NUM-ENTRIES(a, ";"):
                j = ENTRY (i , a , ";" ).
                curr-num = INT(j).
                FIND FIRST queasy WHERE queasy.KEY = 132 AND queasy.number1 = curr-num NO-LOCK NO-ERROR.
                IF AVAILABLE queasy THEN
                DO:
                    IF c = "" THEN
                        c = queasy.char1.
                    ELSE
                        c = c + "," + queasy.char1. 
                END. 
            END.
        END.
        ELSE
        DO:
            c = "".
        END.

        CREATE usr.
        ASSIGN usr.nr   = usr1.nr
               usr.NAME = usr1.NAME
               usr.skill =  c.
        c = "".    
    END.
END.
