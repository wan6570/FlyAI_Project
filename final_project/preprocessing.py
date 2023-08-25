def normarization(average, GPM, VSPM, DPM, KP, XPD):
    GPM_pre = average[0]['GPM']
    VSPM_pre = average[0]['VSPM']
    DPM_pre = average[0]['DPM']
    KP_pre = average[0]['KP']
    XPD_pre = average[0]['XPD']
    
    GPM_user = GPM / GPM_pre
    VSPM_user = VSPM / VSPM_pre
    DPM_user = DPM / DPM_pre
    KP_user = KP / KP_pre
    XPD_user = (XPD + 10000) /XPD_pre

    return GPM_user, VSPM_user, DPM_user, KP_user, XPD_user