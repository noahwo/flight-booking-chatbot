# flight-booking-chatbot
A chatbot of flight book assistant based on RASA framework.

### Deployment

To deploy this chatbot, required steps are listed below. The development environment of this project is WSL2, for which is subsystem is Ubuntu 20.04 LTS, the host system is Windows 11.

#### Python environment

This program is developed and tested under Python 3.7, using Conda as environments manager. 

##### Conda env

Create a virtual env of Python 3.8, and activate is. Note that every step later on in this project should be surely in this env, meaning you may need to manually activate, or define the command in bash file.

+ create a new env
	```
	conda create --name=py38 python=3.8
	```
	
+ activate the env
	
	```
	conda activate py38
	```

#### Rasa X installation

The following versions of packages were installed for development

````bash
```
pip3 install SQLAlchemy==1.3.22
pip3 install sanic-jwt==1.6.0
pip3 install rasa==2.8.2
pip3 install rasa-sdk==2.8.1
sudo apt install gcc
# skip next one if rasa-x is not needed
pip3 install rasa-x==0.42.0 --extra-index-url https://pypi.rasa.com/simple

```
````

##### Note of versions

 There are some feasible combinations of package versions:
   - Rasa 2.6.3 - Rasa SDK 2.6.0 - Rasa X 0.40.0
   -  Rasa 2.8.2 - Rasa SDK 2.8.1 - Rasa X 0.42.0

The [Compatibility Matrix](https://rasa.com/docs/rasa-x/changelog/compatibility-matrix/) should be followed:

| Rasa X | Rasa Open Source | Rasa SDK |
| ------ | ---------------- | -------- |
| 0.42.x | 2.8.x            | 2.8.x    |
| 0.41.2 | 2.7.1            | 2.7.0    |
| 0.40.0 | 2.6.2            | 2.6.0    |
| 0.39.0 | 2.5.0            | 2.5.0    |
| 0.38.0 | 2.4.0            | 2.4.0    |
| 0.37.0 | 2.3.1            | 2.3.1    |
| 0.36.0 | 2.3.1            | 2.3.1    |

#### Run Rasa and Rasa X

To run Rasa X, execute the following command in the project directory
```bash
rasa x
```
> Learn more about CLI commands of rasa/rasa-x, see [this](https://rasa.com/docs/rasa/command-line-interface/).

To deploy the chatbot on the local server and interact through web UI, follow the commands below
Run these commands in three seperated terminals/shells
``` bash
# to start rasa server
rasa run --enable-api --cors "*" 
# to start action server
rasa run actions 
# to start http server on localhost
python -m http.server 
```
To run without output, run with the following options

``` bash
nohup rasa run --enable-api --cors "*" &
nohup rasa run actions &
nohup python -m http.server &
```

To access the local server of Rasa chatbot
```bash
localhost:8000/web.html
```