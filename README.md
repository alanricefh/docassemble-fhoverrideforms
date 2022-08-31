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
- The interview should now be accessible at https://YOUR_DOCASSEMBLE_URL/fhoverrideforms/interview
  - For more user-friendly URLS, see the [`dispatch` directive](https://docassemble.org/docs/config.html#dispatch) (the interview name is `docassemble.fhoverrideforms:data/questions/interview.yml`)
- Emails will not send to carriers until the `DEBUG_EMAIL = True` line (use the search bar) is set to `DEBUG_EMAIL = False` in `override_forms.py`. To do this, you can make changes via GitHub in your browser, or set up the playground (see below instructions) and edit the file in the 'Modules' section
- Set up the `send_email` function in `override_forms.py` with the correct  `sender`, `cc`, and `reply_to` parameters (see [`send_email`](https://docassemble.org/docs/functions.html#send_email))

## Development setup instructions

- If possible, the docassemble docs recommends running a separate instance of docassemble for development since changes to interview files often require a full server restart and might interfere with users performing interviews.

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

## Notes

Docassemble stores interview answers server-side, and does so by establishing a session with a cookie on the browser. This feature is useful for saving/resuming interviews or even transferring interviews to another device while keeping progress (achieved by transferring the session cookie to the new device).
Unfortunately, this method of keeping the session tied to a cookie also means that you cannot have more than one concurrent session of an interview at the same time.
(i.e. you can't fill in two identical interviews in two different browser tabs, only one session is allowed and the other one is voided)

If this one-interview-at-a-time issue is a bottleneck, a possible solution would be to set up an extension such as [Temporary Containers](https://addons.mozilla.org/en-US/firefox/addon/temporary-containers/) for Firefox (open-source on [GitHub](https://github.com/stoically/temporary-containers)) that isolates docassemble's cookies in it's own tab and voids the cookies when the tab closes, thus providing a separate session cookie for each tab and allowing multiple interviews to be completed at the same time.