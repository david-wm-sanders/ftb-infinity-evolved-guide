from csv import DictReader
from operator import itemgetter
from pathlib import Path

# TODO: Customise for bees!

ip = Path("./data/bee_mutation.csv")
op = Path("./data/bee_mutation.mdi")

# Convert bee UID to name
bees_by_uid = {}
def uid_to_name(uid):
    if uid in bees_by_uid:
        return "{0} *({1})*".format(bees_by_uid[uid][0], bees_by_uid[uid][1])
    elif uid.startswith("forestry"):
        name = uid[16:]
        bees_by_uid[uid] = name, "Forestry"
        return "{0} *(Forestry)*".format(name)
    elif uid.startswith("extrabees"):
        name = uid[18:].capitalize()
        bees_by_uid[uid] = name, "Extrabees"
        return "{0} *(Extrabees)*".format(name)
    elif uid.startswith("magicbees"):
        name = uid[17:]
        if name.startswith(("TE", "TC", "AE")):
            name = "{0} {1}".format(name[0:2], name[2:])
        bees_by_uid[uid] = name, "Magicbees"
        return "{0} *(Magicbees)*".format(name)
    elif uid.startswith("gendustry"):
        name = uid[14:].capitalize()
        bees_by_uid[uid] = name, "Gendustry"
        return "{0} *(Gendustry)*".format(name)
    else:
        return uid

# Read and process the relevant data from the input CSV file into a list of bees
bees = []
with ip.open() as csv_file:
    reader = DictReader(csv_file)
    for row in reader:
        uid, name = row["UID"], row["Name"]
        mod = uid.split(".")[0].capitalize()
        a0, a1 = row["Allele0"], row["Allele1"]
        chance = float(row["baseChance"])
        conditions = row["conditions"].replace("|", " ") if row["conditions"] else "None"
        bees_by_uid[uid] = name, mod
        name = "{0} *({1})*".format(name, mod)
        b = name, uid_to_name(a0), uid_to_name(a1), "{:G}%".format(chance), conditions
        bees.append(b)

# Sort the bees by name
bees.sort(key=itemgetter(0))

# Create a Markdown table from the list
md_table = ["| Bee Z | Bee X | Bee Y | Chance | Condition(s) |\n",
            "| :-- | :-- | :-- | --: | :-- |\n"]
for b in bees:
    md_table.append("| {0[0]} | {0[1]} | {0[2]} | {0[3]} | {0[4]} |\n".format(b))

# Write the Markdown table to a file
with op.open("w") as mdi_file:
    for row in md_table:
        mdi_file.write(row)
