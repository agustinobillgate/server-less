
DEF TEMP-TABLE t-zimkateg LIKE zimkateg.

DEF INPUT PARAMETER zikatstr AS CHAR.
DEF OUTPUT PARAMETER TABLE FOR t-zimkateg.

FIND FIRST zimkateg WHERE zimkateg.kurzbez = zikatstr NO-LOCK.
CREATE t-zimkateg.
BUFFER-COPY zimkateg TO t-zimkateg.
