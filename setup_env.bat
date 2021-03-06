call pip install jupyterlab
call conda create -n py36 python=3.6

REM =============== PACKAGES ==============

call conda activate py36
call conda install pandas=0.24.2 requests=2.22.0 tqdm=4.31.1 seaborn=0.9.0 ipykernel=5.1.1 keras=2.2.4 lightgbm=2.2. ipywidgets=7.4.2 lxml=4.3.2 bottleneck=1.2.1
call conda install -c conda-forge eli5 Skater shap mlxtend
call conda install -c anaconda py-xgboost


REM ================= TALIB ===============


powershell -Command "(New-Object Net.WebClient).DownloadFile('https://drive.google.com/uc?export=download&id=12JbxNQcVLYbvx-ASb5BtgF0mNiHgNfyy', 'TA_Lib-0.4.17-cp36-cp36m-win_amd64.whl')"

python -m pip install TA_Lib-0.4.17-cp36-cp36m-win_amd64.whl

python -m pip install pyfolio==0.9.2



REM ============= KERNEL SETUP ============

python -m ipykernel install --user --name py36

call conda deactivate

REM ======== JUPYTER LAB IPYWIDGETS ======

call conda install nodejs
call jupyter labextension install @jupyter-widgets/jupyterlab-manager

REM ================ CHECK ===============
call conda activate py36

powershell -Command "(New-Object Net.WebClient).DownloadFile('https://drive.google.com/uc?export=download&id=1GQzRpMN_RR1v9kXWOXn5BXMHKfyk0ET4', 'check.py')"
call python check.py