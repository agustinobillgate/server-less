DEFINE TEMP-TABLE origin-list
    FIELD kurzbez       LIKE nation.kurzbez
    FIELD bezeich       LIKE nation.bezeich
    .

DEFINE OUTPUT PARAMETER TABLE FOR origin-list.
FOR EACH nation WHERE nation.natcode = 0 NO-LOCK :
    CREATE origin-list.
    BUFFER-COPY nation TO origin-list.
END.
