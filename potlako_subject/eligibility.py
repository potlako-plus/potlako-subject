from edc_constants.constants import YES


class Eligibility:

    def __init__(self, cancer_status=None, age_in_years=None):
        """checks if participant is eligible otherwise
            error message is the reason for eligibility test failed."""

        self.reasons_ineligible = []
        if cancer_status != YES:
            self.reasons_ineligible.append('not a cancer suspect')
        if age_in_years < 30:
            self.reasons_ineligible.append('younger than 30 years')

        self.eligible = (cancer_status == YES and age_in_years >= 30)
