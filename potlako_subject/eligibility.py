from edc_constants.constants import YES


class CancerStatusEvaluator:

    def __init__(self, cancer_status=None):
        self.eligible = cancer_status == YES


class Eligibility:

    def __init__(self, cancer_status=None):
        self.cancer_status_evaluator = CancerStatusEvaluator(
            cancer_status=cancer_status)
        self.eligible = self.cancer_status_evaluator.eligible
