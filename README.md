# LABDA Parsers

[![pypi](https://img.shields.io/pypi/v/labda-parsers.svg)](https://pypi.python.org/pypi/labda-parsers)
[![downloads](https://static.pepy.tech/badge/labda-parsers/month)](https://pepy.tech/project/labda-parsers)
[![versions](https://img.shields.io/pypi/pyversions/labda-parsers.svg)](https://github.com/labda-lib/parsers)
[![license](https://img.shields.io/github/license/labda-lib/parsers.svg)](https://github.com/labda-lib/parsers/blob/main/LICENSE)

A package designed to extract data from movement sensors such as accelerometers and GPS devices.

Supported formats: **Actigraph** (gt3x), **Axivity** (cwa), **Sens** (bin).

## Installation

Install using `pip install -U labda-parsers`.

## A Simple Example

```python
from labda_parsers import Sens

sens_parser = Sens()
df = sens_parser.from_file('../data/sens.bin')

print(df.head)
#>                                     acc_x     acc_y     acc_z
#>datetime  
#>2024-09-02 08:08:50.227000+00:00  0.218750 -0.171875 -0.773438
#>2024-09-02 08:08:50.307000+00:00  0.257812 -0.203125 -0.937500
#>2024-09-02 08:08:50.387000+00:00  0.242188 -0.226562 -0.953125
#>2024-09-02 08:08:50.467000+00:00  0.234375 -0.242188 -0.945312
#>2024-09-02 08:08:50.548000+00:00  0.257812 -0.226562 -0.953125
```
