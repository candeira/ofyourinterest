OfYourInterest
===

Calculate interest for a Fixed Term Deposit maturing in a set number of years.

Possible enhancements
---
- calculate maturity date given a date
- for monthly and quarterly accumulation schedules, allow maturity of multiples of months and quarters
- allow additional monthly deposits
  - (would probably model them as separate fixed term deposits which would be aggregated seamlessly as a single "product")

Tasting Notes
===

Quick start
---
This project requires a modern Python. It's been developed on 3.13 and also tested on 3.9 locally, and on 3.12 by a Github Action.

1. Clone the project from GitHub at ``.

2. Check out the `ferociously` branch.

3. Now you're ready to look at the project!

- Make sure you're in the project's base directory, the one containing `src` and `tests`.
- Create a virtualenv using your preferred method, or `python -m venv .venv`.
- Activate the virtualenv using your preferred method, or `source .venv/bin/activate`.
- Install the project's dev dependencies with `python -m pip install -r requirements_dev.txt`
- Run tests with `python -m pytest` or `make test`
- Run tests on all your installed/available python versions with `make test-all`. This uses tox, and makes sense if building a library.
- Run linter with `python -m ruff check` or `make lint`
- Run type-checking with `python -m mypy`. It will take a long time the first run and be faster in subsequent runs.

4. Now you know the project is tested, it's time to find out whether it works!

- Install the package with `python -m pip install -e .`
- Run the command by typing `ofyourinterest` and follow the online help

On the shoulders of giants for tooling
---
The project is based on a cookiecutter template to make a PyPI package. It's designed as a package to be published to PyPI, the Python package index.

Design Tradeoffs
---

I decided to follow the features in the brief exactly as requested, no additional frills.

However, I wanted to explore using only stdlib imports, so I ended up spending some "me" time building a little validator/exception object. In production, I would have used Pydantic. But this was fun time, so I built a kludge.

Architecturally, the kludge is separate from the functionality, and could be replaced by a Pydantic validator that parses the input into the object used by the calculations.

Testing
---

 I created sample test data from the suggested calculator. In a production environment, I'd advocate for property testing via Hypothesis (in Python) or similar.

CI
---

The chosen cookiecutter template makes it easier to publish the package to PyPI or to a private registry such as artifactory on merging to main.

For simplicity and to remove noise I haven't configured that push. However, CI runs tests before merging.

Additional automation
---
- I've set pre-commit git hooks that will run the linter, type-checker and tests and not accept a commit unless they pass or the `-n` flag is invoked.


Credits
---

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
