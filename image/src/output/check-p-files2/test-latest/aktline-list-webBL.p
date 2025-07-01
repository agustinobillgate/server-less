
DEFINE TEMP-TABLE aktline-list
  FIELD bezeich     AS CHAR
  FIELD datum       AS DATE
  FIELD zeit        AS INTEGER
  FIELD dauer       AS INTEGER
  FIELD prioritaet  AS INTEGER
  FIELD kontakt     AS CHAR
  FIELD NAME        AS CHAR
  FIELD address     AS CHAR
  FIELD regard      AS CHAR
  FIELD userinit    AS CHAR
  FIELD linenr      AS INTEGER
  FIELD telefon     AS CHAR
  FIELD fax         AS CHAR
  FIELD bemerk      AS CHAR
  FIELD email       AS CHAR
  FIELD username    AS CHAR
  FIELD ftime       AS CHARACTER
  FIELD ttime       AS CHARACTER
  FIELD priority    AS CHARACTER
  FIELD gastnr      AS INTEGER
  FIELD guest-type  AS INTEGER.


DEFINE INPUT PARAMETER inp-gastnr AS INTEGER    NO-UNDO.
DEFINE INPUT PARAMETER next-date  AS DATE       NO-UNDO.
DEFINE INPUT PARAMETER all-flag   AS LOGICAL    NO-UNDO.
DEFINE INPUT PARAMETER prior      AS INTEGER    NO-UNDO.
DEFINE INPUT PARAMETER act-combo  AS CHAR       NO-UNDO.
DEFINE INPUT PARAMETER acttype    AS INTEGER    NO-UNDO.
DEFINE INPUT PARAMETER user-init  AS CHAR. 
DEFINE INPUT PARAMETER to-date  AS DATE         NO-UNDO.
DEFINE OUTPUT PARAMETER TABLE FOR aktline-list.

DEFINE VARIABLE prioritaet AS CHAR EXTENT 3.
prioritaet[1] = "Low".
prioritaet[2] = "Medium".
prioritaet[3] = "High".

/*************** MAIN LOGIC ***************/
IF inp-gastnr NE 0 THEN
DO:
  IF next-date = ? THEN 
     RUN disp-all2. 
  ELSE RUN disp-it2. 
END.
ELSE
DO:
  IF next-date = ? THEN 
     RUN disp-all. 
  ELSE RUN disp-it. 
END.


