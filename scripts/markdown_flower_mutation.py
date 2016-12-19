from csv import DictReader
from operator import itemgetter
from pathlib import Path

ip = Path("./data/flower_mutation.csv")
op = Path("./data/flower_mutation.mdi")

# Read and process the relevant data from the input CSV file into a list of flowers
flowers = []
with ip.open() as csv_file:
    reader = DictReader(csv_file)
    for row in reader:
        f = (row["Name"],
             row["Allele0"].split(".")[3].capitalize(),
             row["Allele1"].split(".")[3].capitalize(),
             "{:G}%".format(float(row["baseChance"])))
        flowers.append(f)

# Sort the flowers by name
flowers.sort(key=itemgetter(0))

# Create a Markdown table from the list
md_table = ["| Flower Z | Flower X | Flower Y | Chance |\n",
            "| :-- | :-- | :-- | --: |\n"]
for f in flowers:
    md_table.append("| {0[0]} | {0[1]} | {0[2]} | {0[3]} |\n".format(f))

# Write the Markdown table to a file
with op.open("w") as mdi_file:
    for row in md_table:
        mdi_file.write(row)
