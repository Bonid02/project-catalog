# Project Catalog (Inventory Catalog)

## App Pre-requisites

### Git

If you don't already have Git installed, [download Git from git-scm.com.](http://git-scm.com/downloads) Install the version for your operating system.

On Windows, Git will provide you with a Unix-style terminal and shell (Git Bash).  
(On Mac or Linux systems you can use the regular terminal program.)

You will need Git to install the configuration for the VM. If you'd like to learn more about Git, [take a look at our course about Git and Github](http://www.udacity.com/course/ud775).

### VirtualBox

VirtualBox is the software that actually runs the VM. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Downloads)  Install the *platform package* for your operating system.  You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

**Ubuntu 14.04 Note:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a [reported bug](http://ubuntuforums.org/showthread.php?t=2227131), installing VirtualBox from the site may uninstall other software you need.

### Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.  [You can download it from vagrantup.com.](https://www.vagrantup.com/downloads) Install the version for your operating system.

**Windows Note:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.


### App Files

Download the files in github https://github.com/Bonid02/project-catalog


### Run the virtual machine!

Using the terminal, change directory to project-catalog (**cd project-catalog**), then type **vagrant up** to launch your virtual machine.


### Running the Inventory Catalog App

Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type **exit** at the shell prompt.  To turn the virtual machine off (without deleting anything), type **vagrant halt**. If you do this, you'll need to run **vagrant up** again before you can log into it.

Now that you have Vagrant up and running type **vagrant ssh** to log into your VM.  change to the /vagrant directory by typing **cd /vagrant**. This will take you to the shared folder between your virtual machine and host machine. Then **cd /inventory-catalog to view the app files.

Create the database first by running **python database_setup.py**. Then to add sample data run **python items_sample_data.py**

If all went ok, run the webserver app type **python items_catalog.py**.


## Website UI

To access website type in your web browser(preferably FF or Chrome) **http://localhost:8000/**

You will be directed to read only page mode. In this mode you will only be able to :
* View the entire catalog.
* View the items listed in a category.
* View the item details.

Login currently only supports google account login. Once logged in you will be directed to the full version of the page. In this mode you will be able to:
* View the entire catalog.
* View the items listed in a category.
* View the item details.
* Add an new item to a category.
* Edit an item.
* Delete an item.

### JSON format

This app also supports JSON view of the database.
To view all items type in you browser **http://localhost:8000/catalog.json**
To view a category and it's item **http://localhost:8000/category/<int:category_id>** 
* sample **http://localhost:8000/category/3**

To view a single item **http://localhost:8000/item/<item_id>** 
* sample **http://localhost:8000/item/1**