/*************** PROCEDURE ***************/
PROCEDURE disp-all:
  IF all-flag THEN 
  DO:
    IF prior = 0 THEN
    DO:
        IF act-combo = "ALL"  THEN
        FOR EACH akt-line WHERE akt-line.flag = acttype NO-LOCK,
          FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
          FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
          FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
          BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

            CREATE aktline-list.
            ASSIGN
              aktline-list.bezeich     = akt-code.bezeich
              aktline-list.datum       = akt-line.datum
              aktline-list.zeit        = akt-line.zeit
              aktline-list.dauer       = akt-line.dauer
              aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM")
              aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
              aktline-list.prioritaet  = akt-line.prioritaet
              aktline-list.kontakt     = akt-line.kontakt 
              aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
              aktline-list.regard      = akt-line.regard
              aktline-list.userinit        = akt-line.userinit
              aktline-list.linenr      = akt-line.linenr
              aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
              aktline-list.telefon     = guest.telefon
              aktline-list.fax         = guest.fax
              aktline-list.bemerk      = akt-line.bemerk
              aktline-list.username    = bediener.username
              aktline-list.gastnr      = akt-line.gastnr
              aktline-list.guest-type  = guest.karteityp.
              FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND
                  akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
              IF AVAILABLE akt-kont THEN
              DO:
                aktline-list.email    = akt-kont.email.
              END.   
              aktline-list.priority   = prioritaet[aktline-list.prioritaet].
        END.
        ELSE
        FOR EACH akt-line WHERE akt-line.flag = acttype NO-LOCK,
          FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
            akt-code.bezeich = act-combo NO-LOCK,
          FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
          FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
          BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

            CREATE aktline-list.
            ASSIGN
              aktline-list.bezeich     = akt-code.bezeich
              aktline-list.datum       = akt-line.datum
              aktline-list.zeit        = akt-line.zeit
              aktline-list.dauer       = akt-line.dauer
              aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
              aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
              aktline-list.prioritaet  = akt-line.prioritaet
              aktline-list.kontakt     = akt-line.kontakt 
              aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
              aktline-list.regard      = akt-line.regard
              aktline-list.userinit        = akt-line.userinit
              aktline-list.linenr      = akt-line.linenr
              aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
              aktline-list.telefon     = guest.telefon
              aktline-list.fax         = guest.fax
              aktline-list.bemerk      = akt-line.bemerk
              aktline-list.username    = bediener.username
              aktline-list.gastnr      = akt-line.gastnr
              aktline-list.guest-type  = guest.karteityp.
            FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
            IF AVAILABLE akt-kont THEN
            DO:
                aktline-list.email    = akt-kont.email.
            END.
            aktline-list.priority   = prioritaet[aktline-list.prioritaet].
        END.
    END.
    ELSE
    DO:
        IF act-combo = "ALL"  THEN
        FOR EACH akt-line WHERE akt-line.flag = acttype
          AND akt-line.prioritaet = prior NO-LOCK,
          FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
          FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
          FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
          BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

            CREATE aktline-list.
            ASSIGN
              aktline-list.bezeich     = akt-code.bezeich
              aktline-list.datum       = akt-line.datum
              aktline-list.zeit        = akt-line.zeit
              aktline-list.dauer       = akt-line.dauer
              aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
              aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
              aktline-list.prioritaet  = akt-line.prioritaet
              aktline-list.kontakt     = akt-line.kontakt 
              aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
              aktline-list.regard      = akt-line.regard
              aktline-list.userinit        = akt-line.userinit
              aktline-list.linenr      = akt-line.linenr
              aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
              aktline-list.telefon     = guest.telefon
              aktline-list.fax         = guest.fax
              aktline-list.bemerk      = akt-line.bemerk
              aktline-list.username    = bediener.username
              aktline-list.gastnr      = akt-line.gastnr
              aktline-list.guest-type  = guest.karteityp.
            FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
            IF AVAILABLE akt-kont THEN
            DO:
                aktline-list.email    = akt-kont.email.
            END.
            aktline-list.priority   = prioritaet[aktline-list.prioritaet].
        END.
        ELSE
        FOR EACH akt-line WHERE akt-line.flag = acttype
            AND akt-line.prioritaet = prior NO-LOCK,
          FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
            akt-code.bezeich = act-combo NO-LOCK,
          FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
          FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
          BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

            CREATE aktline-list.
            ASSIGN
              aktline-list.bezeich     = akt-code.bezeich
              aktline-list.datum       = akt-line.datum
              aktline-list.zeit        = akt-line.zeit
              aktline-list.dauer       = akt-line.dauer
              aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
              aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
              aktline-list.prioritaet  = akt-line.prioritaet
              aktline-list.kontakt     = akt-line.kontakt 
              aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
              aktline-list.regard      = akt-line.regard
              aktline-list.userinit        = akt-line.userinit
              aktline-list.linenr      = akt-line.linenr
              aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
              aktline-list.telefon     = guest.telefon
              aktline-list.fax         = guest.fax
              aktline-list.bemerk      = akt-line.bemerk
              aktline-list.username    = bediener.username
              aktline-list.gastnr      = akt-line.gastnr
              aktline-list.guest-type  = guest.karteityp.
            FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
            IF AVAILABLE akt-kont THEN
            DO:
                aktline-list.email    = akt-kont.email.
            END.
            aktline-list.priority   = prioritaet[aktline-list.prioritaet].
        END.
    END.
  END.
  ELSE
  DO:                  
      IF prior = 0 THEN
      DO:
          IF act-combo = "ALL"  THEN
          FOR EACH akt-line WHERE akt-line.flag = acttype AND 
            akt-line.userinit = user-init NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

                CREATE aktline-list.
                ASSIGN
                  aktline-list.bezeich     = akt-code.bezeich
                  aktline-list.datum       = akt-line.datum
                  aktline-list.zeit        = akt-line.zeit
                  aktline-list.dauer       = akt-line.dauer
                  aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                  aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                  aktline-list.prioritaet  = akt-line.prioritaet
                  aktline-list.kontakt     = akt-line.kontakt 
                  aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                  aktline-list.regard      = akt-line.regard
                  aktline-list.userinit        = akt-line.userinit
                  aktline-list.linenr      = akt-line.linenr
                  aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                  aktline-list.telefon     = guest.telefon
                  aktline-list.fax         = guest.fax
                  aktline-list.bemerk      = akt-line.bemerk
                  aktline-list.username    = bediener.username
                  aktline-list.gastnr      = akt-line.gastnr
                  aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                    aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
          ELSE
          FOR EACH akt-line WHERE akt-line.flag = acttype AND 
            akt-line.userinit = user-init NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
              akt-code.bezeich = act-combo NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

                CREATE aktline-list.
                ASSIGN
                  aktline-list.bezeich     = akt-code.bezeich
                  aktline-list.datum       = akt-line.datum
                  aktline-list.zeit        = akt-line.zeit
                  aktline-list.dauer       = akt-line.dauer
                  aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                  aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                  aktline-list.prioritaet  = akt-line.prioritaet
                  aktline-list.kontakt     = akt-line.kontakt 
                  aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                  aktline-list.regard      = akt-line.regard
                  aktline-list.userinit        = akt-line.userinit
                  aktline-list.linenr      = akt-line.linenr
                  aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                  aktline-list.telefon     = guest.telefon
                  aktline-list.fax         = guest.fax
                  aktline-list.bemerk      = akt-line.bemerk
                  aktline-list.username    = bediener.username
                  aktline-list.gastnr      = akt-line.gastnr
                  aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                    aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
     END.
     ELSE
     DO:
         IF act-combo = "ALL"  THEN
          FOR EACH akt-line WHERE akt-line.flag = acttype AND 
            akt-line.userinit = user-init AND akt-line.prioritaet = prior NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

                CREATE aktline-list.
                ASSIGN
                  aktline-list.bezeich     = akt-code.bezeich
                  aktline-list.datum       = akt-line.datum
                  aktline-list.zeit        = akt-line.zeit
                  aktline-list.dauer       = akt-line.dauer
                  aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                  aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                  aktline-list.prioritaet  = akt-line.prioritaet
                  aktline-list.kontakt     = akt-line.kontakt 
                  aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                  aktline-list.regard      = akt-line.regard
                  aktline-list.userinit        = akt-line.userinit
                  aktline-list.linenr      = akt-line.linenr
                  aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                  aktline-list.telefon     = guest.telefon
                  aktline-list.fax         = guest.fax
                  aktline-list.bemerk      = akt-line.bemerk
                  aktline-list.username    = bediener.username
                  aktline-list.gastnr      = akt-line.gastnr
                  aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                    aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
         END.
          ELSE
          FOR EACH akt-line WHERE akt-line.flag = acttype AND 
            akt-line.userinit = user-init AND akt-line.prioritaet = prior NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
              akt-code.bezeich = act-combo NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

                CREATE aktline-list.
                ASSIGN
                  aktline-list.bezeich     = akt-code.bezeich
                  aktline-list.datum       = akt-line.datum
                  aktline-list.zeit        = akt-line.zeit
                  aktline-list.dauer       = akt-line.dauer
                  aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                  aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                  aktline-list.prioritaet  = akt-line.prioritaet
                  aktline-list.kontakt     = akt-line.kontakt 
                  aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                  aktline-list.regard      = akt-line.regard
                  aktline-list.userinit        = akt-line.userinit
                  aktline-list.linenr      = akt-line.linenr
                  aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                  aktline-list.telefon     = guest.telefon
                  aktline-list.fax         = guest.fax
                  aktline-list.bemerk      = akt-line.bemerk
                  aktline-list.username    = bediener.username
                  aktline-list.gastnr      = akt-line.gastnr
                  aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                    aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
     END.
  END.
