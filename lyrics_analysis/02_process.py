# from sklearn.decomposition import NMF, LatentDirichletAllocation
# from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import nltk
import polars as pl
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


### prep
df = pl.read_ndjson("data/lyrics.json")
df = df.with_columns(
    pl.col("year").str.slice(0, length=4).alias("year"),
)

### feature engineering
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

lemmatizer = WordNetLemmatizer()


def tokenize(x):
    tokens = [lemmatizer.lemmatize(i.lower()) for i in word_tokenize(x) if len(i) > 3]
    return [word for word in tokens if word not in stopwords.words("english")]


df = (
    df.filter(pl.col("lyrics").is_not_null())
    .with_columns(pl.col("lyrics").apply(tokenize).alias("tokens"))
    .drop("lyrics")
)

### write
df.write_ndjson("data/lyrics_processed.json")
