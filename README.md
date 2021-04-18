# investment_app
App to manage investment fund on a simple simulated stock market. Project of practicum course MSU 2021

## Build

```
git clone https://github.com/iden-alex/investment_app.git
cd investement_app
pip install -requirements.txt
```

If you have issues with installing kivymd, the library can be installed in another way:

```
git clone https://github.com/kivymd/KivyMD.git --depth 1
cd KivyMD
pip install .
```
## Launch

```
python main.py
```

### Note
There are small delays of a couple of seconds between switching months in the game because of kivymd widget MDDataTable.
