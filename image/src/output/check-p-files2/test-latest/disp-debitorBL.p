&ANALYZE-SUSPEND _VERSION-NUMBER AB_v9r12 GUI ADM1
&ANALYZE-RESUME
/* Connected Databases 
          vhp              PROGRESS
*/
&Scoped-define WINDOW-NAME CURRENT-WINDOW
&Scoped-define FRAME-NAME fMain
&ANALYZE-SUSPEND _UIB-CODE-BLOCK _CUSTOM _DEFINITIONS fMain 

DEFINE TEMP-TABLE dlist
    FIELD gastnr LIKE guest.gastnr FORMAT ">>>>>9"
    FIELD gname  AS CHAR FORMAT "x(36)"
    FIELD city   AS CHAR FORMAT "x(20)"
    FIELD gtype  LIKE guest.karteityp
    FIELD aging  AS DECIMAL FORMAT "->>,>>>,>>>,>>9.99".

DEFINE OUTPUT PARAMETER TABLE FOR dlist.

RUN create-list.


/* **********************  Internal Procedures  *********************** */


&ANALYZE-SUSPEND _UIB-CODE-BLOCK _PROCEDURE create-list fMain 
PROCEDURE create-list :
/*------------------------------------------------------------------------------
  Purpose:     
  Parameters:  <none>
  Notes:       
------------------------------------------------------------------------------*/
FOR EACH dlist:
    DELETE dlist.
END.

DEFINE BUFFER deb-buff FOR debitor.

FOR EACH debitor WHERE debitor.opart LE 1 /*AND debitor.counter = 0*/
    AND debitor.saldo NE 0 NO-LOCK,
    FIRST artikel WHERE artikel.artnr = debitor.artnr AND 
    artikel.artart = 2 AND artikel.departement = 0 NO-LOCK:
    FIND FIRST guest WHERE guest.gastnr = debitor.gastnr NO-LOCK.
    
    FIND FIRST dlist WHERE dlist.gastnr = debitor.gastnr NO-ERROR.
    IF NOT AVAILABLE dlist THEN
    DO:
        CREATE dlist.
        ASSIGN
            dlist.gastnr    = guest.gastnr
            dlist.gname     = guest.NAME + ", " + guest.vorname1 + " " + 
                guest.anrede1 + guest.anredefirma
            dlist.gtype     = guest.karteityp
            dlist.city      = guest.wohnort
            .
    END.
    dlist.aging = dlist.aging + debitor.saldo.
    
    
    /*IF debitor.counter NE 0 THEN
    DO:
        FOR EACH deb-buff WHERE deb-buff.counter = debitor.counter 
            AND RECID(deb-buff) NE RECID(debitor) NO-LOCK:
            dlist.aging = dlist.aging + deb-buff.saldo.
        END.
    END.*/                                      
END.
END PROCEDURE.

/* _UIB-CODE-BLOCK-END */
&ANALYZE-RESUME
