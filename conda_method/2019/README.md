# College Track One Off Requests
==============================
This repository holds the files for one-off request that don't warrant their own repository. 


## Installation

### Prerequisites

```
python 3.7
conda 4.7.12
```


### Installing
Clone the repository and switch to the created ddt directory
```
git clone https://github.com/College-Track/one-off
cd one-off
```

* For any time after initial install just run the second command
```
conda env create -f environment.yml
conda activate env
```

Copy the example .env file
```
cp .env.example .env
```

Make sure you update the following values in the newly created .env file
```
SF_TOKEN=<your salesforce token>
SF_USERNAME=<your salesforce username>
SF_PASS=<your salesforce password>
```

Optional - updates the nbconvert LateX template for clear PDF report generation
```
python -m nb_pdf_template.install
```


### General Notes
* All `.ipynb` files are added to git as a markdown (md) file. To convert back all md files back to to `.ipynb` run the following:
```
jupytext --set-formats md,ipynb *.ipynb

``` 

* To convert a single md file run:
```
jupytext --set-formats md,ipynb {file name}.ipynb
```