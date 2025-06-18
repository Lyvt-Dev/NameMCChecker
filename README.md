---

# NAMEMC Checker :3

🧱🚀 This Python script generates Minecraft usernames based on customizable criteria and checks their availability on NameMC in real-time, using multiple CPU cores for speed.

---

## Features

* Generate all possible names of a given length using letters, numbers, underscore `_`, and dash `-` (customizable)
* Check availability of generated names on [NameMC](https://namemc.com)
* Multi-core processing with configurable number of instances
* Live progress display with ETA (estimated time remaining)
* Saves all available names into a file `names.txt`
* Friendly console output with color coding (via `colorama`) (it looks buns :()

---

## Requirements

* Python 3.7+
* Click on the `download.cmd` and let it make the magic <3

---

## Usage

Run `download.cmd`

You will be asked to provide:

* Desired username length (3-16 characters)
* Whether to allow numbers, underscore, and dash in names
* How many CPU cores (instances) to use for parallel checking (max your CPU cores)

The script will then generate all possible combinations, check availability on NameMC, and show a live progress bar with estimated time remaining.

Available names found are saved to `names.txt`.

---

## Notes

* Avoid setting `SLEEP_TIME` too low to prevent being rate-limited or blocked by NameMC. (its on default on 0 bcz i am lazyyy!!!)
* The script may take a long time for large name lengths due to combinatorial explosion.
* Use responsibly and respect NameMC’s terms of service.

---

## License

MIT License — feel free to use and modify.

---
