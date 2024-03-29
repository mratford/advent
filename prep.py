import os
from pathlib import Path

YEAR = "2023"

nb_template = """{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "268eeed3-4573-4b1d-9cb6-43d41b160b24",
   "metadata": {},
   "source": [
    "# Day x \\n",
    "## Part 1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "494f7b41-a035-4dd5-bf3d-79a642bc558b",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (AoC)",
   "language": "python",
   "name": "advent"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}"""


os.makedirs(YEAR, exist_ok=True)

for day in range(1, 26):
    zeroday = f"day{day:02}"
    os.makedirs(os.path.join(YEAR, zeroday), exist_ok=True)

    with open(os.path.join(YEAR, zeroday, zeroday + ".ipynb"), "w") as f:
        f.write(nb_template.replace("Day x", f"Day {day}"))
