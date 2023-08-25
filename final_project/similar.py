def pro_player(df, GPM, VSPM, DPM, KP, XPD):
    min_mse = float('inf')
    similar_player = None
    char_pro = None
    GPM_pro = None
    DPM_pro = None
    VSPM_pro = None
    KP_pro = None
    XPD_pro = None

    for play in df:
            mse_sum = ((play["GPM"] - GPM) ** 2 + 
                    (play["VSPM"] - VSPM) ** 2 +
                    (play["DPM"] - DPM) ** 2 + 
                    (play["KP"] - KP) ** 2 + 
                    (play["XPD"] - XPD) ** 2)

            if mse_sum < min_mse:
                min_mse = mse_sum
                similar_player = play["Player"]
                char_pro = play["Champion"]
                GPM_pro = play["GPM"]
                DPM_pro = play["DPM"]
                VSPM_pro = play["VSPM"]
                KP_pro = play['KP']
                XPD_pro = play["XPD"]
                
                
                
    
    

    return similar_player, char_pro, GPM_pro, VSPM_pro, DPM_pro, KP_pro, XPD_pro