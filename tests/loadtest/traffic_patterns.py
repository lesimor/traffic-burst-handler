import pandas as pd

TB_STAY = [
    3,
    3,
    3,
    3,
    3,
    3,
    80,
    70,
    75,
    65,
    55,
    70,
    65,
    70,
    65,
    75,
    60,
    55,
    50,
    45,
    40,
    35,
    45,
    35,
    60,
    50,
    55,
    70,
    65,
    60,
    80,
    75,
    70,
    60,
    55,
    45,
    35,
    45,
    40,
    35,
    30,
    25,
    30,
    25,
    30,
    20,
    15,
    10,
]

# Define a dictionary with some data
data = {
    "p_1": TB_STAY,
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("example.csv", index=False)

df = pd.read_csv("example.csv", usecols=["p_1"])

print(df["p_1"].tolist())
