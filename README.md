# Dofusbot

Dofusbot is an automated program made to harvest ores in the video game dofus.
It uses YOLOv8 nano version with a pre-trained model to identify ores.
The current bundled model used around 40 screenshots and looped through 1000 epochs to learn what is a ore.
You can use the 'best.pt' file packaged inside this project, or make your own model !

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.


## Usage

```bash
python main.py
```
Select what you need to harvest (mining is the only job available) and let the program do it for you.

## License

[MIT](https://choosealicense.com/licenses/mit/)
