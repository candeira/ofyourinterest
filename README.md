OfYourInterest
===

Calculate interest for a Fixed Term Deposit maturing in a set number of years.

Possible enhancements
---

#### More Features
- calculate maturity date given a date
- for monthly and quarterly accumulation schedules, allow maturity of multiples of months and quarters
- allow additional monthly deposits
  - (would probably model them as separate fixed term deposits which would be aggregated seamlessly as a single "product")

#### More Engineering
- Property testing and more edge cases for the calculator
- Dependabot for checking dependency vulnerabilities
- The rounding to cents and to dollars should be in a library module, not ad-hoc
- The parser should be modular to accept different types of conditions depending on the newly added features

Tasting Notes
===

Starting point
---

I've hidden the implementation a bit by leaving it in [a PR in a branch](https://github.com/candeira/ofyourinterest/pull/1).

Quick start
---
This project requires a modern Python, mostly for the typing syntax. It's been developed on 3.13.

Tested on 3.9 locally (where it passed until I updated some deprecated typing syntax, rather than remove the linting rules, too late to go back now), and on 3.12 by a Github Action.

1. Clone the project from GitHub at `(https://github.com/candeira/ofyourinterest)[https://github.com/candeira/ofyourinterest]`.

2. Check out the `ferociously` branch.

3. Now you're ready to look at the project!

- Browse around if you will, or run `git log` maybew?
- In a terminal, make sure you're in the project's base directory, the one containing `src` and `tests`.
- Create a virtualenv using your preferred method, or `python3.13 -m venv .venv` for the exact same Python version.
- Activate the virtualenv using your preferred method, or `source .venv/bin/activate`.
- Install the project's dev dependencies with `python -m pip install -r requirements_dev.txt`
- Run tests with `python -m pytest` or `make test`
- (Optional) Run tests on all your installed/available python versions with `make test-all`. This uses tox, and makes sense if building a library.
- Run linter with `python -m ruff check` or `make lint`
- Run type-checking with `python -m mypy`. It will take a long time the first run and be faster in subsequent runs.

4. Now you know the project is tested, it's time to find out whether it works!

- Install the package with `python -m pip install -e .`
- Run the command by typing `ofyourinterest` and follow the online help

On the shoulders of giants for tooling
---
The project is based on a cookiecutter template to make a PyPI package. It's designed as a package to be published to PyPI, the Python package index.

Design Tradeoffs and Constraints
---

I decided to follow the features in the brief exactly as requested, no additional frills.

However, I wanted to explore an implementation depending only stdlib imports, no external libraries.

I ended up spending some "me time" building a little validator/exception object. In production, I would have used Pydantic. But this was my fun time, so I built an entertaining kludge.

Architecturally, the kludge is separate from the functionality, and could be replaced by a Pydantic validator that parses the input into the object used by the calculations.

I reckon I spent about 6 hours wall time on this project, with about 5 hours actual coding, of which about half was spent figuring out the weird validator and its typing, and fighting the project template a little. Using Pydantic and a template I'm familiar with, this would have been a 2-3 hour project.

I'm also spending time now cleaning up the Readme and checking every single command in the quick start section before sending the email back.

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
