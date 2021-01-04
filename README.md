# abtest-tools
![](https://github.com/taylorplumer/abtest-tools/blob/master/img/min_sample_size_calculator_screenshot.png)

### Introduction
This repo is intended to provide open source tools for ab testing. The intitial tool is a minimum sample size calculator. It is a Dash app that can be run locally. Next steps include extending functionality of the app to include visualizations to aid in the end user's intuition of the statistical parameters involved.

###  Installation
This project utilizes default packages within the Anaconda distribution of Python. Dash will also need to be installed.

You can install the conda environment with dependencies using the following command:

```
conda create --name <env> --file requirements.txt
```

### Acknowledgements
The inspiration for the minimum sample size calculator comes from [Evan's Awesome A/B Tools](https://www.evanmiller.org/ab-testing/sample-size.html).
The min_sample_size.py function is pulled from [Nguyen Ngo's ab-framework repo](https://github.com/mnguyenngo/ab-framework/blob/master/notebooks/min_sample_size.ipynb)
