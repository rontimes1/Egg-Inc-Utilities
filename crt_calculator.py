from decimal import localcontext, Decimal, ROUND_HALF_UP


def run_cap(coop_size, contract_duration):
    with localcontext() as ctx:
        ctx.rounding = ROUND_HALF_UP
        n = min(Decimal(contract_duration * coop_size) / 2, Decimal(20))
        return int(n.to_integral_value())


def calculate_number_of_kicks(cr_cap, cr_per_round):
    kick_rounds = 0
    counter = 0
    for i in range(1, cr_cap + 1):
        if counter == cr_per_round and i < cr_cap:
            kick_rounds += 1
        counter = (counter % cr_per_round) + 1
    return kick_rounds


def print_cr_round_text(cr_cap, coop_size, self_run=False):
    max_cr_per_round = coop_size - 1 if self_run else coop_size - 2
    # print(f"The maximum number of Chicken Runs per person per CRT round with coop size {coop_size}" + (" and Self-Runs" if self_run else "") + f" is {max_cr_per_round}.")
    counter = 0
    cr_round = 1
    for i in range(1, cr_cap + 1):
        if counter == 0 or counter == 1 and i != 2:
            print(num_to_discord_emoji(cr_round), end=' ')

        if counter == 0 and self_run or counter == 1 and i != 2 and self_run:
            e = ", " if i != cr_cap else "\n"
            print(f"CR{i} (self-run)", end=e)
        elif counter == max_cr_per_round:
            print(f"CR{i}")
            if i < cr_cap:
                print("> :leg: Coop creator kicks everyone!")
                cr_round += 1
        else:
            e = ", " if i != cr_cap else "\n"
            print(f"CR{i}", end=e)
        counter = (counter % max_cr_per_round) + 1


def print_react_text(kicks):
    if kicks <= 0:
        return
    number_list = []
    if kicks <= 1:
        number_list = [num_to_discord_emoji(kicks)]
    else:
        for x in range(1, kicks + 1):
            number_list.append(num_to_discord_emoji(x))
            if x != kicks:
                number_list.append(", ")
        number_list[len(number_list) - list(reversed(number_list)).index(", ") - 1] = (", or " if kicks > 2 else " or ")
    number_text = "".join(number_list)
    print(f"React {number_text} when you have completed your Chicken Runs for the current round!")


def print_full_message(coop_size, contract_duration):
    if coop_size <= 2:
        print('Coop Size must be 3 or more for CRT to work.')
        exit()
    if contract_duration < 1:
        print("Contract Duration cannot be less than 1 day.")
        exit()
    chicken_run_cap = run_cap(coop_size=coop_size, contract_duration=contract_duration)
    print(f"Chicken Run Cap: {chicken_run_cap}\n")

    kicks_normal = calculate_number_of_kicks(chicken_run_cap, coop_size - 2)
    kicks_self_run = calculate_number_of_kicks(chicken_run_cap, coop_size - 1)

    if kicks_self_run < kicks_normal:
        print("It is more advantageous if everyone runs chickens on themselves each CRT round!")
    else:
        print("There is no advantage gained by self running chickens.")
    print()

    print("Text for Normal CRT:")
    print("# Coop: \n")
    print(
        f"`Each coop member should be kicked {kicks_normal} time(s) to reach the Chicken Run cap of {chicken_run_cap}.`")
    print("## :chickenrun::chickenrun: Tango :dancer: :tada: \n")
    print_cr_round_text(chicken_run_cap, coop_size, self_run=False)
    print("## :race_car: Boost Order :race_car:")
    print("(copy as needed :white_check_mark::icon_token::arrow_left::Boosted:)")
    print("\n".join(
        [f"{num_to_discord_emoji(x, fill=(True if coop_size > 9 else False))}:" for x in range(1, coop_size + 1)]))
    print()
    print_react_text(kicks_normal)

    print()
    print("*" * 80)
    print("*" * 80)
    print()

    print("Text for Self-Run CRT:")
    print("# Coop: \n")
    print(
        f"`Each coop member should be kicked {kicks_self_run} time(s) to reach the Chicken Run cap of {chicken_run_cap}.`")
    print("## :chickenrun::chickenrun: Tango :dancer: :tada: \n")
    print_cr_round_text(chicken_run_cap, coop_size, self_run=True)
    print("## :race_car: Boost Order :race_car:")
    print("(copy as needed :white_check_mark::icon_token::arrow_left::Boosted:)")
    print("\n".join(
        [f"{num_to_discord_emoji(x, fill=(True if coop_size > 9 else False))}:" for x in range(1, coop_size + 1)]))
    print()
    print_react_text(kicks_self_run)


def num_to_discord_emoji(number, fill=False):
    if fill:
        return "".join([[":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:",
                         ":nine:"][int(d)] for d in (str(number) if number > 9 else f"0{str(number)}")])
    else:
        return "".join([[":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:",
                         ":nine:"][int(d)] for d in str(number)])


if __name__ == '__main__':
    coop_size = int(input("Enter the Coop Size: "))
    contract_duration = int(input("Enter the Contract Duration: "))
    print_full_message(coop_size, contract_duration)
