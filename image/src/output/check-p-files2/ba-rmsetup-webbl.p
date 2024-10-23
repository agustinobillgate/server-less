DEFINE TEMP-TABLE bk-list 
    FIELD raum          LIKE bk-rset.raum
    FIELD rset-bezeich  LIKE bk-rset.bezeich
    FIELD raum-bezeich  LIKE bk-raum.bezeich
    FIELD setup-bezeich LIKE bk-setup.bezeich
    FIELD personen      LIKE bk-rset.personen
    FIELD preis         LIKE bk-rset.preis
    FIELD nebenstelle   LIKE bk-rset.nebenstelle
    FIELD vorbereit     LIKE bk-rset.vorbereit
    FIELD vname         LIKE bk-rset.vname
    FIELD setup-id      LIKE bk-rset.setup-id
    FIELD rec-id        AS INTEGER
    .

DEFINE OUTPUT PARAMETER TABLE FOR bk-list.

FOR EACH bk-rset NO-LOCK,
    FIRST bk-raum WHERE bk-raum.raum = bk-rset.raum NO-LOCK,
    FIRST bk-setup WHERE bk-setup.setup-id = bk-rset.setup-id NO-LOCK
    BY bk-rset.raum.

    CREATE bk-list.
    ASSIGN
        bk-list.raum            = bk-rset.raum
        bk-list.rset-bezeich    = bk-rset.bezeich
        bk-list.raum-bezeich    = bk-raum.bezeich
        bk-list.setup-bezeich   = bk-setup.bezeich
        bk-list.personen        = bk-rset.personen
        bk-list.preis           = bk-rset.preis
        bk-list.nebenstelle     = bk-rset.nebenstelle
        bk-list.vorbereit       = bk-rset.vorbereit
        bk-list.vname           = bk-rset.vname
        bk-list.setup-id        = bk-rset.setup-id
        bk-list.rec-id          = RECID(bk-rset)
        .

END.

