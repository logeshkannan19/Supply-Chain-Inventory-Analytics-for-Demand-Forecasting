# Contributing to Supply Chain Analytics

First off, thank you for considering contributing to the Supply Chain Analytics repository! It's people like you that make building transparent data tools such a great endeavor.

## 1. Where do I go from here?
If you've noticed a bug or have a feature request, make sure to check our **Issues** tab to see if someone else in the community has already created a ticket. If not, go ahead and make one!

## 2. Fork & create a branch
If this is something you think you can fix, then fork the repository and create a branch with a descriptive name. 

A good branch name would be (where issue #325 is the ticket you're working on):
`git checkout -b 325-add-lstm-forecasting`

## 3. Implementation Guidelines
- **Keep it modular**: If you are adding a new model, create a new script in `/src/models/` rather than appending huge classes into existing files.
- **Documentation**: All new methods must include Python docstrings explicitly defining Arguments, Returns, and Exceptions.
- **Type Checking**: We prefer Type Hints (`def function(a: int) -> str:`).

## 4. Make a Pull Request
Once you are finished, verify your code runs properly end-to-end:
```bash
python src/generate_data.py
python src/preprocess.py
python src/forecasting.py
```
If everything functions successfully with zero crashes, push your commits and create a Pull Request on GitHub. 
