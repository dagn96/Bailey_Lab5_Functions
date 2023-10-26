def fit_velocity_file(df):
    # Get the site name from the file name
    # site = filename.split('/')[-1].split('_')[0]
    site = str(df['site'][0])
    coeffs_E = np.polyfit(df['yyyy.yyyy'], df['__east(m)'], 1)
    coeffs_N = np.polyfit(df['yyyy.yyyy'], df['_north(m)'], 1)
    coeffs_U = np.polyfit(df['yyyy.yyyy'], df['____up(m)'], 1)
    sigma_E = np.polyfit(df['yyyy.yyyy'], df['sig_e(m)'], 1)
    sigma_N = np.polyfit(df['yyyy.yyyy'], df['sig_n(m)'], 1)
    sigma_U = np.polyfit(df['yyyy.yyyy'], df['sig_u(m)'], 1)
    return site, coeffs_E[0], coeffs_N[0], coeffs_U[0], sigma_E[0], sigma_N[0], sigma_U[0]
    
def coordinates(df):
    lat = np.average(df['_latitude(deg)'])
    lon = np.average(df['_longitude(deg)'])
    elev = np.average(df['__height(m)'])
    return lat, lon, elev
    
def fit_velocity(tlist, ylist):
    coeffs_E = np.polyfit(df['yyyy.yyyy'], df['__east(m)'], 1)
    coeffs_N = np.polyfit(df['yyyy.yyyy'], df['_north(m)'], 1)
    coeffs_U = np.polyfit(df['yyyy.yyyy'], df['____up(m)'], 1)
    sigma_E = np.polyfit(df['yyyy.yyyy'], df['sig_e(m)'], 1)
    sigma_N = np.polyfit(df['yyyy.yyyy'], df['sig_n(m)'], 1)
    sigma_U = np.polyfit(df['yyyy.yyyy'], df['sig_u(m)'], 1)
    return coeffs_E, coeffs_N, coeffs_U, sigma_E, sigma_N, sigma_U
    
def fit_tide_gauge(df):
    df.drop(df.loc[df[1]==-99999].index, inplace=True)
    sealvl_rate = np.polyfit(df[0], df[1], 1)
    return sealvl_rate[0]

# def fit_sealvl_rate(tlist, ylist):
#     sealvl_rate = np.polyfit(df[0], df[1], 1)
#     return sealvl_rate
    
def fit_all_files(folder,pattern,data_type):
    all_gnss_files = glob.glob(folder+'/'+pattern)
    if data_type=="GNSS":
        sites=np.array([])
        lons=np.array([])
        lats=np.array([])
        elevs=np.array([])
        v_E=np.array([])
        v_N=np.array([])
        v_U=np.array([])
        sig_E=np.array([])
        sig_N=np.array([])
        sig_U=np.array([])
        for i in all_gnss_files:
            GPS = pd.read_csv(i,  delim_whitespace=True)
            site, E, N, U, sigma_E, sigma_N, sigma_U =fit_velocity_file(GPS)
            lat,lon, elev =coordinates(GPS)
            sites=np.append(sites,site)
            lons=np.append(lons,lon)
            lats=np.append(lats,lat)
            elevs=np.append(elevs,elev)
            v_E=np.append(v_E,E)
            v_N=np.append(v_N,N)
            v_U=np.append(v_U,U)
            sig_E=np.append(sig_E,sigma_E)
            sig_N=np.append(sig_N,sigma_N)
            sig_U=np.append(sig_U,sigma_U)
        out_dict={'site':sites,'longitude':lons, 'latitude':lats,'elevation':elevs, 'velocity_e':v_E,'velocity_n':v_N, 'velocity_u':v_U, 'sigma_E':sig_E,'sigma_N':sig_N, 'sigma_U':sig_U}
        out_df = pd.DataFrame(data=out_dict)
        return out_df


    elif data_type=="TIDE":
        sealvl_timeseries_files = glob.glob(folder+'/'+pattern)
        rates=np.array([])
        sites=np.array([])
        for i in sealvl_timeseries_files:
            tide = pd.read_csv(i, sep=';',header=None)
            site = i.split('.')[0].split('\\')[1]
            sealvl_rate = fit_tide_gauge(tide)
            sites=np.append(sites,site)
            rates=np.append(rates,sealvl_rate)
            tide_out_dict = {'site':sites,'rate':rates}
            tide_out_df = pd.DataFrame(data=tide_out_dict)
        return tide_out_df


sealvl_df = fit_all_files('Monthly Sea Level Timeseries','*',data_type='TIDE')
velocity_df = fit_all_files('timeseries','*',data_type='GNSS')

display(sealvl_df)
display(velocity_df)