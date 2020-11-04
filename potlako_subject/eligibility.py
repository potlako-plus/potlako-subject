from edc_constants.constants import NO


class Eligibility:

    def __init__(self, cancer_status=None, age_in_years=None,
                 residency=None, nationality=None, consented_contact=None,
                 enrollment_interest=None):
        """checks if participant is eligible otherwise
            error message is the reason for eligibility test failed."""

        self.reasons_ineligible = []
        if residency == NO:
            self.reasons_ineligible.append('Not a community resident')
        if nationality == NO:
            self.reasons_ineligible.append('Not a Botswana citizen')
        if cancer_status == NO:
            self.reasons_ineligible.append('Not a cancer suspect')
        if age_in_years < 30:
            self.reasons_ineligible.append('Younger than 30 years')
        if consented_contact == NO:
            self.reasons_ineligible.append(
                'Did not consent to being contacted.')
        if enrollment_interest == NO:
            self.reasons_ineligible.append(
                'Did not want to enroll.')
        if enrollment_interest == 'deceased':
            self.reasons_ineligible.append(
                'Patient deceased')

        self.is_eligible = False if self.reasons_ineligible else True