END.

PROCEDURE disp-all2:
   DO:
      IF all-flag THEN 
      DO:
        IF act-combo = "ALL"  THEN
        FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.gastnr = inp-gastnr NO-LOCK,
          FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
          FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
          FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
          BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

            CREATE aktline-list.
            ASSIGN
              aktline-list.bezeich     = akt-code.bezeich
              aktline-list.datum       = akt-line.datum
              aktline-list.zeit        = akt-line.zeit
              aktline-list.dauer       = akt-line.dauer
              aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
              aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
              aktline-list.prioritaet  = akt-line.prioritaet
              aktline-list.kontakt     = akt-line.kontakt 
              aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
              aktline-list.regard      = akt-line.regard
              aktline-list.userinit        = akt-line.userinit
              aktline-list.linenr      = akt-line.linenr
              aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
              aktline-list.telefon     = guest.telefon
              aktline-list.fax         = guest.fax
              aktline-list.bemerk      = akt-line.bemerk
              aktline-list.username    = bediener.username
              aktline-list.gastnr      = akt-line.gastnr
              aktline-list.guest-type  = guest.karteityp.
            FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
            IF AVAILABLE akt-kont THEN
            DO:
                aktline-list.email    = akt-kont.email.
            END.
            aktline-list.priority   = prioritaet[aktline-list.prioritaet].
        END.
        ELSE 
        FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.gastnr = inp-gastnr NO-LOCK,
          FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
            akt-code.bezeich = act-combo NO-LOCK,
          FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
          FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
          BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

            CREATE aktline-list.
            ASSIGN
              aktline-list.bezeich     = akt-code.bezeich
              aktline-list.datum       = akt-line.datum
              aktline-list.zeit        = akt-line.zeit
              aktline-list.dauer       = akt-line.dauer
              aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
              aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
              aktline-list.prioritaet  = akt-line.prioritaet
              aktline-list.kontakt     = akt-line.kontakt 
              aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
              aktline-list.regard      = akt-line.regard
              aktline-list.userinit        = akt-line.userinit
              aktline-list.linenr      = akt-line.linenr
              aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
              aktline-list.telefon     = guest.telefon
              aktline-list.fax         = guest.fax
              aktline-list.bemerk      = akt-line.bemerk
              aktline-list.username    = bediener.username
              aktline-list.gastnr      = akt-line.gastnr
              aktline-list.guest-type  = guest.karteityp.
            FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
            IF AVAILABLE akt-kont THEN
            DO:
                aktline-list.email    = akt-kont.email.
            END.
            aktline-list.priority   = prioritaet[aktline-list.prioritaet].
        END.
      END.
      ELSE
      DO:
          IF act-combo = "ALL"  THEN
          FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.userinit = user-init AND akt-line.gastnr = inp-gastnr NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

                CREATE aktline-list.
                ASSIGN
                  aktline-list.bezeich     = akt-code.bezeich
                  aktline-list.datum       = akt-line.datum
                  aktline-list.zeit        = akt-line.zeit
                  aktline-list.dauer       = akt-line.dauer
                  aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                  aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                  aktline-list.prioritaet  = akt-line.prioritaet
                  aktline-list.kontakt     = akt-line.kontakt 
                  aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                  aktline-list.regard      = akt-line.regard
                  aktline-list.userinit        = akt-line.userinit
                  aktline-list.linenr      = akt-line.linenr
                  aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                  aktline-list.telefon     = guest.telefon
                  aktline-list.fax         = guest.fax
                  aktline-list.bemerk      = akt-line.bemerk
                  aktline-list.username    = bediener.username
                  aktline-list.gastnr      = akt-line.gastnr
                  aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                    akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                    aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
          ELSE 
          FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.userinit = user-init AND 
              akt-line.gastnr = inp-gastnr NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
            akt-code.bezeich = act-combo NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

                CREATE aktline-list.
                ASSIGN
                  aktline-list.bezeich     = akt-code.bezeich
                  aktline-list.datum       = akt-line.datum
                  aktline-list.zeit        = akt-line.zeit
                  aktline-list.dauer       = akt-line.dauer
                  aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                  aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                  aktline-list.prioritaet  = akt-line.prioritaet
                  aktline-list.kontakt     = akt-line.kontakt 
                  aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                  aktline-list.regard      = akt-line.regard
                  aktline-list.userinit        = akt-line.userinit
                  aktline-list.linenr      = akt-line.linenr
                  aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                  aktline-list.telefon     = guest.telefon
                  aktline-list.fax         = guest.fax
                  aktline-list.bemerk      = akt-line.bemerk
                  aktline-list.username    = bediener.username
                  aktline-list.gastnr      = akt-line.gastnr
                  aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                    akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                    aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
      END.
   END.
