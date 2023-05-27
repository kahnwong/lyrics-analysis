import polars as pl
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

### prep
df = pl.read_ndjson("data/lyrics_processed.json")

df = (
    df.filter(pl.col("tokens").is_not_null())
    .groupby("artist")
    .agg(pl.col("tokens").flatten())
    .select("artist", "tokens")
    .sort("artist")
)


### feature engineering
def topic_modeling_nmf(x):
    # create word matrix
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = tfidf_vectorizer.fit_transform(x)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()

    # modeling
    model = NMF(n_components=1)

    model.fit_transform(tfidf)
    H = model.components_[0]  # we defined only 1 topic (per artist)

    # interpret
    NO_TOP_WORDS = 15

    return " ".join(
        [tfidf_feature_names[i] for i in H.argsort()[: -NO_TOP_WORDS - 1 : -1]]
    )


def topic_modeling_lda(x):
    # create word matrix
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = tfidf_vectorizer.fit_transform(x)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()

    # modeling
    model = LatentDirichletAllocation(n_components=1)

    model.fit_transform(tfidf)
    H = model.components_[0]  # we defined only 1 topic (per artist)

    # interpret
    NO_TOP_WORDS = 15

    return " ".join(
        [tfidf_feature_names[i] for i in H.argsort()[: -NO_TOP_WORDS - 1 : -1]]
    )


df = df.with_columns(
    pl.col("tokens").apply(topic_modeling_nmf).alias("topic_modeling_nmf")
).with_columns(pl.col("tokens").apply(topic_modeling_lda).alias("topic_modeling_lda"))

### reporting
data = df.select("artist", "topic_modeling_nmf", "topic_modeling_lda").rows(named=True)
for i in data:
    print(f"===== {i['artist']} =====")
    print("NMF")
    print(f"\t{i['topic_modeling_nmf']}")
    print("LDA")
    print(f"\t{i['topic_modeling_lda']}")
