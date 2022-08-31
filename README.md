# Docassemble Override Forms

Automation script for creating override forms at Financial Horizons.

## Setup instructions

- Install docassemble (see [How to install docassemble](https://docassemble.org/docs/installation.html))
- Log in to admin account
- Set up the [Configuration](https://docassemble.org/docs/config.html)

  > ⚠️ Make sure that any newly-added property in the YAML file is not already defined in the file.

  - Email

    Email config is required to send emails to carriers, see [E-mail configuration](https://docassemble.org/docs/config.html#mail)

    SMTP is likely the best option to work with FH's Microsoft Exchange server.
  - Translations

    Make sure the `words` property (used to translate words in interviews) is set to the below code. See [words](https://docassemble.org/docs/config.html#words)

    ```yaml
    words:
      - docassemble.base:data/sources/us-words.yml
      # adds french translation for docassemble
      - docassemble.base:data/sources/fr-words.yml
      # adds french translations for override form interview
      - docassemble.fhoverrideforms:data/sources/words.yml
    ```
- In 'Package Management', install this package using the Github URL (i.e. https://github.com/bensengupta/docassemble-fhoverrideforms)
- The interview should now be accessible at https://YOUR_DOCASSEMBLE_URL/fhoverrideforms/interview?new_session=1
  - For user-friendly URLS, see the [`dispatch` directive](https://docassemble.org/docs/config.html#dispatch) (the interview name is `docassemble.fhoverrideforms:data/questions/interview.yml`)
- Note that emails will not send to carriers until the `DEBUG_EMAIL = True` line is set to `DEBUG_EMAIL = False` in `override_forms.py`. To do this, you can make changes via GitHub in your browser or set up the playground (see below instructions) and edit the file in the 'Modules' section

## Development setup instructions

- If possible, the docassemble docs recommends running a separate instance of docassemble for development since changes to interview files often require a full server restart and might inconvenience users.

- Set up [GitHub integration](https://docassemble.org/docs/packages.html#github) (or another integration) to back up and track version history of interview files.

  Note that if you wish to delete a file in the Playground, you must also manually delete it on GitHub.
- Set up the playground
  - Open the Playground, click on arrow on top left and click 'Manage Projects'
  - Create a new project
  - Folders > Packages > Pull
  - Enter GitHub URL and click Pull
  - The package is now ready to edit in the playground
    
    If you configured GitHub integration, you should see a GitHub button at the bottom of the packages screen to push changes to GitHub

    Make sure you are running the main interview file `interview.yml`. Running the other files will not work.