END.


PROCEDURE disp-it:
   DO:
      IF all-flag THEN 
      DO:
          IF prior = 0 THEN
          DO:
            IF act-combo = "ALL"  THEN
            FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.datum GE next-date
              AND akt-line.datum LE to-date NO-LOCK,
              FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
              FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
              FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
              BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

                CREATE aktline-list.
                ASSIGN
                    aktline-list.bezeich     = akt-code.bezeich
                    aktline-list.datum       = akt-line.datum
                    aktline-list.zeit        = akt-line.zeit
                    aktline-list.dauer       = akt-line.dauer
                    aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                    aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                    aktline-list.prioritaet  = akt-line.prioritaet
                    aktline-list.kontakt     = akt-line.kontakt 
                    aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                    aktline-list.regard      = akt-line.regard
                    aktline-list.userinit        = akt-line.userinit
                    aktline-list.linenr      = akt-line.linenr
                    aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                    aktline-list.telefon     = guest.telefon
                    aktline-list.fax         = guest.fax
                    aktline-list.bemerk      = akt-line.bemerk
                    aktline-list.username    = bediener.username
                    aktline-list.gastnr      = akt-line.gastnr
                    aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                    akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                    aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
            END.
            ELSE 
            FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.datum GE next-date
              AND akt-line.datum LE to-date NO-LOCK,
              FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
                akt-code.bezeich = act-combo NO-LOCK,
              FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
              FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
              BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

            CREATE aktline-list.
            ASSIGN
              aktline-list.bezeich     = akt-code.bezeich
              aktline-list.datum       = akt-line.datum
              aktline-list.zeit        = akt-line.zeit
              aktline-list.dauer       = akt-line.dauer
              aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
              aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
              aktline-list.prioritaet  = akt-line.prioritaet
              aktline-list.kontakt     = akt-line.kontakt 
              aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
              aktline-list.regard      = akt-line.regard
              aktline-list.userinit        = akt-line.userinit
              aktline-list.linenr      = akt-line.linenr
              aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
              aktline-list.telefon     = guest.telefon
              aktline-list.fax         = guest.fax
              aktline-list.bemerk      = akt-line.bemerk
              aktline-list.username    = bediener.username
              aktline-list.gastnr      = akt-line.gastnr
              aktline-list.guest-type  = guest.karteityp.
              FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                  akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
              IF AVAILABLE akt-kont THEN
              DO:
                  aktline-list.email    = akt-kont.email.
              END.
              aktline-list.priority   = prioritaet[aktline-list.prioritaet].
            END.
         END.
         ELSE
         DO:
             IF act-combo = "ALL"  THEN
            FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.datum GE next-date
              AND akt-line.datum LE to-date AND akt-line.prioritaet = prior NO-LOCK,
              FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
              FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
              FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
              BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:

                CREATE aktline-list.
                ASSIGN
                  aktline-list.bezeich     = akt-code.bezeich
                  aktline-list.datum       = akt-line.datum
                  aktline-list.zeit        = akt-line.zeit
                  aktline-list.dauer       = akt-line.dauer
                  aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                  aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                  aktline-list.prioritaet  = akt-line.prioritaet
                  aktline-list.kontakt     = akt-line.kontakt 
                  aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                  aktline-list.regard      = akt-line.regard
                  aktline-list.userinit        = akt-line.userinit
                  aktline-list.linenr      = akt-line.linenr
                  aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                  aktline-list.telefon     = guest.telefon
                  aktline-list.fax         = guest.fax
                  aktline-list.bemerk      = akt-line.bemerk
                  aktline-list.username    = bediener.username
                  aktline-list.gastnr      = akt-line.gastnr
                  aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                  akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                  aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
             END.
            ELSE 
            FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.datum GE next-date
              AND akt-line.datum LE to-date AND akt-line.prioritaet = prior NO-LOCK,
              FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
                akt-code.bezeich = act-combo NO-LOCK,
              FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
              FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
              BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:
                CREATE aktline-list.
                ASSIGN
                  aktline-list.bezeich     = akt-code.bezeich
                  aktline-list.datum       = akt-line.datum
                  aktline-list.zeit        = akt-line.zeit
                  aktline-list.dauer       = akt-line.dauer
                  aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                  aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                  aktline-list.prioritaet  = akt-line.prioritaet
                  aktline-list.kontakt     = akt-line.kontakt 
                  aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                  aktline-list.regard      = akt-line.regard
                  aktline-list.userinit        = akt-line.userinit
                  aktline-list.linenr      = akt-line.linenr
                  aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                  aktline-list.telefon     = guest.telefon
                  aktline-list.fax         = guest.fax
                  aktline-list.bemerk      = akt-line.bemerk
                  aktline-list.username    = bediener.username
                  aktline-list.gastnr      = akt-line.gastnr
                  aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                  akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                  aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
            END.
         END.
      END.
      ELSE
      DO:
        IF prior = 0 THEN
        DO:
          IF act-combo = "ALL"  THEN
          FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.userinit = user-init AND akt-line.datum GE next-date
            AND akt-line.datum LE to-date NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode  NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:
              CREATE aktline-list.
              ASSIGN
                  aktline-list.bezeich     = akt-code.bezeich
                  aktline-list.datum       = akt-line.datum
                  aktline-list.zeit        = akt-line.zeit
                  aktline-list.dauer       = akt-line.dauer
                  aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                  aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                  aktline-list.prioritaet  = akt-line.prioritaet
                  aktline-list.kontakt     = akt-line.kontakt 
                  aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                  aktline-list.regard      = akt-line.regard
                  aktline-list.userinit        = akt-line.userinit
                  aktline-list.linenr      = akt-line.linenr
                  aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                  aktline-list.telefon     = guest.telefon
                  aktline-list.fax         = guest.fax
                  aktline-list.bemerk      = akt-line.bemerk
                  aktline-list.username    = bediener.username
                  aktline-list.gastnr      = akt-line.gastnr
                  aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                  akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                  aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
          ELSE 
          FOR EACH akt-line WHERE akt-line.flag = acttype 
            AND akt-line.userinit = user-init AND akt-line.datum GE next-date
            AND akt-line.datum LE to-date NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
            akt-code.bezeich = act-combo NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:
              CREATE aktline-list.
              ASSIGN
                aktline-list.bezeich     = akt-code.bezeich
                aktline-list.datum       = akt-line.datum
                aktline-list.zeit        = akt-line.zeit
                aktline-list.dauer       = akt-line.dauer
                aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                aktline-list.prioritaet  = akt-line.prioritaet
                aktline-list.kontakt     = akt-line.kontakt 
                aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                aktline-list.regard      = akt-line.regard
                aktline-list.userinit        = akt-line.userinit
                aktline-list.linenr      = akt-line.linenr
                aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                aktline-list.telefon     = guest.telefon
                aktline-list.fax         = guest.fax
                aktline-list.bemerk      = akt-line.bemerk
                aktline-list.username    = bediener.username
                aktline-list.gastnr      = akt-line.gastnr
                aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                  akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                  aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
        END.
        ELSE
        DO:
          IF act-combo = "ALL"  THEN
          FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.userinit = user-init AND akt-line.datum GE next-date
            AND akt-line.datum LE to-date AND akt-line.prioritaet = prior NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode  NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:
              CREATE aktline-list.
              ASSIGN
                aktline-list.bezeich     = akt-code.bezeich
                aktline-list.datum       = akt-line.datum
                aktline-list.zeit        = akt-line.zeit
                aktline-list.dauer       = akt-line.dauer
                aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                aktline-list.prioritaet  = akt-line.prioritaet
                aktline-list.kontakt     = akt-line.kontakt 
                aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                aktline-list.regard      = akt-line.regard
                aktline-list.userinit        = akt-line.userinit
                aktline-list.linenr      = akt-line.linenr
                aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                aktline-list.telefon     = guest.telefon
                aktline-list.fax         = guest.fax
                aktline-list.bemerk      = akt-line.bemerk
                aktline-list.username    = bediener.username
                aktline-list.gastnr      = akt-line.gastnr
                aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                  akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                  aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
          ELSE 
          FOR EACH akt-line WHERE akt-line.flag = acttype 
            AND akt-line.userinit = user-init AND akt-line.datum GE next-date
            AND akt-line.datum LE to-date AND akt-line.prioritaet = prior NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
            akt-code.bezeich = act-combo NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:
              CREATE aktline-list.
              ASSIGN
                aktline-list.bezeich     = akt-code.bezeich
                aktline-list.datum       = akt-line.datum
                aktline-list.zeit        = akt-line.zeit
                aktline-list.dauer       = akt-line.dauer
                aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                aktline-list.prioritaet  = akt-line.prioritaet
                aktline-list.kontakt     = akt-line.kontakt 
                aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                aktline-list.regard      = akt-line.regard
                aktline-list.userinit        = akt-line.userinit
                aktline-list.linenr      = akt-line.linenr
                aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                aktline-list.telefon     = guest.telefon
                aktline-list.fax         = guest.fax
                aktline-list.bemerk      = akt-line.bemerk
                aktline-list.username    = bediener.username
                aktline-list.gastnr      = akt-line.gastnr
                aktline-list.guest-type  = guest.karteityp.
                FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                  akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
                IF AVAILABLE akt-kont THEN
                DO:
                  aktline-list.email    = akt-kont.email.
                END.
                aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
        END.
      END.
   END.
