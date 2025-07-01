
DEFINE TEMP-TABLE op-list       LIKE l-op
    FIELD bezeich LIKE l-art.bezeich
    FIELD username AS CHAR. 

DEF INPUT-OUTPUT PARAMETER TABLE FOR op-list.

DEF BUFFER l-art FOR l-artikel.
DEFINE buffer sys-user FOR bediener.
DEF TEMP-TABLE buf-op-list LIKE op-list.

FOR EACH op-list:
    CREATE buf-op-list.
    BUFFER-COPY op-list TO buf-op-list.
END.
FOR EACH op-list:
    DELETE op-list.
END.
FOR EACH buf-op-list,
    FIRST l-art WHERE l-art.artnr = buf-op-list.artnr, 
    FIRST sys-user WHERE sys-user.nr = buf-op-list.fuellflag 
    NO-LOCK BY buf-op-list.datum descending BY buf-op-list.zeit descending:
    CREATE op-list.
    BUFFER-COPY buf-op-list TO op-list.
    ASSIGN
        op-list.bezeich = l-art.bezeich
        op-list.username = sys-user.username.
END.
