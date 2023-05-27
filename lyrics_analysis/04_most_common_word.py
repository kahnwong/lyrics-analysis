from collections import Counter

import polars as pl
from matplotlib import pyplot as plt


####################################
# prep data
####################################
df = pl.read_ndjson("data/lyrics_processed.json")

df = (
    df.filter(pl.col("tokens").is_not_null())
    .groupby("artist")
    .agg(pl.col("tokens").flatten())
    .with_columns(
        pl.col("tokens")
        .apply(lambda x: dict(Counter(x).most_common(10)))
        .alias("count")
    )
    .select("artist", "count")
    .sort("artist")
)
print(df)

####################################
# visualize A: word count ratio
####################################
data = df.rows(named=True)

fig, axs = plt.subplots(
    len(data), figsize=(10, 70)
)  # adjust figure size here if it's too cramped
for index, i in enumerate(data):
    word_count = i["count"]
    word_count = {k: v for k, v in word_count.items() if v is not None}
    word_count = dict(
        sorted(word_count.items(), key=lambda item: item[1], reverse=True)
    )

    axs[index].bar(word_count.keys(), word_count.values())
    axs[index].set_title(i["artist"])

fig.savefig("images/most_common_word.png")