END.

PROCEDURE disp-it2:
   DO:
      IF all-flag THEN 
      DO:
        IF act-combo = "ALL"  THEN
        FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.datum GE next-date
          AND akt-line.datum LE to-date AND akt-line.gastnr = inp-gastnr NO-LOCK,
          FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
          FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
          FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
          BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:
            CREATE aktline-list.
            ASSIGN
              aktline-list.bezeich     = akt-code.bezeich
              aktline-list.datum       = akt-line.datum
              aktline-list.zeit        = akt-line.zeit
              aktline-list.dauer       = akt-line.dauer
              aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
              aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
              aktline-list.prioritaet  = akt-line.prioritaet
              aktline-list.kontakt     = akt-line.kontakt 
              aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
              aktline-list.regard      = akt-line.regard
              aktline-list.userinit        = akt-line.userinit
              aktline-list.linenr      = akt-line.linenr
              aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
              aktline-list.telefon     = guest.telefon
              aktline-list.fax         = guest.fax
              aktline-list.bemerk      = akt-line.bemerk
              aktline-list.username    = bediener.username
              aktline-list.gastnr      = akt-line.gastnr
              aktline-list.guest-type  = guest.karteityp.
            FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
            IF AVAILABLE akt-kont THEN
            DO: 
                aktline-list.email    = akt-kont.email.
            END.
            aktline-list.priority   = prioritaet[aktline-list.prioritaet].
        END.
        ELSE 
        FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.datum GE next-date
          AND akt-line.datum LE to-date AND akt-line.gastnr = inp-gastnr NO-LOCK,
          FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
            akt-code.bezeich = act-combo NO-LOCK,
          FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
          FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
          BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:
            CREATE aktline-list.
            ASSIGN
              aktline-list.bezeich     = akt-code.bezeich
              aktline-list.datum       = akt-line.datum
              aktline-list.zeit        = akt-line.zeit
              aktline-list.dauer       = akt-line.dauer
              aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
              aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
              aktline-list.prioritaet  = akt-line.prioritaet
              aktline-list.kontakt     = akt-line.kontakt 
              aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
              aktline-list.regard      = akt-line.regard
              aktline-list.userinit        = akt-line.userinit
              aktline-list.linenr      = akt-line.linenr
              aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
              aktline-list.telefon     = guest.telefon
              aktline-list.fax         = guest.fax
              aktline-list.bemerk      = akt-line.bemerk
              aktline-list.username    = bediener.username
              aktline-list.gastnr      = akt-line.gastnr
              aktline-list.guest-type  = guest.karteityp.
            FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
            IF AVAILABLE akt-kont THEN
            DO: 
                aktline-list.email    = akt-kont.email.
            END.
            aktline-list.priority   = prioritaet[aktline-list.prioritaet].
        END.
      END.
      ELSE
      DO:
          IF act-combo = "ALL"  THEN
          FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.userinit = user-init AND akt-line.datum GE next-date
            AND akt-line.datum LE to-date AND akt-line.gastnr = inp-gastnr NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:
              CREATE aktline-list.
              ASSIGN
                aktline-list.bezeich     = akt-code.bezeich
                aktline-list.datum       = akt-line.datum
                aktline-list.zeit        = akt-line.zeit
                aktline-list.dauer       = akt-line.dauer
                aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                aktline-list.prioritaet  = akt-line.prioritaet
                aktline-list.kontakt     = akt-line.kontakt 
                aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                aktline-list.regard      = akt-line.regard
                aktline-list.userinit        = akt-line.userinit
                aktline-list.linenr      = akt-line.linenr
                aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                aktline-list.telefon     = guest.telefon
                aktline-list.fax         = guest.fax
                aktline-list.bemerk      = akt-line.bemerk
                aktline-list.username    = bediener.username
                aktline-list.gastnr      = akt-line.gastnr
                aktline-list.guest-type  = guest.karteityp.
              FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
              IF AVAILABLE akt-kont THEN
              DO: 
                aktline-list.email    = akt-kont.email.
              END.
              aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
          ELSE 
          FOR EACH akt-line WHERE akt-line.flag = acttype AND akt-line.userinit = user-init AND akt-line.datum GE next-date
            AND akt-line.datum LE to-date AND akt-line.gastnr = inp-gastnr NO-LOCK,
            FIRST akt-code WHERE akt-code.aktionscode = akt-line.aktionscode AND
            akt-code.bezeich = act-combo NO-LOCK,
            FIRST guest WHERE guest.gastnr = akt-line.gastnr NO-LOCK,
            FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK
            BY akt-line.datum BY akt-line.zeit BY akt-line.prioritaet DESC:
              CREATE aktline-list.
              ASSIGN
                aktline-list.bezeich     = akt-code.bezeich
                aktline-list.datum       = akt-line.datum
                aktline-list.zeit        = akt-line.zeit
                aktline-list.dauer       = akt-line.dauer
                aktline-list.ftime       = STRING(akt-line.zeit, "HH:MM") 
                aktline-list.ttime       = STRING(akt-line.dauer, "HH:MM")
                aktline-list.prioritaet  = akt-line.prioritaet
                aktline-list.kontakt     = akt-line.kontakt 
                aktline-list.NAME        = guest.NAME + ", " + guest.anredefirma
                aktline-list.regard      = akt-line.regard
                aktline-list.userinit        = akt-line.userinit
                aktline-list.linenr      = akt-line.linenr
                aktline-list.address     = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3 
                aktline-list.telefon     = guest.telefon
                aktline-list.fax         = guest.fax
                aktline-list.bemerk      = akt-line.bemerk
                aktline-list.username    = bediener.username
                aktline-list.gastnr      = akt-line.gastnr
                aktline-list.guest-type  = guest.karteityp.
              FIND FIRST akt-kont WHERE akt-kont.gastnr = guest.gastnr AND 
                akt-kont.kontakt-nr = akt-line.kontakt-nr NO-LOCK NO-ERROR.
              IF AVAILABLE akt-kont THEN
              DO: 
                aktline-list.email    = akt-kont.email.
              END.
              aktline-list.priority   = prioritaet[aktline-list.prioritaet].
          END.
      END.
   END.
END.
