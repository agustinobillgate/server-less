
DEFINE TEMP-TABLE q1-list
    FIELD guest-name        LIKE guest.name
    FIELD anredefirma       LIKE guest.anredefirma
    FIELD akt-kont-name     LIKE akt-kont.name
    FIELD vorname           LIKE akt-kont.vorname
    FIELD anrede            LIKE akt-kont.anrede
    FIELD flag              LIKE akthdr.flag
    FIELD akthdr-bezeich    LIKE akthdr.bezeich
    FIELD akt-code-bezeich  LIKE akt-code.bezeich
    FIELD t-betrag          LIKE akthdr.t-betrag
    FIELD erl-datum         LIKE akthdr.erl-datum
    FIELD userinit          LIKE akthdr.userinit
    FIELD chg-id            LIKE akthdr.chg-id
    FIELD chg-datum         LIKE akthdr.chg-datum
    FIELD aktnr             LIKE akthdr.aktnr
    
    FIELD next-datum        LIKE akthdr.next-datum
    FIELD erledigt          LIKE akthdr.erledigt
    FIELD akthdr-recid      AS INT.

DEF INPUT  PARAMETER inp-gastnr AS INT.
DEF INPUT  PARAMETER next-date  AS DATE.
DEF INPUT  PARAMETER to-date    AS DATE.
DEF INPUT  PARAMETER all-flag   AS LOGICAL.
DEF INPUT  PARAMETER sflag      AS INT.
DEF INPUT  PARAMETER user-init  AS CHAR.
DEF OUTPUT PARAMETER guest-name AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR q1-list.

IF inp-gastnr NE 0 THEN
DO:
    FIND FIRST guest WHERE guest.gastnr = inp-gastnr NO-LOCK.
    guest-name = guest.NAME.
END.

IF next-date = ? THEN 
  RUN disp-all. 
ELSE RUN disp-it. 


PROCEDURE disp-all:
  IF inp-gastnr = 0 THEN
  DO:
    IF all-flag THEN  /* all users */ 
    DO:
      IF sflag = 1 THEN
      FOR EACH akthdr WHERE akthdr.flag = 1  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
           akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 2 THEN
      FOR EACH akthdr WHERE (akthdr.flag = 2 OR akthdr.flag = 3)  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 3 THEN
      FOR EACH akthdr WHERE akthdr.flag = 4  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
    END. 
    ELSE 
    DO:
      IF sflag = 1 THEN
      FOR EACH akthdr WHERE akthdr.flag = 1 AND akthdr.userinit = user-init NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 2 THEN
      FOR EACH akthdr WHERE (akthdr.flag = 2 OR akthdr.flag = 3) AND akthdr.userinit = user-init NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 3 THEN
      FOR EACH akthdr WHERE akthdr.flag = 4 AND akthdr.userinit = user-init NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
    END.
  END.
  ELSE
  DO:
    IF all-flag THEN  /* all users */ 
    DO:
      IF sflag = 1 THEN
      FOR EACH akthdr WHERE akthdr.flag = 1 AND akthdr.gastnr = inp-gastnr NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr 
          AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 2 THEN
      FOR EACH akthdr WHERE (akthdr.flag = 2 OR akthdr.flag = 3) AND akthdr.gastnr = inp-gastnr NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
        AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 3 THEN
      FOR EACH akthdr WHERE akthdr.flag = 4 AND akthdr.gastnr = inp-gastnr NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
            AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
    END. 
    ELSE 
    DO:
      IF sflag = 1 THEN
      FOR EACH akthdr WHERE akthdr.flag = 1 AND akthdr.userinit = user-init AND akthdr.gastnr = inp-gastnr NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
          AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 2 THEN
      FOR EACH akthdr WHERE (akthdr.flag = 2 OR akthdr.flag = 3) AND akthdr.gastnr = inp-gastnr AND akthdr.userinit = user-init NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
          AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 3 THEN
      FOR EACH akthdr WHERE akthdr.flag = 4 AND akthdr.gastnr = inp-gastnr AND akthdr.userinit = user-init NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
          AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
    END.
  END.
END.


