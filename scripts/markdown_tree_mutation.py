from csv import DictReader
from operator import itemgetter
from pathlib import Path

ip = Path("./data/tree_mutation.csv")
op = Path("./data/tree_mutation.mdi")

# Convert tree UID to name
trees_by_uid = {}
def uid_to_name(uid):
    if uid in trees_by_uid:
        return "{0} *({1})*".format(trees_by_uid[uid], uid.split(".")[0].capitalize())
    elif uid.startswith("forestry"):
        return "{0} *(Forestry)*".format(uid[13:])
    elif uid.startswith("extratrees"):
        return "{0} *(Extratrees)*".format(uid[19:].capitalize())
    else:
        return uid

# Read and process the relevant data from the input CSV file into a list of trees
trees = []
with ip.open() as csv_file:
    reader = DictReader(csv_file)
    for row in reader:
        trees_by_uid[row["UID"]] = row["Name"]
        t = (row["Name"],
             uid_to_name(row["Allele0"]),
             uid_to_name(row["Allele1"]),
             "{:G}%".format(float(row["baseChance"])),
             row["conditions"].replace("|", " ") if row["conditions"] else "None")
        trees.append(t)

# Sort the trees by name
trees.sort(key=itemgetter(0))

# Create a Markdown table from the list
md_table = ["| Tree Z | Tree X | Tree Y | Chance | Condition(s) |\n",
            "| :-- | :-- | :-- | --: | :-- |\n"]
for t in trees:
    md_table.append("| {0[0]} | {0[1]} | {0[2]} | {0[3]} | {0[4]} |\n".format(t))

# Write the Markdown table to a file
with op.open("w") as mdi_file:
    for row in md_table:
        mdi_file.write(row)
