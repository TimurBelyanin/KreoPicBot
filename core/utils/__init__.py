from random import choice
import string

admins = [683634457, 837030149]


def get_id_pack():
    leet = string.ascii_letters + string.digits
    return "".join([choice(leet) for i in range(7)])


proportions = {5: "XS", 10: "S", 20: "M", 30: "L", 50: "XL", 100: "XXL"}
