import glob
import json
import os
from typing import List

import mutagen
from tqdm import tqdm

from lyrics_analysis.model.lyrics import LyricsItem
from lyrics_analysis.utils.log import log


def get_files(paths: List[str]) -> List[str]:
    files = []

    for path in paths:
        extensions = ["m4a"]
        search_patterns = [f"{path}/**/*.{ext}" for ext in extensions]
        log.debug(f"search pattern: {search_patterns}")

        for i in search_patterns:
            matched_files = glob.glob(i, recursive=True)
            matched_files = [i for i in matched_files if "Instrumental" not in i]
            matched_files = [i for i in matched_files if "Live" not in i]

            files.extend(matched_files)

    log.debug(f"files: {files}")

    return files


def get_lyrics_from_tag(file: str) -> str:
    metadata = mutagen.File(file).tags
    log.debug(f"metadata keys: {metadata.keys()}")

    return LyricsItem(
        artist=metadata["aART"][0],
        album=metadata["©alb"][0],
        year=metadata["©day"][0],
        title=metadata["©nam"][0],
        lyrics=metadata.get("©lyr")[0] if metadata.get("©lyr") else None,
    )


if __name__ == "__main__":
    paths = [
        r"D:\Music\# Metal\Ad Infinitum",
        r"D:\Music\# Metal\Amaranthe",
        r"D:\Music\# Metal\Battle Beast",
        r"D:\Music\# Metal\Epica\2003 - The Phantom Agony (Expanded Edition) [Reissued-2013]",
        r"D:\Music\# Metal\Epica\2005 - Consign to Oblivion (Expanded Edition) [Reissued-2015]",
        r"D:\Music\# Metal\Epica\2007 - The Divine Conspiracy",
        r"D:\Music\# Metal\Epica\2009 - Design Your Universe (Gold Edition) [Reissued-2019]",
        r"D:\Music\# Metal\Epica\2012 - Requiem for the Indifferent",
        r"D:\Music\# Metal\Epica\2014 - The Quantum Enigma (Earbook Edition)",
        r"D:\Music\# Metal\Epica\2016 - The Holographic Principle (Earbook Edition)",
        r"D:\Music\# Metal\Epica\2017 - Epica vs Attack On Titan Songs",
        r"D:\Music\# Metal\Epica\2021 - Omega (Earbook Edition)",
        r"D:\Music\# Metal\Epica\2022 - The Alchemy Project - EP",
        r"D:\Music\# Metal\Fallen Sanctuary",
        r"D:\Music\# Metal\Myrath\2011 - Tales of the Sands (Japanese Edition)",
        r"D:\Music\# Metal\Myrath\2016 - Legacy (Japanese Edition)",
        r"D:\Music\# Metal\Myrath\2019 - Shehili (Japanese Edition)",
        r"D:\Music\# Metal\Nightwish\2015 - Endless Forms Most Beautiful",
        r"D:\Music\# Metal\Nightwish\2011 - Imaginaerum (2 CD Digipack Edition)",
        r"D:\Music\# Metal\Nightwish\2007 - Dark Passion Play (Gold Box Edition)",
        r"D:\Music\# Metal\Serenity",
        r"D:\Music\# Metal\Sirenia",
        r"D:\Music\# Metal\Stream of Passion",
        r"D:\Music\# Metal\Temperance",
        r"D:\Music\# Metal\Van Canto",
        r"D:\Music\# Metal\Visions of Atlantis",
        r"D:\Music\# Metal\Warkings",
    ]

    files = get_files(paths)

    os.makedirs("data", exist_ok=True)

    with open("data/lyrics.json", "w", encoding="utf-8") as f:
        for i in tqdm(files):
            r = get_lyrics_from_tag(i).dict()
            f.write(json.dumps(r))
            f.write("\n")
