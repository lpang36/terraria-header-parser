A header parser and editor for Terraria (1.3.5.3 only, tested on Linux). Additional sections not implemented. utils.py taken from Omnitool's [tlib](https://github.com/Berserker66/omnitool/blob/master/omnitool/tlib.py). Made this to solve a [glitch](https://forums.terraria.org/index.php?threads/time-and-background-glitch-1-3-5-3-linux-mint-18-2.86085/) I had where the time did not reset, fix as follows:
```python
from parser import World
input_file = 'world.wld'
output_file = 'world_fixed.wld'
w = World()
w.load(open(input_file, 'rb'))
# sandstorm severity was set to nan for some reason
w['header']['sandstorm_severity'] = 0
w.store(open(output_file, 'wb'))
```
