# Lyrics Analysis

Updated version of <https://github.com/kahnwong/lyrics_visualization>

## Usage

1. `make setup`
2. Edit `lyrics_analysis/01_extract.py` to match your data source (this is what we'll use for actual analysis). See `lyrics_analysis\model\lyrics.py` for expected input format. Resulting file is located in `data/lyrics.json` in single-line JSON format.
3. Run `python3 lyrics_analysis/02_process.py` to tokenize lyrics.
4. Run `lyrics_analysis/03_analyze_word_count.py` to obtain a visuzliation.

## Findings

### Word count

![word count](images/word_count.png)

- Bar chart represents "word count ratio", higher value means lyrics often contain more repeated words.
- Line chart represents unique words, higher value means more corpus.

![word count box plot](images/word_count_box_plot.png)

- Nightwish has a wide q4, since their lyrics contain a lot of spoken words.
- Most bands are not on the "wordy" side, see Warkings and Ad Infinitum.
