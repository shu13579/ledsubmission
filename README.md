# 64 pixels, three little worlds

Three original, code-generated pixel animations for a 64×64 RGB LED matrix.
The submission GIFs were encoded with [Jixoo](https://github.com/glaforge/jixoo)'s
`GifEncoder` from procedurally drawn RGB frames. No third-party artwork, AI image
generation service, fonts, or API keys are needed.

![Three worlds](previews/contact-sheet.png)

| Artwork | Upload | Size | Loop |
| --- | --- | --- | --- |
| Cosmic Jellyfish | [GIF](submissions/01-cosmic-jellyfish.gif) | 71,233 bytes | 7.68 seconds |
| Neon Rain / Rooftop Cat | [GIF](submissions/02-neon-cat.gif) | 79,828 bytes | 7.68 seconds |
| Orbital Seasons | [GIF](submissions/03-orbital-seasons.gif) | 59,311 bytes | 7.68 seconds |

Each final file is **64×64, square, 96 frames, 80ms per frame, infinitely looping,
and below 5 MB**. The enlarged previews are for viewing only.

## Reproduce

Python 3.10+ and Pillow are needed to draw the frames:

```sh
python -m pip install -r requirements.txt
python generate.py
python verify.py
```

This short path creates visually identical GIFs with Pillow. To reproduce the
submitted GIF encoding with the original Jixoo codec on Windows, install Java
17+ for the selected codec classes, Maven, Git, and Python, then run:

```powershell
./build-jixoo.ps1
# Or pass the path to a Python executable:
./build-jixoo.ps1 -Python 'C:/path/to/python.exe'
```

The script pins Jixoo commit `2703d703d7db530a74555b403f3a4a39f6383b55`,
compiles its ten unchanged image codec/model classes, and uses `JixooExport.java`
to encode the 64×64 raw RGB frames. It downloads `pngj` from Maven Central.
The **full Jixoo library and CLI require Java 21+**; this submission uses only
its image codec. No Jixoo sources are redistributed in this repository.

## Credits

- Artwork and procedural animation: original work in `generate.py`.
- GIF encoding: [Jixoo / glaforge](https://github.com/glaforge/jixoo), Apache-2.0.
- Drawing and independent GIF validation: [Pillow](https://python-pillow.org/).

Original code is available under the MIT license. Original artwork may be used,
modified, and submitted with the project. Third-party tools keep their own licenses.
