from random import choice
import string

admins = [683634457, 837030149]
white_list = [837030149, 683634457, 5236215230, 6802569070]


def get_id_pack():
    leet = string.ascii_letters + string.digits
    return "".join([choice(leet) for i in range(7)])


# proportions = {5: "XS", 10: "S", 20: "M", 30: "L", 50: "XL", 100: "XXL"}
proportions = {5: "S", 10: "M", 20: "L", 30: "XL"}
