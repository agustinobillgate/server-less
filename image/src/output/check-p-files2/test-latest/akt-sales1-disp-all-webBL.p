
DEF TEMP-TABLE q1-list LIKE akthdr
    FIELD akthdr-recid      AS INT
    FIELD guest-name        LIKE guest.name
    FIELD guest-anredefirma LIKE guest.anredefirma
    FIELD akt-kont-name     LIKE akt-kont.name
    FIELD akt-kont-vorname  LIKE akt-kont.vorname
    FIELD akt-kont-anrede   LIKE akt-kont.anrede
    FIELD akt-code-bezeich  LIKE akt-code.bezeich.

DEFINE BUFFER akt-code1 FOR akt-code.
DEFINE BUFFER akt-line1 FOR akt-line.

DEF TEMP-TABLE q2-list LIKE akt-line
    FIELD recid-akt-line    AS INT
    FIELD akt-code-bezeich  LIKE akt-code.bezeich
    FIELD bediener-username LIKE bediener.username
    FIELD company-name      AS CHARACTER
    .

DEF INPUT  PARAMETER aktnr AS INT.
DEF OUTPUT PARAMETER TABLE FOR q1-list.
DEF OUTPUT PARAMETER TABLE FOR q2-list.

FOR EACH akthdr WHERE akthdr.aktnr = aktnr AND akthdr.flag NE 0 NO-LOCK,
    FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK,
    FIRST akt-code WHERE akt-code.aktiongrup = 2 AND akt-code.aktionscode = akthdr.stufe NO-LOCK,
    FIRST akt-kont WHERE akt-kont.gastnr = akthdr.gastnr NO-LOCK
    BY guest.NAME BY akthdr.next-datum DESC:
    CREATE q1-list.
    BUFFER-COPY akthdr TO q1-list.
    ASSIGN
    q1-list.akthdr-recid      = RECID(akthdr)
    q1-list.guest-name        = guest.name
    q1-list.guest-anredefirma = guest.anredefirma
    q1-list.akt-kont-name     = akt-kont.name
    q1-list.akt-kont-vorname  = akt-kont.vorname
    q1-list.akt-kont-anrede   = akt-kont.anrede
    q1-list.akt-code-bezeich  = akt-code.bezeich.
END.

FOR EACH akt-line WHERE akt-line.aktnr = aktnr AND akt-line.flag NE 2 NO-LOCK,
    FIRST akt-code1 WHERE akt-code1.aktionscode = akt-line.aktionscode NO-LOCK,
    FIRST bediener WHERE bediener.userinit = akt-line.userinit NO-LOCK,
    FIRST akthdr WHERE akthdr.aktnr = akt-line.aktnr AND akthdr.flag NE 0 NO-LOCK,
    FIRST guest WHERE guest.gastnr = akthdr.gastnr NO-LOCK
    BY akt-line.datum BY akt-line.prioritaet DESC:
    CREATE q2-list.
    BUFFER-COPY akt-line TO q2-list.
    ASSIGN
    q2-list.recid-akt-line    = RECID(akt-line)
    q2-list.akt-code-bezeich  = akt-code1.bezeich
    q2-list.bediener-username = bediener.username.
    q2-list.company-name      = guest.NAME + ", " + guest.anredefirma.
END.
