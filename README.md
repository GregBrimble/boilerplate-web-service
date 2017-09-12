# Boilerplate Web Service
My bare minimum web service deployment

## Setup
1. Clone this repository to wherever you want to deploy.
2. Run `./setup.sh` to build dependencies into `venv`, and will set the `git remote upstream` to point to this repository.
3. Activate any of the features below.

## Features

### Automatic Deployment
Automatic deployment allows you to update a deployment with every push to a GitHub repository.

#### GitHub Webhook
1. Visit https://github.com/YOUR_GITHUB_USERNAME/YOUR_GITHUB_REPOSITORY/settings/hooks/new.
2. Enter the values below:

   | Option                                               | Value                                                                                                             |
   | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
   | Payload URL                                          | Deployment URL + `/meta/github_hook` (e.g. `https://gregbrimble.com/meta/github_hook`)                            |
   | Content type                                         | `application/json`                                                                                                |
   | Secret                                               | Run the following in your terminal: `ruby -rsecurerandom -e 'puts SecureRandom.hex(20)'`, and put the output here |
   | Which events would you like to trigger this webhook? | Just the `push` event.                                                                                            |
   | Active                                               | Checked                                                                                                           |

3. Set the following environment variables on the deployed machine:
   ```ini
   WS_AUTO_DEPLOY=GITHUB_HOOK
   WS_AUTO_DEPLOY_GITHUB_HOOK_SECRET=mySuper5ecretSecr3t!
   ```
   where `mySuper5ecretSecr3t!` is the `Secret` you generated earlier.

### Heroku
1. Follow the steps outlined for [Automatic deploys](https://devcenter.heroku.com/articles/github-integration#automatic-deploys) in [this guide in Heroku's own documentation](https://devcenter.heroku.com/articles/github-integration).
2. Set the following environment variables on the deployed machine:
   ```ini
   WS_AUTO_DEPLOY=HEROKU
   ```
