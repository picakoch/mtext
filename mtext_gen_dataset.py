import os
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
import re

BASE_DIR = "<PATH_TO_TXT_FILES>"
rows = []
re_eos = re.compile(r"([^ ])<\|e\|>")
for subdir, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.split(".")[-1] == "txt":
            print(file)
            full_path = os.path.join(subdir, file)
            with open(full_path) as f:
                txt = f.read()
                re.sub(re_eos, "\g<1> <|e|>", txt, re.MULTILINE)
                rows.append({"text": txt})

df = pd.DataFrame(rows)
print(df.head())

# push to hub
train_mtext = Dataset.from_pandas(df)
test_mtext = Dataset.from_pandas(df)

ds = DatasetDict()
ds["train"] = train_mtext
ds["test"] = test_mtext
print(df.info())
df.to_csv("dataset_15.02.2024.csv")
dataset_name = "ascherrer/mtext-data-150224"
ds.push_to_hub(dataset_name, branch="main", private=True)
