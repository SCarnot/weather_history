import pandas as pd
import utils
import os

main_url = 'https://www.infoclimat.fr/climatologie-mensuelle/07156/{0}/{1}/paris-montsouris.html'
df_data = pd.DataFrame(columns=['year', 'month', 'day', 't_min', 't_max', 'rain'])

yr_start = 2001
yr_stop = 2003

if __name__ == '__main__':

    #Create dump file if not created (not tracked by git)
    if not os.path.exists('../data/'):
        os.makedirs('../data/')

    for yr in range(yr_start,yr_stop+1,1):
        print('Year:',yr)
        for mh in range(1,13,1):
            
            df_data = df_data.append(utils.monthly_data(yr, mh, main_url))

        file_name = '../data/' + 'data_paris_montsouris.csv'
        df_data.to_csv(file_name)
