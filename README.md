## Requirements
- docker
- python3
- postgres
- pyenv, pyenv-virtualenv
- terraform

## Setup Mac OSX
For local dev I like to use pyenv and the virtualenv plugin. 
```
brew update
brew install pyenv
brew install pyenv-virtualenv
brew isntall terraform
```

## Setup Workspace
Install python 3.7.3, create a virtualenv for wsbbot. Then activate it in your working directory and install dependencies.
```console
pyenv install 3.7.3
pyenv virtualenv 3.7.3 wsbbot
cd <project directory>
pyenv activate wsbbot
pip install --no-cache-dir -r requirements.txt
```

## Migrations
Data base migrations are managed by flask. Run the following to generate a migration script in the migrations folder once you are done with model changes.
```console
FLASK_APP=tools/manage.py flask db migration
```
Next you'll want to actually make those changes in the database.
```console
FLASK_APP=tools/manage.py flask db upgrade
```
Don't forget to check in your migration script.

## Run the server
```console
docker-compose up -d
FLASK_APP=main.py flask run
```

## Deploy Infrastructure
```console
terraform init
terraform plan
terraform apply
```

## Destroy Infrastructure
A note about destroy. There is an outstanding bug with tearing down an aws_ecs_cluster provisioned with capacity_providers. As such you'll need to manaually destroy the auto-scaling-group in the AWS Console or CLI. There is a workaround for this, but waiting on Terraform to provide a fix. 
<br><br>
For more context see this github [issue](https://github.com/terraform-providers/terraform-provider-aws/issues/11409). 
```console
terraform destroy
```