from edc_action_item import Action, site_action_items
from edc_locator.action_items import SubjectLocatorAction as BaseSubjectLocatorAction

SUBJECT_LOCATOR_ACTION = 'submit-potlako-subject-locator'
TRANSPORT_ACTION = 'submit-potlako-transport-form'
INVESTIGATIONS_ACTION = 'submit-potlako-investigations-form'


class PotlakoSubjectLocatorAction(BaseSubjectLocatorAction):
    name = SUBJECT_LOCATOR_ACTION
    display_name = 'Submit Subject Locator'
    reference_model = 'potlako_subject.subjectlocator'
    admin_site_name = 'potlako_subject_admin'


class PotlakoTransportAction(Action):
    name = TRANSPORT_ACTION
    display_name = 'Submit Transport Form'
    reference_model = 'potlako_subject.transport'
    admin_site_name = 'potlako_subject_admin'


class PotlakoInvestigationsAction(Action):
    name = INVESTIGATIONS_ACTION
    display_name = 'Submit Investigations Form'
    reference_model = 'potlako_subject.investigations'
    admin_site_name = 'potlako_subject_admin'


site_action_items.register(PotlakoSubjectLocatorAction)
site_action_items.register(PotlakoTransportAction)
site_action_items.register(PotlakoInvestigationsAction)
