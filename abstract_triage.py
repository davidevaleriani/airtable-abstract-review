import airtable
import cherrypy
import numpy as np

# Need to be filled
APP_ID = ""
TABLE_NAME = ""
KEY_ID = ""

table = airtable.Airtable(APP_ID, TABLE_NAME, KEY_ID)

class AbstractEvaluation(object):
    @cherrypy.expose
    def index(self):
        records = table.search('Evaluation', '')
        all_records = table.get_all()
        if len(records) == 0:
            raise cherrypy.HTTPRedirect('completed')
        current_rater = cherrypy.session.get('rater')
        if current_rater is None:
            current_rater = ""
        selected = np.random.randint(0, len(records))
        perc = int((1-len(records)/len(all_records))*100)
        return """<!doctype html><html>
          <head>
          <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
          </head>
          <body>
            <div class="container">
            <h1 class="text-center mt-2">Neuromatch 3.0 Abstract Triaging</h1>
            Progress:
            <div class="progress">
              <div class="progress-bar" role="progressbar" style="width: %d%%;" aria-valuenow="%d" aria-valuemin="0" aria-valuemax="100">%d%%</div>
            </div>
            <form method="post" action="rate">
              <div class="row mt-3">
                <div class="col">
                  <input type="text" name="rater" class="form-control" placeholder="Rater name" value="%s" required>
                </div>
                <div class="col">
                  <input type="text" name="comment" class="form-control" placeholder="Comment">
                </div>
              </div>
              <hr>
              <p align="right">Record ID: %s</p>
              <h3>%s</h3>
              <p class="lead">%s</p>
              <h5 class="text-right mb-3">%s</h5>
              <input type="hidden" name="recid" value="%s">
              <div class="row">
              <div class="col-sm"><button class="btn btn-primary btn-block" type="submit" name="action" value="Yes">Yes</button></div>
              <div class="col-sm"><button class="btn btn-warning btn-block" type="submit" name="action" value="Maybe">Maybe</button></div>
              <div class="col-sm"><button class="btn btn-danger btn-block" type="submit" name="action" value="No">No</button></div>
              <div class="col-sm"><button class="btn btn-secondary btn-block" type="submit" name="action" value="Skip">Skip</button></div>
              </div>
            </form>
            </div>
          <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
          <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
          <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
          </body>
        </html>""" % (perc, perc, perc, current_rater, records[selected]['id'][-6:],
                      records[selected]['fields']['title'], records[selected]['fields']['abstract'],
                      records[selected]['fields']['theme'], records[selected]['id'])

    @cherrypy.expose
    def rate(self, action, recid, rater, comment):
        if rater != None:
            cherrypy.session['rater'] = rater
        if action != 'Skip':
            record = table.get(recid)
            fields = record['fields']
            fields['Evaluation'] = action
            fields['Rater'] = rater
            fields['Comment'] = comment
            table.replace(recid, fields)
        raise cherrypy.HTTPRedirect('index')

    @cherrypy.expose
    def completed(self):
        return """<!doctype html><html>
          <head>
          <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
          </head>
          <body>
            <div class="container">
            <h1 class="text-center mt-2">Neuromatch 3.0 Abstract Triaging</h1>
            Progress:
            <div class="progress">
              <div class="progress-bar" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">100%</div>
            </div>
            <h2 class="text-center mt-3">You are done!</h2>
            <h2 class="lead text-center">There are no more abstract to review.</h2>
            </div>
          <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
          <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
          <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
          </body>
        </html>"""

conf = {
        '/': {
            'tools.sessions.on': True
        }
    }
cherrypy.quickstart(AbstractEvaluation(), '/', conf)
