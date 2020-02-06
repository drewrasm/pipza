# pipza

## welcome to the coolest way to order your pizza

* Getting Started
  * required dependencies: pizzapi - the Domino's api wrapped for python https://github.com/gamagori/pizzapi
  * *Reccomended* Setting up an environment: use virtualenv https://virtualenv.pypa.io/en/latest/installation.html
    > pip install virtualenv
  
  * After you environemnt is set up and you are in the project directory run
    >source env/bin/activate
  * Install pizzapi
    > pip install pizzapi
* Setting up your config.js file
  * there is an example that you can replicate called config_example.json that has all the fields you'll need in your config.json. This will make running the script faster, but you can opt to use custom settings even after you've filled in your config.json
  
* Running the Script
  * after you are in your environment (source env/bin/activate) run the script by running
  > python3 pipza.py [args]
    * the available arguments are -help, -default, and -custom
    * -help: displays a small documentation of the available commands
    * -default: uses all the default values it can from the config.json file (except the actual order, which you can choose to use or not during the script's execution)
    * -custom: permits the user to input all of the values for the order
  
