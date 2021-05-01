import redcap
import sqlite3
import json
from datetime import datetime


def measure_helper_all_hos_per_quarter(cursor, date1, date2):
    # stat 1
    baby_gest_and_aim_nas = 0
    sum_aim_calc_los_baby = 0
    nas_stay_length = 0
    total_nas_stay_length = 0
    # stat 2
    baby_gest = 0
    aim_pharm_tx_2 = 0
    oens_requiring_pharmacologic_therapy = 0
    total_oens_requiring_pharmacologic_therapy = 0
    # stat 3
    sum_aim_calc_length_tx = 0
    nas_pharmacological_treatment_days = 0
    total_nas_pharmacological_treatment_days = 0
    # stat 4
    aim_nas_2_3_4_5 = 0
    oen_nas_symptom = 0
    total_oen_nas_symptom = 0
    # stat 5 is woman
    mom_date_deliv_not_null = 0
    mom_aim_tx_or_mat_2_3_4 = 0
    mom_mat_behavioral_treatment = 0
    total_mom_mat_behavioral_treatment = 0
    # stat 6
    dhs_referral_1 = 0
    dhs_contacted = 0
    total_dhs_contacted = 0
    # stat 7
    aim_roomin_any_2 = 0
    oen_romming_with_mother_any = 0
    total_oen_romming_with_mother_any = 0
    # stat 8
    aim_romming_50plus = 0
    oen_rooming_with_mother_majority = 0
    total_oen_rooming_with_mother_majority = 0
    # stat 9
    aim_mhm_dc_1_2 = 0
    oen_mothers_milk = 0
    total_oen_mothers_milk = 0
    # stat 10
    aim_placement_dc = 0
    biological_mother_discharge = 0
    total_biological_mother_discharge = 0
    # stat 11
    early_intervention = 0
    oen_with_discharge_followup = 0
    total_oen_with_discharge_followup = 0
    # stat 12
    pcp_appt = 0
    percent_oen_pcp = 0
    total_percent_oen_pcp = 0
    # stat 13 INFANT_STI
    infant_sti = 0
    percent_inf_sti = 0
    total_percent_inf_sti = 0
    # stat 14 woman
    mom_oud_dx_timing_1_2 = 0
    mom_hbv_hcv_hiv_rpr_1_2_3 = 0
    mom_sti_among_oud = 0
    total_mom_sti_among_oud = 0
    # stat 15 woman
    mom_nas_consult = 0
    mom_prenatal_pediatric_consult_among_oud = 0
    total_mom_prenatal_pediatric_consult_among_oud = 0
    # stat 16
    dhs_custody = 0
    percent_dhs_custody = 0
    total_percent_dhs_custody = 0
    # stat 17
    baby_calc_mme = 0
    sum_baby_calc_mme = 0
    calc_mme_infant = 0
    total_calc_mme_infant = 0
    # stat 18
    clon_meth_morph_pheno_other_unkown_1_2 = 0
    med_used = 0
    total_med_used = 0
    # STAT 19
    baby_gest_and_nonnas = 0
    sum_calc_los_medreadydc = 0
    sum_aim_calc_los_baby_readmit = 0
    aim_calc_plus_aim_calc_red_minus_calc_los_med = 0
    avg_diff_discharge = 0
    total_avg_diff_discharge = 0

    # STAT 20
    assessment_1_2_3_4_5 = 0
    type_assessment = 0
    total_type_assessment = 0

    # stat 1
    cursor.execute(
        "SELECT SUM(baby_aim_calc_los_baby) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_nos_p0414_p961 BETWEEN 2 AND 5)  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    sum_aim_calc_los_baby=(results[0][0])
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_nos_p0414_p961 BETWEEN 2 AND 5) "
        " AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format( date1,
                                                                                         date2))
    results = cursor.fetchall()
    baby_gest_and_aim_nas=(results[0][0])
    if sum_aim_calc_los_baby is not None and baby_gest_and_aim_nas is not None and baby_gest_and_aim_nas != 0:
        nas_stay_length=(sum_aim_calc_los_baby / baby_gest_and_aim_nas)
    else:
        nas_stay_length=(None)

    # stat 2
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_aim_pharm_tx == 2  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    aim_pharm_tx_2=(results[0][0])
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    baby_gest=(results[0][0])
    if aim_pharm_tx_2 is not None and baby_gest != 0 and baby_gest is not None:
        oens_requiring_pharmacologic_therapy=(aim_pharm_tx_2 / baby_gest)
    else:
        oens_requiring_pharmacologic_therapy=(None)

    # stat 3
    cursor.execute(
        "SELECT SUM(baby_aim_calc_length_tx) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_nos_p0414_p961 BETWEEN 2 AND 5)  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    sum_aim_calc_length_tx=(results[0][0])
    if sum_aim_calc_length_tx is not None and baby_gest_and_aim_nas is not None and baby_gest_and_aim_nas != 0:
        nas_pharmacological_treatment_days=(sum_aim_calc_length_tx / baby_gest_and_aim_nas)
    else:
        nas_pharmacological_treatment_days=(None)

    # stat 4
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_nos_p0414_p961 BETWEEN 2 AND 5)  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    aim_nas_2_3_4_5=(results[0][0])
    if aim_nas_2_3_4_5 is not None and baby_gest != 0 and baby_gest is not None:
        oen_nas_symptom=(aim_nas_2_3_4_5 / baby_gest)
    else:
        oen_nas_symptom=(None)

    # stat 5 is woman
    cursor.execute(
        "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_date_delivery IS NOT NULL)  AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    mom_date_deliv_not_null=(results[0][0])
    cursor.execute(
        "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_date_delivery IS NOT NULL) AND (maternal_aim_tx_or_mat BETWEEN 2 AND 4)  AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    mom_aim_tx_or_mat_2_3_4=(results[0][0])
    if mom_aim_tx_or_mat_2_3_4 is not None and mom_date_deliv_not_null != 0 and mom_date_deliv_not_null is not None:
        mom_mat_behavioral_treatment=(mom_aim_tx_or_mat_2_3_4 / mom_date_deliv_not_null)
    else:
        mom_mat_behavioral_treatment=(None)

    # stat 6
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_dhs_referral == 1  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    dhs_referral_1=(results[0][0])
    if dhs_referral_1 is not None and baby_gest != 0 and baby_gest is not None:
        dhs_contacted=(dhs_referral_1 / baby_gest)
    else:
        dhs_contacted=(None)

    # stat 7
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_aim_roomin_any == 2  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    aim_roomin_any_2=(results[0][0])
    if aim_roomin_any_2 is not None and baby_gest != 0 and baby_gest is not None:
        oen_romming_with_mother_any=(aim_roomin_any_2 / baby_gest)
    else:
        oen_romming_with_mother_any=(None)

    # stat 8
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_aim_rooming_50plus == 2  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    aim_romming_50plus=(results[0][0])
    if aim_romming_50plus is not None and baby_gest != 0 and baby_gest is not None:
        oen_rooming_with_mother_majority=(aim_romming_50plus / baby_gest)
    else:
        oen_rooming_with_mother_majority=(None)

    # stat 9
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_mhm_dc BETWEEN 1 AND 2)  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    aim_mhm_dc_1_2=(results[0][0])
    if aim_mhm_dc_1_2 is not None and baby_gest != 0 and baby_gest is not None:
        oen_mothers_milk=(aim_mhm_dc_1_2 / baby_gest)
    else:
        oen_mothers_milk=(None)

    # stat 10
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_placement_dc BETWEEN 1 AND 2)  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    aim_placement_dc=(results[0][0])
    if aim_placement_dc is not None and baby_gest != 0 and baby_gest is not None:
        biological_mother_discharge=(aim_placement_dc / baby_gest)
    else:
        biological_mother_discharge=(None)

    # stat 11
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_early_intervention IN (1,2,4,6))  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    early_intervention=(results[0][0])
    if early_intervention is not None and baby_gest != 0 and baby_gest is not None:
        oen_with_discharge_followup=(early_intervention / baby_gest)
    else:
        oen_with_discharge_followup=(None)

    # stat 12
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_pcp_appt BETWEEN 2 AND 4)  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    pcp_appt=(results[0][0])
    if pcp_appt is not None and baby_gest != 0 and baby_gest is not None:
        percent_oen_pcp=(pcp_appt / baby_gest)
    else:
        percent_oen_pcp=(None)

    # stat 13 # INFANT_STI
    # NOTE, pdf says get infant_sti == 2,3,4,5 but it is zero index from 0-5 so add one to get 3,4,5,6 as its stored in memory as 1-6
    cursor.execute(
        "SELECT COUNT(baby_id) From Child WHERE baby_gestational_age >= 35 AND (substr(baby_infant_sti, 3, 1) == '1' OR substr(baby_infant_sti, 4, 1) == '1' OR substr(baby_infant_sti, 5, 1) == '1' OR substr(baby_infant_sti, 6, 1) == '1')  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    infant_sti=(results[0][0])
    if infant_sti is not None and baby_gest != 0 and baby_gest is not None:
        percent_inf_sti=(infant_sti / baby_gest)
    else:
        percent_inf_sti=(None)
    # stat 14 WOMAN
    cursor.execute(
        "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_oud_dx_timing BETWEEN 1 AND 2) AND ((maternal_hbv_test BETWEEN 1 AND 3) OR (maternal_hcv_test BETWEEN 1 AND 3) OR (maternal_hiv_test BETWEEN 1 AND 3) OR (maternal_rpr_test BETWEEN 1 AND 3))  AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    mom_hbv_hcv_hiv_rpr_1_2_3=(results[0][0])
    cursor.execute(
        "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_oud_dx_timing BETWEEN 1 AND 2)  AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    mom_oud_dx_timing_1_2=(results[0][0])
    if mom_hbv_hcv_hiv_rpr_1_2_3 is not None and mom_oud_dx_timing_1_2 != 0 and mom_oud_dx_timing_1_2 is not None:
        mom_sti_among_oud=(mom_hbv_hcv_hiv_rpr_1_2_3 / mom_oud_dx_timing_1_2)
    else:
        mom_sti_among_oud=(None)
    # stat 15 woman
    cursor.execute(
        "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_date_delivery IS NOT NULL) AND (maternal_nas_consult BETWEEN 2 AND 3)  AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    mom_nas_consult=(results[0][0])
    if mom_nas_consult is not None and mom_date_deliv_not_null != 0 and mom_date_deliv_not_null is not None:
        mom_prenatal_pediatric_consult_among_oud=(mom_nas_consult / mom_date_deliv_not_null)
    else:
        mom_prenatal_pediatric_consult_among_oud=(None)
    # stat 16
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_dhs_custody IN (2,4,5,6))  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    dhs_custody=(results[0][0])
    if dhs_custody is not None and baby_gest != 0 and baby_gest is not None:
        percent_dhs_custody=(dhs_custody / baby_gest)
    else:
        percent_dhs_custody=(None)
    # stat 17
    cursor.execute(
        "SELECT SUM(baby_calc_mme_infant) FROM Child WHERE baby_gestational_age >= 35 AND baby_calc_mme_infant IS NOT NULL  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    sum_baby_calc_mme=(results[0][0])
    cursor.execute(
        "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_calc_mme_infant IS NOT NULL  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    baby_calc_mme=(results[0][0])
    if sum_baby_calc_mme is not None and baby_calc_mme != 0 and baby_calc_mme is not None:
        calc_mme_infant=(sum_baby_calc_mme / baby_calc_mme)
    else:
        calc_mme_infant=(None)

    # stat 18
    cursor.execute(
        "SELECT COUNT(baby_id) From Child WHERE baby_aim_pharm_tx == 2 AND (substr(baby_clonidine_pharm, 1, 1) == '1' OR substr(baby_clonidine_pharm, 2, 1) == '1' OR substr(baby_methadone_pharm, 1, 1) == '1' OR substr(baby_methadone_pharm, 2, 1) == '1' OR substr(baby_morphine_pharm, 1, 1) == '1' OR substr(baby_morphine_pharm, 2, 1) == '1' OR substr(baby_phenobarb_pharm, 1, 1) == '1' OR substr(baby_phenobarb_pharm, 2, 1) == '1' OR substr(baby_other_pharm, 1, 1) == '1' OR substr(baby_other_pharm, 2, 1) == '1' OR substr(baby_unknown_pharm, 1, 1) == '1' OR substr(baby_unknown_pharm, 2, 1) == '1')  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    clon_meth_morph_pheno_other_unkown_1_2=(results[0][0])
    if clon_meth_morph_pheno_other_unkown_1_2 is not None and aim_pharm_tx_2 != 0 and \
            aim_pharm_tx_2 is not None:
        med_used=(clon_meth_morph_pheno_other_unkown_1_2 / aim_pharm_tx_2)
    else:
        med_used=(None)

    # STAT 19
    cursor.execute(
        "SELECT SUM(baby_aim_calc_los_baby) FROM Child WHERE (baby_gestational_age >= 35 AND baby_nonnas_dx_lengthen_los = 1)  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    sum_aim_calc_los_baby_readmit=(results[0][0])
    cursor.execute(
        "SELECT SUM(baby_calc_los_medreadydc) FROM Child WHERE (baby_gestational_age >= 35 AND baby_nonnas_dx_lengthen_los = 1)  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    sum_calc_los_medreadydc=(results[0][0])
    cursor.execute(
        "SELECT COUNT(baby_id) From Child WHERE (baby_gestational_age >= 35 AND baby_nonnas_dx_lengthen_los = 1)  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    baby_gest_and_nonnas=(results[0][0])
    if sum_aim_calc_los_baby is not None and sum_aim_calc_los_baby is not None and sum_calc_los_medreadydc is not None:
        aim_calc_plus_aim_calc_red_minus_calc_los_med=(
            (sum_aim_calc_los_baby + sum_aim_calc_los_baby) - sum_calc_los_medreadydc)
    else:
        aim_calc_plus_aim_calc_red_minus_calc_los_med=(None)

    if aim_calc_plus_aim_calc_red_minus_calc_los_med is not None and baby_gest_and_nonnas != 0 and \
            baby_gest_and_nonnas is not None:
        avg_diff_discharge=(aim_calc_plus_aim_calc_red_minus_calc_los_med / baby_gest_and_nonnas)
    else:
        avg_diff_discharge=(None)

    # STAT 20
    cursor.execute(
        "SELECT COUNT(baby_id) From Child WHERE baby_gestational_age >= 35 AND (substr(baby_assessment_method, 1, 1) == '1' OR substr(baby_assessment_method, 2, 1) == '1' OR substr(baby_assessment_method, 3, 1) == '1' OR substr(baby_assessment_method, 4, 1) == '1' OR substr(baby_assessment_method, 5, 1) == '1')  AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
             date1, date2))
    results = cursor.fetchall()
    assessment_1_2_3_4_5=(results[0][0])
    if assessment_1_2_3_4_5 is not None and baby_gest != 0 and baby_gest is not None:
        type_assessment=(assessment_1_2_3_4_5 / baby_gest)
    else:
        type_assessment=(None)


    cursor.execute(
        "SELECT COUNT(baby_id) From Child WHERE (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
            date1, date2))
    results = cursor.fetchall()
    record_count = results[0][0]

    statistics = {'num_records': record_count,
                  'measure_1': nas_stay_length, 'measure_2': oens_requiring_pharmacologic_therapy,
                  'measure_3': nas_pharmacological_treatment_days, 'measure_4': oen_nas_symptom,
                  'measure_5': mom_mat_behavioral_treatment, 'measure_6': oens_requiring_pharmacologic_therapy,
                  'measure_7': oen_romming_with_mother_any, 'measure_8': oen_rooming_with_mother_majority,
                  'measure_9': oen_mothers_milk, 'measure_10': biological_mother_discharge,
                  'measure_11': oen_with_discharge_followup, 'measure_12': percent_oen_pcp,
                  'measure_13': percent_inf_sti, 'measure_14': mom_sti_among_oud,
                  'measure_15': mom_prenatal_pediatric_consult_among_oud, 'measure_16': percent_dhs_custody,
                  'measure_17': calc_mme_infant, 'measure_18': med_used,
                  'measure_19': avg_diff_discharge, 'measure_20': type_assessment}
    return statistics

def measure_helper_per_hos_per_quarter(cursor, date1, date2):
    # stat 1
    baby_gest_and_aim_nas = []
    sum_aim_calc_los_baby = []
    nas_stay_length = []
    total_nas_stay_length = []
    # stat 2
    baby_gest = []
    aim_pharm_tx_2 = []
    oens_requiring_pharmacologic_therapy = []
    total_oens_requiring_pharmacologic_therapy = []
    # stat 3
    sum_aim_calc_length_tx = []
    nas_pharmacological_treatment_days = []
    total_nas_pharmacological_treatment_days = []
    # stat 4
    aim_nas_2_3_4_5 = []
    oen_nas_symptom = []
    total_oen_nas_symptom = []
    # stat 5 is woman
    mom_date_deliv_not_null = []
    mom_aim_tx_or_mat_2_3_4 = []
    mom_mat_behavioral_treatment = []
    total_mom_mat_behavioral_treatment = []
    # stat 6
    dhs_referral_1 = []
    dhs_contacted = []
    total_dhs_contacted = []
    # stat 7
    aim_roomin_any_2 = []
    oen_romming_with_mother_any = []
    total_oen_romming_with_mother_any = []
    # stat 8
    aim_romming_50plus = []
    oen_rooming_with_mother_majority = []
    total_oen_rooming_with_mother_majority = []
    # stat 9
    aim_mhm_dc_1_2 = []
    oen_mothers_milk = []
    total_oen_mothers_milk = []
    # stat 10
    aim_placement_dc = []
    biological_mother_discharge = []
    total_biological_mother_discharge = []
    # stat 11
    early_intervention = []
    oen_with_discharge_followup = []
    total_oen_with_discharge_followup = []
    # stat 12
    pcp_appt = []
    percent_oen_pcp = []
    total_percent_oen_pcp = []
    # stat 13 INFANT_STI
    infant_sti = []
    percent_inf_sti = []
    total_percent_inf_sti = []
    # stat 14 woman
    mom_oud_dx_timing_1_2 = []
    mom_hbv_hcv_hiv_rpr_1_2_3 = []
    mom_sti_among_oud = []
    total_mom_sti_among_oud = []
    # stat 15 woman
    mom_nas_consult = []
    mom_prenatal_pediatric_consult_among_oud = []
    total_mom_prenatal_pediatric_consult_among_oud = []
    # stat 16
    dhs_custody = []
    percent_dhs_custody = []
    total_percent_dhs_custody = []
    # stat 17
    baby_calc_mme = []
    sum_baby_calc_mme = []
    calc_mme_infant = []
    total_calc_mme_infant = []
    # stat 18
    clon_meth_morph_pheno_other_unkown_1_2 = []
    med_used = []
    total_med_used = []
    # STAT 19
    baby_gest_and_nonnas = []
    sum_calc_los_medreadydc = []
    sum_aim_calc_los_baby_readmit = []
    aim_calc_plus_aim_calc_red_minus_calc_los_med = []
    avg_diff_discharge = []
    total_avg_diff_discharge = []

    # STAT 20
    assessment_1_2_3_4_5 = []
    type_assessment = []
    total_type_assessment = []

    cursor.execute("SELECT hospital_id From Hospital")
    hos_results = cursor.fetchall()
    hos_ids = []
    for i in range(0, len(hos_results)):
        hospital_id = hos_results[i]
        hos_ids.append(hospital_id[0])
        # stat 1
        cursor.execute(
            "SELECT SUM(baby_aim_calc_los_baby) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_nos_p0414_p961 BETWEEN 2 AND 5) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        sum_aim_calc_los_baby.append(results[0][0])
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_nos_p0414_p961 BETWEEN 2 AND 5) "
            "AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(hospital_id[0], date1,
                                                                                             date2))
        results = cursor.fetchall()
        baby_gest_and_aim_nas.append(results[0][0])
        if sum_aim_calc_los_baby[i] is not None and baby_gest_and_aim_nas[i] is not None and baby_gest_and_aim_nas[
            i] != 0:
            nas_stay_length.append(sum_aim_calc_los_baby[i] / baby_gest_and_aim_nas[i])
        else:
            nas_stay_length.append(None)

        # stat 2
        cursor.execute("SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_aim_pharm_tx == 2 AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
            hospital_id[0], date1, date2))
        results = cursor.fetchall()
        aim_pharm_tx_2.append(results[0][0])
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        baby_gest.append(results[0][0])
        if aim_pharm_tx_2[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            oens_requiring_pharmacologic_therapy.append(aim_pharm_tx_2[i] / baby_gest[i])
        else:
            oens_requiring_pharmacologic_therapy.append(None)

        # stat 3
        cursor.execute(
            "SELECT SUM(baby_aim_calc_length_tx) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_nos_p0414_p961 BETWEEN 2 AND 5) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        sum_aim_calc_length_tx.append(results[0][0])
        if sum_aim_calc_length_tx[i] is not None and baby_gest_and_aim_nas[i] is not None and baby_gest_and_aim_nas[i] != 0:
            nas_pharmacological_treatment_days.append(sum_aim_calc_length_tx[i] / baby_gest_and_aim_nas[i])
        else:
            nas_pharmacological_treatment_days.append(None)

        # stat 4
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_nos_p0414_p961 BETWEEN 2 AND 5) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        aim_nas_2_3_4_5.append(results[0][0])
        if aim_nas_2_3_4_5[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            oen_nas_symptom.append(aim_nas_2_3_4_5[i] / baby_gest[i])
        else:
            oen_nas_symptom.append(None)

        # stat 5 is woman
        cursor.execute(
            "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_date_delivery IS NOT NULL) AND (hospital_id == {}) AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        mom_date_deliv_not_null.append(results[0][0])
        cursor.execute(
            "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_date_delivery IS NOT NULL) AND (maternal_aim_tx_or_mat BETWEEN 2 AND 4) AND (hospital_id == {}) AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        mom_aim_tx_or_mat_2_3_4.append(results[0][0])
        if mom_aim_tx_or_mat_2_3_4[i] is not None and mom_date_deliv_not_null[i] != 0 and mom_date_deliv_not_null[i] is not None:
            mom_mat_behavioral_treatment.append(mom_aim_tx_or_mat_2_3_4[i] / mom_date_deliv_not_null[i])
        else:
            mom_mat_behavioral_treatment.append(None)

        # stat 6
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_dhs_referral == 1 AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        dhs_referral_1.append(results[0][0])
        if dhs_referral_1[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            dhs_contacted.append(dhs_referral_1[i] / baby_gest[i])
        else:
            dhs_contacted.append(None)

        # stat 7
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_aim_roomin_any == 2 AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        aim_roomin_any_2.append(results[0][0])
        if aim_roomin_any_2[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            oen_romming_with_mother_any.append(aim_roomin_any_2[i] / baby_gest[i])
        else:
            oen_romming_with_mother_any.append(None)

        # stat 8
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_aim_rooming_50plus == 2 AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        aim_romming_50plus.append(results[0][0])
        if aim_romming_50plus[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            oen_rooming_with_mother_majority.append(aim_romming_50plus[i] / baby_gest[i])
        else:
            oen_rooming_with_mother_majority.append(None)

        # stat 9
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_mhm_dc BETWEEN 1 AND 2) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        aim_mhm_dc_1_2.append(results[0][0])
        if aim_mhm_dc_1_2[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            oen_mothers_milk.append(aim_mhm_dc_1_2[i] / baby_gest[i])
        else:
            oen_mothers_milk.append(None)

        # stat 10
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_aim_placement_dc BETWEEN 1 AND 2) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        aim_placement_dc.append(results[0][0])
        if aim_placement_dc[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            biological_mother_discharge.append(aim_placement_dc[i] / baby_gest[i])
        else:
            biological_mother_discharge.append(None)

        # stat 11
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_early_intervention IN (1,2,4,6)) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        early_intervention.append(results[0][0])
        if early_intervention[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            oen_with_discharge_followup.append(early_intervention[i] / baby_gest[i])
        else:
            oen_with_discharge_followup.append(None)

        # stat 12
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_pcp_appt BETWEEN 2 AND 4) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        pcp_appt.append(results[0][0])
        if pcp_appt[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            percent_oen_pcp.append(pcp_appt[i] / baby_gest[i])
        else:
            percent_oen_pcp.append(None)

        # stat 13 # INFANT_STI
        # NOTE, pdf says get infant_sti == 2,3,4,5 but it is zero index from 0-5 so add one to get 3,4,5,6 as its stored in memory as 1-6
        cursor.execute(
            "SELECT COUNT(baby_id) From Child WHERE baby_gestational_age >= 35 AND (substr(baby_infant_sti, 3, 1) == '1' OR substr(baby_infant_sti, 4, 1) == '1' OR substr(baby_infant_sti, 5, 1) == '1' OR substr(baby_infant_sti, 6, 1) == '1') AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        infant_sti.append(results[0][0])
        if infant_sti[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            percent_inf_sti.append(infant_sti[i] / baby_gest[i])
        else:
            percent_inf_sti.append(None)
        # stat 14 WOMAN
        cursor.execute(
            "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_oud_dx_timing BETWEEN 1 AND 2) AND ((maternal_hbv_test BETWEEN 1 AND 3) OR (maternal_hcv_test BETWEEN 1 AND 3) OR (maternal_hiv_test BETWEEN 1 AND 3) OR (maternal_rpr_test BETWEEN 1 AND 3)) AND (hospital_id == {}) AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        mom_hbv_hcv_hiv_rpr_1_2_3.append(results[0][0])
        cursor.execute(
            "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_oud_dx_timing BETWEEN 1 AND 2) AND (hospital_id == {}) AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        mom_oud_dx_timing_1_2.append(results[0][0])
        if mom_hbv_hcv_hiv_rpr_1_2_3[i] is not None and mom_oud_dx_timing_1_2[i] != 0 and mom_oud_dx_timing_1_2[i] is not None:
            mom_sti_among_oud.append(mom_hbv_hcv_hiv_rpr_1_2_3[i] / mom_oud_dx_timing_1_2[i])
        else:
            mom_sti_among_oud.append(None)
        # stat 15 woman
        cursor.execute(
            "SELECT COUNT(maternal_id) FROM Mother WHERE (maternal_date_delivery IS NOT NULL) AND (maternal_nas_consult BETWEEN 2 AND 3) AND (hospital_id == {}) AND (maternal_date_delivery BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        mom_nas_consult.append(results[0][0])
        if mom_nas_consult[i] is not None and mom_date_deliv_not_null[i] != 0 and mom_date_deliv_not_null[i] is not None:
            mom_prenatal_pediatric_consult_among_oud.append(mom_nas_consult[i] / mom_date_deliv_not_null[i])
        else:
            mom_prenatal_pediatric_consult_among_oud.append(None)
        # stat 16
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND (baby_dhs_custody IN (2,4,5,6)) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        dhs_custody.append(results[0][0])
        if dhs_custody[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            percent_dhs_custody.append(dhs_custody[i] / baby_gest[i])
        else:
            percent_dhs_custody.append(None)
        # stat 17
        cursor.execute(
            "SELECT SUM(baby_calc_mme_infant) FROM Child WHERE baby_gestational_age >= 35 AND baby_calc_mme_infant IS NOT NULL AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        sum_baby_calc_mme.append(results[0][0])
        cursor.execute(
            "SELECT COUNT(baby_id) FROM Child WHERE baby_gestational_age >= 35 AND baby_calc_mme_infant IS NOT NULL AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        baby_calc_mme.append(results[0][0])
        if sum_baby_calc_mme[i] is not None and baby_calc_mme[i] != 0 and baby_calc_mme[i] is not None:
            calc_mme_infant.append(sum_baby_calc_mme[i] / baby_calc_mme[i])
        else:
            calc_mme_infant.append(None)

        # stat 18
        cursor.execute(
            "SELECT COUNT(baby_id) From Child WHERE baby_aim_pharm_tx == 2 AND (substr(baby_clonidine_pharm, 1, 1) == '1' OR substr(baby_clonidine_pharm, 2, 1) == '1' OR substr(baby_methadone_pharm, 1, 1) == '1' OR substr(baby_methadone_pharm, 2, 1) == '1' OR substr(baby_morphine_pharm, 1, 1) == '1' OR substr(baby_morphine_pharm, 2, 1) == '1' OR substr(baby_phenobarb_pharm, 1, 1) == '1' OR substr(baby_phenobarb_pharm, 2, 1) == '1' OR substr(baby_other_pharm, 1, 1) == '1' OR substr(baby_other_pharm, 2, 1) == '1' OR substr(baby_unknown_pharm, 1, 1) == '1' OR substr(baby_unknown_pharm, 2, 1) == '1') AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        clon_meth_morph_pheno_other_unkown_1_2.append(results[0][0])
        if clon_meth_morph_pheno_other_unkown_1_2[i] is not None and aim_pharm_tx_2[i] != 0 and \
                aim_pharm_tx_2[i] is not None:
            med_used.append(clon_meth_morph_pheno_other_unkown_1_2[i] / aim_pharm_tx_2[i])
        else:
            med_used.append(None)

        # STAT 19
        cursor.execute(
            "SELECT SUM(baby_aim_calc_los_baby) FROM Child WHERE (baby_gestational_age >= 35 AND baby_nonnas_dx_lengthen_los = 1) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        sum_aim_calc_los_baby_readmit.append(results[0][0])
        cursor.execute(
            "SELECT SUM(baby_calc_los_medreadydc) FROM Child WHERE (baby_gestational_age >= 35 AND baby_nonnas_dx_lengthen_los = 1) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        sum_calc_los_medreadydc.append(results[0][0])
        cursor.execute(
            "SELECT COUNT(baby_id) From Child WHERE (baby_gestational_age >= 35 AND baby_nonnas_dx_lengthen_los = 1) AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        baby_gest_and_nonnas.append(results[0][0])
        if sum_aim_calc_los_baby[i] is not None and sum_aim_calc_los_baby[i] is not None and sum_calc_los_medreadydc[i] is not None:
            aim_calc_plus_aim_calc_red_minus_calc_los_med.append(
                (sum_aim_calc_los_baby[i] + sum_aim_calc_los_baby[i]) - sum_calc_los_medreadydc[i])
        else:
            aim_calc_plus_aim_calc_red_minus_calc_los_med.append(None)

        if aim_calc_plus_aim_calc_red_minus_calc_los_med[i] is not None and baby_gest_and_nonnas[i] != 0 and \
                baby_gest_and_nonnas[i] is not None:
            avg_diff_discharge.append(aim_calc_plus_aim_calc_red_minus_calc_los_med[i] / baby_gest_and_nonnas[i])
        else:
            avg_diff_discharge.append(None)

        # STAT 20
        cursor.execute(
            "SELECT COUNT(baby_id) From Child WHERE baby_gestational_age >= 35 AND (substr(baby_assessment_method, 1, 1) == '1' OR substr(baby_assessment_method, 2, 1) == '1' OR substr(baby_assessment_method, 3, 1) == '1' OR substr(baby_assessment_method, 4, 1) == '1' OR substr(baby_assessment_method, 5, 1) == '1') AND (hospital_id == {}) AND (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                hospital_id[0], date1, date2))
        results = cursor.fetchall()
        assessment_1_2_3_4_5.append(results[0][0])
        if assessment_1_2_3_4_5[i] is not None and baby_gest[i] != 0 and baby_gest[i] is not None:
            type_assessment.append(assessment_1_2_3_4_5[i] / baby_gest[i])
        else:
            type_assessment.append(None)

    cursor.execute(
        "SELECT COUNT(baby_id) From Child WHERE (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
            date1, date2))
    results = cursor.fetchall()
    record_count = results[0][0]

    statistics = {'hospital_id': hos_ids,
                  'num_records': record_count,
                  'measure_1': nas_stay_length, 'measure_2': oens_requiring_pharmacologic_therapy,
                  'measure_3': nas_pharmacological_treatment_days, 'measure_4': oen_nas_symptom,
                  'measure_5': mom_mat_behavioral_treatment, 'measure_6': oens_requiring_pharmacologic_therapy,
                  'measure_7': oen_romming_with_mother_any, 'measure_8': oen_rooming_with_mother_majority,
                  'measure_9': oen_mothers_milk, 'measure_10': biological_mother_discharge,
                  'measure_11': oen_with_discharge_followup, 'measure_12': percent_oen_pcp,
                  'measure_13': percent_inf_sti, 'measure_14': mom_sti_among_oud,
                  'measure_15': mom_prenatal_pediatric_consult_among_oud, 'measure_16': percent_dhs_custody,
                  'measure_17': calc_mme_infant, 'measure_18': med_used,
                  'measure_19': avg_diff_discharge, 'measure_20': type_assessment}
    return statistics


def get_measures():
    debug = False
    connection = sqlite3.connect("/home/ubuntu/capstone/records.db")
    cursor = connection.cursor()
    current_year = datetime.now().year
    num_quarter = 4
    current_month = datetime.now().month // num_quarter + 1
    start_year = 2020
    num_years = current_year - start_year
    all_statistics = {}
    for i in range(0, num_years+1):
        prev_month = 0
        all_statistics["{}".format(start_year+i)] = measure_helper_all_hos_per_quarter(cursor,
                                                                                       "{}-01-01".format(start_year + i),
                                                                                       "{}-01-01".format(start_year + 1 +i))
        for j in range(1, num_quarter+1):
            if i < num_years:
                if j == 1:
                    start_month = "01"
                else:
                    start_month = prev_month
                end_month = int(int(prev_month) + (12 / num_quarter)) % 12
                if end_month > 9:
                    end_month = str(end_month)
                else:
                    end_month = "0"+str(end_month)
                if j == 1:
                    end_month = "0"+str(int(end_month)+1)
                prev_month = end_month
                if debug:
                    print("Start: "+"{}-{}-01".format(start_year+i, start_month))

                if j == num_quarter:
                    if debug:
                        print("End: " + "{}-{}-01".format(start_year + i+1, end_month))
                    all_statistics["{}Q{}".format(start_year + i, j)] = measure_helper_per_hos_per_quarter(cursor,
                                                                                       "{}-{}-01".format(start_year + i,
                                                                                                         start_month),
                                                                                       "{}-{}-01".format(start_year + 1 +i,
                                                                                                     end_month))

                    temp = measure_helper_all_hos_per_quarter(cursor,"{}-{}-01".format(start_year + i,start_month),
                                                              "{}-{}-01".format(start_year + 1 +i, end_month))
                    all_statistics["{}Q{}".format(start_year + i, j)]['total'] = []
                    for k in range(1, 21):
                        all_statistics["{}Q{}".format(start_year + i, j)]['total'].append(temp["measure_{}".format(k)])

                    if debug:
                        print("Records Contained: ")
                        print(cursor.execute(
                            "SELECT baby_aim_infant_dob from Child WHERE (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                                "{}-{}-01".format(start_year + i,
                                                  start_month), "{}-{}-01".format(start_year + i+1,
                                                                                  end_month))).fetchall())
                else:
                    if debug:
                        print("End: " + "{}-{}-01".format(start_year + i, end_month))
                    all_statistics["{}Q{}".format(start_year + i, j)] = measure_helper_per_hos_per_quarter(cursor,
                                                                                       "{}-{}-01".format(start_year + i,
                                                                                                         start_month),
                                                                                       "{}-{}-01".format(start_year + i,
                                                                                                         end_month))

                    temp = measure_helper_all_hos_per_quarter(cursor,"{}-{}-01".format(start_year + i,start_month),
                                                                                       "{}-{}-01".format(start_year + i,
                                                                                                         end_month))
                    all_statistics["{}Q{}".format(start_year + i, j)]['total'] = []
                    for k in range(1, 21):
                        all_statistics["{}Q{}".format(start_year + i, j)]['total'].append(temp["measure_{}".format(k)])

                    if debug:
                        print("Records Contained: ")
                        print(cursor.execute(
                            "SELECT baby_aim_infant_dob from Child WHERE (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                                "{}-{}-01".format(start_year + i,
                                                  start_month), "{}-{}-01".format(start_year + i,
                                                                                  end_month))).fetchall())
            else:
                if j <= current_month:
                    if j == 1:
                        start_month = "01"
                    else:
                        start_month = prev_month
                    end_month = int(int(prev_month) + (12 / num_quarter)) % 12
                    if end_month > 9:
                        end_month = str(end_month)
                    else:
                        end_month = "0" + str(end_month)
                    if j == 1:
                        end_month = "0" + str(int(end_month) + 1)
                    prev_month = end_month
                    if debug:
                        print("Start: " + "{}-{}-01".format(start_year + i, start_month))

                    if j == num_quarter:
                        if debug:
                            print("End: " + "{}-{}-01".format(start_year + i + 1, end_month))
                        all_statistics["{}Q{}".format(start_year + i, j)] = measure_helper_per_hos_per_quarter(cursor,
                                                                                           "{}-{}-01".format(
                                                                                               start_year + i,
                                                                                               start_month),
                                                                                           "{}-{}-01".format(
                                                                                               start_year + 1 + i,
                                                                                               end_month))

                        temp = measure_helper_all_hos_per_quarter(cursor,"{}-{}-01".format(start_year + i,
                                                                                               start_month),
                                                                                           "{}-{}-01".format(
                                                                                               start_year + 1 + i,
                                                                                               end_month))
                        all_statistics["{}Q{}".format(start_year + i, j)]['total'] = []
                        for k in range(1, 21):
                            all_statistics["{}Q{}".format(start_year + i, j)]['total'].append(
                                temp["measure_{}".format(k)])

                        if debug:
                            print("Records Contained: ")
                            print(cursor.execute(
                                "SELECT baby_aim_infant_dob from Child WHERE (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                                    "{}-{}-01".format(start_year + i,
                                                      start_month), "{}-{}-01".format(start_year + i + 1,
                                                                                      end_month))).fetchall())
                    else:
                        if debug:
                            print("End: " + "{}-{}-01".format(start_year + i, end_month))
                        all_statistics["{}Q{}".format(start_year + i, j)] = measure_helper_per_hos_per_quarter(cursor,
                                                                                           "{}-{}-01".format(
                                                                                               start_year + i,
                                                                                               start_month),
                                                                                           "{}-{}-01".format(
                                                                                               start_year + i,
                                                                                               end_month))

                        temp = measure_helper_all_hos_per_quarter(cursor,"{}-{}-01".format(start_year + i,
                                                                                               start_month),
                                                                                           "{}-{}-01".format(
                                                                                               start_year + i,
                                                                                               end_month))
                        all_statistics["{}Q{}".format(start_year + i, j)]['total'] = []
                        for k in range(1, 21):
                            all_statistics["{}Q{}".format(start_year + i, j)]['total'].append(
                                temp["measure_{}".format(k)])

                        if debug:
                            print("Records Contained: ")
                            print(cursor.execute(
                                "SELECT baby_aim_infant_dob from Child WHERE (baby_aim_infant_dob BETWEEN '{}' AND '{}')".format(
                                    "{}-{}-01".format(start_year + i,
                                                      start_month), "{}-{}-01".format(start_year + i,
                                                                                      end_month))).fetchall())
                else:
                    all_statistics["{}Q{}".format(start_year+i,j)] = None



    cursor.close()
    connection.close()
    statistics_json = json.dumps(all_statistics)
    if debug:
        for stat in all_statistics:
            print(stat)
            print(all_statistics[stat])
    return statistics_json


stat = get_measures()
print(stat)
