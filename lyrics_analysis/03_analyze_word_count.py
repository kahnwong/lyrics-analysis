import os

import polars as pl
import seaborn as sns
from matplotlib import pyplot as plt

os.makedirs("images", exist_ok=True)


####################################
# prep data
####################################
df = pl.read_ndjson("data/lyrics_processed.json")

df = (
    df.select("artist", "tokens").with_columns(
        pl.col("tokens").arr.lengths().alias("token_count")
    )
).with_columns(pl.col("tokens").arr.unique().arr.lengths().alias("unique_token_count"))


####################################
# visualize A: word count ratio
####################################
### prep
df_a = (
    df.groupby("artist")
    .agg(
        pl.col("token_count").mean().alias("token_count"),
        pl.col("unique_token_count").mean().alias("unique_token_count"),
    )
    .with_columns(
        (pl.col("token_count") / pl.col("unique_token_count")).alias("word_count_ratio")
    )
    .sort("word_count_ratio")
    .to_pandas()
)

### visualize
fig, ax1 = plt.subplots()
fig.set_size_inches(16, 10)
ax2 = ax1.twinx()

sns.barplot(
    data=df_a,
    x="artist",
    y="word_count_ratio",
    # hue="engine",
    ax=ax1,
)
ax1.set_title("Unique word count ratio in relation to total unique word per artist")
ax1.set_xlabel("")
ax1.set_ylabel("Bar: Word count ratio")
ax1.tick_params(axis="x", rotation=45)

sns.pointplot(
    data=df_a,
    x="artist",
    y="unique_token_count",
    # hue="engine",
    ax=ax2,
)
ax2.set_ylabel("Line: Unique word count")

fig.savefig("images/word_count.png")

####################################
# visualize B: word count box plot
####################################
### prep
df_b = df.filter(pl.col("artist") != "Stream of Passion").to_pandas()

### visualize
fig.clf()
plt.figure(figsize=(10, 7))
boxplot = sns.boxplot(x="token_count", y="artist", data=df_b, orient="h")


fig = boxplot.get_figure()
fig.savefig("images/word_count_box_plot.png")
