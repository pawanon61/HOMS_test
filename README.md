```ssh to psbuild-rhel<x>```

source the conda environment: ```source /reg/g/pcds/pyps/conda/pcds_conda```

open HOMS_tst.ipynb through jupyter notebook and run each cell from top

for GUI: ```/reg/g/pcds/epics/ioc/fee/homs/R1.2.1/homsScreens/edm-homs.cmd```

the notebook displays output for current run and logs it into 'HOMS_tst.log' file in the same directory


*NOTE:*
Jupyter notebook might give ImportError. This problem occurs when editing the external code and jupyter notebook at the same time. It gives that error when reloading the external file after the first time it is imported.
The solution is to delete the external python cache directory __pycache__ OR restart the Jupyter notebook kernel (Kernel --> Restart). Doing both of these will force Jupyter to read a new/fresh copy of the external file, recognizing new symbols and other modifications as a result.




