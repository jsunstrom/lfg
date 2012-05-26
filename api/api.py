import json
import logging
import webapp2

class LookoutHandler(webapp2.RequestHandler):
    def get(self):
        from api.lookout import Lookout
        lookout_query = self.request.get('query')
        limit = int(self.request.get('limit', 10))

        query = Lookout.query()
        if lookout_query:
            search = lookout_query.strip().lower()
            query = query.filter(Lookout.n_ >= search)
            query = query.filter(Lookout.n_ < search + u"\uFFFD")

        if limit > 0:
            query = query.fetch(limit)

        out = [entity.to_dict() for entity in query]
        self.response.out.write(json.dumps(out))

    def delete(self):
        from google.appengine.ext import ndb
        from api.lookout import Lookout
        urlsafe = self.request.path.rsplit('/', 1)[-1]
        if not urlsafe:
            return

        key = ndb.Key(urlsafe=urlsafe)
        if key.kind() != Lookout._get_kind():
            self.error(500)
            return

        key.delete()
        logging.info("Deleted lookout with key: %s", urlsafe)

    def post(self):
        self.process()

    def put(self):
        self.process()

    def process(self):
        #from voluptuous import Schema
        from api.lookout import Lookout
        #from api.lookout import lookout_schema

        lookout = json.loads(self.request.body)
#        schema = Schema(lookout_schema, extra=True)
#        try:
#            schema(lookout)
#        except:
#            logging.exception('validation failed')
#            logging.info(person)

        lookout_entity = Lookout.from_dict(person)
        lookout_entity.put()

        out = lookout_entity.to_dict()
        self.response.out.write(json.dumps(out))