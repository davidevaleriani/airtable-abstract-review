# airtable-abstract-review
Python-based backend for Neuromatch 3.0 online conference, used to review
abstracts submitted to Airtable and writing back the review to Airtable.

## Workflow
Attendees submit abstracts through an Airtable form, so that we have an Airtable
spreadsheet with Name, Title, Abstract columns. For review purposes, we add
extra three columns to Airtable:
- Evaluation, being either Yes, No, Maybe
- Rater, including the name of the person reviewing the abstract
- Comment, any additional comment that the rater wanted to leave about the abstract

The script uses [Cherrypy](https://cherrypy.org/) to setup a web application
for reviewing these abstracts. To interface with Airtable, it uses
[airtable-python-wrapper](https://github.com/gtalarico/airtable-python-wrapper).

When started, the application connects to Airtable. Then, when the index
webpage is opened:
- It retrieves all records in the database with empty evaluation
- If there are no records, it redirects the user to a page showing a Completed message
- Otherwise, it selects a random record and displays its title and abstract
- The rater has to indicate his/her name, optionally a comment about the abstract, and then press one of four buttons with the evaluation: Yes / No / Maybe / Skip.
- The evaluation, rater name and comment are then written back to Airtable. If the button Skip is pressed, no action is performed and a new record is shown.

The application uses Session cookies to remember the name of the rater, so this does not need to be filled every time.
