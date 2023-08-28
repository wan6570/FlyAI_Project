def pro_player(df, GPM, VSPM, DPM, KP, XPD):
    min_mse = float('inf')
    similar_player = None
    char_pro = None
    GPM_pro = None
    DPM_pro = None
    VSPM_pro = None
    KP_pro = None
    XPD_pro = None

    GPM_weight = 1
    VSPM_weight = 1
    DPM_weight = 1
    KP_weight = 1
    XPD_weight = 1

    for play in df:
            pro_gpm = play["GPM"] ** GPM_weight
            pro_vspm = play["VSPM"] ** VSPM_weight
            pro_dpm = play["DPM"] ** DPM_weight
            pro_kp = play["KP"] ** KP_weight
            pro_xpd = play["XPD"] ** XPD_weight

            print(pro_gpm, pro_vspm, pro_dpm, pro_kp, pro_xpd)
            print(GPM, VSPM, DPM, KP, XPD)
            mse_sum = ((pro_gpm - GPM) ** 2 + (pro_vspm - VSPM) ** 2 + (pro_dpm - DPM) ** 2 + (pro_kp - KP) ** 2 + (pro_xpd - XPD) ** 2)
            print(mse_sum)
            #mse_lst.append((play['Player'], gpm_dif, vspm_dif, dpm_dif, kp_dif, xpd_dif, mse_sum))        
            if mse_sum < min_mse:
                min_mse = mse_sum
                similar_player = play["Player"]
                print(f'Similar.py!!! : similar_player = {similar_player}')
                char_pro = play["Champion"]
                GPM_pro = pro_gpm 
                DPM_pro = pro_dpm
                VSPM_pro = pro_vspm
                KP_pro = pro_kp
                XPD_pro = pro_xpd
                
                
                
    # print(mse_lst)
    

    return similar_player, char_pro, GPM_pro, VSPM_pro, DPM_pro, KP_pro, XPD_pro