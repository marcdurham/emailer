# Installing emailer in Docker

Using Docker may be helpful to keep the Python environment clean.  Or maybe it's too complicated.  But here's some instructions if you want to try.

## 1. Install Docker on your server.

You can rent a Linux server for about $5 a month at digitalocean.com, or maybe cheaper at Google Cloud Platform or Amazon Web Services.

Ubuntu install instructions here: https://docs.docker.com/install/linux/docker-ce/ubuntu/

## 2. Copy these files over.

Copy the files in this folder into your server, in the "emailer" folder in your home folder (`~/emailer/`).

* `cron.sh` - needed because cron doesn't know your PATH
* `docker-compose.yml` - tells docker how to setup the volumes and build the file
* `Dockerfile` - sets up Python, installs emailer, and runs emailer

## 3. Setup emailer

Copy the [emailer/sample-emailer.json](../../emailer/sample-emailer.json) file to your server and rename it `~/emailer/emailer.json`.

Then replace the apropriate fields.

Also open up `Dockerfile` and replace `mykey` with `testkey` or whatever you named the key under `keys` it in your `emailer.json`.

## 4. Build the docker container

Run `docker-compose build` from inside the `~/emailer/` folder.

This will download python, and install emailer and it's depenencies into a container.  So it won't mess with your system's python environment.

Docker Compose is being used, because it is good at passing variables to `docker run` like the volume, and naming the container.

## 5. Run emailer to make sure it has OAuth access.

We need to run emailer once now to save your login to google.

Run `docker-compose run --rm emailer email -v --test --all-keys`

Copy the OAuth URL, and paste it into the browser, login as the user that will be sending email (Maybe create a new gmail account just for this).  If there was an error about setting up gmail or sheets APIs, then follow the error's instructions and set that up.

## 6. Setup Cron to run this daily.

On the server type `crontab -e`.  This will probably open up your cron in VIM, so here's some specific instructions including saving and exiting vim. :tada:

In the following command, `55 18 * * *` means at minute 55 of the hour 18, or 2:55pm every day.  So change those numbers as you see fit.

* Press the down arrow until you get to the bottom.  Then press 'o' to start a new line.
* Type: `55 18 * * * $HOME/emailer/cron.sh >> $HOME/emailer/log.log 2>&1`
* Then press ESC
* Now type ZZ

Any errors will be saved in the `~/emailer/log.log` file.  And you can look at the time of the file or `sudo grep cron /var/log/syslog` to see when the command last ran.

Hope that helps!
