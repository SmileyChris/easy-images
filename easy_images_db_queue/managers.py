from __future__ import unicode_literals

from . import db_delete_manager


class ActionManager(db_delete_manager.CountDeleteManager):

    def queue(self, limit=120):
        """
        Generator that consumes and then yields action instances (in a
        threadsafe manor).
        """
        actions = self.all()
        if limit:
            actions = actions[:limit]
        for action in actions.iterator():
            if self.filter(pk=action.pk).delete():
                yield action
    queue.alters_data = True

    def pop(self, **kwargs):
        """
        Get the next action on the queue that should be processed.

        If there are no more actions on the queue, returns ``None``.
        """
        try:
            return self.queue(**kwargs).next()
        except StopIteration:
            pass
    pop.alters_data = True
