# tasktracker

[![CI](https://github.com/sahilkalgutkar/tasktracker/actions/workflows/ci.yml/badge.svg)](https://github.com/sahilkalgutkar/tasktracker/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/sahilkalgutkar/tasktracker/branch/main/graph/badge.svg)](https://codecov.io/gh/sahilkalgutkar/tasktracker)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A small command-line task tracker I wrote in Python to keep a to-do list in a
single JSON file, with no database and no dependencies outside the standard
library.

This is an early project of mine and I have kept it deliberately small. It is
here as a tidy, working example rather than a platform — for the larger systems
work, see my [profile](https://github.com/sahilkalgutkar).

## What it does

- Adds a task with a title and a description
- Lists every task with its status and timestamps
- Marks a task done or inactive
- Deletes a task
- Persists everything to a JSON file between runs

Every task carries a status of `active`, `done`, or `inactive`, plus
`created_at` and `updated_at` timestamps that I set whenever the task changes.

## Installing

I recommend a virtual environment, since the install adds a `tasktracker`
command to your `PATH`:

```bash
git clone https://github.com/sahilkalgutkar/tasktracker.git
cd tasktracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Using it

```bash
tasktracker add --title "Write the README" --description "The real one"
tasktracker list
tasktracker done --title "Write the README"
tasktracker inactive --title "Write the README"
tasktracker delete --title "Write the README"
```

You can also run it without installing, straight from a clone:

```bash
python -m tasktracker.cli list
```

## Where tasks are stored

By default I write to `tasks.json` in whatever directory you run the command
from, so a task list belongs to a folder rather than to your whole machine.
Set `TASKTRACKER_STORE` to put it somewhere else, or to keep more than one list:

| Variable | Default | What it does |
| --- | --- | --- |
| `TASKTRACKER_STORE` | `tasks.json` in the working directory | Path to the JSON file holding the tasks |

```bash
TASKTRACKER_STORE=~/.tasks.json tasktracker list
```

The file is created on first write, so there is nothing to set up beforehand.

## Running the tests

```bash
pip install -r requirements.txt
pytest --cov=tasktracker --cov-report=term-missing
```

Each test gets its own temporary store, so the suite is repeatable and never
writes into your working directory. CI runs it twice on purpose to prove that:
the original tests shared one `tasks.json` and passed only on a clean checkout,
failing on the second run once the earlier run's tasks were still sitting in
the file.

## License

MIT — see [LICENSE](LICENSE).
