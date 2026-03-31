#!/usr/bin/env python3
"""Generate variables-only and demo-data versions of all 4 audit templates."""
import re, os

# Demo data mapping for all {Variable} placeholders
DEMO = {
    # General
    'Order_Number': 'ORD-2025-04721',
    'Audit_Order_Number': 'AUD-2025-08934',
    'Report_Creation_Date': '28 March 2026',
    'Plan_Creation_Date': '10 March 2026',
    'Finding_List_Creation_Date': '28 March 2026',
    'Version': '1.0',
    'Total_Pages': '12',
    'Last_Page': '12',
    'N': '—',

    # Auditee
    'Auditee_Name': 'MedTech Solutions GmbH',
    'Auditee_Street': 'Industriestraße 42',
    'Postal_Code': '80939',
    'City': 'München',
    'State': 'Bavaria',
    'Country': 'Germany',
    'Facility_Number': 'FAC-2024-00847',
    'CBW_ID': 'CBW-2024-00847',
    'Contact_FirstName': 'Dr. Julia',
    'Contact_LastName': 'Braun',
    'Project_Handler': 'Stefan Hofmann',
    'Client_Role': 'Manufacturer',

    # Audit
    'Audit_Start_Date': '24 March 2026',
    'Audit_End_Date': '26 March 2026',
    'Audit_Languages': 'English, German',
    'Audit_Mode': 'On-site',
    'Audit_Mode_Detail': 'on-site at the manufacturer\'s facility.',
    'Audit_Type': 'Surveillance',
    'Audit_Type_MDR': 'Initial Certification',
    'Audit_Type_ISO': 'Initial Certification',
    'Next_Audit_Date': '15 September 2026',
    'Next_Audit_Type': 'Surveillance',
    'Total_Manhours': '24',

    # Certificates
    'Certificate_Number_MDR': 'CE-MDR-2026-04521',
    'Certificate_Number_ISO': 'ISO-13485-2026-08832',
    'Certificate_List': 'CE-MDR-2026-04521 (MDR Annex IX), ISO-13485-2026-08832 (EN ISO 13485:2016)',

    # Facilities
    'Facility_No_1': 'FAC-001',
    'Facility_Name_1': 'MedTech Solutions GmbH – Headquarters & Production',
    'Facility_Address_1': 'Industriestraße 42, 80939 München, Germany',
    'Facility_No_2': 'FAC-002',
    'Facility_Name_2': 'MedTech Solutions GmbH – Sterilization Center',
    'Facility_Address_2': 'Garching Innovation Park, Am Coulombwall 8, 85748 Garching, Germany',
    'Facility_CBW_1': 'CBW-001',
    'Facility_CBW_2': 'CBW-002',
    'Facility_Hours_1': '16',
    'Facility_Hours_2': '8',

    # Audit Team
    'Lead_Auditor': 'Dr. Maria Schmidt',
    'Lead_Auditor_Name': 'Dr. Maria Schmidt',
    'Co_Auditors': 'Thomas Weber, Dr. Sarah König',
    'Team_Participants': 'Franz Müller (Observer – TÜV SÜD)',
    'Auditor_Names': 'Dr. Maria Schmidt, Thomas Weber',
    'Auditor_Name': 'Dr. Maria Schmidt',
    'All_Auditors': 'MS, TW, SK',

    # Team Members
    'Team_Member_Name_1': 'Dr. Maria Schmidt',
    'Team_Member_Role_1': 'Lead Auditor',
    'Team_Member_Codes_1': 'MDD/MDR, ISO 13485, MDSAP (AUS, CAN)',
    'Team_Member_Name_2': 'Thomas Weber',
    'Team_Member_Role_2': 'Co-Auditor',
    'Team_Member_Codes_2': 'ISO 13485, MDSAP (BRA, JPN)',

    # Audit Times  
    'Day_1_Date': '24 March 2026',
    'Day_1_From': '08:30',
    'Day_1_To': '17:00',
    'Day_2_Date': '25 March 2026',
    'Day_2_From': '08:45',
    'Day_2_To': '16:30',
    'Audit_Date_1': '24 March 2026',
    'Audit_From_1': '08:30',
    'Audit_To_1': '17:00',

    # Day Schedule
    'Day1_Date': '24 March 2026 (Tuesday)',
    'Day1_Location': 'MedTech Solutions HQ, Industriestraße 42, München',
    'Day2_Date': '25 March 2026 (Wednesday)',
    'Day2_Location': 'MedTech Solutions HQ + Sterilization Center',
    'Day3_Date': '26 March 2026 (Thursday)',
    'Day3_Location': 'Garching Innovation Park',
    'Auditor_Names_Day1': 'MS, TW, SK',

    # Auditor assignments
    'Auditor_MgmtReview': 'MS',
    'Auditor_Design': 'TW',
    'Auditor_Vigilance': 'MS',
    'Auditor_QMS': 'SK',
    'Auditor_AO': 'TW',
    'Auditor_Purchasing': 'MS',
    'Auditor_CAPA': 'SK',
    'Auditor_Infrastructure': 'MS',
    'Auditor_Manufacturing': 'TW',
    'Auditor_Sterilization': 'SK',
    'Auditor_Marketing': 'MS',
    'Auditor_Calibration': 'TW',
    'Auditor_QC': 'SK',
    'Auditor_Validation': 'SK',
    'Auditor_InternalAudit': 'MS',
    'Auditor_Training': 'TW',
    'Audit_Location': 'MedTech Solutions HQ, München',

    # Co-Auditors
    'Co_Auditor_1': 'Thomas Weber',
    'Codes_1': 'ISO 13485, MDSAP',
    'Co_Auditor_2': 'Dr. Sarah König',
    'Codes_2': 'MDR, Sterilization',
    'Co_Auditor_3': 'Franz Müller (Observer)',

    # Participants
    'Participant_Name_1': 'Dr. Julia Braun',
    'Participant_Role_1': 'Quality Manager / Audit Responsible',
    'Participant_Name_2': 'Markus Fischer',
    'Participant_Role_2': 'Head of Production',
    'Participant_Name_3': 'Dr. Anna Lehmann',
    'Participant_Role_3': 'Regulatory Affairs Manager',
    'Participant_Name_4': 'Peter Zimmermann',
    'Participant_Role_4': 'PRRC (Person Responsible for Regulatory Compliance)',
    'Participant_Name_5': 'Sabine Kraft',
    'Participant_Role_5': 'R&D Manager',

    # Comments
    'Opening_Meeting_Notes': 'Opening meeting conducted at 08:45 in Conference Room A. All team members and auditee representatives present. No conflicts of interest identified. Audit plan accepted without modifications.',
    'Closing_Meeting_Notes': 'Closing meeting held at 15:30. One minor NC (TNR-000735) identified and presented. Client acknowledged the finding. Next surveillance audit tentatively scheduled for September 2026.',
    'NC_Followup_Comment': 'Previous NC (TNR-000649) regarding CAPA process documentation was reviewed. Corrective actions were effectively implemented and verified. NC closed.',
    'QMS_Description': 'MedTech Solutions operates a QMS covering design, development, production, sterilization, and distribution of Class IIa/IIb surgical instruments and wound care devices. The QMS is documented in QM-Manual Rev. 12 (dated 15.01.2026).',

    # QMS Documentation Review Comments
    'QMS_Quality_Policy_Comment': 'QM-POL-001 Rev. 5, dated 10.01.2026 – Quality Policy Statement aligned with ISO 13485 and MDR requirements.',
    'QMS_Quality_Objectives_Comment': 'QM-OBJ-2026 Rev. 1, dated 15.01.2026 – Measurable quality objectives defined for all departments.',
    'QMS_Quality_Manual_Comment': 'QM-MAN-001 Rev. 12, dated 15.01.2026 – Comprehensive quality manual covering all ISO 13485 clauses.',
    'QMS_Management_Responsibility_Comment': 'QM-ORG-001 Rev. 8, dated 20.12.2025 – Management Representative: Dr. Julia Braun appointed.',
    'QMS_Management_Review_Comment': 'QM-MRV-2025-02, dated 28.11.2025 – Management Review minutes include all required inputs per ISO 13485:2016 clause 5.6.',
    'QMS_Internal_Audit_Comment': 'QM-IA-PLAN-2026, Rev. 1, dated 05.01.2026 – Internal audit program covers all QMS processes over a 12-month cycle.',
    'QMS_Resource_Management_Comment': 'QM-HR-001 Rev. 4, dated 01.12.2025 – Organizational chart and competency matrix available. Area of Concern: Training records for 2 new production employees incomplete.',
    'QMS_Factory_Layout_Comment': 'Factory layout plan FL-2025-03, dated 15.09.2025. Material flow not fully documented for new warehouse extension.',
    'QMS_Work_Environment_Comment': 'QM-ENV-001 Rev. 3, dated 20.11.2025 – Cleanroom monitoring records available. Temperature logs gap identified for December 2025.',
    'QMS_Purchasing_Comment': 'QM-PUR-001 Rev. 6, dated 01.02.2026 – Approved supplier list with 47 active suppliers. Supplier evaluation records up to date.',
    'QMS_CAPA_Comment': 'QM-CAPA-001 Rev. 5, dated 10.01.2026 – CAPA procedure in place. Area of Concern: Effectiveness review timelines not consistently met.',
    'QMS_Design_Development_Comment': 'QM-DD-001 Rev. 7, dated 01.03.2026 – Design and development procedure covers all phases per ISO 13485:2016 clause 7.3.',
    'QMS_Other_Docs_Comment': 'Additional documents reviewed: Risk management file (QM-RM-001), Post-market surveillance plan (QM-PMS-2026).',

    # AoC Numbers
    'AoC_Number': 'AoC-2026-001',
    'AoC_CAPA_Number': 'AoC-2026-002',

    # MDR Comments
    'MDR_Art10_TD_Comment': 'Technical documentation structure reviewed. TD template QM-TD-001 Rev. 4 in place. Annex II/III structure implemented. Area of Concern: Retention period statement missing for implantable device category.',
    'MDR_UDI_Comment': 'UDI procedure QM-UDI-001 Rev. 2 dated 15.02.2026. UDI-DI assignment documented. Area of Concern: UDI database registration not completed for 2 new product variants.',
    'MDR_PRRC_Comment': 'Peter Zimmermann appointed as PRRC per Article 15. Qualification documented in HR file. Responsibilities defined in QM-ORG-001.',
    'MDR_CE_Marking_Comment': 'CE marking procedure QM-CE-001 Rev. 3 dated 01.01.2026. Area of Concern: Procedure not yet updated to reflect latest MDCG guidance on NB number placement.',
    'MDR_Classification_Comment': 'Product classification documented in QM-CLASS-001 Rev. 2. Area of Concern: Classification rationale for 3 legacy MDD products not yet updated to MDR rules.',
    'MDR_Clinical_Eval_Comment': 'Clinical evaluation procedure QM-CER-001 Rev. 3. CEP template available. PMCF plan integrated. Literature search methodology documented.',
    'MDR_Clinical_Inv_Comment': 'Clinical investigation procedure QM-CI-001 Rev. 1 dated 10.01.2026. Area of Concern: Procedure not yet tested in practice as no investigations initiated.',
    'MDR_PMS_Comment': 'PMS procedure QM-PMS-001 Rev. 4 dated 01.02.2026. PMS plan and PSUR template available. Data collection from complaint system and vigilance reporting integrated.',
    'MDR_Vigilance_Comment': 'Vigilance procedure QM-VIG-001 Rev. 3 dated 15.01.2026. Reporting timelines documented. MedDev/EUDAMED reporting pathway defined.',
    'AoC_Art10_TD': 'AoC-2026-003',
    'AoC_UDI': 'AoC-2026-004',
    'AoC_CE_Marking': 'AoC-2026-005',
    'AoC_Classification': 'AoC-2026-006',
    'AoC_Clinical_Inv': 'AoC-2026-007',

    # Process descriptions
    'Process_Description': 'The management responsibility process was audited including quality policy deployment, quality objectives tracking, organizational structure, management representative duties, and management review outputs. The audit team reviewed the latest management review minutes (MRV-2025-02) and verified implementation of action items.',
    'Key_Documents': 'QM-Manual Rev. 12, Management Review Minutes MRV-2025-02, Quality Policy QM-POL-001, Organization Chart QM-ORG-001, Quality Objectives QM-OBJ-2026',
    'Persons_Interviewed': 'Dr. Julia Braun (Quality Manager), Peter Zimmermann (PRRC), CEO Dr. Hans Meier',
    'Products_Reviewed': 'SurgiCut Pro II (Class IIb surgical instrument), WoundSeal Advanced (Class IIa wound care device)',

    # NC Details
    'NC_Description': 'The CAPA process was not consistently followed for minor nonconformities identified during internal audits. Three out of eight sampled CAPA records did not include a documented root cause analysis.',
    'NC_Details': 'ISO 13485:2016 clause 8.5.2 requires that corrective actions include investigation of the cause of the nonconformity. CAPA records CAPA-2025-014, CAPA-2025-019, and CAPA-2025-022 were missing documented root cause analyses.',
    'NC_Evidence': 'CAPA-2025-014 (dated 15.06.2025), CAPA-2025-019 (dated 22.08.2025), CAPA-2025-022 (dated 05.11.2025) – Root cause analysis field left blank or stated "to be completed".',
    'AOC_Details': 'The supplier evaluation process does not include a formal re-evaluation schedule. While initial evaluations are thorough, ongoing monitoring criteria are not clearly defined.',
    'AOC_Evidence': 'Supplier Evaluation Records SE-2025-003, SE-2025-007 – No re-evaluation dates or criteria documented.',

    # NC Finding List specific
    'NC_Number': 'TNR-000735',
    'NC_Requirement_Text': 'ISO 13485:2016, clause 8.5.2 – Corrective Action: The organization shall take action to eliminate the cause of nonconformities in order to prevent recurrence. Corrective actions shall be proportionate to the effects of the nonconformities encountered.',
    'NC_Description_Text': 'During the review of the CAPA system, it was identified that 3 out of 8 sampled corrective action records (CAPA-2025-014, CAPA-2025-019, CAPA-2025-022) did not include a documented root cause analysis. The root cause analysis field was either left blank or contained the note "to be completed". Without a proper root cause analysis, the effectiveness of corrective actions cannot be assured.',
    'NC_Scheme': 'EN ISO 13485:2016 – Clause 8.5.2',
    'NC_Due_Date': '27 June 2026',
    'NC_Status': 'Open – Awaiting Response',
    'NC_Evidence': 'CAPA-2025-014 (Internal audit finding #IA-2025-06-03), CAPA-2025-019 (Customer complaint CC-2025-041), CAPA-2025-022 (Process deviation PD-2025-018)',
    'NC_Product': 'N/A – systemic finding affecting all product lines',
    'NC_MDSAP_Context': 'N/A – MDSAP not in scope for this audit',
    'NC_Root_Cause_Analysis': 'Investigation using 5-Why analysis revealed that the CAPA procedure (QM-CAPA-001) requires root cause analysis but does not specify the methodology or minimum documentation requirements. New employees were not adequately trained on root cause analysis tools.',
    'NC_Causes': '1. Insufficient procedural detail regarding root cause analysis methodology. 2. Gap in training program for new QA personnel. 3. No automated check in CAPA workflow system to verify completeness.',
    'NC_Corrections': 'All three identified CAPA records (CAPA-2025-014, CAPA-2025-019, CAPA-2025-022) have been retroactively completed with proper root cause analyses using fishbone diagrams.',
    'NC_Corrective_Actions': '1. Updated QM-CAPA-001 Rev. 6 to include mandatory root cause analysis tools (5-Why, Fishbone, Fault Tree). 2. Implemented mandatory training module "ROOT-001" for all QA staff. 3. Added automated completeness check in electronic CAPA system.',
    'NC_Assessment_Response': 'CAPA plan received on 10 April 2026. Root cause analysis is adequate and addresses the systemic cause.',
    'NC_TUV_Implementation_Review': 'Reviewed on 15 May 2026: Updated procedure QM-CAPA-001 Rev. 6 verified. Training records for 12 QA staff confirmed completeness. System validation report for automated check reviewed.',
    'NC_TUV_Effectiveness_Review': 'To be reviewed at next surveillance audit (September 2026). Preliminary evidence: 5 new CAPAs initiated since correction – all contain documented root cause analyses.',
    'NC_TUV_Acceptance': 'Accepted – Dr. Maria Schmidt, 20 May 2026',
    'NC_Assessment_Implementation': 'Evidence of implementation reviewed and accepted. Procedure update, training, and system enhancement verified.',
    'NC_Assessment_Effectiveness': 'Pending – to be verified at next surveillance audit.',

    # Major NC
    'NC_Number_Major': 'TNR-000736',
    'NC_Major_Requirement_Text': 'MDR (EU) 2017/745, Article 10(9) – The manufacturer shall have a system in place to record and report incidents and field safety corrective actions. Vigilance reporting timelines as specified in Article 87(2) shall be met.',
    'NC_Major_Description_Text': 'The vigilance reporting system failed to meet the mandatory reporting timeline for a serious incident. Incident INC-2025-023 (adverse event involving SurgiCut Pro device – patient injury) was reported to the competent authority 22 days after awareness, exceeding the maximum 15-day reporting deadline specified in Article 87(2) MDR. The delay was attributed to unclear escalation responsibilities between the complaint handling team and Regulatory Affairs.',
    'NC_Major_Scheme': 'MDR (EU) 2017/745 – Article 87(2)',
    'NC_Major_Due_Date': '26 June 2026',
    'NC_Major_Status': 'Open – Under Review',
    'NC_Major_Evidence': 'Incident file INC-2025-023, dated 03.10.2025. Competent authority notification timestamp: 25.10.2025 (22 days vs. 15-day maximum). Complaint record CC-2025-067. Internal escalation email chain showing 7-day delay before RA was notified.',
    'NC_Major_Product': 'SurgiCut Pro II (Class IIb), REF SC-PRO-200, Lot 2025-07-142',
    'NC_Major_Root_Cause': 'Root cause analysis (Fault Tree Analysis) determined: Primary cause – the complaint handling SOP (QM-COMP-001 Rev. 4) did not define clear criteria for classifying events as "serious incidents" requiring vigilance reporting. Secondary cause – no automated escalation trigger in the complaint management system for time-critical vigilance events.',
    'NC_Major_Causes': '1. Ambiguous incident classification criteria in QM-COMP-001. 2. No automated vigilance deadline tracking. 3. Regulatory Affairs not included in initial complaint triage process.',
    'NC_Major_Corrections': 'Incident INC-2025-023 was reported to the competent authority on 25.10.2025. A Field Safety Notice (FSN-2026-001) was issued on 15.01.2026. Retroactive EUDAMED notification completed.',
    'NC_Major_Corrective_Actions': '1. Revised QM-COMP-001 Rev. 5 with explicit serious incident classification criteria per MDR Article 2(65). 2. Integrated automated vigilance deadline tracking in complaint system (alerts at Day 1, Day 5, Day 10). 3. Established mandatory Regulatory Affairs involvement in initial complaint triage within 24 hours. 4. Conducted organization-wide vigilance training (VIG-TRN-2026-01).',
    'NC_Major_Assessment': 'CAPA plan received on 05 April 2026. Comprehensive root cause analysis with adequate corrective actions proposed.',
    'NC_Major_TUV_Implementation': 'Under review – evidence submission expected by 26 June 2026.',
    'NC_Major_TUV_Effectiveness': 'Pending – to be assessed after implementation period.',
    'NC_Major_TUV_Acceptance': 'CAPA plan accepted – Dr. Maria Schmidt, 15 April 2026',
    'NC_Major_Assessment_Impl': 'Pending – due 26 June 2026',
    'NC_Major_Assessment_Eff': 'Pending – to be verified at next surveillance audit.',

    # Version History
    'Version_No_1': '1',
    'Version_Date_1': '28 March 2026',
    'Version_Name_1': 'Dr. Maria Schmidt',
    'Version_Description_1': 'Initial version – report issued after closing meeting',
    'Version_No_2': '2',
    'Version_Date_2': '15 April 2026',
    'Version_Name_2': 'Dr. Maria Schmidt',
    'Version_Description_2': 'Updated after client CAPA plan review',
}

