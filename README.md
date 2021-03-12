## Project Plato - Code Challenge

This is a project based on an assignment given by `undisclosed` company.
The assignment description and currently implemented requirements can be found [here](#assignment-description).

### Table of contents:
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Run Tests](#run-tests)
- [Assignment Description](#assignment-description)

### Prerequisites
* [Python 3.8](https://www.python.org/downloads/)

### Usage
1. Make sure `Python 3.8` is installed and running properly.
1. Open the terminal and go to the directory of this project.
1. Run the following command to run the application.
    ```
    $ python3 main.py [-h] -u URL [-p PATH]
    ```

    **Example**: `python3 main.py -u https://www.cirxsoftware.com -p ./out/`

    | Arguments                                  |                                        |
    | ------------------------------------------ | -------------------------------------- |
    | -h, --help                                 | show this help message and exit| $1600 |
    | -u URL, --url URL                          | the initial URL to start crawling from |
    | -p PATH, --path PATH                       | the path to the output file            |


### Run Tests
1. Make sure `Python3.8` is installed and running properly.
1. In case necessary, activate a virtual environment for this project.
1. Run the following command to install the required packages for this project.
    ```
    $ pip install -r requirements.txt
    ```
1. Run the following command to run the tests.
    ```
    $ pytest
    ```

### Assignment Description

| Requirements                                                                                                                                                                                                                       | Currently Implemented | Within 4-Hour Timebox |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------: | :--------------------:|
| Implement recursive web-crawler of the site                                                                                                                                                                                        | :heavy_check_mark:    | :heavy_check_mark:    |
| Crawler is command-line tool which accept starting url and destination directory                                                                                                                                                   | :heavy_check_mark:    | :heavy_check_mark:    |
| Crawler download the initial url and look to links inside original document (recursively)                                                                                                                                          | :heavy_check_mark:    | :heavy_check_mark:    |
| Crawler does not walk to link outside initial url (if starting link is https://start.url/abc, then it goes to https://start.url/abc/123 and https://start.url/abc/456, but skip https://another.domain/ and https://start.url/def) | :heavy_check_mark:    | :heavy_check_mark:    |
| Crawler should correctly process Ctrl+C hotkey                                                                                                                                                                                     | :x:                   | :x:                   |
| Crawler should be parallel                                                                                                                                                                                                         | :heavy_check_mark:    | :x:                   |                                                                                                                                                          |
| Crawler should supports continue to load if destination directory already has loaded data (if we cancel download and than continue)                                                                                                | :x:                   | :x:                   |

