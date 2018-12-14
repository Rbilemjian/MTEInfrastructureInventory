MTE Infrastructure Inventory
-

<br>

<h3>Technologies Used</h3>

<br>

<strong>Back-end / Server-Side Logic</strong>
    
    Python using the Django Framework
    
<strong>Front-end Logic</strong>

    JQuery, Javascript

<strong>Front-end Styling</strong>

    HTML, CSS, Bootstrap

<br>

<h3>Overall Design of the application</h3>

<br>

<strong>Back-end</strong>

Designations of URLs and view functions to be called when they are visited contained in the file:

    urls.py

Definitions for tables and relationships within the database are contained in the file:

    models.py
    
Definitions & logic for forms and auto-fill suggestions for them are defined in the file:
    
    forms.py
    
Logic for view behavior (GET and POST requests) are contained in the files:

    views.py    infoblox_views.py
  
<strong>Front-end</strong>

All HTML files can be found in the folder 

    templates

There is some custom logic that executes within the Django templating system defined in the folder

    templatetags
    
Some custom CSS and Javascript exists in the following files

    styles.css (in static folder)
    script.js (in the bootstrap distribution/js folder)
    
<br>

<h3>App Deployment on CentOS Server</h3>

<br>

<strong>Installing MySQL</strong>

    https://www.tecmint.com/install-latest-mysql-on-rhel-centos-and-fedora/
    
Following installation and securing the MySQL installation as per the linked tutorial, enter into the
MySQL command line and create a database called "mteinfrastructure"

<strong>Installing & using Git</strong>

Install Git with the following command:

    yum install git
    
CD into the home directory and run the command

    git clone https://github.com/Rbilemjian/MTEInfrastructureInventory.git
    
Find the settings.py in the following directory:

    /home/mteinfrastructureinventory/infrastructureinventoryproject/infrastructureinventoryproject
    
Delete the current settings.py file and run the following command to make the production_settings.py the new main settings.py file:

    mv production_settings.py settings.py
    
    
<strong> Installing Python </strong>

You will want to install Python version 3.4.8 for this application.
A guide to install 3.6 (same thing but use a 4 instead of a 6) can be found at:

    https://dev.to/lechatthecat/how-to-install-python3-in-centos7-1bk6
    
<strong>Installing Virtual Environment, Django, Setting up Apache</strong>

Here is a guide to give an idea of the process (the guide also covers configuring apache):

    https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-centos-7
    
If there are problems setting up the virtual environment with that guide, this guide does it slightly differently:

    https://dev.to/lechatthecat/how-to-install-django-in-centos7-vm-2f5i
    
Once the virtual environment is set up, it can be activated with the following command:

    source your-env-name-here/bin/activate

Once that is activated, Django and package requirements can be installed wherever the requirements.txt file is located in the project
directory with the command:

    pip install -r requirements.txt
    
Create a directory called static_root within /home/mteinfrastructureinventory directory and run following command as well
in order to place all the static files for the project where they need to be:

    python manage.py collectstatic
    
Make sure to create a migrations folder in the following directory if it does not already exist and create an empty file called "__init__.py" within it:

    /home/mteinfrastructure/infrastructureinventoryproject/infrastructureinventoryapp
    
Then you can run the following commands in the same directory as the manage.py file:

    python manage.py makemigrations
    python manage.py migrate
    
You can create a superuser with the following command: 

    python manage.py createsuperuser
    
That user can then log into the admin panel and add other users who will then be able to log into the application using their guardhouse credentials

<br>

<h3>Modifying Application Parameters</h3>

<br>

If the credentials for Infoblox need to be updated, this can be done by updating any instance of "auth=('someusername', 'somepassword')" to be the new username and password in the following file (there are 3 instances): 

    infoblox_views.py
    
If the time-out needs to be changed, it can be modified by changing the comparison of "diff", which is currently diff<20, to be diff<x where x is the desired timeout period. 
This change should be done in the same file as the credential change above:

    infoblox_views.py
    

    


    
    

    

    


