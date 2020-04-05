# Cisco HyperFlex Datastore Cleanup

The HyperFlex Datastore Cleanup Script for Cisco HyperFlex utilizes the HyperFlex API to automatically delete any datastores that have met or exceeded a specified retention time limit. The ability to exempt any datastores from the retention time limit is provided.

This script is intended for use on Cisco HyperFlex systems in demonstration or training environments. Do not use on production systems.

## Prerequisites:
1. Python 3 installed, which can be downloaded from [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Clone or download the Cisco HyperFlex Datastore Cleanup repository using the ![Gitub Clone or download](./assets/Github_Clone_or_download_link_button.png "Github Clone or download") link at [https://github.com/ugo-emekauwa/hx-datastore-cleanup](https://github.com/ugo-emekauwa/hx-datastore-cleanup) or run the following command:
    ```
    git clone https://github.com/ugo-emekauwa/hx-datastore-cleanup
    ```
3. Install the required Python modules requests and urllib3. The requirements.txt file in the repository can be used by running the following command:
    ```
    python -m pip install -r requirements.txt
    ```
4. The IP address of the targeted Cisco HyperFlex system.
5. User credentials with administrative rights on the targeted Cisco HyperFlex system.
6. [_Optional_] The names of any datastores on the targeted Cisco HyperFlex system which will be exempt from any retention time limit.


## Getting Started:
1. Please ensure that the above prerequisites have been met.
2. Download the **hx_datastore_cleanup.py** file from this repository here on GitHub.
3. Open the **hx_datastore_cleanup.py** file in an IDE or text editor.
4. Go to the comment section named **Required Variables**, as shown below:
    ```python
    ######################
    # Required Variables #
    ######################
    ```
5. Set the value of the variable named `hx_admin` with the username of the credentials that will be used to access the targeted Cisco HyperFlex system. The value must be a string. For example, here is an entry the sets the username to **admin**:
    ```python
    hx_admin = "admin"
    ```
6. Set the value of the variable named `hx_password` with the password of the credentials that will be used to access the targeted Cisco HyperFlex system. The value must be a string. For example, here is an entry that sets the password to **C1sco12345**:
    ```python
    hx_password = "C1sco12345"
    ```
7. Set the value of the variable named `hx_connect_ip` with the IP address of the targeted Cisco HyperFlex system. The value must be a string. For example, here is an entry that sets the IP address to **192.168.1.100**:
    ```python
    hx_connect_ip = "192.168.1.100"
    ```
8. Set the value of the variable named `hx_datastore_retention_time_limit_hours` with the maximum number of hours that a datastore can be retained on the Cisco HyperFlex system before deletion. The value must be an integer. For example, here is an entry that sets the retention time limit to **24** hours:
    ```python
    hx_datastore_retention_time_limit_hours = 24
    ```
9. [_Optional_] Set the value of the variable named `hx_exempted_datastores_list` by providing the names of any datastores that will be exempt from the retention time limit. The values must be strings separated by commas within the parentheses of the provided empty tuple `()`. For example, here is a sample entry that exempts three datastores from the retention time limit:
    ```python
    hx_exempted_datastores_list = ("datastore1", "datastore2", "datastore3")
    ```
    Here is another example with a sample entry that exempts one datastore from the retention time limit: 
    ```python
    hx_exempted_datastores_list = ("datastore1")
    ```
10. Save the **hx_datastore_cleanup.py** file. The file is now ready for use.


## Author:
Ugo Emekauwa

## Contact Information:
uemekauw@cisco.com or uemekauwa@gmail.com
