from random import choice
import string

admins = [683634457, 837030149]


def get_id_pack():
    leet = string.ascii_letters + string.digits
    return "".join([choice(leet) for i in range(7)])
