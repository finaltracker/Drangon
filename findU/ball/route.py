class DeployRouter(object):
    """
    A router to control all database operations on models in the
    application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'ball':
            return 'develop'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'ball':
            return 'develop'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'ball' or \
           obj2._meta.app_label == 'ball':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'ball':
            return db == 'develop'
        return None