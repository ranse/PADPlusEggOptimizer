from constraint.constraint import *
import time

MAX_NUM_RESULTS = 10

class Monster:
    total_diff = 0
    mon_num = 0

    def __init__(self, hp, atk, rcv):
        self.hp = hp
        self.atk = atk
        self.rcv = rcv

    def set_hp(self, hp):
        self.hp = hp

    def get_hp(self):
        return self.hp

    def set_atk(self, atk):
        self.atk = atk

    def get_atk(self):
        return self.atk

    def set_rcv(self, rcv):
        self.rcv = rcv

    def get_rcv(self):
        return self.rcv

    def get_diff_hp(self):
        return 99 - self.hp

    def get_diff_atk(self):
        return 99 - self.atk

    def get_diff_rcv(self):
        return 99 - self.rcv

    def get_total_diff(self):
        self.total_diff = 297 - (self.hp + self.atk + self.rcv)
        return self.total_diff

    def set_mon_num(self, mon_num):
        self.mon_num = mon_num

    def get_mon_num(self):
        return self.mon_num


def main():
    base_mon_string = input("Base monster + eggs (HP/ATK/RCV): ")
    base_hp = int(base_mon_string.split("/")[0])
    base_atk = int(base_mon_string.split("/")[1])
    base_rcv = int(base_mon_string.split("/")[2])

    base_mon = Monster(base_hp, base_atk, base_rcv)

    all_monster_list = []
    add_mon(all_monster_list)

    print("Calculating...")
    start_time = time.time()
    new_mon_list = calculate_best(base_mon, all_monster_list)
    new_mon_list = remove_extra(new_mon_list)
    sorted_list = sorted(new_mon_list, key=lambda k: k['result'], reverse=True)[:MAX_NUM_RESULTS]
    format_output(sorted_list)
    print("Time to find: %s seconds" % (time.time() - start_time))


# Adds one more monster to the list of all available monsters
def add_mon(all_monster_list):
    monster_count = 1
    print("Enter + eggs of monsters to feed or leave blank to finish")
    while True:
        mon_string = input("Monster %d: " % monster_count)

        if not mon_string.split():
            break

        mon_hp = int(mon_string.split("/")[0])
        mon_atk = int(mon_string.split("/")[1])
        mon_rcv = int(mon_string.split("/")[2])

        monster = Monster(mon_hp, mon_atk, mon_rcv)
        monster.set_mon_num(monster_count)
        all_monster_list.append(monster)
        monster_count += 1


# Function for setting constraint
def add_mons(*arg):
    hp_list = []
    atk_list = []
    rcv_list = []
    for mon in arg[2:]:
        hp_list.append(mon.get_hp())
        atk_list.append(mon.get_atk())
        rcv_list.append(mon.get_rcv())

    hp = arg[1].get_hp() + sum(hp_list)
    atk = arg[1].get_atk() + sum(atk_list)
    rcv = arg[1].get_rcv() + sum(rcv_list)

    return arg[0] == (hp + atk + rcv) \
        and hp <= 99 and atk <= 99 and rcv <= 99


# Calculates options to get as close to +297 as possible
def calculate_best(base_mon, all_monster_list):
    problem = Problem()
    empty_mon = Monster(0, 0, 0)
    problem.addVariable("result", list(range(298)))
    problem.addVariable("base_mon", [base_mon])
    var_list = ["result", "base_mon"]
    for i in all_monster_list:
        var_list.append("mon"+str(i.get_mon_num()))

    for mon in all_monster_list:
        problem.addVariable("mon"+str(mon.get_mon_num()), [mon, empty_mon])

    problem.addConstraint(add_mons, var_list)
    return problem.getSolutions()


def remove_extra(mon_list):
    for mon in mon_list:
        sorted_key = sorted(mon.keys())
        feed_mon_key_list = sorted_key[1:-1]
        for key in feed_mon_key_list:
            mon_hp = mon[key].get_hp()
            mon_atk = mon[key].get_atk()
            mon_rcv = mon[key].get_rcv()

            if (mon_hp == 0) and (mon_atk == 0) and (mon_rcv == 0):
                del mon[key]

    return mon_list


def format_output(mon_list):
    option = 1
    for mon in mon_list:
        if len(mon) >= 3:
            print("Option %d:" % option)
            if len(mon) == 3:
                print("Feed monster", end="")
            else:
                print("Feed monsters", end="")
            sorted_keys = sorted(mon.keys())
            for key in sorted_keys[:-2]:
                if key != "base_mon":
                    print(" #%s," % key[3:], end="")
            last_mon_num = sorted_keys[-2][3:]
            print(" #%s " % last_mon_num)

            print("You will need %d more +eggs"
                  % (297 - mon["result"]))

            feed_mon_key_list = sorted_keys[1:-1]
            base_mon = mon['base_mon']
            result_mon = Monster(base_mon.get_hp(),
                                 base_mon.get_atk(),
                                 base_mon.get_rcv())
            for key in feed_mon_key_list:
                result_mon.set_hp(result_mon.get_hp() +
                                  mon[key].get_hp())
                result_mon.set_atk(result_mon.get_atk() +
                                   mon[key].get_atk())
                result_mon.set_rcv(result_mon.get_rcv() +
                                   mon[key].get_rcv())
            print("Your monster will be at %d HP, %d ATK and %d RCV"
                  % (result_mon.get_hp(), result_mon.get_atk(), result_mon.get_rcv()))
            print("You will need %d HP, %d ATK and %d RCV eggs to hit +297"
                  % (result_mon.get_diff_hp(), result_mon.get_diff_atk(), result_mon.get_diff_rcv()))

            print()
            option += 1


if __name__ == "__main__":
    main()
