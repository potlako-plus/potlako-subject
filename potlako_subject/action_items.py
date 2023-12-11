from edc_action_item import Action, HIGH_PRIORITY, site_action_items
from edc_locator.action_items import SubjectLocatorAction as BaseSubjectLocatorAction

SUBJECT_LOCATOR_ACTION = 'submit-potlako-subject-locator'
NAVIGATION_PLANS_ACTION = 'submit-potlako-navigation-plan'


class PotlakoSubjectLocatorAction(BaseSubjectLocatorAction):
    name = SUBJECT_LOCATOR_ACTION
    display_name = 'Submit Subject Locator'
    reference_model = 'potlako_subject.subjectlocator'
    admin_site_name = 'potlako_subject_admin'


class NavigationPlansAction(Action):
    name = NAVIGATION_PLANS_ACTION
    display_name = 'Submit Navigation Plan'
    reference_model = 'potlako_subject.navigationsummaryandplan'
    admin_site_name = 'potlako_subject_admin'
    priority = HIGH_PRIORITY
    singleton = True


site_action_items.register(PotlakoSubjectLocatorAction)
site_action_items.register(NavigationPlansAction)
