from csv import DictReader
from operator import itemgetter
from pathlib import Path

ip = Path("./data/flower_mutation.csv")
op = Path("./data/flower_mutation.mdi")

# Read the input CSV file into a dictionary
flowers_d = {}
with ip.open() as csv_file:
    reader = DictReader(csv_file)
    for row in reader:
        flowers_d[row["UID"]] = {"name": row["Name"], "a0": row["Allele0"],
                                    "a1": row["Allele1"], "chance": row["baseChance"]}

# Mangle the dictionary into a list
flowers = []
for uid, flower in flowers_d.items():
    f = (flower["name"],
         flower["a0"].split(".")[3].capitalize(),
         flower["a1"].split(".")[3].capitalize(),
         "{:G}%".format(float(flower["chance"])))
    flowers.append(f)

# Sort the flowers by name
flowers.sort(key=itemgetter(0))

# Create a Markdown table from the list
md_table = ["| Flower Z | Flower X | Flower Y | Chance |",
            "| :-- | :-- | :-- | --: |"]
for f in flowers:
    md_table.append("| {0[0]} | {0[1]} | {0[2]} | {0[3]} |".format(f))

# Write the Markdown table to a file
with op.open("w") as mdi_file:
    for row in md_table:
        mdi_file.write(row)
        mdi_file.write("\n")