PROCEDURE disp-it:
  IF inp-gastnr = 0 THEN
  DO:
    IF all-flag THEN  /* all users */ 
    DO:
      IF sflag = 1 THEN
      FOR EACH akthdr WHERE akthdr.flag = 1  
        AND akthdr.next-datum GE next-date AND akthdr.next-datum LE to-date  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND akt-kont.kontakt-nr = 
          akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 2 THEN
      FOR EACH akthdr WHERE (akthdr.flag = 2 OR akthdr.flag = 3)  
        AND akthdr.erl-datum GE next-date AND akthdr.erl-datum LE to-date NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 3 THEN
      FOR EACH akthdr WHERE akthdr.flag = 4  
        AND akthdr.next-datum GE next-date AND akthdr.next-datum LE to-date NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
    END. 
    ELSE 
    DO:
      IF sflag = 1 THEN
      FOR EACH akthdr WHERE akthdr.flag = 1 AND akthdr.userinit = user-init 
        AND akthdr.next-datum GE next-date AND akthdr.next-datum LE to-date NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 2 THEN
      FOR EACH akthdr WHERE (akthdr.flag = 2 OR akthdr.flag = 3) AND akthdr.userinit = user-init 
        AND akthdr.erl-datum GE next-date AND akthdr.erl-datum LE to-date  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 3 THEN
      FOR EACH akthdr WHERE akthdr.flag = 4 AND akthdr.userinit = user-init 
        AND akthdr.next-datum GE next-date AND akthdr.next-datum LE to-date  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr AND
          akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
    END.
  END.
  ELSE
  DO:
    IF all-flag THEN  /* all users */ 
    DO:
      IF sflag = 1 THEN
      FOR EACH akthdr WHERE akthdr.flag = 1 AND akthdr.gastnr = inp-gastnr 
        AND akthdr.next-datum GE next-date AND akthdr.next-datum LE to-date  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
          AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 2 THEN
      FOR EACH akthdr WHERE (akthdr.flag = 2 OR akthdr.flag = 3) AND akthdr.gastnr = inp-gastnr 
        AND akthdr.erl-datum GE next-date AND akthdr.erl-datum LE to-date  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
            AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 3 THEN
      FOR EACH akthdr WHERE akthdr.flag = 4 AND akthdr.gastnr = inp-gastnr 
        AND akthdr.next-datum GE next-date AND akthdr.next-datum LE to-date NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
            AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
    END. 
    ELSE 
    DO:
      IF sflag = 1 THEN
      FOR EACH akthdr WHERE akthdr.flag = 1 AND akthdr.userinit = user-init AND akthdr.gastnr = inp-gastnr 
        AND akthdr.next-datum GE next-date AND akthdr.next-datum LE to-date  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
          AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 2 THEN
      FOR EACH akthdr WHERE (akthdr.flag = 2 OR akthdr.flag = 3) AND akthdr.gastnr = inp-gastnr AND akthdr.userinit = user-init 
        AND akthdr.erl-datum GE next-date AND akthdr.erl-datum LE to-date  NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
          AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
      ELSE IF sflag = 3 THEN
      FOR EACH akthdr WHERE akthdr.flag = 4 AND akthdr.gastnr = inp-gastnr AND akthdr.userinit = user-init 
        AND akthdr.next-datum GE next-date AND akthdr.next-datum LE to-date NO-LOCK,
        FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
        FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
        FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr
          AND akt-kont.kontakt-nr = akthdr.kontakt-nr NO-LOCK
        BY guest.NAME BY akthdr.next-datum DESC:
        RUN create-it.
      END.
    END.
  END.
END.

PROCEDURE create-it:
    CREATE q1-list.
    ASSIGN
        q1-list.guest-name        = guest.name
        q1-list.anredefirma       = guest.anredefirma
        q1-list.akt-kont-name     = akt-kont.name
        q1-list.vorname           = akt-kont.vorname
        q1-list.anrede            = akt-kont.anrede
        q1-list.flag              = akthdr.flag
        q1-list.akthdr-bezeich    = akthdr.bezeich
        q1-list.akt-code-bezeich  = akt-code.bezeich
        q1-list.t-betrag          = akthdr.t-betrag
        q1-list.erl-datum         = akthdr.erl-datum
        q1-list.userinit          = akthdr.userinit
        q1-list.chg-id            = akthdr.chg-id
        q1-list.chg-datum         = akthdr.chg-datum
        q1-list.aktnr             = akthdr.aktnr
        q1-list.akthdr-recid      = RECID(akthdr).
END.