# Template files and their display names
TEMPLATES = [
    ('audit-report-template.html', 'Audit Report'),
    ('stage1-audit-report-template.html', 'Stage 1 Audit Report'),
    ('stage2-audit-plan-template.html', 'Stage 2 Audit Plan'),
    ('stage2-audit-findings-list-template.html', 'Stage 2 Findings List'),
]

BASE = os.path.dirname(os.path.abspath(__file__))

for filename, display_name in TEMPLATES:
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # --- VARIABLES VERSION ---
    # The existing templates already use {Variable} for dynamic data.
    # For the variables version, we also need to convert hardcoded badge states to variables.
    vars_content = content
    
    # Replace the title to indicate this is the variables version
    vars_content = vars_content.replace(
        f'<title>{display_name}',
        f'<title>{display_name} [VARIABLES]'
    ).replace(
        f'<title>Audit Report – Crystal Report Vorlage für Dienstleister</title>',
        f'<title>Audit Report [VARIABLES] – Crystal Report Vorlage für Dienstleister</title>'
    )
    
    # In the sidebar, update subtitle
    vars_content = vars_content.replace(
        'Umsetzungsanweisungen für den Dienstleister',
        'VARIABLES VERSION – Alle dynamischen Felder als {Variable}'
    )
    
    # Replace hardcoded badge states with variables for checklist items
    # In the variables version, every badge result should be a {Variable}
    badge_counter = [0]
    def replace_badge_with_var(match):
        badge_counter[0] += 1
        return f'<span class="badge {{Badge_Class_{badge_counter[0]}}}">{{Status_{badge_counter[0]}}}</span>'
    
    vars_content = re.sub(
        r'<span class="badge badge-(?:completed|yes|no|na|pass|fail|aoc|pending|closed|awaiting|ok|major|minor)">\s*([^<]+?)\s*</span>',
        replace_badge_with_var,
        vars_content
    )
    
    # Also replace hardcoded auditor names in audit trail cards
    vars_content = vars_content.replace('>Kerstin Weitl<', '>{Auditor_1_Name}<')
    vars_content = vars_content.replace('>Tobias Keller<', '>{Auditor_2_Name}<')
    
    vars_outfile = os.path.join(BASE, filename.replace('.html', '-variables.html'))
    with open(vars_outfile, 'w', encoding='utf-8') as f:
        f.write(vars_content)
    print(f'Created: {os.path.basename(vars_outfile)}')
    
    # --- DEMO VERSION ---
    demo_content = content
    
    # Replace title
    demo_content = demo_content.replace(
        f'<title>{display_name}',
        f'<title>{display_name} [DEMO]'
    ).replace(
        f'<title>Audit Report – Crystal Report Vorlage für Dienstleister</title>',
        f'<title>Audit Report [DEMO] – Crystal Report Vorlage für Dienstleister</title>'
    )
    
    # Update sidebar
    demo_content = demo_content.replace(
        'Umsetzungsanweisungen für den Dienstleister',
        'DEMO VERSION – Beispieldaten (fiktiv)'
    )
    
    # Replace all {Variable} patterns with demo data
    def replace_var(match):
        var_name = match.group(1)
        return DEMO.get(var_name, f'[DEMO: {var_name}]')
    
    demo_content = re.sub(r'\{(\w+)\}', replace_var, demo_content)
    
    demo_outfile = os.path.join(BASE, filename.replace('.html', '-demo.html'))
    with open(demo_outfile, 'w', encoding='utf-8') as f:
        f.write(demo_content)
    print(f'Created: {os.path.basename(demo_outfile)}')

print('\nDone! 8 files created.')
