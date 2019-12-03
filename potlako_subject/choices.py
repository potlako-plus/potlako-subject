from .constants import DOCTOR_OTHER, NURSE_OTHER

CLINICIAN_TYPE = (
    ('Medical Officer', 'Medical Officer'),
    ('Specialist - Family Medicine', 'Specialist - Family Medicine'),
    ('Specialist - Internal Medicine', 'Specialist - Internal Medicine'),
    ('Specialist - General Surgeon', 'Specialist - General Surgeon'),
    ('Specialist - Ob/GYN (Gynecologist)', 'Specialist - Ob/GYN (Gynecologist)'),
    ('Specialist - Oncologist', 'Specialist - Oncologist'),
    ('Specialist - Pathologist', 'Specialist - Pathologist'),
    ('Specialist - Hematologist', 'Specialist - Hematologist'),
    ('Specialist - Palliative care', 'Specialist - Palliative care'),
    (DOCTOR_OTHER, 'Doctor - Other type (specify)')
    ('Nurse - FNP', 'Nurse - FNP'),
    ('Nurse - Midwife', 'Nurse - Midwife'),
    ('Nurse - Community health', 'Nurse - Community health'),
    (NURSE_OTHER, 'Nurse - Other type (specify)'),
    ('Nurse - RN', 'Nurse - RN')
)