# Lyrics Analysis

Updated version of <https://github.com/kahnwong/lyrics_visualization>

## Usage

1. `make setup`
2. Edit `lyrics_analysis/01_extract.py` to match your data source (this is what we'll use for actual analysis). See `lyrics_analysis\model\lyrics.py` for expected input format. Resulting file is located in `data/lyrics.json` in single-line JSON format.
3. Run `python3 lyrics_analysis/02_process.py` to tokenize lyrics.
