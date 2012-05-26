"""Person model definition and business logic."""

from google.appengine.ext import ndb

lookout_schema = {
    'key': basestring,
    'name': basestring,
    'notes': basestring,
    #'contact_info': [{'type': basestring, 'value': basestring}],
    }

class Lookout(ndb.Model):
    """Represents a person."""
    # Store the schema version, to aid in migrations.
    version_ = ndb.IntegerProperty('v_', default=1)

    # The entity's change revision counter.
    revision = ndb.IntegerProperty('r_', default=0)

    # Useful timestamps.
    added = ndb.DateTimeProperty('a_', auto_now_add=True)
    modified = ndb.DateTimeProperty('m_', auto_now=True)

    # Person code, name, key
    name = ndb.StringProperty('n', indexed=False)
    n_ = ndb.ComputedProperty(lambda self: self.name.lower())

    # Phone / email / whatever.
    #contact_info = ndb.JsonProperty('ci')

    # General remarks.
    notes = ndb.TextProperty('no')

    def _pre_put_hook(self):
        """Ran before the entity is written to the datastore."""
        self.revision += 1

    @classmethod
    def from_dict(cls, data):
        """Instantiate a Person entity from a dict of values."""
        key = data.get('key')
        lookout = None
        if key:
            key = ndb.Key(urlsafe=key)
            lookout = key.get()

        if not lookout:
            lookout = cls()

        lookout.name = data.get('name')
        #person.contact_info = data.get('contact_info')
        lookout.notes = data.get('notes')

        return lookout

    def to_dict(self):
        """Return a Person entity represented as a dict of values
        suitable for rebuilding via Person.from_dict.
        """
        lookout = {
            'version': self.version_,
            'key': self.key.urlsafe(),
            'revision': self.revision,
            'added': self.added.strftime('%Y-%m-%d %h:%M'),
            'modified': self.modified.strftime('%Y-%m-%d %h:%M'),

            # name
            'name': self.name,

            # Contact info
            #'contact_info': self.contact_info,

            # Notes
            'notes': self.notes,
            }
        return lookout