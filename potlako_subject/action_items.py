from edc_action_item import site_action_items
from edc_locator.action_items import SubjectLocatorAction as BaseSubjectLocatorAction

SUBJECT_LOCATOR_ACTION = 'submit-potlako-subject-locator'


class PotlakoSubjectLocatorAction(BaseSubjectLocatorAction):
    name = SUBJECT_LOCATOR_ACTION
    display_name = 'Submit Subject Locator'
    reference_model = 'potlako_subject.subjectlocator'
    admin_site_name = 'potlako_subject_admin'


site_action_items.register(PotlakoSubjectLocatorAction)
