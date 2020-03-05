# College Track One Off Projects

A collection of projects, organized by the year they started, that were requested via Zen Desk or other means. Each projects follows a general the same general structure as created by a Cookie Cutter Template. This repository doesn't contain any raw data files, but those files should live on an analogous folder in the OP Box One Off folder.

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

Make sure you update the following values in the newly created .env
```
SF_TOKEN=<your salesforce token>
SF_USERNAME=<your salesforce username>
SF_PASS=<your salesforce password>
```

